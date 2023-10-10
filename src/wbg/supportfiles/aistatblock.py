import requests

#from .config import (
#    OPENAI_API_KEY
#)



def generate_statblock(enemy_bio, level, OPENAI_API_KEY):

    preprompt = f"""For an adventuring party of 4 at level {level}, """.strip()

    default_prompt = f"""
    create a D and D statblock for the following character as a foe, listing the CR and level, as well as all the appropriate stats for a D and D 5e foe. With appropriate weapons, attacks, tactics, and if appropriate, spells, for such a character. Provide the relevant XP for defeating such a foe, and an appropriate loot table to roll on as well, including at least one personal plot item or weapon unique to the character.
    """.strip()

    settings_prompt = ""

    selected_prompt = settings_prompt.strip() if settings_prompt and settings_prompt.strip() else default_prompt

    complete_prompt = (preprompt + selected_prompt).strip()


    apiKey = OPENAI_API_KEY  # Replace with your actual ChatGPT API key
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {apiKey}",
        "Content-Type": "application/json",
    }
    params = {
        "messages": [{"role": "system", "content": complete_prompt}, {"role": "user", "content": enemy_bio}],
        "model": "gpt-3.5-turbo"
    }
    response = requests.post(url, headers=headers, json=params)
    if response.ok:
        enemy_statblock = response.json().get('choices')[0].get('message').get('content')
        return enemy_statblock
    else:
        print(f"API Error: {response.status_code} - {response.text}")

