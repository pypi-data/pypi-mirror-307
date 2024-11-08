"""
test_resend_otp.py

This module contains test cases for card purchase otp resend using the Hydrogenpay SDK when OTP faild to deliver
The tests for Resend Otp.

How to Run the Tests:
---------------------
Run this file using the command:

    python -m unittest discover -s tests -p "test_resend_otp.py"

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

    def test_validate_otp(self):
        """
        Test Case: Resend OTP when the otp failed to deliver.
        """

        # Mock data for Opt Validation for purchase call
        request_key = '617602DFEF417A1C00338E37534F002DC5F433490148696B13D193EC5917345D'

        resend_data = {
            "transactionRef": "1164vy32-332231222476",
            "amount": "10",
        }

        try:
            # Call the SDK for Card Purchase
            response = self.hydrogenpay.Card.resendOTP(resend_data, request_key)

            logger.info("OTP Resend Successful:")
            logger.info(json.dumps(response, indent=4))



        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction fails
            self.fail(f"OTP Resend Failed: {e}")


if __name__ == "__main__":
    unittest.main()
