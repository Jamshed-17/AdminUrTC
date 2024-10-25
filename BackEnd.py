import json
from pathlib import Path

def pushing_message_to_admin(kab:str, what:str, comment:str, user:str, time:str):
    """
     Вид базы данных (JSON формат)
    Question: {
        "kab": "45"
        "what": "Не рбаотает интернет"
        "comment": "Нет"
        "user": "@BushmelevaEA"
        "time": "12.10.2024 14:55:26"
        "status": "На обработке"
    }
    
    Ещё нужно обозначить администратора - для этого запишу его id в файлик, с которым потом будет сравниваться входной id
    """
    
    quest = {"kab": kab,
        "what": what,
        "comment": comment,
        "user": f"@{user}",
        "time": time.split(".")[0],
        "status": "onWork"}
    
    
    path = Path('Data/DB.json')
    data = json.loads(path.read_text(encoding='utf-8'))
    data.append(quest)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

pushing_message_to_admin("12", "Привxsacт", "ИРосиворы", "Jamshed", "12:33.232424")
    