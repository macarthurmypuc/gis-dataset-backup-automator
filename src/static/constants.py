import os


USER = os.getlogin()

department = ["power", "water", "wastewater"]

geopackages = {
    "power": {
        "path": f"C:\\Users\\{USER}\\Desktop\\ACTIVE_PROJECTS\\QField\\cloud\\POWER_DISTIRIBUTION_ASSET_NETWORK",
        "file": "power_distribution_infrastructure.gpkg"
    },
    "water": {
        "path": f"C:\\Users\\{USER}\\Desktop\\ACTIVE_PROJECTS\\WATER_ASSET_INVENTORY_DISTRIBUTION_NETWORK\\RESOURCES",
        "file": "water_resources.gpkg"
    },
    "wastewater": {
        "path": f"C:\\Users\\{USER}\\Desktop\\ACTIVE_PROJECTS\\SEWER_ASSET_IVENTORY_DISTRIBUTION_NETWORK\\RESOURCES",
        "file": "sewer_infrastructure.gpkg"
    }
}

path_to_network = {
    "power": "\\\\PUC_NAS\\DataCollection_Project\\ACTIVE PROJECTS\\DATA HUB\\POWER",
    "water": "\\\\PUC_NAS\\DataCollection_Project\\Active Projects\\Data Hub\\water",
    "wastewater": "\\\\PUC_NAS\\DataCollection_Project\\Active Projects\\Data Hub\\wastewater"
}

path_to_local = {
    "power": "C:\\backup_gis_data\\power",
    "water": "c:\\backup_gis_data\\water",
    "wastewater": "c:\\backup_gis_data\\wastewater"
}

power_layer_names = [
    "primary_pole", "primary_line", "transformer", "customer_meter",
    "xfmr_customer_link", "secondary_pole", "secondary_line", "switch",
    "switching_area"
]


ymd = "%Y-%m-%d"
mdy = "%m-%d-%Y"
mmy = "%B %Y"
mmdy = "%B %d, %Y"
year = "%Y"