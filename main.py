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

def average_online_time_for_user(user_id):

    users_data = fetch_user_data(0)

    for user in users_data:
        if user.get('userId') == user_id:
            last_seen = user.get('lastSeenDate', None)
            if last_seen:
                last_seen = last_seen.split('.')[0]
                last_seen_date = datetime.strptime(last_seen, "%Y-%m-%dT%H:%M:%S")

                current_time = datetime.now()
                total_time_seconds = (current_time - last_seen_date).total_seconds()

                weekly_average = total_time_seconds / (7 * 24 * 3600)
                daily_average = total_time_seconds / (24 * 3600)

                return {
                    "weeklyAverage": weekly_average,
                    "dailyAverage": daily_average
                }
    return{
        "weeklyAverage": 0,
        "dailyAverage": 0
    }




def main():

    user_id = input("Enter your user id: ")

    total = total_online_time_for_user(user_id)
    print(total)
    average = average_online_time_for_user(user_id)
    print(average)



main()
