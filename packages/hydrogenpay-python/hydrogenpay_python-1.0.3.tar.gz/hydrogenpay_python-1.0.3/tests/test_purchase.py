"""
test_purchase.py

This module contains test cases for card purchase using the Hydrogenpay SDK.
The tests for card purchase.

How to Run the Tests:
---------------------
Run this file using the command:

    python -m unittest discover -s tests -p "test_purchase.py"

"""

import unittest
from hydrogenpay_python.base import HydrogenpayBase
from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
from dotenv import load_dotenv
import os
import logging
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

class TestPurchase(unittest.TestCase):

    def setUp(self):
        """
        Set up the Hydrogenpay instance before each test.
        Retrieves API keys and sets the mode (test/live).
        """
        mode = os.getenv("MODE")

        # Set up the Hydrogenpay instance using API keys from environment variables and the mode
        # self.hydrogenpay = Hydrogenpay(
        #     os.getenv("SANDBOX_API_KEY"),
        #     os.getenv("LIVE_API_KEY"),
        #     mode=mode
        # )

        self.hydrogenpay = Hydrogenpay("SK_TEST_58bd83bcfb01bb8b18211842143cc4826152131eaa45211e700091fd6872cab5af2724e972070e4cbc395e3dc8d84f7f1fbd4cd1af0a6e61d9adf6accb7685eb", "SK_TEST_58bd83bcfb01bb8b18211842143cc4826152131eaa45211e700091fd6872cab5af2724e972070e4cbc395e3dc8d84f7f1fbd4cd1af0a6e61d9adf6accb7685eb", 'test', setEnv=False)

    def test_purchase(self):
        """
        Test Case: Card Purchase.
        """

        # Call the SDK to generate ClientKey and Iv for Card transaction
        response = self.hydrogenpay.Card.generateClientKey()

        data = response["data"]
        # Get client key and iv from the sdk using generateClientKey
        iv = data['clientIV']  # example IV
        key = data['clientKey']  # example key
        
        # Base64-encoded IV and key
        # iv = '4betVRpFIVwvbNLJwMszew=='  # example IV
        # key = 'NBiPLxlq0WWInT4Hob+glw=='  # example key

        # Card details JSON to be encrypted
        payment_details = {
            "CardNumber": "4456530000001096",
            "ExpiryMonth": "30",
            "ExpiryYear": "50",
            "Pin": "1111",
            "Cvv": "111"
        }

        payment_details_json = json.dumps(payment_details)

        # Encrypt and decrypt the card details
        encrypted_text = self.hydrogenpay.Card._encrypt_card_details(payment_details_json, key, iv)
        print(f"Encrypted Card Details Test: {encrypted_text}")

        decrypted_text = self.hydrogenpay.Card._decrypt_card_details(encrypted_text, key, iv)
        print(f"Decrypted Card Details Test: {decrypted_text}")

        # Mock data for initiating a card purchase call
        request_key = '617602DFEF417A1C00338E37534F002DC5F433490148696B13D193EC5917345D'

        transaction_details = {
            "transactionRef": "994vy44-345123399944978",
            "customerId": "abc",
            "amount": "10",
            "currency": "NGN",
            "ipAddress": "1.0.0.1",
            "callbackUrl": "https://hydrogenpay.com",
            "cardDetails": encrypted_text,
            "deviceInformation": {
                "httpBrowserLanguage": "en-US",
                "httpBrowserJavaEnabled": False,
                "httpBrowserJavaScriptEnabled": True,
                "httpBrowserColorDepth": "24",
                "httpBrowserScreenHeight": "820",
                "httpBrowserScreenWidth": "360",
                "httpBrowserTimeDifference": "05",
                "userAgentBrowserValue": "Mozilla/5.0 (Linux; Android 12; Infinix X6819) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Mobile Safari/537.36",
                "deviceChannel": "browser"
            }
        }

        try:
            # Call the SDK for Card Purchase
            response = self.hydrogenpay.Card.purchase(transaction_details, request_key)

            logger.info("Card Purchase Successful:")
            logger.info(json.dumps(response, indent=4))

            # Assert the expected response structure and values
            data = response["data"]
            self.assertIn("amount", data)
            self.assertIn("transactionRef", data)
            self.assertIn("transactionId", data)
            self.assertIn("transactionId3DSecure", data)
            self.assertIn("accessToken", data)
            self.assertIn("nextActionUrl", data)
            self.assertIn("responseCode", data)
            self.assertIn("referenceInformationCode", data)

        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction fails
            self.fail(f"Card Purchase Failed: {e}")


if __name__ == "__main__":
    unittest.main()
