from gemnify_sdk.scripts.instance import ContractInstance
from gemnify_sdk.scripts.contracts.order import Order
from gemnify_sdk.scripts.utils import zero_address

class MarketOrder(Order):
    def __init__(self, config) -> None:
        super().__init__(config)
        self.config = config
        self.instance = ContractInstance(config, 'PositionRouter')

    def create_increase_position(self, *args, value):
        return self.instance.create_transaction("createIncreasePosition", args, value)

    def create_decrease_position(self, *args, value):
        return self.instance.create_transaction("createDecreasePosition", args, value)

    def get_min_execution_fee(self):
        return self.instance.call_function("minExecutionFee")

    def get_latest_order_index(self, address, is_increase):
        if is_increase:
            return self.instance.call_function("increasePositionsIndex", [address])
        else:
            return self.instance.call_function("decreasePositionsIndex", [address])

    def get_order_info(self, address, index, is_increase):
        request_key = self.instance.call_function("getRequestKey", [address, index])
        if is_increase:
            return self.instance.call_function("increasePositionRequests", [request_key])
        else:
            return self.instance.call_function("decreasePositionRequests", [request_key])

    def check_order_executed(self, address, index, is_increase):
        order_info = self.get_order_info(address, index, is_increase)
        if order_info[0] == zero_address and order_info[1] == zero_address:
            return True
        return False

