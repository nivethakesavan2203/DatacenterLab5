#!/bin/bash
#!/usr/bin/python
apt-get update
apt-get -y install imagemagick

IMAGE_URL=$(curl http://metadata/computeMetadata/v1/instance/attributes/url -H "Metadata-Flavor: Google")
TEXT=$(curl http://metadata/computeMetadata/v1/instance/attributes/text -H "Metadata-Flavor: Google")
CS_BUCKET=$(curl http://metadata/computeMetadata/v1/instance/attributes/bucket -H "Metadata-Flavor: Google")


mkdir image-output
cd image-output
wget $IMAGE_URL
convert * -pointsize 30 -fill white -stroke black -gravity center -annotate +10+40 "$TEXT" output.png

sudo apt-get update
sudo apt-get install -y python3 python3-pip git
git https://github.com/nivethakesavan2203/DatacenterLab5
cd DatacenterLab5
echo "Came to startup script"
sudo pip3 install --upgrade google-api-python-client
export SERVER_FILE=$(curl http://metadata/computeMetadata/v1/instance/attributes/server-file -H "Metadata-Flavor: Google")
echo $SERVER_FILE | tee service-credentials.json
sudo python3 part3b.py
echo "Run python file"
