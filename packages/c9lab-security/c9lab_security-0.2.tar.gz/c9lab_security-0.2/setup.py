from setuptools import setup, find_packages

setup(
    name='c9lab-security',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
        'pycryptodome',
    ],
    include_package_data=True,
    description='Middleware for encrypting and decrypting requests and responses in Django Rest Framework',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',
    author='C9lab',
    author_email='praveen.dhakad@pinakinfosec.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
