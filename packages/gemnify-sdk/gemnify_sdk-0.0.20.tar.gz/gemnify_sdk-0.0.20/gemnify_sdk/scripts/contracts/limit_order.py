from gemnify_sdk.scripts.instance import ContractInstance
from gemnify_sdk.scripts.contracts.order import Order
from gemnify_sdk.scripts.utils import zero_address

class LimitOrder(Order):
    def __init__(self, config) -> None:
        super().__init__(config)
        self.config = config
        self.instance = ContractInstance(config, 'OrderBook')

    def create_increase_order(self, *args, value):
        return self.instance.create_transaction("createIncreaseOrder", args, value)

    def update_increase_order(self, *args):
        return self.instance.create_transaction("updateIncreaseOrder", args)

    def cancel_increase_order(self, *args):
        return self.instance.create_transaction("cancelIncreaseOrder", args)

    def create_decrease_order(self, *args, value):
        return self.instance.create_transaction("createDecreaseOrder", args, value)

    def update_decrease_order(self, *args):
        return self.instance.create_transaction("updateDecreaseOrder", args)

    def cancel_decrease_order(self, *args):
        return self.instance.create_transaction("cancelDecreaseOrder", args)

    def cancel_multiple(self, *args):
        return self.instance.create_transaction("cancelMultiple", args)

    def get_min_execution_fee(self):
        return self.instance.call_function("minExecutionFee")

    def get_latest_order_index(self, address, is_increase):
        if is_increase:
            index = self.instance.call_function("increaseOrdersIndex", [address])
        else:
            index = self.instance.call_function("decreaseOrdersIndex", [address])
        return index - 1

    def get_order_info(self, address, index, is_increase):
        if is_increase:
            increase_order = self.instance.call_function("getIncreaseOrder", [address, index])
            if isinstance(increase_order, list) and len(increase_order) == 9:
                keys = [
                    "token",
                    "token_amount",
                    "collateral_token",
                    "index_token",
                    "size_delta",
                    "is_long",
                    "trigger_price",
                    "trigger_above_threshold",
                    "execution_fee"
                ]
                return dict(zip(keys, increase_order))
            else:
                return None
        else:
            decrease_order = self.instance.call_function("getDecreaseOrder", [address, index])
            if isinstance(decrease_order, list) and len(decrease_order) == 8:
                keys = [
                    "collateral_token",
                    "collateral_delta",
                    "index_token",
                    "size_delta",
                    "is_long",
                    "trigger_price",
                    "trigger_above_threshold",
                    "execution_fee"
                ]
                return dict(zip(keys, decrease_order))
            else:
                return None

    def check_order_executed(self, address, index, is_increase):
        order_info = self.get_order_info(address, index, is_increase)
        if order_info["index_token"] == zero_address and order_info["size_delta"] == 0:
            return True
        return False