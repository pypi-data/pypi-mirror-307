import matplotlib.pyplot as plt
import numpy as np
import datetime
from hjnwtx.colormap import cmp_hjnwtx  # Assuming this is your custom colormap library
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import os
from shancx import crDir

def Glob(array_dt,cd="CHN",ty="CR"):
    if cd == "g":
        env = [-179.617020, 179.632979,-85.098871,85.051128] 
    elif cd == "US":
        env = [-132.0, -47.0, 0, 57.0]
    elif cd == "CHN":
        env = [73,134.99,12.21,54.2]   
    else:
         env = cd
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    outpath = f"./radar_nmc/{str(cd)}_{now_str}.png"
    crDir(outpath)
    # Create figure and set the coordinate system
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    # Set the extent for the United States
    ax.set_extent(env, ccrs.PlateCarree())  # Adjust as needed
    # Add the US map boundaries and features
    add_glob_map(ax)    
    # Add data layers
    if len(array_dt.shape) == 3:
        for i, img_ch_nel in enumerate(array_dt):
            ax.imshow(img_ch_nel, vmin=50, vmax=500, cmap=cmp_hjnwtx["radar_nmc"], transform=ccrs.PlateCarree(), extent=env)
            plt.colorbar(ax.images[0], ax=ax, orientation='vertical')
            plt.savefig(f"{outpath}_layer_{i}.png")
            plt.clf()  # Clear the figure to draw the next channel image
    elif len(array_dt.shape) == 2 and ty =="pre":
        ax.imshow(array_dt, vmin=0, vmax=10, cmap=cmp_hjnwtx["pre_tqw"], transform=ccrs.PlateCarree(), extent=env)   
        plt.colorbar(ax.images[0], ax=ax, orientation='vertical')
        plt.savefig(outpath)
    else :
        ax.imshow(array_dt, vmin=0, vmax=72, cmap=cmp_hjnwtx["radar_nmc"], transform=ccrs.PlateCarree(), extent=env)
        plt.colorbar(ax.images[0], ax=ax, orientation='vertical')
        plt.savefig(outpath)
    plt.close(fig)

def add_glob_map(ax): 
    ax.add_feature(cfeature.COASTLINE, edgecolor='gray')
    ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')
    ax.add_feature(cfeature.LAKES, alpha=0.8)    
    # Adding state boundaries
    if os.path.exists('/home/scx/ne_10m_admin_1_states_provinces.shp'):
        states = '/home/scx/ne_10m_admin_1_states_provinces.shp'
    else:
        states = shpreader.natural_earth(resolution='10m', category='cultural', name='admin_1_states_provinces')  # Automatically download 
    states_features = shpreader.Reader(states).geometries()    
    ax.add_geometries(states_features, ccrs.PlateCarree(), facecolor='none', edgecolor='gray', linestyle=':', linewidth=0.5, alpha=0.8)
 
def GlobLonLat(array_dt,Lon,Lat,cd="CHN",ty="CR"):   ###  x_coords2 维度 
    if cd == "g":
        env = [-179.617020, 179.632979,-85.098871,85.051128] 
    elif cd == "US":
        env = [-132.0, -47.0, 0, 57.0]
    elif cd == "CHN":
        env = [73,134.99,12.21,54.2]   #[73, 134.99, 12.21, 54.2] 
    else:
         env = cd    
    now_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    outpath = f"./radar_nmc/{str(cd)}_{now_str}.png"
    crDir(outpath)

    # Create figure and set the coordinate system
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Set the extent for the United States
    ax.set_extent(env, ccrs.PlateCarree())  # Adjust as needed

    # Add the US map boundaries and features
    add_glob_map(ax)
    
    # Add data layers
    if len(array_dt.shape) == 3:
        for i, img_ch_nel in enumerate(array_dt):
            ax.imshow(img_ch_nel, vmin=50, vmax=500, cmap=cmp_hjnwtx["radar_nmc"], transform=ccrs.PlateCarree(), extent=env)
            plt.colorbar(ax.images[0], ax=ax, orientation='vertical')
            plt.savefig(f"{outpath}_layer_{i}.png")
            plt.close()  
    elif len(array_dt.shape) == 2 and ty =="pre":
        ax.imshow(array_dt, vmin=0, vmax=10, cmap=cmp_hjnwtx["pre_tqw"], transform=ccrs.PlateCarree(), extent=env)   
        plt.colorbar(ax.images[0], ax=ax, orientation='vertical')
        ax.scatter(list(Lon), list(Lat), s=0.5, c='red', marker='o', transform=ccrs.PlateCarree())
        plt.savefig(outpath)
    else :
        ax.imshow(array_dt, vmin=0, vmax=72, cmap=cmp_hjnwtx["radar_nmc"], transform=ccrs.PlateCarree(), extent=env)
        ax.scatter(list(Lon), list(Lat), s=0.5, c='red', marker='o', transform=ccrs.PlateCarree())
        plt.colorbar(ax.images[0], ax=ax, orientation='vertical')
        plt.savefig(outpath)
    plt.close(fig)

def add_us_map(ax):
    ax.add_feature(cfeature.COASTLINE, edgecolor='gray')
    ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='gray')
    ax.add_feature(cfeature.LAKES, alpha=0.8)    
    # Adding state boundaries
    if os.path.exists('/home/scx/ne_10m_admin_1_states_provinces.shp'):
        states = '/home/scx/ne_10m_admin_1_states_provinces.shp'
    else:
        states = shpreader.natural_earth(resolution='10m', category='cultural', name='admin_1_states_provinces')  # Automatically download 
    states_features = shpreader.Reader(states).geometries()    
    ax.add_geometries(states_features, ccrs.PlateCarree(), facecolor='none', edgecolor='gray', linestyle=':', linewidth=0.5, alpha=0.8)

# Example usage
# Assuming array_dt is your data array, pass it to drawUS
# array_dt = np.random.rand(3, 100, 100)  # Example random data; replace with your actual data
# drawUS(array_dt)
