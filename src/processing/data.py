from datetime import datetime
from src.static.constants import *
from src.processing.date_time import convert_to_dateString
import geopandas as gpd
import os
import shutil
import zipfile
import glob  # Added for more efficient file matching

from src.static.constants import path_to_network


def backup_data(geopackage, layer_name, export_path):
    """
    Create a backup of the given layer from the given geopackage.
    Args:
        geopackage (str): path to the geopackage
        layer_name (str): name of the layer to backup
        export_path (str): path to the export directory
    """
    gdf = gpd.read_file(filename=geopackage, layer=layer_name, engine="pyogrio")

    # Use os.path.join for cross-platform path construction
    export_file_path = os.path.join(export_path, f"{layer_name}.shp")

    # Save shapefile
    gdf.to_file(filename=export_file_path, index=False)


def set_backup_path(dept):
    """
    Set the backup path for the given department.
    Create the directory if it does not exist.

    Args:
        dept (str): department name (power, water, wastewater)
    Returns:
        str: path to the backup directory
    """
    current_date = datetime.today()
    date_string = convert_to_dateString(current_date, ymd)

    # Prefer os.path.isdir over os.listdir for performance and simplicity
    if os.path.isdir(path_to_network.get(dept, "")):
        backup_directory = os.path.join(path_to_network[dept], date_string)
    else:
        print("Backup to network is unavailable")
        print("Creating local backup")
        backup_directory = os.path.join(path_to_local[dept], date_string)

    return backup_directory


def convert_shp_to_csv(filename, export_path):
    """
    Convert shapefile to csv with geopandas. Deletes the original shapefile after conversion.
    Args:
        filename (str): path to the shapefile
        export_path (str): path to the export directory
    """
    layer_name = os.path.splitext(os.path.basename(filename))[0]
    gdf = gpd.read_file(filename=filename)
    csv_path = os.path.join(export_path, f"{layer_name}.csv")
    gdf.to_csv(csv_path, index=False)

    # Efficiently delete all associated shapefile files
    pattern = os.path.join(os.path.dirname(filename), f"{layer_name}.*")
    for file in glob.glob(pattern):
        if not file.endswith(".csv"):
            os.remove(file)


def move_files(source, destination):
    """
    Move files from source to destination.
    Args:
        source (str): path to the source directory
        destination (str): path to the destination directory
    """
    if os.path.exists(source):
        if not os.path.exists(destination):
            os.makedirs(destination)

        # Move each file individually
        for file in os.listdir(source):
            shutil.move(os.path.join(source, file), os.path.join(destination, file))

        # Remove empty source directory
        os.rmdir(source)
    else:
        print(f"Path '{source}' does not exist")


def zip_and_remove_files(path_to_file, zip_file):
    """
    Zips files in a given path_to_file and removes them afterward.
    Args:
        path_to_file (str): path to the directory to zip
        zip_file (str): full path to the resulting .zip file
    """
    # Use os.walk with topdown=False to ensure subdirectories are removed after files
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(path_to_file, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                archive_name = os.path.relpath(file_path, path_to_file)
                zipf.write(file_path, archive_name)
                os.remove(file_path)  # Remove each file after adding to ZIP

            # Remove empty directories
            os.rmdir(root)
