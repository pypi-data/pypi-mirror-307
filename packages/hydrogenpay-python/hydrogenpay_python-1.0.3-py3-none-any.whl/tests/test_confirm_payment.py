"""
test_confirm_payment.py

This module contains test cases for confirming payment transactions using the Hydrogenpay SDK.
The tests verify the status of previously initiated transactions.

How to Run the Tests:
---------------------
Run this file using the command:

    python -m unittest test_confirm_payment.py

    OR

    python -m unittest discover -s tests -p "test_confirm_payment.py"

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

class TestConfirmPayment(unittest.TestCase):

    def setUp(self):
        """
        Set up the Hydrogenpay instance before each test.
        Retrieves API keys and sets the mode (test/live).
        """
        mode = os.getenv("MODE")

        # Set up the Hydrogenpay instance using API keys from environment variables and the mode
        self.hydrogenpay = Hydrogenpay(
            os.getenv("SANDBOX_API_KEY"),
            os.getenv("LIVE_API_KEY"),
            mode=mode
        )

    def test_confirm_payment(self):
        """
        Test Case: Confirms the payment status of a previously initiated transaction.
        Validates that the status is 'Paid' for the given transaction reference.
        """

        # Transaction reference obtained from a previous payment initiation
        txRef = "36934683_87087a9180"  # Replace with an actual reference

        try:
            # Call the SDK to confirm the payment status
            response = self.hydrogenpay.PaymentService.confirmpayment(txRef)

            logger.info("Payment confirmation successful:")
            logger.info(json.dumps(response, indent=4))

            # Assert that the payment status is 'Paid'
            self.assertEqual(response["status"], "Paid")
            self.assertEqual(response["transactionStatus"], "Paid")
            self.assertIn("id", response)  # Ensure ID is present
            self.assertIn("amount", response)  
            self.assertIn("transactionRef", response)  
            self.assertEqual(response["currency"], "NGN")  
            self.assertEqual(response["customerEmail"], "bwitlawalyusuf@gmail.com")  # Validate customer email
            self.assertIsNotNone(response["createdAt"]) 
            self.assertIsNotNone(response["paidAt"])  # Ensure payment timestamp is present

        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction confirmation fails
            self.fail(f"Transaction confirmation failed: {e}")



if __name__ == "__main__":
    unittest.main()
