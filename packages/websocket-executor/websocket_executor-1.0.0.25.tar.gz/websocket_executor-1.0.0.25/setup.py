from setuptools import setup

setup(
    name='websocket_executor',
    version='1.0.0.25',
    packages=['websocket_executor'],
    include_package_data=True,
    install_requires=[
        "channels~=4.1.0; python_version >= '3.8'",
        "cryptography~=43.0.3; python_version >= '3.7'",
        "daphne~=4.1.2; python_version >= '3.8'",
        "django~=4.2.16; python_version >= '3.8'",
        "djangorestframework~=3.15.2; python_version >= '3.8'",
        "vm-custom-package~=0.1.5.102",
        "websocket-client~=1.8.0; python_version >= '3.8'",
        "websockets~=13.1; python_version >= '3.8'"
    ],
)

