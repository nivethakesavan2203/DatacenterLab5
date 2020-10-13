#!/usr/bin/env python
import argparse
import os 
import json
import time
from pprint import pprint
import googleapiclient.discovery
import google.auth
import google.oauth2.service_account as service_account

#[Using the service credentials json file as credential]
project = os.getenv('GOOGLE_CLOUD_PROJECT') or 'datacenter-292201'
credentials = service_account.Credentials.from_service_account_file(filename='service-credentials.json')
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

# [START wait_for_operation]
def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()
        print(result)
        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result
        time.sleep(1)

# [END wait_for_operation]

# [START create_instance]
def create_instance(compute, project, zone, name, bucket):
    # Get the latest Debian Jessie image.
    image_response = compute.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-1804-lts').execute()
    source_disk_image = image_response['selfLink']
    # Configure the machine
    machine_type = "zones/%s/machineTypes/f1-micro" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup-script2.sh'), 'r').read()
    image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
    image_caption = "Ready for dessert?"
    config = {
        'name': name,
        'machineType': machine_type,
        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image
                }
            }
        ],
        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],
        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],
        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }, {
                'key': 'url',
                'value': image_url
            }, {
                'key': 'text',
                'value': image_caption
            }, {
                'key': 'bucket',
                'value': bucket
            }]
        }
    }
    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]

# [List the instances]
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

def setTag(compute, project_id, zone , instance):
    # Sets the http and https tags to allow traffic
    data = compute.instances().get(project=project_id,zone=zone,instance=instance).execute()
    tags = data ['tags']
    fingerprint = tags['fingerprint']
    # Waits for the operation to complete.
    #body['fingerprint'] = fingerprint
    body = {
        'items':[
            'allow-5000'
            ],
        'fingerprint': fingerprint
    }   
    # Waits for the operation to complete.
    request = compute.instances().setTags(project=project_id, zone=zone, instance=instance, body=body).execute()
    
project = "datacenter-292201"
zone = "us-west1-b"
inside_instanceName = "part3-instance-2"
create_instance(service,project,zone,inside_instanceName,"dcsc")
setTag(service,"datacenter-292201","us-west1-b",inside_instanceName)
print("Running instances are")
for instance in list_instances(service, project, 'us-west1-b'):
    print(instance['name'])