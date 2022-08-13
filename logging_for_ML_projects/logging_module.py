import logging
import os

class logging_cls:
    def __init__(self, log_path, period, year):
        self.log_path = log_path
        self.period = period
        self.year = year

    def configure_logging(self):
        # Log file location
        os.chdir(self.log_path)
        
        # Log File Name
        name = f"logs_{self.period}_{self.year}_test"

        # format for logs
        # formatter = "%(levelname)s %(asctime)s %(name)s: %(message)s"
        formatter = "%(levelname)s %(asctime)s: %(message)s"

        #Configurations for root logging
        logging.basicConfig(
                            level=logging.DEBUG,
                            format=formatter,
                            handlers=[
                                # "a" - append, "w"- overwrite on each run
                                logging.FileHandler(f"{name}.log", mode='w')])

    def add_log_debug(self, message):
        logging.debug(message)
        print(f"DEBUG: {message}")

    def add_log_info(self, message):
        logging.info(message)
        print(f"INFO: {message}")

    def add_log_warning(self, message):
        logging.warning(message)
        print(f"WARNING: {message}")

    def add_log_error(self, message):
        logging.error(message)
        print(f"ERROR: {message}")

    def add_log_critical(self, message):
        logging.critical(message)
        print(f"CRITICAL: {message}")


# NOTE By default level is warning, which means debug and info is not shown 
# it showns warning and higher level logs 

# 5. CRITICAL  ^
# 4. ERROR     ^
# 3. WARNING   ^
# 2. INFO      ^
# 1. DEBUG     ^