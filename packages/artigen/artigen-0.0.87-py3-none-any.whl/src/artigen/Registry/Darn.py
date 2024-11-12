from .BaseRegistry import BaseRegistry
import httpx
import json
import os


class Darn(BaseRegistry):
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {
            "x-api-key": self.api_key,
        }

    async def _sdk_request(self, service_name, endpoint, method, data=None, headers=None):
        """
        Prepares and forwards the request to the RequestHandler.
        :param service_name: The target service name.
        :param endpoint: The endpoint on the service to be called.
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

    async def create_new_darn(self, name, description=None, tags=None, file_paths=None):

        if not file_paths:
            return {"status": "error", "message": "file_paths is required"}

        try:
            # Step 1: Generate a parent pin
            parent_pin_response = await self._sdk_request(
                service_name="pin-service",
                endpoint="generate-pin",
                method="POST",
                data={"type": "darn", "sub_type": "test"}
            )

            # if parent_pin_response.get("status") == "error" and parent_pin_response.get("message") == "Invalid API key":
            #     return parent_pin_response

            if parent_pin_response.get("status") != "success":
                return {"status": "error", "message": "Failed to generate parent pin"}

            parent_pin = parent_pin_response.get("data", {}).get("pin")
            if not parent_pin:
                return {"status": "error", "message": "Parent pin not found in response"}

            # Step 2: Create the DARN with the parent pin
            darn_response = await self._sdk_request(
                service_name="darn-service",
                endpoint="create-darn",
                method="POST",
                data={
                    "name": name,
                    "description": description,
                    "pin_no": [parent_pin],
                    "tags": tags,
                    "metadata": {},
                    "children_metadata": []
                }
            )

            if darn_response.get("status") != "success":
                return {"status": "error", "message": darn_response.get("message", "Failed to create DARN")}

            darn_id = darn_response.get("data", {}).get("darn", {}).get("id")
            if not darn_id:
                return {"status": "error", "message": "DARN ID not found in response"}

            # Step 3: Process each file
            children_metadata = []
            for file_path in file_paths:
                if not os.path.isfile(file_path):
                    return {"status": "error", "message": f"Path is not a file: {file_path}"}

                if not os.path.exists(file_path):
                    return {"status": "error", "message": f"File not found: {file_path}"}

                # Generate a child pin for each file
                child_pin_response = await self._sdk_request(
                    service_name="pin-service",
                    endpoint="generate-pin",
                    method="POST",
                    data={"type": "darn",
                          "sub_type": "test",
                          "parent": parent_pin
                          }
                )

                if child_pin_response.get("status") != "success":
                    return {"status": "error", "message": "Failed to generate child pin"}

                child_pin = child_pin_response.get("data", {}).get("pin")

                if not child_pin:
                    return {"status": "error", "message": "Child pin not found in response"}

                async with httpx.AsyncClient() as client:
                    with open(file_path, 'rb') as file:
                        file_upload_response = await client.post(
                            url="http://gpu.attentions.ai:30060/file",
                            headers=self.headers,
                            files={"file": (os.path.basename(file_path), file)},
                            data={"type": "darn"}
                        )

                if file_upload_response.status_code != 200:
                    return {"status": "error", "message": "Failed to upload file"}

                file_metadata = file_upload_response.json()

                # Create a child DARN with the file metadata
                child_darn_response = await self._sdk_request(
                    service_name="darn-service",
                    endpoint="process-darn",
                    method="POST",
                    data={
                        "name": str(file_metadata.get("fileName")),
                        "parent": darn_id,
                        "pin_no": [child_pin],
                        "tags": tags,
                        "metadata": {
                            "details": {
                                "duration": file_metadata.get("duration"),
                                "fileName": file_metadata.get("fileName"),
                                "extension": file_metadata.get("extension"),
                                "fileSize": file_metadata.get("fileSize"),
                                "downloadUrl": file_metadata.get("downloadUrl"),
                                "publicUrl": None,
                                "id": file_metadata.get("id"),
                                "type": "darn"
                            },
                            "type": "local",
                            "created_by": None
                        },
                        "children_metadata": []
                    }
                )

                if child_darn_response.get("status") != "success":
                    return {"status": "error", "message": "Failed to create child DARN"}

                # Add to children metadata
                children_metadata.append({
                    "pin_no": child_darn_response.get("data", {}).get("darn", {}).get("pin_no", []),
                    "type": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("type", ""),
                    "connection_id": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("details", {}).get("id", ""),
                    "details": {
                        "details": [
                            {
                                "name": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("details", {}).get("fileName"),
                                "size": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("details", {}).get("fileSize"),
                                "file_type": child_darn_response.get("data", {}).get("darn", {}).get("metadata",{}).get("details",{}).get("extension"),
                                "downloadUrl": child_darn_response.get("data", {}).get("darn", {}).get("metadata",{}).get("details", {}).get("downloadUrl"),
                                "duration": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("details", {}).get("duration")
                            }
                        ]
                    }
                })

            # Update DARN with children metadata
            update_child_metadata = await self._sdk_request(
                service_name="darn-service",
                endpoint="update-darn",
                method="PUT",
                data={
                    "id": darn_id,
                    "children_metadata": [
                        {
                            "pin_no": parent_pin,
                            "type": "local",
                            "details": {}
                        }
                    ]
                }
            )
            if update_child_metadata.get("status") != "success":
                return {"status": "error", "message": "Failed to update DARN with children metadata"}

            update_darn_response = await self._sdk_request(
                service_name="darn-service",
                endpoint="update-darn",
                method="PUT",
                data={
                    "id": darn_id,
                    "pin_no": parent_pin,
                }
            )

            if update_darn_response.get("status") != "success":
                return {"status": "error", "message": "Failed to update DARN with children metadata"}

            return {
                "status": "success",
                "message": "DARN created successfully",
            }

        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

    async def update_darn(self, name, tags=None, file_paths=None):
        if not file_paths:
            return {"status": "error", "message": "file_paths is required"}

        try:
            response = await self._sdk_request(
                service_name="darn-service",
                endpoint="get-all-darn",
                method="GET",
            )

            if response.get("status") == "error":
                return response

            darn_list = response.get('data', {}).get('darn', [])
            darn_id = None

            # Iterate over the list to find the DARN with the specified name
            for darn in darn_list:
                if darn.get('name') == name:
                    darn_id = darn.get('id')
                    break

            if not darn_id:
                return {"status": "error", "message": f"No DARN found with name: {name}"}

            # Step 1: Generate a parent pin
            parent_pin_response = await self._sdk_request(
                service_name="pin-service",
                endpoint="generate-pin",
                method="POST",
                data={"type": "darn", "sub_type": "test"}
            )

            if parent_pin_response.get("status") != "success":
                return {"status": "error", "message": "Failed to generate parent pin"}

            parent_pin = parent_pin_response.get("data", {}).get("pin")
            if not parent_pin:
                return {"status": "error", "message": "Parent pin not found in response"}

            #  Step 2: Update the DARN with the parent pin
            darn_response = await self._sdk_request(
                service_name="darn-service",
                endpoint="update-darn",
                method="PUT",
                data={
                    "id": darn_id,
                    "children_metadata": [{
                        "pin_no": " ",
                        "type": "local",
                        "connection_id": "",
                        "details": {
                            "details": {

                            }
                        }
                    }
                    ]
                }
            )

            if darn_response.get("status") != "success":
                return {"status": "error", "message": "Failed to create DARN"}

            darn_id = darn_response.get("data", {}).get("darn", {}).get("id")
            if not darn_id:
                return {"status": "error", "message": "DARN ID not found in response"}

            # Step 3: Process each file
            children_metadata = []
            for file_path in file_paths:
                if not os.path.isfile(file_path):
                    return {"status": "error", "message": f"Path is not a file: {file_path}"}

                if not os.path.exists(file_path):
                    return {"status": "error", "message": f"File not found: {file_path}"}

                # Generate a child pin for each file
                child_pin_response = await self._sdk_request(
                    service_name="pin-service",
                    endpoint="generate-pin",
                    method="POST",
                    data={"type": "darn",
                          "sub_type": "test",
                          "parent": parent_pin
                          }
                )

                if child_pin_response.get("status") != "success":
                    return {"status": "error", "message": "Failed to generate child pin"}

                child_pin = child_pin_response.get("data", {}).get("pin")

                if not child_pin:
                    return {"status": "error", "message": "Child pin not found in response"}

                async with httpx.AsyncClient() as client:
                    with open(file_path, 'rb') as file:
                        file_upload_response = await client.post(
                            url="http://gpu.attentions.ai:30060/file",
                            headers=self.headers,
                            files={"file": (os.path.basename(file_path), file)},
                            data={"type": "darn"}
                        )

                if file_upload_response.status_code != 200:
                    return {"status": "error", "message": "Failed to upload file"}

                file_metadata = file_upload_response.json()

                # Create a child DARN with the file metadata
                child_darn_response = await self._sdk_request(
                    service_name="darn-service",
                    endpoint="process-darn",
                    method="POST",
                    data={
                        "name": str(file_metadata.get("fileName")),
                        "parent": darn_id,
                        "pin_no": [child_pin],
                        "tags": tags,
                        "metadata": {
                            "details": {
                                "duration": file_metadata.get("duration"),
                                "fileName": file_metadata.get("fileName"),
                                "extension": file_metadata.get("extension"),
                                "fileSize": file_metadata.get("fileSize"),
                                "downloadUrl": file_metadata.get("downloadUrl"),
                                "publicUrl": None,
                                "id": file_metadata.get("id"),
                                "type": "darn"
                            },
                            "type": "local",
                            "created_by": None
                        },
                        "children_metadata": []
                    }
                )

                if child_darn_response.get("status") != "success":
                    return {"status": "error", "message": "Failed to create child DARN"}

                children_metadata.append({
                    "pin_no": child_darn_response.get("data", {}).get("darn", {}).get("pin_no", []),
                    "type": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("type", ""),
                    "connection_id": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get(
                        "details", {}).get("id", ""),
                    "details": {
                        "details": [
                            {
                                "name": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("details", {}).get("fileName"),
                                "size": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("details", {}).get("fileSize"),
                                "file_type": child_darn_response.get("data", {}).get("darn", {}).get("metadata",{}).get("details",{}).get("extension"),
                                "downloadUrl": child_darn_response.get("data", {}).get("darn", {}).get("metadata",{}).get("details", {}).get("downloadUrl"),
                                "duration": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("details", {}).get("duration")
                            }
                        ]
                    }
                })

            update_child_metadata = await self._sdk_request(
                service_name="darn-service",
                endpoint="update-darn",
                method="PUT",
                data={
                    "id": darn_id,
                    "children_metadata": [
                        {
                            "pin_no": "",
                            "type": "local",
                            "details": {}
                        }
                    ]
                }
            )
            if update_child_metadata.get("status") != "success":
                return {"status": "error", "message": "Failed to update DARN with children metadata"}

            update_darn_response = await self._sdk_request(
                service_name="darn-service",
                endpoint="update-darn",
                method="PUT",
                data={
                    "id": darn_id,
                    "pin_no": parent_pin,
                }
            )

            if update_darn_response.get("status") != "success":
                return {"status": "error", "message": "Failed to update DARN with children metadata"}

            return {
                "status": "success",
                "message": "DARN updated successfully",
            }

        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

    async def list_darn(self):
        try:
            response = await self._sdk_request(
                service_name="darn-service",
                endpoint="get-all-darn",
                method="GET",
            )

            # Check if the response indicates an invalid API key
            if response.get("status") == "error" and response.get("message") == "Invalid API key":
                return response

            darn_list = response.get('data', {}).get('darn', [])

            table_data = [
                {
                    "Darn Name": darn.get('name'),
                    "Description": darn.get('description'),
                    "Tags": darn.get('tags'),
                    "Status": darn.get('status')
                }
                for darn in darn_list
            ]

            formatted_output = "\n".join(str(entry) for entry in table_data)

            return formatted_output
        except Exception as e:
            raise Exception(f"An error occurred: {str(e)}")

    async def delete_darn(self, name):
        try:
            response = await self._sdk_request(
                service_name="darn-service",
                endpoint="get-all-darn",
                method="GET",
            )

            # Check if the response indicates an invalid API key
            if response.get("status") == "error" and response.get("message") == "Invalid API key":
                return response

            darn_list = response.get('data', {}).get('darn', [])

            print(darn_list)

            # Find the ID of the DARN to delete
            id_to_delete = None
            for darn in darn_list:
                if darn.get('name') == name:
                    id_to_delete = darn.get('id')
                    break

            print(id_to_delete)

            if not id_to_delete:
                return {"status": "error", "message": f"No DARN found with name: {name}"}

            delete_response = await self._sdk_request(
                service_name="darn-service",
                endpoint=f"delete-darn?id={id_to_delete}",
                method="DELETE",
            )
            return delete_response

        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}
