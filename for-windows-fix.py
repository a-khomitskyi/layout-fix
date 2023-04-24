import win32serviceutil
import win32service
import win32event
import servicemanager
import keyboard
import pyperclip


class LayoutConverterService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'LayoutConverter'
    _svc_display_name_ = 'Layout Converter Service'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        keyboard.add_hotkey('ctrl+alt+u', self.convert_to_ukr)
        keyboard.add_hotkey('ctrl+alt+e', self.convert_to_en)
        keyboard.wait(self.stop_event)

    def convert_layout(self, input_text, layout):
        en_to_ukr = {
            'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з',
            '[': 'х', ']': 'ї', 'a': 'ф', 's': 'і', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л',
            'l': 'д', ';': 'ж', "'": 'є', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь',
            ',': 'б', '.': 'ю', '/': '.'
        }
        ukr_to_en = {v: k for k, v in en_to_ukr.items()}
        output_text = ''
        mapping = en_to_ukr if layout == 'en' else ukr_to_en
        for char in input_text:
            if char.lower() in mapping:
                output_text += mapping[char.lower()].upper() if char.isupper() else mapping[char.lower()]
            else:
                output_text += char
        return output_text

    def convert_to_ukr(self):
        pyperclip.copy(self.convert_layout(pyperclip.paste(), 'en'))

    def convert_to_en(self):
        pyperclip.copy(self.convert_layout(pyperclip.paste(), 'ukr'))


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(LayoutConverterService)
