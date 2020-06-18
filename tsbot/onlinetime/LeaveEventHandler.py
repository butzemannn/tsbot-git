#!/usr/python


class LeaveEventHandler(object):

    queue = None

    def __init__(self, queue):
        self.queue = queue
