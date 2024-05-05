import win32gui
import win32con
import pygame
import pystray
import sys
import os
from PIL import Image
from datetime import datetime
from threading import Event, Thread
from base64 import b64decode

pygame.font.init()
pygame.mixer.init()

COUNTDOWN_TIMER = 1200 # seconds

SMALL_FONT = pygame.font.SysFont('comicsans', 100)
BIG_FONT = pygame.font.SysFont('comicsans', 250)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (30, 30, 30)
exit_event = Event()
last_rest = ""
first_run = True

stray_image = Image.open("kot.png")

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
            if event.type == pygame.QUIT: # if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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
    global first_run, last_rest, HALF_WIDTH, HALF_HEIGHT, WIN

    while not exit_event.is_set():
        if not first_run:
            WIN = pygame.display.set_mode((150, 150), pygame.NOFRAME)
            HALF_WIDTH, HALF_HEIGHT = 75, 75

            win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

            if not drawTimer(10, SMALL_FONT):
                exit_event.wait(COUNTDOWN_TIMER)
                continue

            WIN = pygame.display.set_mode((0, 0))
            WIDTH, HEIGHT = WIN.get_size()
            HALF_WIDTH, HALF_HEIGHT = WIDTH/2, HEIGHT/2

            win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

            drawTimer(20, BIG_FONT)
        else:
            first_run = False

        # Record current time when times up
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        last_rest = current_time

        exit_event.wait(COUNTDOWN_TIMER)


def exit(icon, item):
    global running
    exit_event.set()
    icon.stop()
    running = False
    sys.exit()

icon = pystray.Icon("eyerest", stray_image, "eyerest", menu=pystray.Menu(
    pystray.MenuItem("Last rest", lambda icon, item: icon.notify("Last rest: " + last_rest)),
    pystray.MenuItem("Exit", exit)
))

if __name__ == "__main__":
    Thread(target=main).start()

    icon.run()
