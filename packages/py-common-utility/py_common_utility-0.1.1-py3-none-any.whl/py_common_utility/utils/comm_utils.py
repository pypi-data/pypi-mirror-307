import hashlib
import json
import sys


def dict_to_sha1(input_dict):
    # Serialize the dictionary to a JSON string
    json_str = json.dumps(input_dict, sort_keys=True)
    # Encode the JSON string into bytes
    json_bytes = json_str.encode('utf-8')
    # Compute the SHA-1 hash
    sha1_hash = hashlib.sha1(json_bytes).hexdigest()
    return sha1_hash


def get_memory_size(obj, seen=None) -> int:
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Mark as seen

    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_memory_size(v, seen) for v in obj.values()])
        size += sum([get_memory_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_memory_size(obj.__dict__, seen)
    elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        size += sum([get_memory_size(i, seen) for i in obj])
    return size
