import time
from crealand._core.bridge import _interface
from crealand._apis import _subscribe_event, _constants
from typing import Any, Union
from crealand._utils import _utils

# 超声波传感器

class Ultrasonic:
    _sensors = {}

    # 前端处理传感器信息绑定
    @_utils.check_type
    @staticmethod
    def add_sensor(sensor: str, runtime_id: Union[int,float], attachment_id: tuple) ->None:
        attach=_utils.Handle_point(attachment_id)
        Ultrasonic._sensors[sensor] = (runtime_id, attach)

    @_utils.check_type
    @staticmethod
    def get_sensor(sensor: str) -> list:
        if sensor in Ultrasonic._sensors:
            return Ultrasonic._sensors[sensor]
        else:
            raise KeyError(f"Sensor '{sensor}' not found")

    @_utils.check_type
    @staticmethod
    def onSensorUltrasonicEvent(sensor: str, compare: str, distance: Union[int,float],cb:Any):
        sensor_info = Ultrasonic.get_sensor(sensor) 
        attachment_id = sensor_info[1]
        def cb_wrapper(err,data):
            if err is None:
                cb()
            else:
                _utils.raise_error('onSensorUltrasonicEvent',err,data)

        _subscribe_event.onSensorUltrasonicEvent(sensor_info[0],attachment_id,compare,distance,cb_wrapper)

    @_utils.check_type
    @staticmethod
    def get_obstacle_distance(sensor: str)->Union[int,float]:
        time.sleep(_constants.SLEEP_TIME)
        sensor_info = Ultrasonic.get_sensor(sensor) 
        length = _interface.call_api('unity', 'unity.sensor.ultrasonicRanging', [sensor_info[0], sensor_info[1]])
        return length

class Auditory:

    _decibel_val=0

    @_utils.check_type
    # 获取声音强度
    @staticmethod
    def get_decibel_value():
        return Auditory._decibel_val

    @_utils.check_type
    @staticmethod
    def onSensorSoundEvent(compare:str,decibel_value:Union[int,float],cb:Any):
        decibel_value = max(0, min(decibel_value, 150))
        def cb_wrapper(err,data):
            if err is None:
                if data and data.get('data') and data['data'] != '':
                    Auditory._decibel_val = data['data']
                    cb()
            else:
                _utils.raise_error('onSensorSoundEvent',err,data)

        _subscribe_event.onSensorSoundEvent(compare,decibel_value,cb_wrapper)

    # 开始分贝识别
    @_utils.check_type
    @staticmethod
    def start_decibel_recognition():
        def cb_wrapper(err,data):
            if err is None:
                if data and data.get('data') and data['data'] != '':
                    Auditory._decibel_val = data['data']
            else:
                _utils.raise_error('start_decibel_recognition',err,data)

        _subscribe_event.onSensorSoundEvent('==','',cb_wrapper)

    # 结束分贝识别
    @_utils.check_type
    @staticmethod
    def stop_decibel_recognition():
        _interface.call_api_async('web-ide', 'api.openDecibelDetectionPage', [{'type':'end'}])


class Visual:
    _sensors = {}

    # 将传感器绑定到对象的挂点
    @_utils.check_type
    @staticmethod
    def add_sensor( sensor: str, runtime_id: Union[int,float], attachment_id: tuple):
        attach=_utils.Handle_point(attachment_id)
        Visual._sensors[sensor] = (runtime_id, attach)

    # 获取传感器信息
    @_utils.check_type
    @staticmethod
    def get_sensor( sensor: str):
        if sensor in Visual._sensors:
            return Visual._sensors[sensor]
        else:
            raise KeyError(f"Sensor '{sensor}' not found")

    # 打开或关闭传感器画面
    @_utils.check_type
    @staticmethod
    def open_visual_sensor( sensor: str,action_type: bool=True):
        sensor_info=Visual.get_sensor(sensor)
        if action_type:
            func_name = 'unity.sensor.openVision'
            _interface.call_api('unity',func_name,[sensor_info[0], sensor_info[1],sensor])
        else:
            func_name = 'unity.sensor.closeVision'
            _interface.call_api('unity',func_name,[sensor])

class Temperature:

    _sensors = {}

    @_utils.check_type
    @staticmethod
    def add_sensor(sensor: str, runtime_id: Union[int,float]) ->None:
        Temperature._sensors[sensor] = runtime_id
        _interface.call_api('unity','unity.sensor.attachTemperature',[runtime_id])

    @_utils.check_type
    @staticmethod
    def get_sensor(sensor: str) -> int:
        if sensor in Temperature._sensors:
            return Temperature._sensors[sensor]
        else:
            raise KeyError(f"Sensor '{sensor}' not found")

    @_utils.check_type
    @staticmethod
    def onSensorTemperatureEvent(sensor:str, compare:str, temperature:Union[int,float],cb:Any):
        temperature = max(-40, min(temperature, 120))
        runtime_id = Temperature.get_sensor(sensor)
        def cb_wrapper(err,data):
            if err is None:
                cb()
            else:
                _utils.raise_error('onSensorTemperatureEvent',err,data)
        _subscribe_event.onSensorTemperatureEvent(runtime_id,compare,temperature,cb_wrapper)
    
    # 设置判定区域温度
    @_utils.check_type
    @staticmethod
    def set_temperature( area_id: Union[int,float], temp_val: Union[int,float]=0):
        temp_val = max(-40, min(temp_val, 120))
        _interface.call_api('unity','unity.sensor.setTemperature',[area_id,temp_val])

    # 持续检测判定区域温度
    @_utils.check_type
    @staticmethod
    def startTemperatureDetection(area_id:Union[int,float]):
        _subscribe_event.startTemperatureDetection(area_id)

    # 获取温度值
    @_utils.check_type
    @staticmethod
    def get_temperature_value( sensor: str):
        time.sleep(_constants.SLEEP_TIME)
        runtime_id=Temperature.get_sensor(sensor)
        temperature_value=_interface.call_api('unity','unity.sensor.getTemperature',[runtime_id])
        return temperature_value



class Humidity:

    _sensors = {}

    @_utils.check_type
    @staticmethod
    def add_sensor(sensor: str, runtime_id: Union[int,float]) ->None:
        Humidity._sensors[sensor] = runtime_id
        _interface.call_api('unity','unity.sensor.attachHumidity',[runtime_id])

    @_utils.check_type
    @staticmethod
    def get_sensor(sensor: str) -> int:
        if sensor in Humidity._sensors:
            return Humidity._sensors[sensor]
        else:
            raise KeyError(f"Sensor '{sensor}' not found")

    @_utils.check_type
    @staticmethod
    def onSensorHumidityEvent(sensor:str, compare:str, humidity_value:Union[int,float],cb:Any):
        humidity_value = int(humidity_value)
        humidity_value= max(0, min(humidity_value, 100))
        runtime_id = Humidity.get_sensor(sensor) 
        def cb_wrapper(err,data):
            if err is None:
                cb()
            else:
                _utils.raise_error('onSensorHumidityEvent',err,data)
        _subscribe_event.onSensorHumidityEvent(runtime_id,compare,humidity_value,cb_wrapper)

    # 设置判定区域湿度
    @_utils.check_type
    @staticmethod
    def set_humidity( area_id: Union[int,float], humidity_value: Union[int,float]=0):
        humidity_value = int(humidity_value)
        humidity_value= max(0, min(humidity_value, 100))
        _interface.call_api('unity','unity.sensor.setHumidity',[area_id,humidity_value])

    @_utils.check_type
    @staticmethod
    def get_humidity_value(senser:str):
        time.sleep(_constants.SLEEP_TIME)
        runtime_id=Humidity.get_sensor(senser)
        result= _interface.call_api('unity','unity.sensor.getHumidity',[runtime_id])
        return result

    # 持续检测判定区域湿度
    @_utils.check_type
    @staticmethod
    def startHumidityDetection( area_id: Union[int,float]):
        _subscribe_event.startHumidityDetection(area_id)


class Gravity:

    _sensors = {}

    @_utils.check_type
    @staticmethod
    def add_sensor(sensor: str, area_id: Union[int,float]) ->None:
        Gravity._sensors[sensor] = area_id
        _interface.call_api('unity','unity.sensor.attachGravity',[area_id])

    @_utils.check_type
    @staticmethod
    def get_sensor(sensor: str) -> int:
        if sensor in Gravity._sensors:
            return Gravity._sensors[sensor]
        else:
            raise KeyError(f"Sensor '{sensor}' not found")

    @_utils.check_type
    @staticmethod
    def onSensorGravityEvent(sensor: str, compare: str, gravity_value: Union[int,float],cb:Any):
        gravity_value = int(gravity_value)
        gravity_value= max(0, min(gravity_value, 10000))
        runtime_id = Gravity.get_sensor(sensor)
        def cb_wrapper(err,data):
            if err is None:
                cb()
            else:
                _utils.raise_error('onSensorGravityEvent',err,data)
        _subscribe_event.onSensorGravityEvent(runtime_id,compare,gravity_value,cb_wrapper)

    # 设置对象重力
    @_utils.check_type
    @staticmethod
    def set_gravity( runtime_id: Union[int,float], gravity_value: Union[int,float]=0):
        gravity_value = int(gravity_value)
        gravity_value= max(0, min(gravity_value, 10000))
        _interface.call_api('unity','unity.sensor.setGravity',[runtime_id,gravity_value])

    # 获取重力值
    @_utils.check_type
    @staticmethod
    def get_gravity_value( sensor: str):
        time.sleep(_constants.SLEEP_TIME)
        runtime_id = Gravity.get_sensor(sensor) 
        value= _interface.call_api('unity','unity.sensor.getGravity',[runtime_id])
        return value

