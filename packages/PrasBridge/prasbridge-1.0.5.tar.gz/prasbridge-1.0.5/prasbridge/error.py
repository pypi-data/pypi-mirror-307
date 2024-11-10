"""Error handling for PRAS"""

def pWarning(message, category, filename, lineno, file=None, line=None):
    return f"\033[1;38;5;214mPRAS:\033[0m {message}\n"


class pError(Exception):
    def __init__(self, message):
        super().__init__(self.format_message(message))

    def format_message(self, message):
        return f"PRAS: {message}\n"  