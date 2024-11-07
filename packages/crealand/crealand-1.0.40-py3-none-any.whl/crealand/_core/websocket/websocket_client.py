import asyncio
import websockets
import json
import threading
import uuid
import atexit
from crealand._utils._logger_setup import setup_logger

logger = setup_logger()

global_event_loop = None
global_ws_client = None
global_listen_task = None
global_callback = None

class Callback:
    def __init__(self):
        self.callback_dict = {}
        self.broadcast_dict = {}

    def registerCallback(self, callback_id, callback):
        self.callback_dict[callback_id] = callback

    def registerBroadcast(self, info, callback):
        if info not in self.broadcast_dict:
            self.broadcast_dict[info] = []
            
        self.broadcast_dict[info].append(callback)

    def trigger(self, callback_id, err, data):
        if callback_id in self.callback_dict:
            logger.info(f'Find the callback: {callback_id}')
            self.callback_dict[callback_id](err, data)

    def broadcast(self, info):
        if info in self.broadcast_dict:
            logger.info(f'Find the callback: {info}')
            for callback in self.broadcast_dict[info]:
                callback()

def init_callback():
    global global_callback
    if global_callback is None:
        global_callback = Callback()
    return global_callback

def get_callback():
    global global_callback
    return global_callback

# 会话管理器
class WebSocketClient:
    def __init__(self, server_url: str, session_id: str, task_id: str, event_list: list):
        self.server_url = server_url
        self.session_id = session_id
        self.task_id = task_id
        self.event_list = event_list
        self.subscribe_event_msg_id_list = [None for _ in event_list]
        self.failed_event_list = []
        self.websocket = None
        self.connect_lock = threading.Lock()
        self.connected = False
        self.reconnect_interval = 5  # 重连间隔（秒）
        self.condition = asyncio.Event()
        self.init_index = True
        self.sync_msg_response = {}
        self.sync_msg_condition = {}

    async def connect(self):
        with self.connect_lock:
            if self.connected:
                return
            self.websocket = await websockets.connect(self.server_url)
            self.connected = True
            logger.info(f'Connected to {self.server_url}')
            for i in range(len(self.event_list)):
                msg_id = await self.subscribeEvent(self.event_list[i])
                self.subscribe_event_msg_id_list[i] = msg_id
                
    async def sendMessage(self, method: str, params=None):
        logger.info('Start to send message.')
        if not self.websocket or not self.connected:
            logger.error('WebSocket connection closed, attempting to reconnect...')
            self.connected = False
            await self.reconnect()
            
        msg_id = str(uuid.uuid4())
        message = json.dumps({
            'id': msg_id,
            'method': method, 
            'params': [params] if params else [], 
            'jsonrpc':'2.0'
        })
        await self.websocket.send(message)
        logger.info(f'Sent message: {message}')
        if method == 'crealand-api-transfer':
            return params['bridgeMsg']['id']
        else:
            return msg_id

    async def subscribeEvent(self, event_name: str):
        logger.info(f'Start to subscribe the event {event_name}.')
        return await self.sendMessage('rpc.on', event_name)

    async def sendToCrealandApiTransferAsync(self, dest: str, session_id: str, bridge_msg: dict):
        logger.info('Send message to crealand-api-transfer asynchronously.')
        params = {
            'method': 'call',
            'src' : 'sdk',
            'dest' : dest,
            'bridgeMsg': bridge_msg,
            'sessionID': session_id
        }
        if await self.sendMessage('crealand-api-transfer', params):
            return True
        else:
            return False

    async def sendToCrealandApiTransfer(self, dest: str, session_id: str, bridge_msg: dict):
        logger.info('Send message to crealand-api-transfer synchronously.')
        params = {
            'method': 'call',
            'src' : 'sdk',
            'dest' : dest,
            'bridgeMsg': bridge_msg,
            'sessionID': session_id
        }
        msg_id = await self.sendMessage('crealand-api-transfer', params)
        self.sync_msg_response[msg_id] = None
        self.sync_msg_condition[msg_id] = asyncio.Event()
        await self.sync_msg_condition[msg_id].wait()
        del self.sync_msg_condition[msg_id]
        response = self.sync_msg_response[msg_id]
        del self.sync_msg_response[msg_id]
        return response

    async def listen(self):
        try:
            msg_response_id = None
            msg_response_err = None
            msg_response_data = None
            async for message in self.websocket:
                data = json.loads(message)
                logger.info(f'Received message: {data}')
                if 'id' in data:
                    if data['id'] in self.subscribe_event_msg_id_list:
                        index = self.subscribe_event_msg_id_list.index(data['id'])
                        event_name = self.event_list[index]
                        if 'result' in data:
                            if event_name in data['result'] and data['result'][event_name] == 'ok':
                                logger.info(f'Subscribed to the event {event_name}')
                                if event_name in self.failed_event_list:
                                    self.failed_event_list.remove(event_name)
                            else:
                                logger.info(f'Fail to subscribe the event {event_name}')
                                self.failed_event_list.append(event_name)
                                await asyncio.sleep(self.reconnect_interval)
                                msg_id = await self.subscribeEvent(event_name)
                                self.subscribe_event_msg_id_list[index] = msg_id
                        else:
                            logger.info(f'Fail to subscribe the event {event_name}')
                            self.failed_event_list.append(event_name)
                            await asyncio.sleep(self.reconnect_interval)
                            msg_id = await self.subscribeEvent(event_name)
                            self.subscribe_event_msg_id_list[index] = msg_id
                elif 'notification' in data:
                    if data['notification'] in self.event_list:
                        if ('params' in data and len(data['params']) > 0 
                            and 'bridgeMsg' in data['params'][0] 
                            and 'id' in data['params'][0]['bridgeMsg']
                            and 'code' in data['params'][0]['bridgeMsg']):
                            if data['params'][0]['bridgeMsg']['code'] == 0:
                                if 'data' in data['params'][0]['bridgeMsg']:
                                    #logger.info(f'Received event {data["notification"]} params: {data["params"][0]["bridgeMsg"]["id"]}')
                                    msg_response_id = data['params'][0]['bridgeMsg']['id']
                                    msg_response_err = None
                                    msg_response_data = data['params'][0]['bridgeMsg']['data']
                            else:
                                if 'msg' in data['params'][0]['bridgeMsg']:
                                    msg_response_id = data['params'][0]['bridgeMsg']['id']
                                    msg_response_err = data['params'][0]['bridgeMsg']['code']
                                    msg_response_data = data['params'][0]['bridgeMsg']['msg']
                        elif (msg_response_id and 'params' in data and len(data['params']) > 0
                            and 'msgId' in data['params'][0] and 'msgEnd' in data['params'][0]
                            and data['params'][0]['msgId'] == msg_response_id
                            and data['params'][0]['msgEnd']):
                                logger.info(f'message id: {msg_response_id}')
                                logger.info('Start to trigger the callback')
                                api_callback = get_callback()
                                threading.Thread(
                                    target=api_callback.trigger, 
                                    args=(
                                        msg_response_id, 
                                        msg_response_err,
                                        msg_response_data, 
                                    )
                                ).start()
                                if (msg_response_id in self.sync_msg_response 
                                    and msg_response_id in self.sync_msg_condition):
                                    self.sync_msg_response[msg_response_id] = msg_response_data
                                    self.sync_msg_condition[msg_response_id].set()

                                msg_response_id = None
                                msg_response_err = None
                                msg_response_data = None

                if self.init_index and len(self.failed_event_list) == 0:
                    self.init_index = False
                    self.condition.set()
        except websockets.ConnectionClosed:
            logger.error('WebSocket connection closed, attempting to reconnect...')
            self.connected = False
            await self.reconnect()
        except Exception as e:
            logger.error(f'An error occurred: {e}')
        
    async def reconnect(self):
        while not self.connected:
            with self.connect_lock:
                if not self.connected:
                    await asyncio.sleep(self.reconnect_interval)
                    await self.connect()

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            self.connected = False
            logger.info('WebSocket connection closed')

def init_event_loop():
    global global_event_loop
    if global_event_loop is None:
        global_event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(global_event_loop)
    return global_event_loop

def get_event_loop():
    global global_event_loop
    return global_event_loop

def get_ws_client():
    global global_ws_client
    return global_ws_client

def get_listen_task():
    global global_listen_task
    return global_listen_task

def exit_thread():
    logger.info('Start to execute the exit function.')
    task = get_listen_task()
    if task:
        task.cancel()
    loop = get_event_loop()
    if loop:
        ws_client = get_ws_client()
        task = asyncio.run_coroutine_threadsafe(ws_client.close(), loop)
        task.result()
        loop.call_soon_threadsafe(loop.stop)
        while True:
            if not loop.is_running():
                loop.close()
                break

    logger.info('Exit function has finished.')

async def ws_connect_async(server_url, session_id, task_id):
    global global_ws_client
    event_list = ['crealand-event-oncall-sdk']
    global_ws_client = WebSocketClient(server_url, session_id, task_id, event_list)
    # 尝试连接并订阅事件
    await global_ws_client.connect()
    # 在后台监听事件
    global global_listen_task
    global_listen_task = asyncio.create_task(global_ws_client.listen())
    # 阻塞直到订阅事件成功
    await global_ws_client.condition.wait()
    global_ws_client.condition = None

def ws_connect(server_url, session_id, task_id):
    try:
        # 注册退出执行程序
        atexit.register(exit_thread)
        # 获取全局事件循环
        loop = init_event_loop()
        loop.run_until_complete(ws_connect_async(server_url, session_id, task_id))
        loop.run_forever()
    except Exception as e:
        logger.error(f'An error occurred: {e}')

