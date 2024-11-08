"""
test_generate_client_key.py

This module contains test cases for generate clientkey for card payment using the Hydrogenpay SDK.
The tests generate client key for card transactions.

How to Run the Tests:
---------------------
Run this file using the command:

    python -m unittest discover -s tests -p "test_generate_client_key.py"

"""

import unittest
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

class TestGenerateClientKey(unittest.TestCase):

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


    def test_generate_client_key(self):
        """
        Test Case: Generate Client Key for Card transaction.
        """

        try:
            # Call the SDK to generate ClientKey for Card encryption
            response = self.hydrogenpay.Card.generateClientKey()

            logger.info("Client Key Generated Successful:")
            logger.info(json.dumps(response, indent=4))

            # Assert the expected response structure and values
            data = response["data"]
            self.assertIn("merchantRef", data)
            self.assertIn("apiRequestKey", data)
            self.assertIn("clientIV", data)
            self.assertIn("clientKey", data)

        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction confirmation fails
            self.fail(f"Client Key Generation Failed: {e}")



if __name__ == "__main__":
    unittest.main()
