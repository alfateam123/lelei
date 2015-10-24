
#use None to not set an explicit value
def rangesize(min_, max_):
    def inner_dec(func):
        def passCheck(n):
            if min_!=None and min_ > n: return False
            if max_!=None and max_ < n: return False
            return True

        def inner_func(read_bits):
            if not passCheck(read_bits):
                raise ValueError("you are asking for {} bits, but the type can only be inside [{}, {}] range!".format(
                    read_bits, min_, max_))
            return func(read_bits)
        return inner_func
    return inner_dec

def defaultsize(default_):
    def inner_dec(func):
        def inner_func(read_bits):
            if read_bits == 0:
                return default_
            return func(read_bits)
        return inner_func
    return inner_dec

@rangesize(1, None)
def spareChecker(read_bits):
    return read_bits

def paddingChecker(read_bits):
    return 0

def floatChecker(bits):
    @defaultsize(bits)
    @rangesize(bits, bits)
    def inner_func(read_bits):
        return read_bits
    return inner_func

def intChecker(bits):
    @defaultsize(bits)
    @rangesize(0, bits)
    def inner_func(read_bits):
        return read_bits
    return inner_func

def boolChecker(bits):
    @defaultsize(bits)
    @rangesize(bits, bits)
    def inner_func(read_bits):
        return read_bits
    return inner_func

SIZE_CHECKERS = {
"padding": paddingChecker,
"spare"  : spareChecker,
"float32": floatChecker(32),
"float64": floatChecker(64)
}

for i in range(1, 32+1):
    SIZE_CHECKERS["uint%d"%(i)] = intChecker(i)
    if i>=2:
        SIZE_CHECKERS["int%d"%(i)] = intChecker(i)

SIZE_CHECKERS["int40"] = intChecker(40)
SIZE_CHECKERS["int48"] = intChecker(48)
SIZE_CHECKERS["uint40"] = intChecker(40)
SIZE_CHECKERS["uint48"] = intChecker(48)
SIZE_CHECKERS["uint64"] = intChecker(64)

for i in [1, 8, 16, 32]:
    SIZE_CHECKERS["bool%i"%i] = boolChecker(i)
