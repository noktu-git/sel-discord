import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sel-discord",
    #version="0.0.1",
    author="h0nda",
    author_email="1@1.com",
    description="Discord web API client, using sel-requests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/h0nde/sel-discord",
    packages=setuptools.find_packages(),
    classifiers=[
    ],
    install_requires=[
        "websocket_client",
        "user_agents"
    ],
    python_requires='>=3.6',
)