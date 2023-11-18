import requests, os


def get_user_data_from_vk(user_id: int, access_token: str):
   
    api_url = "https://api.vk.com/method/users.get"
    
    params = {
        'user_ids': user_id,
        'fields': 'id,first_name,last_name,city,country,groups',
        'access_token': access_token,
        'v': '5.131'
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        user_data = response.json()['response'][0]

        return {
            'id': user_data['id'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'city': user_data.get('city', {}).get('title'),
            'country': user_data.get('country', {}).get('title'),
            'followers': get_user_followers(user_id, access_token),
            # 'photo_url': user_data.get('photo_max_orig'),
            'groups': get_user_subscriptions(user_id, access_token)
        }

    except requests.RequestException as e:
        print(f"Error during VK API call: {e}")
        return None
    

def get_user_followers(user_id: int, access_token: str):
    api_url = "https://api.vk.com/method/users.getFollowers"

    params = {
        'user_id': str(user_id),
        'extended': 1,
        'offset': '1',
        'fields': 'first_name',
        'access_token': access_token,
        'v': '5.131'
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        followers = response.json().get('response', {}).get('items', [])

        return followers

    except requests.RequestException as e:
        print(f"Error during VK groups API call: {e}")
        return []

def get_user_subscriptions(user_id: int, access_token: str):
    api_url = "https://api.vk.com/method/users.getSubscriptions"

    params = {
        'user_id': user_id,
        'extended': 1,
        'access_token': access_token,
        'v': '5.131'
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        response_json = response.json()
        if 'error' in response_json:
            error_msg = response_json['error']['error_msg']
            print(f"Error during VK subscriptions API call: {error_msg}")
            return []

        subscriptions = response_json.get('response', {}).get('items', [])

        # Separate user and group information 
        users = [item for item in subscriptions if item.get('type') == 'profile']
        groups = [item for item in subscriptions if item.get('type') == 'page']

        user_names = [user['first_name'] + ' ' + user['last_name'] for user in users]
        group_names = [group['name'] for group in groups]

        return  group_names
        

    except requests.RequestException as e:
        print(f"Error during VK subscriptions API call: {e}")
        return []
