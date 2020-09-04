# The stake pool id that should be managed
stake_pool_id = "get_rich"

# Your account id with funds
# NOTE the bot requires you to already have near deposited to the stake pool
accound_id = "tanderug5.betanet"

# The network to use - Shouldn't be changed
network = "betanet"

# If we adapt our bid it will always be this percentage of the estimated seat price
# atm we bid 130% of the estimated seat price
# FIXME adapt as you like
seat_price_percentage = 1.3

# If our current bid is below this threshold we bid the `seat_price_percentage` amount
# atm we increase our bid if the current bid is below 110% of the estimated seat price
# FIXME adapt as you like
lower_bid_threshold = 1.1

# If our current bid is above this threshold we bid the `seat_price_percentage` amount
# atm we decrease our bid if the current bid is above 180% of the estimated seat price
# FIXME adapt as you like
upper_bid_threshold = 1.8
