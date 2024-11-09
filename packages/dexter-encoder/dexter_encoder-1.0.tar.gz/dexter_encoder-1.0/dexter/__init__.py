# __init__.py

from .dexter import Dexter

# Create a default instance of Dexter for convenience
_default_dexter = Dexter()

# Expose encode and decode as module-level functions
encode = _default_dexter.encode
decode = _default_dexter.decode

# Define what’s accessible when importing the package
__all__ = ["Dexter", "encode", "decode"]
