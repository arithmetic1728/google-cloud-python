from google.cloud import kms_v1
import google.auth
import google.auth.transport.requests

project = "sijun-auth"
#project = "sijunliu-nondca-test"

cred, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
cred._always_use_jwt_access = True
cred._create_self_signed_jwt(None)
req = google.auth.transport.requests.Request()
cred.refresh(req)

client = kms_v1.KeyManagementServiceClient(credentials=cred)
parent = f"projects/{project}/locations/global"

try:
    res = client.list_key_rings(request={"parent": parent})
    print(res)
except Exception as e:
    print("=== e.message ===")
    print(e.message)
    print("=== e.details ====")
    print(e.details)