import json
import os
from typing import Iterator, Dict
from wmain.base import create_path


class WSave:
    """
    manual save
    just allow class attribute type: int, float, str, bool, list, dict
    >>> class A(WSave):
    ...     def __init__(self):
    ...         self.a = 1
    ...         self.b = [1, 2, 3]
    ... 
    ... a = A()
    ... a.save('test.json')
    ... a.a = 2
    ... a.save()
    ... a.b.append(4)
    ... a.save()
    ... a.c = {'a': 1, 'b': 2}
    ... a.save()
    
    """
    __save_allow_types__ = (int, float, str, bool, list, dict)
    __save_attr_whitelist__ = [
        "__save_filepath__",
        "__save_callback__",
        "__dict__",
    ]
    
    def bind_save_file(self, filepath: str) -> None:
        self.__save_filepath__ = filepath
        for instance in self.__save_iter_instances__():
            instance.__dict__["__save_callback__"] = self.save

        if not os.path.exists(filepath):
            self.save()
        else:
            with open(filepath, "r") as f:
                attr_dict = dict(json.load(f))
                self.__save_load_attr_dict__(attr_dict)
                
    def save(self) -> None:
        if "__save_filepath__" in self.__dict__:
            create_path(self.__save_filepath__)
            attr_dict = self.__save_get_attr_dict__()
            with open(self.__save_filepath__, "w") as f:
                json.dump(attr_dict, f)
        elif "__save_callback__" in self.__dict__:
            object.__getattribute__(self, "__save_callback__")()

    def __save_iter_instances__(self) -> Iterator["WSave"]:
        for v in self.__dict__.values():
            if isinstance(v, WSave):
                yield v
                yield from v.__save_iter_instances__()

    def __save_get_attr_dict__(self) -> dict:
        attr_dict = {}
        for k, v in self.__dict__.items():
            if k in self.__save_attr_whitelist__:
                continue
            if isinstance(v, self.__save_allow_types__):
                attr_dict[k] = v
            elif isinstance(v, WSave):
                attr_dict[k] = v.__save_get_attr_dict__()
            else:
                raise TypeError(
                    f"Type {type(v)} of Attribute {k} in {type(self)} is not allowed to be saved."
                )
        return attr_dict

    def __save_load_attr_dict__(self, attr_dict: dict):
        for k, v in attr_dict.items():
            target_type = type(self.__dict__.get(k))
            if target_type in self.__save_allow_types__:
                self.__dict__[k] = target_type(v)
            elif issubclass(target_type, WSave):
                self.__dict__: Dict[str, WSave]
                self.__dict__[k].__save_load_attr_dict__(v)
            else:
                raise TypeError(
                    f"Type {target_type} of Attribute {k} in {type(self)} is not allowed to be saved."
                )


class WAutoSave(WSave):
    """
    this class will auto save when attribute changed
    >>> class B(WAutoSave):
    ...     def __init__(self):
    ...         self.b = [1, 2, 3]
    ... 
    ... class A(WAutoSave):
    ...     def __init__(self):
    ...         self.a = B()
    ... 
    ... a = A()
    ... a.a = 2
    ... a.b.append(4)
    ... a.c = {'a': 1, 'b': 2}

    Args:
        WSave (_type_): _description_
    """

    __save_allow_types__ = (int, float, str, bool)
    __save_attr_whitelist__ = [
        "__save_filepath__",
        "__save_callback__",
        "__dict__",
    ]

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if (
            not callable(getattr(self, name, None))
            and name not in self.__save_attr_whitelist__
        ):
            self.save()
