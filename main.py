import pgzrun
import random

size_w = 9 # Width of field in cells
size_h = 10 # Height of field in cellss
WIDTH = 64 * size_w
HEIGHT = 64 * size_h

# Game WindowsError
cell = Actor("stone") # Stone
cell1 = Actor("grass") # Grass
cell2 = Actor("sand") # Sand

sand_setting = Actor("sand", (WIDTH / 2 - 150, HEIGHT / 2))
grass_setting = Actor("grass", (WIDTH / 2 + 150, HEIGHT / 2))
snow_setting = Actor("snow", (WIDTH / 2, HEIGHT / 2))

select_background = Actor("select-background", (WIDTH / 2, HEIGHT / 4)) # Select Background Text
play_again = Actor("play-again-btn", (285, 325)) # Play Again Button
you_win_text = Actor("you-win", (285, 225)) # You Win Text
you_lose_text = Actor("you-lose", (285, 225)) # You Lose Text
setting = Actor("settings", (WIDTH - 35, 35)) # Settings


ICON = "images/stand.png" # Icon of the Game Window
TITLE = "Milano Bros" # Title of the Game Window

mode = "game"
level = 1
win = 0

FPS = 30 # Number of Frames Per Second
my_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 1, 1, 1, 1, 1, 1, 1, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [-1, -1, -1, -1, -1, -1, -1, -1, -1]] # Attack and health power row

def new_game():
    char.health = 100
    char.attack = 5

    for i in range(5 + level):
        enemy = Actor("horse", topleft = (random.randint(1, 7) * cell.width, random.randint(1, 7) * cell.height))
        enemy.health = random.randint(10, 20)
        enemy.attack = random.randint(4, 8)
        enemy.bonus = random.randint(0, 2)
        enemies.append(enemy)


# Protagonist
char = Actor('stand')
char.top = cell.height
char.left = cell.width

enemies = []
swords = []
hearts = []
new_game()



def map_draw():
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            if my_map[i][j] == 0:
                cell.left = cell.width*j
                cell.top = cell.height*i
                cell.draw()
            elif my_map[i][j] == 1:
                cell1.left = cell.width*j
                cell1.top = cell.height*i
                cell1.draw()
            elif my_map[i][j] == 2:
                cell2.left = cell.width*j
                cell2.top = cell.height*i
                cell2.draw()  
            elif my_map[i][j] == 3:
                cell3.left = cell.width*j
                cell3.top = cell.height*i
                cell3.draw() 

def update(dt):
    victory()
    
    for h in hearts:
        if char.colliderect(h):
            char.health += 5
            hearts.remove(h)
            break
    for s in swords:
        if char.colliderect(s):
            char.attack += 5
            swords.remove(s)
            break
        
def draw():
    screen.fill("#2f3542")
    
    if mode == "game":
        map_draw()
        
        for e in enemies:
            e.draw()
        
        for s in swords:
            s.draw()
        
        for h in hearts:
            h.draw()
        
        char.draw()

        # Level
        screen.draw.text("Level " + str(level), center=( WIDTH / 2, 33), color = 'black', fontsize = 50)

        # Health
        screen.draw.text("HP:", center=( 0 + 100, (size_h - 0.5) * cell1.height ), color = 'white', fontsize = 28)
        screen.draw.text(str(char.health), center=( 0 + 180, (size_h - 0.5) * cell1.height ), color = 'white', fontsize = 28)
        
        # Attack
        screen.draw.text("AP:", center=( (size_w - 2) * cell1.width, (size_h - 0.5) * cell1.height ), color = 'white', fontsize = 28)
        screen.draw.text(str(char.attack), center=( (size_w - 1) * cell1.width, (size_h - 0.5) * cell1.height ), color = 'white', fontsize = 28)

        
        setting.draw()
    
    elif mode == "setting":
        select_background.draw()
        # screen.draw.text("Select Background", center=( WIDTH / 2, 100), color = 'white', fontsize = 75)
        
        grass_setting.draw()
        sand_setting.draw()
        snow_setting.draw()
        
        

    elif mode == "end":
        if win == 1:
            # screen.draw.text("YOU WIN!", center=(WIDTH / 2, HEIGHT / 2), color = 'white', fontsize = 65)
            you_win_text.draw()
        
        elif win == 0:
            # screen.draw.text("YOU LOSE!", center=(WIDTH / 2, HEIGHT / 2), color = 'white', fontsize = 65)
            you_lose_text.draw()
        
        play_again.draw()
    

def on_key_down(key):
    
    old_x = char.x
    old_y = char.y
    
    if (keyboard.d or keyboard.right) and char.x + cell.width < WIDTH - cell.width:
        char.x += cell.width
        char.image = 'stand'
    elif (keyboard.a or keyboard.left) and char.x - cell.width > cell.width:
        char.x -= cell.width
        char.image = 'left'
    elif (keyboard.s or keyboard.down) and char.y + cell.height < HEIGHT - cell.height*2:
        char.y += cell.height
    elif (keyboard.w or keyboard.up) and char.y - cell.height > cell.height:
        char.y -= cell.height
    
    enemy_index = char.collidelist(enemies)
    
    if enemy_index >- 1:
        enemy = enemies[enemy_index]
        char.health -= enemy.attack
        enemy.health -= char.attack
        
        char.x = old_x
        char.y = old_y
        
        if enemy.health <= 0:
            enemies.remove(enemy)
            
            if enemy.bonus == 0:
                pass

            elif enemy.bonus == 1:
                heart = Actor("heart", enemy.pos)
                hearts.append(heart)

            elif enemy.bonus == 2:
                sword = Actor("sword", enemy.pos)
                swords.append(sword)
        
                
def on_mouse_down(button, pos):
    global mode
    
    if mode == "game":
        if setting.collidepoint(pos):
            print("Setting Button Clicked!")
            mode = "setting"
    
    elif mode == "setting":
        if grass_setting.collidepoint(pos):
            cell1.image = "grass"
            mode = "game"
        
        elif sand_setting.collidepoint(pos):
            cell1.image = "sand"
            mode = "game"
        
        elif snow_setting.collidepoint(pos):
            cell1.image = "snow"
            mode = "game"
    
    elif mode == "end":
        if play_again.collidepoint(pos):
            new_game()

            print("Play Again Button Clicked!")
            mode = "game"


# Menang atau Kalah
def victory():
    global win
    global mode
    global level

    if mode == "game":
        if enemies == [] and char.health > 0:
            win = 1
            mode = "end"
            level += 1
        
        elif char.health <= 0:
            win = 0
            mode = "end"

pgzrun.go()