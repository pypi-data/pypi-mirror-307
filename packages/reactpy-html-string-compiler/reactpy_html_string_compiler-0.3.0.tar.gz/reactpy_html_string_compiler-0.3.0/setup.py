from setuptools import setup, find_packages

setup(
    name="reactpy_html_string_compiler",
    version="0.3.0",
    description="compiles reactpy components into html string",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  
    include_package_data=True,
    install_requires=[
        "reactpy>=1.0.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
