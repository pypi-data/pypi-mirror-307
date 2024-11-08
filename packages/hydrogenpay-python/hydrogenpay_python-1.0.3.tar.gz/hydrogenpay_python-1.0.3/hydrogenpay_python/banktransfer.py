from hydrogenpay_python.payment import Payment
from hydrogenpay_python.exceptions import PaymentInitiateError
from hydrogenpay_python.misc import generateTransactionReference

class BankTransfer(Payment):
    """ This is the hydrogen object to simulate bank transfer payment.
    """

    def _handleStimulateBankTransferResponse(self, response, request=None):
        """ This handles transaction simulate bank transfer responses """

        # Perform preliminary checks to validate the response
        res = self._preliminaryResponseChecks(response, PaymentInitiateError)
        responseJson = res["json"]

        status_code = responseJson.get("statusCode", None)

        if status_code == "90000":
         # Return success response when statusCode is 90000
            return {
                "error": False,
                "orderId": responseJson['data'].get("orderId", "No status provided"),  # Handle if status is missing
                "message": responseJson.get("message", "No message provided"),
                "merchantRef": responseJson["data"].get("merchantRef", "No transactionRef provided"),
                "customerEmail": responseJson["data"].get("customerEmail", None),
                "transactionId": responseJson["data"].get("transactionId", None),
                "amount": responseJson["data"].get("amount", None),
                "description": responseJson["data"].get("description", None),
                "currency": responseJson["data"].get("currency", None),
                "merchantInfo": responseJson["data"].get("merchantInfo", None),
                "paymentId": responseJson["data"].get("paymentId", None),
                "discountPercentage": responseJson["data"].get("discountPercentage", None),
                "callBackUrl": responseJson["data"].get("callBackUrl", None),
                "isRecurring": responseJson["data"].get("isRecurring", None),
                "frequency": responseJson["data"].get("frequency", None),
                "serviceFees": responseJson["data"].get("serviceFees", None),
                "isBankDiscountEnabled": responseJson["data"].get("isBankDiscountEnabled", None),
                "bankDiscountValue": responseJson["data"].get("bankDiscountValue", None),
                "vatFee": responseJson["data"].get("vatFee", None),
                "vatPercentage": responseJson["data"].get("vatPercentage", None),
                "transactionMode": responseJson["data"].get("transactionMode", None),
            }

        else:
            # Handle failure case when statusCode is not 90000
            return {
                "error": True,
                "message": responseJson.get("message", "No message provided"),
                "statusCode": status_code
            }

    # Simulate Bank Transfer function
    def simulatetransfer(self, paymentDetails, hasFailed=False):
        """ This is the direct call.\n
            Parameters include:\n
            Payment Details (dict) -- These are the parameters passed to the function for processing\n
        """

        # endpoint
        endpoint = self._baseUrlMap + self._endpointMap['transfer']['stimulatebanktransfer']
        # print(f"Stimulate Bank Transfer Endpoint: {endpoint}")

        # Checking for required parameters
        requiredParameters = [
            'amount',
            'currency',
            'clientTransactionRef',
            ]

        return super(BankTransfer, self).simulatetransfer(paymentDetails, requiredParameters, endpoint)