from hydrogenpay_python.paymentservice import PaymentService
from hydrogenpay_python.transfer import Transfer
from hydrogenpay_python.confirmpayment import ConfirmPayment
from hydrogenpay_python.card import Card
from hydrogenpay_python.banktransfer import BankTransfer


class Hydrogenpay:

    def __init__(self, sandboxKey, liveKey, mode, setEnv=True):
        """ This is main organizing object. It contains the following:\n
            hydrogenpay.PaymentService -- For payment service\n
            hydrogenpay.BankTransfer -- For bank transfer transaction\n
            hydrogenpay.Transfer -- For bank transfers initiation\n
        """

        classes = (
            PaymentService,
            BankTransfer,
            Transfer,
            ConfirmPayment,
            Card
            )

        for _class in classes:
            attr = _class(sandboxKey, liveKey, mode, setEnv)
            setattr(self, _class.__name__, attr)

