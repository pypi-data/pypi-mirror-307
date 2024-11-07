from gemnify_sdk.scripts.instance import ContractInstance

class Fee:
    def __init__(self, config) -> None:
        self.config = config
        self.reader = ContractInstance(config, 'Reader')
        self.vault = ContractInstance(config, 'Vault')

    def claim_funding_fees(self):
        return self.vault.create_transaction("claimFundingFees")

    def get_funding_fee_amount(self, *args):
        return self.vault.call_function("getFundingFeeAmount", args)

    def get_deposit_fee_basis_points(self, *args):
        result = self.reader.call_function("getDepositFeeBasisPoints", args)
        if isinstance(result, list) and len(result) == 2:
            keys = [
                "fee",
                "balanceReward"
            ]
            return dict(zip(keys, result))
        else:
            raise ValueError("Unexpected result format or length")

    def get_withdraw_fee_basis_points(self, *args):
        return self.reader.call_function("getWithdrawFeeBasisPoints", args)

    def get_swap_fee_basis_points(self, *args):
        result = self.reader.call_function("getSwapFeeBasisPoints", args)
        if isinstance(result, list) and len(result) == 2:
            keys = [
                "fee",
                "balanceReward"
            ]
            return dict(zip(keys, result))
        else:
            raise ValueError("Unexpected result format or length")

    def get_borrowing_rates(self, *args):
        return self.reader.call_function("getBorrowingRates", args)


