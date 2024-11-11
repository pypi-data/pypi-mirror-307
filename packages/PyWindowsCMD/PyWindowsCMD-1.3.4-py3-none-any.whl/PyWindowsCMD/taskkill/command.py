from PyWindowsCMD.utilities import count_parameters
from PyWindowsCMD.errors import WrongCommandLineParameter
from PyVarTools.python_instances_tools import get_class_fields
from PyWindowsCMD.taskkill.parameters import ImageName, ProcessFilter, ProcessID, RemoteSystem, TaskKillTypes
#
#
#
#
def build_taskkill_command(
        taskkill_type: str,
        remote_system: RemoteSystem = None,
        selectors: ProcessFilter | ProcessID | ImageName | list[ProcessFilter | ProcessID | ImageName] = None
):
    """
    Constructs a Windows CMD command for terminating processes using `taskkill`.

    Args:
        taskkill_type (str): The type of termination to perform (e.g., "/F" for forceful termination). See `TaskKillType` for options.
        remote_system (RemoteSystem): Specifies a remote system to execute the command on. Defaults to None.
        selectors (ProcessFilter | ProcessID | ImageName | list[ProcessFilter | ProcessID | ImageName]):  One or more selectors to identify processes to terminate. Defaults to None.

    Returns:
        str: The constructed `taskkill` command string.

    Raises:
        WrongCommandLineParameter: If invalid parameter combinations or values are provided.

    Usage:
        command = cmd_taskkill_windows(TaskKillType.force, selectors=ImageName("notepad.exe"))
        command = cmd_taskkill_windows(TaskKillType.force, remote_system=RemoteSystem("192.168.1.100"), selectors=[ProcessID(1234), ProcessID(5678)])
    """
    if count_parameters(taskkill_type, remote_system, selectors) == 0:
        raise WrongCommandLineParameter("Function called with no parameters.")

    if taskkill_type not in get_class_fields(TaskKillTypes).values():
        raise WrongCommandLineParameter(
                f"Invalid taskkill type parameter. Valid types {list(get_class_fields(TaskKillTypes).values())}"
        )

    commands = ["taskkill"]

    if remote_system is not None:
        commands.append(remote_system.get_command())

    if selectors is not None:
        if type(selectors) == list:
            for selector in selectors:
                commands.append(selector.get_command())
        else:
            commands.append(selectors.get_command())

    commands.append(taskkill_type)

    return " ".join(commands)
