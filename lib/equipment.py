from helpers import join_params

class Equipment(object):
    def __init__(self, name='', products=[]):
        self._data = {
            'name': name,
            'products': products
        }

    @property
    def data(self):
        return self._data

    def name(self, name):
        ingredient = join_params(self.data, {'name': name })

        return self.__class__(**ingredient)

    def products(self, products):
        ingredient = join_params(self.data, {'products': products })
        
        return self.__class__(**ingredient)
    
    def add_product(self, name, stores, reviews):
        ingredient = join_params(self.data, {'products': self.data['products'] + [{'name': name, 'stores': stores, 'reviews': reviews}]})

        return self.__class__(**ingredient)       
