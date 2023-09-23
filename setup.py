from setuptools import setup

with open("README.md") as f:
    desc = f.read()

setup(
    name='speedruncompy',
    version="0.0.5",
    author="Jamie",
    author_email="jamiebloomfield8@gmail.com",
    description="A wrapper for speedrun.com's new v2 API, as used by their new site",
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/ManicJamie/speedruncompy",
    project_urls={
        "Bug tracker": "https://github.com/ManicJamie/speedruncompy/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.11",
    packages=['speedruncompy'],
    package_data={'': ['.version']},
    include_package_data=True,
    install_requires=[
        'requests'
    ],
)