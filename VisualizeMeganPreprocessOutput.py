
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                              <<< SOME NOTES >>>                               #
#                                                                               #
#>>> This script visualizes the preprocess output of the LAIv data (LAI3.csv),  #
#    Ecotype data (grid_ecotype.csv), Growth Form data (grid_growth_form.csv),  #
#    and Land Type data (grid_LANDTYPE.csv). The script visualizes the          #
#    specified data column.                                                     #
#                                                                               #
#>>> Give an arbitrary name to the variable on line 45, for example, 'LAIv',    #
#    'Ecotype', etc.                                                            #
#                                                                               #
#>>> Set the map extent on line 49.                                             #
#                                                                               #  
#>>> Set the domain projection data on lines 112-116.                           #
#                                                                               #
#>>> Set the execution aruments on lines 167-171.                               #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

@author : Reza Rezaei
email   : rezarezaei2008@gmail.com
version : 1.0
year    : 2022
"""

import os
import calendar
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
from datetime import datetime
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

# I got this error:   'ERROR 1: PROJ: proj_as_wkt: Cannot find proj.db'
# To solve the error I added the below line:
#os.environ['PROJ_LIB'] = r"C:\\Users\\Reza\\anaconda3\\envs\\env38\\Library\\share\\proj" #<<< Set the path

class PlotLaiOutput():
    def __init__(self, csv_file, lai_column_name, output_plot_dir, year, colorbar_position):
        self.csv = csv_file
        self.lai_col= lai_column_name
        self.variable = "LAIv"
        self.outdir = output_plot_dir
        self.year = year
        self.cbar_pos = colorbar_position
        self.extent = [25.95,30.45,39.29,42.10]
        
    def ReadCSV(self):
        file = pd.read_csv(self.csv, index_col=False)
        lai_arr = file[self.lai_col].values.copy()       
        lat_arr = file["LAT"].values.copy()
        lon_arr = file["LONG"].values.copy()
        lat_size = max(file["Y"])
        lon_size = max(file["X"])
        
        return lai_arr, lat_arr, lon_arr, lat_size, lon_size
    
    def ReshapeArrs(self):
        lai_arr, lat_arr, lon_arr, lat_size, lon_size = self.ReadCSV()    
        lai_2D = np.reshape(lai_arr, (lat_size, lon_size))       
        lat_2D = np.reshape(lat_arr, (lat_size, lon_size))        
        lon_2D = np.reshape(lon_arr, (lat_size, lon_size))
        
        return lai_2D, lat_2D, lon_2D
    
    def GetJulianDate(self, day):
        zeros = ""
        if len(str(day)) < 3:
            zeros_numb = 3 - len(str(day))
            for i in range(zeros_numb):
                zeros+=str(0)
            jdate = eval(f"{self.year}{zeros}{day}")
        else:
            jdate = eval(f"{self.year}{day}")
            
        return jdate
    
    def JulianDate2CalendarDate(self, dayofyear):  
        jdate = self.GetJulianDate(dayofyear)
        
        splitted_jdate = [int(x) for x in str(jdate)]
        spiltted_year = splitted_jdate[:4]
        spiltted_date = splitted_jdate[4:]
        
        strings = [str(integer) for integer in spiltted_year]
        year_string = "".join(strings)
        year_integer = int(year_string)
        
        strings = [str(integer) for integer in spiltted_date]
        date_string = "".join(strings)
        date_integer = int(date_string)
        
        month = 1
        while date_integer - calendar.monthrange(year_integer,month)[1] > 0 and month <= 12:
            date_integer = date_integer - calendar.monthrange(year_integer,month)[1]
            month = month + 1
        
        clndr_date = datetime(year_integer, month, date_integer)
        
        return clndr_date
    
    def PlotLai(self):
        lai_2D, lat_2D, lon_2D = self.ReshapeArrs()
                
        fig = plt.figure(figsize=(24, 18), dpi=300)
        xticks = list(np.arange(-180,180,1))
        yticks = list(np.arange(-90,90,1))
        
        ax = plt.axes(projection=ccrs.LambertConformal(central_latitude = 49, 
                                                       central_longitude = 24,
                                                       standard_parallels = (30, 60),
                                                       false_easting = 6370000,
                                                       false_northing = 6370000))
        
        gl = ax.gridlines(xlocs=xticks, ylocs=yticks, draw_labels=True,
                  linewidth=3, color='indigo', alpha=0.5, linestyle='--')
        
        gl.right_labels = gl.top_labels = gl.left_labels = False
        ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
        ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
                        
        gl.xlabel_style, gl.ylabel_style = {'fontsize': 20}, \
                                           {'fontsize': 20}
        
        plot = plt.pcolormesh(lon_2D, lat_2D, lai_2D,transform=ccrs.PlateCarree(), 
                              cmap=plt.get_cmap("winter"))   # BuGn  winter  viridis
        
        ax.set_extent(self.extent, ccrs.PlateCarree())
        #ax.coastlines(resolution='10m', alpha=0.8)          
        ax.add_feature(cfeature.COASTLINE.with_scale('10m'), alpha=0.8)             
        ax.add_feature(cfeature.BORDERS, linestyle=":", alpha=1)        
        ax.add_feature(cfeature.LAND, facecolor=("peachpuff"))           
        ax.add_feature(cfeature.OCEAN, facecolor=("lightblue"))        
      
        dayofyear = int(self.lai_col[-2:]) * 8 - 7
        clndr_date = self.JulianDate2CalendarDate(dayofyear)
        
        ax.set_title("{0} \u2015 {1}".format(self.variable, clndr_date.date()),
                     fontdict={'fontsize': 36})
    
        if self.cbar_pos.casefold() == "v".casefold():
            cax = fig.add_axes([ax.get_position().x1+0.04,
                                ax.get_position().y0,0.02,
                                ax.get_position().height])
            cbar = fig.colorbar(plot, cax=cax) 
            cbar.ax.set_ylabel("{0} {1}".format(self.variable, "(m\u00B2/10 m\u00B2)"),
                fontsize=32)
        elif self.cbar_pos.casefold() == "h".casefold():
            cax = fig.add_axes([ax.get_position().x0,
                                ax.get_position().y0-0.06,
                                ax.get_position().width, 0.02])
            cbar = fig.colorbar(plot, cax=cax, orientation="horizontal")          
            cbar.ax.set_xlabel("{0} {1}".format(self.variable, "(m\u00B2/10 m\u00B2)"), 
                               fontsize=38)
        
        cbar.ax.tick_params(labelsize=32)
        plt_name = "LAIv_preprocess_output__date_" + str(clndr_date.date()) + ".png"
        plt.savefig(self.outdir + "/" + plt_name, dpi=300, bbox_inches='tight')                         
        plt.show()
        plt.close()
    

#================================== Instance ==================================
ins = PlotLaiOutput(csv_file="C:/Users/mypc/Desktop/LAI3.4km.csv", 
                    lai_column_name="LAI20",
                    output_plot_dir="C:/Users/mpc/Desktop",
                    year = 2012,
                    colorbar_position="h")     # "v" (vertical), "h" (horizontal)                       

ins.PlotLai()