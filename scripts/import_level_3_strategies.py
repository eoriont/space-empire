import urllib.request
import os

dirname = "imported_strategies_level_3"
if not os.path.exists(dirname):
    os.makedirs(dirname)

to_fetch = [
    ("https://raw.githubusercontent.com/eurisko-us/eurisko-us.github.io/master/files/strategies/cohort-1/level-3/colby_strategy_level_3.py",
     "colby_strategy.py"),
    ("https://raw.githubusercontent.com/eurisko-us/eurisko-us.github.io/master/files/strategies/cohort-1/level-3/david_strategy_level_3.py",
     "david_strategy.py"),
    ("https://raw.githubusercontent.com/eurisko-us/eurisko-us.github.io/master/files/strategies/cohort-1/level-3/elijah_strategy_level_3.py",
     "elijah_strategy.py"),
    ("https://raw.githubusercontent.com/eurisko-us/eurisko-us.github.io/master/files/strategies/cohort-1/level-3/george_strategy_level_3.py",
     "george_strategy.py"),
    ("https://raw.githubusercontent.com/eurisko-us/eurisko-us.github.io/master/files/strategies/cohort-1/level-3/numbers_berserker_level_3.py",
     "numbers_berserker.py"),
    ("https://raw.githubusercontent.com/eurisko-us/eurisko-us.github.io/master/files/strategies/cohort-1/level-3/riley_strategy_level_3.py",
     "riley_strategy.py"),

]

for url, file_name in to_fetch:
    with urllib.request.urlopen(url) as response:
        content = response.read()
        with open(os.path.join(dirname, file_name), "wb") as text_file:
            text_file.write(content)
