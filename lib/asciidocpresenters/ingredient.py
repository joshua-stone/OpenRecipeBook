from helpers import generate_link, generate_temperature, ref_encode

class IngredientAsciidocPresenter(object):
    def __init__(self, equipment):
        self._data = equipment.data

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
    def products(self):
        table = []
        for item in self.data['products']:
            ingredient_name = item['name']
            if 'stores' in item.keys():
                stores = []
                for store in item['stores']:
                    link = generate_link(store)
                    stores.append(link)

            table.append((ingredient_name, stores))

        flattened = []
        for product, links in table:
            flattened.append('| ' + product)
            flattened.append('| ' + ' +\n  '.join(links))

        rendered = '\n'.join(['|===\n| Product | Where to buy', *flattened, '|==='])

        return rendered


    def render(self):
        ingredient_parts = [
            self.config_id,
            self.name,
            self.summary,
            self.products,
        ]
        return '\n'.join(ingredient_parts) + '\n'

