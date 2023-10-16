import boto3
import json
import datetime
import requests
import inflect


s3_client = boto3.client('s3')
rek_client = boto3.client('rekognition', region_name='us-east-1')

def lambda_handler(event, context):
    # test demo
    # print("event")
    # print(event)
    s3 = event['Records'][0]['s3']
    
    # print("s3")
    # print(s3)
    bucket = s3['bucket']['name']
    photo = s3['object']['key']
    print(photo, bucket)
    
    # get metadata from s3
    Obj = s3_client.head_object(Bucket=bucket, Key=photo)
    print(Obj)
    metadata = Obj['Metadata']
    last_modify = Obj['LastModified']

    labels = []
    
    # upload photos from S3/API gateway/Frontend
    for key, val in metadata.items():
        labellist = str(val).split(', ')
        for label_i in labellist:
            if(',' in str(label_i)): # multiple labels
                templist = str(label_i).split(',')
                for i in templist:
                    if(str(i).lower() not in labels):
                        labels.append(str(i).lower())
            else: # just one label
                if(str(label_i).lower() not in labels):
                    labels.append(str(label_i).lower())
            
     # get the labels of photo
    Rek_dected_labels = rek_client.detect_labels(Image={'S3Object': {'Bucket': bucket,
    'Name': photo}}, MinConfidence=70) #MaxLabels = 12
    Rek_labels = Rek_dected_labels['Labels']
        
    #reference: https://pypi.org/project/inflect/
    p = inflect.engine()
    
    for i in range(len(Rek_labels)):
        reklabel = Rek_labels[i]['Name'].lower()
        if p.singular_noun(reklabel):
            reklabel = p.singular_noun(reklabel)
        if(reklabel not in labels):
            labels.append(reklabel)
        
    print(labels)
    
    # create JSON object 
    json_object = {
        "objectKey": photo,
        "bucket": bucket,
        "createdTimestamp": last_modify.strftime("%y-%m-%d %H:%M:%S"),
        "labels": labels
    }
    

    # upload data to OpenSearch
    endpoint = 'https://search-photos-s5qn4zliajyen6luy5roy52jae.us-east-1.es.amazonaws.com/photo/_doc'
    headers = {'Content-Type': 'application/json'}
    auth = ('master','Aws6666-')
    
    # region = 'us-east-1'
    # service = 'es'
    # credentials = boto3.Session().get_credentials()
    # awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, 
    #             region, service, session_token=credentials.token)
                
    response = requests.post(endpoint, json = json_object, auth = auth, headers = headers)
    print(response)
    return {'response': str(response)}
