import sys
from luxurylp.main import run_lp
from luxurylp.setup import setup


if __name__ == "__main__":
    if 'setup' in sys.argv:
        setup()
        exit()
    run_lp()