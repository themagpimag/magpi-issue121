import pygame
import random

# Game info

display_width = 200
display_height = 300

bg_colour = (160, 178, 129)

pet_x = 100
pet_y = 100

# Variables for the pet

hunger = 2
happiness = 20
waste = 0
wastexy = {}
button_press = 0
pet_counter = 0
walk_cycle = 0

# Images, including two images for pet idle animation

pet_1 = pygame.image.load("sprites/pet1.png")
pet_2 = pygame.image.load("sprites/pet2.png")
full_heart = pygame.image.load("sprites/fullheart.png")
half_heart = pygame.image.load("sprites/halfheart.png")
empty_heart = pygame.image.load("sprites/emptyheart.png")
hungry = pygame.image.load("sprites/hungry.png")
poop = pygame.image.load("sprites/poop.png")
clean_button = pygame.image.load("sprites/clean.png")
feed_button = pygame.image.load("sprites/feed.png")
pet_button = pygame.image.load("sprites/pet.png")

# Game functions
# Pet location

def pet(pet_x,pet_y,game_display):
    global walk_cycle
    if walk_cycle == 0:
        game_display.blit(pet_1, (pet_x,pet_y))
    else:
        game_display.blit(pet_2, (pet_x,pet_y))

# Pet movement.
# There are checks so it won't move beyond the boundaries

def movement(move, game_display):
    global pet_x, pet_y
    if move == 1:
        pet_y -= 10
    if move == 2:
        pet_x += 10
    if move == 3:
        pet_y += 10
    if move == 4:
        pet_x -= 10
    if pet_x < 10:
        pet_x = 10
    if pet_x > 190:
        pet_x = 190
    if pet_y < 10:
        pet_y = 10
    if pet_y > 190:
        pet_y = 190
    pet(pet_x, pet_y, game_display)

# Happiness as displayed by hearts
# Each heart is worth 20 points

def hearts(game_display):
    global happiness
    if happiness < 1:
        game_display.blit(empty_heart, (40,215))
    if happiness > 0 and happiness < 15:
        game_display.blit(half_heart, (40,215))
    if happiness > 14:
        game_display.blit(full_heart, (40,215))
    if happiness < 25:
        game_display.blit(empty_heart, (80,215))
        game_display.blit(empty_heart, (120,215))
    if happiness > 24 and happiness < 35 :
        game_display.blit(half_heart, (80,215))
    if happiness > 34:
        game_display.blit(full_heart, (80,215))
    if happiness < 45:
        game_display.blit(empty_heart, (120,215))
    if happiness > 44 and happiness < 55:
        game_display.blit(half_heart, (120,215))
    if happiness > 54:
        game_display.blit(full_heart, (120,215))

# Poop location

def poopxy(waste,pet_x,pet_y,game_display):
    global wastexy
    if int(waste) > len(wastexy):
        wastexy[((int(waste))-1)] = ((pet_x + 5), pet_y)
        prev_waste = int(waste)
        
    for i in wastexy:
        game_display.blit(poop, wastexy[i])
    
# Hunger and happiness cycle

def pet_cycle(pet_x, pet_y, game_display):
    global hunger, happiness, waste
    if hunger < 10:
        hunger += 0.2
    if hunger > 7:
        game_display.blit(hungry, ((pet_x + 25),(pet_y - 30)))
    if happiness > 0:
        happiness -= 0.05
        if waste > 3:
            happiness -= 0.4
        if hunger > 9:
            happiness -= 0.2
    hearts(game_display)
    if waste < 5:
        waste += 0.1
    if int(waste) > 0:
        poopxy(waste,pet_x,pet_y,game_display)

# Button locations for press

def button_pressed(mousex, mousey):
    global button_press
    if mousey < 250:
        return 0
    else:
        if mousex >= 0 and mousex <= 60:
            return 1
        elif mousex >= 70 and mousex <= 130:
            return 2
        elif mousex >= 140 and mousex <= 200:
            return 3
        else:
            return 0

# Main game loop

def main():
    pygame.init
    clock = pygame.time.Clock()
    game_display = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption("MagPet")
    move = 0
    global pet_x, pet_y, happiness, hunger, waste, button_press, pet_counter, walk_cycle
    
    while True:
        game_display.fill(bg_colour)
        game_display.blit(feed_button, (0,250))
        game_display.blit(pet_button, (70,250))
        game_display.blit(clean_button, (140,250))
        mousex = 0
        mousey = 0
        
        # Event handler
        for current_event in pygame.event.get():
            if current_event.type == pygame.QUIT:
                pygame.quit()
            elif current_event.type == pygame.MOUSEBUTTONUP:
                mousex, mousey = current_event.pos
                button_press = button_pressed(mousex, mousey)
        
        # How does the pet move - 1-4 are cardinal directions
        if move == 0:
            move = random.randint(0,4)
        
        if move > 0:
            if random.randint(1,10) > 4:
                movement(move, game_display)
            else:
                move = random.randint(0,4)
                movement(move, game_display)
                
        if button_press != 0:
            if button_press == 1:
                hunger = 0
                happiness += 10
                button_press = 0
            if button_press == 2:
                if pet_counter > 0:
                    button_press = 0
                else:
                    happiness += 10
                    pet_counter = 5
                    button_press = 0
            if button_press == 3:
                waste = 0
                wastexy = {}
                button_press = 0
            
        if pet_counter > 0:
            pet_counter -= 1
        
        if happiness < 0 and int(waste) == 5 and hunger > 10:
            print ("Game Over")
        else:
            pet_cycle(pet_x, pet_y, game_display)
            pygame.display.update()
            
            if walk_cycle == 0:
                walk_cycle = 1
            else:
                walk_cycle = 0
            
            if pet_counter > 0:
                pet_counter -= 1
            
            clock.tick(2)
        
        
if __name__ == '__main__':
    main()
