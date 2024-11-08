from PyWindowsCMD.utilities import count_parameters
from PyWindowsCMD.errors import WrongCommandLineParameter
#
#
#
#
def cmd_taskkill_windows(
        s: str = None,
        u: str = None,
        p: str = None,
        fi: str | list[str] = None,
        pid: int | list[int] = None,
        im: str | list[str] = None,
        t: bool = False,
        f: bool = False
):
    """
    Windows CMD command to terminate tasks of the computer. \n
    [/s system [/u username [/p password]]] { [/FI filter] [/PID processid | /IM imagename] } [/T] [/F]
    :param s: specifies the remote system to connect to.
    :param u: specifies the user context under which the command should execute.
    :param p: specifies the password for the given user context. Prompts for input if omitted.
    :param fi: applies a filter to select a set of tasks. Allows "*" to be used.
    :param pid: specifies the PID of the process to be terminated. Use TaskList to get the PID.
    :param im: specifies the image name of the process to be terminated. Wildcard "*" can be used to specify all tasks or image names.
    :param t: terminates the specified process and any child processes which were started by it.
    :param f: specifies to forcefully terminate the process(es).
    :return: CMD command to use. Type str
    """
    if count_parameters(s, u, p, fi, pid, im, t, f) == 0:
        raise WrongCommandLineParameter("Function called with no parameters.")

    if u and not s:
        raise WrongCommandLineParameter("\"taskkill\" command has to have \"u\" parameter with parameter \"s\".")

    if p and not u:
        raise WrongCommandLineParameter("\"taskkill\" command has to have \"p\" parameter with parameter \"u\".")

    if t and f:
        raise WrongCommandLineParameter("Parameters \"t\" and \"f\" are incompatible.")

    commands = ["taskkill"]

    if s:
        commands.append("/s %s" % s)

    if u:
        commands.append("/u %s" % u)

    if p:
        commands.append("/p %s" % p)

    if fi:
        if type(fi) == str:
            commands.append("/fi \"%s\"" % fi)
        elif type(fi) == list:
            for fi_ in fi:
                commands.append("/fi \"%s\"" % fi_)

    if pid:
        if type(pid) == int:
            commands.append("/pid %d" % pid)
        elif type(pid) == list:
            for pid_ in pid:
                commands.append("/pid %d" % pid_)

    if im:
        if type(im) == str:
            commands.append("/im %s" % im)
        elif type(im) == list:
            for im_ in im:
                commands.append("/im %s" % im_)

    if t:
        commands.append("/t")

    if f:
        commands.append("/f")

    return " ".join(commands)
