# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         api.data.queue_consumer.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from api.queue.queue import Queue
from api.data.writer import WriterLog

from time import sleep
# |--------------------------------------------------------------------------------------------------------------------|

writer_log: WriterLog = WriterLog()

class QueueConsumer(object):
    @staticmethod
    def run() -> None:
        """
        Initialize Queue Consumer in another Thread
        """
        while True:
            if Queue.queue_len() > 0:
                data: str = Queue.get_in_queue()
                writer_log.writer(data)
            else:
                sleep(1)