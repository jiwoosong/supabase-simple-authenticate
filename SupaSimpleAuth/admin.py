import requests
import base64

def list_licenses(URL, DB_Name, HEADERS):
    """모든 라이선스 조회"""
    url = f"{URL}/rest/v1/{DB_Name}?select=*"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_license(URL, DB_Name, HEADERS, computer_id, new_license):
    """특정 사용자 라이선스 수정 (존재 여부 확인 + 타입 검증)"""

    # ✅ 먼저 해당 `computer_id`가 존재하는지 확인
    check_url = f"{URL}/rest/v1/{DB_Name}?computer_id=eq.{computer_id}&select=computer_id"
    check_response = requests.get(check_url, headers=HEADERS)

    if check_response.status_code != 200 or not check_response.json():
        return {
            "status": "error",
            "message": f"❌ 지정된 컴퓨터 ID({computer_id})가 존재하지 않습니다."
        }

    # ✅ `license` 값이 `float` 타입인지 확인
    if not isinstance(new_license, (int, float)) or not (0.0 <= new_license <= 1.0):
        return {
            "status": "error",
            "message": "❌ 라이선스 값은 0.0 ~ 1.0 사이의 숫자여야 합니다."
        }

    # 🔹 라이선스 업데이트 실행
    update_payload = {"license": new_license}
    url = f"{URL}/rest/v1/{DB_Name}?computer_id=eq.{computer_id}"
    response = requests.patch(url, json=update_payload, headers=HEADERS)

    if response.status_code in [200, 204]:
        return {
            "status": "success",
            "message": f"✅ 사용자 {computer_id}의 라이선스가 {new_license}로 변경되었습니다."
        }
    else:
        return {
            "status": "error",
            "message": f"❌ 라이선스 업데이트 실패: {response.text}"
        }



def reset_licenses(URL, DB_Name, ADMIN_HEADERS):
    """모든 라이선스 초기화 (Supabase에서 전체 삭제)"""
    url = f"{URL}/rest/v1/{DB_Name}?computer_id=neq.NULL"  # ✅ 모든 데이터 삭제를 위한 조건

    response = requests.delete(url, headers=ADMIN_HEADERS)

    if response.status_code in [200, 204]:
        return "✅ 모든 라이선스가 초기화되었습니다."
    else:
        return f"❌ 초기화 실패: {response.text}"


def admin_request(URL, DB_Name, API_KEY, JWT):
    HEADERS = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {JWT}",
        "Content-Type": "application/json"
    }
    while True:
        print("\n=== 관리자 모드 ===")
        print("1. 모든 라이선스 조회")
        print("2. 특정 사용자 라이선스 수정")
        print("3. 모든 라이선스 초기화")
        print("4. 종료")

        choice = input("원하는 작업을 선택하세요 (1~4): ")

        if choice == "1":
            licenses = list_licenses(URL, DB_Name, HEADERS)
            print("=== 라이선스 목록 ===")
            for item in licenses:
                print(item)
        elif choice == "2":
            computer_id = input("수정할 컴퓨터 ID를 입력하세요: ")
            new_license = float(input("새 라이선스 값을 입력하세요 (0 ~ 1): "))
            result = update_license(URL, DB_Name, HEADERS, computer_id, new_license)
            print(result)
        elif choice == "3":
            confirm = input("⚠️ 정말로 모든 라이선스를 초기화하시겠습니까? (yes/no): ")
            if confirm.lower() == "yes":
                result = reset_licenses(URL, DB_Name, HEADERS)
                print(result)
            else:
                print("초기화가 취소되었습니다.")
        elif choice == "4":
            print("프로그램을 종료합니다.")
            break
        else:
            print("❌ 잘못된 선택입니다. 다시 시도하세요.")

#
# if __name__ == "__main__":
#     admin_request(URL, DB_Name, API_KEY, JWT)
