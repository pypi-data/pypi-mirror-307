import asyncio
import uuid
from typing import Literal
from crealand._core.websocket.websocket_client import get_ws_client, get_event_loop, get_callback
from crealand._utils._logger_setup import setup_logger

logger = setup_logger()

# call API
def call_api(dest: Literal['web-ide', 'unity'], func_name: str, func_args: list):
    #logger.info(f'{dest}, {func_name}, {func_args}')
    bridge_msg = {
        'id': str(uuid.uuid4()),
        'func': func_name,
        'args': func_args if func_args else [],
        'callback': 'callbackName'
    }

    loop = get_event_loop()
    ws_client = get_ws_client()
    task = asyncio.run_coroutine_threadsafe(ws_client.sendToCrealandApiTransfer(dest, ws_client.session_id, bridge_msg), loop)
    result = task.result()
    return result

def call_api_async(dest: Literal['web-ide', 'unity'], func_name: str, func_args: list, callback=None):
    #logger.info(f'{dest}, {func_name}, {func_args}, {callback.__name__}')
    bridge_msg_id = str(uuid.uuid4())
    bridge_msg = {
        'id': bridge_msg_id,
        'func': func_name,
        'args': func_args if func_args else [],
        'callback': 'callbackName'
    }

    loop = get_event_loop()
    ws_client = get_ws_client()
    task = asyncio.run_coroutine_threadsafe(ws_client.sendToCrealandApiTransferAsync(dest, ws_client.session_id, bridge_msg), loop)
    result = task.result()    
    if result and callback:
        api_callback = get_callback()
        api_callback.registerCallback(bridge_msg_id, callback)

    return result
