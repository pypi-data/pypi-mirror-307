from setuptools import setup, find_packages

setup(
    name="sdTranslate",                   # Name of your package
    version="0.2",                        # Version
    packages=find_packages(),             # Automatically find sub-packages
    install_requires=[                    # External packages your code depends on
        "requests",
        "unidecode"
    ],
    author="Siraj_Dal",                   # Your name
    author_email="write2sirajv@gmail.com", # Your email
    description="A description of sdTranslate", # Short description
    long_description=open("README.md").read(),  # Long description from README file
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sdTranslate",  # URL of your project, if any
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",              # Minimum Python version
)
