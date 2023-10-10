import os
from pathlib import Path

#from dotenv import load_dotenv
#load_dotenv()

# Paths
#ROOT = Path(__file__).parent
#DATA = ROOT / "data"


# OpenAI
#AI_MODEL = "gpt-3.5-turbo"
AI_MODEL = "gpt-4"
if AI_MODEL == "gpt-3.5-turbo":
    input_cost_perk = 0.0015
    output_cost_perk = 0.002
elif AI_MODEL == "gpt-4":
    input_cost_perk = 0.03
    output_cost_perk = 0.06
else:
    print("Warning: Unknown AI_MODEL. Using default costs.")
    input_cost_perk = 0.0015  # Default cost per token for input
    output_cost_perk = 0.002  # Default cost per token for output

AI_INPUT_COST = input_cost_perk
AI_OUTPUT_COST = output_cost_perk


# Costs As of 10/10/23 - https://openai.com/pricing
#        Model   Context         Input                   Output
#gpt-3.5-turbo   4K context      $0.0015 / 1K tokens     $0.002 / 1K tokens
#gpt-4           8K context      $0.03   / 1K tokens     $0.06  / 1K tokens
