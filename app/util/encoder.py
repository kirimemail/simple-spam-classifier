import json
from app.util import TaskStatus


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TaskStatus):
            return {"__TaskStatus__": str(obj.value)}
        return json.JSONEncoder.default(self, obj)


def as_enum(obj):
    if "__TaskStatus__" in obj:
        value = obj['__TaskStatus__']
        return TaskStatus(value)
    else:
        return obj
