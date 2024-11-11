import re
import pandas
from typing import Literal
from subprocess import PIPE, Popen
from PyWindowsCMD.netstat.command import build_netstat_connections_list_command, build_netstat_routing_table_command
#
#
#
#
def read_ipv6_routing_table(cmd_output: str):
    """
    Parses the IPv6 routing table from the output of the `netstat /r` command.

    Args:
        cmd_output (str): The output of the `netstat /r` command.

    Returns:
        dict[str, pandas.DataFrame]: A dictionary containing a Pandas DataFrame for active IPv6 routes (and an empty DataFrame for persistent routes, which are not currently parsed).

    :Usage:
        ipv6_routes = read_ipv6_routing_table(netstat_output)
        active_routes_df = ipv6_routes["active_routes"]
    """
    ipv6_routing_table = re.search(
            r"IPv6 Route Table\s+={3,}\s+Active Routes:\s+(.+?)(?:={3,}|\Z)\s+Persistent Routes:\s+(.+?)(?:={3,}|\Z)",
            cmd_output,
            re.DOTALL
    )

    active_routes = re.findall(
            r"(\d+)\s+(\d+)\s+(\S+)\s+(On-link)\s+",
            ipv6_routing_table.group(1)
    )

    return {
        "active_routes": pandas.DataFrame(
                active_routes,
                columns=["If", "Metric", "Network Destination", "Gateway"]
        ),
        "persistent_routes": pandas.DataFrame()
    }
#
#
#
#
def read_ipv4_routing_table(cmd_output: str):
    """
    Parses the IPv4 routing table from the output of the `netstat /r` command.

    Args:
        cmd_output (str):  The output of the `netstat /r` command.

    Returns:
        dict[str, pandas.DataFrame]: A dictionary containing Pandas DataFrames for active and persistent IPv4 routes.

    :Usage:
        ipv4_routes = read_ipv4_routing_table(netstat_output)
        active_routes_df = ipv4_routes["active_routes"]
        persistent_routes_df = ipv4_routes["persistent_routes"]
    """
    ipv4_routing_table = re.search(
            r"IPv4 Route Table\s+={3,}\s+Active Routes:\s+(.+?)(?:={3,}|\Z)\s+Persistent Routes:\s+(.+?)(?:={3,}|\Z)",
            cmd_output,
            re.DOTALL
    )

    active_routes = re.findall(
            r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|On-link)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)\s+",
            ipv4_routing_table.group(1)
    )
    persistent_routes = re.findall(
            r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)\s+",
            ipv4_routing_table.group(1)
    )

    return {
        "active_routes": pandas.DataFrame(
                active_routes,
                columns=[
                    "Network Destination",
                    "Netmask",
                    "Gateway",
                    "Interface",
                    "Metric"
                ]
        ),
        "persistent_routes": pandas.DataFrame(
                persistent_routes,
                columns=["Network Address", "Netmask", "Gateway Address", "Metric"]
        )
    }
#
#
#
#
def read_interface_routing_table(cmd_output: str):
    """
    Parses the interface list from the output of the `netstat /r` command.

    Args:
        cmd_output (str): The output of the `netstat /r` command.

    Returns:
        pandas.DataFrame: A DataFrame containing MAC addresses and interface names.

    :Usage:
        interface_df = read_interface_routing_table(netstat_output)
    """
    interface_routing_table = re.search(r"Interface List\s+(.+?)(?:={3,}|\Z)", cmd_output, re.DOTALL).group(1)
    interfaces = re.findall(
            r"(\w+(?:(?:\.{3}| )\w+)*) \.+([\w#() -]+)\s+",
            interface_routing_table
    )

    return pandas.DataFrame(interfaces, columns=["MAC", "Interface"])
#
#
#
#
def read_netstat_routing_tables(cmd_output: str):
    """
    Parses all routing-related information from the output of `netstat /r`.

    Args:
        cmd_output (str): The output of the `netstat /r` command.

    Returns:
        dict[str, pandas.DataFrame | dict[str, pandas.DataFrame]]: A dictionary containing DataFrames for interfaces, IPv4 routes, and IPv6 routes.

    :Usage:
        routing_data = read_netstat_routing_tables(netstat_output)
        interface_df = routing_data["interface_table"]
        ipv4_df = routing_data["ipv4_routing_table"]
        ipv6_df = routing_data["ipv6_routing_table"]
    """
    interface_table = read_interface_routing_table(cmd_output)
    ipv4_routing_table = read_ipv4_routing_table(cmd_output)
    ipv6_routing_table = read_ipv6_routing_table(cmd_output)

    return {
        "interface_table": interface_table,
        "ipv4_routing_table": ipv4_routing_table,
        "ipv6_routing_table": ipv6_routing_table
    }
#
#
#
#
def get_netstat_routing_data():
    """
    Retrieves and parses routing information using `netstat /r`.

    Returns:
        dict[str, pandas.DataFrame | dict[str, pandas.DataFrame]]: A dictionary containing parsed routing tables (interfaces, IPv4, and IPv6).

    :Usage:
        routing_data = get_netstat_routing_data()
        interface_df = routing_data["interface_table"]
        ipv4_df = routing_data["ipv4_routing_table"]
        ipv6_df = routing_data["ipv6_routing_table"]
    """
    return read_netstat_routing_tables(
            Popen(build_netstat_routing_table_command(), stdout=PIPE, shell=True).communicate()[0].decode("windows-1252", errors="ignore")
    )
#
#
#
#
def get_netstat_ipv6_routing_data():
    """
    Retrieves and parses IPv6 routing information using `netstat /r`.

    Returns:
        dict[str, pandas.DataFrame]: A dictionary containing a DataFrame for active IPv6 routes.

    :Usage:
        ipv6_routes = get_netstat_ipv6_routing_data()
        active_routes_df = ipv6_routes["active_routes"]
    """
    return read_ipv6_routing_table(
            Popen(build_netstat_routing_table_command(), stdout=PIPE, shell=True).communicate()[0].decode("windows-1252", errors="ignore")
    )
#
#
#
#
def get_netstat_ipv4_routing_data():
    """
    Retrieves and parses IPv4 routing information using `netstat /r`.

    Returns:
        dict[str, pandas.DataFrame]: A dictionary containing DataFrames for active and persistent IPv4 routes.

    :Usage:
        ipv4_routes = get_netstat_ipv4_routing_data()
        active_routes_df = ipv4_routes["active_routes"]
        persistent_routes_df = ipv4_routes["persistent_routes"]
    """
    return read_ipv4_routing_table(
            Popen(build_netstat_routing_table_command(), stdout=PIPE, shell=True).communicate()[0].decode("windows-1252", errors="ignore")
    )
#
#
#
#
def get_netstat_interface_routing_data():
    """
    Retrieves and parses interface information using `netstat /r`.

    Returns:
        pandas.DataFrame: A DataFrame with MAC addresses and interface names.

    :Usage:
        interface_df = get_netstat_interface_routing_data()
    """
    return read_interface_routing_table(
            Popen(build_netstat_routing_table_command(), stdout=PIPE, shell=True).communicate()[0].decode("windows-1252", errors="ignore")
    )
#
#
#
#
def read_netstat_connections_list(cmd_output: str):
    """
    Parses the output of the `netstat` command with connection details.

    Args:
        cmd_output (str): The output string from `netstat`.

    Returns:
        pandas.DataFrame: A DataFrame containing the parsed connection information.

    :Usage:
        connections_df = read_netstat_connections_list(netstat_output)
    """
    lines = list(filter(None, cmd_output.splitlines()))

    headers = re.findall(r"(\w+(?: \(?\w+\)?)*)", lines[1])

    regex_line = []

    for header in headers:
        if header == "Proto":
            regex_line.append(r"(TCP|UDP|TCPv6|UDPv6)")
        elif header == "Local Address":
            regex_line.append(r"((?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\[::\]):\d{1,5})")
        elif header == "Foreign Address":
            regex_line.append(
                    r"((?:\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\[::\]|\*:\*):\d{1,5})"
            )
        elif header == "State":
            regex_line.append(
                    r"(LISTENING|ESTABLISHED|CLOSE_WAIT|TIME_WAIT|FIN_WAIT1|FIN_WAIT2|BOUND|)"
            )
        elif header == "PID":
            regex_line.append(r"(\d+)")
        elif header == "Time in State (ms)":
            regex_line.append(r"(\d+)")
        elif header == "Offload State":
            regex_line.append(r"(InHost|)")
        elif header == "Template":
            regex_line.append(r"(Not Applicable|Internet)")

    regex_line = r"\s+".join(regex_line)
    regex_line += r"(?:\n\s*(\w+))?(?:\n\s*\[([\w.]+)\])?\n"

    netstat_frame = pandas.DataFrame(
            re.findall(regex_line, "\n".join(lines[2:])),
            columns=headers + ["Component", "Executable"]
    )

    if all(x == "" for x in netstat_frame["Component"]):
        netstat_frame = netstat_frame.drop("Component", axis="columns")

    if all(x == "" for x in netstat_frame["Executable"]):
        netstat_frame = netstat_frame.drop("Executable", axis="columns")

    return netstat_frame
#
#
#
#
def get_netstat_connections_data(
        show_all_listening_ports: bool = False,
        show_all_ports: bool = False,
        show_offload_state: bool = False,
        show_templates: bool = False,
        show_connections_exe: bool = False,
        show_connections_FQDN: bool = False,
        show_connection_pid: bool = False,
        show_connection_time_spent: bool = False,
        protocol: Literal["TCP", "TCPv6", "UDP", "UDPv6"] = None
):
    """
    Retrieves and parses active connection information using `netstat`.

    Args:
        show_all_listening_ports (bool): Displays all listening ports. Defaults to False.
        show_all_ports (bool):  Displays all ports. Defaults to False.
        show_offload_state (bool): Shows the offload state. Defaults to False.
        show_templates (bool): Shows active TCP connections and the template used to create them. Defaults to False.
        show_connections_exe (bool): Displays the executable involved in creating each connection or listening port. Defaults to False.
        show_connections_FQDN (bool): Displays addresses and port numbers in fully qualified domain name (FQDN) format. Defaults to False.
        show_connection_pid (bool): Displays the process ID (PID) associated with each connection. Defaults to False.
        show_connection_time_spent (bool): Displays the amount of time, in seconds, since the connection was established. Defaults to False.
        protocol (Literal["TCP", "TCPv6", "UDP", "UDPv6"]): The protocol to filter connections by. If None, displays connections for all specified protocols. Defaults to None.

    Returns:
        pandas.DataFrame: A DataFrame containing the parsed connection information.

    :Usage:
        connections_df = get_netstat_connections_data(show_all_ports=True, protocol="TCP")
    """
    return read_netstat_connections_list(
            Popen(
                    build_netstat_connections_list_command(
                            show_all_listening_ports=show_all_listening_ports,
                            show_all_ports=show_all_ports,
                            show_offload_state=show_offload_state,
                            show_templates=show_templates,
                            show_connections_exe=show_connections_exe,
                            show_connections_FQDN=show_connections_FQDN,
                            show_connection_pid=show_connection_pid,
                            show_connection_time_spent=show_connection_time_spent,
                            protocol=protocol
                    ),
                    stdout=PIPE,
                    shell=True
            ).communicate()[0].decode("windows-1252", errors="ignore")
    )
#
#
#
#
def get_localhost_processes_with_pids():
    """
    Gets active processes and their associated ports on localhost.

    Returns:
        dict[int, list[int]]: A dictionary mapping PIDs to a list of their localhost ports.  {pid: [port1, port2, ...], ...}

    :Usage:
        processes_with_ports = get_localhost_processes_with_pids()
    """
    netstat_connections = get_netstat_connections_data(show_all_ports=True, show_connection_pid=True)
    netstat_connections = netstat_connections.loc[
        netstat_connections["Local Address"].apply(
                lambda address: re.search(r"\A(127\.0\.0\.1|\[::])", address) is not None
        )
    ]

    return netstat_connections.groupby(pandas.to_numeric(netstat_connections["PID"]))["Local Address"].apply(
            lambda local_addresses: list(
                    set(
                            int(re.search(r":(\d+)\Z", address).group(1)) for address in local_addresses
                    )
            )
    ).to_dict()
#
#
#
#
def get_localhost_beasy_ports():
    """
    Gets all busy ports on localhost.

    Returns:
        list[int]: A list of busy localhost ports.

	:Usage:
    	busy_ports = get_localhost_beasy_ports()
    """
    ports = get_netstat_connections_data(show_all_ports=True)

    return list(
            set(
                    ports.loc[
                        ports["Local Address"].apply(
                                lambda address: re.search(r"\A(127\.0\.0\.1|\[::])", address) is not None
                        )
                    ]["Local Address"].apply(lambda address: int(re.search(r":(\d+)", address).group(1))).tolist()
            )
    )
#
#
#
#
def get_localhost_free_ports():
    """
    Gets all free ports on localhost (1024-49150).

    Returns:
        list[int]: A list of free localhost ports.

    :Usage:
    	free_ports = get_localhost_free_ports()
    """
    beasy_ports = get_localhost_beasy_ports()
    return list(set(range(1024, 49151)) - set(beasy_ports))
#
#
#
#
def get_localhost_minimum_free_port(ports_to_check: int | list[int] | set = None):
    """
    Gets the minimum free port on localhost checking a specific port or set of ports first.

    Args:
        ports_to_check (int | list[int] | set): A single port, a list of ports, or a set of ports to check first. If None, defaults to finding the minimum free port in the range 1024-49150.

    Returns:
        int: The minimum free localhost port (or the first available port from `ports_to_check` if found).

    Raises:
        ValueError: If `ports_to_check` is a list or set containing non-integer values.

    :Usage:
        # Find the minimum free port from a list of desired ports
        min_free_port = get_localhost_minimum_free_port([8080, 8081, 8082])

        # Find the minimum free port overall
        min_free_port = get_localhost_minimum_free_port()
    """
    localhost_free_ports = get_localhost_free_ports()

    if isinstance(ports_to_check, int):
        return ports_to_check if ports_to_check in localhost_free_ports else min(localhost_free_ports)
    elif isinstance(ports_to_check, (list, set)):
        if not all(isinstance(port, int) for port in ports_to_check):
            raise ValueError("All ports must be int.")

        found_subset = set(ports_to_check) & set(localhost_free_ports)
        return min(found_subset) if found_subset else min(localhost_free_ports)
    else:
        return min(localhost_free_ports)
