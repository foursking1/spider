from collections import deque

class UrlGenerator(object):

    def __init__(self, url_pattern, max_depth, entity_path):
        self.url_pattern = url_pattern
        self.max_depth = max_depth
        self.entity_path = entity_path

    def __iter__(self):
        with open(self.entity_path) as f:
            for line in f:
                line = line.strip()
                for i in range(self.max_depth):
                    yield line, self.url_pattern % (line, i)

class UrlGenerator2(object):

    def __init__(self, url_pattern, entity_path):
        self.url_pattern = url_pattern
        self.entity_path = entity_path

    def __iter__(self):
        with open(self.entity_path) as f:
            for line in f:
                line = line.strip()
                yield line, self.url_pattern % line