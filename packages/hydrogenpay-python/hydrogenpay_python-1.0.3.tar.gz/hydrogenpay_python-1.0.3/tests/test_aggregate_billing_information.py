"""
test_aggregate_billing_information.py

This module contains test cases for aggregate billing informationor 3D Secure if response code is H51.
The tests billing information.

How to Run the Tests:
-------------------
Run this file using the command:

    python -m unittest discover -s tests -p "test_aggregate_billing_information.py"

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

class TestAggregateBillingInformation(unittest.TestCase):

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
        Test Case: Process billing information for 3D Secure if response code is H51.
        aggregate_billing_information
        """

        # Mock data for billing infor.
        request_key = '617602DFEF417A1C00338E37534F002DC5F433490148696B13D193EC5917345D'

        billing_data = {
            "transactionRef": "111213a2411ss23adxsfas4bc1",
            "phoneNumber": "4158880000",
            "email": "kanika02@nagarro.com",
            "country": "Nigeria",
            "countryCode": "+234",
            "postalCode": "521403",
            "administrativeArea": "Abia",
            "locality": "sanfrancisco",
            "address1": " Market St",
            "lastName": "gade",
            "firstName": "amarnath",
            "callBackUrl": "https://qa-dev.hydrogenpay.com/qa/cybersource/v1/payment-redirect-v2?transactionId=1b190000-29d0-fe84-f895-08dc5462f199"
        }

        try:
            # Call the SDK for Aggregate Bill Infor for 3D Secure if response code is H51.
            response = self.hydrogenpay.Card.aggregateBillingInformation(billing_data, request_key)

            logger.info("Aggregate Bill Infor Successful:")
            logger.info(json.dumps(response, indent=4))


        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction fails
            self.fail(f"OTP Resend Failed: {e}")


if __name__ == "__main__":
    unittest.main()
