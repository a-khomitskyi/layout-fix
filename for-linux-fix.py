import keyboard
import pyperclip
import time
import logging
import sys
import os

from systemd.daemon import notify
from systemd.journal import JournalHandler


class LayoutConverterService:
    def __init__(self):
        self.running = True

    def start(self):
        logging.info('LayoutConverter started')
        keyboard.add_hotkey('ctrl+alt+u', self.convert_to_ukr)
        keyboard.add_hotkey('ctrl+alt+e', self.convert_to_en)
        while self.running:
            notify('READY=1')
            time.sleep(1)

    def stop(self):
        logging.info('LayoutConverter stopped')
        self.running = False

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
    # Setup logging to the systemd journal
    log_handler = JournalHandler()
    log_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
    logging.basicConfig(handlers=[log_handler], level=logging.INFO)

    # Start the service
    service = LayoutConverterService()

    if len(sys.argv) > 1 and sys.argv[1] == 'start':
        service.start()
    elif len(sys.argv) > 1 and sys.argv[1] == 'stop':
        service.stop()
    else:
        print(f'Usage: {os.path.basename(sys.argv[0])} <start|stop>')
        sys.exit(1)
