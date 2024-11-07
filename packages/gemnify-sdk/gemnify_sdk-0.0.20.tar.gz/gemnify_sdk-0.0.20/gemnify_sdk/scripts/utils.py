import json
import os
from decimal import Decimal
from eth_account import Account

default_chain = "arbitrum-sepolia"

zero_address = "0x0000000000000000000000000000000000000000"

# Get the absolute path of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))

def get_contract_abi(contract_name):
    contract_abis_dir = os.path.join(base_dir, "..", "contracts", "abis")
    abi_file = os.path.join(contract_abis_dir, contract_name + ".json")
    return json.load(
        open(
            abi_file
        )
    )

def get_contract_address(contract_name, chain):
    contract_addresses_dir = os.path.join(base_dir, "..", "contracts", "addresses")
    addresses_file = os.path.join(contract_addresses_dir, chain + ".json")
    with open(addresses_file, 'r') as f:
        addresses_json = json.load(f)
        return addresses_json[contract_name]

def expand_number(number, decimals):
    multiplier = 10 ** decimals
    result = number * multiplier
    uint256_max_value = 2 ** 256 - 1
    if result > uint256_max_value:
        raise OverflowError("Result exceeds uint256 maximum value")
    return int(result)

def get_address_from_private_key(private_key):
    account = Account.from_key(private_key)
    address = account.address
    return address

def get_token_address(token_name, chain = default_chain):
    return get_contract_address(token_name.lower(), chain)