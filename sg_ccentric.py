import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import json
import hmac
import hashlib

# Load environment variables
load_dotenv()

def check_code_c_centric(imei):
    
    body_string = f'{{"imei":"{imei}"}}'
    print(body_string)
    username = os.getenv('USERNAME1')
    secret = os.getenv('SECRET')
   
    # Get the current date and time in ISO 8601 format
    x_datetime = datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'

    # Function to calculate HMAC-SHA256
    def hmac_sha256(key, data):
        return hmac.new(key.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()

    signing_key = secret + x_datetime
    string_to_sign = f"{x_datetime}\n{body_string}"
    signature = hmac_sha256(signing_key, string_to_sign)

    authorization = f'User:{username},Signature:{signature}'

    # Set headers for the request
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'x-datetime': x_datetime,
        'Authorization': authorization
    }

    # Set the request body
    data = json.loads(body_string)

    # Make the request
    url = 'https://greetme-api.cccsys.co.uk/ccbooking/api/v2/samsung-ref'  # Replace with your actual URL
    response = requests.post(url, json=data, headers=headers)

    json_data = response.text
    parsed_data = json.loads(json_data)

    refnum_value = parsed_data.get('data', {}).get('refnum')

    if refnum_value:
        return(refnum_value)
    elif parsed_data.get('errors', {}).get('imei'):
        refnum_value = parsed_data.get('errors', {}).get('imei')
        return(refnum_value)
    elif parsed_data.get('error'):
        refnum_value = parsed_data.get('error')
        return(refnum_value)
    else:
        return("Error Unknown , contact Administrator")
        

#print('\n***Check Code Samsung C Centrix')

# imei = input("\nPlease enter an IMEI:\n")
# # Call the function
# #check_code_c_centric(imei)
# #imei = "353079701096593"
# print(imei)
# if __name__=="__main__":
#     check_code_c_centric(imei)