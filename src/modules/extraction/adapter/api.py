import json
import requests
from typing import Any

class APIClient():
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers: dict[str,Any] = {}

    def make_post_request(
        self, 
        endpoint: str,
        json_data: dict[str, Any] = {},
        files: dict[str, Any] = {},
        data: dict[str, Any] = {}
    ) -> requests.Response:
        """
        Makes a POST request to the specified endpoint.

        Params:
            endpoint (str): The API endpoint to which the request is made.
            is_root_func (bool, optional): Indicates if this is the root 
            function call. Defaults to True.
            **kwargs: Additional keyword arguments to be sent as JSON in 
            the request body.

        Returns:
            Dict[str, Any]: The JSON response data from the POST request.
        """
        url = f"{self.base_url}{endpoint}"
        print(f"Making a POST request to {url}", flush=True)
        print("headers", self.headers, flush=True)
        response = requests.post(url, headers=self.headers, files=files,json=json_data, data=data)
        return response
    
    def make_get_request(
        self, 
        endpoint: str,
        **kwargs
    ) -> requests.Response:
        """
        Makes a GET request to the specified endpoint.

        Params:
            endpoint (str): The API endpoint to which the request is made.
            is_root_func (bool, optional): Indicates if this is the root 
            function call. Defaults to True.

        Returns:
            Dict[str, Any]: The JSON response data from the POST request.
        """
        url = f"{self.base_url}{endpoint}"
        print(f"Making a GET request to {url}", flush=True)
        response = requests.get(url, headers=self.headers, params=kwargs)
        return response
            