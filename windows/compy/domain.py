import numpy

class Domain(object):
    def __init__(self, start, end, step_num):
        self.start = start
        self.end = end
        self.step_num = step_num + 1
        self.step = float(self.end - self.start) / float(step_num)

    def get_value(self, n):
        return self.start + self.step * n

    def generator(self):
        for n in range(self.step_num):
            yield self.get_value(n)

    def as_array(self):
        return numpy.linspace(self.start, self.end, self.step_num)

    def __len__(self):
        return self.step_num
