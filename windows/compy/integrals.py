
def trapezioidal(D, f):
    result = 0.0

    for v in f[1:-1]:
        result += v

    result = D.step * (result + (f[0] + f[-1]) / 2.0)

    return result
