from helpers import generate_link, generate_temperature, ref_encode
import units

class RecipeAsciidocPresenter(object):
    def __init__(self, recipe):
        self._data = recipe.data

    @property
    def data(self):
        return self._data

    @property
    def config_id(self):
        rendered = f"[[{ref_encode(self.data['config_id'])}]]"

        return rendered

    @property
    def name(self):
        rendered = f"=== {self.data['name']}"

        return rendered

    @property
    def summary(self):    
        if self.data['summary']:
            rendered = f"\nSummary: {self.data['summary']}\n"
        else:
            rendered = ''

        return rendered

    @property
    def servings(self):
        rendered = f"Yield: {self.data['servings']}\n"

        return rendered

    @property
    def preptime(self):
        rendered = f"Prep Time: {self.data['preptime']}\n"

        return rendered

    @property
    def cooktime(self):
        rendered = f"Cook Time: {self.data['cooktime']}\n"

        return rendered


    @property
    def equipment(self):
        equipment = []
        for item in self.data['equipment']:
            link = generate_link(item)
            equipment.append('* ' + link)

        rendered = 'Equipment:\n\n' + '\n'.join(equipment) + '\n'

        return rendered

    @property
    def ingredients(self):
        ingredients = []
        for item in self.data['ingredients']:
            name = item['name']
            quantity = units.parse_amount_with_unit(item['quantity']) 

            if quantity.units == units.NO_UNIT:
                text = f"{quantity.magnitude:g} {name}"
            else:
                text = f"{quantity:~g} of {name}"

            if 'link' in item:
                link = item['link']
                if link.startswith('equipment:') or link.startswith('ingredient:') or link.startswith('recipe:'):
                    line = f"* <<{ref_encode(link)}, {text}>>"
                elif link.startswith('http://') or link.startswith('https://'):
                    line = f'* {link}[{text}]'
                else:
                    line = f'* {text}'
            else:
                line = f'* {text}'

            ingredients.append(line)

        rendered = 'Ingredients:\n\n' + '\n'.join(ingredients) + '\n'

        return rendered

    @property
    def directions(self):
        steps = []
        for direction in self.data['directions']:
            step = '. ' + direction['step']
            if 'note' in direction.keys():
                step += ' +\n  Note: ' + direction['note']
            steps.append(generate_temperature(step))

        rendered = 'Steps:\n\n' + '\n'.join(steps)

        return rendered

    @property
    def notes(self):
        notes = []
        for note in self.data['notes']:
            notes.append('* ' + note)

        if notes:
            rendered = '\nNotes:\n\n' + '\n'.join(notes) + '\n\n'
        else:
            rendered = ''

        return rendered

    def render(self):
        recipe_parts = [
            self.config_id,
            self.name,
            self.summary,
            self.servings,
            self.preptime,
            self.cooktime,
            self.equipment,
            self.ingredients,
            self.directions,
            self.notes,
            '<<<\n'
        ]
        return '\n'.join(recipe_parts)

