# Stakewars warchest bot

The warchest is a Python script for monitoring and adapting your stake to make sure you keep exactly one validator seat

## Requirements

This bot requires:
- near-shell to be installed - If you haven't done it run `npm install -g near-shell
` or check [here](https://github.com/near/near-shell)
- python 3.6+ installed - to check run `whereis python3`
- near-shell needs to be logged in

(It's the easiest to run this bot as service on your machine that also runs the validator node) 


## Installation

```
git clone https://github.com/eorituz/near_warchest.git
```

## Usage

1. First, adapt the `const.py` file with your credentials and your preferred strategy.
2. Make the bot run as a service
   1) `nano /etc/systemd/system/warchest_bot.service`
   2. Paste 
   ```
   [Unit]
   Description=Warchest bot managing near stake
   After=network.target
   StartLimitIntervalSec=0

   [Service]
   Type=simple
   Restart=always
   RestartSec=1
   User=root
   ExecStart=/PATH/TO/python3.6 /PATH/TO/near_warchest/warchest.py

   [Install]
   WantedBy=multi-user.target
   ```
   3. To figure out the path to you python executable run `whereis python`
   4. Run `sudo systemctl start warchest_bot`
   5. Check the logs if it worked `sudo journalctl -u warchest_bot.service -f` They should look something like this 
   ```
   Jun 30 15:33:21 NearValidator systemd[1]: Started Warchest bot managing near stake.
   Jun 30 15:33:22 NearValidator python3.6[3815]: ERROR:root:stakeing.arno_nym.betanet is currently not a validator
   Jun 30 15:33:24 NearValidator python3.6[3815]: INFO:root:The next slotprice will most likely be 109830000000000000000000000000
   Jun 30 15:33:25 NearValidator python3.6[3815]: INFO:root:stakeing.arno_nym.betanet has currently 141554000000000000000000000000 bid in auction
   ```
   6. Enable the service permanently by running `systemctl start warchest_bot`

3. Check if the bot worked by manually staking more ore less than the set threshold in the `const.py` file. Please wait for at least 10 minutes as the bot only runs once every 10 minutes atm.
To see all of the bot's logs run `sudo journalctl -u warchest_bot.service -b`

## Notes

Unfortunately, the bot is quite primitive atm. Feel free to have a look at the code (it's not that complicated) and adapt/improve. The major issues atm are: 
- If the bot crashes there won't be any notification except for the logs
- Currently, the bot gets its information by calling near-shell this could lead to issues in the future. Migrating to the JSON-RPC might be a better approach
- The bot runs every 10 minutes. However, it would be way better from a game-theoretical approach if the bot would run just before an epoch ends or if the monitoring you set up in [Challange 003](https://github.com/nearprotocol/stakewars/blob/master/challenges/challenge003.md) reports something.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)