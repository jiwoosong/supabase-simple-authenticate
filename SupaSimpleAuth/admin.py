import requests
import base64

def list_licenses(URL, DB_Name, HEADERS):
    """Retrieve all licenses"""
    url = f"{URL}/rest/v1/{DB_Name}?select=*"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def update_license(URL, DB_Name, HEADERS, computer_id, new_license):
    """Modify a specific user's license (Check existence + Type validation)"""

    # ✅ First, check if the `computer_id` exists
    check_url = f"{URL}/rest/v1/{DB_Name}?computer_id=eq.{computer_id}&select=computer_id"
    check_response = requests.get(check_url, headers=HEADERS)

    if check_response.status_code != 200 or not check_response.json():
        return {
            "status": "error",
            "message": f"❌ The specified computer ID ({computer_id}) does not exist."
        }

    # ✅ Ensure that `license` value is of type `float`
    if not isinstance(new_license, (int, float)) or not (0.0 <= new_license <= 1.0):
        return {
            "status": "error",
            "message": "❌ License value must be a number between 0.0 and 1.0."
        }

    # 🔹 Execute license update
    update_payload = {"license": new_license}
    url = f"{URL}/rest/v1/{DB_Name}?computer_id=eq.{computer_id}"
    response = requests.patch(url, json=update_payload, headers=HEADERS)

    if response.status_code in [200, 204]:
        return {
            "status": "success",
            "message": f"✅ License for user {computer_id} has been updated to {new_license}."
        }
    else:
        return {
            "status": "error",
            "message": f"❌ License update failed: {response.text}"
        }

def reset_licenses(URL, DB_Name, ADMIN_HEADERS):
    """Reset all licenses (Delete all records from Supabase)"""
    url = f"{URL}/rest/v1/{DB_Name}?computer_id=neq.NULL"  # ✅ Condition for deleting all data

    response = requests.delete(url, headers=ADMIN_HEADERS)

    if response.status_code in [200, 204]:
        return "✅ All licenses have been reset."
    else:
        return f"❌ Reset failed: {response.text}"

def admin_request(URL, DB_Name, API_KEY, JWT):
    HEADERS = {
        "apikey": API_KEY,
        "Authorization": f"Bearer {JWT}",
        "Content-Type": "application/json"
    }
    while True:
        print("\n=== Admin Mode ===")
        print("1. View all licenses")
        print("2. Modify a specific user's license")
        print("3. Reset all licenses")
        print("4. Exit")

        choice = input("Select an action (1~4): ")

        if choice == "1":
            licenses = list_licenses(URL, DB_Name, HEADERS)
            print("=== License List ===")
            for item in licenses:
                print(item)
        elif choice == "2":
            computer_id = input("Enter the computer ID to modify: ")
            new_license = float(input("Enter the new license value (0 ~ 1): "))
            result = update_license(URL, DB_Name, HEADERS, computer_id, new_license)
            print(result)
        elif choice == "3":
            confirm = input("⚠️ Are you sure you want to reset all licenses? (yes/no): ")
            if confirm.lower() == "yes":
                result = reset_licenses(URL, DB_Name, HEADERS)
                print(result)
            else:
                print("Reset has been canceled.")
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("❌ Invalid selection. Please try again.")

#
# if __name__ == "__main__":
#     admin_request(URL, DB_Name, API_KEY, JWT)
