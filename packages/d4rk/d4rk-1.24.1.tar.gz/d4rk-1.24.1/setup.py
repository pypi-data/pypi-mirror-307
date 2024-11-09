from setuptools import setup, find_packages

setup(
    name="d4rk",
    version="1.24.1",
    packages=find_packages(),
    install_requires=[],
    author="Hussain Luai",
    author_email="hxolotl15@gmail.com",
    description="A Python framework with dark mode and custom icons.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
