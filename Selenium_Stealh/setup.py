from setuptools import setup, find_packages

setup(
    name="SeleniumStealth",
    version="1.0.0",
    description="A project created for scraping dynamic websites using selenium and steal",
    author="Darjus Vasiukevic",
    packages=find_packages(),
    install_requires=["requests==2.28.1", "click==8.1.3", "selenium-stealth==1.0.6"],
)
