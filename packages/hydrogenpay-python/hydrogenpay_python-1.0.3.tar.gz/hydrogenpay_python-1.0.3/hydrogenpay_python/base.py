import os
import warnings
import requests
import json
from hydrogenpay_python.exceptions import ServerError


class HydrogenpayBase(object):
    """ This is the core of the implementation. It includes initialization functions and direct Hydrogen endpoint functions that require either liveKey or sandboxKey """

    def __init__(
            self,
            sandboxKey=None,
            liveKey=None,
            mode=None, 
            setEnv=True):

       

        self._baseUrlMap = "https://api.hydrogenpay.com/"
        self._qaUrlMap = "https://qa-api.hydrogenpay.com/"
        self._endpointMap = {
            "paymentservice": {
                "initiate": "bepay/api/v1/merchant/initiate-payment",
                "confirmpayment": "bepay/api/v1/Merchant/confirm-payment",
                "card": "bepay/api/v1/Merchant/confirm-payment"
            },

            "transfer": {
                "initiate": "bepayment/api/v1/Merchant/initiate-bank-transfer",
                "stimulatebanktransfer": "bepay/api/v1/Payment/simulate-bank-transfer",
            },

            "card": {
                "generateClientKey": "bepayment/api/v2/Payment/generate-aggregator-client-keys",
                "purchase": "bepayment/api/v2/Payment/purchase",
                "validateOtp": "bepayment/api/v2/Payment/validate-otp",
                "resendOtp": "bepayment/api/v2/Payment/resend-otp",
                "confirmPurchaseStatus": "bepayment/api/v2/Payment/confirm-status",
                "validate3DSecure": "bepayment/api/v2/Payment/validate-3dsecure",
                "aggregateBillingInformation": "bepayment/api/v2/Payment/Aggregate-Billing-Information"
            },

        }

        # If we are using environment variables to store sandbox api Key and live api key
        if (setEnv):
            self.__mode = os.getenv("MODE", None)
            if self.__mode == "test":
                self.__liveKey = os.getenv("SANDBOX_API_KEY", None)
                self.__sandboxKey = os.getenv("SANDBOX_API_KEY", None)

                if (not self.__sandboxKey) or (not self.__liveKey):
                    raise ValueError(
                        "Please set your LIVE_API_KEY environment variable. Otherwise, pass liveKey and sandboxKey as arguments and set setEnv to false")
                
            elif self.__mode == "live":
                self.__liveKey = os.getenv("LIVE_API_KEY", None)
                self.__sandboxKey = os.getenv("LIVE_API_KEY", None)

                if (not self.__liveKey) or (not  self.__sandboxKey):
                    raise ValueError(
                        "Please set your LIVE_API_KEY environment variable. Otherwise, pass liveKey and sandboxKey as arguments and set setEnv to false")
                
        # If we are not using environment variables
        else:
            self.__mode = mode

            if (not liveKey) or (not sandboxKey) or (not mode):
                raise ValueError("\n Please provide as arguments your liveKey and sandboxKey. \n It is advised however that you provide secret key as an environment variables. \n To do this, remove the setEnv flag and save your keys as environment variables, SANDBOX_API_KEY and LIVE_API_KEY")

            else:
                if self.__mode == "test":

                    self.__liveKey = sandboxKey
                    self.__sandboxKey = sandboxKey

                elif self.__mode == "live":
                    self.__liveKey = liveKey
                    self.__sandboxKey = liveKey

                # Raise warning about not using environment variables
                warnings.warn(
                    "Though you can use the usingEnv flag to pass sandboxKey as an argument, it is advised to store it in an environment variable, especially in production.",
                    SyntaxWarning)

    # This returns the public key
    def _getLiveKey(self):
        """Returns the public key (only available in test mode)."""
        if self.__mode == 'live':
            print(f"Get key set for live {self.__liveKey}")
            return self.__liveKey
        elif self.__mode == 'test':

             return self.__sandboxKey

    # This returns the sandbox api key
    def _getSandboxKey(self):
        """Returns the secret key (only available in live mode)."""
        return self.__sandboxKey
    