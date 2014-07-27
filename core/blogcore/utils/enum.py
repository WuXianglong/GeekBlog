
class Enum(object):
    '''
    An enum type used in django convenience.

    >>> from enum import Enum
    >>> e = Enum({"ONE":(1,"One")})
    >>> print e.ONE
    1
    >>> print e.to_choices()
    ((1, 'One'),)
    >>> print e.to_dict()
    {1: 'One'}
    >>> print e.get_label(1)
    One
    >>> print e.get_key(1)
    ONE
    '''
    def __init__(self, mapping):
        self._DATA_MAPPING = mapping

    def __getattr__(self, name):
        if name in self._DATA_MAPPING:
            return self._DATA_MAPPING[name][0]
        return super(self, Enum).__getattr__(name)

    def to_choices(self):
        value_label_tuples = [ self._DATA_MAPPING[key] for key in self._DATA_MAPPING ]
        return tuple(value_label_tuples)

    def to_dict(self):
        value_label_dict = {}
        for key in self._DATA_MAPPING:
            value_label_dict[self._DATA_MAPPING[key][0]] = self._DATA_MAPPING[key][1]
        return value_label_dict

    def get_label(self, value):
        value_label_dict = self.to_dict()
        return value_label_dict[value]

    def get_key(self,value):
        for key in self._DATA_MAPPING:
            if self._DATA_MAPPING[key][0] == value:
                return key

if __name__ == "__main__":
    import doctest
    doctest.testmod()
