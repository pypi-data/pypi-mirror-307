from .BaseRegistry import BaseRegistry
import httpx
import json
import os


class Darn(BaseRegistry):
    def __init__(self, api_key, user_id):
        self.api_key = api_key
        self.user_id = user_id
        self.headers = {
            "x-api-key": self.api_key,
            "x-user-id": self.user_id,
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
                    "children_metadata": []
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
                            data={"type": "credentials"}
                        )

                if file_upload_response.status_code != 200:
                    return {"status": "error", "message": "Failed to upload file"}

                file_metadata = file_upload_response.json()
                print(file_metadata)
                # Create a child DARN with the file metadata
                child_darn_response = await self._sdk_request(
                    service_name="darn-service",
                    endpoint="create-darn",
                    method="POST",
                    data={
                        "name": str(file_metadata.get("fileName")),
                        # "parent": [darn_id],
                        "pin_no": [child_pin],
                        "tags": tags,
                        "children_metadata": [
                            {
                                # "type": file_metadata.get("type"),
                                # "connection_id": file_metadata.get("connection_id"),
                                # "details": {
                                #     "fileName": file_metadata.get("fileName"),
                                #     "downloadUrl": file_metadata.get("downloadUrl"),
                                #     "extension": file_metadata.get("extension"),
                                #     "fileSize": file_metadata.get("fileSize"),
                                #     "duration": file_metadata.get("duration")
                                # }
                            }
                        ]
                    }
                )
                print(child_darn_response)
                # child_darn_response = await self._sdk_request(
                #     service_name="darn-service",
                #     endpoint="create-darn",
                #     method="POST",
                #     data={
                #         "name": str(file_metadata.get("fileName")),
                #         "pin_no": [child_pin],
                #         "tags": tags,
                #         "children_metadata": [
                #             {
                #                 "type": str(file_metadata.get("type")),
                #                 "connection_id": str(file_metadata.get("id")),
                #                 "pin_no": child_pin,
                #                 "details": [
                #                     {
                #                         "fileName": file_metadata.get("fileName"),
                #                         "downloadUrl": file_metadata.get("downloadUrl"),
                #                         "extension": file_metadata.get("extension"),
                #                         "fileSize": file_metadata.get("fileSize"),
                #                         "duration": file_metadata.get("duration")
                #                     }
                #                 ]
                #             }
                #         ]
                #     }
                # )
                # #
                # print("Child DARN Response:", child_darn_response)

                if child_darn_response.get("status") != "success":
                    return {"status": "error", "message": "Failed to create child DARN"}

                return child_darn_response

                # return child_darn_response
        #
        #         # Add to children metadata
        #         children_metadata.append({
        #             "pin_no": child_darn_response.get("data", {}).get("darn", {}).get("pin_no", []),
        #             "type": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("type", ""),
        #             "connection_id": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("connection_id", ""),
        #             "details": {
        #                 "details": [
        #                     {
        #                         "name": child_darn_response.get("fileName"),
        #                         "size": child_darn_response.get("fileSize"),
        #                         "file_type": child_darn_response.get("extension"),
        #                         "downloadUrl": child_darn_response.get("downloadUrl"),
        #                         "duration": child_darn_response.get("duration")
        #                     }
        #                 ]
        #             }
        #         })
        #
        #     # Update DARN with children metadata
        #     update_darn_response = await self._sdk_request(
        #         service_name="darn-service",
        #         endpoint="update-darn",
        #         method="PUT",
        #         data={
        #             "id": [darn_id],
        #             "pin_no": [parent_pin_response]
        #         }
        #     )
        #
        #     if update_darn_response.get("status") != "success":
        #         return {"status": "error", "message": "Failed to update DARN with children metadata"}
        #
        #     return {
        #     "status": "success",
        #     "message": "DARN created successfully",
        #     "data": update_darn_response.get("data"),
        #     "acknowledgment": "DARN creation process completed successfully."
        # }
        # #
        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

    async def update_darn(self, name, description=None, tags=None, file_paths=None):
        if not file_paths:
            return {"status": "error", "message": "file_paths is required"}

        try:
            # Check if a DARN with the given name already exists
            # existing_darns_response = await self._sdk_request(
            #     service_name="darn-service",
            #     endpoint="get-all-darn",
            #     method="GET",
            # )

            # Check if the response indicates an invalid API key
            # if existing_darns_response.get("status") == "error" and existing_darns_response.get("message") == "Invalid API key":
            #     return existing_darns_response

            # existing_darns = existing_darns_response.get('data', {}).get('darn', [])
            # if any(darn.get('name') == name for darn in existing_darns_response):
            #     return {"status": "error", "message": "Name already exists"}

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
                    "children_metadata": []
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
                            data={"type": "credentials"}
                        )

                if file_upload_response.status_code != 200:
                    return {"status": "error", "message": "Failed to upload file"}

                file_metadata = file_upload_response.json()

                # return file_metadata

                # Create a child DARN with the file metadata
                # child_darn_response = await self._sdk_request(
                #     service_name="darn-service",
                #     endpoint="create-darn",
                #     method="POST",
                #     data={
                #         "name": file_metadata.get("fileName"),
                #         "parent": [darn_id],
                #         "pin_no": [child_pin],
                #         "tags": [tags],
                #         "children_metadata": [
                #             {
                #                 "type": file_metadata.get("type"),
                #                 "connection_id": file_metadata.get("connection_id"),
                #                 "details": {
                #                     "fileName": file_metadata.get("fileName"),
                #                     "downloadUrl": file_metadata.get("downloadUrl"),
                #                     "extension": file_metadata.get("extension"),
                #                     "fileSize": file_metadata.get("fileSize"),
                #                     "duration": file_metadata.get("duration")
                #                 }
                #             }
                #         ]
                #     }
                # )

                child_darn_response = await self._sdk_request(
                    service_name="darn-service",
                    endpoint="create-darn",
                    method="POST",
                    data={
                        "name": str(file_metadata.get("fileName")),  # Ensure name is a string
                        "pin_no": [child_pin],  # Ensure pin_no is a list
                        "tags": tags,  # Assuming tags is a list
                        "children_metadata": [
                            {
                                "type": str(file_metadata.get("type")),
                                "connection_id": str(file_metadata.get("id")),  # Assuming 'id' is the connection_id
                                "pin_no": child_pin,  # Assuming child_pin is a string
                                "details": [
                                    {
                                        # "fileName": file_metadata.get("fileName"),
                                        # "downloadUrl": file_metadata.get("downloadUrl"),
                                        # "extension": file_metadata.get("extension"),
                                        # "fileSize": file_metadata.get("fileSize"),
                                        # "duration": file_metadata.get("duration")
                                    }
                                ]
                            }
                        ]
                    }
                )

                print("Child DARN Response:", child_darn_response)

                if child_darn_response.get("status") != "success":
                    return {"status": "error", "message": "Failed to create child DARN"}

                # return child_darn_response
        #
        #         # Add to children metadata
        #         children_metadata.append({
        #             "pin_no": child_darn_response.get("data", {}).get("darn", {}).get("pin_no", []),
        #             "type": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("type", ""),
        #             "connection_id": child_darn_response.get("data", {}).get("darn", {}).get("metadata", {}).get("connection_id", ""),
        #             "details": {
        #                 "details": [
        #                     {
        #                         "name": child_darn_response.get("fileName"),
        #                         "size": child_darn_response.get("fileSize"),
        #                         "file_type": child_darn_response.get("extension"),
        #                         "downloadUrl": child_darn_response.get("downloadUrl"),
        #                         "duration": child_darn_response.get("duration")
        #                     }
        #                 ]
        #             }
        #         })
        #
        #     # Update DARN with children metadata
        #     update_darn_response = await self._sdk_request(
        #         service_name="darn-service",
        #         endpoint="update-darn",
        #         method="PUT",
        #         data={
        #             "id": [darn_id],
        #             "pin_no": [parent_pin_response]
        #         }
        #     )
        #
        #     if update_darn_response.get("status") != "success":
        #         return {"status": "error", "message": "Failed to update DARN with children metadata"}
        #
        #     return {
        #     "status": "success",
        #     "message": "DARN created successfully",
        #     "data": update_darn_response.get("data"),
        #     "acknowledgment": "DARN creation process completed successfully."
        # }
        # #
        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}
    async def list_darn(self):
        try:
            response = await self._sdk_request(
                service_name="darn-service",
                endpoint="get-all-darn",
                method="GET",
            )

            return response


        #    # Check if the response indicates an invalid API key
        #     if response.get("status") == "error" and response.get("message") == "Invalid API key":
        #         return response
        #
        #     darn_list = response.get('data', {}).get('darn', [])
        #
        #     # Create a list of dictionaries with the required fields
        #     table_data = [
        #         {
        #             "Darn Name": darn.get('name'),
        #             "Description": darn.get('description'),
        #             "Tags": darn.get('tags'),
        #             "Status": darn.get('status')
        #         }
        #         for darn in darn_list
        #     ]
        #
        #     # Convert the list of dictionaries to a string with each entry on a new line
        #     formatted_output = "\n".join(str(entry) for entry in table_data)
        #
        #     return formatted_output
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

            # Check if the response indicates an invalid API key
            if response.get("status") == "error" and response.get("message") == "Invalid API key":
                return response

            darn_list = response.get('data', {}).get('darn', [])

            # Find the ID of the DARN to delete
            id_to_delete = None
            for darn in darn_list:
                if darn.get('name') == name:
                    id_to_delete = darn.get('id')
                    break

            if not id_to_delete:
                return {"status": "error", "message": f"No DARN found with name: {name}"}

            # Attempt to delete the DARN
            delete_response = await self._sdk_request(
                service_name="darn-service",
                endpoint=f"delete-darn?id={id_to_delete}",
                method="DELETE",
            )
            return delete_response

        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}
