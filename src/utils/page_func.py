__author__ = 'sam'
import json

def tojsonstr(d):
    return json.dumps(d, ensure_ascii=False)

def address_to_display_json(d, _ul):
    def scan(d):
        for a1 in d:
            a1['display'] = _ul(a1['display'])
            if 'children' in a1.keys():
                scan(a1['children'])
    scan(d)
    return tojsonstr(d)

