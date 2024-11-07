from .BaseRegistry import BaseRegistry
import httpx


class Darn(BaseRegistry):
    def __init__(self, user_id):
        self.user_id = user_id
        self.headers = {
            # "x-api-key": self.api_key,
            "x-user-id": self.user_id,
            "x-session-id": "",
            "x-request-id": "",
            "x-trace-id": ""
        }

    # def _is_api_key_valid(self):
    #     """
    #     Checks if the API key is valid.
    #     """
    #     return bool(self.user_id)

    async def _sdk_request(self, service_name, endpoint, method, data=None, headers=None):
        """
        Prepares and forwards the request to the RequestHandler.
        :param service_name: The target service name.
        :param endpoint: The endpoint on the service to be called.
        :param method: HTTP method type.
        :param data: Data payload for POST/PUT requests.
        :param headers: Headers including API key for authorization.
        """
        headers = headers or self.headers

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method=method,
                    url=f"http://gpu.attentions.ai:30056/request-handler-svc/proxy/{service_name}/{endpoint}",
                    headers=headers,
                    data=data,
                )
                # if response.status_code == 401:
                #     return {"status": "error", "message": "Invalid API key"}
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {"status": "error", "message": f"HTTP error occurred: {str(e)}"}
            except httpx.RequestError as e:
                return {"status": "error", "message": f"Request error occurred: {str(e)}"}
        
    async def create_new_darn(self, **kwargs):
        try:
            return await self._sdk_request(
                service_name="darn-service",
                endpoint="create-darn",
                method="POST",
                data=kwargs,
            )
        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

    async def update_darn(self, **kwargs):
        try:
            return await self._sdk_request(
                service_name="darn-service",
                endpoint="update-darn",
                method="PUT",
                data=kwargs,
            )
        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

    async def list_darn(self):
        try:
            response = await self._sdk_request(
                service_name="darn-service",
                endpoint="get-all-darn",
                method="GET",
            )
            # Extract the 'name' from each darn in the response
            darn_list = response.get('data', {}).get('darn', [])
            names = [darn.get('name') for darn in darn_list]
            return names
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

    async def delete_darn(self, **kwargs):
        try:
            return await self._sdk_request(
                service_name="darn-service",
                endpoint="delete-darn",
                method="DELETE",
                data=kwargs,
            )
        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}
