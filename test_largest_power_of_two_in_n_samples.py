

n_samples = 720000
base = 2

def largest_power_of_base(n, base = 2):
    """
    Returns the largest power of base in a number of samples
    :param n:       (integer) number of samples
    :param base:    (integer) base of power to be considered, default is 2
    :return:        (integer) largest power of base
    """
    count = 1
    while n // base > 1:
        count += 1
        n = n // base
    return base ** count

print(largest_power_of_base(n_samples, base))

