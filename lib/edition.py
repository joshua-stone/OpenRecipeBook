class Edition(object):
    def __init__(self, book_id='', title='', author='', email='', tags=[], totaltime=''):
        setattr(self, 'book_id', book_id)
        setattr(self, 'title', title)
        setattr(self, 'author', author)
        setattr(self, 'email', email)
        setattr(self, 'tags', tags)
        setattr(self, 'totaltime', totaltime)
