The LAIv input files for the MEGAN (Model of Emissions of Gases and Aerosols from Nature) model are only available for the USA. Users outside the US must generate these data using leaf area index (LAI) and fractional vegetation cover (FVC) datasets. Before assimilation by the model, the generated LAIv data are preprocessed by a script called 'prepmegan4cmaq_lai.f90', which generates a file named ‘LAI3.csv’ at the end of the operation. Given the importance of accurate data in calculating biogenic VOCs, verifying the data's correctness after preprocessing is crucial.
This script visualises the preprocessed LAIv data from ‘LAI3.csv’. It allows users to select one of the 46 LAIv data columns (LAI01-LAI46) in the CSV file, each representing the LAIv values for a single day across the domain grids, for visualization. The script can also be applied to other preprocessing outputs, including ‘CT3.csv’, ‘grid_ecotype.csv’, ‘grid_growth_form.csv’, and ‘grid_LANDTYPE.csv’.
