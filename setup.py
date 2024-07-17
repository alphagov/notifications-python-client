# this restructured text docstring is displayed on https://pypi.org/project/notifications-python-client/
"""
Python API client for GOV.UK Notify - see https://www.notifications.service.gov.uk for more information.

For usage and documentation see https://docs.notifications.service.gov.uk/python.html
"""
import ast
import re

from setuptools import find_packages, setup

# can't just import notifications_python_client.version as requirements may not be installed yet and imports will fail
_version_re = re.compile(r"__version__\s+=\s+(.*)")

with open("notifications_python_client/__init__.py", "rb") as f:
    version = str(ast.literal_eval(_version_re.search(f.read().decode("utf-8")).group(1)))

setup(
    name="notifications-python-client",
    version=version,
    url="https://github.com/alphagov/notifications-python-client",
    license="MIT",
    author="Government Digital Service",
    description="Python API client for GOV.UK Notify.",
    long_description=__doc__,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="gds govuk notify",
    packages=find_packages(include=["notifications_python_client"]),
    include_package_data=True,
    # only support actively patched versions of python (https://devguide.python.org/versions/)
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.0.0",
        "PyJWT>=1.5.1",
        "docopt>=0.3.0",
    ],
)
