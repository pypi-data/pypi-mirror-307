from urllib import request, parse
import json
import socket
import datetime
import platform

address = "https://dc.services.visualstudio.com/v2/track"
instrumentationKey = "2c751560-90c8-40e9-b5dd-534566514723"


class SdkExceptionHelper:

    @staticmethod
    async def send_exception_to_app_insights(e, license_key):
        try:
            javonet_version = "2.0.0"  # Replace with your desired version
            try:
                node_name = socket.gethostname()
            except socket.error as ex:
                print(ex)
                node_name = "Unknown Host"

            operation_name = "JavonetSdkException"
            os_name = platform.system()  # Replace with your desired OS name
            calling_runtime_name = "Python"  # Replace with your desired runtime name
            event_message = str(e)

            formatted_datetime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

            payload = {
                "name": "AppEvents",
                "time": formatted_datetime,
                "iKey": instrumentationKey,
                "tags": {
                    "ai.application.ver": javonet_version,
                    "ai.cloud.roleInstance": node_name,
                    "ai.operation.id": "0",
                    "ai.operation.parentId": "0",
                    "ai.operation.name": operation_name,
                    "ai.internal.sdkVersion": javonet_version,
                    "ai.internal.nodeName": node_name
                },
                "data": {
                    "baseType": "EventData",
                    "baseData": {
                        "ver": 2,
                        "name": event_message,
                        "properties": {
                            "OperatingSystem": os_name,
                            "LicenseKey": license_key,
                            "CallingTechnology": calling_runtime_name
                        }
                    }
                }
            }

            data = json.dumps(payload).encode()
            req = request.Request(address, data=data,
                                  headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
            with request.urlopen(req) as response:
                response_code = response.getcode()
            return response_code
        except Exception as ex:
            print(ex)
            return None