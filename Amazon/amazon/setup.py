from setuptools import setup, find_packages

setup(
    name='AmazonCrawler',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'scrapy',
        'scrapeops-scrapy-proxy-sdk',  # Add ScrapeOps Scrapy Proxy SDK if required
        # Add any other dependencies here
    ],
)
