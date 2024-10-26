import json
from pathlib import Path

def check_new_question():
    path = Path('Data/DB.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    print("ИОИОАРЫИАОРВИОРМАВИОРВМАИРОВАМИВМАОЛИВЛАМРОИВМАОЛ")
    data1 = json.loads(path.read_text(encoding='utf-8'))
    if data1 == data:
        pass
    else:
        data = data1
