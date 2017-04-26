class TestResults:
    def __init__(self,tag):
        self.tag = tag
        self.contents = {}

    def add_result(self,tag,parents,ratio,value):
        if not tag in results:
            results[tag] = ResultsCategory(parents, ratio, value)

    def get_tagged(self,tag):
        return self.contents[tag]

class ResultsCategory:
    def __init__(self,tag):
        self.tag = tag
        self.parents_range = None
        self.ratios_range = None
        self.contents = []

    def add_result(self,parents,ratio,value):
        self.contents.append(ResultEntry(parents, ratio, value))


class ResultEntry:
    def __init__(self,parents,ratio,value):
        self.parents = parents
        self.ratio = ratio
        self.value = value