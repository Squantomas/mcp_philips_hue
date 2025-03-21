from setuptools import setup, find_packages

setup(
    name="hue-mcp-server",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "aiohttp",
        "pyyaml",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Ein Backend-Server zur Steuerung von Philips Hue über MCP im LAN",
    keywords="philips, hue, mcp, home-automation",
    python_requires=">=3.7",
)
