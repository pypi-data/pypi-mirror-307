#!/usr/bin/env python
# -*- coding:utf-8 -*

from abc import abstractmethod, ABCMeta
from collections.abc import Callable
from typing import Any

from . import HttpMethod, RestFul, Hooks
from . import StatsSentUrl
from ..config.rest import RestConfig
from ..generic import T

__all__ = []


class BaseRest(metaclass=ABCMeta):

    @property
    @abstractmethod
    def restful(self) -> RestFul:
        pass

    @restful.setter
    @abstractmethod
    def restful(self, restful: RestFul):
        pass

    @property
    @abstractmethod
    def check_status(self) -> bool:
        pass

    @check_status.setter
    @abstractmethod
    def check_status(self, value):
        pass

    @property
    @abstractmethod
    def encoding(self) -> str:
        pass

    @encoding.setter
    @abstractmethod
    def encoding(self, value):
        pass

    @property
    @abstractmethod
    def server_name(self) -> str:
        pass

    @server_name.setter
    @abstractmethod
    def server_name(self, value):
        pass

    @property
    @abstractmethod
    def server_list(self) -> list:
        pass

    @server_list.setter
    @abstractmethod
    def server_list(self, value):
        pass

    @property
    @abstractmethod
    def server(self) -> dict:
        pass

    @server.setter
    @abstractmethod
    def server(self, value):
        pass

    @property
    @abstractmethod
    def host(self) -> str:
        pass

    @host.setter
    @abstractmethod
    def host(self, value):
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value):
        pass

    @property
    @abstractmethod
    def verify(self) -> str or bool:
        pass

    @verify.setter
    @abstractmethod
    def verify(self, verify: str or bool):
        pass

    @property
    @abstractmethod
    def headers(self) -> dict:
        pass

    @headers.setter
    @abstractmethod
    def headers(self, headers: dict):
        pass

    @property
    @abstractmethod
    def cookies(self) -> dict:
        pass

    @cookies.setter
    @abstractmethod
    def cookies(self, cookies: dict):
        pass

    @property
    @abstractmethod
    def auth(self) -> tuple:
        pass

    @auth.setter
    @abstractmethod
    def auth(self, auth: tuple):
        pass

    @property
    @abstractmethod
    def hooks(self) -> Hooks:
        pass

    @hooks.setter
    @abstractmethod
    def hooks(self, hooks: Hooks):
        pass

    @property
    @abstractmethod
    def retry_times(self) -> int:
        pass

    @retry_times.setter
    @abstractmethod
    def retry_times(self, retry_time: int):
        pass

    @property
    @abstractmethod
    def retry_interval(self) -> int:
        pass

    @retry_interval.setter
    @abstractmethod
    def retry_interval(self, retry_interval: int):
        pass

    @property
    @abstractmethod
    def retry_exit_code_range(self) -> list:
        pass

    @retry_exit_code_range.setter
    @abstractmethod
    def retry_exit_code_range(self, retry_exit_code_range: list):
        pass

    @property
    @abstractmethod
    def retry_exception_retry(self) -> bool:
        pass

    @retry_exception_retry.setter
    @abstractmethod
    def retry_exception_retry(self, retry_exception_retry: bool):
        pass

    @property
    @abstractmethod
    def retry_check_handler(self) -> Callable[[Any], bool]:
        pass

    @retry_check_handler.setter
    @abstractmethod
    def retry_check_handler(self, retry_check_handler: Callable[[Any], bool]):
        pass

    @property
    @abstractmethod
    def proxies(self) -> dict:
        pass

    @proxies.setter
    @abstractmethod
    def proxies(self, proxies: dict):
        pass

    @property
    @abstractmethod
    def cert(self) -> str or tuple:
        pass

    @cert.setter
    @abstractmethod
    def cert(self, cert: str or tuple):
        pass

    @property
    @abstractmethod
    def stats(self) -> bool:
        pass

    @stats.setter
    @abstractmethod
    def stats(self, stats: bool):
        pass

    @property
    @abstractmethod
    def stats_datas(self) -> 'StatsSentUrl':
        pass

    @property
    @abstractmethod
    def show_len(self) -> int:
        pass

    @show_len.setter
    @abstractmethod
    def show_len(self, value: int):
        pass

    @abstractmethod
    def copy(self) -> 'BaseRest':
        """
        Copies the current object.
        !!!!!!WARNING!!!!!!
        Shallow Copy.
        !!!!!!WARNING!!!!!!
        """

    @abstractmethod
    def retry(self, times: int = None, interval: int = None, exit_code_range: list = None, exception_retry: bool = None,
              check_handler: Callable[[Any], bool] = None) -> T:
        """
        if http request fail or exception, will retry.
        :param check_handler: This parameter is a callback function, if function return value check fail,
                              the retry is also triggered.
        it will determine whether to continue (make) the retry by checking the key of the body
        :param times: Number of retries
        :param interval: Retry interval
        :param exit_code_range: The expected HTTP status,
        if the response status code of the HTTP request is within this range, will exit the retry. The range is closed.
        default value [200, 299].
        :param exception_retry: Whether to retry when an exception occurs. True will try again

        If all of the above parameters are provided, the default values are used.

        Example:
            class Api:
                rest = Rest("rest.json", host="http://localhost:8080", description="demo domain")

                @rest.retry(times=2)
                @rest.get(description="打印hello")
                def test_case2(self,  response) -> RestResponse:
                    return response
        """

    @abstractmethod
    def request(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
                method: HttpMethod or str = None, allow_redirection: bool = RestConfig.allow_redirection,
                headers: dict = None, check_status: bool = RestConfig.check_status,
                encoding: str = RestConfig.encoding, description: str = None, restful: RestFul = None,
                stats: bool = True, hooks: Hooks = None, show_len: int = None) -> T:
        """
        http  request, need to specify the request method.
        Configure the interface information
        Important: requests arguments must be keyword arguments
        :param hooks: send request before and after run.
                      Order of execution, opts.hooks > request.hooks > rest.hooks.
        :param description: api's description info
        :param encoding: parse response's text or content encode
        :param check_status: check http response status, default false
        :param api_name: Specify the API name, if empty while use function name as api name
        :param server_name: service name, which overrides the server_name of the instance.
                            If it is blank and the instance server_name is also blank,
                            the class name is used as the server name
        :param host: interface domain name, which is used first
        :param api: service http interface, which takes precedence over this parameter when specified
        :param method: interface request method, which is used in preference after specified
        :param allow_redirection: Whether to automatically redirect, the default is
        :param headers: custom http request header, if allow_redirection parameter is included,
        the allow_redirection in the header takes precedence
        :param restful: if it is a restful-style URL, it is used to replace the keywords in the URL,
        and if the keyword is missing, KeyError will be thrown
        :param stats: Whether the API is counted
        :param show_len: When the response is large, the maximum number of characters that can be displayed.

        The parameters of the func only need a 'response', others, such as params, data, etc.,
        can be specified directly in the argument as keyword arguments.
        Keyword parameter restrictions only support the following parameters,include "params", "data", "json",
        "headers", "cookies", "files", "auth", "timeout", "allow_redirects", "proxies", "verify", "stream", "cert",
        "stream", "hooks".
        if requests module have been added new parameters, Options object is recommended because it is not limited by
        the parameters above.
        usage:
            normal use:
                class User:
                    rest = Rest(host)

                    @rest.get(api="/get_user", method=Method.GET)
                    def get_info(self, response):
                        return response
                user = User()


            type_reference:
                @EntityType()
                class Data(Entity):
                    id: list[str]
                    OK: str


                class User:
                    rest = Rest(host)

                    @rest.get(api="/get_user", method=Method.GET, type_reference=Data)
                    def get_info(self, response):
                        return response
                user = User()
                print(user.get_info())  # Data(id=[1], OK='200')






            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def get(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
            allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
            restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None) -> T:
        """
        http get request method
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.get(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def post(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
             allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             description: str = None, restful: RestFul = None, stats: bool = True,
             hooks: Hooks = None, show_len: int = None) -> T:
        """
        http POST request method.
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.post(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def put(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
            allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
            check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding, description: str = None,
            restful: RestFul = None, stats: bool = True, hooks: Hooks = None, show_len: int = None) -> T:
        """
        http PUT request method.
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.put(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def delete(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
               allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
               check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
               description: str = None, restful: RestFul = None, stats: bool = True,
               hooks: Hooks = None, show_len: int = None) -> T:
        """
        http DELETE request method
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.delete(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def patch(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
              allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
              check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
              description: str = None, restful: RestFul = None, stats: bool = True,
              hooks: Hooks = None, show_len: int = None) -> T:
        """
        http PATCH request method
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.patch(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def head(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
             allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
             check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
             description: str = None, restful: RestFul = None, stats: bool = True,
             hooks: Hooks = None, show_len: int = None) -> T:
        """
        http HEAD request method
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.head(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @abstractmethod
    def options(self, api_name: str = None, server_name: str = None, host: str = None, api: str = None,
                allow_redirection: bool = RestConfig.allow_redirection, headers: dict = None,
                check_status: bool = RestConfig.check_status, encoding: str = RestConfig.encoding,
                description: str = None, restful: RestFul = None, stats: bool = True,
                hooks: Hooks = None, show_len: int = None) -> T:
        """
        http OPTIONS request method
        Refer to request().
        usage:
            class User:
                rest = Rest(host)

                @rest.options(api="/get_user")
                def get_info(self, response):
                    return response
            user = User()

            # There is no such parameter in the formal parameter, but we can still pass the parameter using the
            specified keyword parameter.
            user.get_info(params={}, data={}) equivalent to user.get_info(opts=RestOptions(params={}, data={}))
            We recommend that you use the Options object.
            In the future, RestOptions will be forced to pass requests parameters.
            That is, only the 'user.get_info(opts=RestOptions(params={}, data={}))' model will be supported in the
            future.
        """

    @staticmethod
    @abstractmethod
    def bulk(content: str) -> dict:
        """
        Convert headers copied from the browser to dicts
        :param content: copied header from the browser
        :return: python dict object
        example:
            header = Rest.bulk(r'''
                :method:POST
                :scheme:https
                Accept:*/*
                Accept-Encoding:gzip, deflate, br
                Accept-Language:zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6
                Content-Encoding:gzip
                Content-Length:367
                Content-Type:application/x-protobuf
                Origin:https://zhuanlan.zhihu.com
                Sec-Ch-Ua:"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"
                Sec-Ch-Ua-Mobile:?0
                Sec-Ch-Ua-Platform:"Windows"
                Sec-Fetch-Dest:empty
                Sec-Fetch-Mode:cors
                Sec-Fetch-Site:same-site
                User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0
                X-Za-Batch-Size:1
                X-Za-Log-Version:3.3.74
                X-Za-Platform:DesktopWeb
                X-Za-Product:Zhihu
                    ''')
            print(header)  =>  {':method': 'POST', ':scheme': 'https', 'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6', 'Content-Encoding': 'gzip', 'Content-Length': '367', 'Content-Type': 'application/x-protobuf', 'Origin': 'https://zhuanlan.zhihu.com', 'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0', 'X-Za-Batch-Size': '1', 'X-Za-Log-Version': '3.3.74', 'X-Za-Platform': 'DesktopWeb', 'X-Za-Product': 'Zhihu'}

        """


class BaseContext(metaclass=ABCMeta):
    """
    manage context of rest wrapper.
    """

    @abstractmethod
    def put(self, **kwargs: BaseRest):
        """
        Add tags and REST objects in the form of keywords.
        """
        pass

    @abstractmethod
    def update(self, rests: dict[str, BaseRest]):
        """
        Add tags and REST objects in dictionary form.
        """
        pass

    @abstractmethod
    def get(self, tag, default: BaseRest = None) -> BaseRest:
        """
        Get the REST object by using the tag.
        When a REST object is obtained, default is returned and default is stored in the context.
        """

    @abstractmethod
    def pop(self, tag) -> BaseRest:
        """
        remove tag and return tag value
        :param tag:
        :return:
        """


class ApiAware(metaclass=ABCMeta):
    """
    use rest wrapper's object.
    Provide data penetration capabilities
    """

    @property
    @abstractmethod
    def context(self) -> BaseContext:
        """
        BaseContext
        :return:
        """
        pass
