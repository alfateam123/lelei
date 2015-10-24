
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


@defaultsize(8)
@rangesize(0, 8)
def int8Checker(read_bits):
    return read_bits

@defaultsize(16)
@rangesize(0, 16)
def int16Checker(read_bits):
    return read_bits

@defaultsize(32)
@rangesize(0, 32)
def int32Checker(read_bits):
    return read_bits


@defaultsize(64)
@rangesize(0, 64)
def int64Checker(read_bits):
    return read_bits

@rangesize(1, None)
def spareChecker(read_bits):
	return read_bits

@defaultsize(32)
@rangesize(32, 32)
def float32Checker(read_bits):
    return read_bits

@defaultsize(64)
@rangesize(64, 64)
def float64Checker(read_bits):
    return read_bits


SIZE_CHECKERS = {
"uint8"  : int8Checker,
"uint16" : int16Checker,
"uint32" : int32Checker,
"uint64" : int64Checker,
"spare"  : spareChecker,
"float32": float32Checker,
"float64": float64Checker
}