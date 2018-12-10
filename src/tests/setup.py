import os
import sys

def setup():
    pth = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(pth)