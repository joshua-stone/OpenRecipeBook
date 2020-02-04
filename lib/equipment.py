from helpers import join_params

class Equipment(object):
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

    def config_id(self, config_id):
        equipment = join_params(self.data, {'config_id': config_id })

        return self.__class__(**equipment)

    def name(self, name):
        equipment = join_params(self.data, {'name': name })

        return self.__class__(**equipment)

    def summary(self, name):
        equipment = join_params(self.data, {'summary': summary})

        return self.__class__(**equipment)

    def products(self, products):
        equipment = join_params(self.data, {'products': products })
        
        return self.__class__(**equipment)
    
    def add_product(self, name, stores, reviews):
        equipment = join_params(self.data, {'products': self.data['products'] + [{'name': name, 'stores': stores, 'reviews': reviews}]})

        return self.__class__(**equipment)       
