#!/usr/bin/env python
from setuptools import setup


packages = [
    'statsd_redis_monitor',
]

requires = [
    'redis>=2.10.5',
    'statsd==3.2.1',
]


setup(
    name='statsd-redis-monitor',
    description="AWS Lambda Function to get data stats out of Redis and into Statsd",
    version='0.1.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Operating System :: Unix',
    ],
    author='Craig Weber',
    author_email='crgwbr@gmail.com',
    url='https://github.com/crgwbr/statsd-redis-monitor',
    license='ISC',
    packages=packages,
    install_requires=requires,
)
