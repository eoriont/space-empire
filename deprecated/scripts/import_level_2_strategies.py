import urllib.request
import os

dirname = "imported_strategies_level_2"
if not os.path.exists(dirname):
    os.makedirs(dirname)

to_fetch = [
    ("https://raw.githubusercontent.com/eurisko-us/eurisko-us.github.io/master/files/strategies/cohort-1/level-2/colby_strategy_level_2.py",
     "colby_strategy.py"),
    ("https://raw.githubusercontent.com/eurisko-us/eurisko-us.github.io/master/files/strategies/cohort-1/level-2/david_strategy_level_2.py",
     "david_strategy.py"),
    ("https://raw.githubusercontent.com/eurisko-us/eurisko-us.github.io/master/files/strategies/cohort-1/level-2/elijah_strategy_level_2.py",
     "elijah_strategy.py"),
    ("https://raw.githubusercontent.com/eurisko-us/eurisko-us.github.io/master/files/strategies/cohort-1/level-2/george_strategy_level_2.py",
     "george_strategy.py"),
    ("https://raw.githubusercontent.com/eurisko-us/eurisko-us.github.io/master/files/strategies/cohort-1/level-2/justin_strategy_level_2.py",
     "justin_strategy.py"),
    ("https://raw.githubusercontent.com/eurisko-us/eurisko-us.github.io/master/files/strategies/cohort-1/level-2/riley_strategy_level_2.py",
     "riley_strategy.py"),

]

for url, file_name in to_fetch:
    with urllib.request.urlopen(url) as response:
        content = response.read()
        with open(os.path.join(dirname, file_name), "wb") as text_file:
            text_file.write(content)
