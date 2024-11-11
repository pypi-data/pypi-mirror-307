import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="SEOTool",
    version="1.4",
    author="Jiayu Tan",
    author_email="jtan010@uottawa.ca",
    description="Some scripts for Baidu SEO purpose",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=['fake-useragent>=1.5.1',
                      'requests>=2.32.3',
                      'lxml>=5.3.0'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)