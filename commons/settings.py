# import os
# import sys


class Settings():
    def __init__(self):
#         # EU_AWS_ACCESS_KEY_ID
#         try:
#             self._eu_aws_access_key_id = os.getenv("EU_AWS_ACCESS_KEY_ID")
#         except KeyError:
#             print(f"EU_AWS_ACCESS_KEY_ID is not defined")
#             sys.exit(1)

        # Version
        self._version = '1.0.0'

    @property
    def version(self) -> str:
        return self._version

settings = Settings()
