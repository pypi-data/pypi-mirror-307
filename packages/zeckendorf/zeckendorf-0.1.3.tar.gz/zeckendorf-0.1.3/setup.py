from setuptools import setup, find_packages

setup(
    name="zeckendorf",
    version="0.1.3",
    author="Zeck",
    author_email="synowiecphilip@gmail.com",
    description="Tools aus purer Gierigkeit.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=None,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
