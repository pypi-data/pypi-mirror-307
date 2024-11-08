class HydrogenpayError(Exception):
    def __init__(self, msg):
        """ This is an error pertaining to the usage of one of the functions in Hydrogen """
        super(HydrogenpayError, self).__init__(msg)
        pass

class PaymentInitiateError(HydrogenpayError):
    """ Raised when payment initiate has failed """

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Your payment initiate call failed with message: " + \
            self.err["errMsg"]

class AuthMethodNotSupportedError(HydrogenpayError):
    """ Raised when user requests for an auth method not currently supported by hydrogenpay-python """

    def __init__(self, message):
        msg = "\n We do not currently support authMethod: \"" + \
            str(message) + "\". If you need this to be supported, please report in GitHub issues page"
        super(AuthMethodNotSupportedError, self).__init__(msg)

class InitiateTransferError(HydrogenpayError):
    """ Raised when transfer initiation fails """

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Transfer initiation failed with error: " + self.err["errMsg"]

class IncompletePaymentDetailsError(HydrogenpayError):
    """ Raised when payment details are incomplete """

    def __init__(self, value, requiredParameters):
        msg = "\n\"" + value + "\" was not defined in your dictionary. Please ensure you have supplied the following in the payload: \n " + \
            '  \n '.join(requiredParameters)
        super(IncompletePaymentDetailsError, self).__init__(msg)

class PreauthCaptureError(HydrogenpayError):
    """ Raised when capturing a preauthorized transaction for s2s could not be completed """

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Your preauth capture call failed with message: " + \
            self.err["errMsg"]

class ServerError(HydrogenpayError):
    """ Raised when the server is down or when it could not process your request """

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return " Server is down with error: " + self.err["errMsg"]

class TransactionChargeError(HydrogenpayError):
    """ Raised when a transaction initiate has failed """

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Your payment initiate call failed with message: " + \
            self.err["errMsg"]

class TransactionValidationError(HydrogenpayError):
    """ Raised when validation fails """

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Your transaction validation call failed with message: " + \
            self.err["errMsg"]

class TransactionVerificationError(HydrogenpayError):
    """ Raised when transaction could not be confirm """

    def __init__(self, err):
        self.err = err

    def __str__(self):
        return "Your transaction confirmation call failed with message: " + \
            self.err["errMsg"]
