# For the visuals
from starfinder_visuals import (
    color_input, bluestyle, bold, greenstyle, redstyle, violetstyle,
    stylereset, yellowstyle, clear_console
)


# Default planet characteristics
tectonics = ["Dunes", "Ridges", "Mountains", "Continental", "Chaos", "Jovian_t"]
atmosphere = ["Terran", "Martian", "Venusian", "Steam", "Jovian_a", "Neptunian",
              "Titanian", "Alkali", "Silicate", "None_a"]
oceans = ["Water", "Acid", "Air", "Blood", "Methane", "Ammonia", "Lava", "None_o"]
life_status = ["No_life", "Life"]
planet_characteristics = tectonics + atmosphere + oceans + life_status


def planet_options():
    print("[Available planet search options]\n"
        "============================================================\n"
        f"{'tectonics':<12} | {'atmosphere':<12} | {'oceans':<12} | {'life status':<12}\n"
        "============================================================")

    # Gets a characteristic to put in each row (or nothing if no more to add)
    for i in range(max(len(tectonics), len(atmosphere), len(oceans), len(life_status))):
        tectonics_opt = tectonics[i] if i < len(tectonics) else ""
        atmosphere_opt = atmosphere[i] if i < len(atmosphere) else ""
        oceans_opt = oceans[i] if i < len(oceans) else ""
        life_status_opt = life_status[i] if i < len(life_status) else ""

        print(bluestyle 
            + bold + f"{tectonics_opt:<12}" + stylereset
            + bluestyle + " | "
            + bold + f"{atmosphere_opt:<12}" + stylereset
            + bluestyle + " | "
            + bold + f"{oceans_opt:<12}" + stylereset
            + bluestyle + " | "
            + bold + f"{life_status_opt:<12}"  + stylereset)
    print("============================================================")


def view_parameters(parameters):
    if parameters.first is None:
        print(redstyle + "No parameters selected" + stylereset)
        return

    curr = parameters.first
    before_focus = True
    # Goes node by node starting at the first
    # Colors them green if they are not undone
    while curr:
        text = f"[{curr.data[0]}: {curr.data[1]}]" + ("," if curr.next else "")

        if curr is parameters.focus or before_focus and parameters.focus is not None:
            print(bold, end = "") if curr is parameters.focus else print(end = "")
            print(greenstyle + text + stylereset)
            if curr is parameters.focus:
                before_focus = False
        else:
            print(redstyle + text + stylereset)
        curr = curr.next


def planet_prompt():
    """ prompt for a characteristic choice and returns it """
    choice = color_input(
                bluestyle
                + "Type any of the options above, for example 'Terran' or 'None_oc' to add the parameter"
                + "\nType 'undo' to remove the last parameter"
                + "\nType 'redo' to redo the last undone parameter"
                + "\nType 'done' to search"
                + "\nType 'exit' to return to the main menu"
                + stylereset
                + "\nType here: "
                , color = yellowstyle
                ).strip().lower().capitalize()
    
    return choice


def planet_step(config, planet_parameters):    
    end = False
    while not end:
        planet_options()
        print("\n[Current planet parameters]\n==========================")
        view_parameters(planet_parameters)
        print("==========================")
        print("Num found: " + violetstyle + str(len(search(config, planet_parameters))) + stylereset + "\n")
        choice = planet_prompt()
        end = choice_action(choice, planet_parameters)


def planet_add_parameter(parameters, choice):
    """ adds the choice to a linked list called parameters here"""
    if choice in tectonics:
        parameters.append(("tectonics", choice.split("_", 1)[0]))
    elif choice in atmosphere:
        parameters.append(("atmosphere", choice.split("_", 1)[0]))
    elif choice in oceans:
        parameters.append(("oceans", choice.split("_", 1)[0]))
    elif choice in life_status:
        parameters.append(("life_status", choice == "Life"))
        

def choice_action(choice, parameters):
    """ takes an action based on the choice made """
    clear_console()
    if choice == "Done":
        parameters.solidify()
        return True
    if choice == "Exit":
        print(greenstyle + "Exiting to main menu\n" + stylereset)
        return True
    if choice == "Undo":
        parameters.prev()
        return False
    if choice == "Redo":
        parameters.next()
        return False
    if choice in planet_characteristics:
        planet_add_parameter(parameters, choice)
        return False

    print(redstyle + "Invalid choice\n" + stylereset)
    return False


class Node:
    """ holds planet characteristc data """
    def __init__(self, data):       
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:
    """ Used for the undo/redo functionality """
    def __init__(self):
        self.first = None
        self.focus = None


    def append(self, data):
        new = Node(data)
        # If first node in the linked list
        if self.focus is None:
            self.first = new
            self.focus = new
            return

        # Cut off everything after the focus to delete what was undone
        self.solidify()
        # Added the new node
        self.focus.next = new
        new.prev = self.focus
        self.focus = new


    def next(self):
        # If no current focus (can happen if everything was undone)
        if self.focus is None:
            self.focus = self.first
            # If the linked list was empty
            if self.first is None:
                print(redstyle + "Nothing to redo\n" + stylereset)
            return

        # If focus is at the end of the linked list (no more to redo)
        if self.focus.next is None:
            print(redstyle + "Nothing to redo\n" + stylereset)
            return
        self.focus = self.focus.next


    def prev(self):
        # If the linked list is empty or everything was undone already
        if self.focus is None:
            print(redstyle + "Nothing to undo\n" + stylereset)
            return

        self.focus = self.focus.prev


    def solidify(self):
        if self.focus is None:
            self.first = None
            return
        self.focus.next = None
        # Cuts off everything after the focus


def search(config, planet_parameters):
    # First sets up the dictionary which will be filled with the characteristics being searched for
    characteristics = {"tectonics":[], "atmosphere":[], "oceans":[], "life_status":[]}
    curr = planet_parameters.first
    # Appends everything in the linked list
    while (curr is not None) and (planet_parameters.focus is not None) and (curr is not planet_parameters.focus.next):
        characteristics[curr.data[0]].append(curr.data[1])
        curr = curr.next

    # Returns true if this planet meets all the requirements
    def ok(planet):
        return (
            (len(characteristics["tectonics"]) == 0 or planet["tectonics"] in characteristics["tectonics"])
            and (len(characteristics["atmosphere"]) == 0 or planet["atmosphere"] in characteristics["atmosphere"])
            and (len(characteristics["oceans"]) == 0 or planet["oceans"] in characteristics["oceans"])
            and (len(characteristics["life_status"]) == 0 or planet["life"] in characteristics["life_status"])
        )

    id_list = []
    # Iterates through the data to check all the planets
    for region, systems in config.region_data.items():
        for system_key, system in systems.items():
            for planet in system.get("planets", []):
                if ok(planet):
                    id_list.append(f"{system.get('id')}-{planet.get('id')}")
    return id_list


def find(config):
    # Initializes the linked list for storying choice history
    planet_parameters = LinkedList()
    # Prompts for characterics until user enters 'done' then moves on from there
    planet_step(config, planet_parameters)
    print("[Search Results]\n==========================")
    id_list = search(config, planet_parameters)
    if len(id_list) == 0:
        print(redstyle + "None found" + stylereset)
    for id in id_list:
        print(violetstyle + f"{id}" + stylereset)