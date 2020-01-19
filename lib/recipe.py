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
        return dict(self._data)

    def name(self, name):
        updated = self.data
        updated['name'] = name
        return self.__class__(**updated)

    def servings(self, servings):
        updated = self.data
        updated['servings'] = servings
        return self.__class__(**updated)

    def preptime(self, preptime):
        updated = self.data
        updated['preptime'] = preptime
        return self.__class__(**updated)

    def cooktime(self, cooktime):
        updated = self.data
        updated['cooktime'] = cooktime
        return self.__class__(**updated)

    def equipment(self, equipment):
        updated = self.data
        updated['equipment'] = equipment
        return self.__class__(**updated)

    def ingredients(self, ingredients):
        updated = self.data
        updated['ingredients'] = ingredients
        return self.__class__(**updated)

    def steps(self, steps):
        updated = self.data
        updated['steps'] = steps
        return self.__class__(**updated)

    def notes(self, notes):
        updated = self.data
        updated['notes'] = notes
        return self.__class__(**updated)
