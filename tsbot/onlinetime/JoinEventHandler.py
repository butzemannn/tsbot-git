#!/usr/python


# TODO: Case that user connected and disconnected, without being processed by JoinEventHandler
# will be put back into the queue (then has to wait for some time) and will be discarded
class JoinEventHandler(object):

    join_queue = None

    def __init__(self, join_queue):
        self.join_queue = join_queue

    def create_user_from_event(self, join_event):
        # TODO
        """
        accesses database and creates new user from a joining event
        :param join_event: the join event the user will be created from
        :return: None
        """
        pass

    def run(self):
        while True:
            # wait for new item in queue
            join_event = self.join_queue.get()
            self.create_user_from_event(join_event)
