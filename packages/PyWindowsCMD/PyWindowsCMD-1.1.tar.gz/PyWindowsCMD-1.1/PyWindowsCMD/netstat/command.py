from PyWindowsCMD.utilities import count_parameters
from PyWindowsCMD.errors import WrongCommandLineParameter
#
#
#
#
def cmd_netstat_windows(
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
        x: bool = False
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
    :return: CMD command to use. Type str
    """
    if count_parameters(a, b, e, f, i, n, o, p, r, s, t, x) == 0:
        raise WrongCommandLineParameter("Function called with no parameters.")

    if x and count_parameters(a, b, e, f, i, n, o, p, r, s, t) > 0:
        raise WrongCommandLineParameter("Parameter \"x\" has to be alone.")

    if (e or r or s) and count_parameters(a, b, f, i, n, o, p, t, x) > 0:
        raise WrongCommandLineParameter("Parameters \"e\", \"r\" or/and \"s\" have to be used without other parameters.")

    if i and p:
        raise WrongCommandLineParameter("Parameters \"i\" and \"p\" are incompatible.")

    if i and o:
        raise WrongCommandLineParameter("Parameters \"i\" and \"o\" are incompatible.")

    if p:
        if not s and p not in ["TCP", "UDP", "TCPv6", "UDPv6"]:
            raise WrongCommandLineParameter("Wrong protocol.")
        elif s and p not in ["TCP", "TCPv6", "UDP", "UDPv6", "IP", "IPv6", "ICMP", "ICMPv6"]:
            raise WrongCommandLineParameter("Wrong protocol.")
        elif count_parameters(a, b, e, f, i, n, o, r, s, t, x) == 0:
            raise WrongCommandLineParameter("Parameter \"p\" cannot be used without other parameters.")

    if count_parameters(a, b, e, f, i, n, o, p, r, s, t, x) == count_parameters(a, f, i, o, t):
        raise WrongCommandLineParameter(
                "Parameters \"a\", \"f\", \"i\", \"o\" or/and \"t\" have to be used with other parameters, because alone they produce infinite output."
        )

    commands = ["netstat"]

    if a:
        commands.append("/a")

    if b:
        commands.append("/b")

    if e:
        commands.append("/e")

    if f:
        commands.append("/f")

    if i:
        commands.append("/i")

    if n:
        commands.append("/n")

    if o:
        commands.append("/o")

    if p:
        commands.append("/p %s" % p)

    if r:
        commands.append("/r")

    if s:
        commands.append("/s")

    if t:
        commands.append("/t")

    if x:
        commands.append("/x")

    return " ".join(commands)
