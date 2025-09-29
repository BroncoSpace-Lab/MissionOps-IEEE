import matplotlib
matplotlib.use("Agg")   # safe for headless GMAT

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from scipy.interpolate import griddata

# Load the geomagnetic field data
# !!!!!!!!!!!! CHANGE THIS TO WHEREVER YOURS IS
df = pd.read_csv(
    "C:\geomagnetic_field_data.csv"
)
df.columns = df.columns.str.strip()

print("hello")   # quick test when GMAT loads this module


# ~~~~~~BEGIN Jacob's efficiency changes. Theory - moving one-time events outside the function will speed up function calls.
print("!!!BEGIN EFFICIENCY LOADING!!!")
lon = df["longitude"].values
lat = df["latitude"].values
field = df["total_field_intensity_nT"].values

grid_lon = np.linspace(np.nanmin(lon), np.nanmax(lon), 360)
grid_lat = np.linspace(np.nanmin(lat), np.nanmax(lat), 180)
X, Y = np.meshgrid(grid_lon, grid_lat)

Z = griddata((lon, lat), field, (X, Y), method="linear")

if np.isnan(Z).any():
        Z_near = griddata((lon, lat), field, (X, Y), method="nearest")
        Z = np.where(np.isnan(Z), Z_near, Z)

fig, ax = plt.subplots()
print("!!!END EFFICIENCY LOADING!!!")
# ~~~~~~END Jacob's efficiency changes


def check_satellite_in_contour_gmat(sat_positions, field_strength_threshold):
    """
    GMAT-friendly entry point.

    sat_positions: [Latitude, Longitude] from GMAT (2-element array)
    field_strength_threshold: threshold in nT

    Returns: 1 if inside the contour, else 0
    """
    # Unpack GMAT input (Latitude, Longitude)
    try:
        lat_sat = float(sat_positions[0])
        lon_sat = float(sat_positions[1])
    except Exception:
        # Guard against unexpected shapes (e.g., [[lat, lon]])
        lat_sat = float(sat_positions[0])
        lon_sat = float(sat_positions[1])

    # Data arrays
#    lon = df["longitude"].values
#    lat = df["latitude"].values
#    field = df["total_field_intensity_nT"].values

    # Grid for contouring
#    grid_lon = np.linspace(np.nanmin(lon), np.nanmax(lon), 360)
#    grid_lat = np.linspace(np.nanmin(lat), np.nanmax(lat), 180)
#    X, Y = np.meshgrid(grid_lon, grid_lat)

#    Z = griddata((lon, lat), field, (X, Y), method="linear")

    # Fill gaps with nearest-neighbor if needed
#    if np.isnan(Z).any():
#        Z_near = griddata((lon, lat), field, (X, Y), method="nearest")
#        Z = np.where(np.isnan(Z), Z_near, Z)

    # Build contour and extract segments robustly
#    fig, ax = plt.subplots()
    cs = ax.contour(X, Y, Z, levels=[field_strength_threshold])

    inside = 0  # default = outside
    try:
        if cs.allsegs and len(cs.allsegs[0]) > 0:
            for seg in cs.allsegs[0]:
                path = Path(seg)
                # Path expects (x, y) = (lon, lat)
                if path.contains_point((lon_sat, lat_sat)):
                    inside = 1
                    break
    finally:
        plt.close(fig)

    print(f"Received Latitude: {lat}, Longitude: {lon}")
    print(f"Field Strength Threshold: {field_strength_threshold}")

    return inside

# Quick unit test
def test_check():
    return check_satellite_in_contour_gmat([10.0, -70.0], 40000)
