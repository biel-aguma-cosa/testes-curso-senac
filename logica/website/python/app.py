import websockets
import asyncio
import json
import os

async def broadcast(dict):
    global clients
    if len(clients):
        for client in clients.copy():
            try:
                data = json.dumps(dict).encode()
                await client.send(data)
                print(f'[data [{data}] broadcasted]')
            except websockets.ConnectionClosed:
                pass
async def send(client,dict):
    try:
        data = json.dumps(dict).encode()
        await client.send(data)
        print(f'[data [{data}] sent]')
    except websockets.ConnectionClosed:
        pass
async def update_data():
    global global_data
    with open(os.path.join(dir,'global_data.json'),'w') as file:
        file.write(json.dumps(global_data,indent=3))
        file.close()

async def handler(socket):
    global clients,global_data
    while True:
        try:
            do_broadcast = False
            async for _rdata in socket:
                rdata = json.loads(_rdata)
                for thing in rdata:
                    print(thing,':',rdata[thing])
                match rdata['type']:
                    case 'login':
                        logged = False
                        if rdata['user']['name'] in global_data['user_data']:
                            if rdata['user']['password'] == global_data['user_data'][rdata['user']['name']]['password']:
                                logged = True
                            else:
                                data = {'type':'error'}
                        else:
                            global_data['user_data'][rdata['user']['name']] = rdata['user']
                            logged = True
                        if logged:
                            data = {'type':'login','user':rdata['user'],'data':global_data['public_data']}
                            await send(socket,data)
                            socket_data[socket] = rdata['user']
                            if socket not in clients:
                                    clients.add(socket)
                            dummy = []
                            for patient in global_data['patients']:
                                dummy.append(patient)
                            await send(socket,{'type':'patient_list','list':dummy})
                            global_data['all_data'].append({'type':'patient_list','list':dummy})
                            data = {'type':'message','sender':rdata['user']['name'],'message':rdata['user']['name']+' logged in'}
                            do_broadcast = True
                                            
                            socket_data[socket] = rdata['user']
                    case 'message':
                        if rdata['user']['name'] in global_data['user_data']:
                            if rdata['user']['password'] == global_data['user_data'][rdata['user']['name']]['password']:
                                data = {'type':'message','sender':rdata['user']['name'],'message':rdata['message']}
                                do_broadcast = True
                    case 'get_patient':
                        if rdata['user']['name'] in global_data['user_data']:
                            if rdata['user']['password'] == global_data['user_data'][rdata['user']['name']]['password']:
                                data = {'type':'patient_show','patient':global_data['patients'][rdata['patient']]}
                    case 'save_patient':
                         if rdata['user']['name'] in global_data['user_data']:
                            if rdata['user']['password'] == global_data['user_data'][rdata['user']['name']]['password']:
                                if rdata['patient']:
                                    global_data['patients'][rdata['patient']] = rdata['data']
                                    dummy = []
                                    for patient in global_data['patients']:
                                        dummy.append(patient)
                                    data = {'type':'patient_list','list':dummy}
                                    do_broadcast = True
                    case _:
                        data = {'type':'error'}
                global_data['all_data'].append(data)
                if do_broadcast:
                    global_data['public_data'].append(data)
                    await broadcast(data)
                else:
                    await send(socket,data)

                await update_data()
            
        except websockets.ConnectionClosed:
            logged = False
            if socket in clients:
                clients.remove(socket)
                data = {'type':'message','sender':'server','message':socket_data[socket]['name']+' desconectou-se'}
                await broadcast(data)
            break
async def main():
    global clients, socket_data, dir, global_data

    dir = os.path.dirname(os.path.realpath(__file__))


    with open(os.path.join(dir,'global_data.json'),'r') as file:
        global_data = json.loads(file.read())
        file.close()

    clients = set()
    socket_data = {}

    async with websockets.serve(handler,'10.144.36.88',52007):
            print('[server started]')
            await asyncio.Future()

asyncio.run(main())

