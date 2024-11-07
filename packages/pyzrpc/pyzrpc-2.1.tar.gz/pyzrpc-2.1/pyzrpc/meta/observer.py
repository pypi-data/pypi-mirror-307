# -*- encoding: utf-8 -*-
import abc


class ObserverMeta(abc.ABC):

    @property
    @abc.abstractmethod
    def config(self): ...

    @abc.abstractmethod
    def attach(self, subject) -> None: ...

    @abc.abstractmethod
    def detach(self, subject) -> None: ...

    @abc.abstractmethod
    def notify(self) -> None: ...


class SubjectMeta(abc.ABC):

    @abc.abstractmethod
    def update(self, config: dict): ...
