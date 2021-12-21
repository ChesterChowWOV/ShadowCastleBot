import sys

_end = "\033[0m"

def red(*args, sep=" ", end="\n", file=sys.stdout, flush=False):
  print("\033[91m"+sep.join(args)+_end)

def green(*args, sep=" ", end="\n", file=sys.stdout, flush=False):
  print("\033[92m"+sep.join(args)+_end)

def blue(*args, sep=" ", end="\n", file=sys.stdout, flush=False):
  print("\033[94m"+sep.join(args)+_end)