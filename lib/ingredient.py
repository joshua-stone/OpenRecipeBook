from helpers import join_params

class Ingredient(object):
    def __init__(self, config_id='', name='', summary='', products=[]):
        self._data = {
            'config_id': config_id,
            'name': name,
            'summary': summary,
            'products': products
        }

    @property
    def data(self):
        return self._data

    def config_id(self, name):
        ingredient = join_params(self.data, {'config_id': config_id })

        return self.__class__(**ingredient)

    def name(self, name):
        ingredient = join_params(self.data, {'name': name })

        return self.__class__(**ingredient)

    def summary(self, summary):
        ingredient = join_params(self.data, {'summary': summary})

        return self.__class__(**summary)

    def products(self, products):
        ingredient = join_params(self.data, {'products': products })

        return self.__class__(**ingredient)

    def add_product(self, name, stores):
        ingredient = join_params(self.data, {'products': self.data['products'] + [{'name': name, 'stores': stores}]})

        return self.__class__(**ingredient)
