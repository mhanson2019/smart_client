from setuptools import setup, find_packages

setup(
    name='smart_client',
    version='0.1',
    description='SmartSheet API client wrapper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author = 'Michael Hanson',
    author_email = 'michael.hanson@atelier-therapeutics.com',
    url = 'https://github.com/mhanson2019/smart_client',
    packages=find_packages(),
    install_requires=[
        'smartsheet-python-sdk',
        'KeyManagement @ git+http://github.com/mhanson2019/KeyManagement.git@main#egg=KeyManagement-0.1'
    ],
    dependency_links=[
        'http://github.com/mhanson2019/KeyManagement/tarball/master#egg=KeyManagement-0.1'
    ],
    python_requires='>=3.6',
    
)