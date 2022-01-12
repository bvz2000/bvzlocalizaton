"""
Description
------------------------------------------------------------------------------------------------------------------------
localization is an object that connects to a localized text file that maps error codes to error strings, and text codes
to messages.

The format of a localized resources file is that of an ini file. Its name is in the form:

<custom_name>_<language>.ini

Where custom_name is any name your program wants to use, and language represents the language to use. You need one file
per language you wish to localize your app in.

Tho localization file has two sections (error_codes and messages) in the format:

[error_codes]
101=This is error 101
102=This is error 102

[messages]
hello=Hello world.
do_quit=Do you really want to quit?

It also has the ability to manage variables and color formatting. Colors may be inserted into either error codes or
message with the format: {{COLOR_NAME}}. Variables are formatted as {variable_name}. So if you wanted a
message that said (in all red) "Your name is Bob" and Bob was passed as a variable, then the message string could look
like this:

msg={{COLOR_RED}}Your name is {name}{{COLOR_NONE}}

(do not forget to turn off the color with {{COLOR_NONE}} at the end or your next text will still be the same color)

An example of usage:

Assuming a resource file that looks like the following:

[error codes]
101=This is a sample error code with a variable called {replace_me}

The following code shows how to use this system:

localized_resource_obj = LocalizedResource("/path/to/resource/", "myapp", "english")
msg = localized_resource_obj.get_error_msg(101)
msg = msg.format(replace_me="some text to fill into the replace_me variable")
"""

import configparser
import os

from bvzlocalizationerror import LocalizationError


# define some colors
# ----------------------------------------------------------------------------------------------------------------------
BLACK = '\033[30m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
WHITE = '\033[37m'
BRIGHT_RED = '\033[91m'
BRIGHT_GREEN = '\033[92m'
BRIGHT_YELLOW = '\033[93m'
BRIGHT_BLUE = '\033[94m'
BRIGHT_MAGENTA = '\033[95m'
BRIGHT_CYAN = '\033[96m'
BRIGHT_WHITE = '\033[97m'
ENDC = '\033[0m'


# ======================================================================================================================
class LocalizedResource(configparser.SafeConfigParser):
    """
    A Class to manage the localized resources file. Subclassed from the default python config parser. Note, all error
    messages are presented in English because by definition no language file has been loaded yet.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, resources_d, prefix, language="english"):
        """
        Setup this subclass of the default python config parser.

        :param resources_d:
                The directory where the localized resources files are stored.
        :param prefix:
                The prefix for the resources file. For example, if you want to read the "squirrel_english.ini" localized
                resources file, the prefix would be: "squirrel". Required.
        :param language:
                The language to use when parsing the resources file. If no language is supplied, defaults to "english".

        :return:
                Nothing.
        """

        assert type(resources_d) is str

        if not os.path.exists(resources_d):
            raise LocalizationError(f"Resources directory {resources_d} does not exist.")

        configparser.SafeConfigParser.__init__(self, allow_no_value=True)

        self.resources_d = resources_d
        self.resources_n = prefix + "_" + language + ".ini"
        self.resources_p = os.path.join(self.resources_d, self.resources_n)
        self._read_resources()

    # ------------------------------------------------------------------------------------------------------------------
    def _read_resources(self):
        """
        Opens up the appropriate localized resource .ini file and reads its contents.

        :return:
                Nothing.
        """

        # If this file does not exist, warn the user and bail. Since we cannot find a language yet, report the error in
        # English.
        if not os.path.exists(self.resources_p):
            msg = "Cannot locate resource file: " + os.path.abspath(self.resources_p)
            code = 1
            raise LocalizationError(msg, code)

        # Open and populate the resources object
        self.read(self.resources_p)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _format_string(msg):
        """
        Given a string (msg) this will format it with colors based on the {{COLOR}} tags. (example {{COLOR_RED}}). It
        will also convert literal \n character string into a proper newline.

        :param msg:
                The string to format.

        :return:
                The formatted string.
        """

        assert type(msg) is str

        output = msg.replace(r"\n", "\n")

        output = output.replace("{{COLOR_BLACK}}", BLACK)
        output = output.replace("{{COLOR_RED}}", RED)
        output = output.replace("{{COLOR_GREEN}}", GREEN)
        output = output.replace("{{COLOR_YELLOW}}", YELLOW)
        output = output.replace("{{COLOR_BLUE}}", BLUE)
        output = output.replace("{{COLOR_MAGENTA}}", MAGENTA)
        output = output.replace("{{COLOR_CYAN}}", CYAN)
        output = output.replace("{{COLOR_WHITE}}", WHITE)
        output = output.replace("{{COLOR_BRIGHT_RED}}", BRIGHT_RED)
        output = output.replace("{{COLOR_BRIGHT_GREEN}}", BRIGHT_GREEN)
        output = output.replace("{{COLOR_BRIGHT_YELLOW}}", BRIGHT_YELLOW)
        output = output.replace("{{COLOR_BRIGHT_BLUE}}", BRIGHT_BLUE)
        output = output.replace("{{COLOR_BRIGHT_MAGENTA}}", BRIGHT_MAGENTA)
        output = output.replace("{{COLOR_BRIGHT_CYAN}}", BRIGHT_CYAN)
        output = output.replace("{{COLOR_BRIGHT_WHITE}}", BRIGHT_WHITE)
        output = output.replace("{{COLOR_NONE}}", ENDC)

        return output

    # ------------------------------------------------------------------------------------------------------------------
    def get_error_msg(self, code):
        """
        Extracts the error message associated with the code.

        :param code:
                The code for the error message.

        :return:
                The string associated with this code.
        """

        assert type(code) is str or type(code) is int

        if not self.has_section("error_codes"):
            msg = f"Localization file {self.resources_p} is corrupt: It is missing the error_codes section."
            raise LocalizationError(msg, 2)

        if not self.has_option("error_codes", str(code)):
            msg = f"Localization file {self.resources_p} is corrupt: It is missing the error_code: {code}."
            raise LocalizationError(msg, 3)

        msg = self.get("error_codes", str(code))
        msg = self._format_string(msg)

        return msg

    # ------------------------------------------------------------------------------------------------------------------
    def get_msg(self, message_key):
        """
        Extracts the message associated with the key.

        :param message_key:
                The key for the message.

        :return:
                A string.
        """

        assert type(message_key) is str

        if not self.has_section("messages"):
            msg = f"Localization file {self.resources_p} is corrupt: It is missing the messages section."
            raise LocalizationError(msg, 4)

        if not self.has_option("messages", str(message_key)):
            msg = f"Localization file {self.resources_p} is corrupt: It is missing the message: {message_key}."
            raise LocalizationError(msg, 5)

        msg = self.get("messages", str(message_key))
        msg = self._format_string(msg)

        return msg
