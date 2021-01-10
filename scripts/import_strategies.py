import urllib.request
import os

dirname = "imported_strategies"
if not os.path.exists(dirname):
    os.makedirs(dirname)

to_fetch = [
    ("https://raw.githubusercontent.com/C0BBL3/space-empires/master/src/strategies/basic_strategy.py",
     "basic_strategy.py"),
    ("https://raw.githubusercontent.com/C0BBL3/space-empires/master/src/strategies/combat_strategy.py",
     "colby_combat_strategy.py"),
    ("https://raw.githubusercontent.com/C0BBL3/space-empires/master/src/strategies/dumb_strategy.py",
     "colby_dumb_strategy.py"),
    ("https://raw.githubusercontent.com/RileyPaddock/space-empires/master/src/strategies/combat_strategy.py",
     "riley_combat_strategy.py"),
    ("https://raw.githubusercontent.com/RileyPaddock/space-empires/master/src/strategies/dumb_strategy.py",
     "riley_dumb_strategy.py"),
    ("https://raw.githubusercontent.com/geomeza/space-empires/master/src/strategies/combat_strategy.py",
     "george_combat_strategy.py"),
    ("https://raw.githubusercontent.com/geomeza/space-empires/master/src/strategies/dumb_strategy.py",
     "george_dumb_strategy.py"),
    ("https://raw.githubusercontent.com/DrM00G/space-game/master/src/strategies/combat_strategy.py",
     "david_combat_strategy.py"),
    ("https://raw.githubusercontent.com/DrM00G/space-game/master/src/strategies/dumb_strategy.py",
     "david_dumb_strategy.py"),
    ("https://raw.githubusercontent.com/eoriont/space-empires/master/src/strategies/dumb_strategy.py",
     "elijah_dumb_strategy.py"),
    ("https://raw.githubusercontent.com/eoriont/space-empires/master/src/strategies/combat_strategy.py",
     "elijah_combat_strategy.py"),
    ("https://raw.githubusercontent.com/eoriont/space-empires/master/src/strategies/strategy_util.py", "strategy_util.py")
]

# basic_strategy.py is part of Colby's strategies

# strategy_util.py is used by Elijah's strategies

for url, file_name in to_fetch:
    with urllib.request.urlopen(url) as response:
        content = response.read()
        with open(os.path.join(dirname, file_name), "wb") as text_file:
            text_file.write(content)
