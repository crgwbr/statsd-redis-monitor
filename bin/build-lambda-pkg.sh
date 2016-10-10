#!/usr/bin/env bash

PKGNAME="statsd-redis-monitor-$(python setup.py --version).zip"

mkdir -p dist/ build/

cd build

cp ../requirements.txt ./requirements.txt
cp ../statsd_redis_monitor/*.py ./

virtualenv ENV
source  ENV/bin/activate
pip install -r requirements.txt
deactivate

mv ENV/lib/python2.7/site-packages/* .
rm -rf ./ENV

rm -f "../dist/$PKGNAME"
zip -r "../dist/$PKGNAME" .

cd ..
