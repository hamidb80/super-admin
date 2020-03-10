from argparse import ArgumentParser


def get_args()-> dict:
    parser = ArgumentParser()
    parser.add_argument('--test', '-t', help='is test?',
                        action='store_true',)

    parser.add_argument('--input-file', '--inpf',
                        help='input file path', type=str, default='')

    parser.add_argument('--output-file', '--outf',
                        help='input file path', type=str, default='')

    args = parser.parse_args()

    if args.test is True:
        assert bool(args.output_file and args.input_file) is True

    return {
        'test': args.test,
        'input_file': args.input_file,
        'output_file': args.output_file
    }
