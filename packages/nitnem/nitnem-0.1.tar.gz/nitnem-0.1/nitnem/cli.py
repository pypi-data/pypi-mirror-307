import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="Nitnem using python for Mac and possibly windows latter")
    parser.add_argument("name", type=str, help="Dummy argument")
    return parser


def cli():
    "Nitnem using python for Mac and possibly windows latter"
    parser = create_parser()
    args = parser.parse_args()
    mycommand(args)


def mycommand(args):
    print(args)