import requests
import json
import copy
from hydrogenpay_python.base import HydrogenpayBase
from hydrogenpay_python.misc import checkIfParametersAreComplete, generateTransactionReference
from hydrogenpay_python.exceptions import InitiateTransferError, ServerError, IncompletePaymentDetailsError
import logging


class Transfer(HydrogenpayBase):
    def __init__(self, sandboxKey, liveKey, mode, sandbox):
        super(
            Transfer,
            self).__init__(
            sandboxKey, liveKey, mode, sandbox)

    def _preliminaryResponseChecks(
            self,
            response,
            TypeOfErrorToRaise):
        # Check if we can obtain a json
        try:
            responseJson = response.json()

        except BaseException:
            raise ServerError(
                {"error": True, "errMsg": response})

        # Check if the response contains data parameter
        if not responseJson.get("data", None):
            raise TypeOfErrorToRaise({"error": True,
                                      "errMsg": responseJson.get("message",
                                                                 "Server is down")})

        # Check if it is returning a 200
        if not response.ok:
            errMsg = responseJson.get("message", None)
            raise TypeOfErrorToRaise({"error": True, "errMsg": errMsg})

        return responseJson

    def _handleInitiateResponse(self, response, transferDetails):
        responseJson = self._preliminaryResponseChecks(
            response, InitiateTransferError)
        
        if responseJson["statusCode"] == "90000":
            return {
                "error": False,
                "message": responseJson.get(
                    "message",
                    None),
                "data": responseJson["data"]}

        else:
            raise InitiateTransferError(
                {"error": True, "data": responseJson["data"]})
        

    def initiate(self, transferDetails):
        transferDetails = copy.copy(transferDetails)
        requiredParameters = ["amount", "currency", "email", "customerName"]
        checkIfParametersAreComplete(requiredParameters, transferDetails)

        headers = {
            'Authorization':  self._getLiveKey(),
            'content-type': 'application/json',
        }

        endpoint = self._baseUrlMap + self._endpointMap["transfer"]["initiate"]

        response = requests.post(
            endpoint,
            headers=headers,
            data=json.dumps(transferDetails))
        
        if response.ok:
            responseTime = response.elapsed.total_seconds()
            logging.info(f"Response OK: {responseTime}s")
        else:
            responseTime = response.elapsed.total_seconds()
            logging.error(f"Response Failed: {response.status_code}, Time: {responseTime}s")

        return self._handleInitiateResponse(response, transferDetails)
