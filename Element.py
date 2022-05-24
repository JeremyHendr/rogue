class Element:
    def __init__(self,name,abr=False):
        self.name = name
        if not abr:
            self._abbrv = self.name[0]
        else:
            self._abbrv = abr

    def __repr__(self):
        return self._abbrv

    def description(self):
        return "<"+self.name+">"

    def meet(self,hero):
        raise NotImplementedError("Not implemented yet")