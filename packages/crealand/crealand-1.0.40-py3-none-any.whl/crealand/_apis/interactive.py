from crealand._core.bridge import _interface
from crealand._apis import _constants
from typing import Union
from crealand._utils import _utils

class Dialogue:
    # 立绘对话 获取选项
    option_value = ''
    @staticmethod
    def get_option_value():
        return Dialogue.option_value

    # 立绘对话 初始化
    @staticmethod
    def init():
        _interface.call_api('web-ide', "api.prepareDialogBoard", [{}])
        

    # 立绘对话 显示
    @_utils.check_type
    @staticmethod
    def set_dialogue(
        obj_name: str,
        content: str,
        res_id: str='',
        volume: str = _constants.Volume.MEDIUM,
    ):
        _interface.call_api(
            'web-ide',
            "api.showDialog",
            [
                {
                    "speaker": obj_name,
                    "type": volume,
                    "txt": content,
                    "voiceId": '',
                    "pythonOssId":res_id,
                }
            ],
        )
    
    @_utils.check_type
    @staticmethod
    def set_dialogue_tone(
        obj_name: str,
        content: str,
        res_id: str='',
        tone: str='',
        volume: str = _constants.Volume.MEDIUM,
    ):
        _interface.call_api(
            'web-ide',
            "api.showDialog",
            [
                {
                    "speaker": obj_name,
                    "type": volume,
                    "txt": content,
                    "voiceId": tone,
                    "pythonOssId":res_id,
                }
            ],
        )

    # 立绘对话 设置选项
    @_utils.check_type
    @staticmethod
    def set_option( content: str, opt_name: str = _constants.OptionName.OPTION01):
        options = {}
        options[opt_name] = content
        _interface.call_api(
            'web-ide',
            "api.setDialogOptions",
            [{"options": options}],
        )

    # 立绘对话选项 显示
    @staticmethod
    def set_option_show(is_show: bool = True):
        Dialogue.option_value = _interface.call_api('web-ide', "api.toggleDialogOptions", [{"show": is_show}])
    #  立绘对话 显示
    @staticmethod
    def show(is_show: bool = True):
        if is_show == False:
            Dialogue.option_value = ''
            
        _interface.call_api('web-ide', "api.toggleDialogBoard", [{"show": is_show}])


class HelpPanel:
    # 帮助面板 初始化
    @staticmethod
    def init():
        _interface.call_api('web-ide', "api.prepareHelpboard", [{}])

    # 帮助面板 设置标题
    @_utils.check_type
    @staticmethod
    def set_tips(title: str, res_id: str=''):
        _interface.call_api(
            'web-ide',
            "api.addHelpItem",
            [
                {
                    "title": title,
                    "pythonOssId": res_id,
                }
            ],
        )

    # 帮助面板 显示
    @_utils.check_type
    @staticmethod
    def show(is_show: bool = True):
        _interface.call_api(
            'web-ide',
            "api.toggleHelpboard",
            [
                {
                    "show": is_show,
                }
            ],
        )


class TaskPanel:

    # 任务面板 设置标题
    @_utils.check_type
    @staticmethod
    def set_task(title: str, nickname: str):
        _interface.call_api(
            'web-ide',
            "api.createTaskboard",
            [
                {
                    "title": title,
                    "alias": nickname,
                }
            ],
        )

    # 任务面板 设置任务项
    @_utils.check_type
    @staticmethod
    def set_task_progress(
        task_name: str, subtasks_content: str, completed_tasks: int, total_tasks: int
    ):
        _interface.call_api(
            'web-ide',
            "api.setTaskboard",
            [
                {
                    "alias": task_name,
                    "taskName": subtasks_content,
                    "process": [max(0, completed_tasks), max(1, total_tasks)],
                }
            ],
        )

    # 任务面板 显示
    @_utils.check_type
    @staticmethod
    def set_task_show(task_name: str, is_show: bool = True):
        _interface.call_api(
            'web-ide',
            "api.toggleTaskboard",
            [{"alias": task_name, "show": is_show}],
        )


class Speak:
    # 说
    @_utils.check_type
    @staticmethod
    def text( runtime_id: Union[int,float], content: str, time: int = 2):
        _interface.call_api_async(
            'unity', "unity.actor.speak", [runtime_id, content, time]
        )

    # 说-img
    @_utils.check_type
    @staticmethod
    def image(runtime_id: Union[int,float], res_id: str, time: int = 2):
        _interface.call_api_async(
           'unity', "unity.actor.speakImage", [runtime_id, res_id, time]
        )


class Interactive:
    # 提示面板显示
    @_utils.check_type
    @staticmethod
    def set_tip_show(option: str = _constants.ResultType.START):
        _interface.call_api(
            'web-ide',
            "api.showTipboardResult",
            [
                {
                    "result": option,
                }
            ],
        )

    # 提示面板显示
    @_utils.check_type
    @staticmethod
    def toast(
        content: str,
        position: str = _constants.ToastPosition.TOP,
        state: str = _constants.ToastState.DYNAMIC,
    ):
        _interface.call_api_async(
            'web-ide',
            "api.toast",
            [
                {
                    "position": position,
                    "mode": state,
                    "txt": content,
                }
            ],
            
        )
