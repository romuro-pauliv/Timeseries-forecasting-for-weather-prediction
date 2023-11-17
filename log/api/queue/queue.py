# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 api.queue.queue.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

class LogQueue(object):
    def __init__(self) -> None:
        """
        Initialize LogQueue instance.
        """
        self.queue: list[str] = []
    
    def receiver_in_queue(self, data: str) -> None:
        """
        Receiver data in message queue
        Args:
            data (str): Data Log
        """
        self.queue.append(data)
    
    def get_in_queue(self) -> str:
        """
        Get data in message queue. After get data, the data in delete on the queue.
        Returns:
            str: Data Log
        """
        return self.queue.pop(0)
    
    def queue_len(self) -> int:
        """
        Get length of the queue. Essential to controller data flow
        Returns:
            int: Queue length
        """
        return len(self.queue)


# Initialize Message Queue
Queue: LogQueue = LogQueue()