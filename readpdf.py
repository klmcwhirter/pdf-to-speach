from contextlib import contextmanager
import sys

import pdfplumber
import pyttsx3


@contextmanager
def read_pdf(file):
    with pdfplumber.open(file) as pdf:
        yield pdf


@contextmanager
def sttengine(rate=None, volume=None, voice=None):
    try:
        engine = pyttsx3.init()
        if rate:
            engine.setProperty('rate', rate)     # setting up new voice rate
        if volume:
            engine.setProperty('volume', volume)    # setting up volume level  between 0 and 1
        if voice:
            engine.setProperty('voice', voice)

        yield engine

    finally:
        engine.runAndWait()
        engine.stop()


def main(file='rtl-sdr.pdf', page_num=16):
    with sttengine(rate=150, voice='english-us') as engine:
        with read_pdf(file) as pdf:
            page = pdf.pages[page_num]
            text = page.extract_text()
            print(text)
            engine.say(text)


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
