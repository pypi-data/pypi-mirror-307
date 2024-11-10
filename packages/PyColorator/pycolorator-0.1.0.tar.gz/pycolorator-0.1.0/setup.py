from setuptools import setup, find_packages

setup(
    name='PyColorator',
    version='0.1.0',
    author='borgox',
    author_email='',
    description='A lightweight python library to easily colorate text',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/borgox/PyColorate',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)