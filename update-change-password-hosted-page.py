import argparse

from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("domain")
arg_parser.add_argument("client_id")
arg_parser.add_argument("client_secret")
arg_parser.add_argument("filename")

args = arg_parser.parse_args()

domain = args.domain
client_id = args.client_id
client_secret = args.client_secret
filename = args.filename

try:
    # obtain a token
    get_token = GetToken(domain)
    token_response = get_token.client_credentials(client_id, client_secret, 'https://{}/api/v2/'.format(domain))
    access_token = token_response['access_token']

    # use the token with the management API client
    auth0 = Auth0(domain, access_token)

    # read html file content
    file = open(filename, mode="r")
    html = file.read()

    # strip formatting characters
    html = html.replace('\r', '').replace('\n', '')
    html = " ".join(html.split())

    # initialise the patch request payload
    payload = {
        "change_password": {
            "enabled": True,
            "html": html
        }
    }

    # update the tenant
    auth0.tenants.update(payload)

    print("Hosted page updated OK")
except Exception as ex:
    print(ex)
    exit(1)
finally:
    file.close()
