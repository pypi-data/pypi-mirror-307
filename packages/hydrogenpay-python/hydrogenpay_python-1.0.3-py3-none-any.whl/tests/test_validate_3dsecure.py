"""
test_validate_3dsecure.py

This module contains test cases for validating 3DSecure transactions using the Hydrogenpay SDK when the purchase call response code is H51.
The tests confirms the status of previously initiate purchase transactions.

How to Run the Tests:
---------------------
Run this file using the command:

    python -m unittest discover -s tests -p "test_validate_3dsecure.py"

"""

import unittest
from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
from hydrogenpay_python.hydrogenpay import Hydrogenpay  # Make sure the import path is correct
from dotenv import load_dotenv
import os
import logging
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

class TestValidate3DSecure(unittest.TestCase):

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


    def test_card_purchase_confirm_status(self):
        """
        Test Case: Validates 3D Secure when the purchase call response code is H51.
        Validates 3DSecure Response from the Bank.
        """

        # Transaction reference obtained from a previous purchase call and also request key
        request_key = '617602DFEF417A1C00338E37534F002DC5F433490148696B13D193EC5917345D'

        txRef = "111213a2411ss23adxsfas4bc1_z5"  # Replace with an actual reference

        try:
            # Call the SDK to confirm the payment status
            response = self.hydrogenpay.Card.validate3DSecure(txRef, request_key)

            logger.info("Confirm Status Successful:")
            logger.info(json.dumps(response, indent=4))



        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction confirmation fails
            self.fail(f"Confirm Status Failed: {e}")


if __name__ == "__main__":
    unittest.main()
