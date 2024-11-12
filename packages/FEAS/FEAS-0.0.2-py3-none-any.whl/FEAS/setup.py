from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

# Setup configuration
setup(
    name='FEAS',
    version='0.0.3',
    author='Tahir Iqbal',
    author_email='tahiriqbal70@gmail.com',
    description='Fire Evacuation Automation System',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/tahiriqbal70/FEAS',  # Add your actual GitHub URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10"
    ],
    packages=find_packages(),
    install_requires=['']  # Add dependencies here if any, e.g., ['requests', 'numpy']
)
