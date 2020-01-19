class Recipe(object):
    def __init__(self, name='', servings=1, preptime='1 min', cooktime='1 min', equipment=[],
                 ingredients=[], steps=[], notes=[]):
        self._data = {
            'name': name,
            'servings': servings,
            'preptime': preptime,
            'cooktime': cooktime,
            'equipment': equipment,
            'ingredients': ingredients,
            'steps': steps,
            'notes': notes
        }

    @property
    def data(self):
        return self._data

    def name(self, name):
        recipe = join_params(self.data, {'name': name})

        return self.__class__(**recipe)

    def servings(self, servings):
        recipe = join_params(self.data, {'servings': servings})

        return self.__class__(**recipe)

    def preptime(self, preptime):
        recipe = join_params(self.data, {'preptime': preptime})

        return self.__class__(**updated)

    def cooktime(self, cooktime):
        recipe = join_params(self.data, {'cooktime': cooktime})

        return self.__class__(**recipe)

    def equipment(self, equipment):
        recipe = join_params(self.data, {'equipment': equipment})

        return self.__class__(**updated)

    def ingredients(self, ingredients):
        recipe = join_params(self.data, {'ingredients': ingredients})

        return self.__class__(**updated)

    def steps(self, steps):
        recipe = join_params(self.data, {'step': steps})

        return self.__class__(**updated)

    def notes(self, notes):
        recipe = join_params(self.data, {'notes': notes})

        return self.__class__(**recipe)
