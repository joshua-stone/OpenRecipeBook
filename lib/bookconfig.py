from edition import Edition

class BookConfig(object):
    def __init__(self, config):
        self.editions = []
        self.params = dict(config)
        del self.params['editions']
        for edition in config['editions']:
            vals = {**self.params, **edition}
            self.editions.append(Edition(**vals))

    def __iter__(self):
        yield from self.editions
