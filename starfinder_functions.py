# For the visuals
from starfinder_visuals import (
    color_input, bluestyle, bold, greenstyle, redstyle,
    stylereset, yellowstyle
)
# Decided to put this in a different program file due to its size
from starfinder_find import find


def load_star_data(config):
    """ Prompt for a new data location and its label """
    label = color_input("Enter the label for this star data set: ", color=yellowstyle).strip()
    path = color_input("Enter the path to the star data JSON file: ", color=yellowstyle).strip().strip('"\'')
    config.data_paths[label] = path
    config.update_region_data(label, path)
    config.update_config()


def show_data(config):
    """ prints out a summary for each region (label and path) """
    print("Currently loaded star data sets:\n====================")
    if not config.region_data:
        print(redstyle + "No regions loaded" + stylereset)
        return

    for region, systems in config.region_data.items():
        num_systems = len(systems)
        num_planets = sum(systems[system_id]["planet_count"] for system_id in systems)
        num_moons = sum(
            planet["moons"]
            for system_id in systems
            for planet in systems[system_id]["planets"]
        )

        print(
            bluestyle
            + f"[{region}]\n{'num systems':>15}: {num_systems}\n{'num planets':>15}: {num_planets}\n{'num moons':>15}: {num_moons}"
            + stylereset
        )


def show_config(config):
    print("Config variables:\n====================")
    print(bluestyle + f"config_path: {config.path}" + stylereset)
    print(bluestyle + "config.data_paths:" + stylereset)
    for region, path in config.data_paths.items():
        print(bluestyle + f"\t{region}: {path}" + stylereset)


def end_program(config):
    print(greenstyle + "Exiting program\n" + stylereset)
    return True


prompt_dict = {
    "1": find,
    "2": load_star_data,
    "3": show_data,
    "4": show_config,
    "exit": end_program,
}


def list_prompts():
    print("\nAvailable commands:\n====================")
    for key, fn in prompt_dict.items():
        print(bluestyle + f"[{key:4}] " + bold + f"{fn.__name__}" + stylereset)


def verify_prompt_choice(choice):
    return choice in prompt_dict