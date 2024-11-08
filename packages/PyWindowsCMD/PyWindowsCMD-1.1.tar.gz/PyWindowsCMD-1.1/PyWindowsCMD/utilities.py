from re import search
#
#
#
#
def count_parameters(*args):
    return len(list(filter(lambda x: bool(x), [*args])))
#
#
#
#
def check_ip_is_localhost(ip: str):
    return True if search(r"\A127\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}\Z", ip) else False
#
#
#
#
def get_port_from_ipv4(ipv4: str):
    return int(search(r"\A\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:(\d{1,5})\Z", ipv4).group(1))
