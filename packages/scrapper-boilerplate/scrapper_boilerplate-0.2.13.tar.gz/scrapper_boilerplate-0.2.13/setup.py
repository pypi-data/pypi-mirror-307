from setuptools import setup, find_packages


setup(
    name="scrapper-boilerplate",
    version="0.2.13",
    description="Scrapping/Automating tools, userSwitching, anti-bot detection and more...",
    long_description_content_type="text/markdown",
    long_description=open('README.md', encoding='utf-8').read(),
    url="https://github.com/mx-jeff/scrapper-boilerplate",
    author="Jeferson/MxJeff",
    author_email="mx.jeferson.10@hotmail.com",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "selenium", 
        "requests", 
        "pandas", 
        "beautifulsoup4", 
        "python-dotenv", 
        "python-telegram-bot",
        "lxml",
        "webdriver-manager",
        "openpyxl",
        "pytest"
    ]
)