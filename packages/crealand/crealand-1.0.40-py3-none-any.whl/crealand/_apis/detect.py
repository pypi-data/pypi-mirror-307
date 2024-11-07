from crealand._core.bridge import _interface
from crealand._apis import _subscribe_event
from crealand._utils import _utils
from typing import Any, Union

_decibel_val = 0

# 分贝值
def get_decibel_value():
    global _decibel_val
    return _decibel_val

# 开始识别
def start_decibel_recognition():

    def cb_wrapper(err,data):
        if err is None:
           global _decibel_val
           _decibel_val = data['data']
        else:
            _utils.raise_error('start_decibel_recognition',err,data)

    _subscribe_event.onSensorSoundEvent('==','',cb_wrapper)

# 结束识别
def stop_decibel_recognition():
    _interface.call_api_async('web-ide', 'api.openDecibelDetectionPage', [{'type':'end'}])

@_utils.check_type
def onEventDecibel(decibel_value:Union[int,float],cb:Any):
    decibel_value = max(0, min(decibel_value, 150))
    def cb_wrapper(err,data):
        if err is None:
           global _decibel_val
           _decibel_val = data['data']
           cb()
        else:
            _utils.raise_error('onEventDecibel',err,data)


    _subscribe_event.onSensorSoundEvent('>',decibel_value,cb_wrapper)


# 获取虚拟相机
@_utils.check_type
def virtual_camera(runtime_id: Union[int,float],status: bool=True):
    _interface.call_api('unity', 'unity.camera.openVirsual', [runtime_id,status])
