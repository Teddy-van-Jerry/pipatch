from setuptools import setup, find_packages

setup(
    name="pipatch",
    version="0.1.1",
    description="Minimal patching tool for Python packages.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Teddy van Jerry (Wuqiong Zhao)",
    author_email="me@teddy-van-jerry.org",
    license="MIT",
    packages=find_packages(),
    install_requires=["requests"],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development",
    ],
)
