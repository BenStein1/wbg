"""
RPG Character Backstory Generator
"""
import toga
#from toga import Clipboard
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.style.pack import BOLD, CENTER
import cryptography
from cryptography.fernet import Fernet
import base64
import random
import yaml
import platform
import os


from .supportfiles import aiprompt as ai
from .supportfiles import aistatblock




class WeckterBackstoryGenerator(toga.App):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(current_dir, 'supportfiles', 'AllyEnemyTables.yaml')
    keyfile_path = os.path.join(current_dir, 'supportfiles', 'wbg.tif')
    settings_yaml_path = os.path.join(current_dir, 'supportfiles', 'wbg_settings.yaml')
    font_path = os.path.join(current_dir, 'supportfiles', 'fonts', 'noto', 'NotoSansMono-Regular.ttf')
    font_path_bold = os.path.join(current_dir, 'supportfiles', 'fonts', 'noto', 'NotoSansMono-Bold.ttf')
    OPENAI_API_KEY = None

    def disable_method(func):
        def wrapper(*args, **kwargs):
            print(f"Method {func.__name__} is disabled for testing.")
        return wrapper


    def wrap_text(self, text, max_width):
        paragraphs = text.split('\n')
        wrapped_paragraphs = []

        for paragraph in paragraphs:
            words = paragraph.split(' ')
            lines = []
            current_line = []

            for word in words:
                if len(' '.join(current_line) + ' ' + word) > max_width:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)

            lines.append(' '.join(current_line))
            wrapped_paragraphs.append('\n'.join(lines))

        return '\n'.join(wrapped_paragraphs)


# Function to save the API key

    def save_api_key(self, widget):
        print(f"save_api_key retrieve new encryption key:", self.encryption_key)  # Debug print statement#key = Fernet.generate_key()  # Generate a key for encryption
        cipher_suite = Fernet(self.encryption_key)

        self.OPENAI_API_KEY = self.api_key_input.value

        self.generate_bio_button.enabled = True
        self.statblock_button.enabled = True


        bit_encoded_api_key = self.OPENAI_API_KEY.encode()

        bit_encoded_encrypted_api_key = cipher_suite.encrypt(bit_encoded_api_key)  # Encrypt the API key

# Load existing settings if the YAML file exists
        try:
            with open(self.settings_yaml_path, 'r') as f:
                settings = yaml.safe_load(f)
                if settings is None:
                    settings = {}
        except FileNotFoundError:
            settings = {}

# Update the API key in the settings
        if 'api_settings' not in settings:
            settings['api_settings'] = {}

        # Save the encrypted API key to settings_yaml_path
        bit_decoded_encrypted_api_key = bit_encoded_encrypted_api_key.decode()
        settings['api_settings']['api_key'] = (bit_decoded_encrypted_api_key)
        with open(self.settings_yaml_path, 'w') as f:
            yaml.safe_dump(settings, f)
        print(f"Saved encoded key:", bit_decoded_encrypted_api_key)
        print(f"save_api_key OPENAI_API_KEY:", self.OPENAI_API_KEY)# Debug print statement


    def on_text_change(self, widget):
        print("Called on_text_change.")
        self.save_display_settings()


    def on_field_focus_change(self, widget):
        print("Called on_field_focus_change.")
        self.save_display_settings()


    def save_display_settings(self, widget=None):
        print("Called save_display_settings.")
        # Collect the values from the text input fields
        char_name_value = self.character_name_input.value
        char_level_value = self.character_level_input.value
        char_race_value = self.character_race_input.value
        char_class_value = self.character_class_input.value
        print("Saving new AI Model:", self.aimodel_selection.value)
        self.aimodel = self.aimodel_selection.value

        try:
            with open(self.settings_yaml_path, 'r') as f:
                settings = yaml.safe_load(f)
        except FileNotFoundError:
            settings = {}

        if 'api_settings' not in settings:
            settings['api_settings'] = {}
            settings['api_settings']['ai_model'] = "gpt-3.5-turbo"


        settings['api_settings']['ai_model'] = self.aimodel

        if 'character_details' not in settings:
            settings['character_details'] = {}

        print("Create character dictionary.")
        # Create a dictionary to hold the settings
        settings['character_details']['name'] = char_name_value
        settings['character_details']['level'] = str(char_level_value)
        settings['character_details']['race'] = char_race_value
        settings['character_details']['class'] = char_class_value

        if self.aimodel == "gpt-4":
            input_cost_per_k = 0.03
            output_cost_per_k = 0.06
        elif self.aimodel == "gpt-3.5-turbo":
            input_cost_per_k = 0.0015
            output_cost_per_k = 0.002
        else:
            print("Warning: Unknown AI_MODEL. Using default costs/model.")
            self.aimodel = "gpt-3.5-turbo"
            input_cost_perk = 0.0015  # Default cost per token for input
            output_cost_perk = 0.002  # Default cost per token for output


        self.AI_INPUT_COST = input_cost_per_k
        self.AI_OUTPUT_COST = output_cost_per_k

        print("Write character settings.")
        # Write the settings to wbg_settings.yaml
        with open(self.settings_yaml_path, 'w') as f:
            yaml.safe_dump(settings, f)







    def load_settings(self):
        self.encryption_key = Fernet.generate_key()
        print(f"load_settings generate new encryption key:", self.encryption_key)# Generate a key for encryption
        try:
# Read the old decryption key from resources/wbg.tif
            with open(self.keyfile_path, 'rb') as f:
                decryption_key = f.read()

# Decrypt the API key
            cipher_suite = Fernet(decryption_key)
            print(f"load_settings old decryption key:", decryption_key)
# Load existing settings if the YAML file exists
            try:
                with open(self.settings_yaml_path, 'r') as f:
                    settings = yaml.safe_load(f)
                    if settings is None:
                        settings = {}
            except FileNotFoundError:
                settings = {}
            if 'api_settings' not in settings:
                settings['api_settings'] = {}

            print("load_settings bit decoding beginning...")
            bit_decoded_encrypted_api_key = settings['api_settings'].get('api_key', '')

            bit_encoded_encrypted_api_key = bit_decoded_encrypted_api_key.encode()

            bit_encoded_decrypted_api_key = cipher_suite.decrypt(bit_encoded_encrypted_api_key)

            bit_decoded_decrypted_api_key = bit_encoded_decrypted_api_key.decode()
            print("load_settings bit decoding ending...")

# Store the decrypted API key in an environment variable or attribute
            self.OPENAI_API_KEY = bit_decoded_decrypted_api_key
            print(f"load_settings OPENAI_API_KEY:", self.OPENAI_API_KEY)

            cipher_suite = Fernet(self.encryption_key)

            # Encrypt the API key using the new encryption key
            bit_encoded_encrypted_api_key = cipher_suite.encrypt(bit_encoded_decrypted_api_key)
            bit_decoded_encrypted_api_key = bit_encoded_encrypted_api_key.decode()


            # Save the encrypted API key to settings_yaml_path
            settings['api_settings']['api_key'] = bit_decoded_encrypted_api_key
            with open(self.settings_yaml_path, 'w') as f:
                yaml.safe_dump(settings, f)

        except FileNotFoundError:
            print("Settings file or decryption key file not found. Using default settings.")
        except Exception as e:
            print(f"An error occurred while loading settings: {e}")
            # Generate a new encryption key

        # Save the new encryption key to resources/wbg.tif
        with open(self.keyfile_path, 'wb') as f:
            f.write(self.encryption_key)






    def load_regular_settings(self):
        print(f"Load regular settings:")# Generate a key for encryption
        try:
            with open(self.settings_yaml_path, 'r') as f:
                settings = yaml.safe_load(f)
# Load character details if they exist
            print(f"Load character details:")
            character_details = settings.get('character_details', {})

            if 'name' in character_details:
                self.loaded_character_name = character_details['name']
                print(f"Name:", self.loaded_character_name)
            else:
                self.loaded_character_name = None
            if 'level' in character_details:
                self.loaded_character_level = character_details['level']
                print(f"Level:", self.loaded_character_level)
            else:
                self.loaded_character_level = None
            if 'race' in character_details:
                self.loaded_character_race = character_details['race']
                print(f"Race:", self.loaded_character_race)
            else:
                self.loaded_character_race = None
            if 'class' in character_details:
                self.loaded_character_class = character_details['class']
                print(f"Class:", self.loaded_character_class)
            else:
                self.loaded_character_class = None

            print(f"Attempting AI settings load...")
            ai_settings = settings.get('api_settings', {})

            if 'ai_model' in ai_settings:
                if settings['api_settings']['ai_model'] == 'gpt-4':
                    self.aimodel = 'gpt-4'
                    print(f"Loaded API model:", self.aimodel)
                    #self.aimodel_selection.value = aimodel_selection.items.find(name="gpt-4")
                else:
                    #self.aimodel_selection.value = aimodel_selection.items.find(name="gpt-3.5-turbo")
                    self.aimodel = 'gpt-3.5-turbo'
                    print(f"Loaded AI Model:", self.aimodel)
            else:
                ai_settings['ai_model'] = 'gpt-3.5-turbo'
                print(f"No AI Model Loaded... Using Default:", self.aimodel)

            if self.aimodel == "gpt-4":
                input_cost_per_k = 0.03
                output_cost_per_k = 0.06
            elif self.aimodel == "gpt-3.5-turbo":
                input_cost_per_k = 0.0015
                output_cost_per_k = 0.002
            else:
                print("Warning: Unknown AI_MODEL. Using default costs/model.")
                self.aimodel = "gpt-3.5-turbo"
                input_cost_perk = 0.0015  # Default cost per token for input
                output_cost_perk = 0.002  # Default cost per token for output

            self.AI_INPUT_COST = input_cost_per_k
            self.AI_OUTPUT_COST = output_cost_per_k

        except FileNotFoundError:
            print("Settings file or decryption key file not found. Using default settings.")
        except Exception as e:
            print(f"An error occurred while loading settings: {e}")




    def startup(self):

        self.load_settings()
        self.load_regular_settings()
        print(f"OPEN_API_KEY:", self.OPENAI_API_KEY)
        toga.Font.register("NotoSansMono", self.font_path)
        toga.Font.register("NotoSansMono", self.font_path_bold, weight=BOLD)
        custom_font = toga.Font("NotoSansMono", 14, weight=BOLD)

        big_header_style = Pack(
            padding=(0, 15),
            font_family="NotoSansMono",
            font_size=20,
            font_weight=BOLD,
            alignment=CENTER
            #width=400
        )

        if platform.system() == "Darwin":
            header_style = Pack(
                padding=(5, 0),
                font_family="NotoSansMono",
                font_size=15,
                font_weight=BOLD,
                alignment=CENTER,
                width=350
            )
        else:
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
            #width=400
        )



        description_labels = {}
        selected_sentences = "No features selected."
        self.temperament_selected = None
        self.combined_story = ""
        self.token_count = None
        self.total_aimessage_cost = 0


        def disable_method(func):
            def wrapper(*args, **kwargs):
                print(f"Method {func.__name__} is disabled for testing.")
            return wrapper



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
# Update the ally_enemy_label based on the switch state
            self.ally_enemy_label.text = 'Enemy of' if is_enemy else 'Ally of'
            self.update_combined_story()


            for category, sub_categories_and_rolls in self.data['AllyEnemyTables'].items():
                sub_categories = {key: val for key, val in sub_categories_and_rolls.items() if key != 'rolls'}

                for dice_roll, data in sub_categories.items():
                    choices, description = data['choices'], data['description']
                    replaced_description = description.replace('{{temperament}}', choices[1] if is_enemy else choices[0])
                    wrapped_description = self.wrap_text(replaced_description, 75)
                    description_labels[category][dice_roll].text = wrapped_description
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

        with open(self.yaml_path, 'r') as f:
            self.data = yaml.load(f, Loader=yaml.FullLoader)

# Create a new box for the 'ChatGPT Bio' tab
        chatgpt_bio_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
# Create a new box for the 'statblock' tab
        statblock_box = toga.Box(style=Pack(direction=COLUMN, padding=10))
# Create a new box for the 'appsettings' tab
        appsettings_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

# Create a button to generate the bio
        self.generate_bio_button = toga.Button('Generate Bio', on_press=self.generate_chatgpt_bio, enabled=False, style=Pack(padding=5, width=150))
        chatgpt_bio_box.add(self.generate_bio_button)


# Create a button to generate the bio
        self.statblock_button = toga.Button('Generate Statblock', on_press=self.generate_statblock, enabled=False, style=Pack(padding=5, width=150))
        statblock_box.add(self.statblock_button)



# Create a text input box for the API key

        self.api_key_input = toga.PasswordInput(placeholder='Enter OpenAI API Key', style=Pack(padding=5, width=250))
#Turn OpenAI Options on if API key filled in and fill in box
        if self.OPENAI_API_KEY:
            self.api_key_input.value = self.OPENAI_API_KEY
            self.generate_bio_button.enabled = True
            self.statblock_button.enabled = True

# Add items to Settings tab
# Create a button to save the API key
        save_button = toga.Button('Save API Key', on_press=self.save_api_key, style=Pack(padding=5, width=150))
                # Create a box to hold the input field and button
        self.api_key_label = toga.Label('OpenAI API Key:', style=Pack(direction=ROW, padding=10, alignment=CENTER))
        self.ai_keywarn_label = toga.Label('Enter an OpenAI API Key to enable ChatGPT features.\n https://platform.openai.com/account/api-keys', style=Pack(direction=ROW, padding=3, alignment=CENTER))
        apibox = toga.Box(children=[self.api_key_label, self.api_key_input])
        appsettings_box.add(apibox)
        appsettings_box.add(save_button)

        self.aimodel_selection = toga.Selection(items=["gpt-3.5-turbo", "gpt-4"], on_select=self.on_field_focus_change, style=Pack(padding=5, width=150))


        self.aimodel_label = toga.Label('Select AI Model:', style=Pack(direction=ROW, padding=10, alignment=CENTER))
        self.aimodel_cost_label = toga.Label('GPT 3.5 ~ $0.002 per Bio\nGPT 4    ~ $0.06  per Bio', style=Pack(direction=ROW, padding=5, alignment=CENTER))
        self.formatted_total_aimessage_cost = "${:.4f}".format(self.total_aimessage_cost)
        self.token_cost_label = toga.Label('Cost this session: $0.00', style=Pack(direction=ROW, padding=(10,0,0,20) , alignment=CENTER))
        #self.token_cost_label.text = self.formatted_total_aimessage_cost
        aimodel_box = toga.Box(children=[self.aimodel_label, self.aimodel_selection])
        appsettings_box.add(aimodel_box)
        appsettings_box.add(self.aimodel_cost_label)
        appsettings_box.add(self.token_cost_label)



        char_save_button = toga.Button('Save Character Details', on_press=self.save_display_settings, style=Pack(padding=(25,5,0,0), width=150))
        # Create a box to hold the input field and button
        save_char_box = toga.Box(children=[char_save_button])
        appsettings_box.add(save_char_box)

###############################################




        self.rolled_details_header = toga.Label(f"---Text Copy Area for Exporting Stories---", style=Pack(direction=ROW, padding=(10,0,0,115) , alignment=CENTER))
        self.rolled_details_label = toga.Label(f"Rolled Details:", style=Pack(direction=ROW, padding=(10,12,0,0) , alignment=CENTER))
        self.rolled_details_TextInput = toga.TextInput(value=self.combined_story, readonly=True, style=Pack(padding=5, width=275))

        rolled_details_box = toga.Box(children=[self.rolled_details_label, self.rolled_details_TextInput])
        appsettings_box.add(self.rolled_details_header)
        appsettings_box.add(rolled_details_box)



        self.cgpt_bio_copy_label = toga.Label(f"ChatGPT Bio:", style=Pack(direction=ROW, padding=(10,17,0,0) , alignment=CENTER))
        self.cgpt_bio_copy_TextInput = toga.TextInput(value=self.combined_story, readonly=True, style=Pack(padding=5, width=275))

        cgpt_bio_copy_box = toga.Box(children=[self.cgpt_bio_copy_label, self.cgpt_bio_copy_TextInput])
        appsettings_box.add(cgpt_bio_copy_box)



        self.cgpt_stat_copy_label = toga.Label(f"ChatGPT Stats:", style=Pack(direction=ROW, padding=(10,5,0,0) , alignment=CENTER))
        self.cgpt_stat_copy_TextInput = toga.TextInput(value=self.combined_story, readonly=True, style=Pack(padding=5, width=275))

        cgpt_stat_copy_box = toga.Box(children=[self.cgpt_stat_copy_label, self.cgpt_stat_copy_TextInput])
        appsettings_box.add(cgpt_stat_copy_box)

        appsettings_box.add(self.ai_keywarn_label)




###############################################


# Create a box for the "Display" option
        display_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

# Create a box for the new 'Ally of'/'Enemy of' label and text box
        ally_enemy_name_box = toga.Box(style=Pack(direction=ROW, padding=5, alignment=CENTER))
        ally_enemy_name_box2 = toga.Box(style=Pack(direction=ROW, padding=5, alignment=CENTER))


# Create a text input for the D&D character name
        self.ally_enemy_header = toga.Label('    ', style=Pack(alignment=CENTER))
        self.ally_enemy_label = toga.Label('Ally of', style=Pack(direction=ROW, padding=5, alignment=CENTER))
        self.al_en_box = toga.Box(children=[self.ally_enemy_header, self.ally_enemy_label], style=Pack(direction=COLUMN, alignment=CENTER))

        self.character_name_label = toga.Label('Character Name', style=Pack(alignment=CENTER))
        self.character_name_input = toga.TextInput(placeholder='Enter RPG character name', style=Pack(padding=5, width=225))

        self.character_name_box = toga.Box(children=[self.character_name_label, self.character_name_input], style=Pack(direction=COLUMN, alignment=CENTER))

        self.character_level_label = toga.Label('Level', style=Pack(alignment=CENTER))
        self.character_level_input = toga.NumberInput(min_value=1, value=1, step=1, style=Pack(padding=5))

        self.character_level_box = toga.Box(children=[self.character_level_label, self.character_level_input], style=Pack(direction=COLUMN, alignment=CENTER))

        self.character_race_label = toga.Label('Character Race', style=Pack(alignment=CENTER))
        self.character_race_input = toga.TextInput(placeholder='Enter RPG character race', style=Pack(padding=(0, 5, 0, 0), width=175))#old padding padding=(0, 5, 0, 25)

        self.character_race_box = toga.Box(children=[self.character_race_label, self.character_race_input], style=Pack(direction=COLUMN, alignment=CENTER))

        self.character_class_label = toga.Label('Character Class', style=Pack(alignment=CENTER))
        self.character_class_input = toga.TextInput(placeholder='Enter D&D character class', style=Pack(padding=5, width=175))

        self.character_class_box = toga.Box(children=[self.character_class_label, self.character_class_input], style=Pack(direction=COLUMN, alignment=CENTER))


# Add the new box to the "Display" tab
        display_box.add(ally_enemy_name_box)
        display_box.add(ally_enemy_name_box2)
# Add the label and text input to the box
        ally_enemy_name_box.add(self.al_en_box)
        ally_enemy_name_box.add(self.character_name_box)
        ally_enemy_name_box.add(self.character_level_box)
        ally_enemy_name_box2.add(self.character_race_box)
        ally_enemy_name_box2.add(self.character_class_box)

        self.bio = ""
        self.statblock = ""

# Create a label to show selected sentences (this will be filled later)
        self.selected_sentences_label = toga.Label(f"{selected_sentences}", style=Pack(padding=(0, 5)))

        display_box.add(self.selected_sentences_label)

# Create a label to show chatgpt_bio (this will be filled later)
        self.chatgpt_bio_label = toga.Label(f"{self.bio}", style=Pack(padding=(0, 5)))
        chatgpt_bio_box.add(self.chatgpt_bio_label)

# Create a label to show statblock (this will be filled later)
        self.statblock_label = toga.Label(f"{self.statblock}", style=Pack(padding=(0, 5)))
        statblock_box.add(self.statblock_label)

        main_box = toga.Box(style=Pack(direction=COLUMN, padding=10))

# Create an OptionContainer
        option_container = toga.OptionContainer()

# Create a ScrollContainer for the main_box
        scroll_container = toga.ScrollContainer(horizontal=False, vertical=True)
        scroll_container.content = main_box

# Create a ScrollContainer for the chatgpt_bio_box
        scroll_container_chatgpt = toga.ScrollContainer(horizontal=False, vertical=True)
        scroll_container_chatgpt.content = chatgpt_bio_box
# Create a ScrollContainer for the statblock_box
        scroll_container_statblock = toga.ScrollContainer(horizontal=False, vertical=True)
        scroll_container_statblock.content = statblock_box
# Create a ScrollContainer for the appsettings_box
        scroll_container_appsettings = toga.ScrollContainer(horizontal=False, vertical=True)
        scroll_container_appsettings.content = appsettings_box



        self.active_scroll_container = None

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

# Add the new 'ChatGPT Bio' tab and its contents (now wrapped in a ScrollContainer)
        option_container.add("ChatGPT Bio", scroll_container_chatgpt)

# Add the new 'ChatGPT Statblock' tab and its contents (now wrapped in a ScrollContainer)
        option_container.add("ChatGPT Stats", scroll_container_statblock)

# Add the new 'Settings' tab and its contents (now wrapped in a ScrollContainer)
        option_container.add("Settings", scroll_container_appsettings)

# Set the OptionContainer as the main window content
        self.main_window = toga.MainWindow(title=self.formal_name,size=(430, 932))
        self.main_window.content = option_container

######SET VALUES######

        self.main_window.show()

        if not hasattr(self, 'aimodel'):
            print("Warning: Unknown AI_MODEL. Using default costs/model.")
            self.aimodel = "gpt-3.5-turbo"
            input_cost_perk = 0.0015
            output_cost_perk = 0.002



        self.aimodel_selection.value = self.aimodel
        self.character_name_input.on_change = self.update_combined_story
        self.character_race_input.on_change = self.update_combined_story
        self.character_class_input.on_change = self.update_combined_story

        if hasattr(self, 'loaded_character_name'):
            if self.loaded_character_name:
                self.character_name_input.value = self.loaded_character_name
        if hasattr(self, 'loaded_character_level'):
            if self.loaded_character_level:
                self.character_level_input.value = self.loaded_character_level
        if hasattr(self, 'loaded_character_race'):
            if self.loaded_character_race:
                self.character_race_input.value = self.loaded_character_race
        if hasattr(self, 'loaded_character_class'):
            if self.loaded_character_class:
                self.character_class_input.value = self.loaded_character_class

######SET VALUES######

        for category, sub_categories_and_rolls in self.data['AllyEnemyTables'].items():
#print("sub_categories_and_rolls:", sub_categories_and_rolls)
            num_rolls = sub_categories_and_rolls['rolls']
            sub_categories = sub_categories_and_rolls.copy()  # make a shallow copy
            del sub_categories['rolls']  # remove the 'rolls' entry
            roll_label = toga.Label("", style=roll_label_style)
            category_and_roll_box = toga.Box(style=Pack(padding=(0, 0), direction=COLUMN, alignment=CENTER))

            if platform.system() == "Darwin":
                wrap_value = 1
            else:
                wrap_value = 45
            if len(str(category)) < wrap_value:
                diff = wrap_value - len(str(category))
                padding = ' ' * (diff // 2)

# If the difference is odd, add one more space at the end
                extra_space = ' ' if diff % 2 != 0 else ''

                padded_category = f"{padding}{category}{padding}{extra_space}"
            else:
                padded_category = str(category)

            wrapped_category = self.wrap_text(padded_category, 75)
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
                choice_switch.on_change = lambda s=choice_switch, c=category, r=dice_roll: self.on_switch_toggle(s, c, r)

                self.checkboxes[category][dice_roll] = choice_switch
                self.switch_states[category][dice_roll] = False

                inner_box.add(choice_switch)

                choices, description = data['choices'], data['description']
                replaced_description = description.replace('{{temperament}}', choices[1] if is_enemy else choices[0])
                wrapped_description = self.wrap_text(replaced_description, 45)

                self.selected_sentences.append(replaced_description)

                description_label = toga.Label(f"{wrapped_description}", style=Pack(padding=(0, 5)))
                description_labels.setdefault(category, {})[dice_roll] = description_label
                inner_box.add(description_label)

                main_box.add(inner_box)

        scroll_container = toga.ScrollContainer(horizontal=False, vertical=True)


    def disable_method(func):
        def wrapper(*args, **kwargs):
            print(f"Method {func.__name__} is disabled for testing.")
        return wrapper



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
            self.update_selected_sentences()

        return _inner_roll


    def update_selected_sentences(self):
        print("update_selected_sentences is called!")
# Clear out existing selected_sentences
        self.selected_sentences = {}

        sentences = {}
        for category, switch_state in self.switch_states.items():
            num_rolls = self.data['AllyEnemyTables'][category].get('rolls', 1)
            selected_descriptions = []
            for dice_roll, is_selected in switch_state.items():
                if is_selected:
                    description_data = self.data['AllyEnemyTables'][category][dice_roll]
                    description = description_data['description']
                    choices = description_data.get('choices', [])

# Replace temperament placeholder if available
                    replaced_description = description.replace('{{temperament}}', choices[1] if self.ally_enemy_toggle.value else choices[0])
                    selected_descriptions.append(replaced_description)

            if num_rolls > 1:
                sentences[category] = ", ".join(selected_descriptions)
            elif selected_descriptions:
                sentences[category] = selected_descriptions[0]

        final_sentences = []
        for category, desc in sentences.items():
            final_sentences.append(f"{category}:\n\t {desc}\n")

        self.selected_sentences_label.text = "\n".join(final_sentences)
        self.update_combined_story()


    def update_combined_story(self, widget=None):
        self.combined_story = f"{self.ally_enemy_label.text}: My character (Name: {self.character_name_input.value}, Race: {self.character_race_input.value}, Class/Profession: {self.character_class_input.value})\n{self.selected_sentences_label.text}"
        print("Updated Combined Story:", self.combined_story)  # For debugging
        self.rolled_details_TextInput.value = self.combined_story



    def switch_toggled(widget):
        self.update_selected_sentences()


    def on_switch_toggle(self, switch, category, roll_value):
        is_on = switch.value if switch.value else False
        self.switch_states[category][roll_value] = is_on
        self.update_selected_sentences()


    def generate_chatgpt_bio(self, widget):
# Call the aiprompt.generate_bio method with the combined_story
        self.bio, self.completion_tokens, self.prompt_tokens = ai.generate_bio(self.combined_story, self.OPENAI_API_KEY, self.aimodel)
        print("Generated Bio:", self.bio)  # You can display this bio in the UI as needed
        wrapped_bio = self.wrap_text(self.bio, 115)
        self.chatgpt_bio_label.text = wrapped_bio
        self.cgpt_bio_copy_TextInput.value = self.chatgpt_bio_label.text
        print("Current cost basis:", self.aimodel, self.AI_INPUT_COST, self.AI_OUTPUT_COST)
        sent_cost = (self.completion_tokens/1000) * self.AI_INPUT_COST
        received_cost = (self.prompt_tokens/1000) * self.AI_OUTPUT_COST
        self.total_aimessage_cost += sent_cost + received_cost
        self.formatted_total_aimessage_cost = "${:.4f}".format(self.total_aimessage_cost)
        print("Message Cost:", self.formatted_total_aimessage_cost)
        self.token_cost_label.text = f"Total cost this session: {self.formatted_total_aimessage_cost}"



    def generate_statblock(self, widget):
# Call the aiprompt.generate_bio method with the combined_story
        enemy_statblock, self.completion_tokens, self.prompt_tokens = aistatblock.generate_statblock(self.bio, self.character_level_input.value, self.OPENAI_API_KEY, self.aimodel)
        print("Generated Statblock:", enemy_statblock)  # You can display this bio in the UI as needed
        wrapped_statblock = self.wrap_text(enemy_statblock, 115)
        self.statblock_label.text = wrapped_statblock
        self.cgpt_stat_copy_TextInput.value = self.statblock_label.text
        self.aimodel
        print("Current cost basis:", self.aimodel, self.AI_INPUT_COST, self.AI_OUTPUT_COST)
        sent_cost = (self.completion_tokens/1000) * self.AI_INPUT_COST
        received_cost = (self.prompt_tokens/1000) * self.AI_OUTPUT_COST
        self.total_aimessage_cost += sent_cost + received_cost
        self.formatted_total_aimessage_cost = "${:.4f}".format(self.total_aimessage_cost)
        print("Message Cost:", self.formatted_total_aimessage_cost)
        self.token_cost_label.text = f"Total cost this session: {self.formatted_total_aimessage_cost}"


def main():
    return WeckterBackstoryGenerator()

if __name__ == '__main__':
    main().main_loop()
