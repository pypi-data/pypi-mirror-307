import os
import socket
import threading
import logging
from typing import Optional
from dotenv import load_dotenv

from .proxy.tcp_handler import TCPHandler
from .proxy.udp_handler import UDPHandler
from .proxy.metrics import ConnectionMetrics, MetricsReporter
from .proxy.logger import setup_logging

class TransparentProxy:
    def __init__(
        self,
        proxy_port: int = 8080,
        target_host: str = 'localhost',
        target_port: int = 80,
        proxy_host: str = '0.0.0.0',
        enable_udp: bool = False,
        log_file: Optional[str] = None,
        log_level: str = 'INFO',
        log_data: bool = False,
        full_debug: bool = False
    ):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.target_host = target_host
        self.target_port = target_port
        self.enable_udp = enable_udp
        self.log_file = log_file
        self.log_level = log_level
        self.log_data = log_data
        self.full_debug = full_debug
        
        # Initialize components
        setup_logging(log_file, getattr(logging, log_level))
        self.metrics = ConnectionMetrics()
        self.metrics_reporter = MetricsReporter(self.metrics, interval=60)
        self.tcp_handler = TCPHandler(target_host, target_port, self.metrics)

    def start(self):
        self.metrics_reporter.start()

        # Setup TCP server
        tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        tcp_server.bind((self.proxy_host, self.proxy_port))
        tcp_server.listen(100)

        logging.info(f"TCP proxy listening on {self.proxy_host}:{self.proxy_port}")
        logging.info(f"Forwarding to {self.target_host}:{self.target_port}")

        # Start UDP handler if enabled
        if self.enable_udp:
            udp_handler = UDPHandler(self.proxy_host, self.proxy_port, 
                                   self.target_host, self.target_port)
            udp_thread = threading.Thread(
                target=udp_handler.start,
                args=(self.log_data,),
                daemon=True
            )
            udp_thread.start()
            logging.info("UDP proxy enabled")

        # Main TCP loop
        while True:
            client_socket, addr = tcp_server.accept()
            proxy_thread = threading.Thread(
                target=self.tcp_handler.handle_client,
                args=(client_socket, self.log_data, self.full_debug)
            )
            proxy_thread.start()