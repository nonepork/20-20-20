import win32gui
import win32con
import pygame
import time
import sys
import os
from datetime import datetime
from VividHues import Clr

pygame.font.init()
pygame.mixer.init()

projectFolder = os.path.dirname(os.path.abspath(sys.argv[0]))
resourcesFolder = os.path.join(projectFolder, 'Resources')

SMALL_FONT = pygame.font.SysFont('comicsans', 100)
BIG_FONT = pygame.font.SysFont('comicsans', 250)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (30, 30, 30)
first_time = True

def draw(timer, timerPos):
    WIN.fill(DARK_GRAY)
    WIN.blit(timer, timerPos)
    pygame.display.update()


def main(timerValue, font):
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


if __name__ == "__main__":
    os.system('cls')
    print(Clr.BOLD + Clr.random("スタート~") + Clr.RS)
    while True:
        if not first_time:
            WIN = pygame.display.set_mode((150, 150), pygame.NOFRAME)
            HALF_WIDTH, HALF_HEIGHT = 75, 75

            win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

            if not main(10, SMALL_FONT):
                time.sleep(1200)
                continue

            WIN = pygame.display.set_mode((0, 0))
            WIDTH, HEIGHT = WIN.get_size()
            HALF_WIDTH, HALF_HEIGHT = WIDTH/2, HEIGHT/2

            win32gui.SetWindowPos(pygame.display.get_wm_info()['window'], win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)

            main(20, BIG_FONT)
        else:
            first_time = False

        # Record current time when times up
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", Clr.jazzy(current_time) + Clr.RS)

        time.sleep(1200)
