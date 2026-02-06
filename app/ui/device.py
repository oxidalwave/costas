import epaper


class EpdDevice:
    def __init__(self, display_code: str):
        self._display_code = display_code
        self._epd = epaper.epaper(display_code).EPD()

    @property
    def width(self) -> int:
        return self._epd.width

    @property
    def height(self) -> int:
        return self._epd.height

    def init(self) -> None:
        self._epd.init()

    def init_fast(self) -> None:
        if hasattr(self._epd, "init_fast"):
            self._epd.init_fast()
        else:
            self._epd.init()

    def clear(self) -> None:
        self._epd.Clear()

    def display(self, image) -> None:
        self._epd.display(self._epd.getbuffer(image))

    def cleanup(self) -> None:
        epaper.epaper(self._display_code).epdconfig.module_exit(cleanup=True)
