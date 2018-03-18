import numpy

class Formula:
    def __init__(self):

        self.v  = ''
        self.C  = []
        self.cmatrix = []

    def define_cmatrix(self):
        self.cmatrix = numpy.zeros((len(self.C),self.v))

        for c in self.C:
            for i in c:
                self.cmatrix[self.C.index(c)][abs(i)] = i


    def resolve_on(self, v):
        vector = numpy.zeros(self.v)
        vector[v] = 1


        