import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="acrome-smd",
    version="2.0.6",
    author="Furkan Kırlangıç",
    author_email="furkankirlangic@acrome.net",
    description="Python library for interfacing with Acrome Smart Motion Devices (SMD) products.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Acrome-Smart-Motion-Devices/python-library",
    project_urls={
        "Bug Tracker": "https://github.com/Acrome-Smart-Motion-Devices/python-library/issues",
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(exclude=['tests', 'test']),
    install_requires=["pyserial>=3.5", "stm32loader>=0.5.1", "crccheck>=1.3.0", "requests>=2.31.0", "packaging>=23.2"],
    python_requires=">=3.7"
)
