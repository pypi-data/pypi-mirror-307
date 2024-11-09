from setuptools import setup, find_packages

setup(
    name="toffee-flask",
    version="0.1.1",
    author="PiratesTv",
    description="Flask app for Toffee by @PiratesTv",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=2.0",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "toffee-flask=toffee_flask.app:app",
        ],
    },
)
