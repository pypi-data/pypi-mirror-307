# -*- encoding: utf-8 -*-

from pyzrpc.meta import ObserverMeta


class _Observer(ObserverMeta):
    _config = None
    _observer_list = []

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        self._config = value

    def attach(self, subject) -> None:
        self._observer_list.append(subject)

    def detach(self, subject) -> None:
        self._observer_list.remove(subject)

    def notify(self) -> None:
        for _observer in self._observer_list:
            _observer.update(self.config)
