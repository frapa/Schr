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

def schrod(domain, V, boundary_start, boundary_end, m=1.0, dE=0.1, E_max=10.0,
        eigen_num=None, precision=0.0001):

    # Find minimum of potential
    E_min = numpy.min(V)

    # Find eigenvalues of energy using the shooting method
    # The following lines allow the function to accept both a range of energies
    # or a number of eigenvalues to be found
    if eigen_num is None:
        energies = numpy.linspace(E_min, E_max, int((E_max - E_min)/dE))
    else:
        # Generator of energies. In the following for loop
        # we will exit when we have found eigen_num number of eigenvalues
        def energies():
            n = 0
            while True:
                yield E_min + dE * n
                n += 1

        energies = energies()

    eigenvalues = []
    eigenfunctions = []
    err = None
    last_E = None
    for E in energies:
        a = 2.0*m*(V - E) / h**2

        psi = numerov_integration(domain, a, boundary_start, boundary_start+1.0)
        new_err = psi[-1] - boundary_end

        if err is not None and err*new_err < 0:
            # We found a energy eigenvalue!
            # Now, using the shooting method (bisection), we get the wave function
            # according to precision
            error = new_err # error instead of err to avoid confusion with outer loop
            E1 = last_E
            E2 = E
            while abs(error) > precision:
                E = (E2 + E1) / 2.0

                a = 2.0*m*(V - E) / h**2

                psi = numerov_integration(domain, a, boundary_start, boundary_start+1.0)
                new_error = psi[-1] - boundary_end

                if error*new_error < 0:
                    E1 = E2
                    E2 = E
                else:
                    E2 = E

                error = new_error

            eigenvalues.append(E)
            eigenfunctions.append(psi)

        if eigen_num is not None and len(eigenvalues) == eigen_num:
            break

        err = new_err
        last_E = E

    return (eigenvalues, eigenfunctions)
