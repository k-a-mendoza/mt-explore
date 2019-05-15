import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    r = f.read().splitlines()
    requirements=[]
    for x in r:
        if '#' not in x:
            requirements.append(x)


setuptools.setup(
    name="mtexplore",
    version="0.0.0",
    author="Kevin Mendoza",
    author_email='kevinmendoza@icloud.com',
    description="MT Explore is a cartopy and mtpy based utility for viewing and cleaning Magnetotelluric data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/El-minadero/mt-explore",
    packages=setuptools.find_packages(),
    install_requires = requirements,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
print(setuptools.find_packages())