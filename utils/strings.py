def string_hash(string):
    prime = 307  # this is arbritrary prime
    m = 87178291199  # also arbitrary
    s = 0
    for i, chr in enumerate(string):
        val = ord(chr)
        s += val * (prime ** i)
    return s % m
