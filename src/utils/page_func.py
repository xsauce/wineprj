__author__ = 'sam'
import json

def tojsonstr(d):
    return json.dumps(d, ensure_ascii=False)
