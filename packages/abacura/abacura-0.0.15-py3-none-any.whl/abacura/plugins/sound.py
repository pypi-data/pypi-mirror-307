"""
Handle MSP
"""


from abacura.mud import OutputMessage
from abacura.plugins import Plugin, action


class SoundPlugin(Plugin):
    """Handle MSP sound"""
    @action(r'^!!SOUND\((.*)\)')
    def msp(self, wav: str, msg: OutputMessage):
        msg.gag = True

        try:
            from playsound import playsound
        except ModuleNotFoundError as exc:
            pkg = 'pip install playsound PyGObject'
            self.session.show_warning(f"Unable to play sounds without playsound module. Use '{pkg}' ")
            return

        if not self.config.get_specific_option(self.session.name, 'sound_dir', None):
            return
        try:
            playsound(f"{self.config.get_specific_option(self.session.name, 'sound_dir')}/{wav}", block=False)
        except Exception as exc:
            self.session.show_exception(exc, msg=f"Failure to play sound {wav}: {repr(exc)}", show_tb=False)

        # return msg
