from gemnify_sdk.scripts.http import HTTP
import time

class Order:
    def __init__(self, config) -> None:
        self.config = config

    def get_order_by_hash(self, tx_hash):
        http = HTTP(self.config)
        return http.post(
            "getOrderByTx",
            payload={
                'tx': tx_hash
            }
        )

    def get_order_index_by_hash(self, tx_hash):
        order = self.get_order_by_hash(tx_hash)
        if not order:
            return None
        else:
            order = self.get_order_by_hash(tx_hash)
            if order:
                return order["order_index"]

    def get_order_status(self, tx_hash):
        order = self.get_order_by_hash(tx_hash)
        if not order:
            return None
        else:
            switch = {
                10000: "OrderReceived",
                10001: "OrderWaitingBlockConfirm",
                10002: "OrderConfirmed",
                10011: "OrderCanceledByKeeper",
                10012: "OrderCanceledByUser",
                10013: "OrderCanceledByContract"
            }
            return switch.get(order["status"], str(order["status"]))

    def wait_order_received(self, tx_hash, timeout=60, polling_interval=1):
        start_time = time.time()
        while time.time() - start_time < timeout:
            order = self.get_order_by_hash(tx_hash)
            if order:
                return True
            time.sleep(polling_interval)

        return False

    def wait_order_confirmed(self, tx_hash, timeout=60, polling_interval=1):
        start_time = time.time()
        while time.time() - start_time < timeout:
            order = self.get_order_by_hash(tx_hash)
            if order and order["status"] == 10002:
                return True
            time.sleep(polling_interval)

        return False

    def get_orders_by_account(self, account, status=10000, market='', pageIndex=1, pageSize=10):
        http = HTTP(self.config)
        return http.post(
            "getOrdersByAccount",
            payload={
                'account': account,
                'status': status,
                'market': market,
                "pageIndex": pageIndex,
                'pageSize': pageSize
            }
        )
