import win32gui
import win32con
import pygame
import pystray
import sys
from datetime import datetime
from dateutil.parser import parse
from threading import Event, Thread
from windows_toasts import Toast, InteractableWindowsToaster

pygame.font.init()
pygame.mixer.init()

COUNTDOWN_TIMER = 1200  # seconds

SMALL_FONT = pygame.font.SysFont("comicsans", 100)
BIG_FONT = pygame.font.SysFont("comicsans", 250)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (30, 30, 30)
exit_event = Event()
last_rest = ""
first_run = True
paused_seconds = 0

paused = False
gamer = False

toaster = InteractableWindowsToaster(" - your eyerest xoxo")


def draw(timer, timerPos):
    WIN.fill(DARK_GRAY)
    WIN.blit(timer, timerPos)
    pygame.display.update()


def drawTimer(timerValue, font):
    global running
    clock = pygame.time.Clock()

    timer = font.render(str(timerValue), True, LIGHT_GRAY)

    halfTimerWidth, halfTimerHeight = timer.get_size()
    halfTimerHeight /= 2
    halfTimerWidth /= 2

    timerPos = [HALF_WIDTH - halfTimerWidth, HALF_HEIGHT - halfTimerHeight]

    draw(timer, timerPos)

    running = True
    while running:
        clock.tick(1)

        for event in pygame.event.get():
            # if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #     running = False
            if event.type == pygame.QUIT:
                pass

        timerValue -= 1
        timer = font.render(str(timerValue), True, LIGHT_GRAY)
        timerPos[0] = HALF_WIDTH - timer.get_width() / 2

        if timerValue == 0:
            break

        draw(timer, timerPos)

    pygame.display.quit()

    if running:
        return True

    return False


def main():
    global first_run, last_rest, paused, HALF_WIDTH, HALF_HEIGHT, WIN

    while not exit_event.is_set():
        if not first_run:
            WIN = pygame.display.set_mode((150, 150), pygame.NOFRAME)
            HALF_WIDTH, HALF_HEIGHT = 75, 75

            win32gui.SetWindowPos(
                pygame.display.get_wm_info()["window"],
                win32con.HWND_TOPMOST,
                0,
                0,
                0,
                0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
            )

            if not drawTimer(10, SMALL_FONT):
                exit_event.wait(COUNTDOWN_TIMER)
                continue

            WIN = pygame.display.set_mode((0, 0))
            WIDTH, HEIGHT = WIN.get_size()
            HALF_WIDTH, HALF_HEIGHT = WIDTH / 2, HEIGHT / 2

            win32gui.SetWindowPos(
                pygame.display.get_wm_info()["window"],
                win32con.HWND_TOPMOST,
                0,
                0,
                0,
                0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
            )

            drawTimer(20, BIG_FONT)
        else:
            first_run = False

        last_rest = datetime.now().strftime("%H:%M:%S")

        if paused:
            paused = False
            exit_event.wait(paused_seconds)
        else:
            exit_event.wait(COUNTDOWN_TIMER)


def gamermode(arg):
    pass


def pause_countdown(icon, item):
    global running, paused, first_run, paused_seconds
    if not paused:
        exit_event.set()
        running = False
        paused = True
        paused_seconds = COUNTDOWN_TIMER - (datetime.now() - parse(last_rest)).total_seconds()

        newToast = Toast()
        newToast.text_fields = ["Eyerester paused."]
        toaster.show_toast(newToast)
    else:
        first_run = True
        exit_event.clear()

        newToast = Toast()
        newToast.text_fields = ["Did you miss me?"]
        toaster.show_toast(newToast)

        Thread(target=main).start()


def exit(icon, item):
    global running
    exit_event.set()
    running = False
    icon.stop()
    sys.exit()

icon = pystray.Icon(
    "eyerest",
    "",
    "eyerest",
    menu=pystray.Menu(
        pystray.MenuItem("Gamer mode",
                         gamermode,
                         checked=lambda item: paused),
        pystray.MenuItem("Pause",
                         pause_countdown,
                         checked=lambda item: paused),
        pystray.MenuItem(
            "Last rest",
            lambda icon, item: icon.notify("Last rest: " + last_rest)
        ),
        pystray.MenuItem("Exit", exit),
    ),
)

if __name__ == "__main__":
    newToast = Toast()
    newToast.text_fields = ["Program started."]
    toaster.show_toast(newToast)

    Thread(target=main).start()

    icon.run()
