# Config class handles the Json data
from starfinder_config import Config
# Handling the main menu prompts
from starfinder_functions import prompt_dict, list_prompts
# For the program visuals
from starfinder_visuals import color_input, clear_console, yellowstyle, redstyle, stylereset


def setup_config():
    """ Creates a config object, loads in/initialize it if needed """
    config = Config()
    config.ensure_config_exists()
    config.load_config()
    return config


def command_prompt_ui(config):
    """ Main menu command prompting loop"""
    end = False
    while not end:

        # Repeat until the command is valid
        while True:
            list_prompts()
            choice = color_input("Enter the number of the command to execute: ",
                                 color=yellowstyle).strip().lower()
            if choice in prompt_dict:
                break
            clear_console()
            print(redstyle + "Invalid choice" + stylereset)

        clear_console()
        # Does the command and returns whether program should end after
        # Looking back on this I believe I should have created a command class and have the config variable be a variable within it
        # That way I wouldn't have had to pass the config variable to every command function despite some not using it
        end = prompt_dict[choice](config)


def main():
    """ Main """
    command_prompt_ui(setup_config())


if __name__ == "__main__":
    main()