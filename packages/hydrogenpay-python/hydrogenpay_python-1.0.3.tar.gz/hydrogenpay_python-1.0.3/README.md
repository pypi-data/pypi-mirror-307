# Hydrogen Python SDK

## Introduction

The Python library facilitates seamless payments via card transactions and account transfers, ensuring faster delivery of goods and services. 
Seamlessly integrate Hydrogen APIs with Flask, Django, and other Python applications. Our library simplifies direct integration, enabling rapid and efficient API requests.

Python library for [Hydrogen](https://hydrogenpay.com/)
View on [pypi.python.org](https://pypi.org/project/hydrogenpay-python/1.0.3/)

Key features:

- Collections: Card, Transfers, Payments, 3DSecure, Bank Transfers.
- Recurring payments: Subscription-based payments.
- Confirmation: Payment Confirmation.
- Validation: OTP Validation, 3DSecure Validation

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Initialization](#initialization)
4. [Usage](#usage)
5. [Testing](#testing)
5. [Support](#Support)
6. [Contribution](#Contribution)
7. [License](#License)
7. [ Hydrogenpay API References](#Hydrogenpay API References)


## Requirements
1. Supported Python versions: >=2.7, !=3.0.\*, !=3.1.\*, !=3.2.\*, !=3.3.\*, !=3.4.\*
2.  **Recommended Python version:** >=3.7


## Installation
To install the library, run

```sh

pip install hydrogenpay_python

```

## Initialization

```py
from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions


# Initialize Hydrogenpay with API keys from environment variables
hydrogenpay = Hydrogenpay("YOUR SANDBOX_API_KEY", "YOUR SECRET API_KEY", 'test', setEnv=True)

# Initialize Hydrogenpay without API keys from environment variables
# hydrogenpay = Hydrogenpay(os.getenv("SANDBOX_API_KEY"), os.getenv("LIVE_API_KEY"), os.getenv("MODE"), setEnv=False)
hydrogenpay = Hydrogenpay("YOUR SANDBOX_API_KEY", "YOUR SECRETE API_KEY", 'test', setEnv=False)

# Call the PaymentService class to confirm the payment status
response = self.hydrogenpay.PaymentService.confirmpayment(txRef)

# Call the Transfer class to initiate a transfer and validate the response
response = self.hydrogenpay.Transfer.initiate(transfer_details)

# Call the PaymentService class to initiate a payment and validate the response
response = self.hydrogenpay.PaymentService.initiate(payment_details)

# Call the BankTransfer class to simulate a bank transfer
response = self.hydrogenpay.BankTransfer.simulatetransfer(transfer_details)

# Call the Card class to initiate a card payment request to the customer
response = self.hydrogenpay.Card.purchase(transaction_details, request_key)

# Call the Card class to validate the OTP when the purchase call response code is H01
response = self.hydrogenpay.Card.validateOTP(validation_data, request_key)

# Call the Card class to resend the OTP if it fails to deliver to the customer
response = self.hydrogenpay.Card.resendOTP(resend_data, request_key)

# Call the Card class to confirm the status of transactions
response = self.hydrogenpay.Card.confirmPurchaseStatus(txRef, request_key)

# Call the Card class to generate an apiRequestKey, clientIV, and clientKey for secure communication
response = self.hydrogenpay.Card.generateClientKey()

# Call the Card class to validate 3D Secure when the purchase call response code is H51
response = self.hydrogenpay.Card.validate3DSecure(txRef, request_key)

# Call the Card class to process billing information for 3D Secure if the response code is H51
response = self.hydrogenpay.Card.aggregateBillingInformation(billing_data, request_key)

```

# Usage
This documentation covers all components of the hydrogen_python SDK.

## ```Payment```
This is used to facilitating the completion of payments through their preferred methods, including card or bank transfer..


*Usage*

```python

from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
import logging #If Using Logging instead of print.


# Mock data for initiating a payment
        payment_details = {
            "amount": "50",
            "currency": "NGN",
            "email": "devtest@randomuser.com",
            "customerName": "Dev Test",
            "meta": "Test transaction",
            "callback": "https://webhook.site/43309fe4-a1f7-406d-afff-09e1cb12b9ec", #"https://example.com/callback"
            "isAPI": True
        }

        try:
            # Call the Transfer class to initiate a transfer and validate the response
            response = self.hydrogenpay.PaymentService.initiate(payment_details)
            # print(f"Payment initiation success: {response}")
            logger.info("Payment initiation successful:")
            logger.info(json.dumps(response, indent=4))


        except HydrogenpayExceptions.PaymentInitiateError as e:
            # Mark test as failed if payment initiation fails
            self.fail(f"Payment initiation failed: {e}")

```

*Arguments*

- `amount`: Amount to debit the customer.
- `currency`: Default to NGN if not passed, other currencies available are USD and GBP.
- `email`: Customer’s Email Address.
- `customerName`: Customer's name.
- `meta`: Customer's email address
- `callback`: Redirect URL after payment has been completed on the gateway.
- `isAPI`: Amount in kobo


*Returns*

Response Example:

```py
Payment initiation successful:
{
    "error": false,
    "validationRequired": true,
    "txRef": "36934683_766196b316",
    "authUrl": "https://payment.hydrogenpay.com?transactionId=94850000-d1b0-2648-175f-08dce946623e&Mode=19289182"
}

```


## ```Confirm Payment```

This allows businesses to verify the status of initiated payments using the transaction reference. This process utilizes the transaction reference to retrieve the specified payment's current status (e.g., success, failed, pending).

*Usage*

```python

from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
import logging #If Using Logging instead of print.

 # Transaction reference obtained from a previous payment initiation
        txRef = "36934683_87087a9180"  # Replace with an actual reference

        try:
            # Call the SDK to confirm the payment status
            response = self.hydrogenpay.PaymentService.confirmpayment(txRef)

            logger.info("Payment confirmation successful:")
            logger.info(json.dumps(response, indent=4))


        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction confirmation fails
            self.fail(f"Transaction confirmation failed: {e}")

```

*Arguments*

- `txRef`: Transaction Ref that is returned oncallback 


*Returns*

Response Example:

```py
Payment confirmation successful:
{
    "id": "94850000-d1b0-2648-4dda-08dce8bc64e0",
    "amount": 50.0,
    "chargedAmount": 50.0,
    "currency": "NGN",
    "customerEmail": "bwitlawalyusuf@gmail.com",
    "narration": null,
    "description": null,
    "status": "Paid",
    "transactionStatus": "Paid",
    "transactionRef": "36934683_87087a9180",
    "processorResponse": null,
    "createdAt": "2024-10-09T23:45:02.3685068",
    "paidAt": "2024-10-09T23:45:02.3685068",
    "ip": "145.224.74.164",
    "paymentType": "Card",
    "authorizationObject": null,
    "fees": 0.5,
    "vat": 0.04,
    "meta": "Test Py transaction",
    "recurringCardToken": "",
    "metadata": null,
    "error": false,
    "transactionComplete": true
}
```


## ```Transfer```

Generates dynamic virtual account details for completing payment transactions. Customers can request these details to facilitate payments through bank transfers.


*Usage*

```python

from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
import logging #If Using Logging instead of print.

 # Mock data for initiating a bank transfer
        payment_details = {
            "amount": "50",
            "currency": "NGN",
            "email": "bwitlawalyusuf@gmail.com",
            "customerName": "Lawal Yusuf",
            "meta": "Test transaction",
            "callback": "https://webhook.site/43309fe4-a1f7-406d-afff-09e1cb12b9ec", #"https://example.com/callback"
            "isAPI": True
        }

        try:
            # Call the Transfer class to initiate a transfer and validate the response
            response = self.hydrogenpay.PaymentService.initiate(payment_details)
            # print(f"Payment initiation success: {response}")
            logger.info("Bank transfer initiated successfully:")
            logger.info(json.dumps(response, indent=4))


        except HydrogenpayExceptions.PaymentInitiateError as e:
            # Mark test as failed if payment initiation fails
            self.fail(f"Payment initiation failed: {e}")

```

*Arguments*

- `amount`: Amount to trasfer
- `currency`: Default to NGN if not passed, other currencies available are USD and GBP.
- `email`: Customer’s Email Address.
- `customerName`: Customer's name.
- `meta`: Customer's email address
- `callback`: Redirect URL after payment has been completed on the gateway.
- `isAPI`: Amount in kobo


*Returns*

Response Example:

```py

Bank transfer initiated successfully:
{
    "error": false,
    "message": "Initiate bank transfer successful",
    "data": {
        "transactionRef": "36934683_473281644c",
        "virtualAccountNo": "1811357132",
        "virtualAccountName": "HYDROGENPAY",
        "expiryDateTime": "2024-10-10 19:09:32",
        "capturedDatetime": null,
        "completedDatetime": null,
        "transactionStatus": "Pending",
        "amountPaid": 50,
        "bankName": "Access Bank"
    }
}

```


## ```Bank Transfer```

Simulate a Bank Transfer Transaction to test account transfer behavior for completing transactions. The response includes essential details such as transaction status. Use the transactionRef from the initiate transfer to complete the simulation."

*Usage*

```python

from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
import logging #If Using Logging instead of print.

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


        except HydrogenpayExceptions.TransactionValidationError as e:
            # Handle errors and mark the test as failed
            self.fail(f"Simulate bank transfer failed: {e}")

```

*Arguments*

- `amount`: The amount to be transferred.
- `currency`: The currency in which the transaction is being made..
- `clientTransactionRef`: A unique reference for the client’s transaction.

*Returns*

Response Example:

```py

Simulate bank transfer successful:
{
    "error": false,
    "orderId": "36934683_886923fa59",
    "message": "Operation Successful",
    "merchantRef": "36934683",
    "customerEmail": "bwitlawalyusuf@gmail.com",
    "transactionId": "94850000-d1b0-2648-4dda-08dce8bc64e0",
    "amount": "50.00",
    "description": null,
    "currency": "NGN",
    "merchantInfo": null,
    "paymentId": "success-success-success-474512713",
    "discountPercentage": 0,
    "callBackUrl": null,
    "isRecurring": false,
    "frequency": null,
    "serviceFees": null,
    "isBankDiscountEnabled": false,
    "bankDiscountValue": null,
    "vatFee": null,
    "vatPercentage": 0,
    "transactionMode": 0
}

```


## ```Recurring Payment```
Recurring Payment allows businesses to set up subscription-based payments.


*Usage*

```python

from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
import logging #If Using Logging instead of print.


# Mock data for initiating a payment
        payment_details = {
            "amount": 50,
            "customerName": "Lawal",
            "email": "bwitlawalyusuf@gmail.com",
            "currency": "NGN", # Default to NGN if not passed, other currencies available are USD and GBP.
            "description": "test desc",
            "meta": "test meta",
            "callback": "https://webhook.site/43309fe4-a1f7-406d-afff-09e1cb12b9ec", #"https://example.com/callback"
            "frequency": 0, # Daily
            #   "frequency": 1, // Weekly
            #   "frequency": 2, // Monthly
            #   "frequency": 3, // Quarterly
            #   "frequency": 4, // Yearly
            #   "frequency": 5, // Disable auto debit.
            "isRecurring": true, # Indicates if the payment is recurring.
            "endDate": "2024-10-09T19:01:41.745Z" #End date for the recurring payment cycle in ISO 8601 format (e.g., 2024-10-29T19:01:41.745Z).
        }

        try:
            # Call the Transfer class to initiate a transfer and validate the response
            response = self.hydrogenpay.PaymentService.initiate(payment_details)
            # print(f"Payment initiation success: {response}")
            logger.info("Payment initiation successful:")
            logger.info(json.dumps(response, indent=4))


        except HydrogenpayExceptions.PaymentInitiateError as e:
            # Mark test as failed if payment initiation fails
            self.fail(f"Payment initiation failed: {e}")

```

*Arguments*

- `amount`: Amount to debit the customer.
- `currency`: Default to NGN if not passed, other currencies available are USD and GBP.
- `email`: Customer’s Email Address.
- `customerName`: Customer's name.
- `meta`: Customer's email address
- `callback`: Redirect URL after payment has been completed on the gateway.
- `frequency`: Frequency of recurring payment
- `isRecurring`: Indicates if the payment is recurring.
- `endDate`: End date for the recurring payment cycle in ISO 8601 format



*Returns*

Response Example:

```py
Payment initiation successful:
{
    "error": false,
    "validationRequired": true,
    "txRef": "36934683_71131c452e",
    "authUrl": "https://payment.hydrogenpay.com?transactionId=94850000-d1b0-2648-175f-08dce946623e&Mode=19289182"
}

```

## ```Generate Client Key```
Generates an apiRequestKey, clientIV and clientKey for secure communication with other endpoints.


*Usage*

```python

from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
import logging #If Using Logging instead of print.

# Generate Client Key for Card transaction

        try:
            # Call the SDK to generate ClientKey for Card encryption
            response = self.hydrogenpay.Card.generateClientKey()

            logger.info("Client Key Generated Successful:")
            logger.info(json.dumps(response, indent=4))


        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction confirmation fails
            self.fail(f"Client Key Generation Failed: {e}")

```

*Returns*

Response Example:

```py

Client Key Generated Successful:
{
    "statusCode": "90000",
    "message": null,
    "data": {
        "merchantRef": "30013606",
        "apiRequestKey": "617602DFEF417A1C00338E37534F002DC5F433490148696B13D193EC5917345D",
        "clientIV": "4betVRpFIVwvbNLJwMszew==",
        "clientKey": "NBiPLxlq0WWInT4Hob+glw=="
    }
}

```

## ```Card Purchase```
Initiates a card payment request to the customer.

*Usage*

```python

from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
import logging #If Using Logging instead of print.


        # Use the SDK to generate a ClientKey and Iv for card transactions.
        response = self.hydrogenpay.Card.generateClientKey()

        data = response["data"]
        # Retrieve the client key and IV from the generateClientKey method.
        iv = data['clientIV']  # example IV
        key = data['clientKey']  # example key
        
        # Encrypt the card details JSON.
        card_details = {
            "CardNumber": "4456530000001096",
            "ExpiryMonth": "30",
            "ExpiryYear": "50",
            "Pin": "1111",
            "Cvv": "111"
        }

        payment_details_json = json.dumps(card_details)

        # Encrypt card details
        encrypted_text = self.hydrogenpay.Card._encrypt_card_details(payment_details_json, key, iv)
        print(f"Encrypted Card Details Test: {encrypted_text}")

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
            # Use the SDK to initiate a card purchase.
            response = self.hydrogenpay.Card.purchase(transaction_details, request_key)

            logger.info("Card Purchase Successful:")
            logger.info(json.dumps(response, indent=4))


        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction fails
            self.fail(f"Card Purchase Failed: {e}")

```

*Arguments*

- `amount`: Amount to be charged..
- `currency`: Default to NGN if not passed, other currencies available are USD and GBP.
- `callbackUrl`: URL to redirect after transaction.
- `customerId`: Unique identifier for the customer.
- `transactionRef`: Unique reference for the transaction.
- `cardDetails`: Encrypted card details.


*Returns*

Response Example:

```py
Encrypted Card Details Test: w20lrIwGih9wyrnDNYfqXndcwtsfz8onveKhcQooFHBhpZHW5B5/CA4iTVdGUv7BY6c9purFu6JN6P1XclRvd3AOYrrZwDY3iCed2D0xjyLK7A9e2UDJ9cs+ese9y9akfQCNHi84ox32MUdCyhZ6mg==

Card Purchase Successful:

{
    "statusCode": "90000",
    "message": "Kindly enter the OTP sent to 234805***1111",
    "data": {
        "referenceInformationCode": "30013606_36754a39f5",
        "responseCode": "H01",
        "amount": "10.00",
        "transactionRef": "994vy44-345123399944978",
        "status": null,
        "submitTimeUtc": "Nov 7th 2024 | 09:13am",
        "transactionId": "d0020000-524b-fa8e-c52b-08dcff0c80e5",
        "transactionId3DSecure": "474512713",
        "eciFlag": null,
        "md": null,
        "termUrl": null,
        "accessToken": null,
        "nextActionUrl": null,
        "errors": []
    }
}

```

## ```OTP```
Validates the OTP when the purchase call response code is H01

*Usage*

```python

from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
import logging #If Using Logging instead of print.

        # Mock data for Opt Validation for purchase call
        request_key = '617602DFEF417A1C00338E37534F002DC5F433490148696B13D193EC5917345D'

        validation_data = {
            "otp": "123456",
            "transactionRef": "503021992595_99550f9c94"
        }

        try:
            # OTP Validation
            response = self.hydrogenpay.Card.validateOTP(validation_data, request_key)

            logger.info("OTP Validation Successful:")
            logger.info(json.dumps(response, indent=4))


        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction fails
            self.fail(f"OTP Validation Failed: {e}")

```

*Arguments*

- `otp`: One-time password received by the customer.
- `transactionRef`: Unique reference for the transaction.


*Returns*

Response Example:

```py
OTP Validation Successful:

{
    "statusCode": "90000",
    "message": "Operation Successful",
    "data": {
        "amount": "789.00",
        "transactionIdentifier": "FBN|API|MX102560|25-07-2023|474512713|693990",
        "message": "Approved by Financial Institution",
        "transactionRef": "503021992595_99550f9c94",
        "responseCode": "00"
    }
}

```

## ```Resend OTP```
Used when OTP fails to deliver.

*Usage*

```python

from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
import logging #If Using Logging instead of print.


        request_key = '617602DFEF417A1C00338E37534F002DC5F433490148696B13D193EC5917345D'

        resend_data = {
            "transactionRef": "1164vy32-332231222476",
            "amount": "10",
        }

        try:
            # Resend OTP
            response = self.hydrogenpay.Card.resendOTP(resend_data, request_key)

            logger.info("OTP Resend Successful:")
            logger.info(json.dumps(response, indent=4))


        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction fails
            self.fail(f"OTP Resend Failed: {e}")


```

*Arguments*

- `amount`: Amount to be charged.
- `transactionRef`: Unique reference for the transaction.

```
```

## ```Confirm Status```
Confirms the status of card transactions.

*Usage*

```python

from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
import logging #If Using Logging instead of print.

        # Transaction reference obtained from a previous payment initiation
        request_key = '617602DFEF417A1C00338E37534F002DC5F433490148696B13D193EC5917345D'

        txRef = "1164vy32-332231222476"  # Replace with an actual reference

        try:
            # Use the SDK to confirm the payment status.
            response = self.hydrogenpay.Card.confirmPurchaseStatus(txRef, request_key)

            logger.info("Status Confirm Successful:")
            logger.info(json.dumps(response, indent=4))


        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction confirmation fails
            self.fail(f"Confirm Status Failed: {e}")

```

*Arguments*

- `transactionRef`: Unique reference for the transaction.

*Returns*

Response Example:

```py

Status Confirm Successful:
{
    "status": "90000",
    "message": null,
    "data": {
        "responseCode": "0000",
        "responseDescription": "Approved by Financial Institution",
        "transactionReference": "2347063908100_49656fafd7",
        "amount": 1000,
        "remittanceAmount": 0,
        "customerName": null,
        "bank": null,
        "status": null,
        "submitTimeUtc": "11/07/2024 10:05:58",
        "clientReferenceInformation": null,
        "accountName": null,
        "accountNo": null,
        "maskedPan": "445653******1096",
        "cardExpiry": "jXLGNL6Jz9iMIFwhQrsdWQ==",
        "transactionId": "53950000-ca6c-aabb-3d5e-08dcf8fa1ecb",
        "completedTimeUtc": "Oct 30th 2024 | 03:47pm",
        "errors": []
    },
    "error": false
}

```

## ```Billing Information```
Process billing information for 3D Secure if response code is H51.

*Usage*

```python

from hydrogenpay_python import Hydrogenpay, HydrogenpayExceptions
import logging #If Using Logging instead of print.


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
            # Use the SDK to aggregate billing information for 3D Secure if the response code is H51.
            response = self.hydrogenpay.Card.aggregateBillingInformation(billing_data, request_key)

            logger.info("Aggregate Bill Infor Successful:")
            logger.info(json.dumps(response, indent=4))


        except HydrogenpayExceptions.TransactionVerificationError as e:
            # Fail the test if transaction fails
            self.fail(f"Aggregate Bill Failed: {e}")

```

*Returns*

Response Example:

```py

{
    "statusCode": "90000",
    "message": "Operation Successful",
    "data": {
        "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI4NGIzZTAwZS1hYmZkLTRlZmItYjFmMi0wOWJkMTU0YjI0OWQiLCJpYXQiOjE3MzAzNzgxMDAsImlzcyI6IjVkZDgzYmYwMGU0MjNkMTQ5OGRjYmFjYSIsImV4cCI6MTczMDM4MTcwMCwiT3JnVW5pdElkIjoiNjQ4MThiZmY3M2M5NjYzNGY0N2JiYTkxIiw",
        "nextActionUrl": "https://centinelapistag.cardinalcommerce.com/V2/Cruise/StepUp",
        "html": null
    }
}

```

**Endpoint Flow Summary For Card Transaction**

- The payment flow varies based on the response code from the purchase call:

***Response Code H01 (OTP Authentication Required):***

- Directs user to an OTP page.

- User inputs the OTP they receive.

- OTP is validated via a separate call.

- Payment status is updated based on OTP validation.

***Response Code H21 (Local Cards - 3D Secure Required):***

- Redirects user to the issuing bank's 3D Secure page.

- Completes 3D Secure authentication.

- Validates the 3D Secure response from the bank.

- Updates the payment status accordingly.

***Response Code H51 (International Cards - 3D Secure with Billing Information):***

- Collects additional billing information from the user.

- Redirects user to the issuing bank's 3D Secure page.

- Completes 3D Secure authentication.

- Validates the bank's response.

- Updates the payment status based on the outcome.


## Testing

All SDK tests are implemented using Python's ```unittest``` module. They currently cover:

```hydrogenpay.PaymentService```
```hydrogenpay.ConfirmPayment```
```hydrogenpay.BankTransfer```
```hydrogenpay.Transfer```
```hydrogenpay.Card```

```sh
Running the Tests

1. Navigate to the tests directory in your terminal.

2. You can run each test file separately using the following command:

python -m unittest test_initiate_payment.py
python -m unittest test_confirm_payment.py
python -m unittest test_initiate_bank_transfer.py
python -m unittest test_simulate_bank_transfer.py

3. Optional: Run All Tests at Once

If you want to run all tests in the tests directory together, you can use the following command:

python -m unittest discover -s tests 

OR

To run specific tests by name, use the following command:

python -m unittest discover -s tests -p "test_card_purchase_confirm_status.py"

```

## Support

For more assistance with this SDK, reach out to the Developer Experience team via [email](mailto:support@hydrogenpay.com) or consult our documentation [here](https://docs.hydrogenpay.com/reference/api-authentication)


## Contribution

If you discover a bug or have a solution to improve the Hydrogen Payment Gateway for the WooCommerce plugin, we welcome your contributions to enhance the code.


Create a detailed bug report or feature request in the "Issues" section.

If you have a code improvement or bug fix, feel free to submit a pull request.

 * Fork the repository on GitHub

 * Clone the repository into your local system and create a branch that describes what you are working on by pre-fixing with feature-name.

 * Make the changes to your forked repository's branch. Ensure you are using PHP Coding Standards (PHPCS).

 * Make commits that are descriptive and breaks down the process for better understanding.

 * Push your fix to the remote version of your branch and create a PR that aims to merge that branch into master.
 
 * After you follow the step above, the next stage will be waiting on us to merge your Pull Request.


## License

By contributing to this library, you agree that your contributions will be licensed under its [MIT license](/LICENSE).
Copyright (c) Hydrogen.


## Hydrogenpay API References

- [Hydrogenpay Dashboard](https://dashboard.hydrogenpay.com/merchant/profile/api-integration)
- [Hydrogenpay API Documentation](https://docs.hydrogenpay.com/reference/api-authentication)