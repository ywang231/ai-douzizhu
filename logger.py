# pylint: disable=invalid-name
# pylint: disable=missing-function-docstring,
# pylint: disable=missing-module-docstring
# pylint: disable=broad-exception-caught
# pylint: disable=missing-class-docstring

import os
from datetime import datetime
from dotenv import load_dotenv


class Logger:

    instance_ = None

    def __new__(cls):
        if not cls.instance_:
            cls.instance_ = super(Logger, cls).__new__(cls)
            print("Creating Logger instance")
        return cls.instance_

    @property
    def mode(self):
        '''Returns the current logging mode'''
        return self.dev_mode_

    @mode.setter
    def mode(self, mode):
        '''Sets the logging mode'''
        self.dev_mode_ = mode

    @property
    def log_file(self):
        '''Returns the current log file path'''
        return self.log_file_

    @property
    def file_log_switch(self):
        return self.file_log_switch_

    @file_log_switch.setter
    def file_log_switch(self, sw_state: bool):
        '''Sets the file logging switch'''
        self.file_log_switch_ = sw_state

    def __init__(self):

        load_dotenv()

        self.dev_mode_ = os.environ.get(
            'DEV_MODE', default='production').upper()

        self.log_file_ = os.environ.get('LOG_FILE_PATH', default='game.log')
        self.file_log_switch_ = os.environ.get(
            'FILE_LOG_SWITCH', default='true').lower() == 'true'

    def log(self, message):
        # Add time for each log message
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")
        message = f"[{self.dev_mode_}]: {message}"
        message = f"{timestamp} - {message}"

        if self.dev_mode_ == "DEBUG":
            print(message)

        if not self.file_log_switch_:
            return

        try:
            with open(self.log_file_, encoding='utf-8', mode='a') as log_file:
                log_file.write(f"{message}\n")
        except Exception as e:
            print(f"[ERROR]: Failed to log message to file: {e}")


LLG = Logger()

# LLG.file_log_switch = False


def Logging(message):
    LLG.log(message)


if __name__ == "__main__":
    Logging("Logger initialized")
    Logging("This is a test log message")
    Logging("This is another test log message")

    LLG.file_log_switch = False

    Logging("This log should not appear in the file")
    Logging("End of logging test")
    LLG.mode = "Production"
    Logging("This log should appear in the file")
