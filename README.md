# MT Explore

MT-Explore is a GUI meant to assist in the compilation of datasets for MT inversion.



## Acknowledgements

MT-Explore would not be possible without the hard and extensive work by the Cartopy and MtPy team. If you deal with location plotting or Magnetotelluric data, I suggest you check out their packages:

[mtpy](https://github.com/MTgeophysics/mtpy)
[cartopy](https://scitools.org.uk/cartopy/docs/latest/)

MT-Explore also leverages numpy, pandas, matplotlib, and tk. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install MT-Explore.

```bash
pip install mtexplore
```

## Usage

First, create an Mt_Ex_Main Object

```python
from mtexplore import Mt_Ex_Main

main_app = Mt_Ex_Main()
main_app.connect_database('MT Data/')

```
You should see a window pop up with a map view and associated phase/apparent resistivity plot. It is possible to interact with the data using the mouse or specific keys. For a full list of commands press 'h'

Mt Explore assumes the point of this data exploration is to identify stations with strategic location and data quality important to your study area. Ultimately, stations are either included, or excluded from the dataset. To include stations, press 'i'. Similarly stations are excluded by pressing 'o'. 

The incldue/exclude metadata is exported as a pandas dataframe via the load-save commands in .csv format for later data manipulation. This exported dataframe does not contain the transfer function information from the .edi files, but only the location on disk for each station. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)

## Citation

At this time I dont ask that you use an official citation of MT-Explore, but if it is helpful in class projects, publications, training, surveys, or any other endeavor, I would appreciate an acknowledgement. Something like [Mendoza, K; Mt-Explore 2019](https://github.com/El-minadero/mt-explore.git) could be appropriate.
