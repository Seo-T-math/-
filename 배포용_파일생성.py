#!/usr/bin/env python3
"""
학부모 뷰어 배포용 파일 생성 스크립트
────────────────────────────────────
사용법:
  1. student_dashboard_v6.html 에서 "저장" 버튼 클릭 → JSON 파일 다운로드
  2. 이 스크립트(배포용_파일생성.py)와 학부모_뷰어.html을 같은 폴더에 놓기
  3. 터미널에서: python3 배포용_파일생성.py
     또는 더블클릭(macOS: 터미널에서 실행)
  4. 생성된 index.html 을 GitHub Pages에 업로드
"""

import json
import os
import sys
import glob
from datetime import datetime

# ── 경로 설정 ──────────────────────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
VIEWER_FILE  = os.path.join(SCRIPT_DIR, '학부모_뷰어.html')
OUTPUT_FILE  = os.path.join(SCRIPT_DIR, 'index.html')

# ── JSON 파일 자동 탐색 ────────────────────────────────────
def find_json():
    # 1순위: 같은 폴더에서 '학생관리_' 로 시작하는 가장 최신 파일
    pattern = os.path.join(SCRIPT_DIR, '학생관리_*.json')
    files = sorted(glob.glob(pattern), reverse=True)
    if files:
        return files[0]
    # 2순위: 폴더 내 모든 .json 파일 중 가장 최신
    all_json = sorted(glob.glob(os.path.join(SCRIPT_DIR, '*.json')), reverse=True)
    if all_json:
        return all_json[0]
    return None

def main():
    print("=" * 50)
    print("  학부모 뷰어 배포 파일 생성")
    print("=" * 50)

    # JSON 파일 확인
    json_path = find_json()
    if not json_path:
        print("\n❌ JSON 파일을 찾을 수 없습니다.")
        print("   대시보드에서 [저장] 버튼 → JSON 파일을 이 폴더에 넣어주세요.")
        input("\nEnter 키를 눌러 종료...")
        sys.exit(1)

    print(f"\n📂 JSON 파일: {os.path.basename(json_path)}")

    # JSON 읽기
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"\n❌ JSON 파일 읽기 실패: {e}")
        input("\nEnter 키를 눌러 종료...")
        sys.exit(1)

    students = data.get('students', [])
    print(f"👤 학생 수: {len(students)}명")
    print(f"📚 서비스 수: {sum(len(s.get('services',[])) for s in students)}건")

    # 뷰어 HTML 읽기
    if not os.path.exists(VIEWER_FILE):
        print(f"\n❌ 학부모_뷰어.html 파일이 없습니다.")
        print(f"   이 스크립트와 같은 폴더에 놓아주세요.")
        input("\nEnter 키를 눌러 종료...")
        sys.exit(1)

    with open(VIEWER_FILE, 'r', encoding='utf-8') as f:
        viewer_html = f.read()

    # 데이터 주입
    json_str   = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    updated_at = datetime.now().strftime('%Y년 %m월 %d일 %H:%M')

    output_html = viewer_html.replace(
        '__DASHBOARD_DATA__', json_str
    ).replace(
        "'__UPDATED_AT__'", f"'{updated_at}'"
    )

    # 결과 확인
    if '__DASHBOARD_DATA__' in output_html:
        print("\n❌ 데이터 주입 실패. 뷰어 파일 형식을 확인해주세요.")
        input("\nEnter 키를 눌러 종료...")
        sys.exit(1)

    # 저장
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(output_html)

    print(f"\n✅ 완료! index.html 생성됨")
    print(f"   업데이트 시각: {updated_at}")
    print(f"\n📤 GitHub 업로드 방법:")
    print("   1. github.com → 저장소 → index.html 클릭")
    print("   2. 연필(✏) 아이콘 → 내용 전체 삭제 → index.html 내용 붙여넣기")
    print("   3. 또는 파일을 드래그해서 저장소에 올리기")
    print(f"\n🔗 학부모 공유 링크:")
    print("   https://[내아이디].github.io/[저장소이름]/")
    print("\n학부모가 링크를 열면 이름 입력 후 본인 자녀 현황만 볼 수 있습니다.")

    input("\nEnter 키를 눌러 종료...")

if __name__ == '__main__':
    main()
