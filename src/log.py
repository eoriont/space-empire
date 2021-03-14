class Log:
    def __init__(self, stdout: any, debug_mode: bool):
        self.stdout = stdout
        self.debug_mode = debug_mode
        if type(stdout) == str:
            self.file = open(stdout, "w")

    def info(self, s: str):
        if type(self.stdout) == bool and self.stdout:
            print(s)
        elif type(self.stdout) == str:
            self.file.write(str(s) + "\n")

    def throw(self, s):
        self.info(s)
        if self.debug_mode:
            import sys
            sys.exit(0)

    def save(self):
        if type(self.stdout) == str:
            self.file.close()
