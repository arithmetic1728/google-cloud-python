from google.cloud import kms_v1
import google.auth
import google.auth.transport.requests
import asyncio

project = "sijun-auth"
#project = "sijunliu-nondca-test"
parent = f"projects/{project}/locations/global"

cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
cred._always_use_jwt_access = True
cred._create_self_signed_jwt(None)
req = google.auth.transport.requests.Request()
cred.refresh(req)

async def sample_list_key_rings():
    client = kms_v1.KeyManagementServiceAsyncClient(credentials=cred)
    res = await client.list_key_rings(request={"parent": parent})
    print(res)

try:
    asyncio.run(sample_list_key_rings())
except Exception as e:
    print("=== e.message ===")
    print(e.message)
    print("=== e.details ====")
    print(e.details)