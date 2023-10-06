from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.lang import Builder
import random
import yaml

# Load the .kv file
Builder.load_file('supportfiles/BackstoryGenerator.kv')

class CustomBoxLayout(BoxLayout):
    pass

class CategoryBoxLayout(BoxLayout):
    pass

class ChoiceBoxLayout(BoxLayout):
    pass

class ChoiceInnerBox(BoxLayout):
    pass

class CategoryLabel(Label):
    pass

class CustomLabel(Label):
    pass

class DiceLabel(Label):
    pass

class BackstoryGenerator(App):
    def roll_dice(self, instance):
        roll = random.randint(1, 100)
        self.dice_label.text = f"Dice Result: {roll}"
        # Your code for checking the checkbox that matches the roll result should go here

    def build(self):
        scroll_view = ScrollView(size_hint=(1, 1))
        main_box = CustomBoxLayout()
        main_box.bind(minimum_height=main_box.setter('height'))

        # Add a button for rolling dice
        roll_button = Button(text="Roll Dice")
        roll_button.bind(on_press=self.roll_dice)
        main_box.add_widget(roll_button)

        # Add a label to display the dice roll result
        self.dice_label = DiceLabel(text="Dice Result: 0")
        main_box.add_widget(self.dice_label)

        # Load YAML data
        with open('supportfiles/AllyEnemyTables.yaml', 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        for category, sub_categories in data['AllyEnemyTables'].items():
            category_box = CategoryBoxLayout()
            category_box.bind(minimum_height=category_box.setter('height'))

            category_label = CategoryLabel()
            category_label.text = f"{category}"
            category_box.add_widget(category_label)

            choice_box = ChoiceBoxLayout()
            choice_box.bind(minimum_height=choice_box.setter('height'))

            for dice_roll, description in sub_categories.items():
                choice_inner_box = ChoiceInnerBox()

                choice_checkbox = CheckBox()
                choice_inner_box.add_widget(choice_checkbox)

                choice_label = CustomLabel()
                choice_label.text = f"{dice_roll}: {description}"
                choice_inner_box.add_widget(choice_label)

                choice_box.add_widget(choice_inner_box)

            category_box.add_widget(choice_box)
            main_box.add_widget(category_box)

        scroll_view.add_widget(main_box)
        return scroll_view

if __name__ == '__main__':
    BackstoryGenerator().run()
