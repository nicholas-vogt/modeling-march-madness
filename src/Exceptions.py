class Error(Exception):
   """Base class for other exceptions"""
   pass

class OverwriteError(Error):
   """Raised when the user tries to overwrite an existing file."""
   pass
