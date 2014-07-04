#!/bin/bash

cd ../deployment/ansible

ansible-playbook -i www.glucosetracker.net, production.yml --tags="deploy" --ask-vault-pass
