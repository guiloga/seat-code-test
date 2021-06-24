class ConfigPathError(Exception):
    def __str__(self):
        msg = ("Unable to read config from default location; "
               "set CONFIG_PATH environment variable.")
        return msg

