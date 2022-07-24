from .anycmd import AnyCmd

def load_ipython_extension(ip):
  any_magic = AnyCmd(ip)
  ip.register_magics(any_magic)