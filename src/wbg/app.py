"""
RPG Character Backstory Generator
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.style.pack import BOLD, CENTER
import random
import yaml
import os

class WeckterBackstoryGenerator(toga.App):

    def startup(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        yaml_path = os.path.join(current_dir, 'supportfiles', 'AllyEnemyTables.yaml')
        font_path = os.path.join(current_dir, 'supportfiles', 'fonts', 'noto', 'NotoSansMono-Regular.ttf')
        font_path_bold = os.path.join(current_dir, 'supportfiles', 'fonts', 'noto', 'NotoSansMono-Bold.ttf')

        self.current_state = {
            'allyenemy': '',
            'category': '',
            'description': ''
        }


        toga.Font.register("NotoSansMono", font_path)
        toga.Font.register("NotoSansMono", font_path_bold, weight=BOLD)
        custom_font = toga.Font("NotoSansMono", 14, weight=BOLD)

        big_header_style = Pack(
            padding=(0, 15),
            font_family="NotoSansMono",
            font_size=20,
            font_weight=BOLD,
            alignment=CENTER
        )

        header_style = Pack(
            padding=(5, 0),
            font_family="NotoSansMono",
            font_size=15,
            font_weight=BOLD,
            alignment=CENTER
        )

        roll_label_style = Pack(
            padding=(0, 10),
            font_family="NotoSansMono",
            font_size=15,
            #font_weight=BOLD,
            height=20,
            padding_top=5,
            padding_bottom=0
        )

        description_labels = {}
        selected_sentences = "No features selected."
        selected_sentences_list = []
        self.temperment_selected = ""


        def wrap_text(text, max_width):
            words = text.split(' ')
            lines = []
            current_line = []

            for word in words:
                if len(' '.join(current_line) + ' ' + word) > max_width:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)

            lines.append(' '.join(current_line))
            return '\n'.join(lines)






        def on_tab_select(self, widget):
            selected_tab = widget.index
            if selected_tab == 0:
                # Perform actions for the first tab
                self.update_selected_sentences()
            elif selected_tab == 1:
                # Perform actions for the second tab
                self.update_selected_sentences()


        def update_descriptions(widget):
            print("update_descriptions is called!")
            is_enemy = self.ally_enemy_toggle.value if self.ally_enemy_toggle else False
            print(f"is_enemy: {is_enemy}")

            # Update current_state dictionary
            self.current_state['allyenemy'] = 'Enemy' if is_enemy else 'Ally'

            # Initialize a dict to hold active categories and their corresponding descriptions
            self.current_state['active_categories'] = {}

            # Update the descriptions for all, irrespective of their state
            for category, sub_categories_and_rolls in self.data['AllyEnemyTables'].items():
                sub_categories = {key: val for key, val in sub_categories_and_rolls.items() if key != 'rolls'}

                for dice_roll, data in sub_categories.items():
                    choices, description = data['choices'], data['description']
                    replaced_description = description.replace('{{temperment}}', choices[1] if is_enemy else choices[0])
                    wrapped_description = wrap_text(replaced_description, 75)

                    # Update the label's text regardless of its switch state
                    description_labels[category][dice_roll].text = wrapped_description

                    # Only store it in the current_state if it's selected (switch is on)
                    if self.switch_states.get(category, {}).get(dice_roll, False):
                        # Update the current_state dictionary
                        if category not in self.current_state['active_categories']:
                            self.current_state['active_categories'][category] = []
                        self.current_state['active_categories'][category].append(wrapped_description)

            self.update_selected_sentences()

        self.is_enemy = False
        is_enemy = False
        self.ally_enemy_toggle = toga.Switch(text=None, on_change=update_descriptions)
        self.ally_label = toga.Label('Ally', style=big_header_style)
        self.enemy_label = toga.Label('Enemy', style=big_header_style)

        self.ally_enemy_box = toga.Box(style=Pack(direction=ROW, padding=5, alignment=CENTER))

        self.ally_enemy_box.add(self.ally_label)
        self.ally_enemy_box.add(self.ally_enemy_toggle)
        self.ally_enemy_box.add(self.enemy_label)

        with open(yaml_path, 'r') as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)



        # Create a box for the "Display" option
        display_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Create a label to show selected sentences (this will be filled later)
        self.selected_sentences_label = toga.Label(f"{selected_sentences}", style=Pack(padding=(0, 5)))
        display_box.add(self.selected_sentences_label)

        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

        # Create an OptionContainer
        option_container = toga.OptionContainer()

        # Create a ScrollContainer for the main_box
        scroll_container = toga.ScrollContainer(horizontal=False, vertical=True)
        scroll_container.content = main_box




        main_box.add(self.ally_enemy_box)
        self.dice_label = toga.Label('Dice Result: 0', style=big_header_style)
        self.roll_button = toga.Button('Roll All Categories', on_press=self.roll_dice, style=Pack(padding=5, width=150))




        main_box.add(self.roll_button)

        self.switch_states = {}
        self.checkboxes = {}
        self.selected_sentences = []


        # Add the "Build" tab and its contents (now wrapped in a ScrollContainer)
        option_container.add("Build", scroll_container)

        # Add the "Display" tab and its contents
        option_container.add("Display", display_box)

        # Set the OptionContainer as the main window content
        self.main_window = toga.MainWindow(title=self.formal_name,size=(750, 1334))
        self.main_window.content = option_container
        self.main_window.show()


        for category, sub_categories_and_rolls in self.data['AllyEnemyTables'].items():
            #print("sub_categories_and_rolls:", sub_categories_and_rolls)
            num_rolls = sub_categories_and_rolls['rolls']
            sub_categories = sub_categories_and_rolls.copy()  # make a shallow copy
            del sub_categories['rolls']  # remove the 'rolls' entry
            roll_label = toga.Label("", style=roll_label_style)
            category_and_roll_box = toga.Box(style=Pack(padding=(0, 0), direction=COLUMN, alignment=CENTER))
            #Orig width 31
            if len(str(category)) < 45:
                diff = 45 - len(str(category))
                padding = ' ' * (diff // 2)

                # If the difference is odd, add one more space at the end
                extra_space = ' ' if diff % 2 != 0 else ''

                padded_category = f"{padding}{category}{padding}{extra_space}"
            else:
                padded_category = str(category)

            wrapped_category = wrap_text(padded_category, 75)
            category_button = toga.Button(f"{wrapped_category}", on_press=self.roll_dice_for_category(category, roll_label, num_rolls), style=header_style)

            self.checkboxes[category] = {}
            self.switch_states[category] = {}

            # Add category button and roll label to the new Box
            category_and_roll_box.add(category_button)
            category_and_roll_box.add(roll_label)

            category_box = toga.Box(style=Pack(direction=ROW, padding=5))
            category_box.add(category_and_roll_box)
            main_box.add(category_box)

            for dice_roll, data in sub_categories.items():
                if len(str(dice_roll)) < 6:
                    padded_dice_roll = str(dice_roll) + "  "
                else:
                    padded_dice_roll = str(dice_roll)
                inner_box = toga.Box(style=Pack(direction=ROW, padding=5, alignment=CENTER))
                choice_switch = toga.Switch(text=f"{padded_dice_roll}")
                self.checkboxes[category][dice_roll] = choice_switch
                self.switch_states[category][dice_roll] = False

                inner_box.add(choice_switch)

                choices, description = data['choices'], data['description']
                replaced_description = description.replace('{{temperment}}', choices[1] if is_enemy else choices[0])
                wrapped_description = wrap_text(replaced_description, 75)

                self.selected_sentences.append(replaced_description)

                description_label = toga.Label(f"{wrapped_description}", style=Pack(padding=(0, 5)))
                description_labels.setdefault(category, {})[dice_roll] = description_label
                inner_box.add(description_label)

                main_box.add(inner_box)

        scroll_container = toga.ScrollContainer(horizontal=False, vertical=True)
        #scroll_container.content = main_box



    def roll_dice(self, widget):
        roll = random.randint(1, 100)
        self.dice_label.text = f"Dice Result: {roll}"
        self.roll_button.text = f"Roll All Categories"

        # Roll dice for all categories
        for category, sub_categories_and_rolls in self.data['AllyEnemyTables'].items():
            num_rolls = sub_categories_and_rolls['rolls']
            roll_label = toga.Label("", style=Pack(padding=(0, 10), font_family="NotoSansMono", font_size=15))
            self.roll_dice_for_category(category, roll_label, num_rolls)(widget)

    def roll_dice_for_category(self, category, roll_label, num_rolls=1):
        def _inner_roll(widget):
            groups = set()  # Use a set to keep track of unique groups
            rolls = []

            while len(rolls) < num_rolls:
                roll = random.randint(1, 100)
                group = None

                # Determine which group this roll belongs to
                for roll_value in self.checkboxes[category]:
                    if '-' in roll_value:
                        lower, upper = map(int, roll_value.split('-'))
                        if lower <= roll <= upper:
                            group = (lower, upper)
                            break
                    elif int(roll_value) == roll:
                        group = (roll, roll)
                        break

                # Add the roll if its group is unique
                if group not in groups:
                    rolls.append(roll)
                    if group is not None:  # Add the group to our set
                        groups.add(group)

            roll_label.text = f"Dice Roll: {', '.join(map(str, rolls))}"

            # Update the switches
            for roll_value, switch in self.checkboxes[category].items():
                should_be_on = False
                if '-' in roll_value:
                    lower, upper = map(int, roll_value.split('-'))
                    should_be_on = any(lower <= roll <= upper for roll in rolls)
                else:
                    should_be_on = any(int(roll_value) == roll for roll in rolls)

                if should_be_on != self.switch_states[category][roll_value]:
                    switch.toggle()
                    self.switch_states[category][roll_value] = should_be_on


        return _inner_roll


    def update_selected_sentences(self):
        """
        Update the {selected_sentences} variable with selected sentence data.
        """

        def wrap_text(text, max_width):
            words = text.split(' ')
            lines = []
            current_line = []

            for word in words:
                if len(' '.join(current_line) + ' ' + word) > max_width:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)

            lines.append(' '.join(current_line))
            return '\n'.join(lines)

        selected_sentences_list = []
        is_enemy = self.ally_enemy_toggle.value if hasattr(self, 'ally_enemy_toggle') else False
        if not hasattr(self, 'temperment_selected'):
            print("Warning: temperment_selected not initialized.")
            return

        if not hasattr(self, 'data') or 'AllyEnemyTables' not in self.data:
            print("Warning: data or AllyEnemyTables not initialized.")
            return

        for category, sub_categories_and_rolls in self.data['AllyEnemyTables'].items():
            sub_categories = {key: val for key, val in sub_categories_and_rolls.items() if key != 'rolls'}
            for dice_roll, data in sub_categories.items():
                choices, description = data['choices'], data['description']
                replaced_description = description.replace('{{temperment}}', choices[1] if is_enemy else choices[0])
                wrapped_description = wrap_text(replaced_description, 75)
                selected_sentences_list.append(f"{category}:\n\t{wrapped_description}")

        self.selected_sentences = "\n".join(selected_sentences_list)

        if hasattr(self, 'selected_sentences_label'):
            self.selected_sentences_label.text = self.selected_sentences if selected_sentences_list else "No features selected."
        else:
            print("Warning: selected_sentences_label not initialized.")


def main():
    return WeckterBackstoryGenerator()

if __name__ == '__main__':
    main().main_loop()
