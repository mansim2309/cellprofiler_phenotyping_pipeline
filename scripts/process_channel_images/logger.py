import logging


class Logger():

    LOG_FILENAME = 'logs/aws-task-logs.log'
    logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

    @classmethod
    def get_logger(cls):
        return logging
