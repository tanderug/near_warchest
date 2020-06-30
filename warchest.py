import os
import subprocess
import sys
import time

import requests
import logging

from const import stake_pool_id, network, accound_id, seat_price_percentage, lower_bid_threshold, \
    upper_bid_threshold

""""
We're using near to figure out how we need to adapt
our current stake to keep exactly one validator slot
"""

logging.basicConfig(level=logging.INFO)

# Required to export the correct network
env = dict(os.environ)
env["NODE_ENV"] = network


def run():
    are_we_validator()
    next_slot_price = get_next_slot_price()
    my_bid = get_current_bid()
    adapt_stake(my_bid, next_slot_price)


def are_we_validator():
    response = requests.post(f"https://rpc.{network}.near.org",
                             json={"jsonrpc": "2.0", "method": "status", "id": stake_pool_id},
                             params='[]'
                             ).json()
    for validator in response["result"]["validators"]:
        if stake_pool_id == validator["account_id"]:
            logging.info(f"{stake_pool_id} is currently a validator")
            return
        else:
            continue
    logging.error(f"{stake_pool_id} is currently not a validator")


def get_next_slot_price():
    try:
        validator_output = subprocess.check_output(
            ["near", "proposals"],
            env=env
        ).decode('UTF-8')
    except Exception as e:
        logging.error("Getting the next slot price failed:")
        logging.error(e)
        # FIXME notify the user that something went wrong
        sys.exit()
    next_slot_price_string = validator_output.split("seat price = ")[1].split(")")[0]
    # Make sure slot price is in the correct format and in the unit of yocto near
    next_slot_price = int(next_slot_price_string.replace(",", ""))*10**24
    logging.info(f"The next slotprice will most likely be {next_slot_price} yocto nears")
    return next_slot_price


def get_current_bid():
    try:
        locked = subprocess.check_output(
            [f"near proposals | grep {stake_pool_id}"],
            shell=True,
            env=env
        ).decode('UTF-8')
    except Exception as e:
        logging.error("Getting the next slot price failed:")
        logging.error(e)
        # FIXME notify the user that something went wrong
        sys.exit()
    locked_amount = int(locked.split("|")[3].replace(",", "").replace(" ", ""))*10**24
    logging.info(f"{stake_pool_id} has currently {locked_amount} bid in auction")
    return locked_amount


def adapt_stake(my_bid, next_slot_price):
    # Decrease bid if our current bid is more than 180% of the estimated seat price
    if my_bid > next_slot_price * upper_bid_threshold:
        reduce_stake(my_bid, next_slot_price)
    # Increase bid if our current bid is less than 110% of the estimated seat price
    elif my_bid < next_slot_price * lower_bid_threshold:
        increase_stake(my_bid, next_slot_price)
    # Otherwise do nothing
    else:
        logging.info("The current bid is fine")


def reduce_stake(my_stake, next_slot_price):
    # Unstake funds so that we have 130% seat price staked
    # FIXME this can/should be adapted depending on your strategy
    amount_to_unstake = int(my_stake - (next_slot_price * seat_price_percentage))
    try:
        subprocess.check_output(
            [f'near call {stake_pool_id} unstake \'{{"amount": "{amount_to_unstake}"}}\' --accountId {accound_id}'],
            env=env,
            shell=True
        ).decode('UTF-8')
    except Exception as e:
        logging.error("Unstaking the currently staked Funds failed!")
        logging.error(e)
        # FIXME notify the user that something went wrong
        sys.exit()


def increase_stake(my_stake, next_slot_price):
    # Stake additional funds so that we have 130% seat price staked
    # FIXME this can/should be
    amount_to_stake = int((next_slot_price * seat_price_percentage) - my_stake)
    try:
        subprocess.check_output(
            [f'near call {stake_pool_id} stake \'{{"amount": "{amount_to_stake}"}}\' --accountId {accound_id}'],
            env=env,
            shell=True
        ).decode('UTF-8')
    except Exception as e:
        logging.error("Staking the Funds failed!")
        logging.error(e)
        # FIXME notify the user that something went wrong
        sys.exit()
    logging.info(f"Successfully staked {amount_to_stake}")


def wait_until_close_to_next_epoch():
    logging.info("Waiting for 10 minutes")
    time.sleep(10*60)


if __name__ == "__main__":
    logging.info("Started Warchest bot")
    # Run in infinite loop
    while True:
        # Start main logic
        run()
        # Wait for some time
        # FIXME ideally the bot should wait until a couple of block before the end of an epoch
        #  to avoid getting overbid by other bots before the bidding period ends
        wait_until_close_to_next_epoch()
