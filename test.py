

class Select:
    
    def __init__(self, source):
        self.source = source
        
    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            row = next(self.source)
            return row
        except StopIteration:
            raise

class From:
    
    def __init__(self):
        self.source = iter([1, 2, 3, 4])
        self.current_row = None
        self.current_index = 0
    
    def __iter__(sefl):
        return sefl
    
    def __next__(self):
        try:
            return next(self.source)
        except StopIteration:
            raise  


i = iter([1, 2, 4, 5])
k = iter(i)
