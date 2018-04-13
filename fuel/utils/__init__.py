import json

def printJson(j):
    print(json.dumps(j, indent=2, separators=(',', ': ')))