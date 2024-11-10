import json


# function to iterate through a dictionary and ensure all values are json serializable
# truncates strings at 500 for sake of readability
def make_serializable(obj):
    MAX_STRING_LENGTH = 500

    if isinstance(obj, dict):
        new_dict = {}
        for key, value in obj.items():
            new_dict[key] = make_serializable(value)
        return new_dict
    elif isinstance(obj, list):
        return [make_serializable(item) for item in obj]
    else:
        try:
            json.dumps(obj)
            return obj
        except TypeError:
            try:
                stringified = str(obj)[:MAX_STRING_LENGTH]
                if len(stringified) == MAX_STRING_LENGTH:
                    stringified += "..."
                return stringified
            except Exception:
                return "Unserializable"


def make_serializable_dict(dictionary: dict):
    return make_serializable(dictionary)
