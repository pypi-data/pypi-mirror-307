import time
from .gautomator import GAClient
from .core._types import By, Context
from .core._exceptions import *


KEY_W = 87
KEY_A = 65
KEY_D = 68
KEY_S = 83


class GATest:
    def __init__(self, client: GAClient) -> None:
        self._client = client

    def _sleep(self, timeout: float = 0.2):
        time.sleep(timeout)

    def screenshots(self, num: int = 1):
        for i in range(num):
            self._client.screenshot(time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime()))
            self._sleep()

    def print_page_source(self, context: Context = Context.Slate):
        print(self._client.page_source(context=context))
        self._sleep()

    def click_play(self):
        try:
            self._client.find_element(Context.Slate, By.text, "Play").click()
            return
        except NoSuchElementException:
            pass
        try:
            self._client.find_element(Context.Slate, By.text, "运行").click()
            return
        except NoSuchElementException:
            pass
        raise NoSuchElementException('Cannot find <"Play"> or <"运行"> by text')

    def click_skip(self):
        skip_btn = self._client.find_element(Context.Umg, By.name, "SkipLabel")
        skip_btn.click()

    def start_game(self):
        self.click_play()
        self._sleep(2)
        self.click_skip()
        self._sleep(1)

    def move_forward(self, hover: float) -> None:
        self._client.key(KEY_W, hover)

    def move_back(self, hover: float) -> None:
        self._client.key(KEY_S, hover)

    def move_left(self, hover: float) -> None:
        self._client.key(KEY_A, hover)

    def move_right(self, hover: float) -> None:
        self._client.key(KEY_D, hover)

    def left_mouse_click(self, hover: float) -> None:
        self._client.key(1, hover)

    def right_mouse_click(self, hover: float) -> None:
        self._client.key(2, hover)

    def test_actor(self):
        print(self._client.location)
        self._client.set_location = (1480.484375, 145.146484375, 880.149658203125)
        self._sleep(1)
        self._client.yaw = 10
        self._client.roll = 10
        self._client.pitch = 10
        print(self._client.rotation)

    def test_exec_cmd(self):
        time.sleep(1)
        print(self._client.exec_console_cmd("lua.dofile myunlua"))
