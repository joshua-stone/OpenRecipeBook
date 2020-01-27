class Chapter(object):
    def __init__(self, config_id='', title='', summary='', level=1):
        self._data = {
            'config_id': config_id, 
            'title': title,
            'summary': summary,
            'level': level
        }

    @property
    def data(self):
        return self._data

    def config_id(self, config_id):
        equipment = join_params(self.data, {'config_id': config_id })

    def title(self, title):
        equipment = join_params(self.data, {'title': title })

        return self.__class__(**equipment)

    def summary(self, summary):
        equipment = join_params(self.data, {'summary': summary })

    def level(self, level):
        equipment = join_params(self.data, {'level': level })


