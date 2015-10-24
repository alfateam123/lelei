
def maxsize(max_):
    def inner_dec(func):
        def inner_func(read_bits):
            if max_ < read_bits:
                raise ValueError("you are asking for %d bits, but the type can contain only %d!"%(read_bits, max_))
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

def negativenotallowed(func):
    def inner_func(read_bits):
        if read_bits < 0:
            raise ValueError("type sizes must be zero or higher than zero. no negative values allowed")
        return func(read_bits)
    return inner_func

def nonzero(func):
    def inner_func(read_bits):
        if read_bits == 0:
            raise ValueError("this type requires a size higher than zero")
        return func(read_bits)
    return inner_func



@negativenotallowed
@maxsize(8)
@defaultsize(8)
def int8Checker(read_bits):
    return read_bits

@negativenotallowed
@maxsize(16)
@defaultsize(16)
def int16Checker(read_bits):
    return read_bits

@negativenotallowed
@maxsize(32)
@defaultsize(32)
def int32Checker(read_bits):
    return read_bits


@negativenotallowed
@maxsize(64)
@defaultsize(64)
def int64Checker(read_bits):
    return read_bits

@nonzero
@negativenotallowed
def spareChecker(read_bits):
	return read_bits

SIZE_CHECKERS = {
"uint8" : int8Checker,
"uint16": int16Checker,
"uint32": int32Checker,
"uint64": int64Checker,
"spare" : spareChecker
}