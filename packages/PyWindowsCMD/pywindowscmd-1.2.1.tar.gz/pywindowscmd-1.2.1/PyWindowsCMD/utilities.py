from re import search
#
#
#
#
def count_parameters(*args):
    """
    Counts the number of non-empty parameters passed to the function.

    Args:
        *args: Variable number of arguments of any type.

    Returns:
        int: The number of non-empty arguments.

    :Usage:
        count = count_parameters(1, "", "hello", None, [], 0)  # Returns 2
    """
    return len(list(filter(lambda x: bool(x), [*args])))
#
#
#
#
def check_ip_is_localhost(ip: str):
    """
    Checks if the given IP address string represents a localhost address (127.0.0.0/8).

    Args:
        ip (str): The IP address string in the format "127.x.x.x:port".

    Returns:
        bool: True if the IP is a localhost address, False otherwise.

    :Usage:
        is_localhost = check_ip_is_localhost("127.0.0.1:8080")  # Returns True
        is_localhost = check_ip_is_localhost("192.168.1.1:80")  # Returns False
    """
    return True if search(r"\A127\.0\.0\.1:\d{1,5}\Z", ip) else False
#
#
#
#
def get_port_from_ipv4(ipv4: str):
    """
    Extracts the port number from an IPv4 address string.

    Args:
        ipv4 (str):  The IPv4 address string in the format "x.x.x.x:port".

    Returns:
        int: The port number as an integer.

    Raises:
        AttributeError: If the input string does not match the expected format.

    :Usage:
        port = get_port_from_ipv4("192.168.1.1:8080")  # Returns 8080
    """
    return int(search(r"\A\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:(\d{1,5})\Z", ipv4).group(1))
