import os
from pathlib import Path
import logging

logger = logging.getLogger('django')

api_key = 'IPAAS_API_KEY'
api_secret = 'IPAAS_API_SECRET'


class CredentialManager:
    def __init__(self, credentialsFilePath=None) -> None:
        readFromEnv = False
        fileobject = None
        try:
            if not credentialsFilePath:
                credentialsFilePath = os.path.join(
                    Path.home(), '.ipaas/credentials')
            with open(credentialsFilePath, "r") as fileobject:
                while True:
                    line = fileobject.readline()
                    if not line:
                        break
                    splits = line.split('=')
                    if splits[0] == api_key:
                        self.apiKey = splits[1].strip()
                    elif splits[0] == api_secret:
                        self.apiSecret = splits[1].strip()
        except Exception as e:
            logger.exception('no valid credentials file')
            readFromEnv = True
        finally:
            if fileobject:
                fileobject.close()

        if readFromEnv:
            self.apiKey = os.getenv(api_key)
            self.apiSecret = os.getenv(api_secret)

        if not self.apiKey:
            raise Exception('no valid api key')

        if not self.apiSecret:
            raise Exception('no valid api secret')
