from setuptools import setup, find_packages

setup(
    name="bidd_Manager325",  # Replace with your package name
    version="1.1.1",
    packages=find_packages(),
    description="A brief description of your library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Rahul",
    author_email="rahulshirsat9156@gmail.com",
    url="https://github.com/yourusername/your_library",
    license="MIT",  # Choose your license type
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)