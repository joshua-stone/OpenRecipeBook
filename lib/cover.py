class Cover(object):
    def __init__(self, title='', author='', email=''):
        self._data = {
            'title': title,
            'author': author,
            'email': email
        }

    @property
    def data(self):
        return self._data

    def title(self, title):
        equipment = join_params(self.data, {'title': title })

        return self.__class__(**equipment)

    def author(self, author):
        equipment = join_params(self.data, {'author': author })

        return self.__class__(**equipment)

    def email(self, email):
        equipment = join_params(self.data, {'email': email})

        return self.__class__(**equipment)

