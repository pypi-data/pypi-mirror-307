from setuptools import setup, find_namespace_packages

setup(
    name="magic-moonshine",
    version="0.1.9",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=[
        "requests>=2.25.0",
        "boto3>=1.26.0",
        "opencv-python>=4.5.0",
        "typing-extensions>=4.0.0",
    ],
    author="Harsha Gundala",
    author_email="harsha@usemoonshine.com",
    description="A Python client for the Moonshine API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://usemoonshine.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)