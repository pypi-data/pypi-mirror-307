import requests

class APIClient:
    """
    A class to make HTTP requests to the Compext AI API.
    """
    def __init__(self, base_url:str, api_key:str):
        self.base_url = base_url + "/api/v1"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def get(self, route:str, data:dict={},**kwargs):
        response = requests.get(self.base_url + route, headers=self.headers, json=data, **kwargs)
        return {
            "status": response.status_code,
            "data": response.json()
        }
    
    def post(self, route:str, data:dict={},**kwargs):
        response = requests.post(self.base_url + route, headers=self.headers, json=data, **kwargs)
        return {
            "status": response.status_code,
            "data": response.json()
        }
    
    def put(self, route:str, data:dict={},**kwargs):
        response = requests.put(self.base_url + route, headers=self.headers, json=data, **kwargs)
        return {
            "status": response.status_code,
            "data": response.json()
        }

    def delete(self, route:str, data:dict={},**kwargs):
        response = requests.delete(self.base_url + route, headers=self.headers, json=data, **kwargs)
        response_data = {
            "status": response.status_code,
            "data": {}
        }

        if response.status_code != 204:
            response_data["data"] = response.json()

        return response_data
