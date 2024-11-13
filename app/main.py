from broker import init_broker


def init():
    init_broker()
    print("Waiting for messages...")


init()
