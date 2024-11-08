import json
import requests
from hydrogenpay_python.base import HydrogenpayBase
from hydrogenpay_python.exceptions import ServerError


class ConfirmPayment(HydrogenpayBase):
    def __init__(self, sandboxKey, liveKey, mode, setEnv):
        super(
            ConfirmPayment,
            self).__init__(
            sandboxKey,
            liveKey,
            mode,
            setEnv)

    def _preliminaryResponseChecks(self, response, TypeOfErrorToRaise):
        try:
            responseJson = response.json()
        except BaseException:
            raise ServerError(
                {"error": True, "errMsg": response})

        # check for data parameter in response
        if not responseJson.get("data", None):
            raise TypeOfErrorToRaise({"error": True,
                                      "errMsg": responseJson.get("message",
                                                                 "Server is down")})

        # check for 200 response
        if not response.ok:
            errMsg = response["data"].get("message", None)
            raise TypeOfErrorToRaise({"error": True, "errMsg": errMsg})

        return responseJson