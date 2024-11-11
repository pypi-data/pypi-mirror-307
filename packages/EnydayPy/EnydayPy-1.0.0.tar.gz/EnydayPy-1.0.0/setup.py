from setuptools import setup, find_packages  # noqa: H301

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools
NAME = "EnydayPy"
VERSION = "1.0.0"
PYTHON_REQUIRES = ">= 3.8"
REQUIRES = [
    "urllib3 >= 1.25.3, < 3.0.0",
    "python-dateutil >= 2.8.2",
    "pydantic >= 2",
    "typing-extensions >= 4.7.1",
]

setup(
    name=NAME,
    version=VERSION,
    description="Enyday API",
    author="Bruno Adam",
    author_email="bruno.adam@pm.me",
    url="https://github.com/bruadam/EnydayPy",
    keywords=["OpenAPI", "OpenAPI-Generator", "Enyday API"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type='text/markdown',
    long_description="""\
    This API allows integration with the Enyday platform, providing access to user authentication, user details, authorization data, address information, and power consumption data. It helps in integrating Enyday into platforms like Home Assistant. 
    """,
    package_data={"openapi_client": ["py.typed"]},
)
