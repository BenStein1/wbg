from config import (
    OPENAI_API_KEY
)


    @staticmethod
    def generate_bio(combined_story):

            prompt = f"""
        I have description of an acquaintance to my D and D character I will provide. Given the description I will provide you after this example format, give them a name and a short bio in the form of:

        Name:
            Eldrin the Sly

        Race:
            Half-Elf (Same as Randalf the Wizened)

        Strength of Relationship:
            Casual friend turned enemy.

        Length of Acquaintance:
            Known briefly, for a few months.

        Relative Influence:
            Average influence; not particularly well-known or powerful.

        Personality:
            Gregarious among allies, but unscrupulous and cruel to foes.

        Profession:
            Thief/Bandit operating within a notorious guild.

        Short Bio:

        Eldrin the Sly was once an ally of Randalf the Wizened. In fact, they were introduced by a common acquaintance within the arcane circles both dabbled in. Eldrin showed promise in thievery but was caught up in dark magic, manipulated by a warlock aiming to use him as a pawn in a grander scheme. Randalf saved him, breaking the warlock's enchantment over him, and Eldrin was grateful but remained cautious.

        However, Eldrin couldn't completely escape his darker tendencies. He's the sort to flash a charming smile while planning something nefarious. Although gregarious among his own circles, he is ruthless and cruel to those he considers enemies or obstacles. Randalf had hoped that his act of saving Eldrin would serve as a catalyst for change, but Eldrin instead saw it as an opportunity for power, secretly resenting Randalf for both rescuing him and for showing him what he considered to be "weakness" — kindness and compassion.

        The final straw was when Eldrin stole an arcane artifact that Randalf had been safeguarding, leading to dire consequences. Eldrin thought he could wield its power for his own purposes but instead, he inadvertently unleashed a dangerous entity upon the land. Realizing that Eldrin's moral compass was beyond repair, Randalf severed ties with him, marking the beginning of a tense and dangerous rivalry.

        Now, Eldrin remains a constant shadow in Randalf's life, always plotting, always watching, and waiting for the perfect moment to exact what he perceives to be just revenge.
    """.strip()



        apiKey = OPENAI_API_KEY  # Replace with your actual ChatGPT API key
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {apiKey}",
            "Content-Type": "application/json",
        }
        params = {
            "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": combined_story}]
            "model": "gpt-3.5-turbo"
        }
        response = requests.post(url, headers=headers, json=params)
        if response.ok:
            chatgpt_bio = response.json().get('choices')[0].get('message').get('content')
            return chatgpt_bio
        else:
            print(f"API Error: {response.status_code} - {response.text}")



