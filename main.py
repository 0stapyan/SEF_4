from datetime import datetime
import requests


def fetch_user_data(offset):

    api_url = f'https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}'
    response = requests.get(api_url)

    if response.status_code == 200:
        user_data = response.json()
        return user_data.get('data', [])
    else:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        return None

def total_online_time_for_user(user_id):

    users_data = fetch_user_data(0)

    for user in users_data:
        if user.get('userId') == user_id:
            last_seen = user.get('lastSeenDate', None)
            if last_seen:
                last_seen = last_seen.split('.')[0]
                last_seen_date = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S")
                return {"totalTime (in seconds)": (datetime.now() - last_seen_date).total_seconds()}

    return {"totalTime": 0}



def main():

    user_id = input("Enter your user id: ")

    result = total_online_time_for_user(user_id)
    print(result)



main()
