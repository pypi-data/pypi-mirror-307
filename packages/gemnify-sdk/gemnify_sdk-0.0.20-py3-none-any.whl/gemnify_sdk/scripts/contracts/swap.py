from gemnify_sdk.scripts.instance import ContractInstance

class Swap:
    def __init__(self, config) -> None:
        self.instance = ContractInstance(config, 'Router')

    def swap(self, *args):
        return self.instance.create_transaction("swap", args)
