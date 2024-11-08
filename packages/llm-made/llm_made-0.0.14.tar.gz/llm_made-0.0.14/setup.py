from setuptools import setup, find_packages


setup(
    name="llm_made",
    version="0.0.14",
    description="multi-agent development",
    author="onebottlekick",
    author_email="gksqudcks97@gmail.com",
    url="https://github.com/onebottlekick/MADE",
    license="Apache-2.0",
    packages=find_packages(include=["made", "made.*"]),
    include_package_data=True,
    install_requires=["openai==1.45.1", "tenacity==9.0.0", "docker==7.1.0", "chromadb==0.5.15"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
