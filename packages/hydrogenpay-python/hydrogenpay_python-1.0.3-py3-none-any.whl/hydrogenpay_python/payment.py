import requests
import json
import copy
from hydrogenpay_python.base import HydrogenpayBase
from hydrogenpay_python.exceptions import HydrogenpayError, TransactionChargeError, TransactionVerificationError, TransactionValidationError, ServerError
from hydrogenpay_python.misc import checkIfParametersAreComplete
import logging

response_object = {
    "error": False,
    "transactionComplete": False,
    "txRef": "",
    "status": "",
    "currency": "",
    "chargedamount": 00,
    "chargemessage": "",
    "meta": ""
}


class Payment(HydrogenpayBase):
    """ This is the base class for all the payments """

    def __init__(self, sandboxKey, liveKey, mode, setEnv):
        # Instantiating the base class
        super(
            Payment,
            self).__init__(
            sandboxKey,
            liveKey,
            mode,
            setEnv)

    @classmethod
    def retrieve(cls, mapping, *keys):
        return (mapping[key] for key in keys)

    @classmethod
    def deleteUnnecessaryKeys(cls, response_dict, *keys):
        for key in keys:
            del response_dict[key]
        return response_dict

    def _preliminaryResponseChecks(
            self,
            response,
            TypeOfErrorToRaise,
            txRef=None):
        preliminary_error_response = copy.deepcopy(response_object)
        preliminary_error_response = Payment.deleteUnnecessaryKeys(
            preliminary_error_response,
            "transactionComplete",
            "currency")

        # Check if we can obtain a json
        try:
            responseJson = response.json()
        except BaseException:
            raise ServerError({"error": True, "txRef": txRef, "errMsg": response})

        # Check if the response contains data parameter
        if responseJson.get("data", None):
            if txRef:
                txRef = responseJson["data"].get("transactionRef", None)
        else:
            raise TypeOfErrorToRaise({"error": True,
                                      "txRef": responseJson["data"].get("transactionRef", None),
                                      "errMsg": responseJson.get("message",
                                                                 "Server is down")})

        # Check if it is returning a 200
        if not response.ok:
            errMsg = responseJson.get("message", "Unknown error")
            raise TypeOfErrorToRaise(
                {"error": True, "errMsg": responseJson.get("message", None)})

        return {"json": responseJson,"txRef": txRef} 

        
    def _handleInitiateResponse(self, response, txRef=None, request=None):
        """ This handles transaction charge responses """

        # Perform preliminary checks to validate the response
        res = self._preliminaryResponseChecks(response, TransactionChargeError, txRef=txRef)
        responseJson = res["json"]

        # Check if statusCode is "90000" (indicating success)
        status_code = responseJson.get("statusCode", None)

        if status_code == "90000":
         # Return success response when statusCode is 90000
            return {
                "error": False,
                "status": responseJson.get("status", "No status provided"),  # Handle if status is missing
                "message": responseJson.get("message", "No message provided"),
                "txRef": txRef or responseJson["data"].get("transactionRef", "No transactionRef provided"),
                "authUrl": responseJson["data"].get("url", None)  # Return the URL for further action
            }

        else:
            # Handle failure case when statusCode is not 90000
            return {
                "error": True,
                "message": responseJson.get("message", "No message provided"),
                "statusCode": status_code
            }


    def _handleStimulateBankTransferResponse(self, response, request=None):
        """ This handles transaction simulate responses """

        # Perform preliminary checks to validate the response
        res = self._preliminaryResponseChecks(response, TransactionChargeError)
        responseJson = res["json"]

        # Check if statusCode is "90000" (indicating success)
        status_code = responseJson.get("statusCode", None)

        if status_code == "90000":
         # Return success response when statusCode is 90000
            return {
                "error": False,
                "orderId": responseJson['data'].get("orderId", "No status provided"),  # Handle if status is missing
                "message": responseJson.get("message", "No message provided"),
                "merchantRef": responseJson["data"].get("merchantRef", "No transactionRef provided"),
                "customerEmail": responseJson["data"].get("customerEmail", None),
                "transactionId": responseJson["data"].get("transactionId", None),
                "amount": responseJson["data"].get("amount", None),
                "description": responseJson["data"].get("description", None),
                "currency": responseJson["data"].get("currency", None),
                "merchantInfo": responseJson["data"].get("merchantInfo", None),
                "discountPercentage": responseJson["data"].get("discountPercentage", None),
                "callBackUrl": responseJson["data"].get("callBackUrl", None),
                "isRecurring": responseJson["data"].get("isRecurring", None),
                "frequency": responseJson["data"].get("frequency", None),
                "serviceFees": responseJson["data"].get("serviceFees", None),
                "isBankDiscountEnabled": responseJson["data"].get("isBankDiscountEnabled", None),
                "bankDiscountValue": responseJson["data"].get("bankDiscountValue", None),
                "vatFee": responseJson["data"].get("vatFee", None),
                "vatPercentage": responseJson["data"].get("vatPercentage", None),
                "transactionMode": responseJson["data"].get("transactionMode", None),
            }

        else:
            # Handle failure case when statusCode is not 90000
            return {
                "error": True,
                "message": responseJson.get("message", "No message provided"),
                "statusCode": status_code
            }
  

    # Confirm Response
    def _handleConfirmResponse(self, response, txRef, request=None):
        """ This handles all responses from the confirmation call.\n
             Parameters include:\n
            response (dict) -- This is the response Http object returned from the payment confirm call
         """
        # Perform preliminary checks to validate the response
        res = self._preliminaryResponseChecks(response, TransactionChargeError, txRef=txRef)
        responseJson = res["json"]

        confirm_response = responseJson['data']
        if responseJson.get('statusCode') == "90000":
            # Transaction was successful
            confirm_response["error"] = False
            confirm_response["transactionComplete"] = True
        else:
            # Transaction failed or was incomplete
            confirm_response["error"] = True
            confirm_response["transactionComplete"] = False

        # Return the final confirmation response
        return confirm_response


    # Initiate function (hasFailed is a flag that indicates there is a timeout),
    def initiate(
            self,
            paymentDetails,
            requiredParameters,
            endpoint):
        """ This is the base initiate call. It is usually overridden by implementing classes.\n
             Parameters include:\n
            paymentDetails (dict) -- These are the parameters passed to the function for processing\n
            requiredParameters (list) -- These are the parameters required for the specific call\n
        """
        # Checking for required components
        try:
            checkIfParametersAreComplete(requiredParameters, paymentDetails)
        except BaseException:
            raise

        # Performing shallow copy of payment details to prevent tampering with original payment details
        paymentDetails = copy.copy(paymentDetails)

        # Request headers
        headers = {
            'Authorization': self._getLiveKey(),
            'content-type': 'application/json',
        }

        response = requests.post(
            endpoint, headers=headers, data=json.dumps(paymentDetails))

        # Log if the response is ok
        if response.ok:
            responseTime = response.elapsed.total_seconds()
            logging.info(f"Response OK: {responseTime}s")
        else:
            responseTime = response.elapsed.total_seconds()
            logging.error(f"Response Failed: {response.status_code}, Time: {responseTime}s")

        return self._handleInitiateResponse(
                response, paymentDetails)
    

    # Confirm Card Purchase Response
    def _handleConfirmPurchaseStatusResponse(self, response, request=None):
        """ This handles all responses from the confirm staus call.\n
             Parameters include:\n
            response (dict) -- This is the response Http object returned from the payment confirm call
         """
        
        responseJson = self._preliminaryResponseChecks(
            response, TransactionValidationError)

        transactionRef = responseJson["data"]["transactionReference"]
        responseJsonData = responseJson["data"]

        # If all preliminary checks passed
        if responseJsonData["responseCode"] != "0000":
            transactionRef = responseJsonData["transactionReference"]
            errMsg = responseJsonData["responseDescription"]
            raise TransactionValidationError({
                "error": True,
                "transactionRef": transactionRef,
                "errMsg": errMsg
            })
    
        else:
            return {
                "status": responseJson["statusCode"],
                "message": responseJson["message"],
                "data": responseJsonData,
                "error": False,
            }

     # Validate 3DSecure Response
    def _handleValidate3DSecureResponse(self, response, request=None):
        """ This handles all responses from the 3DSecure Validation call.\n
             Parameters include:\n
            response (dict) -- This is the response Http object returned from the payment confirm call
         """
        
        responseJson = self._preliminaryResponseChecks(
            response, TransactionValidationError)

        transactionRef = responseJson["data"]["transactionRef"]
        responseJsonData = responseJson["data"]

        # If all preliminary checks passed
        if responseJsonData["responseCode"] != "00":
            transactionRef = responseJsonData["transactionReference"]
            errMsg = responseJsonData["responseDescription"]
            raise TransactionValidationError({
                "error": True,
                "transactionRef": transactionRef,
                "errMsg": errMsg
            })
    
        else:
            return {
                "status": responseJson["statusCode"],
                "message": responseJson["message"],
                "data": responseJsonData,
                "error": False,
            }


    def simulatetransfer(
            self,
            paymentDetails,
            requiredParameters,
            endpoint):
        """ This is the base initiation call. It is usually overridden by implementing classes.\n
             Parameters include:\n
            paymentDetails (dict) -- These are the parameters passed to the function for processing\n
            requiredParameters (list) -- These are the parameters required for the specific call\n
        """
        # Checking for required components
        try:
            checkIfParametersAreComplete(requiredParameters, paymentDetails)
        except BaseException:
            raise

        # Performing shallow copy of payment details to prevent tampering with original payment details
        paymentDetails = copy.copy(paymentDetails)

        # Request headers
        headers = {
            'Authorization': self._getLiveKey(),
            'Mode': str(19289182),
            'content-type': 'application/json',
        }

        response = requests.post(
            endpoint, headers=headers, data=json.dumps(paymentDetails))
            
        if response.ok:
            responseTime = response.elapsed.total_seconds()
            logging.info(f"Response OK: {responseTime}s")
        else:
            responseTime = response.elapsed.total_seconds()
            logging.error(f"Response Failed: {response.status_code}, Time: {responseTime}s")

        return self._handleStimulateBankTransferResponse(
                response, paymentDetails)
    

    def _handleResendOtpResponse(self, response, request=None):
        """ This handles Otp Resend responses """

        responseJson = self._preliminaryResponseChecks(
            response, TransactionValidationError)

        transactionRef = responseJson["data"]["transactionRef"]
        responseJsonData = responseJson["data"]
        responseCode = responseJson["data"]["responseCode"]

        # If all preliminary checks passed
        if responseJsonData["responseCode"] != "T0":
            transactionRef = responseJsonData["transactionRef"]
            errMsg = responseJsonData["message"]
            raise TransactionValidationError({
                "error": True,
                "transactionRef": transactionRef,
                "errMsg": errMsg
            })
    
        else:
            return {
                "status": responseJson["statusCode"],
                "message": responseJson["message"],
                "data": responseJsonData,
                "error": False,
            }

    def _handleAggregateBillingInfoResponse(self, response, request=None):
        """ This Aggregate Billing Information responses """

        responseJson = self._preliminaryResponseChecks(
            response, TransactionValidationError)

        responseJsonData = responseJson["data"]

        # If all preliminary checks passed
        if responseJsonData is None:
            statusCode = responseJson["statusCode"]
            errMsg = responseJsonData["message"]
            raise TransactionValidationError({
                "error": True,
                "statusCode": statusCode,
                "errMsg": errMsg
            })
    
        else:
            return {
                "status": responseJson["statusCode"],
                "message": responseJson["message"],
                "data": responseJsonData,
                "error": False,
            }


    def confirmpayment(self, txRef, endpoint):
        """
            This is used to check the status of a transaction.
        Parameters:
            txRef (string): The transaction reference that was passed to the payment call. 
            If you didn't define a reference, you can access the auto-generated
            endpoint (string): The API endpoint to confirm the payment.
        """    
    # Prepare request headers
        headers = {
                'Authorization': self._getLiveKey(), 
                'content-type': 'application/json',
        }
        
    # Prepare the request payload containing the transaction reference
        payload = {
            "transactionRef": txRef  # Pass the transaction reference in the correct format
        }
    
        try:
            response = requests.post(endpoint, headers=headers, data=json.dumps(payload)) # Serialize the payload to JSON
        # Handle the confirmation response
            if response.ok:
                # If successful, handle the response
                return self._handleConfirmResponse(response, txRef)
            else:
            # If the response fails, log the error
                print(f"Error during confirmation: {response.status_code} - {response.text}")
                return None  # Or raise an exception based on your error handling needs

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            print(f"Request failed: {e}")
            return None
        
   
    def card(self, endpoint):
         """ Handles card-specific transactions client key """
         headers = {
             'Authorization': self._getLiveKey(),
             'content-type': 'application/json',
         }

         response = requests.get(endpoint, headers=headers)

         if response.ok:
             return self._preliminaryResponseChecks(response, TransactionChargeError)

         else:
             logging.error(f"Failed card transaction clinetkey with status code: {response.status_code}")
             raise TransactionChargeError({"error": True, "message": "Failed to process card transaction clinetkey generation"})
         

    def _handleValidateOtpResponse(self, response, request=None):
        """ This handles validation responses """

        responseJson = self._preliminaryResponseChecks(
            response, TransactionValidationError)

        transactionRef = responseJson["data"]["transactionRef"]
        responseJsonData = responseJson["data"]
        # If all preliminary checks passed
        if responseJsonData["responseCode"] != "00":
            transactionRef = responseJsonData["transactionRef"]
            errMsg = responseJsonData["message"]
            raise TransactionValidationError({
                "error": True,
                "transactionRef": transactionRef,
                "errMsg": errMsg
            })
    
        else:
            return {
                "status": responseJson["statusCode"],
                "message": responseJson["message"],
                "data": responseJsonData,
                "error": False,
            }
         

    def purchase(self, transactionDetails, requiredParameters, endpoint, RequestKey):
        """ Handles card-specific transactions client key """

        # Checking for required parameters
        try:
            checkIfParametersAreComplete(requiredParameters, transactionDetails)

        except BaseException:

            raise

         # Performing shallow copy of payment details to prevent tampering with original payment details
        transactionDetails = copy.copy(transactionDetails)

        headers = {
            'Authorization': self._getLiveKey(),
            'RequestKey': RequestKey,
            'content-type': 'application/json',
        }
        
        # Send the POST request to the API endpoint
        response = requests.post(
            endpoint, headers=headers, json=transactionDetails
        )
        
        if response.ok:
            return self._preliminaryResponseChecks(response, TransactionChargeError)

        else:
            logging.error(f"Failed card purchase: {response.status_code}")
            raise TransactionChargeError({"error": True, "message": "Failed to process card purchase"})
        
    # Validate Otp
    def validateOtp(self, validateData, requiredParameters, endpoint, requestKey):
        """ This is the base validate call.\n
             Parameters include:\n
            transactionRef (string) -- This is the hydrogen reference returned from a successful initiate call\n
            otp (string) -- This is the otp sent to the user \n
        """

        # Checking for required parameters
        try:
            checkIfParametersAreComplete(requiredParameters, validateData)

        except BaseException:

            raise

        headers = {
            'Authorization': self._getLiveKey(),
            'RequestKey': requestKey,
            'content-type': 'application/json',
        }

        # Send the POST request to the API endpoint
        response = requests.post(
            endpoint,
            headers=headers,
            data=json.dumps(validateData))
                
        if response.ok:
            return self._handleValidateOtpResponse(response)

        else:
            logging.error(f"Failed purchase validate: {response.status_code}")
            raise TransactionChargeError({"error": True, "message": "Failed to process purchase card validation"})
        

    # Resend Otp
    def resendOTP(self, resendData, requiredParameters, endpoint, requestKey):
        """ This is the base OTO Resend call.\n
            Parameters include:\n
            transactionRef (string) -- This is the hydrogen reference returned from a successful initiate call\n
            amount (string) -- This is the amount sent to the user \n
        """

        # Checking for required parameters
        try:
            checkIfParametersAreComplete(requiredParameters, resendData)

        except BaseException:

            raise

        headers = {
            'Authorization': self._getLiveKey(),
            'RequestKey': requestKey,
            'content-type': 'application/json',
        }

        # Send the POST request to the API endpoint
        response = requests.post(
            endpoint,
            headers=headers,
            data=json.dumps(resendData))
                
        if response.ok:
            return self._handleResendOtpResponse(response)

        else:
            logging.error(f"Failed purchase Resend OTP: {response.status_code}")
            raise TransactionChargeError({"error": True, "message": "Failed to process Otp Resend"})
        

    def confirmPurchaseStatus(self, txRef, endpoint, requestKey):
        """
            This is used to check the card purchase status of the transaction.
        Parameters:
            txRef (string): The transaction reference that was passed to the payment call. 
            If you didn't define a reference, you can access the auto-generated
            endpoint (string): The API endpoint to confirm the payment.
        """
    # Prepare request headers

        headers = {
            'Authorization': self._getLiveKey(),
            'RequestKey': requestKey,
            'content-type': 'application/json',
        }
        
    # Prepare the request payload containing the transaction reference
        payload = {
            "transactionRef": txRef  # Pass the transaction reference in the correct format
        }
    
        try:
            response = requests.post(endpoint, headers=headers, data=json.dumps(payload)) # Serialize the payload to JSON
        # Handle the confirm status response
            if response.ok:
                # If successful, handle the response
                return self._handleConfirmPurchaseStatusResponse(response)
            
            else:
            # If the response fails, log the error
                print(f"Error during confirm status: {response.status_code} - {response.text}")
                return None  # Or raise an exception based on your error handling needs

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            print(f"Confirm Status failed: {e}")
            return None
        

    def validate3DSecure(self, txRef, endpoint, requestKey):
        """
            This is used to validate 3DSecure .
            Parameters:
            txRef (string): The transaction reference that was passed to the payment call. 
            If you didn't define a reference, you can access the auto-generated
            endpoint (string): The API endpoint to confirm the payment.
        """
    # Prepare request headers

        headers = {
            'Authorization': self._getLiveKey(),
            'RequestKey': requestKey,
            'content-type': 'application/json',
        }
        
    # Prepare the request payload containing the transaction reference
        payload = {
            "transactionRef": txRef  # Pass the transaction reference in the correct format
        }
    
        try:
            response = requests.post(endpoint, headers=headers, data=json.dumps(payload)) # Serialize the payload to JSON
        # Handle the validate response
            if response.ok:
                # If successful, handle the 3DSecure response
                return self._handleValidate3DSecureResponse(response)
            
            else:
            # If the response fails, log the error
                print(f"Error during 3dSecure Validation: {response.status_code} - {response.text}")
                return None  # Or raise an exception based on your error handling needs

        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the request
            print(f"3dSecure Dalidation Failed: {e}")
            return None
        

    # Aggregate Billing Information
    def aggregateBillingInformation(self, billingInfoData, requiredParameters, endpoint, requestKey):
        """ This Process billing information for 3D Secure if response code is H51\n
            Parameters include:\n
            transactionRef (string) -- This is the hydrogen reference returned from a successful initiate call\n
            phoneNumber":\n
            email:\n
            country:\n
            countryCode:\n
            postalCode:\n
            administrativeArea:\n
            locality:\n
            address1:\n
            lastName:\n
            firstName:\n
            callBackUrl:\n
        """

        # Checking for required parameters
        try:
            checkIfParametersAreComplete(requiredParameters, billingInfoData)

        except BaseException:
            raise

        headers = {
            'Authorization': self._getLiveKey(),
            'RequestKey': requestKey,
            'content-type': 'application/json',
        }

        # Send the POST request to the API endpoint
        response = requests.post(
            endpoint,
            headers=headers,
            data=json.dumps(billingInfoData))
                
        if response.ok:
            return self._handleAggregateBillingInfoResponse(response)

        else:
            logging.error(f"Failed Aggregate Bill Info: {response.status_code}")
            raise TransactionChargeError({"error": True, "message": "Failed Aggregate Bill Info"})