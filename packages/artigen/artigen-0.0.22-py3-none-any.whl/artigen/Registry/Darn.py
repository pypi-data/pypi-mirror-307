from .BaseRegistry import BaseRegistry
import httpx
import json


class Darn(BaseRegistry):
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "x-api-key": self.api_key,
            "x-session-id": "",
            "x-request-id": "",
            "x-trace-id": ""
        }

    def _is_api_key_valid(self):
        """
        Checks if the API key is valid.
        """
        return bool(self.api_key)

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
                    url=f"http://gpu.attentions.ai:30060/request-handler-svc/proxy/{service_name}/{endpoint}",
                    headers=headers,
                    content=json.dumps(data) if data else None,
                )
                if response.status_code == 401:
                    return {"status": "error", "message": "Invalid API key"}
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {"status": "error", "message": f"HTTP error occurred: {str(e)}"}
            except httpx.RequestError as e:
                return {"status": "error", "message": f"Request error occurred: {str(e)}"}

    async def create_new_darn(self, name, description=None, tags=None):
        try:
            # Step 1: Generate a pin by making a call to the pin-service
            pin_response = await self._sdk_request(
                service_name="pin-service",
                endpoint="generate-pin",
                method="POST",
                data={
                    "type": "darn",
                    "sub_type": "data"
                }
            )

            # Step 2: Check if the pin generation was successful
            if pin_response.get("status") != "success":
                return {"status": "error", "message": "Failed to generate pin"}

            # Extract the pin from the response data
            pin = pin_response.get("data", {}).get("pin")
            if not pin:
                return {"status": "error", "message": "Pin not found in response"}

            # Step 3: Make a call to the darn-service to process the darn
            # Include the extracted pin in the data payload
            process_response = await self._sdk_request(
                service_name="darn-service",
                endpoint="process-darn",
                method="POST",
                data={
                    "name": name,
                    "description": description,
                    "pin_no": [pin],
                    "tags": tags
                }
            )

            return process_response
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
            darn_list = response.get('data', {}).get('darn', [])

            # Create a list of dictionaries with the required fields
            table_data = [
                {
                    "Darn Name": darn.get('name'),
                    "Description": darn.get('description'),
                    "Tags": darn.get('tags'),
                    "Status": darn.get('status')
                }
                for darn in darn_list
            ]

            # Convert the list of dictionaries to a string with each entry on a new line
            formatted_output = "\n".join(str(entry) for entry in table_data)

            return formatted_output
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

    async def delete_darn(self, name):
        try:
            # Fetch all DARNs
            response = await self._sdk_request(
                service_name="darn-service",
                endpoint="get-all-darn",
                method="GET",
            )
            darn_list = response.get('data', {}).get('darn', [])

            # Find the ID of the DARN to delete
            id_to_delete = None
            for darn in darn_list:
                if darn.get('name') == name:
                    id_to_delete = darn.get('id')
                    break

            if not id_to_delete:
                return {"status": "error", "message": f"No DARN found with name: {name}"}

            # Log the ID to be deleted for debugging
            print(f"Deleting DARN with ID: {id_to_delete}")

            # Attempt to delete the DARN
            delete_response = await self._sdk_request(
                service_name="darn-service",
                endpoint=f"delete-darn?id={id_to_delete}",
                method="DELETE",
            )

            # Log the response for debugging
            print(f"Delete response: {delete_response}")

            return delete_response
        except Exception as e:
            # Log the exception for debugging
            print(f"An error occurred: {str(e)}")
            return {"status": "error", "message": f"An error occurred: {str(e)}"}