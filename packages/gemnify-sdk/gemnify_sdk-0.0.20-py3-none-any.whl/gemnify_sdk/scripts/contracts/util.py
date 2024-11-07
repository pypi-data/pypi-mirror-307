from gemnify_sdk.scripts.instance import ContractInstance, get_contract_address
from gemnify_sdk.scripts.utils import get_token_address, default_chain
import time
from web3 import Web3
from gemnify_sdk.scripts.logging import getLogger

class Util:
    def __init__(self, config) -> None:
        self.web3 = Web3(Web3.HTTPProvider(config.node_rpc))
        self.config = config
        self.logger = getLogger(config)

    def mint_token(self, token_address, amount, receiver):
        instance = ContractInstance(self.config, 'Token', token_address)
        return instance.create_transaction("mint", [receiver, amount])

    # add liquidity
    def approve_token_to_ulp_manager(self, token_address, amount):
        instance = ContractInstance(self.config, 'Token', token_address)
        ulp_manger_address = get_contract_address("UlpManager", self.config.chain_name)
        return instance.create_transaction("approve", [ulp_manger_address, amount])

    # swap
    def approve_token_to_router(self, token_address, amount):
        instance = ContractInstance(self.config, 'Token', token_address)
        ulp_manger_address = get_contract_address("Router", self.config.chain_name)
        return instance.create_transaction("approve", [ulp_manger_address, amount])

    def token_balance(self, token_address, *user_address):
        instance = ContractInstance(self.config, 'Token', token_address)
        return instance.call_function("balanceOf", user_address)

    def token_decimals(self, token_address, *user_address):
        instance = ContractInstance(self.config, 'Token', token_address)
        return instance.call_function("decimals", user_address)

    def token_name(self, token_address, *user_address):
        instance = ContractInstance(self.config, 'Token', token_address)
        return instance.call_function("name", user_address)
    # position
    def approve_plugin_position_router(self):
        instance = ContractInstance(self.config, 'Router')
        position_router_address = get_contract_address("PositionRouter", self.config.chain_name)
        return instance.create_transaction("approvePlugin", [position_router_address])

    # order
    def approve_plugin_order_book(self):
        instance = ContractInstance(self.config, 'Router')
        order_book_address = get_contract_address("OrderBook", self.config.chain_name)
        return instance.create_transaction("approvePlugin", [order_book_address])

    def check_tx_confirmed(self, tx_hash):
        receipt = self.web3.eth.get_transaction_receipt(tx_hash)
        if receipt is not None:
            if receipt.status == 1:
                self.logger.info(f"transaction {tx_hash} successful")
                return True
            else:
                self.logger.error(f"transaction {tx_hash} failed")
                return False

        self.logger.error(f"transaction {tx_hash} not confirmed")
        return False

    def wait_tx_confirmed(self, tx_hash, timeout=60, polling_interval=1):
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                receipt = self.web3.eth.get_transaction_receipt(tx_hash)
                if receipt is not None:
                    if receipt.status == 1:
                        self.logger.info(f"transaction {tx_hash} successful")
                        return True
                    else:
                        self.logger.error(f"transaction {tx_hash} failed")
                        return False
            except Exception as e:
                self.logger.debug(f"checking... {e}")

            time.sleep(polling_interval)

        self.logger.error(f"transaction {tx_hash} not confirmed in {timeout}s")
        return False
