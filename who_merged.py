import http.client
import json
import ssl
from jwt import encode
from datetime import datetime, timedelta

# Your GitHub Enterprise server and API endpoint
server = "<your_github_enterprise_url>"
endpoint = "/api/v3/repos/{owner}/{repo}"

# Generating a JWT for authentication
private_key = """-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----"""  # Your private key here

# Prepare the payload for the JWT
payload = {
    'iat': datetime.utcnow(),
    'exp': datetime.utcnow() + timedelta(minutes=10),
    'iss': 'your_app_id'  # Your GitHub App's identifier
}

# Generate the JWT token
encoded_jwt = encode(payload, private_key, algorithm='RS256')

# Headers with the JWT token for authentication
headers = {
    'Authorization': f'Bearer {encoded_jwt}',
    'User-Agent': 'Python http.client'
}

# Function to make a GET request
def github_api_request(server, endpoint):
    context = ssl._create_unverified_context()  # Only if SSL verification is not needed
    connection = http.client.HTTPSConnection(server, context=context)
    
    try:
        connection.request("GET", endpoint, headers=headers)
        response = connection.getresponse()
        return json.loads(response.read())
    except Exception as e:
        return {'error': str(e)}
    finally:
        connection.close()

# Making an API call
response = github_api_request(server, endpoint)
print(json.dumps(response, indent=4))

