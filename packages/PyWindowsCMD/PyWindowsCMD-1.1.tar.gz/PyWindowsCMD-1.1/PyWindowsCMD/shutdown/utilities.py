from PyWindowsCMD.errors import WrongCommandLineParameter
from PyVarTools.python_instances_tools import get_class_fields
#
#
#
#
class ShutdownType:
	display_gui = "/i"
	logoff = "/l"
	shutdown = "/s"
	shutdown_with_sign_in_on_boot = "/sg"
	restart = "/r"
	restart_with_sign_in_on_boot = "/g"
	abort_shutting_down = "/a"
	shutdown_without_warning = "/p"
	hibernate = "/h"
#
#
#
#
class ShutdownReasonType:
	planned = "P:"
	user_defined = "U:"
	unplanned = ""
#
#
#
#
class ShutdownReason:
	def __init__(
			self,
			reason_type: str = "",
			major_reason_number: int = 0,
			minor_reason_number: int = 0
	):
		"""
		Class for parameter "d" for shutdown command. \n
		:param reason_type: indicates that the restart or shutdown is planned or user defined. If neither "p" nor "u" is specified the restart or shutdown is unplanned.
		:param major_reason_number: is the major reason number. Acceptable range: [0;255]
		:param minor_reason_number: is the minor reason number. Acceptable range: [0;65535]
		"""
		if reason_type not in get_class_fields(ShutdownReasonType).values():
			raise WrongCommandLineParameter("Unknown shutdown type (%s)" % str(reason_type))
		#
		#
		#
		#
		if not (0 <= major_reason_number <= 255):
			raise WrongCommandLineParameter(
					"Major reason number of shutdown or reboot has to be in range [0;255]"
			)
		#
		#
		#
		#
		if not (0 <= minor_reason_number <= 65535):
			raise WrongCommandLineParameter(
					"Minor reason number of shutdown or reboot has to be in range [0;65535]"
			)
		#
		#
		#
		#
		self.reason_type = reason_type
		self.major_reason_number = major_reason_number
		self.minor_reason_number = minor_reason_number
	#
	#
	#
	#
	def get_command(self):
		return f"/d {self.reason_type}{self.major_reason_number}:{self.minor_reason_number}"
