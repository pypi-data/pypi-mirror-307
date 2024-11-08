"""
test_initiate_payment.py

This module contains test cases for initiating payment transactions using the Hydrogenpay SDK.
The tests validate the success of payment initiation and the structure of the response received.

How to Run the Tests:
---------------------
Run this file using the command:
    python -m unittest test_initiate_payment.py

    OR

    python -m unittest discover -s tests -p "test_initiate_payment.py"
"""

import unittest
from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
from dotenv import load_dotenv
import os
import logging
import json

# Load environment variables from .env file
load_dotenv()

# Configure logging for the module
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

class TestInitiatePayment(unittest.TestCase):

    def setUp(self):
        """
        Set up the Hydrogenpay instance before each test.
        This method retrieves API keys and sets the mode (test/live) for the SDK instance.
        """
        mode = os.getenv("MODE")  # Retrieve mode from environment variables

        # Set up the Hydrogenpay instance using API keys from environment variables and the mode
        self.hydrogenpay = Hydrogenpay(
            os.getenv("SANDBOX_API_KEY"),
            os.getenv("LIVE_API_KEY"),
            mode=mode  # Set mode for the Hydrogenpay instance
        )

    def test_initiate_payment(self):
        """
        Test Case: Initiates a payment transaction using mock data.
        Validates that the response contains necessary fields such as validationRequired and authUrl.
        """

        # Mock data for initiating a payment
        payment_details = {
            "amount": "50",
            "currency": "NGN",
            "email": "bwitlawalyusuf@gmail.com",
            "customerName": "Lawal Yusuf",
            "meta": "Test live transaction",
            "callback": "https://webhook.site/43309fe4-a1f7-406d-afff-09e1cb12b9ec", #"https://example.com/callback"
            "isAPI": True
        }

        try:
            # Call the SDK initiate function and validate the response
            response = self.hydrogenpay.PaymentService.initiate(payment_details)
            # print(f"Payment initiation success: {response}")
            logger.info("Transfer initiated successful:")
            logger.info(json.dumps(response, indent=4))

            # Assert the presence and validity of expected response fields
            self.assertIn("validationRequired", response)
            self.assertTrue(response["validationRequired"])
            self.assertIn("authUrl", response)
            self.assertIsNotNone(response["authUrl"])

        except HydrogenpayExceptions.PaymentInitiateError as e:
            # Mark test as failed if payment initiation fails
            self.fail(f"Payment initiation failed: {e}")

if __name__ == "__main__":
    unittest.main()
