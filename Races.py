# Импортирование библиотек
import random
import time
import os
import pygame

pygame.init()

scrn_w = 400
scrn_h = 600

btn_x = 75
btn_nw_y = 400
exit_y = 460
btn_w = 242
btn_h = 50

# Блок для назначения цвета кнопкам и тексту
blk_clr = (0, 0, 0)
wht_clr = (255, 255, 255)
red_clr = (255, 0, 0)
redLt_clr = (255, 21, 21)
gry_clr = (112, 128, 144)
grn_clr = (0, 255, 0)
grnLt_clr = (51, 255, 51)
blu_clr = (0, 0, 255)



gm_lyt_disp = pygame.display.set_mode((scrn_w, scrn_h))
pygame.display.set_caption('Race Priora vs Ferrari')
tm_clk = pygame.time.Clock()

# Визуализация
car_img = pygame.image.load(os.getcwd() + '\\images/priora.png')
left_car = pygame.image.load(os.getcwd() + '\\images/car_left.png')
right_car = pygame.image.load(os.getcwd() + '\\images/car_right.png')
obstacle_img = pygame.image.load(os.getcwd() + '\\images/obstacle.png')
texture_img = pygame.image.load(os.getcwd() + '\\images/texture')
(c_w, c_h) = car_img.get_rect().size
(l_c_w, l_c_h) = left_car.get_rect().size
(r_c_w, r_c_h) = right_car.get_rect().size
(t_w, t_h) = obstacle_img.get_rect().size
(txt_w, txt_h) = texture_img.get_rect().size

icon = pygame.image.load(os.getcwd() + '\\images/logo.png')
pygame.display.set_icon(icon)

bg_img = pygame.image.load(os.getcwd() + '\\images/background.png')
bg_still = pygame.image.load(os.getcwd() + '\\images/background_inv.png')
bgRect = bg_img.get_rect()

# Звук
intro_snd_1 = pygame.mixer.Sound(os.getcwd() + '\\audio/intro1.wav')
intro_snd_2 = pygame.mixer.Sound(os.getcwd() + '\\audio/intro2.wav')
crash_snd = pygame.mixer.Sound(os.getcwd() + '\\audio/car_crash.wav')
ignition_snd = pygame.mixer.Sound(os.getcwd() + '\\audio/ignition.wav')
pygame.mixer.music.load(os.getcwd() + '\\audio/running.wav')


def dodged_things(count, top_score, speed):
    fnt = pygame.font.SysFont(None, 25)
    score = fnt.render("Dodged: " + str(count), True, grn_clr)
    top_score = fnt.render("High Score: " + str(top_score), True, grn_clr)
    speed = fnt.render("Speed: " + str(speed) + "Km/h", True, grn_clr)
    gm_lyt_disp.blit(score, (10, 0))
    gm_lyt_disp.blit(top_score, (10, 27))
    gm_lyt_disp.blit(speed, (scrn_w - 125, 0))


def update_high_score(dodged):
    high_scores = open(os.getcwd() + '\\textfile/high_score.txt', 'w')
    temp = str(dodged)
    high_scores.write(temp)


def draw_obstacle(th_x, th_y):
    gm_lyt_disp.blit(obstacle_img, (th_x, th_y))


def draw_car(x, y, direction):
    if direction == 0:
        gm_lyt_disp.blit(car_img, (x, y))
    if direction == -1:
        gm_lyt_disp.blit(left_car, (x, y))
    if direction == 1:
        gm_lyt_disp.blit(right_car, (x, y))


def text_surf(text, font, color):
    txtSurf = font.render(text, True, color)
    return txtSurf, txtSurf.get_rect()


def display_message(text, x, y, color, sleep_time):
    lar_txt = pygame.font.Font('freesansbold.ttf', 50)
    txtSurf, TxtRect = text_surf(text, lar_txt, color)
    TxtRect.center = ((scrn_w / 2 - x), (scrn_h / 2 - y))
    gm_lyt_disp.blit(txtSurf, TxtRect)
    pygame.display.update()
    time.sleep(sleep_time)


def title_message(sh_x, sh_y, color):
    lar_txt = pygame.font.Font('freesansbold.ttf', 30)
    txtSurf, TxtRect = text_surf("Race Priora vs Ferrari", lar_txt, color)
    TxtRect.center = ((scrn_w / 2 - sh_x), (scrn_h / 3 - sh_y))
    gm_lyt_disp.blit(txtSurf, TxtRect)
    time.sleep(0.15)
    pygame.display.update()


def title_msg():
    anim_height = scrn_h
    pygame.mixer.Sound.play(intro_snd_1)
    while anim_height > -600:
        gm_lyt_disp.fill(wht_clr)
        draw_obstacle(scrn_w / 2 - t_w / 2, anim_height)
        anim_height -= 1.5
        pygame.display.update()
    title_message(0, 0, blk_clr)
    time.sleep(0.1)
    pygame.mixer.Sound.play(intro_snd_2)


def move_texture(th_start):
    gm_lyt_disp.blit(texture_img, (0, th_start - 400))
    gm_lyt_disp.blit(texture_img, (0, th_start))
    gm_lyt_disp.blit(texture_img, (0, th_start + 400))


def crash():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_snd)
    display_message("Авария", 0, 0, red_clr, 0)
    while True:
        play_again = button("Запустить игру", btn_x, btn_nw_y, btn_w, btn_h, grnLt_clr, grn_clr)
        exit_game = button("Выйти", btn_x, exit_y, btn_w, btn_h, redLt_clr, red_clr)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or exit_game == 1 or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if play_again == 1 or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                game_loop()
        pygame.display.update()
        tm_clk.tick(15)


def button(msg, x, y, wid, hei, in_act_color, act_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + wid > mouse[0] > x and y + hei > mouse[1] > y:
        pygame.draw.rect(gm_lyt_disp, act_color, (x, y, wid, hei))
        if click[0] == 1:
            return 1
    else:
        pygame.draw.rect(gm_lyt_disp, in_act_color, (x, y, wid, hei))

    small_txt = pygame.font.Font('freesansbold.ttf', 20)
    TxtSurf, TxtRect = text_surf(msg, small_txt, wht_clr)
    TxtRect.center = ((x + wid / 2), (y + hei / 2))
    gm_lyt_disp.blit(TxtSurf, TxtRect)


def welcome_screen():
    welcome = True
    gm_lyt_disp.fill(wht_clr)
    title_msg()
    exit_game = 0
    while welcome:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or exit_game == 1 or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
        play_game = button("Новая игра", btn_x, btn_nw_y, btn_w, btn_h, grnLt_clr, grn_clr)
        exit_game = button("Выход", btn_x, exit_y, btn_w, btn_h, redLt_clr, red_clr)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit_game = 1
        if play_game or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            welcome = False

        pygame.display.update()
        tm_clk.tick(15)


def count_down():
    count = 3
    pygame.mixer.music.pause()
    pygame.mixer.Sound.play(ignition_snd)
    while count >= 0:
        gm_lyt_disp.blit(bg_img, bgRect)
        draw_car(scrn_w * 0.40, scrn_h * 0.6, 0)
        if count == 0:
            display_message("GO!", 0, 0, grn_clr, 0.75)
            pygame.mixer.music.play(-1)
        else:
            display_message(str(count), 0, 0, red_clr, 0.75)
        count -= 1
    tm_clk.tick(15)


def paused_game():
    pygame.mixer.music.pause()
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            display_message("pause", 0, 0, blu_clr, 1.5)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.unpause()
                    return
        pygame.display.update()
        tm_clk.tick(15)


def game_loop():
    pygame.mixer.music.play(-1)
    width_x = (scrn_w * 0.4)
    height_y = (scrn_h * 0.6)
    ch_x = 0

    th_st_x = random.randrange(8, scrn_w - t_w - 8)
    th_st_y = -600
    th_speed = 5

    track_y = 0
    track_speed = 25

    dodged = 0
    direction = 0

    highest_score_file = open(os.getcwd() + '/textfile/high_score.txt', 'r')
    high_score = highest_score_file.read()

    game_exit = False
    count_down()

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    ch_x = -10
                    direction = -1
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    ch_x = 10
                    direction = 1
                if event.key == pygame.K_SPACE:
                    paused_game()
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                    ch_x = 0
                    direction = 0
        width_x += ch_x
        gm_lyt_disp.blit(bg_img, bgRect)

        move_texture(th_st_y)
        draw_obstacle(th_st_x, th_st_y)
        th_st_y += th_speed
        draw_car(width_x, height_y, direction)

        dodged_things(dodged, high_score, th_speed)
        if width_x > scrn_w - c_w or width_x < 0:
            crash()
        if th_st_y > scrn_h:
            th_st_y = 0 - t_h
            th_st_x = random.randrange(0, scrn_w)
            dodged += 1
            th_speed += 1
        if dodged > int(high_score):
            update_high_score(dodged)
        if height_y < th_st_y + t_h - 15 and width_x > th_st_x - c_w - 5 and width_x < th_st_x + t_w - 5:
            crash()

        pygame.display.update()
        tm_clk.tick(60)


welcome_screen()
game_loop()
pygame.quit()
quit()
