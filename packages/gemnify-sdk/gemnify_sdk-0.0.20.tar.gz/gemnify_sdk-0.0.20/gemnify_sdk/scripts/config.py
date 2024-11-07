from gemnify_sdk.scripts.utils import default_chain

class Config:
    def __init__(self, chain = default_chain):
        self.chain = chain
        self.node_rpc = None
        self.private_key = None
        self.chain_name = "arbitrum-sepolia"
        self.gas_increment = 5  # proportion of gas increase, percentage， default 5%
        self.logger_level = "fatal"
        self.logger_file_path = ""

    def set_node_rpc(self, value):
        self.node_rpc = value

    def set_chain_name(self, value):
        self.chain_name = value

    def set_logger_level(self, value):
        self.logger_level = value

    def set_logger_file_path(self, value):
        self.logger_file_path = value

    def set_private_key(self, value):
        self.private_key = value

    def set_gas_increment(self, value):
        self.gas_increment = value

    def set_url(self, value):
        self.url = value
