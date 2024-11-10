from setuptools import setup, find_packages

setup(
    name="opencommerce-sdk",
    version="1.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "web3>=6.0.0",
        "eth-account>=0.8.0",
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
    ],
    python_requires=">=3.7",
)