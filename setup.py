# this restructured text docstring is displayed on https://pypi.python.org/pypi/notifications-python-client/
"""
Python API client for GOV.UK Notify - see https://www.notifications.service.gov.uk for more information.

For usage and documentation see https://docs.notifications.service.gov.uk/python.html
"""
import re
import ast
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

# can't just import notifications_python_client.version as requirements may not be installed yet and imports will fail
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('notifications_python_client/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


class IntegrationTestCommand(TestCommand):
    user_options = []

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ''

    def run_tests(self):
        import shlex
        import sys
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args) + ['integration_test/integration_tests.py'])
        sys.exit(errno)


setup(
    name='notifications-python-client',
    version=version,
    url='https://github.com/alphagov/notifications-python-client',
    license='MIT',
    author='Government Digital Service',
    description='Python API client for GOV.UK Notify.',
    long_description=__doc__,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='gds govuk notify',

    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        'requests>=2.0.0',
        'PyJWT>=1.5.1',
        'docopt>=0.3.0',
        'monotonic>=0.1',
        'future',
    ],
    # for running pytest as `python setup.py test`, see
    # http://doc.pytest.org/en/latest/goodpractices.html#integrating-with-setuptools-python-setup-py-test-pytest-runner
    setup_requires=[
        'pytest-runner'
    ],
    cmdclass={'integration_test': IntegrationTestCommand},
)
