#!/usr/bin/env python
# -*- coding:utf-8 -*-
import inspect
import traceback
from collections.abc import Callable
from datetime import datetime
from functools import wraps
from inspect import getfullargspec
from pathlib import Path
from time import sleep
from typing import Optional, Union, Any
from urllib.parse import urlparse

from hyper.contrib import HTTP20Adapter
from requests import Response, Session
from urllib3 import Retry

from . import RestOptions, HttpMethod, RestResponse, RestFul, Hooks, _utils, BaseRest, ApiAware, \
    BaseContext
from . import StatsSentUrl
from ._constants import _OPTIONAL_ARGS_KEYS, _Constant, _HTTP_INFO_TEMPLATE
from ._meta import _RequestMeta
from .. import sjson as complexjson
from ..character import StringBuilder
from ..config.log import LogLevel
from ..config.rest import RestConfig
from ..converter import TimeUnit
from ..exceptions import HttpException, RestInternalException
from ..generic import T
from ..log import LoggerFactory
from ..serialize import Serializable, serializer
from ..utils.objects import ObjectsUtils
from ..utils.strings import StringUtils

__all__ = []

_LOGGER = LoggerFactory.get_logger("rest")


class RestContext(BaseContext):

    def __init__(self):
        self.__context = {}

    def put(self, **kwargs: BaseRest):
        self.__context.update(kwargs)

    def update(self, rests: dict[str, BaseRest]):
        self.__context.update(rests or {})

    def get(self, tag, default: BaseRest = None) -> BaseRest:
        return self.__context.setdefault(tag, default)

    def pop(self, tag) -> BaseRest:
        return self.__context.pop(tag)


class RestFast(object):
    """
    Quickly build a streaming HTTP request client.
    """

    def __init__(self, host, http2: bool = False, retry_times: int = 3, retry_backoff_factor: int = 5,
                 trust_env: bool = True, max_redirects: int = 30, **kwargs):
        self.__host: str = host
        self.__api: str = ""
        self.__opts: RestOptions = RestOptions()
        self.__method: HttpMethod = HttpMethod.OPTIONS
        self.__kw = kwargs
        self.__session: Session = Session()
        self.__session.trust_env = trust_env
        self.__session.max_redirects = max_redirects
        self.__resp: Optional[Response] = None
        retry = Retry(total=retry_times, backoff_factor=retry_backoff_factor)
        if http2:
            scheme = urlparse(self.__host).scheme
            if scheme != _Constant.HTTPS:
                raise HttpException(f"http2 need https protocol, but found '{scheme}'")
            self.__session.mount(f"{_Constant.HTTPS}://", HTTP20Adapter(max_retries=retry))

    def api(self, api: str) -> 'RestFast':
        """
        set server api
        """
        self.__api = api if api else ""
        return self

    def opts(self, opts: RestOptions) -> 'RestFast':
        """
        http request params, headers, data, json, files etc.
        """
        self.__opts = opts if opts else RestOptions()
        return self

    def method(self, method: Union[HttpMethod, str]) -> 'RestFast':
        """
        set http request method.
        """
        if isinstance(method, str):
            self.__method = HttpMethod.get_by_value(method.upper())
        elif isinstance(method, HttpMethod):
            self.__method = method
        else:
            raise HttpException(f"invalid http method: '{method}'")
        if not self.__method:
            raise HttpException(f"invalid http method: '{method}'")
        return self

    def send(self) -> 'RestFast':
        """
        send http request
        :return:
        """
        if StringUtils.is_empty(self.__api):
            _LOGGER.warning(f'api is empty')
        url = f"{self.__host}{self.__api}"
        self.__resp = None
        try:
            self.__resp = getattr(self.__session, self.__method.value.lower())(url=f"{url}",
                                                                               **self.__opts.opts_no_none, **self.__kw)
            return self
        finally:
            if self.__resp is not None:
                content = self.__resp.text if self.__resp else ""
                url_ = self.__resp.url if self.__resp.url else url
                msg = f"http fast request: url={url_}, method={self.__method}, " \
                      f"opts={self.__opts.opts_no_none}, response={StringUtils.abbreviate(content)}"
                _LOGGER.log(level=10, msg=msg, stacklevel=3)
            else:
                msg = f"http fast request no response: url={self.__host}{self.__api}, method={self.__method}, " \
                      f"opts={self.__opts.opts_no_none}"
                _LOGGER.log(level=10, msg=msg, stacklevel=3)
            self.__api = ""
            self.__opts = RestOptions()
            self.__method = HttpMethod.OPTIONS.value

    def response(self) -> RestResponse:
        """
        send request and get response.
        type_reference priority is greater than only_body.
        type_reference will return custom entity object.

        usage:
            type_reference example:

                @EntityType()
                class Data(Entity):
                    id: list[str]
                    OK: str
                    data: str

            response body:
                {"data":"data content","id":[1],"OK":"200"}



            resp = RestFast("http://localhost:8080").api("/hello").opts(RestOptions(params={"id": 1})).method("GET").send().response().to_entity(Data)
            print(resp)  # Data(id=[1], OK='200', data='data content')
        """
        return RestResponse(self.__resp)

    @staticmethod
    def bulk(content: str) -> dict:
        return RestWrapper.bulk(content)


class RestWrapper:
    """
    A simple http request frame.
    """

    def __init__(self, tag=None, rest: BaseRest = None, file: str = None, server_list: list = None,
                 server_name: str = None, host: str = None,
                 headers: dict or Serializable = None, cookies: dict or Serializable = None,
                 auth: tuple or Serializable = None, hooks: Hooks = None, show_len: int = None,
                 http2: bool = False, check_status: bool = False, encoding: str = "utf-8", description: str = None,
                 restful: dict or Serializable = None, retry_times: int = 10, retry_interval: int = 5,
                 retry_exit_code_range: list = None, retry_exception_retry: bool = True,
                 retry_check_handler: Callable[[Any], bool] = None, verify: bool = None,
                 proxies: dict or Serializable = None, cert: str or tuple or Serializable = None,
                 trust_env: bool = True, max_redirects: int = 30, stats: bool = False):
        """
            def retry(times: int = 10, interval: int = 5, exit_code_range: list = None, exception_retry: bool = True,
              check_handler: Callable[[Any], bool] = None) -> T:
        Build a request client.
        :param file: The path where the interface configuration file is stored.
                     configuration format：
                        [
                          {
                            "serverName": "s1",
                            "serverHost": "http://localhost1",
                            "desc": "",
                            "apis": [
                              {
                                "apiName": "user",
                                "apiPath": "/user",
                                "httpMethod": "post",
                                "headers": {"Content-type": "multipart/form-data"},
                                "desc": ""
                              }
                            ]
                          },
                          {
                            "serverName": "s2",
                            "serverHost": "http://localhost2",
                            "desc": "",
                            "apis": [
                              {
                                "apiName": "admin",
                                "apiPath": "/admin",
                                "httpMethod": "get",
                                "desc": ""
                              }
                            ]
                          }
                        ]
        :param server_name: Service name, which allows you to read interface information from the interface
        configuration file.
        """
        self.__tag = tag
        if isinstance(rest, BaseRest):
            self.__rest = rest
        else:
            self.__rest = Rest(file=file, server_list=server_list, server_name=server_name, host=host, headers=headers,
                               cookies=cookies, auth=auth, hooks=hooks, check_status=check_status, encoding=encoding,
                               description=description, restful=restful, http2=http2, retry_times=retry_times,
                               retry_interval=retry_interval, retry_exit_code_range=retry_exit_code_range,
                               show_len=show_len,
                               retry_exception_retry=retry_exception_retry, retry_check_handler=retry_check_handler,
                               verify=verify, proxies=proxies, cert=cert, trust_env=trust_env,
                               max_redirects=max_redirects,
                               stats=stats)
        self.__rest_ = None

    @property
    def rest(self) -> BaseRest:
        return self.__rest

    @rest.setter
    def rest(self, rest: BaseRest):
        if not isinstance(rest, BaseRest):
            raise TypeError(f"Expected type is '{BaseRest.__name__}', got a '{type(rest).__name__}'")
        self.__rest_ = rest

    @property
    def tag(self) -> str:
        return self.__tag

    def retry(self, times: int = None, interval: int = None, exit_code_range: list = None, exception_retry: bool = None,
              check_handler: Callable[[Any], bool] = None) -> T:
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__get_rest(func, args)
                times_ = times if isinstance(times, int) else self.__rest_.retry_times
                interval_ = interval if isinstance(interval, int) else self.__rest_.retry_interval
                exit_code_range_ = exit_code_range if isinstance(exit_code_range,
                                                                 list) else self.__rest_.retry_exit_code_range
                ObjectsUtils.check_iter_type(exit_code_range_, int)
                exception_retry_ = exception_retry if isinstance(exception_retry,
                                                                 bool) else self.__rest_.retry_exception_retry
                check_handler_ = check_handler if callable(check_handler) else self.__rest_.retry_check_handler

                def default_check_body_call_back(res) -> bool:
                    if isinstance(res, RestResponse):
                        return res.code in exit_code_range_
                    else:
                        return True

                check_handler_ = check_handler_ if callable(check_handler_) else default_check_body_call_back
                number_ = times_ + 1
                for i in range(1, times_ + 2):
                    # noinspection PyBroadException
                    try:
                        resp = func(*args, **kwargs)
                        if check_handler_(resp):
                            return resp
                        if i == number_:
                            break
                        else:
                            _LOGGER.log(level=30, msg=f"http request retry times: {i}", stacklevel=3)
                            sleep(interval_)
                    except BaseException as e:
                        if isinstance(e, RestInternalException):
                            if exception_retry_:
                                if i == number_:
                                    break
                                else:
                                    _LOGGER.log(level=30, msg=f"http request retry times: {i}", stacklevel=3)
                                    sleep(interval_)
                            else:
                                return
                        else:
                            raise e
                else:
                    _LOGGER.log(level=40, msg=f"The maximum '{times_}' of HTTP request retries is reached",
                                stacklevel=3)

            return __wrapper

        return __inner

    def request(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
                method: HttpMethod or str = None, allow_redirection: bool = RestConfig.allow_redirection,
                headers: dict = None, check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
                description: str = None, restful: RestFul = None, stats: bool = True,
                hooks: Hooks = None, show_len: int = None) -> T:
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api_name=api_name, server_name=server_name,
                               host=host, api=api,
                               method=method, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, description=description, restful=restful,
                               stats=stats, hooks=hooks, show_len=show_len,
                               opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def get(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
            allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
            restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None) -> T:
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api_name=api_name, server_name=server_name,
                               host=host, api=api,
                               method=HttpMethod.GET, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, description=description, restful=restful,
                               stats=stats, hooks=hooks, show_len=show_len,
                               opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def post(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
             allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             description: str = None, restful: RestFul = None, stats: bool = True,
             hooks: Hooks = None, show_len: int = None) -> T:
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api_name=api_name, server_name=server_name,
                               host=host, api=api,
                               method=HttpMethod.POST, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, description=description, restful=restful,
                               stats=stats, hooks=hooks, show_len=show_len,
                               opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def put(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
            allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
            restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None) -> T:
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api_name=api_name, server_name=server_name,
                               host=host, api=api,
                               method=HttpMethod.PUT, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, description=description, restful=restful,
                               stats=stats, hooks=hooks, show_len=show_len,
                               opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def delete(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
               allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
               check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
               description: str = None, restful: RestFul = None, stats: bool = True,
               hooks: Hooks = None, show_len: int = None) -> T:
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api_name=api_name, server_name=server_name,
                               host=host, api=api,
                               method=HttpMethod.DELETE, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, description=description, restful=restful,
                               stats=stats, hooks=hooks, show_len=show_len,
                               opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def patch(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
              allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
              check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
              description: str = None, restful: RestFul = None, stats: bool = True,
              hooks: Hooks = None, show_len: int = None) -> T:
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api_name=api_name, server_name=server_name,
                               host=host, api=api,
                               method=HttpMethod.PATCH, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, description=description, restful=restful,
                               stats=stats, hooks=hooks, show_len=show_len,
                               opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def head(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
             allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             description: str = None, restful: RestFul = None, stats: bool = True,
             hooks: Hooks = None, show_len: int = None) -> T:
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api_name=api_name, server_name=server_name,
                               host=host, api=api,
                               method=HttpMethod.HEAD, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, description=description, restful=restful,
                               stats=stats, hooks=hooks, show_len=show_len,
                               opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def options(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
                allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
                check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
                description: str = None, restful: RestFul = None, stats: bool = True,
                hooks: Hooks = None, show_len: int = None) -> T:
        def __inner(func):
            @wraps(func)
            def __wrapper(*args, **kwargs):
                self.__request(func=func, args=args, kwargs=kwargs, api_name=api_name, server_name=server_name,
                               host=host, api=api,
                               method=HttpMethod.OPTIONS, allow_redirection=allow_redirection, headers=headers,
                               check_status=check_status, encoding=encoding, description=description, restful=restful,
                               stats=stats, hooks=hooks, show_len=show_len,
                               opts=kwargs.pop(_Constant.OPTS, RestOptions()))
                return func(*args, **kwargs)

            return __wrapper

        return __inner

    def __request(self, func, args, **kw):
        spec = getfullargspec(func)
        func_name = func.__name__
        if "response" not in spec.args and "response" not in spec.kwonlyargs:
            raise HttpException(f"function {func_name} need 'response' args, ex: {func_name}(response) "
                                f"or {func_name}(response=None)")

        self.__get_rest(func, args)
        kwargs = kw.pop('kwargs')
        resp = getattr(self.__rest_, f"_{self.__rest_.__class__.__name__}__request")(func=func,
                                                                                     **kw)
        kwargs['response'] = resp

    def __get_rest(self, func, args):
        if self.__rest_ is None:
            self.__rest_ = self.rest
            if inspect.ismethod(func):
                self.__rest_ = func.__self__.context.get(self.__tag)
            elif len(args) > 0:
                if isinstance(args[0], ApiAware):
                    self.__rest_ = args[0].context.get(self.__tag)

    @staticmethod
    def bulk(content: str) -> dict:
        return _utils.bulk_header(content)


class Rest(BaseRest):
    """
    A simple http request frame.
    """

    def __init__(self, file: str = None, server_list: list = None, server_name: str = None, host: str = None,
                 headers: dict or Serializable = None, cookies: dict or Serializable = None,
                 auth: tuple or Serializable = None, hooks: Hooks = None, show_len: int = None,
                 http2: bool = False, check_status: bool = False, encoding: str = "utf-8", description: str = None,
                 restful: dict or Serializable = None, retry_times: int = 10, retry_interval: int = 5,
                 retry_exit_code_range: list = None, retry_exception_retry: bool = True,
                 retry_check_handler: Callable[[Any], bool] = None, verify: bool = None,
                 proxies: dict or Serializable = None, cert: str or tuple or Serializable = None,
                 trust_env: bool = True, max_redirects: int = 30, stats: bool = False):
        """
            def retry(times: int = 10, interval: int = 5, exit_code_range: list = None, exception_retry: bool = True,
              check_handler: Callable[[Any], bool] = None) -> T:
        Build a request client.
        :param file: The path where the interface configuration file is stored.
                     configuration format：
                        [
                          {
                            "serverName": "s1",
                            "serverHost": "http://localhost1",
                            "desc": "",
                            "apis": [
                              {
                                "apiName": "user",
                                "apiPath": "/user",
                                "httpMethod": "post",
                                "headers": {"Content-type": "multipart/form-data"},
                                "desc": ""
                              }
                            ]
                          },
                          {
                            "serverName": "s2",
                            "serverHost": "http://localhost2",
                            "desc": "",
                            "apis": [
                              {
                                "apiName": "admin",
                                "apiPath": "/admin",
                                "httpMethod": "get",
                                "desc": ""
                              }
                            ]
                          }
                        ]
        :param server_name: Service name, which allows you to read interface information from the interface
        configuration file.
        """
        self.__restful: dict or Serializable = None
        self.__check_status: Optional[bool] = None
        self.__encoding: Optional[str] = None
        self.__server_name: Optional[str] = None
        self.__server_list: Optional[list[dict[str, str]]] = None
        self.__server: Optional[dict[str, Any]] = None
        self.__host: Optional[str] = None
        self.__headers: Optional[dict[str, str], Serializable] = None
        self.__cookies: Optional[dict[str, str], Serializable] = None
        self.__auth: Optional[tuple, Serializable] = None
        self.__description: Optional[str] = None
        self.__http2: Optional[bool] = None
        self.__session: Optional[Session] = None
        self.__retry_times: Optional[int] = None
        self.__retry_interval: Optional[int] = None
        self.__retry_exit_code_range: Optional[list] = None
        self.__retry_exception_retry: Optional[bool] = None
        self.__retry_check_handler: Optional[Callable[[Any], bool]] = None
        self.__verify: Optional[bool] = None
        self.__proxies: Optional[dict, Serializable] = None
        self.__hooks: Optional[Hooks] = None
        self.__show_len: Optional[int] = None
        self.__cert: str or tuple or Serializable = None
        self.__stats: bool = False
        self.__stats_datas: Optional[StatsSentUrl] = None
        self.__cache: Optional[dict[str, _RequestMeta]] = None
        self.__initialize(file=file, server_list=server_list, server_name=server_name, host=host, headers=headers,
                          cookies=cookies, auth=auth, hooks=hooks, check_status=check_status, encoding=encoding,
                          description=description, restful=restful, http2=http2, retry_times=retry_times,
                          retry_interval=retry_interval, retry_exit_code_range=retry_exit_code_range, show_len=show_len,
                          retry_exception_retry=retry_exception_retry, retry_check_handler=retry_check_handler,
                          verify=verify, proxies=proxies, cert=cert, trust_env=trust_env, max_redirects=max_redirects,
                          stats=stats)

    def __initialize(self, file: str = None, server_list: list = None, server_name: str = None, host: str = None,
                     headers: dict[str, str] or Serializable = None,
                     cookies: dict[str, str] or Serializable = None, auth: tuple or Serializable = None,
                     hooks: Hooks = None, show_len: int = None,
                     check_status: bool = False,
                     encoding: str = "utf-8", description: str = None, restful: dict or Serializable = None,
                     http2: bool = False, retry_times: int = 10, retry_interval: int = 5,
                     retry_exit_code_range: list = None, retry_exception_retry: bool = True,
                     retry_check_handler: Callable[[Any], bool] = None, verify: bool = False,
                     proxies: dict or Serializable = None, cert: str or tuple or Serializable = None,
                     trust_env: bool = True, max_redirects: int = 30, stats: bool = False):
        self.__stats_datas: Optional[StatsSentUrl] = StatsSentUrl()
        self.__restful = serializer(restful or RestFul())
        self.__check_status: bool = check_status if isinstance(check_status, bool) else False
        self.__encoding: str = encoding if isinstance(encoding, str) else "utf-8"
        self.__server_name: str = server_name
        self.__server_list: list[dict[str, str]] = []
        self.__server: dict[str, dict[Any, Any]] = {}
        self.__host: str = host
        self.__headers: dict[str, str] = serializer(headers) or {}
        self.__cookies: dict[str, str] = serializer(cookies) or {}
        self.__auth: tuple = serializer(auth) or ()
        self.__description: str = description
        self.__http2: bool = http2 if isinstance(http2, bool) else False
        self.__retry_times: int = retry_times if isinstance(retry_times, int) else 10
        self.__retry_interval: int = retry_interval if isinstance(retry_interval, int) else 5

        self.__retry_exit_code_range: int = retry_times if isinstance(retry_exit_code_range, list) else (i for i in
                                                                                                         range(200,
                                                                                                               300))
        self.__retry_exception_retry: int = retry_times if isinstance(retry_exception_retry, bool) else True
        self.__retry_check_handler: Callable[[Any], bool] = retry_check_handler
        self.__verify: bool = verify
        self.__proxies: dict or Serializable = serializer(proxies)
        self.__hooks: Optional[Hooks] = hooks if isinstance(hooks, Hooks) else Hooks()
        self.__show_len: int = _utils.get_show_len(show_len, None, None)
        self.__cert: str or tuple or Serializable = serializer(cert)
        self.__stats: bool = stats
        self.__session: Session = Session()
        self.__session.trust_env = trust_env if isinstance(trust_env, bool) else True
        self.__session.max_redirects = max_redirects if isinstance(max_redirects, int) else 30
        self.__cache: dict[str, _RequestMeta] = {}
        if http2:
            scheme = urlparse(self.__host).scheme
            if scheme != _Constant.HTTPS:
                raise HttpException(f"http2 need https protocol, but found '{scheme}'")
            self.__session.mount(f"{_Constant.HTTPS}://", HTTP20Adapter())
        if server_list:
            self.__server_list = server_list
        else:
            if file:
                path = Path(file)
                if not path.is_absolute():
                    path = Path.cwd().joinpath(file)
                if not path.exists():
                    raise RuntimeError(f"not found file: {path}")
                with open(path.absolute(), "r") as f:
                    self.__server_list = complexjson.load(f)

    def lazy_init(self, rest: 'RestWrapper' = None, file: str = None, server_list: list = None, server_name: str = None,
                  host: str = None, headers: dict or Serializable = None, cookies: dict or Serializable = None,
                  auth: tuple or Serializable = None, hooks: Hooks = None, show_len: int = None,
                  http2: bool = False, check_status: bool = False, encoding: str = "utf-8", description: str = None,
                  restful: dict or Serializable = None, retry_times: int = 10, retry_interval: int = 5,
                  retry_exit_code_range: list = None, retry_exception_retry: bool = True,
                  retry_check_handler: Callable[[Any], bool] = None, verify: bool = None,
                  proxies: dict or Serializable = None, cert: str or tuple or Serializable = None,
                  trust_env: bool = True, max_redirects: int = 30, stats: bool = False):
        """
        Lazy loading.
        Sometimes it is not necessary to provide parameters at instantiation,
        and lazy_init methods delay initialization operations.
        """
        if isinstance(rest, RestWrapper):
            self.__dict__.update(rest.__dict__)
        else:
            self.__initialize(file=file, server_list=server_list, server_name=server_name, host=host, headers=headers,
                              cookies=cookies, auth=auth, hooks=hooks, check_status=check_status, encoding=encoding,
                              description=description, restful=restful, http2=http2, retry_times=retry_times,
                              retry_interval=retry_interval, retry_exit_code_range=retry_exit_code_range,
                              show_len=show_len, retry_exception_retry=retry_exception_retry,
                              retry_check_handler=retry_check_handler, verify=verify, proxies=proxies, cert=cert,
                              trust_env=trust_env, max_redirects=max_redirects, stats=stats)

    @property
    def restful(self) -> RestFul:
        return self.__restful

    @restful.setter
    def restful(self, restful: RestFul):
        if not issubclass(t := type(restful), RestFul):
            raise TypeError(f"Excepted type is 'RestFul', got a '{t.__name__}'")
        self.__restful = restful

    @property
    def check_status(self) -> bool:
        return self.__check_status

    @check_status.setter
    def check_status(self, value):
        if isinstance(value, bool):
            self.__check_status = value
        else:
            raise TypeError(f"Excepted type is 'bool', got a '{type(value).__name__}'")

    @property
    def encoding(self) -> str:
        return self.__encoding

    @encoding.setter
    def encoding(self, value):
        if issubclass(value_type := type(value), str):
            self.__encoding = value
        else:
            raise TypeError(f"Excepted type is 'str', got a '{value_type.__name__}'")

    @property
    def server_name(self) -> str:
        return self.__server_name

    @server_name.setter
    def server_name(self, value):
        if issubclass(value_type := type(value), str):
            self.__server_name = value
        else:
            raise TypeError(f"Excepted type is 'str', got a '{value_type.__name__}'")

    @property
    def server_list(self) -> list:
        return self.__server_list

    @server_list.setter
    def server_list(self, value):
        if issubclass(value_type := type(value), list):
            self.__server_list = value
        else:
            raise TypeError(f"Excepted type is 'str', got a '{value_type.__name__}'")

    @property
    def server(self) -> dict:
        return self.__server

    @server.setter
    def server(self, value):
        if issubclass(value_type := type(value), dict):
            self.__server = value
        else:
            raise TypeError(f"Excepted type is 'dict', got a '{value_type.__name__}'")

    @property
    def host(self) -> str:
        return self.__host

    @host.setter
    def host(self, value):
        if issubclass(value_type := type(value), str):
            self.__host = value
        else:
            raise TypeError(f"Excepted type is 'str', got a '{value_type.__name__}'")

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value):
        if issubclass(value_type := type(value), str):
            self.__description = value
        else:
            raise TypeError(f"Excepted type is 'str', got a '{value_type.__name__}'")

    @property
    def verify(self) -> str or bool:
        return self.__verify

    @verify.setter
    def verify(self, verify: str or bool):
        if not issubclass(t := type(verify), (str, bool)):
            raise TypeError(f"Excepted type is 'str' or 'bool', got a '{t.__name__}'")
        self.__verify = verify

    @property
    def headers(self) -> dict:
        return self.__headers

    @headers.setter
    def headers(self, headers: dict):
        if not issubclass(t := type(headers), dict):
            raise TypeError(f"Excepted type is 'dict', got a '{t.__name__}'.")
        self.__headers.update(headers)

    @property
    def cookies(self) -> dict:
        return self.__cookies

    @cookies.setter
    def cookies(self, cookies: dict):
        if not issubclass(t := type(cookies), dict):
            raise TypeError(f"Excepted type is 'dict', got a '{t.__name__}'.")
        self.__cookies = cookies

    @property
    def auth(self) -> tuple:
        return self.__auth

    @auth.setter
    def auth(self, auth: tuple):
        if not issubclass(t := type(auth), (tuple, list)):
            raise TypeError(f"Excepted type is 'tuple' or 'list', got a '{t.__name__}'.")
        self.auth = auth

    @property
    def hooks(self) -> Hooks:
        return self.__hooks

    @hooks.setter
    def hooks(self, hooks: Hooks):
        if not isinstance(hooks, Hooks):
            raise TypeError(f"Excepted type is 'Hooks', got a '{type(hooks).__name__}'.")
        if self.__hooks:
            self.__hooks.add_hook_before(hooks.before_hooks)
            self.__hooks.add_hook_after(hooks.after_hooks)
        else:
            self.__hooks = hooks

    @property
    def retry_times(self) -> int:
        return self.__retry_times

    @retry_times.setter
    def retry_times(self, retry_time: int):
        if not issubclass(t := type(retry_time), int):
            raise TypeError(f"Excepted type is 'int', got a '{t.__name__}'")
        self.__retry_times = retry_time

    @property
    def retry_interval(self) -> int:
        return self.__retry_interval

    @retry_interval.setter
    def retry_interval(self, retry_interval: int):
        if not issubclass(t := type(retry_interval), int):
            raise TypeError(f"Excepted type is 'int', got a '{t.__name__}'")
        self.__retry_interval = retry_interval

    @property
    def retry_exit_code_range(self) -> list:
        return self.__retry_exit_code_range

    @retry_exit_code_range.setter
    def retry_exit_code_range(self, retry_exit_code_range: list):
        if not issubclass(t := type(retry_exit_code_range), int):
            raise TypeError(f"Excepted type is 'list', got a '{t.__name__}'")
        self.__retry_exit_code_range = retry_exit_code_range

    @property
    def retry_exception_retry(self) -> bool:
        return self.__retry_exception_retry

    @retry_exception_retry.setter
    def retry_exception_retry(self, retry_exception_retry: bool):
        if not issubclass(t := type(retry_exception_retry), bool):
            raise TypeError(f"Excepted type is 'bool', got a '{t.__name__}'")
        self.__retry_exception_retry = retry_exception_retry

    @property
    def retry_check_handler(self) -> Callable[[Any], bool]:
        return self.__retry_check_handler

    @retry_check_handler.setter
    def retry_check_handler(self, retry_check_handler: Callable[[Any], bool]):
        if not issubclass(t := type(retry_check_handler), Callable):
            raise TypeError(f"Excepted type is 'callable', got a '{t.__name__}'")
        self.__retry_check_handler = retry_check_handler

    @property
    def proxies(self) -> dict:
        return self.__proxies

    @proxies.setter
    def proxies(self, proxies: dict):
        if not issubclass(t := type(proxies), dict):
            raise TypeError(f"Excepted type is 'dict', got a '{t.__name__}'")
        self.__proxies = proxies

    @property
    def cert(self) -> str or tuple:
        return self.__cert

    @cert.setter
    def cert(self, cert: str or tuple):
        if not issubclass(t := type(cert), (str, tuple)):
            raise TypeError(f"Excepted type is 'str' or 'tuple', got a '{t.__name__}'")
        self.__cert = cert

    @property
    def stats(self) -> bool:
        return self.__stats

    @stats.setter
    def stats(self, stats: bool):
        if not issubclass(t := type(stats), bool):
            raise TypeError(f"Excepted type is 'bool', got a '{t.__name__}'")
        self.__stats = stats

    @property
    def stats_datas(self) -> 'StatsSentUrl':
        return self.__stats_datas

    @property
    def show_len(self) -> int:
        return self.__show_len

    @show_len.setter
    def show_len(self, value: int):
        if not issubclass(t := type(value), int):
            raise TypeError(f"Excepted type is 'int', got a '{t.__name__}'")
        if value < 0:
            raise ValueError(f"Excepted value great than 0, got a {value}")

        self.__show_len: int = value

    def copy(self) -> 'RestWrapper':
        new = RestWrapper()
        new.__dict__.update(self.__dict__)
        return new

    def retry(self, times: int = None, interval: int = None, exit_code_range: list = None, exception_retry: bool = None,
              check_handler: Callable[[Any], bool] = None) -> T:
        raise NotImplementedError()

    def request(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
                method: HttpMethod or str = None, allow_redirection: bool = RestConfig.allow_redirection,
                headers: dict = None, check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
                description: str = None, restful: RestFul = None, stats: bool = True,
                hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        return self.__request(api_name=api_name, server_name=server_name, host=host, api=api, method=method,
                              allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                              encoding=encoding, description=description, restful=restful, stats=stats,
                              hooks=hooks, show_len=show_len, opts=opts)

    def get(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
            allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
            restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None,
            opts: RestOptions = None) -> T:
        return self.__request(api_name=api_name, server_name=server_name, host=host, api=api, method=HttpMethod.GET,
                              allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                              encoding=encoding, description=description, restful=restful, stats=stats,
                              hooks=hooks, show_len=show_len, opts=opts)

    def post(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
             allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             description: str = None, restful: RestFul = None, stats: bool = True,
             hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        return self.__request(api_name=api_name, server_name=server_name, host=host, api=api, method=HttpMethod.POST,
                              allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                              encoding=encoding, description=description, restful=restful, stats=stats,
                              hooks=hooks, show_len=show_len, opts=opts)

    def put(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
            allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
            restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None,
            opts: RestOptions = None) -> T:
        return self.__request(api_name=api_name, server_name=server_name, host=host, api=api, method=HttpMethod.PUT,
                              allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                              encoding=encoding, description=description, restful=restful, stats=stats,
                              hooks=hooks, show_len=show_len, opts=opts)

    def delete(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
               allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
               check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
               description: str = None, restful: RestFul = None, stats: bool = True,
               hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        return self.__request(api_name=api_name, server_name=server_name, host=host, api=api, method=HttpMethod.DELETE,
                              allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                              encoding=encoding, description=description, restful=restful, stats=stats,
                              hooks=hooks, show_len=show_len, opts=opts)

    def patch(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
              allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
              check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
              description: str = None, restful: RestFul = None, stats: bool = True,
              hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        return self.__request(api_name=api_name, server_name=server_name, host=host, api=api, method=HttpMethod.PATCH,
                              allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                              encoding=encoding, description=description, restful=restful, stats=stats,
                              hooks=hooks, show_len=show_len, opts=opts)

    def head(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
             allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             description: str = None, restful: RestFul = None, stats: bool = True,
             hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        return self.__request(api_name=api_name, server_name=server_name, host=host, api=api, method=HttpMethod.HEAD,
                              allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                              encoding=encoding, description=description, restful=restful, stats=stats,
                              hooks=hooks, show_len=show_len, opts=opts)

    def options(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
                allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
                check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
                description: str = None, restful: RestFul = None, stats: bool = True,
                hooks: Hooks = None, show_len: int = None, opts: RestOptions = None) -> T:
        return self.__request(api_name=api_name, server_name=server_name, host=host, api=api, method=HttpMethod.OPTIONS,
                              allow_redirection=allow_redirection, headers=headers, check_status=check_status,
                              encoding=encoding, description=description, restful=restful, stats=stats,
                              hooks=hooks, show_len=show_len, opts=opts)

    def __request(self, api_name: str, server_name: str, host: str = None, func=None, api: str = None,
                  method: HttpMethod or str = None, allow_redirection: bool = True, headers: dict = None,
                  check_status: bool = None, encoding: str = None, description: str = None,
                  restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None,
                  opts: RestOptions = None):
        if opts is None:
            opts = RestOptions()
        log_builder = StringBuilder()
        func_name = ""
        source_stack = inspect.stack()[1]
        if (inspect.ismethod(func) or inspect.isfunction(func)) and source_stack.filename == str(__file__) and \
                source_stack.function == "__request":
            func_name = f"<{func.__qualname__}>"
            caller_name = func.__name__
            key = func.__qualname__
            stacklevel = 5
        else:
            caller_frame = inspect.stack()[2]
            caller_name = caller_frame[3]
            caller_file = caller_frame[1]
            caller_line = caller_frame[2]
            key = f"{caller_file}.{caller_line}.{caller_name}"
            stacklevel = 4
        _utils.build_log_message(log_builder, f' [{func_name}Request Start] '.center(81, '*'))
        server_name_ = _utils.server_name_handler(self.server_name, server_name, func)
        api_name_ = _utils.api_name_handler(api_name or caller_name)
        meta = self.__cache.get(key)
        if not meta or meta.key != key:
            meta = _RequestMeta(None, key)
            self.__cache[key] = meta
            meta.server_name = server_name_
            meta.api_name = api_name_
            meta.server_dict = _utils.server_dict_handler(self.server, self.server_list, meta.server_name)
            meta.api_info = _utils.api_handler(meta.server_dict, meta.api_name)
            meta.api_description = _utils.api_desc_handler(description, meta.server_dict, meta.api_name,
                                                           _Constant.DESC)
            meta.server_description = _utils.server_desc_handler(self.description, meta.server_dict)
            meta.host = _utils.host_handler(self.host, host, meta.server_dict)
            meta.api = ObjectsUtils.none_of_default(meta.api_info.get(_Constant.API_PATH), api)
            meta.method = meta.api_info.get(_Constant.HTTP_METHOD, _utils.http_method_handler(method))
            meta.headers = meta.api_info.get(_Constant.HEADERS, {})

        cookies = _utils.cookies_handler(self.cookies, opts.get("cookies"))
        optional_args: dict = _utils.optional_args_handler(meta.api_info, opts)
        optional_args[_Constant.ALLOW_REDIRECTS] = allow_redirection
        _utils.header_handler(optional_args, self.headers, meta.method.upper(), meta.headers, headers,
                              opts.get(_Constant.HEADERS))

        check_status_: bool = self.__check_status if not check_status else check_status
        _encoding: str = self.__encoding if not encoding else encoding
        req_args = {'auth': self.__auth, 'proxies': self.__proxies, 'cert': self.__cert, 'verify': self.__verify}
        _show_len = _utils.get_show_len(self.show_len, show_len, optional_args.get("show_len"))

        for k in list(optional_args.keys()):
            if k in _OPTIONAL_ARGS_KEYS:
                v = optional_args.pop(k)
                if v:
                    req_args[k] = serializer(v)
        req_args[_Constant.COOKIES] = cookies
        resp: Optional[Response] = None
        start_time, end_time = None, None
        rest_resp = RestResponse(None)
        url: str = meta.url.format(
            **_utils.restful_handler(self.restful, restful, serializer(optional_args.pop(_Constant.RESTFUL, None)),
                                     None))
        # noinspection PyBroadException
        try:
            req_args = _utils.run_before_hooks(self.__hooks, hooks or Hooks(),
                                               optional_args.get("hooks") or Hooks(), req_args)
            start_time = datetime.now()
            resp, start_time, end_time = _utils.action(self.__session, meta.method.lower(), url,  **req_args)
            if check_status_:
                if 200 > resp.status_code or resp.status_code >= 300:
                    _LOGGER.log(level=40, msg=f"check http status code is not success: {resp.status_code}",
                                stacklevel=4)
                    raise HttpException(f"http status code is not success: {resp.status_code}")

            rest_resp = RestResponse(resp)

        except BaseException as e:
            _LOGGER.log(level=40, msg=f"An exception occurred when a request was sent without a response:\n"
                                      f"{traceback.format_exc()}", stacklevel=4)
            raise RestInternalException(f"An exception occurred during the http request process: "
                                        f"url is {meta.url}: {e}")
        finally:
            if end_time is None:
                end_time = datetime.now()
            _url = url if not resp else resp.url
            arguments_list = []
            for k, v in req_args.items():
                if not v:
                    continue
                if k in ['json', 'headers', 'data', 'params']:
                    arguments_list.append(f'\t{k.ljust(20, " ")} => {complexjson.dumps(v or "")}')
                else:
                    arguments_list.append(f'\t{k.ljust(20, " ")} => {v or ""}')
            arguments = '\n'.join(arguments_list)
            try:
                content = rest_resp.content.decode(_encoding)
            except BaseException as e:
                _LOGGER.log(level=LogLevel.WARNING.value, msg=f"RestResponse content decode error: {str(e)}",
                            stacklevel=2)
                content = rest_resp.text
            if 0 < _show_len < len(content):
                content = f"{content[:_show_len]}..."
            _utils.build_log_message(log_builder,
                                     _HTTP_INFO_TEMPLATE.format(
                                         meta.server_description,
                                         meta.api_description,
                                         'url'.ljust(20, ' '), _url,
                                         'method'.ljust(20, ' '), meta.method.upper(),
                                         arguments,
                                         'http status'.ljust(20, " "), rest_resp.code,
                                         _show_len,
                                         'resp body'.ljust(20, ' '), content.strip(),
                                         'headers'.ljust(20, ' '), rest_resp.headers,
                                         'start time'.ljust(20, ' '), start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                                         'end time'.ljust(20, ' '), end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
                                         'use time'.ljust(20, ' '), TimeUnit.format(
                                             TimeUnit.MICRO_SECOND.of((end_time - start_time).microseconds), 3)
                                     ))
            _utils.build_log_message(log_builder, f" [{func_name}Request End] ".center(83, '*'))
            _LOGGER.log(level=RestConfig.http_log_level.value, msg=log_builder, stacklevel=stacklevel)
            rest_resp = _utils.run_after_hooks(self.__hooks, hooks or Hooks(),
                                               optional_args.get("hooks") or Hooks(), rest_resp)
            if self.__stats is True and stats is True:
                self.__stats_datas.add((_url, meta.method))
            return rest_resp

    @staticmethod
    def bulk(content: str) -> dict:
        return _utils.bulk_header(content)
