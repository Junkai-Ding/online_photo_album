import json
import boto3
import requests
import inflect


def lambda_handler(event, context):
    
    print("event: ",event)
    #query_text = "balabu and dogs"
    query_text = event["queryStringParameters"]['q']
    print('query_text: ', query_text)
    client = boto3.client('lexv2-runtime')
    lex_response = client.recognize_text(
            botId='D4DNYZJJFY', # MODIFY HERE
            botAliasId='YAYFEVKV5R', # MODIFY HERE
            localeId='en_US',
            sessionId='testuser',
            text=query_text)
    
    labels = []
    intent = lex_response['sessionState']['intent']
    print("lex_response: ",lex_response)
    #reference: https://pypi.org/project/inflect/
    p = inflect.engine()
    
    if 'slots' in intent:
        slots = intent['slots']
        for key,val in slots.items():
            if val!=None:
                label = val['value']['interpretedValue']
                if p.singular_noun(label):
                    label = p.singular_noun(label)
                labels.append(label)

    print(labels)

    endpoint = 'https://search-photos-s5qn4zliajyen6luy5roy52jae.us-east-1.es.amazonaws.com/'
    auth = ('master','Aws6666-')
    headers = {'Content-Type': 'application/json'}

    photo_paths = []
    
    for label in labels:
        search_url = endpoint + '/_search?q=labels:' + label
        search_res = requests.get(search_url, auth=auth, headers=headers)
        search_res = search_res.json()
        print(search_res)
        for data in search_res['hits']['hits']:
            source = data['_source']
            bucket = source['bucket']
            objkey = source['objectKey']
            
            # check url format
            photo_url = 'https://{}.s3.amazonaws.com/{}'.format(bucket, objkey)
            photo_paths.append(photo_url)
            
    photo_paths = list(set(photo_paths))
    print(photo_paths)

    return {
      "statusCode": 200,
      "headers": {
        "Access-Control-Allow-Origin":"*",
        "Content-Type": "application/json"
      },
      "isBase64Encoded": False,
      "body": json.dumps(photo_paths)
    }

