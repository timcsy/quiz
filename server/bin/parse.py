import json
import pandas as pd
import os
import sys
import magic
mime = magic.Magic(mime=True)

def is_json(path):
    with open(path) as f:
        try:
            json.load(f)
            return True
        except ValueError as e:
            return False
    return False

def parse(path, print_result = True):
    path = os.path.relpath(path)
    mimetype = mime.from_file(path)

    df = None
    if mimetype == 'application/json':
        df = pd.read_json(path)
    elif mimetype == 'text/plain' and is_json(path):
        df = pd.read_json(path)
    elif mimetype == 'text/csv':
        df = pd.read_csv(path)
    elif mimetype == 'application/vnd.ms-excel':
        df = pd.read_excel(path)
    elif mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(path)
    elif mimetype == 'application/zip' and path.endswith('.xlsx'):
        df = pd.read_excel(path)
    else:
        return 'Invalid mimetype: ' + mimetype

    output = json.loads(df.to_json(orient='index'))
    return output

if __name__ == '__main__':
    path = os.path.relpath(sys.argv[1] if len(sys.argv) > 1 else '.')
    print(json.dumps(parse(path, print_result=False)))