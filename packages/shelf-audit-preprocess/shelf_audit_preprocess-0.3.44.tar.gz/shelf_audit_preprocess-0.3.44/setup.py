import os
from setuptools import setup, find_packages
build_number = os.getenv('BUILD_NUMBER', '0')

# Get package version
#with open("VERSION.txt") as version_file:
#    version = version_file.read().strip()

setup(
    name='shelf_audit_preprocess',
    version=f'0.3.{build_number}',
    # version=version,
    # version='0.3.{build_number}'.format(build_number=currentBuild.getNumber()),
    packages=find_packages(),
    description='Pre processing for model training.',
    author='Blackstraw',
    author_email='arshpreet.singh@blackstraw.ai',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    install_requires=[
        'albumentations==1.4.11',
        'matplotlib',
        'numpy',
        'opencv-python==4.10.0.84',
        'opencv-python-headless==4.10.0.84',
        'tqdm==4.66.4'
    ],
)
