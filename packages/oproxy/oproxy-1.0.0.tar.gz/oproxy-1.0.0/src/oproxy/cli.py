import os
import argparse
from dotenv import load_dotenv
from .core import TransparentProxy


def parse_args():
    parser = argparse.ArgumentParser(
        description="Transparent TCP/UDP Proxy with logging capabilities"
    )
    # Required proxy configuration
    parser.add_argument(
        "--proxy-port",
        type=int,
        default=11434,
        help="Port the proxy will listen on (default: 11434)",
    )
    parser.add_argument(
        "--target-host",
        type=str,
        default="192.168.1.100",
        help="Target host to forward traffic to (default: 192.168.1.100)",
    )
    parser.add_argument(
        "--target-port",
        type=int,
        default=11434,
        help="Target port to forward traffic to (default: 11434)",
    )

    # Optional features
    parser.add_argument(
        "--log-file",
        type=str,
        help="Path to the log file",
        default="/var/log/oproxy.log",
    )
    parser.add_argument(
        "--log-data",
        action="store_true",
        help="Enable logging of data content",
        default=False,
    )
    parser.add_argument(
        "--full-debug",
        action="store_true",
        help="Enable full data logging (entire payload)",
        default=False,
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the logging level",
    )
    parser.add_argument(
        "--enable-udp", action="store_true", help="Enable UDP proxy alongside TCP"
    )
    return parser.parse_args()


def main():
    load_dotenv()  # Still load .env for backward compatibility
    args = parse_args()

    # CLI args take precedence over env vars
    proxy = TransparentProxy(
        proxy_port=args.proxy_port,
        target_host=args.target_host,
        target_port=args.target_port,
        enable_udp=args.enable_udp,
        log_file=args.log_file,
        log_level=args.log_level,
        log_data=args.log_data,
        full_debug=args.full_debug,
    )

    proxy.start()


if __name__ == "__main__":
    main()
