import pygame
import sys
import datetime
import sqlite3

con = sqlite3.connect('Database')
cur = con.cursor()
cur.execute('UPDATE Acheivement SET receive = "False"')
con.commit()
con.close()


pygame.init()
size = width, height = 1820, 980
screen_width = 1820
screen_height = 980
screen = pygame.display.set_mode(size)

pep_x = 0
FPS = 60

to_left = False
to_right = False

level1 = True
level2 = True

pep_y = 330
fon_n = 1

fon_image = pygame.image.load('data/fon1.png')
pep_image = pygame.image.load('data/pep1.png')
key = pygame.image.load("data/key.png")
clip = pygame.image.load("data/clip.png")
veshalka = pygame.image.load("data/veshalka.png")

clock = pygame.time.Clock()

inventory = [["", ], ["", ], ["", ], ["", ], ["", ], ["", ], ["", ], ["", ]]
working_triggers = ["clip", "key", "use_key", "veshalka"]

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ИГРА 'Побег' версия 2.0",
                  "",
                  "Вы все знаете события первой игры",
                  "Помогите Родиону сбежать вновь",
                  "",
                  "Правила игры",
                  "Для передвижения нажимайте стрелки",
                  "Для взаимодействия с предметами кнопку 'E'",
                  "Для начала игры нажмите любую кнопку"]

    screen.fill('white')
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 650
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)

def ney_game():
    intro_text = ["Стоп, ты думал что будет так просто?",
                  "Хаха, нет :).",
                  "В этот раз я спрячу ключ получше."]

    screen.fill('white')
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 650
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    z = True
    while z:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    z = False  # начинаем игру
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)

def end_screen1():
    intro_text = ["Ура, вы сбежали!",
                  "Нажмите кнопку 'E' для выхода."]

    screen.fill('white')
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 650
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    d = True
    while d:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not level1 and level2:
                    ney_game()
                    d = False
                elif not level2:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)

def end_screen2(duration):
    con = sqlite3.connect('Database')
    cur = con.cursor()
    cur.execute('SELECT receive FROM Acheivement')
    items_list = cur.fetchall()
    find_items = 0
    for i in items_list:
        if i[0] == 'True':
            find_items += 1
    intro_text = ["Ура, вы сбежали!",
                  "Нажмите кнопку 'E' для выхода.",
                  "Найдено предметов: " + str(find_items) + " из " + str(len(items_list)),
                  "Время " + duration]

    screen.fill('white')
    font = pygame.font.Font(None, 40)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 30
        intro_rect.top = text_coord
        intro_rect.x = 650
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    con.commit()
    con.close()
    d = True
    while d:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and not level1 and level2:
                    ney_game()
                    d = False
                elif not level2:
                    terminate()
            if event.type == pygame.QUIT:
                terminate()
        pygame.display.flip()
        clock.tick(FPS)

# чекбокс подбора предмета
def add_object(object):
    for i in range(len(inventory)):
        if inventory[i][0] == "":
            inventory[i][0] = object
            break

def in_inventory(object):
    for i in range(len(inventory)):
        if inventory[i][0] == object:
            return True
    return False

def remove_object(object):
    for i in range(len(inventory)):
        if inventory[i][0] == object:
            inventory[i][0] = ""
            break

def adding_time_to_database(duration):
    con = sqlite3.connect('Database')
    cur = con.cursor()

    cur.execute('INSERT INTO Time_leader (time) VALUES (?)', (duration,))

    con.commit()
    con.close()

def achievement(achiev):
   con = sqlite3.connect('Database')
   cur = con.cursor()

   cur.execute('UPDATE Acheivement SET receive = ? WHERE achievement = ?', ('True', achiev))

   con.commit()
   con.close()

# рисовка инвентаря
def draw_inventory():
    for i in range(len(inventory)):
        pygame.draw.rect(screen, (255, 255, 255), (500 + i * 100, 820, 100, 100), 1)
        if inventory[i][0] == "clip":
            screen.blit(clip, (505 + i * 100, 825))
        elif inventory[i][0] == "key":
            screen.blit(key, (505 + i * 100, 825))
        elif inventory[i][0] == "veshalka":
            screen.blit(veshalka, (505 + i * 100, 825))

# игровой процесс
game = True
time_start = datetime.datetime.now()
start_screen()
while level1:
    pygame.time.delay(15)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                to_left = True
            if event.key == pygame.K_RIGHT:
                to_right = True

            if event.key == pygame.K_e and 700 <= pep_x <= 900 and 'key' in working_triggers and fon_n == 1:
                achievement('key1')
                add_object('key')
                working_triggers[working_triggers.index('key')] = ""

            elif event.key == pygame.K_e and 1300 <= pep_x <= 1700 and 'clip' in working_triggers and fon_n == 2:
                achievement('clip1')
                add_object('clip')
                working_triggers[working_triggers.index('clip')] = ""

            elif event.key == pygame.K_e and 650 <= pep_x <= 1130 and 'veshalka' in working_triggers and fon_n == 2:
                achievement('veshalka1')
                add_object('veshalka')
                working_triggers[working_triggers.index('veshalka')] = ""

            elif event.key == pygame.K_e and 150 <= pep_x <= 500 and in_inventory("key") and fon_n == 2:
                remove_object('key')
                level1 = False
                working_triggers[working_triggers.index('use_key')] = ""

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False

            if event.key == pygame.K_RIGHT:
                to_right = False

        if event.type == pygame.QUIT:
            terminate()

    if to_right and pep_x < 1620 and fon_n == 1:
        pep_x += 10
        pep_image = pygame.image.load('data/pep1.png')

    if to_left and pep_x > -80 and fon_n == 1:
        pep_x -= 10
        pep_image = pygame.image.load('data/pep2.png')

    if pep_x <= -80 and fon_n == 1:
        fon_image = pygame.image.load('data/fon2.png')
        fon_n = 2
        pep_x = 1610

    if pep_x >= 1620 and fon_n == 2:
        fon_image = pygame.image.load('data/fon1.png')
        fon_n = 1
        pep_x = 0

    if to_right and pep_x < 1620 and fon_n == 2:
        pep_x += 10
        pep_image = pygame.image.load('data/pep1.png')

    if to_left and pep_x > -20 and fon_n == 2:
        pep_x -= 10
        pep_image = pygame.image.load('data/pep2.png')

    screen.blit(fon_image, (0, 0))
    screen.blit(pep_image, (pep_x, pep_y))
    draw_inventory()
    pygame.display.update()

end_screen1()
inventory = [["", ], ["", ], ["", ], ["", ], ["", ], ["", ], ["", ], ["", ]]
working_triggers = ["clip", "key", "use_key", "veshalka"]
pep_x = 0
fon_image = pygame.image.load('data/fon1.png')
fon_n = 1

while level2:
    pygame.time.delay(15)

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                to_left = True
            if event.key == pygame.K_RIGHT:
                to_right = True

            if event.key == pygame.K_e and 700 <= pep_x <= 900 and 'key' in working_triggers and fon_n == 1 and in_inventory("clip"):
                achievement('key2')
                remove_object('clip')
                add_object('key')
                working_triggers[working_triggers.index('key')] = ""

            elif event.key == pygame.K_e and 1200 <= pep_x <= 1600 and 'clip' in working_triggers and fon_n == 1 and in_inventory("veshalka"):
                achievement('clip2')
                remove_object('veshalka')
                add_object('clip')
                working_triggers[working_triggers.index('clip')] = ""

            elif event.key == pygame.K_e and 650 <= pep_x <= 1130 and 'veshalka' in working_triggers and fon_n == 2:
                achievement('veshalka2')
                add_object('veshalka')
                working_triggers[working_triggers.index('veshalka')] = ""

            elif event.key == pygame.K_e and 150 <= pep_x <= 500 and in_inventory("key") and fon_n == 2:
                remove_object('key')
                level2 = False
                working_triggers[working_triggers.index('use_key')] = ""

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                to_left = False

            if event.key == pygame.K_RIGHT:
                to_right = False

        if event.type == pygame.QUIT:
            terminate()

    if to_right and pep_x < 1620 and fon_n == 1:
        pep_x += 10
        pep_image = pygame.image.load('data/pep1.png')

    if to_left and pep_x > -80 and fon_n == 1:
        pep_x -= 10
        pep_image = pygame.image.load('data/pep2.png')

    if pep_x <= -80 and fon_n == 1:
        fon_image = pygame.image.load('data/fon2.png')
        fon_n = 2
        pep_x = 1610

    if pep_x >= 1620 and fon_n == 2:
        fon_image = pygame.image.load('data/fon1.png')
        fon_n = 1
        pep_x = 0

    if to_right and pep_x < 1620 and fon_n == 2:
        pep_x += 10
        pep_image = pygame.image.load('data/pep1.png')

    if to_left and pep_x > -20 and fon_n == 2:
        pep_x -= 10
        pep_image = pygame.image.load('data/pep2.png')

    screen.blit(fon_image, (0, 0))
    screen.blit(pep_image, (pep_x, pep_y))
    draw_inventory()
    pygame.display.update()

time_end = datetime.datetime.now()
adding_time_to_database(str(time_end - time_start))
end_screen2(str(time_end - time_start))