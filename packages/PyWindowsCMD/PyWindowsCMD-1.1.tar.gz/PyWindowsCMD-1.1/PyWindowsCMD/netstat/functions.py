from operator import and_
from functools import reduce
from subprocess import PIPE, Popen
from PyWindowsCMD.netstat.command import cmd_netstat_windows
from PyWindowsCMD.utilities import check_ip_is_localhost, get_port_from_ipv4
from PyWindowsCMD.netstat.utilities import read_netstat_ethernet_stats, read_netstat_line, read_netstat_line_with_pid, read_netstat_line_with_time, read_protocol_stats, read_routing_table
#
#
#
#
def netstat_windows(
        a: bool = False,
        b: bool = False,
        e: bool = False,
        f: bool = False,
        i: bool = False,
        n: bool = False,
        o: bool = False,
        p: str = None,
        r: bool = False,
        s: bool = False,
        t: bool = False,
        x: bool = False,
        return_str: bool = False
):
    """
    Windows CMD command to get network statistics of the computer. \n
    [/a] [/b] [/e] [/f] [/i] [/n] [/o] [/p proto] [/r] [/s] [/t] [/x]
    :param a: displays all connections and listening ports.
    :param b: displays the executable involved in creating each connection or listening port. In some cases well-known executables host multiple independent components, and in these cases the sequence of components involved in creating the connection or listening port is displayed. In this case the executable name is in [] at the bottom, on top is the component it called, and so forth until TCP/IP was reached. Note that this option can be time-consuming and will fail unless you have sufficient permissions.
    :param e: displays Ethernet statistics. This may be combined with the "s" parameter.
    :param f: displays Fully Qualified Domain Names (FQDN) for foreign addresses.
    :param i: displays the time spent by a TCP connection in its current state.
    :param n: displays addresses and port numbers in numerical form.
    :param o: displays the owning process ID associated with each connection.
    :param p: shows connections for the protocol specified by proto; proto may be any of: TCP, UDP, TCPv6, or UDPv6. If used with the "s" parameter to display per-protocol statistics, proto may be any of: IP, IPv6, ICMP, ICMPv6, TCP, TCPv6, UDP, or UDPv6.
    :param r: displays the routing table.
    :param s: displays per-protocol statistics. By default, statistics are shown for IP, IPv6, ICMP, ICMPv6, TCP, TCPv6, UDP, and UDPv6; the "p" parameter may be used to specify a subset of the default.
    :param t: displays the current connection offload state.
    :param x: displays NetworkDirect connections, listeners, and shared endpoints.
    :param return_str: if True returns netstat as string, if False returns netstat as dict.
    """
    netstat_output = Popen(cmd_netstat_windows(a, b, e, f, i, n, o, p, r, s, t, x), stdout=PIPE, shell=True).communicate()[0].decode("windows-1252", errors="ignore")

    if return_str:
        return netstat_output
    else:
        netstat_output = netstat_output.splitlines()

        if n:
            if i:
                return list(map(lambda line: read_netstat_line_with_time(line, t), netstat_output[4:]))
            elif o:
                return list(map(lambda line: read_netstat_line_with_pid(line, t), netstat_output[4:]))
            else:
                return list(map(lambda line: read_netstat_line(line, t), netstat_output[4:]))
        else:
            internet_blocs = {}

            if e:
                internet_blocs["ethernet"], netstat_output = read_netstat_ethernet_stats(netstat_output)

            if s:
                internet_blocs["ethernet_protocols"], netstat_output = read_protocol_stats(netstat_output)

            if r:
                internet_blocs["routing_table"] = read_routing_table("\n".join(netstat_output))

            return internet_blocs
#
#
#
#
def get_localhost_processes_with_pids():
    """
    Function to get all active processes on localhost IPv4.
    :return: dictionary of processes. Type: {pid: [port, port...], pid: [port, port...]...}.
    """
    processes = {}

    for netstat in netstat_windows(a=True, f=True, n=True, o=True, p="TCP"):
        if check_ip_is_localhost(netstat["local_address"]):
            if netstat["pid"] in processes.keys():
                processes[netstat["pid"]].append(get_port_from_ipv4(netstat["local_address"]))
            else:
                processes[netstat["pid"]] = [get_port_from_ipv4(netstat["local_address"])]

        if check_ip_is_localhost(netstat["foreign_address"]):
            if netstat["pid"] in processes.keys():
                processes[netstat["pid"]].append(get_port_from_ipv4(netstat["foreign_address"]))
            else:
                processes[netstat["pid"]] = [get_port_from_ipv4(netstat["foreign_address"])]

    return processes
#
#
#
#
def get_localhost_beasy_ports():
    """
    Function to get all beasy ports of localhost IPv4.
    :return: list of ports. Type: [port, port...].
    """
    return list(
            set(
                    filter(
                            lambda port: port is not None,
                            map(
                                    lambda line: get_port_from_ipv4(line["local_address"]) if check_ip_is_localhost(line["local_address"]) else None,
                                    netstat_windows(a=True, f=True, n=True, p="TCP")
                            )
                    )
            )
    )
#
#
#
#
def get_localhost_free_ports():
    """
    Function to get all free ports of localhost IPv4.
    :return: list of ports. Type: [port, port...].
    """
    beasy_ports = get_localhost_beasy_ports()
    return list(filter(lambda port: port not in beasy_ports, list(range(1024, 49151))))
#
#
#
#
def get_localhost_minimum_free_port(ports_to_check: int | list[int] = None):
    """
    Function to get minimum free port of localhost IPv4. \n
    Rules: \n
    - If "ports_to_check" is None function searches minimum localhost free port in range [1024;49150]. \n
    - If "ports_to_check" is int function searches this port in localhost free ports, if this port isn't free then searches as "ports_to_check" is None. \n
    - If "ports_to_check" is list function searches minimum overlap of "ports_to_check" and localhost free ports, if there's no overlap then searches as "ports_to_check" is None.
    :param ports_to_check: port/ports to check in localhost free ports.
    :return: minimum localhost free port.
    """
    localhost_free_ports = get_localhost_free_ports()

    if type(ports_to_check) == int:
        if ports_to_check in localhost_free_ports:
            return ports_to_check
        else:
            return min(localhost_free_ports)
    elif type(ports_to_check) == list:
        if list(reduce(and_, [set(ports_to_check), set(localhost_free_ports)])):
            return min(list(reduce(and_, [set(ports_to_check), set(localhost_free_ports)])))
        else:
            return min(localhost_free_ports)
    else:
        return min(localhost_free_ports)
