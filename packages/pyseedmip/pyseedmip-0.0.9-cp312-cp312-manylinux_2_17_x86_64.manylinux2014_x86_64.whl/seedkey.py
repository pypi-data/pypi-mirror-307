import sys
from pyseedmip import License


def activate_license():
    if len(sys.argv) > 1:
        License.activate(sys.argv[1])
    else:
        print("Error: No key provided.")
        sys.exit(1)
