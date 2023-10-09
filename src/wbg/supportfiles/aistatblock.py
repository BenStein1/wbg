import requests

#from .config import (
#    OPENAI_API_KEY
#)



def generate_statblock(enemy_bio, OPENAI_API_KEY):
#{party_level}
    prompt = f"""
    For an adventuring party of 4 at level 5, create a D and D statblock for the following character as a foe, with the all the appropriate stats for a D and D 5e foe. With appropriate weapons, attacks, tactics, and if appropriate, spells, for such a character. Provide the relevant XP for defeating such a foe, and an appropriate loot table to roll on as well.
    """.strip()



    apiKey = OPENAI_API_KEY  # Replace with your actual ChatGPT API key
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {apiKey}",
        "Content-Type": "application/json",
    }
    params = {
        "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": enemy_bio}],
        "model": "gpt-3.5-turbo"
    }
    response = requests.post(url, headers=headers, json=params)
    if response.ok:
        enemy_statblock = response.json().get('choices')[0].get('message').get('content')
        return enemy_statblock
    else:
        print(f"API Error: {response.status_code} - {response.text}")

