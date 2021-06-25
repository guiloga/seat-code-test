class ConfigPathError(Exception):
    def __str__(self):
        msg = ("Unable to read config from default location; "
               "set CONFIG_PATH environment variable.")
        return msg



class VoidScheduleError(Exception):
    def __str__(self):
        return ("Unable to run controller schedule: is void.")


class InvalidCommandError(Exception):
    def __init__(self, cmd, valids, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmd = cmd
        self.valids = valids
    
    def __str__(self):
        return ("Invalid command provided %s: valid ones are %s" %
                (self.cmd, self.valids))
