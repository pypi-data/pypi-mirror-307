import uuid
import threading
from crealand._core.bridge._interface import call_api_async
from crealand._core.websocket.websocket_client import get_ws_client, get_callback
from crealand._utils._logger_setup import setup_logger

logger = setup_logger()

def _subscribeEvent(dest, func_name, func_args, subscribe_id, callback=None):
    def eventCallback(err, data):
        try:
            logger.info(f'Trigger the event callback. err: {err}, data: {data}')
            if 'type' in data and 'result' in data:
                logger.info('This is an event trigger.')
                if data['type'] == 'trigger' and data['result']:
                    logger.info('The type is trigger.')
                    callback(err, data)
                elif data['type'] == 'callback' and data['result']:
                    logger.info('The type is callback.')
                    ws_client = get_ws_client()
                    call_api_async(
                        dest='web-ide', 
                        func_name='event.addTaskSubscribe', 
                        func_args=[
                            dest, 
                            ws_client.session_id, 
                            ws_client.task_id, 
                            subscribe_id
                        ], 
                        callback=None
                    )
            else:
                logger.info('This is an api trigger.')
                callback(err, data)
            logger.info('Finished!')
        except Exception as e:
            logger.error(f'An error occurred: {e}')

    return call_api_async(dest, func_name, func_args, eventCallback if callback else None)

def onBroadcastEvent(info, callback):
    event_callback = get_callback()
    event_callback.registerBroadcast(info, callback)

def sendBroadcast(info):
    event_callback = get_callback()
    threading.Thread(
        target=event_callback.broadcast, 
        args=(info, )
    ).start()

# Crealand IDE-WEB
def onAIFigureEvent(number, callback):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        'AIFigureEvent', {
            'subscribeId': subscribe_id, 
            'targets': [{
                'name': 'number', 
                'type': 'and', 
                'conditions': {
                    '==': number
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='web-ide', 
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

def onAIGestureEvent(direction, callback):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        'AIGestureEvent', {
            'subscribeId': subscribe_id, 
            'targets': [{
                'name': 'direction', 
                'type': 'and', 
                'conditions': {
                    '==': direction
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='web-ide', 
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

def onAIAsrEvent(text, callback):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        'AIAsrEvent', {
            'subscribeId': subscribe_id, 
            'targets': [{
                'name': 'text', 
                'type': 'and', 
                'conditions': {
                    '==': text
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='web-ide', 
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

def onSensorSoundEvent(compare, decibel_value, callback):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        'SensorSoundEvent', {
            'subscribeId': subscribe_id, 
            'targets': [{
                'name': 'decibel_value', 
                'type': 'and', 
                'conditions': {
                    compare: decibel_value
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='web-ide', 
        func_name='event.subscribeRemoteEvent', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

# Crealand IDE-3D
def onKeyEvent(action, button, callback):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        button, 
        action, {
            'subscribeId': subscribe_id, 
            'targets': []
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.input.onEventKeyCode', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

def onAreaObjectEvent(runtime_id, action, area_id, callback):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        runtime_id, 
        action, 
        area_id, {
            'subscribeId': subscribe_id, 
            'targets': []
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.editableTrigger.onEventRuntimeIdTrigger', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

def onAreaClassEvent(config_id, action, area_id, callback):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        config_id, 
        action, 
        area_id, {
            'subscribeId': subscribe_id, 
            'targets': []
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.editableTrigger.onEventConfigIdTrigger', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

def onSensorUltrasonicEvent(runtime_id, attachment_id, compare, distance, callback):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        runtime_id, 
        attachment_id, {
            'subscribeId': subscribe_id, 
            'targets': [{
                'name': 'distance', 
                'type': 'and', 
                'conditions': {
                    compare: distance
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.sensor.onEventUltrasonicRanging', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

def onSensorTemperatureEvent(temperature_sensor, compare, temperature, callback):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        temperature_sensor, {
            'subscribeId': subscribe_id, 
            'targets': [{
                'name': 'temperature', 
                'type': 'and', 
                'conditions': {
                    compare: temperature
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.sensor.onEventTemperature', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

def onSensorHumidityEvent(humidity_sensor, compare, humidity_value, callback):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        humidity_sensor, {
            'subscribeId': subscribe_id, 
            'targets': [{
                'name': 'humidity_value', 
                'type': 'and', 
                'conditions': {
                    compare: humidity_value
                }}
            ]
        }
    ]
    return _subscribeEvent( 
        dest='unity', 
        func_name='unity.sensor.onEventHumidity', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

def onSensorGravityEvent(gravity_sensor, compare, gravity_value, callback):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        gravity_sensor, {
            'subscribeId': subscribe_id, 
            'targets': [{
                'name': 'gravity_value', 
                'type': 'and', 
                'conditions': {
                    compare: gravity_value
                }}
            ]
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.sensor.onEventGravity', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

def startTemperatureDetection(judge_area_id, callback=None):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        judge_area_id, {
            'subscribeId': subscribe_id, 
            'targets': []
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.sensor.startTemperatureDetection', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

def startHumidityDetection(judge_area_id, callback=None):
    subscribe_id = str(uuid.uuid4())
    func_args = [
        judge_area_id, {
            'subscribeId': subscribe_id, 
            'targets': []
        }
    ]
    return _subscribeEvent(
        dest='unity', 
        func_name='unity.sensor.startHumidityDetection', 
        func_args=func_args, 
        subscribe_id=subscribe_id, 
        callback=callback
    )

