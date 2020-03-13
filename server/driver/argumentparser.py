from argparse import ArgumentParser


def get_args()-> dict:
    parser = ArgumentParser()
    parser.add_argument('--password', '-p', help='is test?')

    args = parser.parse_args()

    return {
        'password': args.password
    }
