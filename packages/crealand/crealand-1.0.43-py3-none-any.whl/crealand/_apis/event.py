from crealand._core.bridge import _interface
from crealand._apis import _subscribe_event, _constants
from crealand._utils import _utils
from typing import Any,Union
import time

#收到广播事件
@_utils.check_type
def onBroadcastEvent(info:str,cb:Any):
    _subscribe_event.onBroadcastEvent(info,cb)

#发送广播事件
@_utils.check_type
def send_broadcast(info:str):
    _subscribe_event.sendBroadcast(info)

#对象进入/离开判定区域事件
@_utils.check_type
def onAreaObjectEvent(runtime_id:Union[int,float],action:int,area_id:Union[int,float],cb:Any):
    def cb_wrapper(err,data):
        if err is None:
            cb()
        else:
            _utils.raise_error('onAreaObjectEvent',err,data)
    _subscribe_event.onAreaObjectEvent(runtime_id,action,area_id,cb_wrapper)

#分类进入/离开判定区域事件
@_utils.check_type
def onAreaClassEvent(config_id:str,action:int,area_id:Union[int,float],cb:Any):
    def cb_wrapper(err,data):
        if err is None:
            cb()
        else:
            _utils.raise_error('onAreaClassEvent',err,data)
    _subscribe_event.onAreaClassEvent(config_id,action,area_id,cb_wrapper)

# 验证按键是否按下
@_utils.check_type
def keypress_state(button:int):
    time.sleep(_constants.SLEEP_TIME)
    result = _interface.call_api('unity',"unity.input.verifyKeyCodeState",[button, _constants.KeyPress.KEY_PRESS])
    return result

# 鼠标键盘事件
@_utils.check_type
def onKeyEvent(action:int,button:int,cb:Any):
    def cb_wrapper(err,data):
        if err is None:
            cb()
        else:
            _utils.raise_error('onKeyEvent',err,data)
    _subscribe_event.onKeyEvent(action,button,cb_wrapper)
