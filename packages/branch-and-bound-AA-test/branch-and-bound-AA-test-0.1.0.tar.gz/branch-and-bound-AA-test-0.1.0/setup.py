from setuptools import setup, find_packages

setup(
    name="branch-and-bound-AA-test",           
    version="0.1.0",                     
    author="Markus Schmidt",
    author_email="freedomTraderFinance@gmail.com",
    description="A knapsack problem solved with branch and bound",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
