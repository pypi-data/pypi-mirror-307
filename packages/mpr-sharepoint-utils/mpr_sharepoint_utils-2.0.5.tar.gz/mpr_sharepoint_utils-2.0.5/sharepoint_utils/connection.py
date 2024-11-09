import requests


class SharePointConnection:
    def __init__(self, client_id: str, client_secret: str, site_id: str, tenant: str):
        """
        Parameters
        ----------
        * client_id (str): ID of service credentials
        * client_secret (str): secret string of service credentials
        * site_id (str): id of SharePoint site you wish to access
        * tenant (str): the name of your organization (you can find this in a SharePoint URL, like "tenant.sharepoint.com")
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_base_url = f"https://graph.microsoft.com/beta/sites/{site_id}/"
        self.tenant = tenant.lower()
        self._set_token()

    def _set_token(self):
        get_token_url = f"https://login.microsoftonline.com/{self.tenant}.onmicrosoft.com/oauth2/v2.0/token"
        payload_to_get_token = {
            "Grant_Type": "client_credentials",
            "Scope": "https://graph.microsoft.com/.default",
            "client_id": self.client_id,
            "Client_Secret": self.client_secret,
        }
        token_response = requests.post(get_token_url, data=payload_to_get_token).json()
        self.graph_auth_header = {
            "Authorization": f"{token_response['token_type']} {token_response['access_token']}"
        }
