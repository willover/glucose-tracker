#!/bin/bash

# Build 'base' image. Must be built first as all other images depend on it.
cd base
docker build -t jcalazan/base --no-cache .
cd ..

# Build 'postgresql' image.
cd postgresql
docker build -t jcalazan/postgresql --no-cache .
cd ..

# Build 'django' image.
cd django
docker build -t jcalazan/django --no-cache .
cd ..
