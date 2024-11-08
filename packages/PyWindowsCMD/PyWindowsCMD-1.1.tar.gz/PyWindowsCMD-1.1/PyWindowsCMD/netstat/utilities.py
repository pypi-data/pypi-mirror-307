from re import DOTALL, findall, search, sub
#
#
#
#
def read_netstat_line(netstat_line: str, offload_state: bool):
    vars_ = {}
    protocol = search(r"\A\s*(\w+)", netstat_line).group(1)

    vars_["protocol"] = protocol
    netstat_line = sub(r"\A\s*\w+\s+", "", netstat_line, 1)

    vars_["local_address"] = search(r"\A\S+", netstat_line).group(0)
    netstat_line = sub(r"\A\S+\s+", "", netstat_line, 1)

    vars_["foreign_address"] = search(r"\A\S+", netstat_line).group(0)
    netstat_line = sub(r"\A\S+\s+", "", netstat_line, 1)

    if protocol == "TCP":
        vars_["state"] = search(r"\A\w+", netstat_line).group(0)
    else:
        vars_["state"] = ""

    if offload_state and protocol == "TCP":
        netstat_line = sub(r"\A\w+\s+", "", netstat_line, 1)
        vars_["offload_state"] = search(r"\A\w+", netstat_line).group(0)

    return vars_
#
#
#
#
def read_netstat_line_with_time(netstat_line: str, offload_state: bool):
    vars_ = {}
    protocol = search(r"\A\s*(\w+)", netstat_line).group(1)

    vars_["protocol"] = protocol
    netstat_line = sub(r"\A\s*\w+\s+", "", netstat_line, 1)

    vars_["local_address"] = search(r"\A\S+", netstat_line).group(0)
    netstat_line = sub(r"\A\S+\s+", "", netstat_line, 1)

    vars_["foreign_address"] = search(r"\A\S+", netstat_line).group(0)
    netstat_line = sub(r"\A\S+\s+", "", netstat_line, 1)

    if protocol == "TCP":
        vars_["state"] = search(r"\A\w+", netstat_line).group(0)
    else:
        vars_["state"] = ""
    netstat_line = sub(r"\A\w+\s+", "", netstat_line, 1)

    vars_["time"] = int(search(r"\A\d+", netstat_line).group(0))

    if offload_state and protocol == "TCP":
        netstat_line = sub(r"\A\w+\s+", "", netstat_line, 1)
        vars_["offload_state"] = search(r"\A\w+", netstat_line).group(0)

    return vars_
#
#
#
#
def read_netstat_line_with_pid(netstat_line: str, offload_state: bool):
    vars_ = {}
    protocol = search(r"\A\s*(\w+)", netstat_line).group(1)

    vars_["protocol"] = protocol
    netstat_line = sub(r"\A\s*\w+\s+", "", netstat_line, 1)

    vars_["local_address"] = search(r"\A\S+", netstat_line).group(0)
    netstat_line = sub(r"\A\S+\s+", "", netstat_line, 1)

    vars_["foreign_address"] = search(r"\A\S+", netstat_line).group(0)
    netstat_line = sub(r"\A\S+\s+", "", netstat_line, 1)

    if protocol == "TCP":
        vars_["state"] = search(r"\A\w+", netstat_line).group(0)
    else:
        vars_["state"] = ""
    netstat_line = sub(r"\A\w+\s+", "", netstat_line, 1)

    vars_["pid"] = int(search(r"\A\d+", netstat_line).group(0))

    if offload_state and protocol == "TCP":
        netstat_line = sub(r"\A\w+\s+", "", netstat_line, 1)
        vars_["offload_state"] = search(r"\A\w+", netstat_line).group(0)

    return vars_
#
#
#
#
def read_netstat_ethernet_stats(netstat_ethernet_stats: list[str]):
    vars_ = {}
    netstat_ethernet_stats = netstat_ethernet_stats[4:]

    bytes_ = search(r"(\d+)\s+(\d+)", netstat_ethernet_stats.pop(0))
    vars_["bytes"] = {"received": int(bytes_.group(1)), "send": int(bytes_.group(1))}

    unicast = search(r"(\d+)\s+(\d+)", netstat_ethernet_stats.pop(0))
    vars_["unicast"] = {"received": int(unicast.group(1)), "send": int(unicast.group(1))}

    multicast = search(r"(\d+)\s+(\d+)", netstat_ethernet_stats.pop(0))
    vars_["multicast"] = {"received": int(multicast.group(1)), "send": int(multicast.group(1))}

    discarded = search(r"(\d+)\s+(\d+)", netstat_ethernet_stats.pop(0))
    vars_["discarded"] = {"received": int(discarded.group(1)), "send": int(discarded.group(1))}

    errors = search(r"(\d+)\s+(\d+)", netstat_ethernet_stats.pop(0))
    vars_["errors"] = {"received": int(errors.group(1)), "send": int(errors.group(1))}

    vars_["unknown_protocols"] = int(search(r"\d+", netstat_ethernet_stats.pop(0)).group(0))

    return vars_, netstat_ethernet_stats
#
#
#
#
def read_ipv6_route_line(netstat_ipv4_route_line: str):
    stats = search(r"\A\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", netstat_ipv4_route_line)

    return {
        "if": int(stats.group(1)),
        "metric": int(stats.group(2)),
        "network_destination": stats.group(3),
        "gateway": stats.group(4)
    }
#
#
#
#
def read_ipv6_route_table(
        netstat_ipv6_active_route_table: list[str],
        netstat_ipv6_persistent_route_table: list[str]
):
    return {
        "active_routes": list(
                map(
                        lambda line: read_ipv6_route_line(line),
                        findall(r"\s*\S+\s+\S+\s+\S+\s+\S+", "\n".join(netstat_ipv6_active_route_table[2:]))
                )
        ),
        "persistent_routes": list(
                map(
                        lambda line: read_ipv6_route_line(line),
                        findall(r"\s*\S+\s+\S+\s+\S+\s+\S+", "\n".join(netstat_ipv6_persistent_route_table[2:]))
                )
        )
    }
#
#
#
#
def read_ipv4_persistent_route_line(netstat_ipv4_persistent_route_line: str):
    stats = search(r"\A\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", netstat_ipv4_persistent_route_line)

    return {
        "network_address": stats.group(1),
        "netmask": stats.group(2),
        "gateway": stats.group(3),
        "metric": int(stats.group(4))
    }
#
#
#
#
def read_ipv4_active_route_line(netstat_ipv4_active_route_line: str):
    stats = search(r"\A\s*(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)", netstat_ipv4_active_route_line)

    return {
        "network_destination": stats.group(1),
        "netmask": stats.group(2),
        "gateway": stats.group(3),
        "interface": stats.group(4),
        "metric": int(stats.group(5))
    }
#
#
#
#
def read_ipv4_route_table(
        netstat_ipv4_active_route_table: list[str],
        netstat_ipv4_persistent_route_table: list[str]
):
    return {
        "active_routes": list(
                map(
                        lambda line: read_ipv4_active_route_line(line),
                        findall(
                                r"\s*\S+\s+\S+\s+\S+\s+\S+\s+\S+",
                                "\n".join(netstat_ipv4_active_route_table[2:])
                        )
                )
        ),
        "persistent_routes": list(
                map(
                        lambda line: read_ipv4_persistent_route_line(line),
                        findall(r"\s*\S+\s+\S+\s+\S+\s+\S+", "\n".join(netstat_ipv4_persistent_route_table[2:]))
                )
        )
    }
#
#
#
#
def read_interface_list(netstat_interface_list: list[str]):
    return netstat_interface_list[1:]
#
#
#
#
def read_routing_table(netstat_routing_table: str):
    tables = search(
            r"\A=+\n(.+?)=+\n.*?IPv4.*?=+\n(.+?)=+\n(.*?)=+\n.*?IPv6.*?=+\n(.+?)=+\n(.*?)",
            netstat_routing_table,
            DOTALL
    )

    return {
        "interface_list": read_interface_list(tables.group(1).splitlines()),
        "IPv4_route_table": read_ipv4_route_table(tables.group(2).splitlines(), tables.group(3).splitlines()),
        "IPv6_route_table": read_ipv6_route_table(tables.group(4).splitlines(), tables.group(5).splitlines())
    }
#
#
#
#
def read_icmpv6_stats(netstat_icmpv6_stats: list[str]):
    vars_ = {
        "messages": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "errors": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "destination_unreachable": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "packet_too_big": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "time_exceeding": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "parameter_problems": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "echos": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "echo_replies": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "mld_queries": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "mld_reports": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "mld_dones": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "router_solicitations": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "router_advertisements": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "neighbor_solicitations": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "neighbor_advertisements": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "redirects": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        },
        "router_renumberings": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv6_stats.pop(0)).group(2))
        }
    }

    return vars_, netstat_icmpv6_stats
#
#
#
#
def read_icmpv4_stats(netstat_icmpv4_stats: list[str]):
    vars_ = {
        "messages": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "errors": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "destination_unreachable": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "time_exceeding": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "parameter_problems": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "source_quenches": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "redirects": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "echo_replies": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "echos": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "timestamps": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "timestamp_replies": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "address_masks": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "address_mask_replies": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "router_solicitations": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        },
        "router_advertisements": {
            "received": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats[0]).group(1)),
            "send": int(search(r"(\d+)\s+(\d+)", netstat_icmpv4_stats.pop(0)).group(2))
        }
    }

    return vars_, netstat_icmpv4_stats
#
#
#
#
def read_ip_stats(netstat_ip_stats: list[str]):
    vars_ = {
        "packets_received": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "received_header_errors": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "received_address_errors": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "datagrams_forwarded": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "unknown_protocols_received": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "received_packets_discarded": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "received_packets_delivered": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "output_requests": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "routing_discards": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "discarded_output_packets": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "output_packet_no_route": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "reassembly_required": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "reassembly_successful": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "reassembly_failures": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "datagrams_successfully_fragmented": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "datagrams_failing_fragmentation": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0)),
        "fragments_created": int(search(r"\d+", netstat_ip_stats.pop(0)).group(0))
    }

    return vars_, netstat_ip_stats
#
#
#
#
def read_udp_ip_stats(netstat_udp_ip_stats: list[str]):
    vars_ = {
        "datagrams_received": int(search(r"\d+", netstat_udp_ip_stats.pop(0)).group(0)),
        "no_ports": int(search(r"\d+", netstat_udp_ip_stats.pop(0)).group(0)),
        "receive_errors": int(search(r"\d+", netstat_udp_ip_stats.pop(0)).group(0)),
        "datagrams_sent": int(search(r"\d+", netstat_udp_ip_stats.pop(0)).group(0))
    }

    return vars_, netstat_udp_ip_stats
#
#
#
#
def read_tcp_ip_stats(netstat_tcp_ip_stats: list[str]):
    vars_ = {
        "active_opens": int(search(r"\d+", netstat_tcp_ip_stats.pop(0)).group(0)),
        "passive_opens": int(search(r"\d+", netstat_tcp_ip_stats.pop(0)).group(0)),
        "failed_connection_attempts": int(search(r"\d+", netstat_tcp_ip_stats.pop(0)).group(0)),
        "reset_connections": int(search(r"\d+", netstat_tcp_ip_stats.pop(0)).group(0)),
        "current_connections": int(search(r"\d+", netstat_tcp_ip_stats.pop(0)).group(0)),
        "segments_received": int(search(r"\d+", netstat_tcp_ip_stats.pop(0)).group(0)),
        "segments_sent": int(search(r"\d+", netstat_tcp_ip_stats.pop(0)).group(0)),
        "segments_retransmitted": int(search(r"\d+", netstat_tcp_ip_stats.pop(0)).group(0))
    }

    return vars_, netstat_tcp_ip_stats
#
#
#
#
def read_protocol_stats(netstat_protocol_stats: list[str]):
    vars_ = {}

    try:
        while search(r"IPv[46]|ICMPv[46]", netstat_protocol_stats[1]):
            if search(r"IPv[46]", netstat_protocol_stats[1]) and search(r"\bTCP\b", netstat_protocol_stats[1]):
                vars_["TCP_%s" % search(r"IPv[46]", netstat_protocol_stats[1]).group(0)], netstat_protocol_stats = read_tcp_ip_stats(netstat_protocol_stats[3:])
            elif search(r"IPv[46]", netstat_protocol_stats[1]) and search(r"\bUDP\b", netstat_protocol_stats[1]):
                vars_["UDP_%s" % search(r"IPv[46]", netstat_protocol_stats[1]).group(0)], netstat_protocol_stats = read_udp_ip_stats(netstat_protocol_stats[3:])
            elif search(r"IPv[46]", netstat_protocol_stats[1]):
                vars_[search(r"IPv[46]", netstat_protocol_stats[1]).group(0)], netstat_protocol_stats = read_ip_stats(netstat_protocol_stats[3:])
            elif search(r"ICMPv4", netstat_protocol_stats[1]):
                vars_["ICMPv4"], netstat_protocol_stats = read_icmpv4_stats(netstat_protocol_stats[4:])
            elif search(r"ICMPv6", netstat_protocol_stats[1]):
                vars_["ICMPv6"], netstat_protocol_stats = read_icmpv6_stats(netstat_protocol_stats[4:])
    except IndexError:
        pass

    return vars_, netstat_protocol_stats
