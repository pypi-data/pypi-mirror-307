from hydrogenpay_python.exceptions import PaymentInitiateError
from hydrogenpay_python.misc import generateTransactionReference
from hydrogenpay_python.payment import Payment

class PaymentService(Payment):
    """ This is the hydrogen object for payment transactions. It contains the following public functions:\n
        .initiate -- This is for initiating payment\n
        .confirm -- This checks the status of your transaction\n
    """

    def _handleInitiateResponse(self, response, txRef=None, request=None):
        """ This handles payment initiate responses """
        # This checks if we can parse the json successfully
        res = self._preliminaryResponseChecks(
            response, PaymentInitiateError, txRef=txRef)

        response_json = res['json']
        response_data = response_json['data']
        txRef = response_data['transactionRef']

        # If all preliminary checks are passed
        data = {
            'error': False,
            'validationRequired': True,
            'txRef': txRef,
            'authUrl': None,
        }

        if response_json.get("statusCode") == "90000":
            # If contains authurl
            data['authUrl'] = response_data.get("url") 
        else:
            data['validateInstructions'] = response_json['message']
        return data

    # Process Payment function
    def initiate(self, paymentDetails, hasFailed=False):
        """ This is the direct payment initiate call.\n
             Parameters include:\n
            paymentDetails (dict) -- These are the parameters passed to the function for processing\n
        """
        endpoint = self._baseUrlMap + self._endpointMap['paymentservice']['initiate']

        # Checking for required account components
        requiredParameters = [
            'currency',
            'amount',
            'email',
            'customerName',
            ]

        return super(PaymentService, self).initiate(paymentDetails, requiredParameters, endpoint)

    def confirmpayment(self, txRef):
        endpoint = self._baseUrlMap + self._endpointMap['paymentservice']['confirmpayment']
        return super(PaymentService, self).confirmpayment(txRef, endpoint)
    
