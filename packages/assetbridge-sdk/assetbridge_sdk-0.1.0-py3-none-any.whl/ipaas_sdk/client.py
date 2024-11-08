import requests
import ecdsa
import base64
import json
from .credentials_manager import CredentialManager


class Client:
    def __init__(self, hostName=None, credentialsFilePath=None) -> None:
        self.hostName = hostName
        self.credentialManager = CredentialManager(credentialsFilePath)

    def getHostName(self):
        if self.hostName:
            return self.hostName
        return 'http://demo-api.ipaas.com/'

    def sign(self, method, url, body=None):
        decodedSecret = ecdsa.SigningKey.from_string(
            base64.b16decode(self.credentialManager.apiSecret.encode('ascii')), curve=ecdsa.SECP256k1)
        payload = method + url
        if body:
            payload += json.dumps(body)
        payload = payload.encode("utf-8")
        sig = decodedSecret.sign(payload)
        sigEncoded = base64.urlsafe_b64encode(sig)
        return sigEncoded

    def getHeaders(self, method, url, body=None):
        return {
            'Api-Key': self.credentialManager.apiKey,
            'Api-Sig': self.sign(method, url, body),
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }

    def _get_request(self, provider, url, entity_integration_auth=None, custom_auth=None, include_raw=False):
        body = {
            "provider": provider,
            "include_raw": include_raw,
            "auth": {}
        }
        if custom_auth:
            body["auth"] = {
                "customAuth": custom_auth,
            }
        # if custom auth not provided then it should be stored with iPaaS secret manager
        if entity_integration_auth:
            body["auth"] = {
                "entityIntegrationAuth": entity_integration_auth,
            }

        return requests.get(url, data=json.dumps(body), headers=self.getHeaders('GET', url, body))

    def get_wallets(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False, vault_id="DEFAULT"):
        url = '{host_name}custodians/organizations/DEFAULT/accounts/DEFAULT/vaults/{vault_id}/wallets'.format(
            host_name=self.getHostName(),
            vault_id=vault_id
        )
        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)

    def get_wallet_addresses(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False, vault_id="DEFAULT", wallet_id="DEFAULT"):
        url = '{host_name}custodians/organizations/DEFAULT/accounts/DEFAULT/vaults/{vault_id}/wallets/{wallet_id}/addresses'.format(
            host_name=self.getHostName(),
            vault_id=vault_id,
            wallet_id=wallet_id
        )

        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)

    def get_wallet_balances(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False, vault_id="DEFAULT", wallet_id="DEFAULT", exclude_zero=False):
        url = '{host_name}custodians/organizations/DEFAULT/accounts/DEFAULT/vaults/{vault_id}/wallets/{wallet_id}/balances?exclude_zero={exclude_zero}'.format(
            host_name=self.getHostName(),
            vault_id=vault_id,
            wallet_id=wallet_id,
            exclude_zero=exclude_zero
        )

        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)

    def get_users(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False):
        url = '{host_name}custodians/users'.format(
            host_name=self.getHostName()
        )
        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)
    
    def get_organizations(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False):
        url = '{host_name}custodians/organizations'.format(
            host_name=self.getHostName()
        )
        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)

    def get_organization_transactions(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False, org_id="DEFAULT"):
        url = '{host_name}custodians/organizations/{org_id}/transactions'.format(
            host_name=self.getHostName(),
            org_id=org_id
        )

        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)
    
    def get_organization_balances(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False, org_id="DEFAULT", exclude_zero=False):
        url = '{host_name}custodians/organizations/{org_id}/balances?exclude_zero={exclude_zero}'.format(
            host_name=self.getHostName(),
            org_id=org_id,
            exclude_zero=exclude_zero
        )

        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)
    
    def get_account_transactions(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False, org_id="DEFAULT", account_id="DEFAULT"):
        url = '{host_name}custodians/organizations/{org_id}/accounts/{account_id}/transactions'.format(
            host_name=self.getHostName(),
            org_id=org_id,
            account_id=account_id
        )

        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)
    
    def get_account_balances(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False, org_id="DEFAULT", account_id="DEFAULT"):
        url = '{host_name}custodians/organizations/{org_id}/accounts/{account_id}/balances'.format(
            host_name=self.getHostName(),
            org_id=org_id,
            account_id=account_id
        )

        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)
    
    def get_vault_transactions(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False, org_id="DEFAULT", account_id="DEFAULT", vault_id="DEFAULT"):
        url = '{host_name}custodians/organizations/{org_id}/accounts/{account_id}/vaults/{vault_id}/transactions'.format(
            host_name=self.getHostName(),
            org_id=org_id,
            account_id=account_id,
            vault_id=vault_id
        )

        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)
    
    def get_vault_balances(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False, org_id="DEFAULT", account_id="DEFAULT", vault_id="DEFAULT"):
        url = '{host_name}custodians/organizations/{org_id}/accounts/{account_id}/vaults/{vault_id}/balances'.format(
            host_name=self.getHostName(),
            org_id=org_id,
            account_id=account_id,
            vault_id=vault_id
        )

        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)
    
    def get_wallet_transactions(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False, org_id="DEFAULT", account_id="DEFAULT", vault_id="DEFAULT", wallet_id="DEFAULT"):
        url = '{host_name}custodians/organizations/{org_id}/accounts/{account_id}/vaults/{vault_id}/wallets/{wallet_id}/transactions'.format(
            host_name=self.getHostName(),
            org_id=org_id,
            account_id=account_id,
            vault_id=vault_id,
            wallet_id=wallet_id
        )

        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)
    
    
    def get_exchange_accounts(self, provider, entity_integration_auth=None, custom_auth=None, include_raw=False):
        url = '{host_name}exchanges/accounts'.format(
            host_name=self.getHostName(),
        )
        return self._get_request(provider, url, entity_integration_auth, custom_auth, include_raw)