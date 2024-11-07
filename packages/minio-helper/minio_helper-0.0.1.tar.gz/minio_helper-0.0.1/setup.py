from setuptools import setup, find_packages

setup(
    name="minio_helper",
    version="0.0.1",  # update version if re-uploading
    packages=find_packages(),
    install_requires=[
        # "minio",
    ],
    # Include README as the long description
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    # Other metadata
    description="Minio helper utility for digital-club project",
    author="Frank Maduka",
    license="MIT",
    # Include README and LICENSE files in the distribution
    include_package_data=True,
)


# python setup.py sdist bdist_wheel 
# pip install setuptools wheel twine
# pip install --upgrade setuptools wheel
# python setup.py sdist bdist_wheel

# After try to install it locally. 
# pip install dist/minio_helper-0.1-py3-none-any.whl
# twine upload dist/*
# twine upload --skip-existing dist/*

# HOW TO USE THE PACKAGE AFTER INSTALLATION 
# from minio_helper import get_signed_urlsigned_url = get_signed_url('/clubs-media/myfile.jpg', 24) 


