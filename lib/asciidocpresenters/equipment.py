from helpers import generate_link, generate_temperature, ref_encode

class EquipmentAsciidocPresenter(object):
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
            equipment_name = item['name']
            reviews = []
            stores = []
            if 'stores' in item.keys():
                for store in item['stores']:
                    store_link = generate_link(store)
                    stores.append(store_link)

            if 'reviews' in item.keys():
                for review in item['reviews']:
                    review_link = generate_link(review)
                    reviews.append(review_link)

            table.append([equipment_name, reviews, stores])
        flattened = []
        for (product, reviews, links) in table:
            flattened.append('| ' + product)
            flattened.append('| ' + ' +\n  '.join(reviews))
            flattened.append('| ' + ' +\n  '.join(links))

        rendered = '\n'.join(['|===\n| Product | Reviews | Where to buy', *flattened, '|==='])

        return rendered

    def render(self):
        equipment_parts = [
            self.config_id,
            self.name,
            self.summary,
            self.products,
        ]
        return '\n'.join(equipment_parts) + '\n'

