"""Telnet Options handler module"""
SB = b'\xfa'
SE = b'\xf0'
WILL = b'\xfb'
WONT = b'\xfc'
DO = b'\xfd'
DONT = b'\xfe'
IAC = b'\xff'
GA = b'\xf9'

class TelnetOption():
    """Base class for Telnet Option handling"""
    code: int = 0
    name: str = "TelnetOption"

    def __init__(self, code: int):
        pass

    def do(self) -> None:
        """IAC DO handler"""

    def dont(self) -> None:
        """IAC DONT handler"""

    def will(self) -> None:
        """IAC WILL handler"""

    def wont(self) -> None:
        """IAC WONT handler"""

    def sb(self, sb):
        """IAC SB handler"""
