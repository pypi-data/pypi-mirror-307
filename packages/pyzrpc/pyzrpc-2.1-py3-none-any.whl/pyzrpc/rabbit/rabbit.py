# -*- encoding: utf-8 -*-

import json
import pika
import logging

from pyzrpc.meta import SubjectMeta, CONFIG_RABBIT_CONFIG_KEY


class _RabbitMQ(SubjectMeta):
    _config = None

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def update(self, config):
        self.config = config.get(CONFIG_RABBIT_CONFIG_KEY)

    def _mq_channel(self):
        host = self.config.split('@')[1].split(':')[0]
        port = self.config.split('@')[1].split(':')[1]

        user = self.config.split('@')[0].split('//')[1].split(':')[0]
        passwd = self.config.split('@')[0].split('//')[1].split(':')[1]

        credentials = pika.PlainCredentials(user, passwd)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host, port=port, virtual_host='/', credentials=credentials, heartbeat=0))
        return connection.channel()

    def _create_queue(self, queue):
        _mq_channel = self._mq_channel()
        try:
            _mq_channel.queue_declare(queue=queue)
        except Exception as e:
            logging.error(e)
        return _mq_channel

    def send_message(self, queue, message):
        _mq_channel = self._create_queue(queue=queue)
        if type(message) is not str:
            message = json.dumps(message)
        _mq_channel.basic_publish(exchange='', routing_key=queue, body=message)

    def get_message(self, queue, callback):
        _mq_channel = self._create_queue(queue=queue)
        _mq_channel.basic_consume(on_message_callback=callback, queue=queue, auto_ack=False)
        _mq_channel.start_consuming()
