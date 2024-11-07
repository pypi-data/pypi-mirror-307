# 正式版本号
__version__ = '1.0.40'
# 测试版本号
# __version__ = '1.0.9'

from ._utils._logger_setup import (
    enable_user_log, 
    disable_user_log, 
    setup_logger
)

def __initialize():
    import os
    from ._utils._logger_setup import set_log_dir

    server_url = os.getenv('ENV_CREALAND_UCODELINK_SERVER_URL')
    session_id = os.getenv('ENV_CREALAND_SESSIONID')
    task_id = os.getenv('ENV_CREALAND_TASKID')
    enable_log = os.getenv('ENV_CREALAND_SDK_ENABLE_LOG')
    log_dir = os.getenv('ENV_CREALAND_SDK_DIR')

    if enable_log == 'True':
        enable_user_log()
    if log_dir:
        set_log_dir(log_dir)

    logger = setup_logger()
    logger.info(f'server_url: {server_url}, session_id: {session_id}, \
task_id: {task_id}, enable_log: {enable_log}, log_dir: {log_dir}')
    try:
        import time
        import threading
        from ._core.bridge._interface import call_api
        from ._core.websocket.websocket_client import ws_connect, get_ws_client, init_callback
        threading.Thread(target=ws_connect, args=(server_url, session_id, task_id, )).start()
        while True:
            time.sleep(0.1)
            ws_client = get_ws_client()
            if (ws_client and ws_client.websocket and 
                ws_client.connected and ws_client.session_id):
                break
        init_callback()
        call_api('web-ide', "api.prepareCompleted", [{}])
    except Exception as e:
        logger.error(f'An error occurred: {e}')

__initialize()

from ._apis import (
    ai as AI, 
    detect as Detect, 
    event as Event, 
    interactive as Interactive, 
    object as Object
)

from ._apis._constants import (
    KeyType, 
    KeyActiveType, 
    HangPointType, 
    Actions, 
    AxisType, 
    Tone, 
    Volume, 
    OptionName, 
    ResultType, 
    ToastPosition, 
    ToastState, 
    Direction,  
    FilterStyle, 
    ActionType
)

from ._apis.interactive import (
    Dialogue, 
    HelpPanel, 
    TaskPanel, 
    Speak, 
    Interactive
)

from ._apis.media import (
    Sound, 
    Video, 
    Image
)

from ._apis.sensor import (
    Ultrasonic, 
    Auditory, 
    Visual, 
    Temperature, 
    Humidity, 
    Gravity
)


