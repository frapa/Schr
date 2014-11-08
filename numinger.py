import numpy
import matplotlib.pyplot as plt

h = 1.0

class Domain(object):
    def __init__(self, start, end, step_num):
        self.start = start
        self.end = end
        self.step_num = step_num + 1
        self.step = float(self.end - self.start) / float(step_num)

    def as_array(self):
        return numpy.linspace(self.start, self.end, self.step_num)

    def __len__(self):
        return self.step_num

def numerov_integration(domain, a, f0, f1):
    f = numpy.zeros(len(domain))
    f[0] = f0
    f[1] = f1

    step = domain.step
    for i in range(2, len(domain)):
        phi_i1 = f[i-1] * (2.0 + 5.0 * step**2 * a[i-1] / 6.0)
        phi_i2 = f[i-2] * (1.0 - step**2 * a[i-2] / 12.0)
        f[i] = (phi_i1 - phi_i2) / (1.0 - step**2 * a[i] / 12.0)

    return f

def schrod(domain, V, boundary_start, boundary_end, m=1.0, dE=0.1, E_max=10.0):
    # Find minimum of potential
    E_min = numpy.min(V)

    # Find eigenvalues of energy using the shooting method
    err = None
    for E in numpy.linspace(E_min, E_max, int((E_max - E_min)/dE)):
        a = 2.0*m*(V - E) / h**2

        psi = numerov_integration(domain, a, boundary_start, boundary_start+1.0)
        new_err = psi[-1]
        print(E, new_err)

        if err is not None and err*new_err < 0:
            # We found a energy eigenvalue!
            print("Eigenvalue:", E)

        err = new_err
