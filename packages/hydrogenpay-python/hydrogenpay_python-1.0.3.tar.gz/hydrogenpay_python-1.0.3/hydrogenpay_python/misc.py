""" Miscellaneous Helper Functions """
import time
from hydrogenpay_python.exceptions import IncompletePaymentDetailsError


# Helper function to generate unique transaction reference
def generateTransactionReference(merchantId=None):
    """ This is a helper function for generating unique transaction  references.\n
         Parameters include:\n
        merchantId (string) -- (optional) You can specify a merchant id to start references e.g. merchantId-12345678
    """
    rawTime = round(time.time() * 1000)
    timestamp = int(rawTime)
    if merchantId:
        return merchantId + "-" + str(timestamp)
    else:
        return "HY-" + str(timestamp)


# If parameters are complete, returns true. If not returns false with arameter missing
def checkIfParametersAreComplete(requiredParameters, paymentDetails):
    """ This returns true/false depending on if the paymentDetails match the required parameters """
    for i in requiredParameters:
        if i not in paymentDetails:
            raise IncompletePaymentDetailsError(i, requiredParameters)
    return True, None
