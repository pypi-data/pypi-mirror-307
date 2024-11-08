import functools
import inspect
import logging
import re
from typing import Dict, get_type_hints, Callable, Union, List, get_origin, get_args
import requests
from requests.exceptions import RequestException


def http_host(base_url: str = ""):
    def decorator(cls):
        # add properties to class marked by http_host decorator
        cls.base_url = base_url
        cls.default_headers = {}
        cls.enable_logging = True
        cls.logger = logging.getLogger("http-client")
        
        def log_request(self, method: str, url: str, headers: dict, params: dict, data: Union[dict, None]):
            if self.enable_logging:
                self.logger.info(f"Request - Method: {method}, URL: {url}, Headers: {headers}, Params: {params}, Data: {data}")
                
        def log_response(self, response):
            if self.enable_logging:
                self.logger.info(f"with status code : {response.status_code} "
                             f"with content : {response.content}")
                
        cls.log_request = log_request
        cls.log_response = log_response
        
        return cls
    return decorator


def _extract_and_send(method_name: str, api, uri: str, func: Callable, *args, **kwargs):
    """
    Extracts the parameters from the function and sends the request to the server.
        
    :param method_name: HTTP method can be GET, POST, PUT, DELETE, etc.
    :param api: the instance of the API class
    :param uri: the URI of the endpoint
    :param func: the function to be called
    :param args: 
    :param kwargs: 
    :return: 
    """
    signature = inspect.signature(func)
    bound_arguments = signature.bind(api, *args, **kwargs)
    bound_arguments.apply_defaults()
    param_types = get_type_hints(func)
    paths_keys = re.findall(r'{(.*?)}', uri)
    
    paths, queries, data = {}, {}, None
    
    for param_name, param_value in bound_arguments.arguments.items():
        if param_name == "self":
            continue
        
        param_type = param_types.get(param_name)
        if param_name in paths_keys:
            paths[param_name] = param_value
        elif param_name == "data":
            data = param_value.json() if hasattr(param_value, "json") else param_value
        elif param_type in [str, int, float, bool]:
            queries[param_name] = param_value
        else:
            api.logger.warning(f"Unknown parameter type: {param_type} in {func}")
    
    # Merge default headers with any provided headers
    headers = api.default_headers.copy()
    if 'headers' in kwargs:
        headers.update(kwargs['headers'])
    
    for key in paths:
        uri = uri.replace(f"{{{key}}}", str(paths[key]))
    
    url = api.base_url + uri
    
    # Check if path parameters are not replaced
    unfilled_path_params = re.findall(r'{(.*?)}', url)
    if unfilled_path_params:
        raise ValueError(f"Unfilled path parameters: {', '.join(unfilled_path_params)}")
    
    api.log_request(method_name, url, headers, queries, data)
    
    try:
        response = requests.request(method_name, url, params=queries, headers=headers, data=data, timeout=100)
        api.log_response(response)
        response.raise_for_status()
    except RequestException as e:
        # self.logger.error(f"Request failed: {e}")
        api.logger.exception(f"Failed to send request to {url} "
                             f"with status code : {response.status_code} "
                             f"with content : {response.content}")
        return None
    
    return_type = param_types.get("return")
    if return_type is None:
        return None
    
    data_dict = response.json()
    
    # return return_type.parse_obj(response.json())
    
    # Check return type is a type that extends from BaseModel
    if hasattr(return_type, "parse_obj") :
        return return_type.parse_obj(data_dict)
    
    if get_origin(return_type) is list:
        inner_type = get_args(return_type)[0]
        if hasattr(inner_type, "parse_obj"):
            return [inner_type.parse_obj(item) for item in data_dict]
        else:
            return response.json()
    
    if return_type == str:
        return response.text
    
    if return_type == bytes:
        return response.content
    
    return data_dict

def http_endpoint(method_name: str):
    def decorator(uri):
        def wrapper(func):
            @functools.wraps(func)
            def wrapped(api, *args, **kwargs):
                return _extract_and_send(
                    method_name,
                    api,
                    uri,
                    func,
                    *args,
                    **kwargs
                )
            
            return wrapped
        
        return wrapper
    
    return decorator

http_get = http_endpoint("GET")
http_post = http_endpoint("POST")
http_put = http_endpoint("PUT")
http_delete = http_endpoint("DELETE")
http_patch = http_endpoint("PATCH")
http_head = http_endpoint("HEAD")
http_options = http_endpoint("OPTIONS")
http_trace = http_endpoint("TRACE")
http_connect = http_endpoint("CONNECT")

    