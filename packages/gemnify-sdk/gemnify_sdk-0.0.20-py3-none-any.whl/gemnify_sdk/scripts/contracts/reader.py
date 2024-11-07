from gemnify_sdk.scripts.instance import ContractInstance
from gemnify_sdk.scripts.http import HTTP
import time

class Reader:
    def __init__(self, config) -> None:
        self.config = config
        self.reader = ContractInstance(config, 'Reader')
        self.vault = ContractInstance(config, 'Vault')
        self.price_record = ContractInstance(config, 'PriceRecord')

    def get_aum(self):
        return self.reader.call_function("getAum")

    def get_global_OI(self):
        result = self.reader.call_function("getGlobalOI")
        if isinstance(result, list) and len(result) == 2:
            keys = [
                "max_global_OI",
                "available_global_OI"
            ]
            return dict(zip(keys, result))
        else:
            raise ValueError("Unexpected result format or length")

    def get_pool_info(self, *args):
        result = self.vault.call_function("getPoolInfo", args)
        if isinstance(result, tuple) and len(result) == 8:
            keys = [
                "pool_amount",
                "reserved_amount",
                "buffer_amount",
                "global_long_size",
                "global_long_average_price",
                "global_short_size",
                "global_short_average_price",
                "usdg_amount"
            ]
            return dict(zip(keys, result))
        else:
            raise ValueError("Unexpected result format or length")

    def get_max_price(self, *args):
        return self.vault.call_function("getMaxPrice", args)

    def get_min_price(self, *args):
        return self.vault.call_function("getMinPrice", args)

    def get_position(self, *args):
        instance = ContractInstance(self.config, 'Vault')
        result = instance.call_function("getPosition", args)
        if isinstance(result, tuple) and len(result) == 9:
            keys = [
                "size",
                "collateral",
                "average_price",
                "entry_borrowing_rate",
                "funding_fee_amount_per_size",
                "claimable_funding_amount_per_size",
                "reserve_amount",
                "realised_pnl",
                "last_increased_time"
            ]
            return dict(zip(keys, result))
        else:
            raise ValueError("Unexpected result format or length")

    def get_positions(self, account, market = "", status = 20000, page_index = 1, page_size = 10):
        http = HTTP(self.config)
        positions = http.post(
            "getPositionsByAccount",
            payload={
                'account': account,
                'status': status,
                "market": market,
                'pageIndex': page_index,
                'pageSize': page_size
            }
        )
        return positions

    def get_position_pnl_and_fees(self, *args):
        position = self.get_position(*args)
        position_size = position["size"]
        collateral = position["collateral"]
        if position_size > 0:
            result = self.vault.call_function("getPositionDeltaAndFees", args)
            has_profit = result[0]
            delta = int(result[1])
            borrowing_fee = int(result[2])
            funding_fee_amount = int(result[3])
            claimable_amount = int(result[4])
            close_position_fee = position_size * 0.0001
            pnl = delta if has_profit else delta * -1
            pnl_after_fee = pnl - borrowing_fee - funding_fee_amount - close_position_fee

            pnl_percent = pnl / int(collateral)
            pnl_after_fee_percent = pnl_after_fee / int(collateral)
            return {
                "pnl": round(divide(pnl, 30), 4),
                "pnl_percent": pnl_percent,
                "pnl_after_fee": round(divide(pnl_after_fee, 30), 4),
                "pnl_after_fee_percent": pnl_after_fee_percent,
                "borrowing_fee": round(divide(borrowing_fee, 30), 4),
                "close_position_fee": round(divide(close_position_fee, 30), 4),
                "negative_funding_fee": round(divide(funding_fee_amount, 30), 4),
                "positive_funding_fee": round(divide(claimable_amount, 30), 4)
            }

        return None

def divide(number, power):
    result = number / (10 ** power)
    return result
