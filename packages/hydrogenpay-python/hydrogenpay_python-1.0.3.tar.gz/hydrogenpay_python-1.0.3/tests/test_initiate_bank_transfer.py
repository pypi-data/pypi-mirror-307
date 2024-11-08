"""
test_initiate_bank_transfer.py

This module contains test cases for initiating bank transfers using the Hydrogenpay SDK.
The tests validate the initiation of bank transfers and check the structure of the response.

How to Run the Tests:
---------------------
Run this file using the command:
    python -m unittest test_initiate_bank_transfer.py

    OR

    python -m unittest discover -s tests -p "test_initiate_bank_transfer.py"
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

class TestInitiateBankTransfer(unittest.TestCase):

    def setUp(self):
        """
        Set up the Hydrogenpay instance before each test.
        Retrieves API keys and sets the mode (test/live).
        """

        # Set up the Hydrogenpay instance using API keys from environment variables and the mode
        mode = os.getenv("MODE")
        self.hydrogenpay = Hydrogenpay(
            os.getenv("SANDBOX_API_KEY"),
            os.getenv("LIVE_API_KEY"),
            mode=mode
        )

    def test_initiate_bank_transfer(self):
        """
        Test Case: Initiates a bank transfer using mock data.
        Validates that the response structure contains required fields.
        """

        # Mock data for initiating a payment
        transfer_details = {
            "amount": "50",
            "currency": "NGN",
            "email": "bwitlawalyusuf@gmail.com",
            "customerName": "Lawal Yusuf",
            "description": "Test bank transfer",
            "meta": "Test Py transfer",
            "callback": "https://webhook.site/43309fe4-a1f7-406d-afff-09e1cb12b9ec" #https://example.com/callback
        }

        try:
            # Call the SDK initiate function and validate the response
            response = self.hydrogenpay.Transfer.initiate(transfer_details)
            logger.info("Bank transfer initiated successfully:")
            logger.info(json.dumps(response, indent=4))

            # Assert the expected response structure and values
            self.assertFalse(response["error"])  # Ensure no error occurred
            self.assertEqual(response["message"], "Initiate bank transfer successful")
            data = response["data"]
            self.assertIn("transactionRef", data)
            self.assertIn("virtualAccountNo", data)
            self.assertEqual(data["transactionStatus"], "Pending")  # Ensure status is 'Pending'

        except HydrogenpayExceptions.TransactionValidationError as e:
            # Handle errors and mark the test as failed
            self.fail(f"Bank transfer initiation failed: {e}")




if __name__ == "__main__":
    unittest.main()
