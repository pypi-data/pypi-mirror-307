from dataclasses import dataclass
from typing import Any


@dataclass(kw_only=True)
class BaseConf:
    backend: str | None = None

    def __repr__(self):
        type_name = type(self).__name__
        fields = self.dict_wo_none(self.__dict__)
        return f"{type_name} {fields}"

    def set_to_none(self, keys: list[str]):
        for key in keys:
            if hasattr(self, key):
                setattr(self, key, None)

    def move(self, source_keys: list[str], target_key: str):
        if not hasattr(self, target_key):
            raise ValueError(f"{type(self).__name__} does not have attribute {target_key}")
        if getattr(self, target_key) is not None:
            return

        source_keys = [key for key in source_keys if getattr(self, key) is not None]

        if len(source_keys) == 0:
            return
        elif len(source_keys) == 1:
            value = getattr(self, source_keys[0])
            setattr(self, target_key, value)
            self.set_to_none(source_keys[0])
        else:
            first_value = getattr(self, source_keys[0])
            if all(first_value == getattr(self, key) for key in source_keys):
                setattr(self, target_key, first_value)
                self.set_to_none(source_keys)
            else:
                raise ValueError(f"{source_keys} have different values")

    @staticmethod
    def dict_wo_none(dict_: dict[str, Any]):
        return {key: value for key, value in dict_.items() if value is not None}
