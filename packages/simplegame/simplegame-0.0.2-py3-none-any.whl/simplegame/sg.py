import multiprocessing
import os
import signal
import tkinter
import time
import threading
from PIL import Image, ImageTk, ImageOps #py -3.12 -m pip install Pillow
import math
import random
import pygame

class Game:
    def __init__(self, width, height, backdrops=[], title="My simple game"):
        self.sprites = []
        self.current_backdrop_idx = 0
        self.backdrop_x = width // 2
        self.backdrop_y = height // 2
        self.window = KeyRepeater()# tkinter.Tk()
        self.window.title(title)
        self.canvas = tkinter.Canvas(self.window, width=width, height=height)
        self.__backdrops = []
        for bg_file in backdrops:
            pil_image = Image.open(bg_file).convert('RGB')
            image = ImageTk.PhotoImage(pil_image)
            self.__backdrops.append(Backdrop(image, pil_image.load(), pil_image.getcolors(pil_image.width * pil_image.height)))
        self.canvas.pack()
        self.window.protocol("WM_DELETE_WINDOW", self.__on_closing)
        self.__is_running = True
        self.__is_paused = False
        self.width = width
        self.height = height
        self.__bg_position_changed = False
        self.__bg_changed = False
        self.__backdrop_id = None
        self.canvas.bind_all('<Motion>', self.__mouse_moved)
        self.canvas.bind('<Button-1>', self.__mouse_left)
        self.canvas.bind_all('<ButtonRelease-1>', self.__mouse_release)
        self.canvas.bind_all('<KeyPress>', self.__key_press, add="+")
        self.canvas.bind_all('<KeyRelease>', self.__key_release, add="+")
        self.mouse_x = None
        self.mouse_y = None
        self.is_mouse_down = False
        self.__keys_pressed = []
        self.__start_time = time.time()
        self.__messages = []
        self.__invoke_bg_event = False
        self.labels = []

    def has_backdrop(self):
        return len(self.__backdrops) > 0
    
    def wait(self, seconds):
        pygame.time.wait(round(seconds * 1000.0))

    def timer(self):
        return time.time() - self.__start_time
    
    def reset_timer(self):
        self.__start_time = time.time()
    
    def __key_press(self, evt):
        if evt.keysym not in self.__keys_pressed:
            self.__keys_pressed.append(evt.keysym)

    def __key_release(self, evt):
        if evt.keysym in self.__keys_pressed:
            self.wait(0.1)
            self.__keys_pressed.remove(evt.keysym)

    def is_key_pressed(self, key):
        return key in self.__keys_pressed

    def __mouse_moved(self, evt):
        self.mouse_x, self.mouse_y = evt.x, evt.y

    def __mouse_left(self, evt):
        self.is_mouse_down = True
        top_sprite = self.get_top_sprite(self.mouse_x, self.mouse_y)
        if top_sprite != None:
            if top_sprite.is_draggable:
                t = threading.Thread(target=self.__drag_sprite, args=[top_sprite])
                t.start()

    def __drag_sprite(self, sprite):
        dx = self.mouse_x - sprite.x
        dy = self.mouse_y - sprite.y
        while self.is_mouse_down:
            sprite.set_x(self.mouse_x - dx)
            sprite.set_y(self.mouse_y - dy)
            pygame.time.wait(100)

    def __mouse_release(self, evt):
        self.is_mouse_down = False

    def create_sprite(self, x, y, costumes):
        sprite = Sprite(costumes, x, y)
        sprite.game = self
        self.sprites.append(sprite)
        return sprite
    
    def create_label(self, x, y, text):
        label = Label(x, y, text)
        self.labels.append(label)
        return label

    def set_backdrop_x(self, x):
        self.backdrop_x = x
        self.__bg_position_changed = True
    
    def set_backdrop_y(self, y):
        self.backdrop_y = y
        self.__bg_position_changed = True

    def change_backdrop_x(self, x):
        self.backdrop_x = self.backdrop_x + x
        self.__bg_position_changed = True
    
    def change_backdrop_y(self, y):
        self.backdrop_y = self.backdrop_y + y
        self.__bg_position_changed = True

    def set_backdrop_idx(self, idx):
        if self.current_backdrop_idx != idx:
            self.current_backdrop_idx = idx
            self.__bg_changed = True

    def next_backdrop(self):
        self.set_backdrop_idx((self.current_backdrop_idx + 1) % len(self.__backdrops))

    def current_backdrop(self):
        return self.__backdrops[self.current_backdrop_idx]
    
    def __draw_backdrop(self):
        if not self.has_backdrop():
            return
        
        if self.__backdrop_id == None:
            self.__backdrop_id = self.canvas.create_image(self.backdrop_x, self.backdrop_y, image=self.current_backdrop().image)
        
        if self.__bg_position_changed:
            self.canvas.coords(self.__backdrop_id, self.backdrop_x, self.backdrop_y)
            self.__bg_position_changed = False

        if self.__bg_changed:
            self.canvas.itemconfig(self.__backdrop_id, image=self.current_backdrop().image)
            self.__bg_changed = False
            self.__invoke_bg_event = True

    def __on_closing(self):
        self.__is_running = False
        
    def __draw_sprite(self, sprite):
        costume_changed = sprite.costume_updated()
        current_costume = sprite.current_costume() 
        if sprite.id == None:
            img = self.__create_costume(current_costume)
            sprite.id = self.canvas.create_image(sprite.x, sprite.y, image=img)         
        
        if sprite.text_changed:
            sprite.text_changed = False
            if sprite.text != '':
                if sprite.text_id == None:
                    sprite.text_id = self.canvas.create_text(0, 0, text=sprite.text, fill="black", font=('Helvetica 15 bold'))
                else:
                    self.canvas.delete(sprite.polygon_id)
                    self.canvas.itemconfigure(sprite.text_id, text=sprite.text)

                self.__draw_text(sprite, current_costume)
            else:
                self.canvas.delete(sprite.polygon_id)
                self.canvas.delete(sprite.text_id)
                sprite.text_id = None

        if sprite.position_changed:
            sprite.position_changed = False
            self.canvas.coords(sprite.id, sprite.x, sprite.y)
            self.__refresh_text(sprite, current_costume)

        if costume_changed:
            img = self.__create_costume(current_costume)
            self.canvas.itemconfig(sprite.id, image=img)
            self.__refresh_text(sprite, current_costume)         

        if current_costume.changed:
            current_costume.changed = False
            img = self.__refresh_costume(sprite, current_costume)
            self.canvas.itemconfig(sprite.id, image=img)
            self.__refresh_text(sprite, current_costume)        

        if sprite.visibility_changed:
            sprite.visibility_changed = False
            if sprite.is_visible:
                self.canvas.itemconfigure(sprite.id, state='normal')
            else:
                self.canvas.itemconfigure(sprite.id, state='hidden')         
        
        if sprite.z_index_changed:
            sprite.z_index_changed = False
            if sprite.z_index_forward:
                self.canvas.tag_raise(sprite.id)
            else:
                self.canvas.tag_lower(sprite.id)           

        if sprite.is_question:
            sprite.is_question = False
            textentry = tkinter.Entry(self.canvas, font=('Helvetica 15 bold'), borderwidth=10, relief=tkinter.FLAT)
            margin = 20
            entry_width = self.width - (2 * margin)
            entry_height = 40
            entry_x = (self.width // 2) 
            entry_y = self.height - (entry_height // 2) - margin
            self.canvas.create_window(entry_x, entry_y, window=textentry, height=50, width=entry_width)
            textentry.focus()
            textentry.bind('<Return>', lambda evt, sp = sprite: sp.set_answer(evt))       

        if sprite.is_deleted:
            sprite.say('')
            self.canvas.delete(sprite.id)
            if sprite.parent != None:
                sprite.parent.children.remove(sprite)
                sprite.parent = None
            self.sprites.remove(sprite)

    def __refresh_text(self, sprite, current_costume):
        if sprite.text_id != None:
            self.canvas.delete(sprite.polygon_id)
            self.__draw_text(sprite, current_costume)

    def __draw_label_border(self, label):
        box = self.canvas.bbox(label.id)
        x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
        d = 10
        t_height = y2 - y1
        t_width = x2 - x1

        ty = label.y + t_height // 2
        tx = label.x + t_width // 2

        self.canvas.coords(label.id, tx, ty)

        box = self.canvas.bbox(label.id)
        x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
        label.rectangle_id =  self.canvas.create_rectangle(x1 - d, y1 - d, x2 + d, y2 + d, fill="white", outline="black", width=2)
        self.canvas.tag_lower(label.rectangle_id, label.id)

    def __draw_label(self, label):
        if label.id == None:
            label.id = self.canvas.create_text(label.x, label.y, text=label.text, fill="black", font=('Helvetica 15 bold'))        
            self.__draw_label_border(label)

        if label.text_changed:
            self.canvas.itemconfig(label.id, text=label.text)
            self.canvas.delete(label.rectangle_id)
            self.__draw_label_border(label)
            label.text_changed = False

        if label.is_deleted:
            self.canvas.delete(label.id)
            self.canvas.delete(label.rectangle_id)
            self.labels.remove(label)

    def __draw_text(self, sprite, current_costume):
        box = self.canvas.bbox(sprite.text_id)
        x1, y1, x2, y2 = box[0], box[1], box[2], box[3]
        t_height = y2 - y1
        t_width = x2 - x1
        is_left = sprite.x < (self.width / 2)
        d = 10

        sprite_height = round(current_costume.cmn.init_height * sprite.size / 100)
        ty2 = sprite.y - sprite_height // 2 - 2 * d
        ty1 = ty2 - t_height
        if is_left:
            tx1 = sprite.x - d
            tx2 = tx1 + t_width
        else:
            tx2 = sprite.x + d
            tx1 = tx2 - t_width

        self.canvas.coords(sprite.text_id, tx1 + t_width // 2, ty1 + t_height // 2)
        polygon = [tx2, ty2 + d]  
        if is_left:
            polygon.extend([tx1 + 2 * d, ty2 + d, tx1 + d, ty2 + 2 * d, tx1 + d, ty2 + d])
        else:  
            polygon.extend([tx2 - d, ty2 + d, tx2 - d, ty2 + 2 * d, tx2 - 2 * d, ty2 + d])
            
        polygon.extend([tx1, ty2 + d, tx1 - d, ty2, tx1 - d, ty1, tx1, ty1 - d, tx2, ty1 - d, tx2 + d, ty1, tx2 + d, ty2, tx2, ty2 + d])
        sprite.polygon_id = self.canvas.create_polygon(polygon, fill="white", outline="black", width=2)
        self.canvas.tag_lower(sprite.polygon_id, sprite.text_id)
        
    def __run_events(self, sprite):
        if len(sprite.events) > 0:
            e_to_delete = []
            for e in sprite.events:
                name = e[0]
                if name == Events.START:
                    self.__event_wrapper(e[1], sprite, name)
                    e_to_delete.append(e)
                elif (name == Events.TIMER_GREATER_THAN 
                      or name == Events.RECEIVE_MESSAGE 
                      or name == Events.BACKDROP_SWITCHES_TO):
                    self.__event_wrapper(e[1], sprite, name, e[2])
                else:
                    parts = name.split('-')
                    if parts[0] == "<KeyPress":
                        self.window.key_bind(parts[1].replace('>', ''), lambda action=e[1], sp = sprite, evt_name=name : self.__event_wrapper(action, sp, evt_name))
                    else:
                        self.canvas.bind_all(name, lambda evt, action=e[1], sp = sprite, evt_name=name : self.__event_wrapper(action, sp, evt_name))
                    e_to_delete.append(e)
            for e in e_to_delete:
                sprite.events.remove(e)

    def __create_costume(self, current_costume):
        if current_costume.image == None:
            if current_costume.cmn.pil_image == None:
                img = Image.open(current_costume.cmn.file).convert('RGBA')
                current_costume.cmn.pil_image = img
            current_costume.image = ImageTk.PhotoImage(current_costume.cmn.pil_image)
            if len(current_costume.cmn.grid) == 0:
                self.__fill_grid(current_costume)
        return current_costume.image
    
    def __refresh_costume(self, sprite, current_costume):
        img = current_costume.cmn.pil_image
        img_dir = sprite.image_direction()
        if img_dir != 0:
            if sprite.rotation_style == RotationStyles.LEFT_RIGHT:
                if img_dir == 180:
                    img2 = ImageOps.mirror(img)
                else:
                    img2 = img
            else:
                img2 = img.rotate(img_dir, expand=True, resample=Image.BICUBIC)
        else:
            img2 = img

        if sprite.size != 100:
            f = sprite.size / 100
            img3 = img2.resize((round(img2.width * f), round(img2.height * f)), resample=Image.BICUBIC)
        else:
            img3 = img2

        current_costume.width = img3.width
        current_costume.height = img3.height
        current_costume.image = ImageTk.PhotoImage(img3)
        return current_costume.image

    def __fill_grid(self, sprite_costume):
        img = sprite_costume.cmn.pil_image
        width = img.width
        height = img.height
        max_count = 100

        if width > max_count:
            cell_width = (width // max_count) + 1
        else:
            cell_width = 1

        if height > max_count:
            cell_height = (height // max_count) + 1
        else:
            cell_height = 1

        sprite_costume.width = width
        sprite_costume.height = height
        sprite_costume.cmn.init_width = width
        sprite_costume.cmn.init_height = height
        sprite_costume.cmn.cell_width = cell_width
        sprite_costume.cmn.cell_height = cell_height

        for x in range(cell_width // 2, width, cell_width):          
            for y in range(cell_height // 2, height, cell_height):
                rgba = img.getpixel((x, y))
                if rgba[3] > 0:
                    r = rgba[0]
                    g = rgba[1]
                    b = rgba[2]
                    if not x in sprite_costume.cmn.grid:
                        sprite_costume.cmn.grid[x] = {}
                    sprite_costume.cmn.grid[x][y] = (r, g, b)

                    if not r in sprite_costume.cmn.rgb:
                        sprite_costume.cmn.rgb[r] = {}
                    if not g in sprite_costume.cmn.rgb[r]:
                        sprite_costume.cmn.rgb[r][g] = []
                    if not b in sprite_costume.cmn.rgb[r][g]:
                        sprite_costume.cmn.rgb[r][g].append(b)

    def __event_wrapper(self, action, sprite, evt_name, arg = None):
        if evt_name == Events.MOUSE_LEFT or evt_name == Events.MOUSE_RIGHT:
            if not sprite.is_on_top(self.mouse_x, self.mouse_y):
                return

        if evt_name == Events.TIMER_GREATER_THAN and self.timer() <= arg:
            return
        
        if evt_name == Events.BACKDROP_SWITCHES_TO and (self.current_backdrop_idx != arg or not self.__invoke_bg_event):
            return
        
        if evt_name == Events.RECEIVE_MESSAGE and not arg in self.__messages:
            return

        t = threading.Thread(target=action, args=[sprite])
        t.start()

    def get_top_sprite(self, x, y):
        objects = self.canvas.find_overlapping(x, y, x + 1, y + 1)
        for sprite in self.sprites[::-1]:
            if sprite.id in objects:
                if sprite.is_touching_xy(x, y):
                    return sprite
        return None

    def run(self):   
        is_paused = False  
        while self.__is_running:      
            if not is_paused:
                is_paused = self.__is_paused
                self.__draw_backdrop()
                for s in self.sprites:
                    self.__draw_sprite(s)
                for s in self.sprites:
                    self.__run_events(s)
                for l in self.labels:
                    self.__draw_label(l)
                self.__messages.clear()
                self.__invoke_bg_event = False              
            self.window.update()
            pygame.time.wait(10)
                   
        process = multiprocessing.current_process()
        os.kill(process.pid, signal.SIGTERM)

    def close_app(self):
        self.__is_running = False

    def stop_all(self):
        self.__is_paused = True

    def are_colors_touching(self, color1, color2):
        for i in range(len(self.sprites) - 1):
            if self.sprites[i].is_color_touching_color(self.sprites[i + 1:len(self.sprites)], color1, color2):
                return True
            if self.sprites[i].is_color_touching_bg_color(color1, color2):
                return True
        if self.sprites[len(self.sprites) - 1].is_color_touching_bg_color(color1, color2):
            return True
        return False

class Label:
    def __init__(self, x , y, text):
        self.id = None
        self.rectangle_id = None
        self.x = x
        self.y = y
        self.text = text
        self.is_deleted = False
        self.text_changed = False

    def update_text(self, text):
        if self.text != text:
            self.text = text
            self.text_changed = True

    def delete(self):
        self.is_deleted = True

class Backdrop:
    def __init__(self, image, pil_image, colors):
        self.image = image
        self.pil_image = pil_image
        self.rgb = {}
        for c in colors:
            r = c[1][0]
            g = c[1][1]
            b = c[1][2]
            if not r in self.rgb:
                self.rgb[r] = {}
            if not g in self.rgb[r]:
                self.rgb[r][g] = []
            if not b in self.rgb[r][g]:
                self.rgb[r][g].append(b)

    def has_color(self, color):
        return has_color(self.rgb, color)

class Events:
    def __init__(self):
        pass

    SPACE = '<space>'
    MOUSE_LEFT = '<Button-1>'
    MOUSE_RIGHT = '<Button-3>'
    ANY_KEY = '<KeyPress>'
    UP = '<KeyPress-Up>'
    DOWN = '<KeyPress-Down>'
    LEFT = '<KeyPress-Left>'
    RIGHT = '<KeyPress-Right>'
    _0 = '<KeyPress-0>'
    _1 = '<KeyPress-1>'
    _2 = '<KeyPress-2>'
    _3 = '<KeyPress-3>'
    _4 = '<KeyPress-4>'
    _5 = '<KeyPress-5>'
    _6 = '<KeyPress-6>'
    _7 = '<KeyPress-7>'
    _8 = '<KeyPress-8>'
    _9 = '<KeyPress-9>'
    A = '<KeyPress-a>'
    B = '<KeyPress-b>'
    C = '<KeyPress-c>'
    D = '<KeyPress-d>'
    E = '<KeyPress-e>'
    F = '<KeyPress-f>'
    G = '<KeyPress-g>'
    H = '<KeyPress-h>'
    I = '<KeyPress-i>'
    J = '<KeyPress-j>'
    K = '<KeyPress-k>'
    L = '<KeyPress-l>'
    M = '<KeyPress-m>'
    N = '<KeyPress-n>'
    O = '<KeyPress-o>'
    P = '<KeyPress-p>'
    Q = '<KeyPress-q>'
    R = '<KeyPress-r>'
    S = '<KeyPress-s>'
    T = '<KeyPress-t>'
    U = '<KeyPress-u>'
    V = '<KeyPress-v>'
    W = '<KeyPress-w>'
    X = '<KeyPress-x>'
    Y = '<KeyPress-y>'
    Z = '<KeyPress-z>'
    START = 'start'
    RECEIVE_MESSAGE = 'message'
    TIMER_GREATER_THAN = 'timer'
    BACKDROP_SWITCHES_TO = 'backdrop'

class Keys:
    def __init__(self):
        pass

    SPACE = 'space'
    UP = 'Up'
    DOWN = 'Down'
    LEFT = 'Left'
    RIGHT = 'Right'
    _0 = '0'
    _1 = '1'
    _2 = '2'
    _3 = '3'
    _4 = '4'
    _5 = '5'
    _6 = '6'
    _7 = '7'
    _8 = '8'
    _9 = '9'
    A = 'a'
    B = 'b'
    C = 'c'
    D = 'd'
    E = 'e'
    F = 'f'
    G = 'g'
    H = 'h'
    I = 'i'
    J = 'j'
    K = 'k'
    L = 'l'
    M = 'm'
    N = 'n'
    O = 'o'
    P = 'p'
    Q = 'q'
    R = 'r'
    S = 's'
    T = 't'
    U = 'u'
    V = 'v'
    W = 'w'
    X = 'x'
    Y = 'y'
    Z = 'z'

class RotationStyles:
    def __init__(self):
        pass

    DONT_ROTATE = 0
    LEFT_RIGHT = 1
    ALL_AROUND = 2

class Sprite:
    def __init__(self, costumes, x, y):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.direction = 0
        self.costumes = []
        for file in costumes:
            self.costumes.append(Costume(file)) 
        self.current_costume_idx = 0
        self.next_costume_idx = 0
        self.events = []
        self.id = None
        self.position_changed = False
        self.size = 100
        self.is_visible = True
        self.visibility_changed = False
        self.z_index_forward = False
        self.z_index_changed = False
        self.rotation_style = RotationStyles.ALL_AROUND
        self.is_draggable = False
        self.text_id = None
        self.polygon_id = None
        self.text = ""
        self.text_changed = False
        self.is_question = False
        self.answer = None
        self.is_deleted = False
        self.volume = 100
        self.parent = None
        self.children = []

    def clone(self):
        c = Sprite([], self.x, self.y)
        c.costumes = []
        for costume in self.costumes:
            new_costume = Costume()
            new_costume.width = costume.width
            new_costume.height = costume.height
            new_costume.changed = self.direction != 0 or self.size != 100 or self.rotation_style != RotationStyles.ALL_AROUND
            new_costume.cmn = costume.cmn
            c.costumes.append(new_costume)
        c.direction = self.direction
        c.current_costume_idx = self.current_costume_idx 
        c.position_changed = self.position_changed
        c.next_costume_idx = self.next_costume_idx
        c.size = self.size
        c.is_visible = self.is_visible
        c.visibility_changed = not self.is_visible
        c.z_index_forward = self.z_index_forward
        c.z_index_changed = self.z_index_changed
        c.rotation_style = self.rotation_style     
        c.is_draggable = self.is_draggable
        c.volume = self.volume
        c.parent = self
        self.children.append(c)
        c.events = []
        for e in self.events:

            if e[0] != Events.START:
                c.add_event(e[0], e[1], e[2])
        c.game = self.game
        self.game.sprites.append(c)
        return c  

    def current_costume(self):
        return self.costumes[self.current_costume_idx]
    
    def image_direction(self):
        if self.rotation_style == RotationStyles.DONT_ROTATE:
            return 0
        elif self.rotation_style == RotationStyles.ALL_AROUND:
            return self.direction
        else:
            d = self.direction % 360
            if d < 270 and d > 90:
                return 180
            else:
                return 0
    
    def move(self, steps):
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = self.x + math.cos(math.radians(self.direction)) * steps
        self.y = self.y - math.sin(math.radians(self.direction)) * steps
        self.position_changed = True
    
    def set_x(self, x):
        self.prev_x = x
        self.x = x
        self.position_changed = True
    
    def set_y(self, y):
        self.prev_y = y
        self.y = y
        self.position_changed = True

    def change_x(self, x):
        self.prev_x = self.x
        self.x = self.x + x
        self.position_changed = True
    
    def change_y(self, y):
        self.prev_y = self.y
        self.y = self.y + y
        self.position_changed = True

    def set_direction(self, direction):
        if self.direction != direction:
            for c in self.costumes:
                c.changed = True
            self.direction = direction

    def set_direction_to_xy(self, x, y):
        if x != None:
            dir = math.atan2(self.y - y, x - self.x)
            self.set_direction(math.degrees(dir))

    def point_towards_mouse(self):
        if self.game.mouse_x != None:
            self.set_direction_to_xy(self.game.mouse_x, self.game.mouse_y)

    def go_to_random(self):
        self.set_x(random.randint(0, self.game.width - 1))
        self.set_y(random.randint(0, self.game.height - 1))

    def go_to_mouse(self):
        if self.game.mouse_x != None:
            self.set_x(self.game.mouse_x)
            self.set_y(self.game.mouse_y)

    def go_to_sprite(self, sprite):
        if sprite.x != None:
            self.set_x(sprite.x)
            self.set_y(sprite.y)

    def change_direction(self, direction):
        if direction != 0:
            for c in self.costumes:
                c.changed = True
            self.direction = self.direction + direction

    def set_rotation_style(self, style):
        if self.rotation_style != style:
            for c in self.costumes:
                c.changed = True
            self.rotation_style = style

    def set_size(self, size):
        if self.size != size:
            for c in self.costumes:
                c.changed = True
            self.size = size

    def change_size(self, size):
        if size != 0:
            for c in self.costumes:
                c.changed = True
            self.size = self.size + size

    def set_volume(self, volume):
        self.volume = volume
    
    def change_volume(self, volume):
        self.volume += volume

    def set_costume(self, idx):
        self.next_costume_idx = idx

    def costume_updated(self):
        if self.next_costume_idx != self.current_costume_idx:
            self.current_costume_idx = self.next_costume_idx
            return True
        return False

    def next_costume(self):
        self.set_costume((self.current_costume_idx + 1) % len(self.costumes))
            
    def show(self):
        self.is_visible = True
        self.visibility_changed = True
    
    def hide(self):
        self.is_visible = False
        self.visibility_changed = True

    def go_backward(self):
        self.z_index_forward = False
        self.z_index_changed = True

    def go_forward(self):
        self.z_index_forward = True
        self.z_index_changed = True

    def add_event(self, name, action, arg = None):
        self.events.append((name, action, arg))

    def get_distance_to_mouse(self):
        if self.game.mouse_x == None:
            return 0
        
        return math.dist([self.game.mouse_x, self.game.mouse_y], [self.x, self.y])
    
    def get_distance_to_sprite(self, sprite):
        return math.dist([sprite.x, sprite.y], [self.x, self.y])

    def glide_to(self, seconds, x, y):
        distance = math.dist([x, y], [self.x, self.y])
        count = int(distance // 10)
        if count > 0:
            time_step = seconds / count
            x_step = (x - self.x) / count
            y_step = (y - self.y) / count
            for i in range(count):
                self.change_x(x_step)
                self.change_y(y_step)
                self.game.wait(time_step)
        self.set_x(x)
        self.set_y(y)

    def __bounce(self, horizontal: bool):
        if horizontal:
            self.set_direction(180 - self.direction)
        else:
            self.set_direction(-self.direction)

    def bounce_if_on_edge(self, steps):
        self.move(steps)
        if (self.is_touching_xy(0, None) 
            or self.is_touching_xy(self.game.width, None)
            or self.x < 0 or self.x > self.game.width):
            self.__bounce(True)
            self.move(steps)
        if (self.is_touching_xy(None, 0) 
            or self.is_touching_xy(None, self.game.height)
            or self.y < 0 or self.y > self.game.height):
            self.__bounce(False)
            self.move(steps)

    def has_color(self, color):
        return has_color(self.current_costume().cmn.rgb, color)
    
    def get_corners(self):
        c = self.current_costume()
        w = c.get_width()
        h = c.get_height()
        return int(self.x - w/2), int(self.y - h/2), int(self.x + w/2), int(self.y + h/2)
    
    def get_top_left(self):
        c = self.current_costume()
        return int(self.x - c.cmn.init_width/2), int(self.y - c.cmn.init_height/2)

    def is_touching_sprite(self, sprite):
        for child in sprite.children:
            if self.is_touching_sprite(child):
                return True
            
        if not sprite.is_visible or not self.is_visible:
            return False

        self_costume = self.current_costume()
        sprite_costume = sprite.current_costume()
        if self_costume.get_width() == None or sprite_costume.get_width() == None:
            return False

        p1x1, p1y1, p1x2, p1y2 = self.get_corners()
        p2x1, p2y1, p2x2, p2y2 = sprite.get_corners()
        top_left_x1, top_left_y1 = self.get_top_left()
        top_left_x2, top_left_y2 = sprite.get_top_left()

        cw1 = self_costume.cmn.cell_width
        ch1 = self_costume.cmn.cell_height
        cw2 = sprite_costume.cmn.cell_width
        ch2 = sprite_costume.cmn.cell_height
        min_cw = min(cw1, cw2)
        min_ch = min(ch1, ch2)
        img_dir1 = self.image_direction()
        img_dir2 = sprite.image_direction()

        if not (p1x2 < p2x1 or p1x1 > p2x2 or p1y1 > p2y2 or p1y2 < p2y1):
            x1 = max(p1x1, p2x1)
            y1 = max(p1y1, p2y1)
            x2 = min(p1x2, p2x2)
            y2 = min(p1y2, p2y2)
            for i in range(x1, x2, min_cw):
                for j in range(y1, y2, min_ch):
                    gxy1 = self.get_grid_coords(i, j, img_dir1, top_left_x1, top_left_y1, cw1, ch1)                   
                    if gxy1[0] in self_costume.cmn.grid:
                        if gxy1[1] in self_costume.cmn.grid[gxy1[0]]:
                            gxy2 = sprite.get_grid_coords(i, j, img_dir2, top_left_x2, top_left_y2, cw2, ch2)    
                            if gxy2[0] in sprite_costume.cmn.grid:
                                if gxy2[1] in sprite_costume.cmn.grid[gxy2[0]]:
                                    return True
            return False
        else:
            return False
        
    def is_touching_mouse(self):
        return self.is_touching_xy(self.game.mouse_x, self.game.mouse_y)
    
    def is_touching_edge(self):
        if self.is_touching_xy(0, None):
            return True
        if self.is_touching_xy(self.game.width, None):
            return True
        if self.is_touching_xy(None, 0):
            return True
        if self.is_touching_xy(None, self.game.height):
            return True
        return False
        
    def is_touching_xy(self, x, y):
        if not self.is_visible:
            return False

        self_costume = self.current_costume()
        if self_costume.get_width() == None:
            return False

        p1x1, p1y1, p1x2, p1y2 = self.get_corners()
        top_left_x1, top_left_y1 = self.get_top_left()

        cw1 = self_costume.cmn.cell_width
        ch1 = self_costume.cmn.cell_height

        img_dir = self.image_direction()

        if y == None:          
            if x != None and x > p1x1 and x < p1x2:
                for j in range(p1y1, p1y2, ch1):
                    gxy1 = self.get_grid_coords(x, j, img_dir, top_left_x1, top_left_y1, cw1, ch1)                   
                    if gxy1[0] in self_costume.cmn.grid:
                        if gxy1[1] in self_costume.cmn.grid[gxy1[0]]:
                            return True
            return False

        if x == None:          
            if y != None and y > p1y1 and y < p1y2:
                for i in range(p1x1, p1x2, cw1):
                    gxy1 = self.get_grid_coords(i, y, img_dir, top_left_x1, top_left_y1, cw1, ch1)                   
                    if gxy1[0] in self_costume.cmn.grid:
                        if gxy1[1] in self_costume.cmn.grid[gxy1[0]]:
                            return True
            return False

        if y == None or x == None:
            return False
        
        if y > p1y1 and y < p1y2 and x > p1x1 and x < p1x2:
            gxy1 = self.get_grid_coords(x, y, img_dir, top_left_x1, top_left_y1, cw1, ch1)
            if gxy1[0] in self_costume.cmn.grid:
                return gxy1[1] in self_costume.cmn.grid[gxy1[0]]
            
        return False
        
    
    def is_touching_color(self, color):
        self_costume = self.current_costume()
        if not self.is_visible or self_costume.get_width() == None:
            return False
        
        p1x1, p1y1, p1x2, p1y2 = self.get_corners()
        top_left_x1, top_left_y1 = self.get_top_left()
        cw1 = self_costume.cmn.cell_width
        ch1 = self_costume.cmn.cell_height
        img_dir1 = self.image_direction()

        for sprite in self.game.sprites:
            sprite_costume = sprite.current_costume()
            if not sprite.is_visible or sprite_costume.get_width() == None:
                continue
         
            p2x1, p2y1, p2x2, p2y2 = sprite.get_corners()    
            top_left_x2, top_left_y2 = sprite.get_top_left()
            cw2 = sprite_costume.cmn.cell_width
            ch2 = sprite_costume.cmn.cell_height
            min_cw = min(cw1, cw2)
            min_ch = min(ch1, ch2)
            img_dir2 = sprite.image_direction()

            if not (p1x2 < p2x1 or p1x1 > p2x2 or p1y1 > p2y2 or p1y2 < p2y1):
                if not sprite.has_color(color):
                    continue
                x1 = max(p1x1, p2x1)
                y1 = max(p1y1, p2y1)
                x2 = min(p1x2, p2x2)
                y2 = min(p1y2, p2y2)
                for i in range(x1, x2, min_cw):
                    for j in range(y1, y2, min_ch):
                        gxy1 = self.get_grid_coords(i, j, img_dir1, top_left_x1, top_left_y1, cw1, ch1)                   
                        if gxy1[0] in self_costume.cmn.grid:
                            if gxy1[1] in self_costume.cmn.grid[gxy1[0]]:
                                gxy2 = sprite.get_grid_coords(i, j, img_dir2, top_left_x2, top_left_y2, cw2, ch2)    
                                if gxy2[0] in sprite_costume.cmn.grid:
                                    if gxy2[1] in sprite_costume.cmn.grid[gxy2[0]]:
                                        if are_colors_the_same(color, sprite_costume.cmn.grid[gxy2[0]][gxy2[1]]):
                                            return True

        if not self.game.has_backdrop():
            return False
            
        bgimg = self.game.current_backdrop().pil_image
        bgw = self.game.current_backdrop().image.width()
        bgh = self.game.current_backdrop().image.height()
        dx = self.game.backdrop_x - round(bgw / 2)
        dy = self.game.backdrop_y - round(bgh / 2)
        size = 10000 / self.size                 
        for x in self_costume.cmn.grid:
            for y in self_costume.cmn.grid[x]:
                ax = x + top_left_x1
                ay = y + top_left_y1
                rij = self.__transform_apsolute(ax, ay, -img_dir1, size)
                rx = round(rij[0])
                ry = round(rij[1])
                if rx < self.game.width and ry < self.game.height and rx >= 0 and ry >= 0:
                    bgx = rx - dx
                    bgy = ry - dy
                    if bgx < bgw and bgy < bgh and bgx >= 0 and bgy >= 0:
                        rgb = bgimg[bgx, bgy]
                        if are_colors_the_same(color, rgb):
                            return True
        
        return False
    
    def is_color_touching_bg_color(self, color1, color2):
        if not self.game.has_backdrop():
            return False
        
        current_bg = self.game.current_backdrop()

        if not (self.has_color(color1) and current_bg.has_color(color2)
                or self.has_color(color2) and current_bg.has_color(color1)):
            return False

        top_left_x, top_left_y = self.get_top_left()
        img_dir = self.image_direction()        
        bgimg = current_bg.pil_image
        bgw = current_bg.image.width()
        bgh = current_bg.image.height()
        cx = self.game.width // 2
        cy = self.game.height // 2
        dx = self.game.backdrop_x - cx
        dy = self.game.backdrop_y - cy
        size = 10000 / self.size        
        self_costume = self.current_costume()         
        for x in self_costume.cmn.grid:
            for y in self_costume.cmn.grid[x]:
                self_color = self_costume.cmn.grid[x][y]
                is_self_color1 = are_colors_the_same(color1, self_color)
                is_self_color2 = are_colors_the_same(color2, self_color)
                if is_self_color1 or is_self_color2:
                    ax = x + top_left_x
                    ay = y + top_left_y
                    rij = self.__transform_apsolute(ax, ay, -img_dir, size)
                    rx = round(rij[0])
                    ry = round(rij[1])
                    if rx < self.game.width and ry < self.game.height and rx >= 0 and ry >= 0:
                        bgx = rx - dx
                        bgy = rx - dx
                        if bgx < bgw and bgy < bgh and bgx >= 0 and bgy >= 0:
                            bg_color = bgimg[rx - dx, ry - dy]
                            is_bg_color1 = are_colors_the_same(color1, bg_color)
                            is_bg_color2 = are_colors_the_same(color2, bg_color)
                            if ((is_self_color1 and is_bg_color2)
                                or (is_self_color2 and is_bg_color1)):
                                return True
        return False
    
    def is_color_touching_color(self, sprites, color1, color2):
        self_costume = self.current_costume()
        if not self.is_visible or self_costume.get_width() == None:
            return False
        
        has_color1 = self.has_color(color1)
        has_color2 = self.has_color(color2)

        if not has_color1 and not has_color2:
            return False
              
        p1x1, p1y1, p1x2, p1y2 = self.get_corners()
        top_left_x1, top_left_y1 = self.get_top_left()
        cw1 = self_costume.cmn.cell_width
        ch1 = self_costume.cmn.cell_height
        img_dir1 = self.image_direction()
        for sprite in sprites:
            sprite_costume = sprite.current_costume()
            if not sprite.is_visible or sprite_costume.get_width() == None:
                continue
       
            p2x1, p2y1, p2x2, p2y2 = sprite.get_corners()
            top_left_x2, top_left_y2 = sprite.get_top_left()
            cw2 = sprite_costume.cmn.cell_width
            ch2 = sprite_costume.cmn.cell_height
            min_cw = min(cw1, cw2)
            min_ch = min(ch1, ch2)
            
            img_dir2 = sprite.image_direction()

            if not (p1x2 < p2x1 or p1x1 > p2x2 or p1y1 > p2y2 or p1y2 < p2y1):
                if not ((sprite.has_color(color1) and has_color2)
                     or (sprite.has_color(color2) and has_color1)):
                    continue
                x1 = max(p1x1, p2x1)
                y1 = max(p1y1, p2y1)
                x2 = min(p1x2, p2x2)
                y2 = min(p1y2, p2y2)
                for i in range(x1, x2, min_cw):
                    for j in range(y1, y2, min_ch):
                        gxy1 = self.get_grid_coords(i, j, img_dir1, top_left_x1, top_left_y1, cw1, ch1)                   
                        if gxy1[0] in self_costume.cmn.grid:
                            if gxy1[1] in self_costume.cmn.grid[gxy1[0]]:
                                self_color = self_costume.cmn.grid[gxy1[0]][gxy1[1]]
                                is_self_color1 = are_colors_the_same(self_color, color1)
                                is_self_color2 = are_colors_the_same(self_color, color2)
                                if is_self_color1 or is_self_color2:
                                    gxy2 = sprite.get_grid_coords(i, j, img_dir2, top_left_x2, top_left_y2, cw2, ch2)    
                                    if gxy2[0] in sprite_costume.cmn.grid:
                                        if gxy2[1] in sprite_costume.cmn.grid[gxy2[0]]:
                                            sprite_color = sprite_costume.cmn.grid[gxy2[0]][gxy2[1]]
                                            is_sprite_color1 = are_colors_the_same(sprite_color, color1)
                                            is_sprite_color2 = are_colors_the_same(sprite_color, color2)
                                            if ((is_self_color1 and is_sprite_color2)
                                                or (is_self_color2 and is_sprite_color1)):
                                                return True
        
        return False

    def __transform_apsolute(self, i, j, img_dir, size):
        if img_dir != 0:
            if self.rotation_style == RotationStyles.LEFT_RIGHT:
                if img_dir == 180:
                    rij = mirror_point(self.x, i, j)
                else:
                    rij = (i, j)
            else:
                rij = rotate_point(self.x, self.y, i, j, img_dir)
        else:
            rij = (i, j)

        if self.size != 100:
            rij = move_point(self.x, self.y, rij[0], rij[1], size)
        return rij
    
    def get_grid_coords(self, i, j, img_dir, top_left_x, top_left_y, cw, ch):
        rij = self.__transform_apsolute(i, j, img_dir, self.size)
        rx = rij[0] - top_left_x
        ry = rij[1] - top_left_y
        gx = (rx // cw) * cw + cw // 2
        gy = (ry // ch) * ch + ch // 2
        return (gx, gy)
    
    def is_on_top(self, x, y):
        top_sprite = self.game.get_top_sprite(x, y)
        if top_sprite != None:
            return top_sprite.id == self.id
        return False
    
    def say(self, text):
        self.text = text
        self.text_changed = True

    def ask(self, text):
        self.say(text)
        self.is_question = True
        while self.answer == None:
            pygame.time.wait(200)
        answer = self.answer
        self.answer = None
        return answer
    
    def set_answer(self, evt):
        self.answer = evt.widget.get()
        evt.widget.destroy()
        self.say("")

    def delete(self):
        self.is_deleted = True

    def broadcast_message(self, message):
        self.game.__messages.append(message)

    def play_sound(self, file):
        mixer = pygame.mixer
        mixer.init()
        sound = mixer.Sound(file)
        sound.set_volume(self.volume / 100)
        channel = sound.play()
        return channel
        
    def play_sound_until_done(self, file):
        channel = self.play_sound(file)
        while channel.get_busy():
            pygame.time.wait(100)
    
class Costume:
    def __init__(self, file = ""):
        self.image = None
        self.width = None
        self.height = None
        self.changed = False
        self.cmn = CostumeCommon(file)
    
    def get_width(self):
        if self.width != None:
            return self.width
        else:
            return self.cmn.init_width
        
    def get_height(self):
        if self.height != None:
            return self.height
        else:
            return self.cmn.init_height
        
class CostumeCommon:
    def __init__(self, file):
        self.file = file
        self.pil_image = None
        self.init_width = None
        self.init_height = None
        self.cell_width = None
        self.cell_height = None
        self.grid = {}
        self.rgb = {}

class KeyRepeater(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current = {}
        self.functions = {}
        self.bind("<KeyPress>", self.keydown, add="+")
        self.bind("<KeyRelease>", self.keyup, add="+")
        self.key_loop()

    def key_loop(self):
        for function in self.current.values():
            if function:
                function()
        self.after(30, self.key_loop)

    def key_bind(self, key, function):
        self.functions[key]=function

    def keydown(self, event=None):
        if event.keysym in self.functions:
            self.current[event.keysym]=self.functions.get(event.keysym)

    def keyup(self, event=None):
        self.current.pop(event.keysym,None)

def has_color(rgb, color):
        r = color[0]
        g = color[1]
        b = color[2]
        if r in rgb:
            if g in rgb[r]:
                if b in rgb[r][g]:
                    return True
        return False

def rotate_point(cx, cy, x, y, agle):
        rad = math.radians(agle)
        s = math.sin(rad)
        c = math.cos(rad)
        x -= cx
        y -= cy

        xnew = x * c - y * s
        ynew = x * s + y * c

        x = xnew + cx
        y = ynew + cy
        return (x, y)

def move_point(cx, cy, x, y, size):
    f = 100 / size
    return (cx + (x - cx) * f, cy + (y - cy) * f)

def mirror_point(cx, i, j):
    return (cx * 2 - i, j)

def are_colors_the_same(color1, color2):
    if color1[0] != color2[0]:
        return False
    if color1[1] != color2[1]:
        return False
    if color1[2] != color2[2]:
        return False
    return True



