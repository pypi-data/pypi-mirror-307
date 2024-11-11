import json
import logging
import sched
import time
from threading import Thread
from typing import Callable, Union

from zur_ecu_client.senml.senml_msg_dv import SenmlNames, Dv
from zur_ecu_client.udp_server import UdpServer
from zur_ecu_client.messages import Messages, Acknowledgment, Data

EcuClientListener = Callable[[Acknowledgment | Data], None]


class EcuClient:

    def __init__(
        self,
        listener: EcuClientListener,
        ecu_ip: str,
        ecu_port: int,
        client_ip: str = "127.0.0.1",
        client_port: int = 9000,
        calls_per_second: int = 1,
    ) -> None:
        logging.basicConfig(level=logging.CRITICAL)
        self.listener = listener
        self.requestInterval = 1.0 / calls_per_second
        self.subscriptions: dict[SenmlNames, list[Callable]] = {}
        self.compiledMessages = []

        self.client_ip = client_ip
        self.client_port = client_port

        self.udpServer = UdpServer(self.client_ip, self.client_port, ecu_ip, ecu_port)

        self.thread1 = Thread(target=self.__receive_msg)
        # self.thread1.daemon = True
        self.thread2 = Thread(target=self.__schedule_requests)
        # self.thread2.daemon = True

    def start(self):
        self.thread1.start()
        self.thread2.start()

    def subscribe(self, data_field: Union[SenmlNames, str], subscriber: Callable):
        if type(data_field) is not SenmlNames and SenmlNames(data_field):
            data_field = SenmlNames(data_field)
        if data_field in self.subscriptions:
            self.subscriptions.get(data_field).append(subscriber)
        else:
            self.subscriptions[data_field] = [subscriber]
        self.__compile_subscriptions()

    def unsubscribe(self, data_field: Union[SenmlNames, str], subscriber: Callable):
        if data_field in self.subscriptions:
            self.subscriptions.get(data_field).remove(subscriber)
            if not self.subscriptions[data_field]:
                self.subscriptions.pop(data_field)
            self.__compile_subscriptions()

    def unsubscribe_all(self):
        self.subscriptions = {}
        self.__compile_subscriptions()

    def send_msg(self, msg):
        if not msg:
            return
        msg = json.dumps(msg)
        self.udpServer.send_data(msg)

    def __compile_subscriptions(self):
        self.compiledMessages = []
        for key in self.subscriptions:
            parameters = key.value.split(":")
            new = [{"bn": parameters[0], "n": parameters[1], "vs": parameters[2]}]
            if new not in self.compiledMessages:
                self.compiledMessages.append(
                    [{"bn": parameters[0], "n": parameters[1], "vs": parameters[2]}]
                )

    def __receive_msg(self):
        while True:
            data = self.udpServer.receive_data()
            if data:
                senml_messages = Messages.parse(data)
                for message in senml_messages:
                    self.listener(message)
                logging.info(f"Received -> {senml_messages}")

    def __request_messages(self):
        self.send_msg(self.compiledMessages)

    def __schedule_requests(self):
        scheduler = sched.scheduler(time.time, time.sleep)
        while True:
            scheduler.enter(self.requestInterval, 1, self.__request_messages, ())
            scheduler.run()
