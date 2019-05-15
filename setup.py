import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mtexplore-el-minadero",
    version="0.0.0",
    author="Kevin Mendoza",
    author_email='kevinmendoza@icloud.com',
    description="MT Explore is a cartopy and mtpy based utility for viewing and cleaning Magnetotelluric data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/El-minadero/mt-explore",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU GPLv3",
        "Operating System :: OS Independent",
    ],
)
print(setuptools.find_packages())