import requests
import clearbit

CLEARBIT_SECRET_API_KEY = "sk_6dfb36e62432f0f2652fc411469e3178"
CLEARBIT_PUBLIC_API_KEY = "pk_2391e9f98d6862fbe1fd4045690a14d5"

clearbit.key = CLEARBIT_SECRET_API_KEY

def enrichmentCall(email):
        response = clearbit.Enrichment.find(email=email, stream=True)
        # if response is None:
        #     return

        # if 'person' in response:
        #     print(response['person']['name']['fullName'])

        # if 'company' in response:
        #     print(response['company']['name'])

        
        return response