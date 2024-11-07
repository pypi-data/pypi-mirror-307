from pyzrpc.observer.observer import _Observer


class Observer(_Observer):

    def config(self): super().config()

    def attach(self, subject) -> None: super().attach(subject)

    def detach(self, subject) -> None: super().detach(subject)

    def notify(self) -> None: super().notify()
