import ghostink


try:
    builtins = __import__('__builtin__')
except ImportError:
    builtins = __import__('builtins')


def ghostall(GhostInk='GhostInk'):
    setattr(builtins, GhostInk, ghostink.GhostInk)


def unghostall(GhostInk='GhostInk'):
    delattr(builtins, GhostInk)
