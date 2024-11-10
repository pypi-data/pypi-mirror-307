from setuptools import setup, find_packages

setup(
    name="journ_app",
    version="1.0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "journ=journ.main:main",
        ]
    },
    python_requires=">=3.6",
)
