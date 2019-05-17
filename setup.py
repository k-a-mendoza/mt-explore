import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mtexplore",
    version="0.0.6",
    author="Kevin Mendoza",
    author_email='kevinmendoza@icloud.com',
    description="MT Explore is a cartopy and mtpy based utility for viewing and cleaning Magnetotelluric data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/El-minadero/mt-explore",
    packages=setuptools.find_packages(),
    install_requires = ['cartopy>=0.17.0',
    'matplotlib>=3.0.3',
    'numpy>=0.16.2',
    'pandas>=0.24.',
    'mtpy>=1.0.1'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
print(setuptools.find_packages())