# Json file handling
import json
# For interacting with the os
import os
# Visual things
from starfinder_visuals import greenstyle, redstyle, bluestyle, stylereset


def find_config_path():
    """ finds the config path based on current program path """
    try:
        parent = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(parent, "config.json")
    except Exception as e:
        print(redstyle + f"{e}" + stylereset)


class Config:
    """ handles config.json file and its data """

    def __init__(self):
        self.path = find_config_path()
        self.data_paths = {}
        self.region_data = {}
        print(greenstyle + f"\nCreated new config object with path: {self.path}\n" + stylereset)


    def ensure_config_exists(self):
        # If it can't find where it should be
        if not os.path.exists(self.path):
            # Initialize blank slate data
            print(redstyle + f"Cannot find config.json, creating at: {self.path}\n" + stylereset)
            config_data = {"config_path": self.path, "region_data_path(s)": {}}
            with open(self.path, "w") as file:
                json.dump(config_data, file, indent=4)


    def update_config(self):
        config_data = {"config_path": self.path, "region_data_path(s)": self.data_paths}
        with open(self.path, "w") as file:
            json.dump(config_data, file, indent=4)
        print(greenstyle + "\nUpdated config.json file" + stylereset)


    def load_config(self):
        with open(self.path, "r") as file:
            loaded_config = json.load(file)
        self.path = loaded_config["config_path"]
        path_lookup = loaded_config["region_data_path(s)"]

        # If theres nothing in the path_lookup
        if len(path_lookup) == 0:
            print(redstyle + "No regions loaded" + stylereset)
            return

        print("Region data:\n====================")
        region_data = {}
        # reads the contents of the json files in the path_lookup dictionary
        for region, path in path_lookup.items():
            self.data_paths[region] = path
            with open(path, "r") as file:
                region_data[region] = json.load(file)
            print(bluestyle + f"Loaded {region} data" + stylereset)

        self.region_data = region_data


    def update_region_data(self, region_label, data_path):
        """ Updates the Config object variable self.region_data dictionary with the paths currently in config.json """
        with open(data_path, "r") as file:
            self.region_data[region_label] = json.load(file)
        self.data_paths[region_label] = data_path