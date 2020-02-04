from helpers import ref_encode

class ChapterAsciidocPresenter(object):
    def __init__(self, chapter):
        self._data = chapter.data

    @property
    def data(self):
        return self._data

    def render(self):
        return f'''[[{ref_encode(self.data['config_id'])}]]
{'=' * self.data['level']} {self.data['title']}

{self.data['summary']}

<<<
'''
