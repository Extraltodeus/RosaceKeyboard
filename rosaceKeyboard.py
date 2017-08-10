import pygame
import pyautogui
from random import randint
from math import atan2, pi, degrees, cos, sin

special_chars_1   = '-,.!? '
special_chars_2   = '=:\'"/'
ascii_lowercase = 'abcdefghijklmnopqrstuvwxyz'+special_chars_1
ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'+special_chars_2
digits = '0123456789'

press = pyautogui.press

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 180, 0)
BLUE  = (0,0,180)
RED   = (180,0,0)
YELLOW= (180,180,0)
GRAY_BLUE=(50,120,150)

circle_background_color = GRAY_BLUE
text_color = WHITE

pygame.init()

size_xy = 500
size_x = size_xy
size_y = size_xy
size = [size_x, size_y]
pygame.display.set_caption("Rosace Keyboard")
screen = pygame.display.set_mode(size)
circle_diameter = 60
c_offset = circle_diameter/1.5
font_size = 50
font = pygame.font.Font(None, font_size)

done = False

pizza = 8

tranche_sel = 1
old_x = 0
old_y = 0

FPS=60

deadzone_percent = 15
zone_morte = (size_xy/100)*deadzone_percent

couleurs = dict()
lettres  = dict()
touches  = dict()
centres  = dict()

touches[2]=0 #X
touches[3]=1 #Y
touches[1]=2 #B
touches[0]=3 #A

pyautogui.hotkey('alt', 'tab')

for tranchette in range (0,pizza):
    centres[tranchette] = dict()
    centres[tranchette]['x'] = int(size_xy/2+((size_xy/3)*cos((360*tranchette/pizza-90)*pi/180)))
    centres[tranchette]['y'] = int(size_xy/2+((size_xy/3)*sin((360*tranchette/pizza-90)*pi/180)))

    tranchette+=1
    lettres[tranchette] = {}
    for bouton in range(0,4):
        indic = bouton+(tranchette-1)*4
        lettres[tranchette][bouton] = {}
        try:
            lettres[tranchette][bouton]['L'] = ascii_lowercase[indic]
            lettres[tranchette][bouton]['U'] = ascii_uppercase[indic]
        except:
            lettres[tranchette][bouton]['L'] = " "
            lettres[tranchette][bouton]['U'] = " "
        try:
            lettres[tranchette][bouton]['D'] = digits[indic]
        except:
            lettres[tranchette][bouton]['D'] = " "

def print_text(textString,x,y):
    textBitmap = font.render(textString, True, text_color)
    screen.blit(textBitmap, [x-font_size/5, y-font_size/3])

def draw_back_circles(x,y):
    pygame.draw.circle(screen, BLUE, (x-int(c_offset),y), int(font_size/2.6))
    pygame.draw.circle(screen, YELLOW, (x,y-int(c_offset)), int(font_size/2.6))
    pygame.draw.circle(screen, RED, (int(x+c_offset),y), int(font_size/2.6))
    pygame.draw.circle(screen, GREEN, (x,y+int(c_offset)), int(font_size/2.6))

def print_layout(lettre,charset,x,y):
    print_text(lettre[0][charset],x-c_offset,y)
    print_text(lettre[1][charset],x,y-c_offset)
    print_text(lettre[2][charset],x+c_offset,y)
    print_text(lettre[3][charset],x,y+c_offset)

def typewrite(lettre):
    pyautogui.typewrite(lettre)

while done==False:
    try:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    except:
        print("Joystick non détecté")
        break

    L_Trig = joystick.get_axis(2)
    R_Trig = joystick.get_axis(5)

    screen.fill(BLACK)

    for centre in centres:
        c_x = centres[centre]['x']
        c_y = centres[centre]['y']
        pygame.draw.circle(screen, circle_background_color, (c_x,c_y), circle_diameter)
        if tranche_sel == (centre+1): draw_back_circles(c_x,c_y)
        if L_Trig > 0:
            print_layout(lettres[centre+1],'D',c_x,c_y)
        elif R_Trig < 0:
            print_layout(lettres[centre+1],'L',c_x,c_y)
        else:
            print_layout(lettres[centre+1],'U',c_x,c_y)

    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            if tranche_sel != 0 and event.button in touches:
                if L_Trig > 0:
                    typewrite(lettres[tranche_sel][touches[event.button]]['D'])
                elif R_Trig < 0:
                    typewrite(lettres[tranche_sel][touches[event.button]]['L'])
                else:
                    typewrite(lettres[tranche_sel][touches[event.button]]['U'])
            elif event.button == 7:
                done=True
            elif event.button == 4:
                press('backspace')
            elif event.button == 5:
                press('enter')
            elif event.button == 9:
                press('space')
            elif event.button == 6:
                press('escape')
            elif event.button == 10:
                pyautogui.click()
            else:
                print(event.button)
        if event.type == pygame.QUIT:
            done=True

    joyX = joystick.get_axis(0)
    joyY = joystick.get_axis(1)

    x = int(joyX*(size_x/2)+(size_x/2))
    y = int(joyY*(size_y/2)+(size_y/2))

    angle = int(atan2(joyY,joyX)/pi*180+90+180/pizza)

    if angle < 0:
        angle+=360

    if not (size_x/2-zone_morte) < x < (size_x/2+zone_morte) or not (size_y/2-zone_morte) < y < (size_y/2+zone_morte):
        for tranche in range(0,pizza):
            tranche+=1
            bonne_tranche = (360/pizza)*tranche
            if bonne_tranche > angle > (bonne_tranche-(360/pizza)):
                tranche_sel = tranche
    else:
        tranche_sel = 0

    pygame.display.update()
    pygame.time.Clock().tick(FPS)

pygame.quit ()

