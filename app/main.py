import sys
import os
from broker import init_broker


def init():
    print("Waiting for messages...")
    init_broker()


if __name__ == "__main__":
    try:
        init()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
