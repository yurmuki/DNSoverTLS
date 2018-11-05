# DNS Proxy Over TLS

## Objective
These days nearly all DNS queries are sent unencrypted, which makes them vulnerable to eavesdropping by an attacker that has access to the network channel, reducing the privacy of the querier. To overcome this situation there is an alternate approach to run DNS over TLS.

## Performance Consideration
1. DNS-over-TLS incurs additional latency at session startup. It also requires additional state (memory) and increased processing (CPU).

2. Latency: Compared to UDP, DNS-over-TCP requires an additional round-trip-time (RTT) of latency to establish the connection. The TLS handshake adds another two RTTs of latency. Clients and servers should support connection keepalive (reuse) and out-of-order processing to amortize connection setup costs. Moreover, TLS connection resumption can further reduce the setup delay.

3. State: The use of connection-oriented TCP requires keeping additional state in both kernels and applications. TLS has marginal increases in state over TCP alone. The state requirements are of particular concerns on servers with many clients. Smaller timeout values will reduce the number of concurrent connections, and servers can preemptively close connections when resources limits are exceeded.

4. Processing: Use of TLS encryption algorithms results in slightly higher CPU usage. Servers can choose to refuse new DNS-over-TCP clients if processing limits are exceeded.

5. Number of connections: To minimize state on DNS servers and connection startup time, clients SHOULD minimize creation of new TCP connections. Use of a local DNS forwarder allows a single active DNS-over-TLS connection allows a single active TCP connection for DNS per client computer.

## Security concerns for this kind of service:
There are a number of residual risks that may impact this goal.

1. There are known attacks on TLS, such as person-in-the-middle and protocol downgrade. These are general attacks on TLS and not specific to DNS-over-TLS; please refer to the TLS RFCs for discussion of these security issues.

2. Any protocol interactions prior to the TLS handshake are performed in the clear and can be modified by a man-in-the-middle attacker. For this reason, clients MAY discard cached information about server capabilities advertised prior to the start of the TLS handshake.

3. As with other uses of STARTTLS-upgrade to TLS, the mechanism specified here is susceptible to downgrade attacks, where a person-in-the-middle prevents a successful TLS upgrade. Keeping track of servers known to support TLS (i.e., "pinning") enables clients to detect downgrade attacks. For servers with no connection history, clients may choose to refuse non-TLS DNS, or they may continue without TLS, depending on their privacy requirements.

## Microservice Architecture Consideration:
We have to ensure that the application server has to be linked with our DNS server so that it can resolve its queries. To acheive this, we have to link our application server as below:

`docker run -t -d --name application-container-name --link=dnsovertls application-image-name`

## Other recommendations for the project:
We should consider DNS caching to optimize DNS queries and DNS response time. 

**Building Docker Image**
`docker build -t dnsovertls:proxy .`

**Running Container from Built Image**
`docker run --name dnsovertls -p 53:53 -d dnsovertls:proxy`

**Container Logs showing running python script**
```docker logs dnsovertls
[dnsproxy] tcp://127.0.0.1:53 -> tcp+tls://1.1.1.1:853
```

**Using getdns_query Tool to Query over tls. DNS response is as below**
```
getdns_query @127.0.0.1:53 -A google.com
```
```
{
  "answer_type": GETDNS_NAMETYPE_DNS,
  "canonical_name": <bindata for google.com.>,
  "just_address_answers":
  [
    {
      "address_data": <bindata for 2a00:1450:4019:803::200e>,
      "address_type": <bindata of "IPv6">
    },
    {
      "address_data": <bindata for 216.58.207.110>,
      "address_type": <bindata of "IPv4">
    }
  ],
  "replies_full":
  [
     <bindata of 0x00008180000100010000000106676f6f...>,
     <bindata of 0x00008180000100010000000106676f6f...>
  ],
  "replies_tree":
  [
    {
      "additional":
      [
        {
          "do": 1,
          "extended_rcode": 0,
          "rdata":
          {
            "rdata_raw": <bindata of 0x>
          },
          "type": GETDNS_RRTYPE_OPT,
          "udp_payload_size": 65535,
          "version": 0,
          "z": 0
        }
      ],
      "answer":
      [
        {
          "class": GETDNS_RRCLASS_IN,
          "name": <bindata for google.com.>,
          "rdata":
          {
            "ipv6_address": <bindata for 2a00:1450:4019:803::200e>,
            "rdata_raw": <bindata of 0x2a00145040190803000000000000200e>
          },
          "ttl": 299,
          "type": GETDNS_RRTYPE_AAAA
        }
      ],
      "answer_type": GETDNS_NAMETYPE_DNS,
      "authority": [],
      "canonical_name": <bindata for google.com.>,
      "header":
      {
        "aa": 0,
        "ad": 0,
        "ancount": 1,
        "arcount": 1,
        "cd": 0,
        "id": 0,
        "nscount": 0,
        "opcode": GETDNS_OPCODE_QUERY,
        "qdcount": 1,
        "qr": 1,
        "ra": 1,
        "rcode": GETDNS_RCODE_NOERROR,
        "rd": 1,
        "tc": 0,
        "z": 0
      },
      "question":
      {
        "qclass": GETDNS_RRCLASS_IN,
        "qname": <bindata for google.com.>,
        "qtype": GETDNS_RRTYPE_AAAA
      }
    },
    {
      "additional":
      [
        {
          "do": 1,
          "extended_rcode": 0,
          "rdata":
          {
            "rdata_raw": <bindata of 0x>
          },
          "type": GETDNS_RRTYPE_OPT,
          "udp_payload_size": 65535,
          "version": 0,
          "z": 0
        }
      ],
      "answer":
      [
        {
          "class": GETDNS_RRCLASS_IN,
          "name": <bindata for google.com.>,
          "rdata":
          {
            "ipv4_address": <bindata for 216.58.207.110>,
            "rdata_raw": <bindata of 0xd83acf6e>
          },
          "ttl": 300,
          "type": GETDNS_RRTYPE_A
        }
      ],
      "answer_type": GETDNS_NAMETYPE_DNS,
      "authority": [],
      "canonical_name": <bindata for google.com.>,
      "header":
      {
        "aa": 0,
        "ad": 0,
        "ancount": 1,
        "arcount": 1,
        "cd": 0,
        "id": 0,
        "nscount": 0,
        "opcode": GETDNS_OPCODE_QUERY,
        "qdcount": 1,
        "qr": 1,
        "ra": 1,
        "rcode": GETDNS_RCODE_NOERROR,
        "rd": 1,
        "tc": 0,
        "z": 0
      },
      "question":
      {
        "qclass": GETDNS_RRCLASS_IN,
        "qname": <bindata for google.com.>,
        "qtype": GETDNS_RRTYPE_A
      }
    }
  ],
  "status": GETDNS_RESPSTATUS_GOOD
}
```
