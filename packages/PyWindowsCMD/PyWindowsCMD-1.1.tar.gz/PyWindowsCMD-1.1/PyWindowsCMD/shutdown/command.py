from PyVarTools.python_instances_tools import get_class_fields
from PyWindowsCMD.utilities import count_parameters
from PyWindowsCMD.shutdown.utilities import ShutdownReason, ShutdownType
from PyWindowsCMD.errors import WrongCommandLineParameter
#
#
#
#
def cmd_shutdown_windows(
        shutdown_type: str,
        prepare_for_fast_startup: bool = False,
        fw: bool = False,
        document_reason_of_shutdown: bool = False,
        open_advanced_boot_options_menu: bool = False,
        target_computer: str = None,
        time_out_period: int = 30,
        force_running_applications_to_close: bool = False,
        shutdown_reason: ShutdownReason = None,
        comment: str = ""
):
    """
    Windows CMD command for shutdown or restart the computer. \n
    The "SHUTDOWN" command is used to end the user's session, restart the computer, put it into sleep mode, or turn off the power. \n
    [ /i | /l | /s | /sg | /r | /g | /a | /p | /h | /e | /o ] [/hybrid] [/soft] [/fw] [/f] [/m \\computer] [/t xxx] [/d [p|u]xx:yy [/c "comment"]]
    :param shutdown_type:
    :param prepare_for_fast_startup: performs a shutdown of the computer and prepares it for fast startup. Must be used with "s" option.
    :param fw: combine with a shutdown option to cause the next boot to go to the firmware user interface.
    :param document_reason_of_shutdown: document the reason for an unexpected shutdown of a computer.
    :param open_advanced_boot_options_menu: go to the advanced boot options menu and restart the computer. Must be used with "r" parameter.
    :param target_computer: specify the target computer (IPv4).
    :param time_out_period: set the time-out period before shutdown to xxx seconds. The valid range is 0-315360000 (10 years), with a default of 30. If the timeout period is greater than 0, the "f" parameter is implied.
    :param force_running_applications_to_close: force running applications to close without forewarning users. The "f" parameter is implied when a value greater than 0 is specified for the "t" parameter.
    :param shutdown_reason: provide the reason for the restart or shutdown.
    :param comment: reason comment. Maximum of 512 characters allowed.
    :return: CMD command to use.
    :rtype: str
    """
    if count_parameters(shutdown_type, prepare_for_fast_startup, fw, document_reason_of_shutdown, open_advanced_boot_options_menu, target_computer, time_out_period, force_running_applications_to_close, shutdown_reason,  comment) == 0:
        raise WrongCommandLineParameter("Function called with no parameters.")

    if shutdown_type not in get_class_fields(ShutdownType).values():
        raise WrongCommandLineParameter("Unknown shutdown type (%s)" % str(shutdown_type))

    if prepare_for_fast_startup and shutdown_type != ShutdownType.shutdown:
        raise WrongCommandLineParameter("\"hybrid\" parameter used only with \"s\" parameter.")

    if open_advanced_boot_options_menu and shutdown_type != ShutdownType.restart:
        raise WrongCommandLineParameter("\"shutdown\" command has to have \"r\" parameter with parameter \"o\".")

    if shutdown_type == ShutdownType.abort_shutting_down and count_parameters(document_reason_of_shutdown, open_advanced_boot_options_menu, target_computer, force_running_applications_to_close, shutdown_reason) > 0:
        raise WrongCommandLineParameter("Parameter \"a\" has to be alone or with parameter \"fw\".")

    if shutdown_type == ShutdownType.logoff and (target_computer or shutdown_reason):
        raise WrongCommandLineParameter(
                "\"shutdown\" command can't have \"m\" or \"d\" parameters with parameter \"l\"."
        )

    if not (0 <= time_out_period <= 315360000):
        raise WrongCommandLineParameter("Wrong timeout. It has to be in range [0;315360000].")
    elif force_running_applications_to_close and time_out_period == 0:
        raise WrongCommandLineParameter("\"f\" parameter has to be used only with parameter \"t\" > 0.")

    commands = ["shutdown", shutdown_type]

    if prepare_for_fast_startup:
        commands.append("/hybrid")

    if fw:
        commands.append("/fw")

    if document_reason_of_shutdown:
        commands.append("/e")

    if open_advanced_boot_options_menu:
        commands.append("/o")

    if target_computer:
        commands.append(f"/m \\\\{target_computer}")

    if time_out_period:
        commands.append(f"/t {time_out_period}")

    if force_running_applications_to_close:
        commands.append("/f")

    if shutdown_reason:
        commands.append(shutdown_reason.get_command())

    if bool(comment):
        commands.append(f"/c \"{comment}\"")

    return " ".join(commands)
