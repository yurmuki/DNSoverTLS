#!/usr/bin/env python
import signal
from maproxy.iomanager import IOManager
from maproxy.proxyserver import ProxyServer

g_IOManager = IOManager()
ssl_certs={     "certfile":  "./certificate.pem",
                "keyfile": "./privatekey.pem" }


if __name__ == '__main__':
  
  server = ProxyServer("1.1.1.1", 853, server_ssl_options = True, client_ssl_options=ssl_certs)
  server.listen(53)
  g_IOManager.add(server)

  print("[dnsproxy] tcp://127.
