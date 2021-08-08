import apps
from apps import *

if __name__ == "__main__":
    for app in apps.__all__:
        print("{}.py - {}".format(app, apps.__dict__[app].make_parser().description))
