from crealand._core.bridge import _interface
from crealand._apis import _constants
from crealand._utils import _utils
from typing import List, Union, Literal

# 信息
class Info:

    # 别名对象id
    @_utils.check_type
    @staticmethod
    def get_alias_id(
        nickname: str ,
    ):
        result = _interface.call_api(
            'unity', "unity.alias.getAlias", [nickname]
        )
        return result

    # 获取configID的对象id
    @_utils.check_type
    @staticmethod
    def get_object_id(runtime_id:Union[int,float]) -> int:
        result = _interface.call_api(
            'unity',
            "unity.actor.getConfigID",
           [runtime_id] ,
        )
        return result

    # 获取对象的空间坐标
    @_utils.check_type
    @staticmethod
    def get_object_coordinates(runtime_id: Union[int,float]) :
        result = _interface.call_api(
            'unity', "unity.actor.getCoordinate", [runtime_id]
        )
        return result

    # 获取判定区域中的对象id
    @_utils.check_type
    @staticmethod
    def get_id_in_area(area_id: Union[int,float], config_ids: List[str]) :
        result = _interface.call_api(
            'unity',
            "unity.editableTrigger.getContentRuntimeIds",
            [area_id, config_ids],
        )
        return result

    # 获取空间坐标某个轴的值
    @_utils.check_type
    @staticmethod
    def get_spatial_coordinates(coordinate: List[Union[int,float]], axis: Literal['X', 'Y','Z']='X') :
        AXIS = {"X": 0, "Y": 1, "Z": 2}
        return coordinate[AXIS[axis]]

    # 获取对象的运动方向向量
    @_utils.check_type
    @staticmethod
    def get_motion_vector(runtime_id: Union[int,float]) :
        result = _interface.call_api(
            'unity', "unity.character.getMoveDirection", [runtime_id]
        )
        return result


class Camera:

    # 获取相机ID
    @_utils.check_type
    @staticmethod
    def get_default_id():
        return _interface.call_api(
            'unity', "unity.camera.getDefaultID",[]
        )

    # 获取空间坐标
    @_utils.check_type
    @staticmethod
    def get_object_coordinates(runtime_id: Union[int,float]) :
        result = _interface.call_api(
            'unity', "unity.actor.getCoordinate", [runtime_id]
        )
        return result

    # 相机移动
    @_utils.check_type
    @staticmethod
    def move_to(time: Union[int,float], coordinate: List[Union[int,float]], block: bool = False):
        new_time = max(0, time)
        _interface.call_api(
            'unity',
            "unity.camera.moveTo",
            [Camera.get_default_id(), new_time, coordinate, block ],
        )

    # 调整FOV
    @_utils.check_type
    @staticmethod
    def adjust_FOV(time: Union[int,float] = 1, fov: Union[int,float] = 80):
        new_time = max(0, time)
        new_fov = max(60, min(fov, 120))
        _interface.call_api_async(
            'unity',
            "unity.camera.adjustFOV",
            [Camera.get_default_id(), new_time, new_fov],
        )

    # 相机锁定朝向并移动
    @_utils.check_type
    @staticmethod
    def move_while_looking(
        coordinate_1: List[Union[int,float]],
        time: Union[int,float] = 1,
        coordinate_2: List[Union[int,float]] = [0, 0, 1],
        block: bool = False,
    ):
        new_time = max(0, time)
        _interface.call_api_async(
            'unity',
            "unity.camera.moveWhileLooking",
            [Camera.get_default_id(), new_time, coordinate_2, coordinate_1, block],
        )

    # 获取相机坐标
    @_utils.check_type
    @staticmethod
    def get_camera_coordinate() -> List[Union[int,float]]:
        result = Camera.get_object_coordinates(Camera.get_default_id())
        return result

    # 相机朝向
    @_utils.check_type
    @staticmethod
    def look_at(coordinate: List[Union[int,float]]):
        _interface.call_api_async(
            'unity',
            "unity.camera.lookAt",
            [Camera.get_default_id(), coordinate],
        )

    # 相机跟随
    @_utils.check_type
    @staticmethod
    def follow_target(runtime_id: int, distance: Union[int,float] = 10, is_rotate: bool = True):
        _interface.call_api_async(
            'unity',
            "unity.camera.followTarget",
            [Camera.get_default_id(), runtime_id, distance, is_rotate],
        )

    # 相机结束跟随
    @_utils.check_type
    @staticmethod
    def end_follow_target():
        _interface.call_api_async(
            'unity',
            "unity.camera.stopFollowing",
            [
                Camera.get_default_id(),
            ],
        )

    # 相机 滤镜
    @_utils.check_type
    @staticmethod
    def filters(filter_name: int = _constants.FilterStyle.FOG, state: bool = True):
 
        _interface.call_api_async(
            'unity',
            "unity.camera.openEffect",
            [Camera.get_default_id(), filter_name, state],
        )


class Motion:
    # 创建对象
    @_utils.check_type
    @staticmethod
    def create_object_coordinate(config_id: str, coordinate: List[Union[int,float]]):
        result = _interface.call_api(
            'unity',
            "unity.actor.createObject",
            [config_id, coordinate],
        )
        return result

    # 测距
    @_utils.check_type
    @staticmethod
    def ray_ranging(runtime_id: int, attachment_id: int = (_constants.HangPointType.LEFT_FRONT_WHEEL,)):
        
        result = _interface.call_api(
            'unity',
            "unity.actor.rayRanging",
            [runtime_id, _utils.Handle_point(attachment_id), 20],
        )
        return result

    # 移动
    @_utils.check_type
    @staticmethod
    def move_to(runtime_id: int, coordinate: List[Union[int,float]] = [0, 0, 1]):
        _interface.call_api(
            'unity',
            "unity.actor.setObjectPosition",
            [
                runtime_id,
                coordinate,
            ],
        )

    # 朝向
    @_utils.check_type
    @staticmethod
    def face_towards(runtime_id: Union[int,float], coordinate: List[Union[int,float]] = [0, 0, 1]):
        _interface.call_api(
            'unity',
            "unity.actor.setObjectTowardPosition",
            [
                runtime_id,
                coordinate,
            ],
        )

    # 前进
    @_utils.check_type
    @staticmethod
    def move_forward(
        runtime_id: Union[int,float], speed: Union[int,float] =1, distance: Union[int,float] =3, block: bool = False
    ):
        new_speed = max(1, min(speed, 5))
        _interface.call_api(
            'unity',
            "unity.actor.moveForwardByDistance",
            [
                runtime_id,
                distance,
                abs(distance/new_speed),
            block ,
            ],
        )

    # 对象旋转
    @_utils.check_type
    @staticmethod
    def rotate(runtime_id: Union[int,float], time: Union[int,float]=1, angle: Union[int,float]=90, block: bool = False):
        new_time = max(time, 0)
        _interface.call_api(
            'unity',
            "unity.character.rotateUpAxisByAngle",
            [
                runtime_id,
                angle,
                new_time,
                block 
            ],
        )

    # 云台旋转 & 机械臂旋转
    @_utils.check_type
    @staticmethod
    def ptz(runtime_id: Union[int,float], angle: Union[int,float]=90, block: bool = False):
        _interface.call_api(
            'unity',
            "unity.actor.rotatePTZUpAxisByAngle",
            [runtime_id, angle, abs(angle) / 30, block],
        )

    # 播放动作
    @_utils.check_type
    @staticmethod
    def action(runtime_id: Union[int,float], action: str, block: bool = False):
        _interface.call_api(
            'unity',
            "unity.actor.playAnimation",
            [runtime_id, action, block ],
        )

    # # 将对象吸附到挂点
    @_utils.check_type
    @staticmethod
    def attach_to(absorbed_runtime_id: Union[int,float], absorb_runtime_id: Union[int,float], attachment_id: tuple):
       
        _interface.call_api(
            'unity',
            "unity.actor.attach",
            [absorbed_runtime_id, absorb_runtime_id,  _utils.Handle_point(attachment_id)],
        )

    # 绑定挂点
    @_utils.check_type
    @staticmethod
    def bind_to_object_point(
        runtime_id_1: Union[int,float],
        attachment_id_1: str,
        runtime_id_2: Union[int,float],
        attachment_id_2: str,
    ):
        _interface.call_api(
            'unity',
            "unity.actor.bindAnchor",
            [runtime_id_1, _utils.Handle_point(attachment_id_1), runtime_id_2, _utils.Handle_point(attachment_id_2)],
        )

    # 解除绑定
    @_utils.check_type
    @staticmethod
    def detach(runtime_id: Union[int,float]):
        _interface.call_api(
            'unity',
            "unity.actor.detach",
            [
                runtime_id,
            ],
        )

    # 向画面空间前进
    @_utils.check_type
    @staticmethod
    def move_towards_screen_space(
        runtime_id: Union[int,float], speed: Union[int,float] = 1, direction: List[Union[int,float]] = [0, 0, 1]
    ):
        new_speed = max(1, min(speed, 5))
        _interface.call_api(
            'unity',
            "unity.actor.moveByVelocity",
            [
                runtime_id,
                new_speed,
                2,
                direction,
            ],
        )

    @_utils.check_type
    @staticmethod
    def get_motion_vector(runtime_id: Union[int,float]):
        result = _interface.call_api('unity', "unity.character.getMoveDirection", [runtime_id])
        return result

    # 旋转运动方向向量
    @_utils.check_type
    @staticmethod
    def rotate_to_direction(
        runtime_id: Union[int,float], angle: Union[int,float] = 0, direction: List[Union[int,float]] = [0, 0, 1]
    ):
        _interface.call_api(
            'unity',
            "unity.character.rotateUpAxisByDirection",
            [runtime_id, angle, direction,0],
        )

    # 停止运动
    @_utils.check_type
    @staticmethod
    def stop(runtime_id: Union[int,float]):
        _interface.call_api_async(
            'unity',
            "unity.character.stop",
            [runtime_id],
        )

    # 设置别名
    @_utils.check_type
    @staticmethod
    def create_object(
        config_id: Union[int,float],
        nickname: str,
        coordinate: List[Union[int,float]] = [0, 0, 1],
    ):
        _interface.call_api_async(
            'unity',
            "unity.alias.setAlias",
            [
                nickname,
                Motion.create_object_coordinate(config_id, coordinate),
            ],
        )

    # 销毁对象
    @_utils.check_type
    @staticmethod
    def destroy(runtime_id: Union[int,float]):
        _interface.call_api(
            'unity',
            "unity.alias.destoryObject",
            [
                runtime_id,
            ],
        )

    # 上升
    @_utils.check_type
    @staticmethod
    def rise(
        runtime_id: Union[int,float], speed: Union[int,float] = 3, height: Union[int,float] = 10, block: bool = False
    ):
        new_speed = max(1, min(speed, 5))
        _interface.call_api(
            'unity',
            "unity.character.moveUpByDistance",
            [runtime_id, height, abs(height/new_speed), block],
        )
    # 降落
    @_utils.check_type
    @staticmethod
    def landing(
        runtime_id: Union[int,float] 
    ):
        _interface.call_api(
            'unity',
            "unity.character.land",
            [runtime_id, 3],
        )

    # 获取离自身距离的坐标
    @_utils.check_type
    @staticmethod
    def get_object_local_position(
        runtime_id: Union[int,float], coordinate: List[Union[int,float]] = [0, 0, 1], distance: Union[int,float] = 0
    ):
        result = _interface.call_api_async(
            'unity',
            "unity.actor.getObjectLocalPosition",
            [runtime_id, coordinate, distance],
        )
        return result

    # 移动到指定坐标
    @_utils.check_type
    @staticmethod
    def move_by_point(
        runtime_id: int, time: Union[int,float] = 1, coordinate: List[Union[int,float]] = [0, 0, 1], block: bool = False
    ):
        new_time = max(time, 0)
        _interface.call_api(
            'unity',
            "unity.actor.moveByPoint",
            [runtime_id, new_time, coordinate, block ],
        )

    # 绕坐标轴旋转
    @_utils.check_type
    @staticmethod
    def rotate_by_origin_and_axis(
        runtime_id: Union[int,float],
        time: Union[int,float] = 2,
        point_1: int=_constants.AxisType.LOCAL,
        coordinate_1: List[Union[int,float]] = [0, 0, 0],
        point_2: int=_constants.AxisType.LOCAL,
        coordinate_2: List[Union[int,float]]= [0, 0, 1],
        angle: Union[int,float]=90,
        block: bool = False,
    ):
        new_time = max(time, 0)
        _interface.call_api(
            'unity',
            "unity.actor.rotateByOringinAndAxis",
            [
                runtime_id,
                coordinate_1,
                point_1,
                coordinate_2,
                point_2,
                angle,
                new_time,
                block 
            ],
        )


class Property:
    # 新增自定义属性
    @_utils.check_type
    @staticmethod
    def add_attr(runtime_id: Union[int,float], attr_name: str, attr_value: str):
        _interface.call_api(
            'unity',
            "unity.actor.addCustomProp",
            [runtime_id, attr_name, attr_value],
        )

    # 删除自定义属性
    @_utils.check_type
    @staticmethod
    def del_attr(runtime_id: Union[int,float], attr_name: str):
        _interface.call_api(
            'unity',
            "unity.actor.delCustomProp",
            [runtime_id, attr_name],
        )

    # 修改自定义属性
    @_utils.check_type
    @staticmethod
    def set_attr(runtime_id: Union[int,float], attr_name: str, attr_value: str):
        _interface.call_api(
            'unity',
            "unity.actor.setCustomProp",
            [runtime_id, attr_name, attr_value],
        )

    # 获取自定义属性的值
    @_utils.check_type
    @staticmethod
    def get_value(runtime_id: Union[int,float], attr_name: str):
        result = _interface.call_api(
            'unity',
            "unity.actor.getCustomProp",
            [runtime_id, attr_name],
        )
        return result

    # 获取自定义属性组中某一项的值
    @_utils.check_type
    @staticmethod
    def get_value_by_idx(runtime_id: Union[int,float], index: int = 1):
        result= _interface.call_api(
            'unity',
            "unity.actor.getCustomPropValueByIdx",
            [runtime_id, index],
        )
        return result

    # 获取自定义属性组中某一项的名称
    @_utils.check_type
    @staticmethod
    def get_key_by_idx(runtime_id: Union[int,float], index: int = 1):
        result=_interface.call_api(
            'unity',
            "unity.actor.getCustomPropKeyByIdx",
            [runtime_id, index],
        )
        return result


class Show:
    # 3d文本-RGB
    @_utils.check_type
    @staticmethod
    def set_3D_text_status_rgb(runtime_id: Union[int,float], rgb: List[Union[int,float]] = [255, 255, 255], size: int = 30, text: str = '文本'):
        _interface.call_api(
            'unity',
            "unity.building.set3DTextStatus",
            [runtime_id, rgb, size, text],
        )
