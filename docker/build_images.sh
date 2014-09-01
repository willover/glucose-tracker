#!/bin/bash

# Build 'base' image. Must be built first as all other images depend on it.
cd base
docker build -t jcalazan/base .
cd ..

# Build 'postgresql' image.
cd postgresql
docker build -t jcalazan/postgresql .
cd ..

# Build 'django' image.
cd django
docker build -t jcalazan/django .
cd ..