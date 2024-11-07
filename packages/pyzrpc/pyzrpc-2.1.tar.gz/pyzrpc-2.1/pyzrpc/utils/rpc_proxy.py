# -*- encoding: utf-8 -*-
import uuid
from kombu import Queue
from nameko.extensions import Entrypoint
from nameko.containers import WorkerContext
from nameko.standalone.rpc import PollingQueueConsumer, ConsumeEvent
from nameko.rpc import ReplyListener, RPC_REPLY_QUEUE_TEMPLATE, get_rpc_exchange, RPC_REPLY_QUEUE_TTL, MethodProxy

from pyzrpc.meta import CONFIG_RPC_PROXY_NAME_KEY, CONFIG_RPC_PROXY_METHOD_NAME_KEY


class MyReplyListener(ReplyListener):
    queue = None
    routing_key = None

    def setup(self):
        if self.queue is None:
            reply_queue_uuid = uuid.uuid4()
            service_name = self.container.service_name

            queue_name = RPC_REPLY_QUEUE_TEMPLATE.format(service_name, reply_queue_uuid)

            self.routing_key = str(reply_queue_uuid)
            exchange = get_rpc_exchange(self.container.config)
            self.queue = Queue(
                queue_name,
                exchange=exchange,
                routing_key=self.routing_key,
                queue_arguments={
                    'x-expires': RPC_REPLY_QUEUE_TTL
                },
                auto_delete=True
            )
            self.queue_consumer.register_provider(self)


class MySingleThreadedReplyListener(MyReplyListener):
    queue_consumer = None

    def __init__(self, timeout=None):
        self.queue_consumer = PollingQueueConsumer(timeout=timeout)
        super(MySingleThreadedReplyListener, self).__init__()

    def get_reply_event(self, correlation_id):
        reply_event = ConsumeEvent(self.queue_consumer, correlation_id)
        self._reply_events[correlation_id] = reply_event
        return reply_event


class MyStandaloneProxyBase(object):
    class ServiceContainer(object):
        service_name = '{}'.format(CONFIG_RPC_PROXY_NAME_KEY)

        def __init__(self, config):
            self.config = config
            self.shared_extensions = {}

    class Dummy(Entrypoint):
        method_name = CONFIG_RPC_PROXY_METHOD_NAME_KEY

    _proxy = None

    def __init__(
            self, config, context_data=None, timeout=None,
            reply_listener_cls=MySingleThreadedReplyListener
    ):
        container = self.ServiceContainer(config)
        self._worker_ctx = WorkerContext(
            container, service=None, entrypoint=self.Dummy,
            data=context_data)
        self._reply_listener = reply_listener_cls(
            timeout=timeout).bind(container)

    def __enter__(self):
        return self.start()

    def __exit__(self, tpe, value, traceback):
        self.stop()

    def start(self):
        self._reply_listener.setup()
        return self._proxy

    def stop(self):
        self._reply_listener.stop()


class MyServiceProxy(object):
    def __init__(self, worker_ctx, service_name, reply_listener, **options):
        self.worker_ctx = worker_ctx
        self.service_name = service_name
        self.reply_listener = reply_listener
        self.options = options

    def __getattr__(self, name):
        return MethodProxy(
            self.worker_ctx,
            self.service_name,
            name,
            self.reply_listener,
            **self.options
        )


class MyServiceRpcProxy(MyStandaloneProxyBase):
    def __init__(self, service_name, *args, **kwargs):
        super(MyServiceRpcProxy, self).__init__(*args, **kwargs)
        self._proxy = MyServiceProxy(self._worker_ctx, service_name, self._reply_listener)


class MyClusterProxy(object):
    def __init__(self, worker_ctx, reply_listener):
        self._worker_ctx = worker_ctx
        self._reply_listener = reply_listener
        self._proxies = {}

    def __getattr__(self, name):
        if name not in self._proxies:
            _service_proxy = MyServiceProxy(self._worker_ctx, name, self._reply_listener)
            self._proxies[name] = _service_proxy
        return self._proxies[name]

    def __getitem__(self, name):
        return getattr(self, name)


class MyClusterRpcProxy(MyStandaloneProxyBase):
    def __init__(self, *args, **kwargs):
        super(MyClusterRpcProxy, self).__init__(*args, **kwargs)
        self._proxy = MyClusterProxy(self._worker_ctx, self._reply_listener)
