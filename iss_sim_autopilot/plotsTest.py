import matplotlib.pyplot as plt
rangeDist=23

class Switch(dict):
    def __getitem__(self, item):
        for key in self.keys():                   # iterate over the intervals
            if item in key:                       # if the argument is part of that interval
                return super().__getitem__(key)   # return its associated value
        raise KeyError(item)                      # if not in any interval, raise KeyError


switch = Switch({
    range(1, 21): 'a',
    range(21, 31): 'b'
})
print(switch(rangeDist))