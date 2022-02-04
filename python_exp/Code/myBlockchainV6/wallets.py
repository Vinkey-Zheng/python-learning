import pickle
import wallet


class Wallets(object):
    WALLETS_FILE = 'wallets.db'

    def __init__(self):
        try:
            with open(Wallets.WALLETS_FILE, 'rb') as f:
                self._wallets = pickle.load(f)
        except FileNotFoundError:
            self._wallets = {}

    def create_wallet(self, comments=''):
        w = wallet.Wallet(comments)
        addr_str = w.address.get_address_str()
        self._wallets[addr_str] = w
        return w

    def get_wallet(self, addr_str):
        return self._wallets[addr_str]

    def get_addresses(self):
        return [addr for addr in self._wallets.keys()]

    def save_to_file(self):
        with open(Wallets.WALLETS_FILE, 'wb') as f:
            pickle.dump(self._wallets, f)
