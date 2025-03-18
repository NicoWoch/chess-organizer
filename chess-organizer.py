import logging

from src.main import main

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.fatal('Fatal Exception!')
        logging.fatal(e)
        raise e
