"""
test_simulate_bank_transfer.py

This module contains test cases for simulating bank transfers using the Hydrogenpay SDK.
The tests validate the response structure when simulating bank transfers.

How to Run the Tests:
---------------------
Run this file using the command:
    python -m unittest test_simulate_bank_transfer.py

    OR

    python -m unittest discover -s tests -p "test_simulate_bank_transfer.py"
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

class TestSimulateBankTransfer(unittest.TestCase):

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

    def test_simulate_bank_transfer(self):
        """
        Test Case: Simulates a bank transfer using mock data.
        Validates that the response contains required fields like orderId and transactionId.
        """

        # Mock data for simulating a bank transfer
        transfer_details = {
            "amount": "50",
            "currency": "NGN",
            "clientTransactionRef": "36934683_87087a9180"  # Replace with an actual reference
        }

        try:
            # Call the SDK to simulate the bank transfer
            response = self.hydrogenpay.BankTransfer.simulatetransfer(transfer_details)
            logger.info("Simulate bank transfer successful:")
            logger.info(json.dumps(response, indent=4))

            # Assert the expected response structure and values
            self.assertFalse(response["error"])  # Ensure no error occurred
            self.assertEqual(response["message"], "Operation Successful")
            self.assertIn("orderId", response)
            self.assertIn("transactionId", response)

            data = response
            self.assertIn("merchantRef", data)
            self.assertIn("customerEmail", data)
            self.assertEqual(data["customerEmail"], "bwitlawalyusuf@gmail.com") #Confirm email used during initiate transfer
            self.assertIn("transactionId", data)
            self.assertEqual(data["amount"], '50.00')
            self.assertIn("transactionMode", data)

        except HydrogenpayExceptions.TransactionValidationError as e:
            # Handle errors and mark the test as failed
            self.fail(f"Simulate bank transfer failed: {e}")



if __name__ == "__main__":
    unittest.main()
