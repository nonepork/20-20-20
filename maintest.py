import win32gui
import win32con
import pygame

pygame.font.init()
pygame.mixer.init()

COUNTDOWN_TIMER = 1200  # seconds

SMALL_FONT = pygame.font.SysFont("comicsans", 100)
BIG_FONT = pygame.font.SysFont("comicsans", 250)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (30, 30, 30)
first_run = True

def draw(timer, timerPos):
    pygame.draw.rect(WIN, DARK_GRAY, pygame.Rect(0, 0, 150, 150), 0, 20)
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
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

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

    drawTimer(10, SMALL_FONT)

main()
