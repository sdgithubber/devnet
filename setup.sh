#!/bin/sh
wget -O terraform.zip https://releases.hashicorp.com/terraform/0.11.7/terraform_0.11.7_linux_amd64.zip
unzip terraform.zip
rm -rf terraform.zip
sudo mv terraform /usr/local/bin
sudo chmod +x /usr/local/bin/terraform
