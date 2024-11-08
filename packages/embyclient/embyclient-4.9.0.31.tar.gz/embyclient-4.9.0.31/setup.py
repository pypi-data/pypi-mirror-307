import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


VERSION = "4.9.0.31"
REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]


classifiers = [
    'Intended Audience :: Developers',  # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'Topic :: Multimedia :: Video',
    'Topic :: Multimedia',
    'Topic :: Internet :: WWW/HTTP',
    'Operating System :: OS Independent'
]

setuptools.setup(
    name="embyclient",
    packages=setuptools.find_packages(exclude=["tests"]),
    include_package_data=True,
    version=VERSION,
    install_requires=REQUIRES,
    description="A Python client for Emby Media Server's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://emby.media",
    keywords=["Emby", "Rest", "API", "client", "media", "server", "JSON"],
    classifiers=classifiers,
)
