import requests
import socket
from datetime import datetime

def client_request(URL, DB_Name, API_KEY, JWT, init_license=1.0, init_extra_data=None):
    computer_id = socket.gethostname()

    HEADERS = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {JWT}",
        "Content-Type": "application/json"
    }

    try:
        url = f"{URL}/rest/v1/{DB_Name}?computer_id=eq.{computer_id}&select=*"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        data = response.json()

        now = datetime.utcnow().isoformat()

        if isinstance(data, list) and len(data) > 0:
            license_info = data[0]
            new_count = int(license_info.get("request_n", 0)) + 1

            update_payload = {
                "request_n": new_count,
                "updated_at": now
            }
            if init_extra_data is not None:
                update_payload['extra_data'] = init_extra_data
            update_url = f"{URL}/rest/v1/{DB_Name}?computer_id=eq.{computer_id}"
            update_response = requests.patch(update_url, json=update_payload, headers=HEADERS)
            update_response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

            return {
                "status": "success",
                "message": f"조회 횟수 업데이트 완료: {new_count}회",
                "data": {**license_info, "request_n": new_count, "updated_at": now}
            }

        elif isinstance(data, list) and len(data) == 0:
            create_payload = {
                "computer_id": computer_id,
                "license": init_license,  # 기본 허용 값
                "request_n": 1,  # 최초 조회 횟수
                "created_at": now,
                "updated_at": now,
                "extra_data": init_extra_data if init_extra_data else {}
            }

            create_response = requests.post(f"{URL}/rest/v1/{DB_Name}", json=create_payload, headers=HEADERS)
            create_response.raise_for_status()  # HTTP 오류 발생 시 예외 발생

            return {
                "status": "success",
                "message": f"신규 라이선스 등록 완료 (computer_id={computer_id})",
                "data": create_payload
            }

        else:
            return {
                "status": "error",
                "message": f"예상치 못한 응답 형식: {data}",
                "data": None
            }

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"네트워크 오류 또는 HTTP 요청 실패: {e}",
            "data": None
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"예기치 않은 오류 발생: {e}",
            "data": None
        }

if __name__ == "__main__":
    res = client_request(URL, DB_Name, API_KEY, JWT, init_license=1.0, init_extra_data=None)
    print(res)