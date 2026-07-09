import json
from datetime import datetime
import hashlib

with open('data.json', 'r', encoding='utf-8') as f:
    raw = f.read()
    data = json.loads(raw)

with open('viewer.html', 'r', encoding='utf-8') as f:
    viewer = f.read()

json_str   = json.dumps(data, ensure_ascii=False, separators=(',',':'))
updated_at = datetime.now().strftime('%Y년 %m월 %d일 %H:%M')
# 데이터 해시로 캐시 버전 생성
version    = hashlib.md5(raw.encode()).hexdigest()[:8]

result = viewer.replace('__DASHBOARD_DATA__', json_str) \
               .replace("'__UPDATED_AT__'", f"'{updated_at}'") \
               .replace('</head>', f'<meta name="version" content="{version}">\n</head>', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(result)

print(f'완료: 학생 {len(data.get("students",[]))}명 / 버전: {version}')
