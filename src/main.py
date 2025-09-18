from datetime import datetime
from src.static.constants import *
from src.processing.date_time import convert_to_dateObject, convert_to_dateString
from src.processing.data import set_backup_path, backup_data, move_files, convert_shp_to_csv, zip_and_remove_files
import os
import glob


def main():
    ###========== BACKUP DATA FROM GEOPACKAGE ==========###
    print(f"Checking if network backup path is available")
    working_department = department[0]

    backup_export_path = set_backup_path(working_department)
    os.makedirs(backup_export_path, exist_ok=True)

    dept_geopackage = geopackages[working_department]
    working_geopackage = os.path.join(dept_geopackage["path"], dept_geopackage["file"])

    print(f"Backing up layers from {dept_geopackage['file']}")
    for layername in power_layer_names:
        backup_data(working_geopackage, layername, backup_export_path)
    print(f"Layers backed up")


    ###========== MOVE LOCAL BACKUP TO NETWORK ==========###
    network_path = path_to_network[working_department]
    local_path = path_to_local[working_department]

    if os.path.isdir(network_path):
        print(f"Moving local backup to network")
        for dir in os.listdir(local_path):
            if dir != "ARCHIVE":
                src_path = os.path.join(local_path, dir)
                dst_path = os.path.join(network_path, dir)
                move_files(src_path, dst_path)
        print(f"Moving local backup complete")


    ###========== CONVERT OLD SHAPEFILES TO CSV & ARCHIVE ==========###
    current_date = datetime.today()
    print(f"Converting old shapefile backup to CSV and archiving backups older than 30 days")

    for dir in os.listdir(network_path):
        if dir != "ARCHIVE" and not dir.endswith(".zip"):
            dir_path = os.path.join(network_path, dir)
            dir_date = convert_to_dateObject(dir, ymd)
            days_old = (current_date - dir_date).days

            if days_old >= 5:
                shp_files = glob.glob(os.path.join(dir_path, "*.shp"))
                for shp_file in shp_files:
                    convert_shp_to_csv(shp_file, dir_path)

            if days_old >= 30:
                archive_path = os.path.join(
                    "//PUC_NAS/DataCollection_Project/ARCHIVED/BACKUP_GIS_DATA",
                    working_department.upper(),
                    dir.split("-")[0]
                )
                os.makedirs(archive_path, exist_ok=True)
                print(f"Archiving '{dir}' to Zip file")
                zip_to_path = os.path.join(archive_path, dir + ".zip")
                zip_and_remove_files(dir_path, zip_to_path)

    print(f"Conversion and archiving complete")


if __name__ == "__main__":
    main()
