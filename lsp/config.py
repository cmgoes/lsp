import sys, os

SAFE       = 1000
SAFE_UPPER = 1500
UNSAFE     = 2000  
DANGER     = 4000

RECURSION_LIMIT = DANGER
sys.setrecursionlimit(RECURSION_LIMIT)


DEBUG = False
EXIT_ON_ERROR = True
RECOVERING_FROM_ERROR = False

COLORS = True
if os.name == 'nt':  
    COLORS = False   
