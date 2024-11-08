from enum import IntEnum

SLEEP_TIME = 0.01

class DestType:
    UNITY = "unity"
    WEB_IDE = "web-ide"


# 键盘按键
class KeyType(IntEnum):
    SPACE = 32
    DIGIT_0 = 48
    DIGIT_1 = 49
    DIGIT_2 = 50
    DIGIT_3 = 51
    DIGIT_4 = 52
    DIGIT_5 = 53
    DIGIT_6 = 54
    DIGIT_7 = 55
    DIGIT_8 = 56
    DIGIT_9 = 57
    A = 97
    B = 98
    C = 99
    D = 100
    E = 101
    F = 102
    G = 103
    H = 104
    I = 105
    J = 106
    K = 107
    L = 108
    M = 109
    N = 110
    O = 111
    P = 112
    Q = 113
    R = 114
    S = 115
    T = 116
    U = 117
    V = 118
    W = 119
    X = 120
    Y = 121
    Z = 122
    NUM_0 = 256
    NUM_1 = 257
    NUM_2 = 258
    NUM_3 = 259
    NUM_4 = 260
    NUM_5 = 261
    NUM_6 = 262
    NUM_7 = 263
    NUM_8 = 264
    NUM_9 = 265
    ARROW_UP = 273
    ARROW_DOWN = 274
    ARROW_RIGHT = 275
    ARROW_LEFT = 276
    SHIFT_RIGHT = 303
    SHIFT_LEFT = 304
    CONTROL_RIGHT = 305
    CONTROL_LEFT = 306
    MOUSE_LEFT = 323
    MOUSE_RIGHT = 324
    MOUSE_MIDDLE = 325


# 鼠标按键动作
class KeyActiveType(IntEnum):
    KEY_DOWN = 2
    KEY_UP = 4

class KeyPress(IntEnum):
    KEY_PRESS = 1

# 挂点
class HangPointType(IntEnum):
    BOTTOM = 1
    CAMERA = 2
    LEFT_FRONT_WHEEL = 3
    RIGHT_FRONT_WHEEL = 4
    LEFT_HAND = 10
    RIGHT_HAND = 11
    ITEM_HANGING_POINT = 100
    CAMERA_FOLLOW_POINT = 1000
    TOP = 2000
    USER_DEFINE = 0


# 角色动作
class Actions:
    PICK = "Pick"
    PLACE = "Place"
    LAUGH = "Laugh"
    HAPPY = "Happy"
    THINK = "Think"
    CONFUSE = "Confuse"
    SAD = "Sad"
    TALK = "Talk"
    GREET = "Greet"
    NO = "No"
    YES = "Yes"
    LOOKAROUND = "LookAround"
    APOLOGIZE = "Apologize"
    APPLAUD = "Applaud"
    BOW = "Bow"
    ANGRY = "Angry"
    FAINT = "Faint"
    ARMRESET = "ArmReset"
    DOWNPICK = "DownPick"
    UPPICK = "UpPick"
    REPAIR = "Repair"
    STANDGUARD = "StandGuard"


# 坐标类型 本地坐标或世界坐标
class AxisType(IntEnum):
    LOCAL = 1
    WORLD = 0


# 说话语气
class Tone:
    BOBO_ANGRY = "img_bobo_angry.png"
    BOBO_EXPRESSION = "img_bobo_expression.png"
    BOBO_SADNESS = "img_bobo_sadness.png"
    BOBO_SHY = "img_bobo_shy.png"
    BOBO_SMILE = "img_bobo_smile.png"
    BOBO_SURPRISE = "img_bobo_surprise.png"
    UU_ANGRY = "img_UU_angry.png"
    UU_EXPRESSION = "img_UU_expression.png"
    UU_SADNESS = "img_UU_sadness.png"
    UU_SHY = "img_UU_shy.png"
    UU_SMILE = "img_UU_smile.png"
    UU_SURPRISE = "img_UU_surprise.png"
    X_ANGRY = "img_x_angry.png"
    X_EXPRESSION = "img_x_expression.png"
    X_SADNESS = "img_x_sadness.png"
    X_SHY = "img_x_shy.png"
    X_SMILE = "img_x_smile.png"
    X_SURPRISE = "img_x_surprise.png"
    Y_ANGRY = "img_y_angry.png"
    Y_SADNESS = "img_y_expression.png"
    Y_SADNESS = "img_y_sadness.png"
    Y_SHY = "img_y_shy.png"
    Y_SMILE = "img_y_smile.png"
    Y_SURPRISE = "img_y_surprise.png"


# 音量大小
class Volume:
    LARGE = "large"
    MEDIUM = "medium"
    SMALL = "small"


# 立绘对话选项
class OptionName:
    OPTION01 = "option1"
    OPTION02 = "option2"
    OPTION03 = "option3"


# 提示面板展示内容
class ResultType:
    SUCCESS = "success"
    FAIL = "failure"
    START = "start"


# Toast提示位置
class ToastPosition:
    TOP = "top"
    BOTTOM = "bottom"
    MIDDLE = "middle"


# Toast提示状态
class ToastState:
    DYNAMIC = "dynamic"
    STATIC = "static"


# 手势方向
class Direction:
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"


# 滤镜类型
class FilterStyle(IntEnum):
    FOG = 1


# 对象的动作
class ActionType(IntEnum):
    ENTER = 1
    LEAVE = -1
