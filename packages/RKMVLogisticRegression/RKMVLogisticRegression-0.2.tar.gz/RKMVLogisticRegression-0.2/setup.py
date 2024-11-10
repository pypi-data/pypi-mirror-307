# setup.py

from setuptools import setup, find_packages

setup(
    name='RKMVLogisticRegression',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    description='A package for Encrypted Logistic Regression',
    author='Rajdip Bera',
    author_email='rajdipbera2002@gmail.com',
    url='https://github.com/Me-Rajdip/RKMVLogisticRegression',  # Update with your repository URL
)
