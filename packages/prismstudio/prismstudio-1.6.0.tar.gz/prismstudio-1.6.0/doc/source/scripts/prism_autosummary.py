from sphinx.ext.autosummary import Autosummary


class PrismAutosummary(Autosummary):

    def get_items(self, names):
        items = Autosummary.get_items(self, names)
        print(names)
        return items