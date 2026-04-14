import socket, pygame, threading, json, time
import numpy as np

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(('10.144.36.139',52007))

clients = []
objects = []

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

positions = {
    '000' : [10,10],
    '001' : [40,10],
    '010' : [0,0],
    '011' : [0,0],
    '100' : [0,0],
    '101' : [0,0],
    '110' : [0,0],
    '111' : [40,40]
}

players = {
}

running = True
clock = pygame.Clock()
idk = ''

def _data(**kwargs):
    return kwargs
def cook(arg=None,**kwargs):
    if arg:
        data = json.dumps(arg)+'\n'
        return data.encode()
    else:
        data = json.dumps(arg)+'\n'
        return data.encode()
def uncook(data):
    return json.loads(data.decode())

def cmd():
    global idk, running
    while running:
        idk = input()
        if idk == 'quit':
            running = False

def broadcast(data):
    if clients != []:
        for client in clients.copy():
            print(len(players))
            client.send(cook(arg=data))

def physics():
    global players, running, clients
    t = 0
    dt = 0
    step = 1/30
    while running:
        t0 = time.time()
        player_list = players.copy()
        object_list = objects.copy()
        client_list = clients.copy()

        t += dt

        while t >= step:
            for index in player_list:
                player = player_list[index]
                direction = np.array(player['dir'],float)
                magnitude = np.linalg.norm(direction)
                if magnitude != 0:
                    player['spd'] += (step*20*direction)/magnitude
                else:
                    player['spd'] += [0.0,0.0]
                player['spd'] -= step*player['spd']/player['friction']
                player['pos'] += player['spd']
                player['rect'].topleft = player['pos']
                for object in object_list:
                    if player['rect'].colliderect(object['rect']):
                        player['pos'] -= player['spd']
                        player['rect'].topleft = player['pos']
                        player['spd'] = -player['spd']/4
                for p2 in player_list:
                    if index != p2 and player['rect'].colliderect(player_list[p2]['rect']):
                        player['pos'] -= player['spd']
                        player['rect'].topleft = player['pos']
                        player_list[p2]['spd'] += player['spd']/4
                        player['spd'] = -player['spd']/4
            t -= step
        data = _data(type='physics',players=[],objects=[])
        ready= False
        if len(player_list):
            for player in player_list:
                data['players'].append((player_list[player]['rect'].topleft,player_list[player]['angle'],player_list[player]['color']))
            ready = True
        if len(object_list) and object_list != objects:
            for object in object_list:
                data['objects'].append((object['rect'].topleft,object['color']))
            ready = True
        if ready:
            broadcast(data)
        dt = time.time() - t0

def valid_colors(client=socket.socket):
    invalids = []
    check = players.copy()
    for player in check:
        invalids.append(check[player]['color'])
    data = _data(type='valid',colors=invalids)
    client.send(cook(data))

def move(address,data):
    try:
        players[address]['dir'] = data['dir']
    except:
        print(':(')

def shoot(address,data):
    pass

def enter_game(client,address,data):
    invalids = []
    check = players.copy()
    for player in check:
        invalids.append(check[player]['color'])
    if data['color'] in colors and not (data['color'] in invalids):
        players[address] = {
            'rect'    : pygame.rect.Rect(0,0,16,16),
            'pos'     : np.array(positions[data['color']],float),
            'spd'     : np.array([0,0],float),
            'dir'     : (0,0),
            'angle'   : 0,
            'color'   : data['color'],
            'friction': 0.9
        }
    client.send(cook(type='enter',data=data['color']))
    

def handler(client,address):
    print(f'[NEW CLIENT] {address}')
    print(type(client))
    clients.append(client)
    buffer = ''
    while running:
        try:
            thread = None
            raw_data = client.recv(1024).decode()
            buffer += raw_data
            while '\n' in buffer:
                string_data, buffer = buffer.split('\n',1)
                if string_data:
                    data = json.loads(string_data)
                    if data['type'] != 'move':
                        print(f'[COMMAND: {data['type']}] {address}')
                    match data['type']:
                        case 'valid':
                            thread = threading.Thread(target=valid_colors,args=[client])    
                        case 'move':
                            thread = threading.Thread(target=move,args=[address,data])      
                        case 'shoot':
                            thread = threading.Thread(target=shoot,args=[address,data])     
                        case 'enter':
                            thread = threading.Thread(target=enter_game,args=[client,address,data])
                        case _:
                            print('[NULL DATA]')
                    thread.start() if thread else print(end='')
        except:
            try: clients.remove(client)
            except: pass
            try: del players[address]
            except: pass
            print(f'[PLAYER DISCONECTED] {address}')
            return
            
server.listen(8)

threading.Thread(target=physics).start()
threading.Thread(target=cmd).start()
print('[SERVER RUNNING]')
while running:
    client, address = server.accept()
    threading.Thread(target=handler,args=[client,address]).start()

