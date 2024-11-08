import json
import requests
import base64
from Crypto.Cipher import AES
from hydrogenpay_python.base import HydrogenpayBase
from hydrogenpay_python.exceptions import ServerError
from hydrogenpay_python.payment import Payment
from hydrogenpay_python.exceptions import PaymentInitiateError
from hydrogenpay_python.misc import generateTransactionReference


# class Card(HydrogenpayBase):
class Card(Payment):

    def __init__(self, sandboxKey, liveKey, mode, setEnv):
        super(
            Card,
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
    

    def generateClientKey(self):

    # """ Processes card transactions clientKey """
        endpoint = self._qaUrlMap + self._endpointMap['card']['generateClientKey']
        return super(Card, self).card(endpoint)
    

    def purchase(self, transactionDetails, requestKey):
        # """ Processes card purchase transactions"""
        endpoint = self._qaUrlMap + self._endpointMap['card']['purchase']
        # Generate transaction reference if txRef doesn't exist
        transactionDetails.setdefault('transactionRef', generateTransactionReference())

    # Checking for required parameters
        requiredParameters = [
            'transactionRef',
            'amount',
            'cardDetails',
            ]
        return super(Card, self).purchase(transactionDetails, requiredParameters, endpoint, requestKey)
    

    def _encrypt_card_details(self, plain_text, key, iv):
        """Encrypts card details using AES in CBC mode."""
        # Decode the base64 key and iv
        cryptkey = base64.b64decode(key)
        iv_bytes = base64.b64decode(iv)
        
        # Create cipher and pad plaintext
        cipher = AES.new(cryptkey, AES.MODE_CBC, iv_bytes)
        padded_plain_text = self._pad_pkcs7(plain_text)

        # Encrypt the plaintext
        encrypted_bytes = cipher.encrypt(padded_plain_text.encode('utf-8'))

        # Base64 encode the result
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    

    def _decrypt_card_details(self, cipher_text, key, iv):
        """Decrypts card details using AES in CBC mode."""
        cryptkey = base64.b64decode(key)
        iv_bytes = base64.b64decode(iv)

        # Decrypt the cipher text
        cipher = AES.new(cryptkey, AES.MODE_CBC, iv_bytes)
        encrypted_bytes = base64.b64decode(cipher_text)
        padded_plain_text = cipher.decrypt(encrypted_bytes).decode('utf-8')

        # Unpad the plaintext
        return self._unpad_pkcs7(padded_plain_text)

    def _pad_pkcs7(self, data):
        """Applies PKCS7 padding."""
        block_size = AES.block_size
        padding_length = block_size - len(data) % block_size
        padding = chr(padding_length) * padding_length
        return data + padding
    
    def _unpad_pkcs7(self, data):
        """Removes PKCS7 padding."""
        padding_length = ord(data[-1])
        return data[:-padding_length]
    

    def validateOTP(self, validateData, requestKey):
        # """ Processes card purchase transactions"""
        endpoint = self._qaUrlMap + self._endpointMap['card']['validateOtp']
        # Checking for required parameters
        requiredParameters = [
            'transactionRef',
            'otp',
            ]
        return super(Card, self).validateOtp(validateData, requiredParameters, endpoint, requestKey)


    def resendOTP(self, resendData, requestKey):
        # """ Processes resend OTP when failed to deliver """
        endpoint = self._qaUrlMap + self._endpointMap['card']['resendOtp']
        # Checking for required parameters
        requiredParameters = [
            'transactionRef',
            'amount',
            ]
        return super(Card, self).resendOTP(resendData, requiredParameters, endpoint, requestKey)


    def confirmPurchaseStatus(self, txRef, requestKey):
        # """ Confirm purchase status of the transaction """
        endpoint = self._qaUrlMap + self._endpointMap['card']['confirmPurchaseStatus']
        return super(Card, self).confirmPurchaseStatus(txRef, endpoint, requestKey)
    
    
    def validate3DSecure(self, txRef, requestKey):
        # """ Validates 3D Secure when the purchase call response code is H51. """
        endpoint = self._qaUrlMap + self._endpointMap['card']['validate3DSecure']
        return super(Card, self).validate3DSecure(txRef, endpoint, requestKey)
    

    def aggregateBillingInformation(self, billingInfoData, requestKey):
        # """ Process billing information for 3D Secure if response code is H51. """
        endpoint = self._qaUrlMap + self._endpointMap['card']['aggregateBillingInformation']
        # Checking for required parameters
        requiredParameters = [
            'transactionRef',
            'email',
            'phoneNumber',
            'lastName',
            'firstName',
            'callBackUrl',
            ]
        return super(Card, self).aggregateBillingInformation(billingInfoData, requiredParameters, endpoint, requestKey)
