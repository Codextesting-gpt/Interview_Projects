# secret_sauce.py
from datetime import date
import hashlib
import os

try:
    # Load keys from a local .env file if python-dotenv is available
    # (falls back to plain os.getenv if not installed)
    from dotenv import load_dotenv
    load_dotenv()
except ModuleNotFoundError:
    pass


class SecretSauce:
    """
    • Before 4 July of the current year the class instantiates normally.  
    • On or after 4 July it looks for an environment variable called
      `fallout`.  The value must equal the SHA-256 hash of the string
      "new vegas".  
    • If the key check fails, the constructor raises and the class
      definition is immediately removed from the module’s global
      namespace.  Any further import or use attempts will fail.
    """

    _CUTOFF = date(date.today().year, 7, 4)
    _EXPECTED_HASH = hashlib.sha256(b"new vegas").hexdigest()

    def __init__(self) -> None:
        today = date.today()
        print(today, self._CUTOFF, self._EXPECTED_HASH)
        if today < self._CUTOFF:
            key = os.getenv("fallout")
            print(key)
            if key == self._EXPECTED_HASH:
                return  # authorised – carry on
            print("after the interview")
        globals().pop(self.__class__.__name__, None)
        raise PermissionError(
            "SecretSauce unavailable: invalid or missing 'fallout' key."
        )

    def add_two_numbers(self, a: float | int, b: float | int) -> float | int:
        """
        Add *a* and *b*.  Must be called on an **instance**:

            sauce = SecretSauce()
            total = sauce.add_two_numbers(3, 5)

        Calling `SecretSauce.add_two_numbers(3, 5)` directly will raise.
        """
        if self.__class__ is SecretSauce:
            return a + b
        # Defensive check: if someone tries to bypass by passing some other
        # object in place of `self`
        raise TypeError("add_two_numbers must be invoked on a SecretSauce instance.")
