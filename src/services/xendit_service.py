from datetime import  datetime, timedelta
import xendit
from xendit.apis import PaymentRequestApi
from dotenv import load_dotenv
import os

load_dotenv()
XENDIT_API_KEY = os.getenv('XENDIT_API_KEY_TEST')
xendit.set_api_key(XENDIT_API_KEY)

api_client = xendit.ApiClient()

api_instance = PaymentRequestApi(api_client)

# this key are optional parameter
# idempotency_key = "5f9a3fbd571a1c4068aa40ce"
# for_user_id = "5f9a3fbd571a1c4068aa40cf" 
# with_split_rule = "splitru_c676f55d-a9e0-47f2-b672-77564d57a40b" 

def create_payment_va(customer_name: str, amount: float):
    payment_request_parameters = {
        "reference_id" : "example-ref-1234",
        "currency" : "IDR",
        "amount" : amount,
        "country" : "ID",
        "payment_method" : {
            "type" : "VIRTUAL_ACCOUNT",
            "reusability" : "ONE_TIME_USE",
            "reference_id" : "example-1234",
            "virtual_account" : {
                "channel_code" : "BNI",
                "channel_properties" : {
                    "customer_name" : customer_name,
                    "expires_at" : "2024-12-23T18:25:00.000Z",
                }
            }
        },
        "metadata" : {
            "sku" : "example-sku-1234"
        }
    }

    try:
        api_response = api_instance.create_payment_request(
            # idempotency_key = idempotency_key,
            # for_user_id = for_user_id,
            # with_split_rule = with_split_rule,
            payment_request_parameters = payment_request_parameters
            )
        return api_response
    except xendit.XenditSdkException as e:
        print("Exception when calling PaymentRequestApi->create_payment_request: %s\n" % e)

def create_payment_ewallet(amount: float):
    payment_request_parameters = {
        "reference_id" : "example-ref-1234",
        "currency" : "IDR",
        "amount" : amount,
        "country" : "ID",
        "payment_method" : {
            "type" : "EWALLET",
            "reusability": "ONE_TIME_USE",
            "ewallet" : {
                "channel_code" : "SHOPEEPAY",
                "channel_properties" : {
                    "success_return_url": "https://your-redirect-website.com/success"
                }
            },
        }
    }

    try:
        api_response = api_instance.create_payment_request(
            # idempotency_key = idempotency_key,
            # for_user_id = for_user_id,
            # with_split_rule = with_split_rule,
            payment_request_parameters = payment_request_parameters
            )
        return api_response
    except xendit.XenditSdkException as e:
        print("Exception when calling PaymentRequestApi->create_payment_request: %s\n" % e)


