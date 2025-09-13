from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math, random


hakis = []
marines= []
powerups = []
player_pos = [0, 0, 0]
player_rot = 0
health = 5
score = 0
game_over = False
boss_counter = 0
game_win = False

rain_active = False
raindrops = []
n_raindrops = 200 
rain_length = 10.0
rain_speed = 10.0
rain_used = False
rain_timer = 0
rain_duration = 900

game_state = "menu" 
selected_character = 'luffy'#default
current_character = 'luffy'
character_time = 50.0
time_counter = 0

camera_radius = 500.0 
camera_azimuth = 0.0 
camera_elevation = 45.0 

boss_enemy = None
boss_health = 20
boss_active = False

player_max_health = 5
player_current_health = 5

boss_max_health = 20
boss_current_health = 20

shield_active = False
shield_time = 0
shield_counter = 0

luffy_left_hand_scale = 1.0
luffy_right_hand_scale = 1.0
zoro_speed_boost = False

santorio_active = False
santorio_timer = 0
santorio_duration = 90       
santorio_speed = 35.0
santorio_hit_cooldown = 0

cam_pos = (0, 400, 400)
view_angle = 130
grid_size = 15
tile_size = 100
camera_mode = "third_person"

background_color = [0.0, 0.0, 0.0] 

sword_rotation_angle= 0.0
sword_rotating_speed = 8.0 
sword_attack_in_progress = False   
sword_attack_duration = 30          
sword_attack_range = 160.0

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

def draw_ground():
    total_length = grid_size * tile_size
    
    glBegin(GL_QUADS)
    for i in range(grid_size):
        for j in range(grid_size):
            total = i + j
            if total % 2 == 0:
                glColor3f(0.8, 0.8, 0.8)
            else:
                glColor3f(0.4, 0.4, 0.6)
                
            x = (i - grid_size / 2) * tile_size
            y = (j - grid_size / 2) * tile_size
            
            glVertex3f(x, y, 0)
            glVertex3f(x + tile_size, y, 0)
            glVertex3f(x + tile_size, y + tile_size, 0)
            glVertex3f(x, y + tile_size, 0)
    glEnd()

def draw_luffy():
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(player_rot, 0, 0, 1)
    
    if game_over:
        glTranslatef(0, 0, 60)
        glRotatef(90, 1, 0, 0)
    
    # Body
    glPushMatrix()
    glTranslatef(0, 0, 80)
    glColor3f(1.0, 0.0, 0.0) 
    glutSolidCube(50)
    glPopMatrix()
    
    # Head
    glPushMatrix()
    glTranslatef(0, 0, 130)
    glColor3f(0.9, 0.7, 0.5) 
    gluSphere(gluNewQuadric(), 25, 15, 15)
    glPopMatrix()
    
    # Hat
    glPushMatrix()
    glTranslatef(0, 0, 150)
    glColor3f(1.0, 1.0, 0.0) 
    glutSolidCube(30)
    glPopMatrix()
    
    # Left leg
    glPushMatrix()
    glTranslatef(-15, 0, 20)
    glColor3f(0.0, 0.0, 1.0) 
    gluCylinder(gluNewQuadric(), 10, 8, 60, 10, 10)
    glPopMatrix()
    
    # Right leg  
    glPushMatrix()
    glTranslatef(15, 0, 20)
    glColor3f(0.0, 0.0, 1.0)
    gluCylinder(gluNewQuadric(), 10, 8, 60, 10, 10)
    glPopMatrix()
    
    # Left hand
    glPushMatrix()
    glTranslatef(-35, 0, 100)
    glRotatef(-90, 0, 0, 1)
    glRotatef(-90, 0, 1, 0)
    glScalef(1.0, 1.0, luffy_left_hand_scale)
    glColor3f(0.9, 0.7, 0.5)
    gluCylinder(gluNewQuadric(), 8, 6, 40, 10, 10)
    glPopMatrix()
    
    # Right hand
    glPushMatrix()
    glTranslatef(35, 0, 100)
    glRotatef(-90, 0, 0, 1)
    glRotatef(-90, 0, 1, 0)
    glScalef(1.0, 1.0, luffy_right_hand_scale)
    glColor3f(0.9, 0.7, 0.5)
    gluCylinder(gluNewQuadric(), 8, 6, 40, 10, 10)
    glPopMatrix()
    
    glPopMatrix()

def draw_zoro():
    glPushMatrix()
    glTranslatef(*player_pos)
    glRotatef(player_rot, 0, 0, 1)
    
    if game_over:
        glTranslatef(0, 0, 60)
        glRotatef(90, 1, 0, 0)
    
    # Body
    glPushMatrix()
    glTranslatef(0, 0, 80)
    glColor3f(0.0, 0.8, 0.0) 
    glutSolidCube(50)
    glPopMatrix()
    
    # Head
    glPushMatrix()
    glTranslatef(0, 0, 130)
    glColor3f(0.9, 0.7, 0.5)  
    gluSphere(gluNewQuadric(), 25, 15, 15)
    glPopMatrix()
    
    # Green hair
    glPushMatrix()
    glTranslatef(0, 0, 150)
    glColor3f(0.0, 0.6, 0.0)
    glutSolidCube(25)
    glPopMatrix()
    
    # Left leg
    glPushMatrix()
    glTranslatef(-15, 0, 20)
    glColor3f(0.2, 0.2, 0.2) 
    gluCylinder(gluNewQuadric(), 10, 8, 60, 10, 10)
    glPopMatrix()
    
    # Right leg
    glPushMatrix()
    glTranslatef(15, 0, 20)
    glColor3f(0.2, 0.2, 0.2)
    gluCylinder(gluNewQuadric(), 10, 8, 60, 10, 10)
    glPopMatrix()
    
    # Left hand
    glPushMatrix()
    glTranslatef(-35, 0, 100)
    glColor3f(0.9, 0.7, 0.5)
    gluCylinder(gluNewQuadric(), 8, 6, 40, 10, 10)
    glPopMatrix()
    
    # Right hand with sword
    glPushMatrix()
    glTranslatef(35, 0, 100) 
    glColor3f(0.9, 0.7, 0.5)
    gluCylinder(gluNewQuadric(), 8, 6, 40, 10, 10)
    glTranslatef(0, 15, 20)
    glRotatef(sword_rotation_angle, 0, 1, 0)  
    glColor3f(0.7, 0.7, 0.9)
    gluCylinder(gluNewQuadric(), 3, 3, 80, 8, 8) 
    glPopMatrix()
    
    glPopMatrix()

def draw_marines(enemy):
    glPushMatrix()
    glTranslatef(*enemy['pos'])
    
    # Body 
    glPushMatrix()
    glTranslatef(0, 0, 80)
    glColor3f(0.9, 0.9, 0.9) 
    glutSolidCube(45)
    glPopMatrix()
    
    # Head
    glPushMatrix()
    glTranslatef(0, 0, 125)
    glColor3f(0.9, 0.7, 0.5)
    gluSphere(gluNewQuadric(), 20, 15, 15)
    glPopMatrix()
    
    # Cap
    glPushMatrix()
    glTranslatef(0, 0, 140)
    glColor3f(0.2, 0.2, 0.6) 
    glutSolidCube(25)
    glPopMatrix()
    
    # Left leg
    glPushMatrix()
    glTranslatef(-12, 0, 25)
    glColor3f(0.1, 0.1, 0.1) 
    gluCylinder(gluNewQuadric(), 8, 6, 55, 10, 10)
    glPopMatrix()
    
    # Right leg
    glPushMatrix()
    glTranslatef(12, 0, 25)
    glColor3f(0.1, 0.1, 0.1) 
    gluCylinder(gluNewQuadric(), 8, 6, 55, 10, 10)
    glPopMatrix()
    
    # Left arm
    glPushMatrix()
    glTranslatef(-25, 0, 95)
    glColor3f(0.9, 0.7, 0.5) 
    gluCylinder(gluNewQuadric(), 6, 4, 30, 8, 8)
    glPopMatrix()
    
    # Right arm holding gun 
    glPushMatrix()
    glTranslatef(25, 0, 95)
    glColor3f(0.9, 0.7, 0.5)
    gluCylinder(gluNewQuadric(), 6, 4, 30, 8, 8)
    
    # Marine's gun
    glTranslatef(0, 12, 15)
    glRotatef(45, 1, 0, 0) 
    glColor3f(0.3, 0.3, 0.3) 
    gluCylinder(gluNewQuadric(), 3, 3, 60, 8, 8)
    
    # Gun barrel 
    glTranslatef(0, 0, 60)
    glColor3f(0.2, 0.2, 0.2) 
    gluCylinder(gluNewQuadric(), 2, 2, 15, 6, 6)
    glPopMatrix()
    
    # Marine belt/equipment
    glPushMatrix()
    glTranslatef(0, 0, 70)
    glColor3f(0.4, 0.2, 0.1) 
    glScalef(1.2, 1.2, 0.3)
    glutSolidCube(35)
    glPopMatrix()
    
    glPopMatrix()

def draw_crocodile():
    global game_win
    if not boss_enemy:
        return
    if game_win:
        glTranslatef(0,0,60)
        glRotatef(90, 1, 0, 0)
        
    glPushMatrix()
    glTranslatef(*boss_enemy['pos'])
    glScalef(2.0, 2.0, 2.0) 

    # Body
    glPushMatrix()
    glTranslatef(0, 0, 80)
    glColor3f(1.0, 0.4, 0.6)
    glutSolidCube(45)
    glPopMatrix()
    
    # Head
    glPushMatrix()
    glTranslatef(0, 0, 120)
    glColor3f(0.9, 0.7, 0.5) 
    gluSphere(gluNewQuadric(), 20, 15, 15)

    # Yellow Hair 
    glPushMatrix()
    glTranslatef(0, 0, 20) 
    glColor3f(1.0, 1.0, 0.0) 
    glutSolidCube(25)
    glPopMatrix()

    glPopMatrix()
    
    # Sunglasses
    glColor3f(0.6, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(-10, 15, 125)
    glScalef(0.5, 0.1, 0.1)
    glutSolidCube(20)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(10, 15, 125)
    glScalef(0.5, 0.1, 0.1)
    glutSolidCube(20)
    glPopMatrix()
    
    # Legs 
    glColor3f(1, 0, 1)
    glPushMatrix()
    glTranslatef(-12, 0, 25)
    gluCylinder(gluNewQuadric(), 8, 6, 55, 10, 10)
    glPopMatrix()
    
    glPushMatrix()
    glTranslatef(12, 0, 25)
    gluCylinder(gluNewQuadric(), 8, 6, 55, 10, 10)
    glPopMatrix()
    
    # Arms and String Attack
    glColor3f(0.9, 0.7, 0.5)
    glPushMatrix()
    glTranslatef(-25, 0, 95)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 6, 4, 30, 8, 8)
    glPopMatrix()
    
    glColor3f(0.9, 0.7, 0.5)
    glPushMatrix()
    glTranslatef(25, 0, 95)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 6, 4, 30, 8, 8)
    
    # Doflamingo's String Attack
    glPushMatrix()
    glTranslatef(0, 12, 15)
    glRotatef(45, 1, 0, 0)
    
    glColor3f(1.0, 1.0, 1.0)
    gluCylinder(gluNewQuadric(), 3, 3, 100, 8, 8) 
    glPopMatrix()
    
    glPopMatrix()
    
    glPopMatrix()

def draw_haki():
    for haki in hakis:
        glPushMatrix()
        glTranslatef(*haki['pos'])
        if current_character == "luffy":
            glColor3f(1.0, 0.5, 0.0)  
            glutSolidCube(12)
        else:  
            glColor3f(0.8, 0.8, 1.0)
            glutSolidCube(15)
        glPopMatrix()

def draw_powerups():
    for powerup in powerups:
        glPushMatrix()
        glTranslatef(*powerup['pos'])
        glColor3f(1.0, 0.0, 1.0) 
        gluSphere(gluNewQuadric(), 15, 12, 12)
        
        glTranslatef(0, 0, 15)
        glColor3f(0.0, 0.8, 0.0)
        gluCylinder(gluNewQuadric(), 2, 2, 10, 6, 6)
        glPopMatrix()

def draw_player_health_bar(x, y):
    global health
    
    health_bar_width = 200
    health_bar_height = 20
    dynamic_width = (float(health) / 5) * health_bar_width
    
    glColor3f(0.0, 1.0, 0.0) 
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + dynamic_width, y)
    glVertex2f(x + dynamic_width, y + health_bar_height)
    glVertex2f(x, y + health_bar_height)
    glEnd()
    

def draw_crocodile_health_bar(x, y):
    global boss_health, boss_active
    
    if not boss_active:
        return
        
    boss_bar_width = 200
    boss_bar_height = 20
    dynamic_width_boss = (float(boss_health) / 20) * boss_bar_width
    
    glColor3f(1.0, 0.0, 0.0) 
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + dynamic_width_boss, y)
    glVertex2f(x + dynamic_width_boss, y + boss_bar_height)
    glVertex2f(x, y + boss_bar_height)
    glEnd()
   
    
def init_raindrops():
    global raindrops
    raindrops = []
    total_length = grid_size * tile_size
    half_length = total_length / 2
    for i in range(n_raindrops):
        raindrops.append({
            'x': random.uniform(-half_length, half_length),
            'y': random.uniform(-half_length, half_length),
            'z': random.uniform(500,700) 
        })
        
def new_marines():
    #range
    min_distance = 350  
    max_distance = 500  
    
    angle = random.uniform(0, 2 * math.pi)
    
    distance = random.uniform(min_distance, max_distance)
    
    spawn_x = player_pos[0] + distance * math.cos(angle)
    spawn_y = player_pos[1] + distance * math.sin(angle)
    
    arena_limit = (grid_size * tile_size) // 2 - 60
    spawn_x = max(-arena_limit, min(arena_limit, spawn_x))
    spawn_y = max(-arena_limit, min(arena_limit, spawn_y))
    
    return {'pos': [spawn_x, spawn_y, 0]}

    
def spawn_boss():
    global boss_enemy, boss_active, boss_health, boss_counter
    if not boss_active and boss_counter < 3 and score > 0 and score % 20 == 0 and not game_win:  
        boss_health = 20
        while True:
            x = random.randint(-300, 300)
            y = random.randint(-300, 300)
            distance_from_player = math.hypot(x - player_pos[0], y - player_pos[1])
            if distance_from_player > 300: 
                break
        boss_enemy = {'pos': [x, y, 0]}
        boss_active = True
        print(f"A boss enemy has appeared!")

        
def spawn_powerup():
    if random.random() < 0.001:  
        x = random.randint(-300, 300)
        y = random.randint(-300, 300)
        powerups.append({'pos': [x, y, 0]})

def fire_haki():
    global hakis
    if game_over:
        return
        
    ang = math.radians(player_rot)
    dx, dy = -math.sin(ang), math.cos(ang)
    haki_x = player_pos[0] + dx * 50
    haki_y = player_pos[1] + dy * 50
    haki_z = player_pos[2] + 50
    
    hakis.append({'pos': [haki_x, haki_y, haki_z], 'dir': (dx, dy)})

def update_character_timer():
    global character_time, current_character, time_counter
    
    time_counter += 1
    if time_counter >= 60:  
        character_time -= 1
        time_counter = 0
        
        if character_time <= 0:
            if current_character == "luffy":
                current_character = "zoro"
            else:
                current_character = "luffy"
            character_time = 50.0
            print(f"Switch! Now playing as {current_character}")

def update_shield():
    global shield_active, shield_time
    if shield_active:
        shield_time -= 1
        if shield_time <= 0:
            shield_active = False

def update_raindrops():
    if not rain_active:
        return
    
    for rain in raindrops:
        rain['z'] -= rain_speed
        if rain['z'] < 0.0:
            rain['z'] = random.uniform(500,700)

def draw_raindrops():
    if not rain_active:
        return
    
    glColor3f(0.0, 0.0, 1.0) 
    glLineWidth(1.5) 

    glBegin(GL_LINES)
    for rain in raindrops:
        glVertex3f(rain['x'], rain['y'], rain['z'] + rain_length) 
        glVertex3f(rain['x'], rain['y'], rain['z']) 
    glEnd()
    glLineWidth(1.0)
    
def zoro_haki_slash():
    global marines, score, boss_health, boss_enemy
    survivors = []
    
    for m in marines:
        dis_x = m['pos'][0] - player_pos[0]
        dis_y = m['pos'][1] - player_pos[1]
        if math.hypot(dis_x, dis_y) <= sword_attack_range:
            score += 2
        else:
            survivors.append(m)
    marines[:] = survivors
    while len(marines) < 5: 
        marines.append(new_marines())

    # if boss_enemy and math.hypot(boss_enemy['pos'][0] - player_pos[0], boss_enemy['pos'][1] - player_pos[1]) <= sword_attack_range:
    #     boss_health -= 5
    #     print(f"Zoro Haki Slash hit Boss! Boss Health: {boss_health}")

         
def key_input(key, x, y):
    global game_state, game_win, game_over
    
    if game_state == "menu":
        return  
    else:
        global player_pos, player_rot, game_over, luffy_left_hand_scale, luffy_right_hand_scale
        global zoro_speed_boost, rain_active, rain_used, rain_timer
        global santorio_active, santorio_timer
        global boss_active, boss_enemy, boss_health, shield_counter
        global sword_attack_in_progress, sword_rotation_angle
        
        if game_over or game_win:
            if key == b'r':
                reset_game()
            return
        
        if key == b't':
            if not rain_used and boss_active: 
                rain_active = True
                rain_used = True
                rain_timer = rain_duration  
                init_raindrops()
                print("Rain activated for 15 seconds! Boss will slow down (single use)")
            elif not boss_active:
                print("Rain can only be used when Boss is present!")
            elif rain_used:
                print("Rain power already used!")
        
        speed = 15
        if current_character == "zoro" and zoro_speed_boost and boss_active:
            speed = 20  
        
        arena_limit = (grid_size * tile_size) // 2 - 30
        
        if key == b'w':  # Forward
            ang = math.radians(player_rot)
            new_x = player_pos[0] + (-math.sin(ang)) * speed
            new_y = player_pos[1] + math.cos(ang) * speed
            if abs(new_x) < arena_limit and abs(new_y) < arena_limit:
                player_pos[0], player_pos[1] = new_x, new_y
        
        if key == b's':  # Backward
            ang = math.radians(player_rot)
            new_x = player_pos[0] - (-math.sin(ang)) * speed
            new_y = player_pos[1] - math.cos(ang) * speed
            if abs(new_x) < arena_limit and abs(new_y) < arena_limit:
                player_pos[0], player_pos[1] = new_x, new_y
        
        if key == b'a':  # Rotate left
            player_rot += 5
        
        if key == b'd':  # Rotate right
            player_rot -= 5
    
        #Gum Gum powers
        if current_character == "luffy" and boss_active:
            if key == b'q': 
                luffy_left_hand_scale = min(luffy_left_hand_scale + 0.5, 10.0)
                check_gum_gum_attack('left')
                print(f"Gum-gum Left Hand activated")

            if key == b'e': 
                luffy_right_hand_scale = min(luffy_right_hand_scale + 0.5, 10.0)
                check_gum_gum_attack('right')
                print(f"Gum-gum Right Hand activated")
                
        
        # Santorio power 
        if current_character == "zoro" and boss_active:
            if key == b'e': 
                if boss_active and not santorio_active:
                    santorio_active = True
                    santorio_timer = santorio_duration
                    zoro_speed_boost = True
                    print("Zoro's Santorio dash activated")
                elif not boss_active:
                    print("Santorio unavailable (Boss not present)")
        
        # Fire haki
        if key == b'h':  
            if current_character == "zoro":
                sword_attack_in_progress = True
                sword_rotation_angle = 45.0
                print("Zoro's sword attack initiated!")
                zoro_haki_slash()
            else:  
                fire_haki()
            

def special_keys(k, x, y):
    global camera_azimuth, camera_elevation
    
    if game_over:
        return
        
    if k == GLUT_KEY_LEFT:
        camera_azimuth += 3.0
    if k == GLUT_KEY_RIGHT:
        camera_azimuth -= 3.0 
    if k == GLUT_KEY_UP:
        camera_elevation = min(90.0, camera_elevation + 3.0) 
    if k == GLUT_KEY_DOWN:
        camera_elevation = max(10.0, camera_elevation - 3.0)


def check_gum_gum_attack(hand):
    global boss_health, luffy_left_hand_scale, luffy_right_hand_scale
    if boss_enemy:
        distance = math.sqrt((player_pos[0] - boss_enemy['pos'][0])**2 + 
                           (player_pos[1] - boss_enemy['pos'][1])**2)
        extended_reach = max(luffy_left_hand_scale, luffy_right_hand_scale) * 50
        
        if hand == 'left':
            extended_reach = luffy_left_hand_scale * 50
            if distance <= extended_reach:
                boss_health -= 5
                luffy_left_hand_scale = 1.0 
        elif hand == 'right':
            extended_reach = luffy_right_hand_scale * 50
            if distance <= extended_reach:
                boss_health -= 5
                luffy_right_hand_scale = 1.0

def update_hakis():
    global hakis
    for haki in hakis:
        haki['pos'][0] += haki['dir'][0] * 25
        haki['pos'][1] += haki['dir'][1] * 25
    
    arena_limit = (grid_size * tile_size) // 2
    hakis = [s for s in hakis if abs(s['pos'][0]) < arena_limit and abs(s['pos'][1]) < arena_limit]

def check_collisions():
    global marines, hakis, score, health, game_over, boss_enemy, boss_health, boss_active
    global powerups, shield_active, shield_time, boss_counter, game_win, shield_counter
    global luffy_left_hand_scale, luffy_right_hand_scale
    hit_hakis = []
    hit_marines = []
    
    for i, haki in enumerate(hakis):
        for j, enemy in enumerate(marines):
            distance = math.sqrt((haki['pos'][0] - enemy['pos'][0])**2 + 
                               (haki['pos'][1] - enemy['pos'][1])**2)
            if distance < 30:
                hit_hakis.append(i)
                hit_marines.append(j)
                score += 2
    
    if boss_enemy:
        for i, haki in enumerate(hakis):
            distance = math.sqrt((haki['pos'][0] - boss_enemy['pos'][0])**2 + 
                               (haki['pos'][1] - boss_enemy['pos'][1])**2)
            if distance < 60:
                hit_hakis.append(i)
                boss_health -= 1
    
    for i in sorted(set(hit_hakis), reverse=True):
        if i < len(hakis):
            hakis.pop(i)
    
    for i in sorted(set(hit_marines), reverse=True):
        if i < len(marines):
            marines.pop(i)
            marines.append(new_marines())  
    
    if not shield_active and not santorio_active:
        for enemy in marines:
            distance = math.sqrt((player_pos[0] - enemy['pos'][0])**2 + 
                               (player_pos[1] - enemy['pos'][1])**2)
            if distance < 40:
                health -= 1
                marines.remove(enemy)
                marines.append(new_marines())
                if health <= 0:
                    game_over = True
                break
    
    if boss_enemy and not shield_active and not santorio_active:
        distance = math.sqrt((player_pos[0] - boss_enemy['pos'][0])**2 + 
                           (player_pos[1] - boss_enemy['pos'][1])**2)
        if distance < 80:
            health -= 5
            if health <= 0:
                game_over = True
    
    for powerup in powerups[:]:
        distance = math.sqrt((player_pos[0] - powerup['pos'][0])**2 + 
                           (player_pos[1] - powerup['pos'][1])**2)
        if distance < 25:
            shield_active = True
            shield_counter +=1 
            shield_time = shield_counter * 600 
            powerups.remove(powerup)
    
    if boss_enemy and boss_health <= 0:
        score += 10
        boss_enemy = None
        boss_active = False
        boss_counter += 1
        luffy_left_hand_scale = 1.0
        luffy_right_hand_scale = 1.0
        print(f"Boss defeated! Score updated: {score}")
        print(f"Bosses defeated: {boss_counter}/3")
    if boss_counter == 3:
        game_win = True
        print("Congartulations!! You have defeated all bosses and won the game!")

def update_marines():
    speed_multiplier = 0.2
    for enemy in marines:
        dx = player_pos[0] - enemy['pos'][0]
        dy = player_pos[1] - enemy['pos'][1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 1:
            enemy['pos'][0] += (dx / distance) * speed_multiplier
            enemy['pos'][1] += (dy / distance) * speed_multiplier
    

def update_boss():
    if boss_enemy:
        if rain_active:
            boss_speed = 0.25 
        else:
            boss_speed = 0.5 
        dx = player_pos[0] - boss_enemy['pos'][0]
        dy = player_pos[1] - boss_enemy['pos'][1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 1:
            boss_enemy['pos'][0] += (dx / distance) * boss_speed
            boss_enemy['pos'][1] += (dy / distance) * boss_speed

def setup_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    if camera_mode == "third_person":
        gluPerspective(view_angle, 1.43, 0.1, 2000)
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        cam_x = camera_radius * math.cos(math.radians(camera_elevation)) * math.sin(math.radians(camera_azimuth))
        cam_y = camera_radius * math.cos(math.radians(camera_elevation)) * math.cos(math.radians(camera_azimuth))
        cam_z = camera_radius * math.sin(math.radians(camera_elevation))
        
        gluLookAt(cam_x, cam_y, cam_z, 0, 0, 0, 0, 0, 1)
        
    elif camera_mode == "first_person":
        gluPerspective(100, 1.43, 0.1, 2000) 
        
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        ang = math.radians(player_rot)
        target_x = player_pos[0] + (-math.sin(ang)) * 5
        target_y = player_pos[1] + math.cos(ang) * 5
        
        cam_x, cam_y, cam_z = player_pos[0]+5, player_pos[1]+5, player_pos[2] + 180
        
        gluLookAt(cam_x, cam_y, cam_z,target_x, target_y, cam_z, 0, 0, 1)

def mouse_click(button, state, x, y):
    global camera_mode, game_state, selected_character, current_character
    
    if game_state == "menu" and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        y = 700 - y
        
        if 400 <= x <= 600 and 450 <= y <= 500:
            current_character = selected_character
            reset_game()
            game_state = "playing"
            print(f"Starting game with {current_character.title()}!")
        
        elif 300 <= x <= 450 and 250 <= y <= 300:
            selected_character = "luffy"
            print("Selected Luffy!")
        
        elif 550 <= x <= 700 and 250 <= y <= 300:
            selected_character = "zoro"
            print("Selected Zoro!")
    
    elif game_state == "playing":
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            if camera_mode == "third_person":
                camera_mode = "first_person"
                print("Switched to First-Person Perspective")
            else:
                camera_mode = "third_person"
                print("Switched to Third-Person Perspective")

def reset_game():
    global health, score, game_over, marines, hakis, powerups, boss_enemy, boss_active
    global shield_active, current_character, character_time, luffy_left_hand_scale, luffy_right_hand_scale
    global rain_active,rain_length,rain_speed,n_raindrops, rain_used, rain_timer
    global santorio_active, santorio_timer, zoro_speed_boost, santorio_hit_cooldown
    global sword_attack_in_progress, sword_rotation_angle, boss_counter, game_win, shield_counter
    
    health = 5
    score = 0
    game_over = False
    current_character = selected_character
    character_time = 50.0
    player_pos[0] = player_pos[1] = player_pos[2] = 0
    
    marines.clear()
    hakis.clear()
    powerups.clear()
    boss_enemy = None
    boss_active = False
    shield_active = False
    luffy_left_hand_scale = 1.0
    luffy_right_hand_scale = 1.0
    
    rain_active = False
    raindrops.clear()
    rain_used = False
    rain_timer = 0
    n_raindrops = 200 
    rain_length = 10.0
    rain_speed = 10.0
    
    shield_counter = 0
    shield_time = 0  
    
    boss_counter = 0
    game_win = False
    santorio_active = False
    santorio_timer = 0
    zoro_speed_boost = False

    sword_attack_in_progress = False
    sword_rotation_angle = 0.0
    
    for i in range(5):
        marines.append(new_marines())
        
def handle_santorio_dash():
    global santorio_active, santorio_timer, zoro_speed_boost, boss_health, boss_enemy, score
    global marines, player_pos, santorio_speed, santorio_hit_cooldown, boss_counter

    if santorio_active and current_character == "zoro" and boss_active:
        dx = boss_enemy['pos'][0] - player_pos[0]
        dy = boss_enemy['pos'][1] - player_pos[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx = dx / distance  
            dy = dy / distance
            
            player_pos[0] += dx * santorio_speed  
            player_pos[1] += dy * santorio_speed
        
        arena_limit = (grid_size * tile_size) // 2 - 30
        player_pos[0] = max(-arena_limit, min(arena_limit, player_pos[0]))
        player_pos[1] = max(-arena_limit, min(arena_limit, player_pos[1]))

        if santorio_hit_cooldown > 0:
            santorio_hit_cooldown -= 1

        dist_x = boss_enemy['pos'][0] - player_pos[0]
        dist_y = boss_enemy['pos'][1] - player_pos[1]
        if math.hypot(dist_x, dist_y) <= 120 and santorio_hit_cooldown == 0:
            boss_health -= 5
            santorio_hit_cooldown = 20 
            print(f"Santorio passed through boss! Boss Health: {boss_health}")
        
        # boss_counter += 1
        # print(f'Boss killed {boss_counter}')
        # if santorio_hit_cooldown == 0:
        #     marines_hit = []
        #     for i, m in enumerate(marines):
        #         dis_x = m['pos'][0] - player_pos[0]
        #         dis_y = m['pos'][1] - player_pos[1]
        #         if math.hypot(dis_x, dis_y) <= 80:
        #             marines_hit.append(i)
        #             score += 2
            
        #     for i in sorted(marines_hit, reverse=True):
        #         marines.pop(i)
        #         marines.append(new_enemy())
            
        #     if marines_hit:  
        #         santorio_hit_cooldown = 20

        santorio_timer -= 1
        if santorio_timer <= 0:
            santorio_active = False
            zoro_speed_boost = False
            santorio_hit_cooldown = 0

    elif santorio_active and not boss_active:
        santorio_active = False
        zoro_speed_boost = False
        santorio_hit_cooldown = 0
        

def idle():
    if game_state == "playing":
        global santorio_active, santorio_timer, zoro_speed_boost, boss_health, boss_enemy, score
        global sword_attack_in_progress, sword_rotation_angle, sword_attack_duration

        global rain_active, rain_timer
        if not game_over and not game_win:
            update_character_timer()
            update_shield()
            update_hakis()
            check_collisions()
            update_marines()
            update_boss()
            spawn_boss()
            spawn_powerup()
            update_raindrops()
            
            if rain_active and rain_timer > 0:
                rain_timer -= 1
                if rain_timer <= 0:
                    rain_active = False
                    raindrops.clear()  # rain stops
                    print("Rain effect ended!")
                    
            if sword_attack_in_progress:
                sword_rotation_angle += sword_rotating_speed  
            
            if sword_rotation_angle >= 90: 
                sword_attack_in_progress = False
                sword_rotation_angle = 0.0  

        handle_santorio_dash()
                    
        glutPostRedisplay()

def draw_controls_box():
    
    box_width = 600
    box_height = 40
    box_x = (1000 - box_width) // 2
    box_y = 40
    
    glColor3f(0.1, 0.1, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(box_x, box_y)
    glVertex2f(box_x + box_width, box_y)
    glVertex2f(box_x + box_width, box_y + box_height)
    glVertex2f(box_x, box_y + box_height)
    glEnd()
    
    glColor3f(1, 1, 1)
    draw_text(box_x + 10, box_y + 18, "WASD: Move/Rotate | H: Attack")
    
    if boss_active:
        if current_character == "luffy":
            glColor3f(1.0, 1.0, 0.0)
            draw_text(box_x + 280, box_y + 18, "Q: GUM GUM POWER")
        elif current_character == "zoro":
            glColor3f(1.0, 1.0, 0.0)
            draw_text(box_x + 280, box_y + 18, "Z: SANTORIO")

def draw_info_box():
    
    box_x = 5
    box_y = 450
    box_width = 280
    box_height = 230
    
    start = box_y + box_height - 25
    glColor3f(0.1, 0.1, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(box_x, box_y)
    glVertex2f(box_x + box_width, box_y)
    glVertex2f(box_x + box_width, box_y + box_height)
    glVertex2f(box_x, box_y + box_height)
    glEnd()
    
    glColor3f(1.0, 1.0, 1.0)
    
    if not game_over and not game_win:
        draw_text(box_x + 10, start , f"Character: {current_character.title()}")
        draw_text(box_x + 10, start - 25, f"Time: {int(character_time)}")
        draw_text(box_x + 10, start - 50, f"Health: {health}")
        draw_text(box_x + 10, start - 75, f"Score: {score}")
        
        #player and boss health_bar -> text box
        draw_player_health_bar(box_x + 10, start - 100) 
        if boss_active and boss_enemy:
            glColor3f(1.0, 0.5, 0.5) 
            draw_text(box_x + 10, start - 125, f"Boss Health: {boss_health}")
            draw_crocodile_health_bar(box_x + 10, start - 150)
            
        # shield -> text box
        if shield_active:
            glColor3f(0.5, 1.0, 0.5) 
            draw_text(box_x + 10, start - 175, f"SHIELD ACTIVE: {shield_time//60}s")
        
        #rain -> text box
        glColor3f(1.0, 1.0, 1.0)
        if rain_active:
            glColor3f(0.0, 0.0, 1.0)
            remaining_time = rain_timer // 60
            draw_text(box_x + 10, start - 200, f"Rain: IN USE ({remaining_time}s)")
        elif rain_used:
            glColor3f(0.7, 0.7, 0.7)
            draw_text(box_x + 10, start - 200, "Rain: USED ALREADY")
        elif not boss_active:
            glColor3f(0.9, 0.6, 0.0)
            draw_text(box_x + 10, start - 200, "Rain: INACTIVE (No Boss)")
        else:
            glColor3f(0.0, 1.0, 1.0)
            draw_text(box_x + 10, start - 200, "Rain: Available (T)")
    
    elif game_win:
        glColor3f(1.0, 1.0, 1.0)
        draw_text(box_x + 10, start, "YOU WIN! Congratulations!")
        draw_text(box_x + 10, start - 25, f"Final Score: {score}")
        draw_text(box_x + 10, start - 50, "Press R to Restart")
       
    else:
        glColor3f(1.0, 0.2, 0.2) 
        draw_text(box_x + 10, start, f"GAME OVER! Final Score: {score}")
        glColor3f(1.0, 1.0, 1.0) 
        draw_text(box_x + 10, start - 25, "Press R to Restart")
    
    
        
def showScreen():
    if game_state == "menu":
            draw_menu()
    else:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glViewport(0, 0, 1000, 700)
        setup_camera()
        
        draw_ground()
        for enemy in marines:
            draw_marines(enemy)
            
        draw_crocodile()
        draw_haki()
        draw_powerups()
        draw_raindrops()
        if current_character == "luffy":
            draw_luffy()
        else:
            draw_zoro()
            
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, 1000, 0, 700)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        draw_info_box()
        draw_controls_box()
        
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        
        glutSwapBuffers()


def draw_menu():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 700)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(0.05, 0.05, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(1000, 0)
    glVertex2f(1000, 700)
    glVertex2f(0, 700)
    glEnd()
    
    glColor3f(1.0, 1.0, 0.0)
    draw_text(350, 600, "3D ONE PIECE GAME")
    
    glColor3f(0.2, 0.2, 0.8)
    glBegin(GL_QUADS)
    glVertex2f(400, 450)
    glVertex2f(600, 450)
    glVertex2f(600, 500)
    glVertex2f(400, 500)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    draw_text(450, 470, "NEW GAME")
    
    glColor3f(1.0, 1.0, 1.0)
    draw_text(350, 350, "CHOOSE STARTING CHARACTER:")
    
    if selected_character == "luffy":
        glColor3f(1.0, 0.5, 0.0)  
    else:
        glColor3f(0.5, 0.5, 0.5)  
    glBegin(GL_QUADS)
    glVertex2f(300, 250)
    glVertex2f(450, 250)
    glVertex2f(450, 300)
    glVertex2f(300, 300)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    draw_text(360, 270, "LUFFY")
    
    if selected_character == "zoro":
        glColor3f(0.0, 0.8, 0.0)  
    else:
        glColor3f(0.5, 0.5, 0.5)  
    glBegin(GL_QUADS)
    glVertex2f(550, 250)
    glVertex2f(700, 250)
    glVertex2f(700, 300)
    glVertex2f(550, 300)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)
    draw_text(620, 270, "ZORO")
    
    glColor3f(0.7, 0.7, 0.7)
    draw_text(380, 150, "Click to select and start")
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    glutSwapBuffers()


for i in range(5):
    marines.append(new_marines())

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 700)
    glutInitWindowPosition(100, 50)
    glutCreateWindow(b"3D One Piece Game")

    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(key_input)
    glutSpecialFunc(special_keys)
    glutMouseFunc(mouse_click)
    glutIdleFunc(idle)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
