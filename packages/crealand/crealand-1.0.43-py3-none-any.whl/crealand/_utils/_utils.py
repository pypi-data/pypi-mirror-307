from typing import Any, Union, Callable, List, Tuple, Set, Dict, get_origin, get_args, Generic, TypeVar, _GenericAlias,Literal
from functools import wraps
from crealand._utils import _logger_setup
import inspect
from inspect import signature
_logger = _logger_setup.setup_logger()
# 限制参数值范围
def value_range(
    val: float,
    min: float = float("-inf"),
    max: float = float("-inf"),
):
    if val < min:
        val = min
    elif val > max:
        val = max
    return val

def Handle_point(value: tuple):
    result = {"id": value[0]}
    if len(value) ==2:
        result["name"] = value[1]
    return result

def check_type(func):
    @wraps(func)
    def inner(*args, **kwargs):
        # 获取原始函数
        original_func = func
        is_classmethod = isinstance(original_func, classmethod)
        if isinstance(original_func, (staticmethod, classmethod)):
            original_func = original_func.__func__
        
        # 获取函数的类型注解
        annotations = original_func.__annotations__

        # 获取函数的签名信息
        signature = inspect.signature(original_func)
        parameters = signature.parameters

        # 获取函数的参数名称
        arg_names = list(parameters.keys())

        # 处理 classmethod 的 cls 参数
        cls_arg=None
        if is_classmethod:
            if args:
                cls_arg=args[0]
                arg_names = arg_names[1:] 
            elif 'cls' in kwargs:
                cls_arg=kwargs.pop('cls')
                arg_names = arg_names[1:]
            else:
                raise TypeError(f"{original_func.__name__}() missing 1 required positional argument: 'cls'")

        # 检查位置参数数量
        if len(args) > len(arg_names):
            raise TypeError(f"{original_func.__name__}() takes {len(arg_names)} positional arguments but {len(args)} were given")
        
        # 检查位置参数
        for i, arg in enumerate(args):
            if i < len(arg_names):
                param_name = arg_names[i]
                param = parameters[param_name]
                if param_name in annotations:
                    annotation = annotations[param_name]
                    if not is_instance_of(arg, annotation):
                        raise TypeError(f"{original_func.__name__}() argument type wrong: {param_name} must be of type {annotation}, but got {type(arg)}")
        
        # 检查关键字参数
        for key, value in kwargs.items():
            if key in parameters:
                param = parameters[key]
                if param.default == inspect.Parameter.empty and key in annotations:
                    annotation = annotations[key]
                    if not is_instance_of(value, annotation):
                        raise TypeError(f"{original_func.__name__}() argument type wrong: {key}  must be of type {annotation}, but got {type(value)}")

        # 检查是否有未传递的必需参数
        provided_args = list(args) + list(kwargs.keys())
        required_params = [name for name in arg_names if name not in provided_args and parameters[name].default == inspect.Parameter.empty]
        if len(provided_args) <len(required_params):
            raise TypeError(f"{original_func.__name__}() missing {len(required_params) - len(provided_args)} required positional arguments: {', '.join(required_params[len(provided_args):])}")
        # if required_params:
        #     raise TypeError(f"{original_func.__name__}() missing {len(required_params)} required positional arguments: {', '.join(required_params)}")
        
        if is_classmethod:
            ar=arg_names
            a=args
            k=kwargs
            return original_func(cls_arg, *args, **kwargs)
        else:
            return original_func(*args, **kwargs)
    
    def is_instance_of(value, annotation):
        if annotation is Any:
            return True
        if get_origin(annotation) is Union:
            return any(is_instance_of(value, t) for t in get_args(annotation))
        elif annotation is Callable:
            return callable(value)
        elif get_origin(annotation) in (List, Tuple, Set, Dict,Literal):
            if get_origin(annotation) is Literal:
                return value in get_args(annotation)
            if not isinstance(value, get_origin(annotation)):
                return False
            if not get_args(annotation):  # 如果没有指定元素类型，直接返回 True
                return True
            if get_origin(annotation) is dict:
                key_type, value_type = get_args(annotation)
                return all(is_instance_of(k, key_type) and is_instance_of(v, value_type) for k, v in value.items())
            else:
                element_type = get_args(annotation)[0]
                return all(is_instance_of(item, element_type) for item in value)
        elif isinstance(annotation, type):
            return isinstance(value, annotation)
        elif isinstance(annotation, _GenericAlias):
            origin = get_origin(annotation)
            args = get_args(annotation)
            if origin is None:
                return False
            if not isinstance(value, origin):
                return False
            if args:
                if origin is dict:
                    key_type, value_type = args
                    return all(is_instance_of(k, key_type) and is_instance_of(v, value_type) for k, v in value.items())
                elif origin in (list, tuple, set):
                    element_type = args[0]
                    if get_origin(annotation) is Union:
                        return any(is_instance_of(item, element_type) for item in value)
                    else:
                        return all(is_instance_of(item, element_type) for item in value)
            return True
        return False
    
    return inner

def raise_error(func,err,data):
    if err > 0:
        raise Exception(f"Error occurred:func {func} {err}, {data}")
    else:
        _logger.info(f"Error occurred:func {func} {err}, {data}")