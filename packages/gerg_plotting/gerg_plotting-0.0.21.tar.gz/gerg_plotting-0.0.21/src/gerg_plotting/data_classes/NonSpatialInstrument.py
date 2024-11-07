from attrs import define,asdict
from pprint import pformat


@define
class NonSpatialInstrument:
    def _has_var(self, key):
        return key in asdict(self).keys()
    def __getitem__(self, key):
        if self._has_var(key):
            return getattr(self, key)
        raise KeyError(f"Attribute '{key}' not found")
    def __setitem__(self, key, value):
        if self._has_var(key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Attribute '{key}' not found")
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self), indent=1,width=2,compact=True,depth=1)