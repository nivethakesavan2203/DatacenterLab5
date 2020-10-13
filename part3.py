#!/usr/bin/env python

import argparse
import os
import time
from pprint import pprint

import googleapiclient.discovery
import google.auth
import google.oauth2.service_account as service_account

#
# Use Google Service Account - See https://google-auth.readthedocs.io/en/latest/reference/google.oauth2.service_account.html#module-google.oauth2.service_account
#
credentials = service_account.Credentials.from_service_account_file(filename='service-credentials.json')
project = os.getenv('GOOGLE_CLOUD_PROJECT') or 'datacenter-292201'
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

#
# Stub code - just lists all instances
#
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

print("Your running instances are:")
for instance in list_instances(service, project, 'us-west1-b'):
    print(instance['name'])