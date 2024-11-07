# -*- encoding: utf-8 -*-

from pyzrpc.rabbit.rabbit import _RabbitMQ


class RabbitMQ(_RabbitMQ):

    def config(self): super().config()

    def update(self, config): super().update(config)

    def send_message(self, queue, message): super().send_message(queue, message)

    def get_message(self, queue, callback): super().get_message(queue, callback)
