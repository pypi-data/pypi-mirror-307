from oproxy import TransparentProxy

proxy = TransparentProxy(
    proxy_port=11434,
    target_host="remote.example.com",
    target_port=11434,
    enable_udp=True
)
proxy.start()