import numpy

def numerov_integration(domain, a, f0, f1):
    f = numpy.zeros(len(domain), dtype=numpy.complex)
    f[0] = f0
    f[1] = f1

    step = domain.step
    for i in range(2, len(domain)):
        phi_i1 = f[i-1] * (2.0 + 5.0 * step**2 * a[i-1] / 6.0)
        phi_i2 = f[i-2] * (1.0 - step**2 * a[i-2] / 12.0)
        f[i] = (phi_i1 - phi_i2) / (1.0 - step**2 * a[i] / 12.0)

    return f
