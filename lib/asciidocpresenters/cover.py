class CoverAsciidocPresenter(object):
    def __init__(self, cover):
        self._data = cover.data

    @property
    def data(self):
        return self._data

    def render(self):
        return f'''= {self.data['title']}
{self.data['author']} <{self.data['email']}>
:doctype: book
:toc:
'''
