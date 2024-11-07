from gemnify_sdk.scripts.instance import ContractInstance

class Liquidity:
    def __init__(self, config) -> None:
        self.config = config
        self.instance = ContractInstance(config, 'RewardRouter')

    def add_liquidity(self, *args):
        return self.instance.create_transaction("mintAndStakeUlp", args)

    def remove_liquidity(self, *args):
        return self.instance.create_transaction("unstakeAndRedeemUlp", args)

    # def get_tokens_amount_out(self, *args):
    #     reader_instance = ContractInstance(self.config, 'Reader')
    #     value = reader_instance.call_function("getAmountOutWhenSellUlp", args)
    #     formatted_value = [
    #         {
    #             "token": token,
    #             "amountOut": amountOut,
    #             "amountOutFormatPrecision": amountOutFormatPrecision
    #         }
    #         for token, amountOut, amountOutFormatPrecision in value
    #     ]
    #     return formatted_value

    def handleRewards(self, *args):
        return self.instance.create_transaction("handleRewards", args)

    def get_claimable(self, *args):
        tracker = ContractInstance(self.config, 'RewardTracker')
        return tracker.call_function("claimable", args)

    def get_user_ulp(self, *args):
        tracker = ContractInstance(self.config, 'RewardTracker')
        return tracker.call_function("depositBalances", args)

    def get_total_ulp(self, *args):
        tracker = ContractInstance(self.config, 'RewardTracker')
        return tracker.call_function("totalDepositSupply", args)

    def get_amount_when_add_liquidity(self, *args):
        reader = ContractInstance(self.config, 'Reader')
        return reader.call_function("getAmountWhenBuyUlp", args)

    def get_tokens_amount_out_when_remove_liquidity(self, *args):
        reader_instance = ContractInstance(self.config, 'Reader')
        value = reader_instance.call_function("getAmountOutWhenSellUlp", args)
        formatted_value = [
            {
                "token": token,
                "amountOut": amountOut,
                "amountOutFormatPrecision": amountOutFormatPrecision
            }
            for token, amountOut, amountOutFormatPrecision in value
        ]
        return formatted_value