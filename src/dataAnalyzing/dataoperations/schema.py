'''
@author: hectorz
'''

class Schema(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.params = {}
    
    def __str__(self):
        s = '( \n'
        for name, type in self.params:
            s = s+ name + "\t"+ type + "\n"
        s = s+ '\n)'
        return s    
    
    def append(self, name, type):
        self.params[name] = type
        
    def getSize(self):
        return len(self.params)
        