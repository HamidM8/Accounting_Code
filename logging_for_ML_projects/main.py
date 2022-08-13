from config import *
import logging_module

def main():
    Logger = logging_module.logging_cls(log_path, period, year)
    Logger.configure_logging()

    first_log = "debud test"
    Logger.add_log_debug(first_log)

    sec_log = "info test"
    Logger.add_log_info(sec_log)

    third_log = "warning test"
    Logger.add_log_warning(third_log)   

    forth_log = "error test"
    Logger.add_log_error(forth_log)   

    fifth_log = "critical test"
    Logger.add_log_critical(fifth_log)  
    

if __name__=="__main__":
    main()
    

