import construct


_regbuiolder = construct.Int32sl.compile()

_regs = [0,0,0,0]


def write_register(addr: int, value: bytes):
    assert isinstance(addr, int), f"addr should be an integer, but was {type(addr)}"
    assert isinstance(value, bytes), f"value should be an integer, but was {type(value)}"
    value = _regbuiolder.parse(value)
    assert addr >= 0, f"addr should be greater or equal to 0, but was {addr}"
    assert addr < len(_regs), f"addr should be less than {len(_regs)}, but was {addr}"

    if addr >= 0 and addr <= 2:
     _regs[addr] = value
    print(_regs[0])
    if _regs[0] == 0x80:
        _regs[3] = _regs[1] + _regs[2]
    elif _regs[0] == 0x40:
        _regs[3] = _regs[1] - _regs[2]
    elif _regs[0] == 0x20:
        _regs[3] = _regs[1] * _regs[2]
    elif _regs[0] == 0x10:
        _regs[3] = _regs[1] // _regs[2]
    else:
        pass #invalid opcode... do nothing


def read_register(addr: int):
    assert isinstance(addr, int), f"addr should be an integer, but was {type(addr)}"
    assert addr >= 0, f"addr should be greater or equal to 0, but was {addr}"
    assert addr < len(_regs), f"addr should be less than {len(_regs)}, but was {addr}"

    return _regbuiolder.build(_regs[addr])
