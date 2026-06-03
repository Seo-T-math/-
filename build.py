import json
from datetime import datetime

with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('viewer.html', 'r', encoding='utf-8') as f:
    viewer = f.read()

json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
updated_at = datetime.now().strftime('%Y년 %m월 %d일 %H:%M')

result = viewer.replace('__DASHBOARD_DATA__', json_str).replace("'__UPDATED_AT__'", f"'{updated_at}'")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(result)

print(f'완료: 학생 {len(data.get("students",[]))}명')
