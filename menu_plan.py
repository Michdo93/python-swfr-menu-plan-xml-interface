import requests

def get_menu_plan(api_key, location_id=None, days=None, en=False):
    type=98

    base_url = "https://www.swfr.de/apispeiseplan?&type={}&tx_speiseplan_pi1[apiKey]={}".format(type, api_key)
    if en:
        base_url = "https://www.swfr.de/en/apispeiseplan?&type={}&tx_speiseplan_pi1[apiKey]={}".format(type, api_key)

    if location_id is not None:
        base_url += "&tx_speiseplan_pi1[ort]={}".format(location_id)

    if days is not None:
        base_url += "&tx_speiseplan_pi1[tage]={}".format(days)

    response = requests.get(base_url)

    if response.status_code == 200:
        return response.text
    else:
        return f"Error {response.status_code}: {response.text}"

if __name__ == "__main__":
    api_key = ""
    location_id = 641 # Mensa Furtwangen
    days = 5

    # Without filter
    response = get_menu_plan(api_key)
    print (response)

    # With location id
    response = get_menu_plan(api_key, location_id)
    print (response)

    # With days
    response = get_menu_plan(api_key, location_id, days)
    print (response)
