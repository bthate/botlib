# This file is in the Public Domain.

kernels = []

def kernel():
    if kernels:
        return kernels[0]

def opts(ops):
    k = kernel()
    for opt in ops:
        if opt in k.cfg.opts:
            return True
    return False
        