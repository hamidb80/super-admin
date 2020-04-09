from argparse import ArgumentParser


def get_args()-> dict:
    parser = ArgumentParser()
    parser.add_argument('--test', '-t', help='is test?',
                        action='store_true',)

    args = parser.parse_args()

    return {
        'test': args.test,
    }
