import pygame, socket, json, threading, copy

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def cook(arg=None,**kwargs):
    if arg:
        data = json.dumps(arg   )+'\n'
    else:
        data = json.dumps(kwargs)+'\n'
    return data.encode()
def send(arg=None,**kwargs):
    if arg:
        data = json.dumps(arg   )+'\n'
    else:
        data = json.dumps(kwargs)+'\n'
    client.send(data.encode())
def uncook(data):
    return json.loads(data.decode())

direction = [0,0]
SCREEN = (600,400)
index = 0
offset = [0,0]
COLOR = None
self = None

colors = {
    '000' : 'black',
    '001' : 'blue',
    '010' : 'green',
    '011' : 'cyan',
    '100' : 'red',
    '101' : 'magenta',
    '110' : 'yellow',
    '111' : 'white'
}

running = True
clock = pygame.Clock()
dt = 0 

pygame.init()
screen = pygame.display.set_mode(SCREEN)

text_fields = []
selected_field = ''

class TextField():
    char_check = {
        'int' : ['0','1','2','3','4','5','6','7','8','9','.']
    }
    def __init__(self,pos,size,font=pygame.font.SysFont('consolas',12),default_text = '',data_type='string'):
        self.data_type = data_type
        self.font = font
        self.color = 'black'
        self.bgcolor = 'white'
        self.text = default_text

        self.image = pygame.Surface(size=size)
        self.image.fill(self.bgcolor)
        self.image.blit(self.font.render(self.text,False,self.color),(0,0))
        
        self.rect = pygame.Rect(pos[0],pos[1],size[0],size[1])
    def insert(self,char):
        text = ''
        buffer = []
        for character in self.text:
            buffer.append(character)
        if char == '\x08':
            if len(buffer):
                buffer.pop()
            for character in buffer:
                text += character
            self.text = text
        elif char == '\r':
            pass
        else:
            if self.data_type == 'string':
                self.text += char
            else:
                if char in self.char_check[self.data_type]:
                    self.text += char

        self.image.fill(self.bgcolor)
        self.image.blit(self.font.render(self.text,False,self.color),(0,0))
    def backspace(self):
        self.text

    def draw(self):
        global screen
        screen.blit(self.image,self.rect)



players = []
objects = []
#(list[player]['pos'],list[player]['angle'],list[player]['color']

def handler():
    global client, running, COLOR, index, players
    buffer = ''
    while running:
        raw_data = client.recv(1024).decode()
        buffer += raw_data
        while '\n' in buffer:
            string_data, buffer = buffer.split('\n',1)
            if string_data:
                data = json.loads(string_data)
                if data:
                    match data['type']:
                        case 'players':
                            if COLOR:
                                with lock:
                                    players = data['data']
                                    for i, player in enumerate(players):
                                        if player[2] == COLOR:
                                            index = i
                        case 'objects':
                            with lock:
                                objects = data['data']
                                for i, object in enumerate(objects):
                                    if object[2] == COLOR:
                                        index = i
                        case _:
                            pass
def send_direction():
    global direction, running
    while running:
        send(type='move',dir=direction)
        pygame.time.delay(int(1000/15))

key_translate = {
    True  : {True: 0,False:-1},
    False : {True: 1,False: 0}
}

lock = threading.Lock()
handler_thread   = threading.Thread(target=handler  )
direction_thread = threading.Thread(target=send_direction)


def setup():
    global dt, running, mouse, screen, text_fields, selected_field, colors, handler_thread, direction_thread
    complete = False
    while running and not complete:
        mouse= pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if selected_field:
                    selected_field.insert(event.unicode)
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_field = None
                for field in text_fields:
                    if field.rect.collidepoint(mouse[0],mouse[1]):
                        selected_field = field
        screen.fill(pygame.color.Color(70,30,30))

        for field in text_fields:
            field.draw()

        pygame.display.flip()
        dt = clock.tick(30)/1000
    selected_field = None
    
    handler_thread  .start()
    direction_thread.start()
    main()

def main():
    global players, objects, direction, screen, key, mouse, colors, selected_field, text_fields, dt, running
    while running:
        key  = pygame.key.get_pressed()
        mouse= pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if selected_field:
                    selected_field.insert(event.unicode)
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected_field = None
                for field in text_fields:
                    if field.rect.collidepoint(mouse[0],mouse[1]):
                        selected_field = field
        screen.fill(pygame.color.Color(70,30,30))

        direction = [key_translate[key[pygame.K_a]][key[pygame.K_d]],key_translate[key[pygame.K_w]][key[pygame.K_s]]]

        with lock:
            current_players = players.copy()
            current_objects = objects.copy()

        for player in current_players:
            try:
                pygame.draw.rect(screen,color=colors[player[2]],rect=pygame.Rect(player[0][0],player[0][1],16,16))
            except:
                print(player)

        pygame.display.flip()
        dt = clock.tick(30)/1000
setup()

handler_thread  .join()
direction_thread.join()
print('Client Ended')