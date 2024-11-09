import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="returnsage",  # The name of your package
    version="0.0.1",  # Version of your package
    author="Ranjith Bhaskaran",
    author_email="ranjithbhaskaran05@gmail.com",  # Your email
    description="A library to calculate real estate returns, taxes, stamp duty, and admin fees",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Format of the long description
    url="https://github.com/Ranji-Bhaskaran/Pypi_Library.git",  # Link to your project page
    packages=setuptools.find_packages(),  # Automatically find your packages
    install_requires=[  # List any dependencies here
        # Example: 'django', 'requests'
    ],
    classifiers=[  # Classifiers for your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Your chosen license
        "Operating System :: OS Independent",  # This package is OS independent
    ],
    python_requires='>=3.6',  # Python version compatibility
)
