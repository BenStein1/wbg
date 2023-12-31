import requests


def generate_bio(combined_story, OPENAI_API_KEY, AI_MODEL):


    default_prompt = f"""
    I have a description of an acquaintance to my D and D character that I will provide. Your bio must follow and include the features given. If the acquaintance is the same race as the character, your generated bio must have the race of your character be the same race of my provided character. You may not stray from any of the user provided character features, however I want you to create fantastic stories using the features presented. as well my character's race and class/profession as well, and then embelish details as you please to fill in personal events between our two characters. Given the description that will be provided to you after this example format, give your generated acquaintance a name and a short bio in the form of:

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

    settings_prompt = ""

    selected_prompt = settings_prompt.strip() if settings_prompt and settings_prompt.strip() else default_prompt

    complete_prompt = (selected_prompt).strip()


    apiKey = OPENAI_API_KEY  # Replace with your actual ChatGPT API key
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {apiKey}",
        "Content-Type": "application/json",
    }
    params = {
        "messages": [{"role": "system", "content": complete_prompt}, {"role": "user", "content": combined_story}],
        "model": AI_MODEL
    }



    response = requests.post(url, headers=headers, json=params)
    if response.ok:
        chatgpt_bio = response.json().get('choices')[0].get('message').get('content')

        compl_tokens = response.json().get('usage').get('completion_tokens')
        pr_tokens = response.json().get('usage').get('prompt_tokens')
        returned_tokens = response.json().get('usage').get('total_tokens')

        #sent_cost = (compl_tokens/1000) * AI_INPUT_COST
        #received_cost = (pr_tokens/1000) * AI_OUTPUT_COST
        #total_aimessage_cost = sent_cost + received_cost
        #formatted_total_aimessage_cost = "${:.4f}".format(total_aimessage_cost)

        print(f"GPTTok completion_tokens: {compl_tokens}") #SENT TOKENS
        print(f"GPTTok prompt_tokens    : {pr_tokens}") #RECEIVED TOKENS
        print(f"GPTTok total tokens     : {returned_tokens}") #GRAND TOTAL TOKENS
        #print(f"Total message cost      : {formatted_total_aimessage_cost}")


        return chatgpt_bio, compl_tokens, pr_tokens
    else:
        print(f"API Error: {response.status_code} - {response.text}")



