from .BaseRegistry import BaseRegistry
import httpx


class Darn(BaseRegistry):
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "x-api-key": self.api_key,
            "x-session-id": "",
            "x-request-id": "",
            "x-trace-id": ""
        }

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
            response = await client.request(
                method=method,
                url=f"http://gpu.attentions.ai:30056/request-handler-svc/proxy/{service_name}/{endpoint}",
                headers=headers,
                data=data,
            )
            response.raise_for_status()
            return response.json()

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
            return await self._sdk_request(
                service_name="darn-service",
                endpoint="get-all-darn",
                method="GET",
            )
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
