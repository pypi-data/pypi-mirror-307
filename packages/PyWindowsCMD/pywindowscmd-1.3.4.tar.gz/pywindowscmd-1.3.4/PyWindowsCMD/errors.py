class WrongCommandLineParameter(Exception):
    """
    Custom exception raised when an invalid command-line parameter is provided.

    :Usage:
        raise WrongCommandLineParameter("Invalid value for --option")
    """
    #
    #
    #
    #
    def __init__(self, message):
        """
        Initializes the WrongCommandLineParameter exception.

        Args:
            message (str): The error message to store.

        :Usage:
            raise WrongCommandLineParameter("Invalid input")
        """
        super().__init__(message)
