# Gemnify SDK Python
A python based SDK developed for interacting with Gemnify

# Pip Install

The SDK can be installed via pip:

`pip install gemnify-sdk`

# Requirements
Developed using:

`python>=3.11.9`

# Example Scripts
There are several example scripts which can be run and can be found in [example scripts](https://github.com/GMX-For-NFT/gemnify-sdk-python/tree/main/example_scripts). These are mostly for demonstration purposes on how to utilise the SDK, and can should be incoporated into your own scripts and strategies.



# General Usage


## Config

need to configure the following items:
1. node rpc

```python
config.set_node_rpc("https://sepolia-rollup.arbitrum.io/rpc")
```
2. user's private key
```python
config.set_private_key("")
```
3. log level, can be set to `fatal`, `error`, `warn`, `info`, `debug`, default is `fatal`
```python
config.set_logger_level("info")
```
4. log file path, must absolute path. if not set, log will be printed on the console, and if set, log will be output to a file
```python
config.set_logger_file_path("/Users/Gemnify/Documents")
```

## Mock Token

now contract has been deployed on arbitrum sepolia, and mock stable coins are 
```
  "usdt": "0xeF0339A533E68f920444a3BB576669871Ce54c29",
  "usdc": "0x2f2F7Aa330Ef17019A9cB086da0970470fFe5a8c",
  "usde": "0x3c3ac50dc87d549609a238E287666C82E4bCBA6F",
  "fdusd": "0xc8E2ace39233FA977c7F388f31b4f232DAc647A2",
  "dai": "0x254b40Ce47F7DA1867e594613D08a23E198d7FE7"
```

if you want to get the test token, can directly mint on the testnet explorer
, or use the [example](https://github.com/GMX-For-NFT/gemnify-sdk-python/blob/main/example_scripts/liquidity.py#L19)
```python
util.mint_token(usdc_address, amount, receiver)
```

## Liquidity
[example](https://github.com/GMX-For-NFT/gemnify-sdk-python/blob/main/example_scripts/liquidity.py)
### Add Liquidity
```python
liquidity.add_liquidity(
    token, 
    amount,
    min_usdg,
    min_ulp  
)
```

- `token`  type str, token address, eg: dai address
- `amount` type int, token amount to deposit
- `min_usdg` type int, minimum acceptable USDG value of the ULP purchased
- `min_ulp` type int, minimum acceptable ULP amount

before add liquidity, should approve token to `UlpManager` first

```python
util.approve_token_to_ulp_manager(token_address, amount)
```

### Remove Liquidity
```python
liquidity.remove_liquidity(
    ulp_amount,  
    min_out,      
    receiver,  
)
```
- `ulp_amount`  type int, the amount of ULP to remove, decimal is 18
- `min_out`  type int, the minimum acceptable amount of tokens to be received
- `receiver`  type str, the address to receive tokens



### Get Amount When Add Liquidity
when add liquidity, user need to deposit token and can receive ulp token
```python
tokens_amount = liquidity.get_amount_when_add_liquidity(
    token,
    amount,
    out
)
```

- `token` token address to deposit, eg dai address
- if `out` is true, `amount` is amount of token to deposit, and return is the amount of ULP that user can received
- if `out` is false, `amount` is amount of ulp that user want to receive, and return is the amount of token that need to deposit


### Get Amount When Remove Liquidity
when remove liquidity, users can receive all tokens of the stable tokens proportionally， this interface returns the amount of each token
```python
tokens_amount = liquidity.get_tokens_amount_out_when_remove_liquidity(
    ulp_amount
)
```
return is a `dict` and can format output as:
```python
print(json.dumps(tokens_amount, indent=4))

[
    {
        "token": "0xeF0339A533E68f920444a3BB576669871Ce54c29",
        "amountOut": 220317890964816501,
        "amountOutFormatPrecision": 220317890964816501
    },
    {
        "token": "0x3c3ac50dc87d549609a238E287666C82E4bCBA6F",
        "amountOut": 100399169213540645,
        "amountOutFormatPrecision": 100399169213540645
    }
]

```


### Get Claimable Reward
get claimable reward usdc
```python
liquidity.get_claimable(user)
```

### Claim Reward
claim reward usdc
```python
liquidity.handleRewards()
```

### Get User ULP
get deposited ULP of specific user
```python
liquidity.get_user_ulp(
    user,
    ulp_address
)
```
- `user` user address
- `ulp_address`, ulp address, can get from `util.get_token_address("ulp")`

return:
- ulp amount, decimal is 18

### Get Total ULP
get total deposited ULP
```python
liquidity.get_total_ulp(
    ulp_address
)
```
- `ulp_address` ulp address, can get from `util.get_token_address("ulp")`

return:
- ulp amount, decimal is 18

## Market Order
[example](https://github.com/GMX-For-NFT/gemnify-sdk-python/blob/main/example_scripts/market_order.py)

### Increase Long or Short Position
user's request to open a position
```python
market_order.create_increase_position(
    index_token,
    amount_in,
    size_delta,
    is_long,
    acceptable_price,
    execution_fee,
    callback_target
    value = val,
) 
```
- `index_token` type str, the address of token you want to long or short, eg, dai address
- `amount_in` type int, the amount of token you want to deposit as collateral
- `size_delta` type int, the USD value of the change in position size, decimal is 30
- `is_long` type bool, is position long or short? (long->true,short->false)
- `acceptable_price` type int, the price acceptable when executing the request, decimal is 30. (if long, > `reader.get_max_price`, if short, < `reader.get_min_price`)
- `execution_fee` type int,  execution_fee >= `market_order.get_min_execution_fee`, setting on arbitrum sepolia is 0.0001 eth
- `callback_target` type string, an optional callback contract, this contract will be called on request execution or cancellation
- `value` type int, = execution_fee

before call `create_increase_position`, should:
1. approve plugin, it only needs to be called once the first time to open position, and does not need to be done again afterward
```python
util.approve_plugin_position_router()
```
2. approve usdc to router,
```python
util.approve_token_to_router(
    usdc_address, 
    amount
)
```

### Decrease Long or Short Position
user's request to decrease a position
```python
market_order.create_decrease_position(
    index_token,
    collateral_delta,
    size_delta,
    is_long,
    receiver,
    acceptable_price,
    execution_fee,
    callback_target,
    value = val
) 
```

- `index_token`  type str, the address of token you want to long or short
- `collateral_delta` type int, the amount of collateral in USD value to withdraw, if decrease max position, set 0. decimal is 30
- `size_delta` type int, the USD value of the change in position size, decimal is 30
- `is_long` type bool, is position long or short?(long->true,short->false)
- `receiver` type str, the address that receive the token after decrease the position 
- `acceptable_price` type int, the price acceptable when executing the request, decimal is 30. (if long, < `reader.get_min_price`, if short, > `reader.get_max_price`)
- `execution_fee` type int, execution_fee >= `market_order.get_min_execution_fee`
- `callback_target`type str
- `value` type int,  = execution_fee


### Add Collateral

use `market_order.create_increase_position`, and set size_delta to 0

### Remove Collateral

use `market_order.create_decrease_position`, and set size_delta to 0

### Get Latest Order Index
```python
order_index = market_order.get_latest_order_index(address, is_increase)
```
- `address`  type str, 
- `is_increase`  type bool, 

### Check Order Executed
```python
order_index = market_order.check_order_executed(address, order_index, is_increase)
```
- `address`  type str, 
- `order_index`  type int, 
- `is_increase`  type bool,


so, how to check if market order has been executed?

first, get tx hash
```python
tx_hash = market_order.create_increase_position()
```
then, check tx status
```python
tx_status = util.wait_tx_confirmed(tx_hash)
```
if `tx_status` is true, get user's latest order index
```python
order_index = market_order.get_latest_order_index()
```
then, check if order executed
```python
order_executed = market_order.check_order_executed()
```
this function can be called by polling to check the order status.

- if `order_executed` is false, means order has not been executed.
- if `order_executed` is true, means order has been executed. but if want to know if the order was executed successfully or failed, need to check the position changes

## Limit Order
[example](https://github.com/GMX-For-NFT/gemnify-sdk-python/blob/main/example_scripts/limit_order.py)

### Create Increase Order

```python
limit_order.create_increase_order(
    amount_in,
    index_token,
    size_delta,
    collateral_token,
    is_long,
    trigger_price,
    trigger_above_threshold,
    execution_fee,
    value=val
)
```
- `amount_in` type int, the amount of token you want to deposit as collateral
- `index_token` type str, the address of token you want to long or short
- `size_delta` type int, the USD value of the change in position size, decimal is 30
- `collateral_token` type str, usdc address
- `is_long` type bool, is position long or short?(long->true,short->false)
- `trigger_price` type int, the trigger price for the position, decimal is 30 
- `trigger_above_threshold` type bool, when executing order if need market price < trigger_price, set false or if need market price > _trigger_price, set true
- `execution_fee`, type int,   >= `limit_order.get_min_execution_fee`
- `value` type int,  = execution_fee

`trigger_price`/`trigger_above_threshold` should be set as:
- if position is long:
    - is_long: true
    - trigger_price: < current market price
    - triggerAboveThreshold: false
- if position is short:
    - is_long: false
    - trigger_price: > current market price
    - triggerAboveThreshold: true
  

before call `create_increase_order`, should:
1. approve plugin, it only needs to be called once the first time to create order, and does not need to be done again afterward
```python
util.approve_plugin_order_book()
```
2. approve usdc to router,
```python
util.approve_token_to_router(
    usdc_address, # usdc
    amount
)
```

### Create Decrease Order
```python
limit_order.create_decrease_order(
    index_token,
    size_delta,
    collateral_token,
    collateral_delta,
    is_long,
    trigger_price,
    trigger_above_threshold,
    value=val
) 
```

- `index_token` type str, the address of token you want to long or short
- `size_delta` type int, the USD value of the change in position size, decimal is 30
- `collateral_token` type str, usdc address
- `collateral_delta` type int, the amount of collateral in USD value to withdraw, decimal is 30, if close max position, set 0
- `is_long` type bool, is position long or short?(long->true,short->false)
- `trigger_price` type int, the trigger price for the position, decimal is 30 
- `trigger_above_threshold` type int
- `value` type int, >= `limit_order.get_min_execution_fee`

`trigger_price`/`trigger_above_threshold` should be set as:

- if position is long:
  - TP(take profit):
    - is_long: true
    - trigger_price: > current market price
    - triggerAboveThreshold: true 
  - SL(stop loss):
    - is_long: true 
    - trigger_price: < current market price
    - trigger_above_threshold: false 
- if position is short:
  - TP:
    - is_long: false 
    - trigger_price: < current market price
    - trigger_above_threshold: false 
  - SL:
    - is_long: false
    - trigger_price: > current market price 
    - trigger_above_threshold: true



### Update Increase Order

```python
limit_order.update_increase_order(
    order_index,
    size_delta,
    trigger_price,
    trigger_above_threshold
)
```

- `order_index` type int, the index of the order
- `size_delta` type int, size of order after update
- `trigger_price` type int, the trigger price after update
- `trigger_above_threshold` type bool, trigger_above_threshold after update

### Update Decrease Order
```python
limit_order.update_decrease_order(
   order_index,
   collateral_delta,
   size_delta,
   trigger_price,
   trigger_above_threshold
) 
```

- `order_index` type int, the index of the order
- `collateral_delta` type int, size of position after update
- `size_delta` type int, size of order after update
- `trigger_price` type int, the trigger price after update
- `trigger_above_threshold` type bool trigger_above_threshold after update



### Cancel Increase Order

```python
limit_order.cancel_increase_order(
    order_index
)
```
- `order_index` type int, the index of the order

### Cancel Decrease Order

```python
limit_order.cancel_decrease_order(
    order_index 
)
```

- `order_index` the index of the order

### Cancel Multiple Order
cancel multiple order
```python
limit_order.cancel_multiple(
    swap_order_indexes,
    increase_order_indexes,
    decrease_order_indexes
) 
```

- `swap_order_indexes`  the index array of swap order 
- `increase_order_indexes` the index array of increase order 
- `decrease_order_indexes` the index array of decrease order



### Get Latest Order Index
```python
order_index = limit_order.get_latest_order_index(address, is_increase)
```
- `address`  type str, 
- `is_increase`  type bool, 


### Check Order Executed
```python
order_index = limit_order.check_order_executed(address, order_index, is_increase)
```
- `address`  type str, 
- `order_index`  type int, 
- `is_increase`  type bool,


so, how to check if limit order has been executed?

first, get tx hash
```python
tx_hash = limit_order.create_increase_order()
```
then, check tx status
```python
tx_status = util.wait_tx_confirmed(tx_hash)
```
if `tx_status` is true, get user's latest order index
```python
order_index = limit_order.get_latest_order_index()
```
then, check if order executed
```python
order_executed = limit_order.check_order_executed()
```
this function can be called by polling to check the order status.

- if `order_executed` is false, means order has not been executed.
- if `order_executed` is true, means order has been executed. but if want to know if the order was executed successfully or failed, need to check the position changes

## Swap
[example](https://github.com/GMX-For-NFT/gemnify-sdk-python/blob/main/example_scripts/swap.py)

```python
swap.swap(
    path,
    amount_in,
    min_out,
    receiver
)
```

- `path` type array, if swap A to B, _path is [A, B]
- `amount_in` type int, amount of token in to swap
- `min_out` type int, min amount of token out
- `receiver` type str

before swap, should approve to router first
```python
util.approve_token_to_router(token_address, amount)
```

## Fee
[example](https://github.com/GMX-For-NFT/gemnify-sdk-python/blob/main/example_scripts/fee.py)

### Claim Funding Fee
claim funding fee
```python 
fee.claim_funding_fees()
```

### Get Funding Fee
get funding fee
```python
fee.get_funding_fee_amount(user_address)
```

### Get Deposit  Fee
 get deposit fee basis point 
```python
deposit_fee = fee.get_deposit_fee_basis_points(
   token_address,
   amount
)
```
- `token_address`  token to deposit
- `amount_in`  amount of token to deposit

return is a `dict`:
- the first value is basic point of deposit fee, denominator is 10000
- the second value is balance reward

```python
print(json.dumps(deposit_fee, indent=4))

{
    "fee": 8,
    "balanceReward": 100
}
```


### Get Withdraw  Fee

```python
fee.get_withdraw_fee_basis_points(
  ulp_address,
  amount
)
```
- `ulp_address`  ulp address
- `amount`  amount of ulp to withdraw

return:
- basic point of withdraw fee, denominator is 10000  



### Get Swap Fee

```python
swap_fee = fee.get_swap_fee_basis_points(
    token_in,
    token_out,
    token_amount
)
```

return is a `dict`:
- the first value is basic point of swap fee, denominator is 10000
- the second value is balance reward

```python
print(json.dumps(swap_fee, indent=4))

{
    "fee": 8,
    "balanceReward": 100
}
```

### Get Borrowing Rates

```python
fee.get_borrowing_rates(
    token
)
```
- `token`, only usdc address

## Reader

[example](https://github.com/GMX-For-NFT/gemnify-sdk-python/blob/main/example_scripts/reader.py)


### Get Position

```python
user_position = reader.get_position(
    user_address,
    collateral_token,
    index_token,
    is_long
)
```
- `user_address` type str
- `collateral_token` type str, usdc address
- `index_token`, type str, the address of token has been long or short
- `is_long` type bool

return is a `dict`:
```python
print(json.dumps(user_position, indent=4))

{
    "size": 4000000000000000000000000000000000,
    "collateral": 64356959836112582840576038015910,
    "average_price": 999941021133670046267807594895,
    "entry_borrowing_rate": 16125,
    "funding_fee_amount_per_size": 34293929831927222356296728313000,
    "claimable_funding_amount_per_size": 335816860153201919014462145430,
    "reserve_amount": 200000000000000000000,
    "realised_pnl": -14087681835359073095730203677,
    "last_increased_time": 1720434112
}

```

### Get Pnl
```python
result = reader.get_position_pnl_and_fees(
    user_address,
    collateral_token,
    index_token,
    is_long  
)
```
- `user_address` type str
- `collateral_token` type str, usdc address
- `index_token`, type str, the address of token has been long or short
- `is_long` type bool

```python
print(json.dumps(result, indent=4))

{
    "pnl": 297.6012,
    "pnl_percent": 0.06904959436095,
    "pnl_after_fee": 289.0028,
    "pnl_after_fee_percent": 0.067716254529,
    "borrowing_fee": 0.396,
    "accr_negative_funding_fee": 7.2122,
    "accr_positive_funding_fee": 0.9666,
    "close_position_fee": 0.9901
}
```
- pnl: profit generated of the position due to price change
- pnl_after_fee: actual profit that user can receive by closing the position at this time
- pnl_percent = pnl / collateral
- pnl_after_fee = pnl - borrowing_fee - accr_negative_funding_fee - close_position_fee
- pnl_after_fee_percent = pnl_after_fee / collateral

### Get Global OI
get global OI
```python
oi = reader.get_global_OI()
```

return is a `dict`:

```python
print(json.dumps(oi, indent=4))

{
    "max_global_OI": 16527266546217310778227256594002320840,
    "available_global_OI": 16240882881752412827331256594002320840
}
```
decimals is 30

### Get Aum
```python
reader.get_aum()
```

### Get Pool Info
```python
pool_info = reader.get_pool_info(
    token_address
)
```

return is a `dict`:

```python
print(json.dumps(pool_info, indent=4))

{
    "pool_amount": 184124301083056626443184,
    "reserved_amount": 0,
    "buffer_amount": 0,
    "global_long_size": 59366183546917035140000000000000000,
    "global_long_average_price": 980888313409868535168969222751,
    "global_short_size": 230781533693570940000000000000000,
    "global_short_average_price": 999378242704742748391145661272,
    "usdg_amount": 184095747307695844794481
}

```

### Get Min Price
```python
reader.get_min_price(
    token_address
)
```

### Get Max Price
```python
reader.get_max_price(
    token_address
)
```
