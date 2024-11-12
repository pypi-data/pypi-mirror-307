"""The python wrapper for IQ Option API package setup."""
from setuptools import (setup, find_packages)


setup(
    name="api_iqoption_faria",
    version="8.0.0",
    packages=find_packages(),
    install_requires=["pylint", "requests", "websocket-client==0.56"],
    include_package_data=True,
    description="Best IQ Option API for python creditos: Rafael Faria",
    long_description="Best IQ Option API for python creditos: Rafael Faria",
    url="https://github.com/iqoptionapi/iqoptionapi",
    author="Rafael Faria",
    zip_safe=False
)
