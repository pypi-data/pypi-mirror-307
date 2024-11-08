from subprocess import Popen
from PyWindowsCMD.taskkill.command import cmd_taskkill_windows
#
#
#
#
def taskkill_windows(
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
    """
    Popen(cmd_taskkill_windows(s, u, p, fi, pid, im, t, f), shell=True)
