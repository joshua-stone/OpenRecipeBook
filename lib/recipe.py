class Recipe(object):
    def __init__(self, config_id='', name='', summary='', servings=1, preptime='1 min', cooktime='1 min', equipment=[],
                 ingredients=[], steps=[], directions=[], notes=[], tags=[]):
        self._data = {
            'config_id': config_id,
            'name': name,
            'summary': summary,
            'servings': servings,
            'preptime': preptime,
            'cooktime': cooktime,
            'equipment': equipment,
            'ingredients': ingredients,
            'steps': steps,
            'directions': directions,
            'notes': notes,
            'tags': tags
        }

    @property
    def data(self):
        return self._data

    def config_id(self, config_id):
        recipe = join_params(self.data, {'config_id': config_id})

        return self.__class__(**recipe)

    def name(self, name):
        recipe = join_params(self.data, {'name': name})

        return self.__class__(**recipe)

    def summary(self, name):
        recipe = join_params(self.data, {'summary': summary})

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

    def tags(self, tags):
        recipe = join_params(self.data, {'tags': tags})

        return self.__class__(**recipe)

