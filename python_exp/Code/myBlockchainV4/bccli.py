import argparse
from Blockchain import BlockChain


def mine_block(args):
    args_dict = vars(args)
    data = args_dict['data']

    bc = BlockChain()
    bc.mine_block(data)


def print_chain(args):
    bc = BlockChain()
    bc.print_chain()


class BcCli(object):
    def __init__(self):
        self._parser = argparse.ArgumentParser()
        sub_parser = self._parser.add_subparsers(help='commands')

        print_parser = sub_parser.add_parser(
                       'printchain', help='Print all the blocks of the blockchain.')
        print_parser.set_defaults(func=print_chain)

        mine_parser = sub_parser.add_parser(
                      'mineblock', help='Mine a new block for the blockchain.')
        mine_parser.add_argument('-d', '--data', required=True, help='block data')
        mine_parser.set_defaults(func=mine_block)

    def run(self):
        args = self._parser.parse_args()
        if hasattr(args, 'func'):
            args.func(args)


if __name__ == '__main__':
    bccli = BcCli()
    bccli.run()
