from crealand._core.bridge import _interface
from crealand._apis import _subscribe_event
from crealand._utils import _logger_setup, _utils
from typing import Any

_logger = _logger_setup.setup_logger()

# 人脸识别
# 机器学习
# 数字识别


class Figure:

    _digit=''
    # 打开手写数字识别教学页面
    @staticmethod
    def open_teach_page():
        _interface.call_api('web-ide','api.openDigitRecognitionTeachingPage',[{'name':''}])

    # 打开神经网络教学页面
    @staticmethod
    def open_NN_teach_page():
        _interface.call_api('web-ide','api.openNeuralNetworkTeachingPage',[{'type':''}])

    # 开始手写数字识别
    @staticmethod
    def start_digital_recognition():
        # 识别返回的结果需要设置保存
        # call_api_async('web-ide','api.digitRecognition',[{'type':'start'}])
        def on_result(err,data):
            if err is None:
                if data and data.get('data') and data['data'] != '':
                    Figure._digit = int(data['data'])
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIFigureEvent('',on_result)

    # 结束手写数字识别
    @staticmethod
    def stop_digital_recognition():
        Figure._digit =''
        _interface.call_api_async('web-ide','api.digitRecognition',[{'type':'end'}])

    # 数字识别结果
    @staticmethod
    def get_figure_value():
        return Figure._digit

    # 清除数字识别结果
    @staticmethod
    def clear_figure_value():
        Figure._digit =''
        _interface.call_api('web-ide','api.digitRecognitionClear',[{'type':''}])

    @_utils.check_type
    @staticmethod
    def onAIFigureEvent(number:int,cb:Any):
        # 识别返回的结果需要设置保存
        # call_api_async('web-ide','api.digitRecognition',[{'type':'start'}])
        def on_result(err,data):
            if err is None:
                if data and data.get('data') and data['data'] != '':
                    Figure._digit = int(data['data'])
                    cb()
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIFigureEvent(number,on_result)


# 手势识别
class Gesture:
    _direction=''
    # 开始手势识别 并等待结束
    @staticmethod
    def start_gesture_recognition():
        def on_result(err,data):
            if err is None:
                if data and data.get('data') and data['data'] != '':
                    Gesture._direction = data['data']
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIGestureEvent('',on_result)

    # 结束手势识别
    @staticmethod
    def stop_gesture_recognition():
        Gesture._direction=''
        _interface.call_api_async('web-ide','api.gestureRecognition',[{'type':'end'}])

    # 当前手势识别结果为
    @staticmethod
    def get_gesture_value():
        return Gesture._direction

    # 帽子积木块
    @_utils.check_type
    @staticmethod
    def onAIGestureEvent(direction:str,cb:Any):
        def on_result(err,data):
            if err is None:
                if data and data.get('data') and data['data'] != '':
                    Gesture._direction = data['data']
                    cb()
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIGestureEvent(direction,on_result)

# 语音识别
class Voice:
    _text=''
    # 开始语音识别
    @staticmethod
    def start_voice_recognition():
        def on_result(err,data):
            if err is None:
                if data and data.get('data') and data['data'] != '':
                    Voice._text = data['data']
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIAsrEvent('',on_result)


    # 结束识别
    @staticmethod
    def stop_voice_recognition():
        Voice._text =''
        _interface.call_api('web-ide','api.openVoiceRecognition',[{'type':'end'}])

    # 语音识别结果
    @staticmethod
    def get_voice_value():
        return Voice._text


    # 打开语音识别教学页面
    @staticmethod
    def open_voice_teach_page():
        _interface.call_api('web-ide','api.openVoiceRecognitionTeachingPage',[{'name':''}])

    # 帽子积木块
    @_utils.check_type
    @staticmethod
    def onAIAsrEvent(text:str,cb:Any):
        def on_result(err,data):
            if err is None:
                if data and data.get('data') and data['data'] != '':
                    Voice._text = data['data']
                    cb()
            else:
                _logger.error(f"Error occurred: {err},{data}")

        _subscribe_event.onAIAsrEvent(text,on_result)


