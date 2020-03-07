from argparse import ArgumentParser


def get_args() -> dict:
    parser = ArgumentParser()
    parser.add_argument('--test', '-t', help='is test?',
                        action='store_True', type=bool)

    parser.add_argument('--input-file', '-inpf',
                        help='input file path', type=str, default='')

    parser.add_argument('--output-file', '-outf',
                        help='input file path', type=str, default='')

    args = parser.parse_args()

    if args.test is True:
        assert (args.inpf and args.outf) is True

    return {
        'test': args.test,
        'input_file': args.inpf,
        'output_file': args.outf
    }
