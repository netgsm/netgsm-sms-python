"""
Netgsm Python SDK setup script.
"""

import os
from setuptools import setup, find_packages

# Read version from __init__.py file
version = ''
with open('netgsm/__init__.py', 'r') as f:
    for line in f:
        if line.startswith('__version__'):
            version = line.split('=')[1].strip().strip('"\'')
            break

# Read long description from README.md
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

# Define dependencies
install_requires = [
    'requests>=2.25.0',
    'python-dotenv>=0.15.0',
]

# Define development dependencies
dev_requires = [
    'pytest>=6.0.0',
    'pytest-cov>=2.10.0',
    'flake8>=3.8.0',
    'black>=20.8b1',
]

setup(
    name='netgsm-sms',
    version=version,
    description='Netgsm Python SDK for SMS API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Netgsm',
    author_email='info@netgsm.com.tr',
    url='https://github.com/netgsm/netgsm-sms-python',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.*', 'examples', 'examples.*']),
    install_requires=install_requires,
    extras_require={
        'dev': dev_requires,
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Communications :: Telephony',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    keywords='netgsm, sms, api, sdk',
    project_urls={
        'Documentation': 'https://github.com/netgsm/netgsm-sms-python/tree/main/docs',
        'Source': 'https://github.com/netgsm/netgsm-sms-python',
        'Tracker': 'https://github.com/netgsm/netgsm-sms-python/issues',
    },
) 