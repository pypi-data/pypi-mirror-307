from gemnify_sdk.scripts.contracts import order, limit_order, market_order, liquidity, swap, util, fee, reader

class Gemnify:
    def __init__(self, config):
        self.config = config

    def fee(self):
        return fee.Fee(self.config)

    def liquidity(self):
        return liquidity.Liquidity(self.config)

    def limit_order(self):
        return limit_order.LimitOrder(self.config)

    def market_order(self):
        return market_order.MarketOrder(self.config)

    def order(self):
        return order.Order(self.config)

    def swap(self):
        return swap.Swap(self.config)

    def util(self):
        return util.Util(self.config)

    def reader(self):
        return reader.Reader(self.config)