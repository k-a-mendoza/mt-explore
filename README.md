[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


![Mt-Explore](https://github.com/El-minadero/mt-explore/blob/master/images/social_card_modified.png)

MT-Explore is a GUI meant to assist in the compilation of magnetotelluric datasets for inversion purposes.



## Acknowledgements

MT-Explore would not be possible without the hard and extensive work by the Cartopy and MtPy team. If you deal with location plotting or Magnetotelluric data, I suggest you check out their packages:

[mtpy](https://github.com/MTgeophysics/mtpy)

[cartopy](https://scitools.org.uk/cartopy/docs/latest/)

MT-Explore also leverages numpy, pandas, matplotlib, and tk. 

## Installation
Because of the way things are, for version 0.0.4, you'll have to do a 2 part install, one with anaconda and one with pip.
First, install cartopy using anaconda:
```bash
conda install cartopy
```

Then use the package manager [pip](https://pip.pypa.io/en/stable/) to install MT-Explore.

```bash
pip install mtexplore
```

## Usage

First, create an Mt_Ex_Main Object and link it with your local .edi database directory.

```python
from mtexplore import Mt_Ex_Main

main_app = Mt_Ex_Main()
main_app.connect_database('MT Data/')

```
![Mt-Explore](https://github.com/El-minadero/mt-explore/blob/master/images/ex.png)

You should see a window pop up with a map view and associated phase/apparent resistivity plot. It is possible to interact with the data using the mouse or specific keys. For a full list of commands press 'h'

Mt Explore is meant to help identify stations with strategic location and data quality importance to your study area. Ultimately, stations are either included, or excluded from the dataset. To include stations, press 'i'. Similarly stations are excluded by pressing 'o'. 

The include/exclude metadata is exported as a pandas dataframe via the load-save commands in .csv format for later data manipulation. This exported dataframe does not contain the transfer function information from the .edi files, but only the location on disk for each station. 

## Known Issues
There are a few cosmetic issues that I probably wont fix as they dont impact the usability of MT-Explore. However, if you know how to fix them feel free to submit a pull request.

By overriding some of the key bindings of Matplotlib, a few unexpected plot and map behaviors were introduced. If things mess up just kill the plot window and instantiate the Main object again. 

tick locators are temporarily broken. this shouldn't impact usability however.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

## Attribution

If you use this package, please cite [mtpy](https://github.com/MTgeophysics/mtpy) and [cartopy](https://scitools.org.uk/cartopy/docs/latest/). Much of the functionality of this package comes from their work. 

At this time I dont ask that you use an official citation of MT-Explore, but if it is helpful in class projects, publications, training, surveys, or any other endeavor, I would appreciate an acknowledgement. Something like [Mendoza, K; Mt-Explore 2019](https://github.com/El-minadero/mt-explore.git) could be appropriate.


