from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()

PATCH_FILE = os.getenv("PATCH_FILE", "latest_patch_notes.txt")

def load_patch_text():
    if not os.path.exists(PATCH_FILE):
        return ""
    with open(PATCH_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def llm(messages, model="gpt-5-mini"):
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
    )
    return resp.choices[0].message.content

def get_legends():
    text = load_patch_text()
    if not text:
        return "No patch notes found."
    
    prompt = f"""
    Extract ONLY legend changes from these Apex Legends patch notes. 
    Format each change as: Legend Name (Buff|Nerf|Adjust) - brief description (one sentence, max 10 words). 
    For each legend only include it once. The brief description should summarize every change regarding that legend. 
    If no legend changes found, say 'No legend changes in this patch.
    
    Patch Notes: {text}
    """
    return llm([{"role": "user", "content": prompt}])

def get_weapons():
    text = load_patch_text()
    if not text:
        return "No patch notes found."
    
    prompt = f"""
    Extract ONLY weapon changes from these Apex Legends patch notes. 
    Format each change as: Weapon Name (Buff|Nerf|Adjust) - brief description (one sentence, max 10 words). 
    For each weapon only include it once. The brief description should summarize every change regarding that weapon. 
    If no weapon changes found, say 'No weapon changes in this patch.
    
    Patch Notes: {text}
    """
    return llm([{"role": "user", "content": prompt}])

def get_other():
    text = load_patch_text()
    if not text:
        return "No patch notes found."
    
    prompt = f"""
    Extract ONLY map rotation changes and gamemode updates from these Apex Legends patch notes. 
    Focus on ranked maps, new modes, or map-related changes. 
    If none found, say 'No map or gamemode changes in this patch.
    
    Patch Notes: {text}
    """
    return llm([{"role": "user", "content": prompt}])

if __name__ == "__main__":
    print("Legends:\n", get_legends())
    print("\nWeapons:\n", get_weapons())
    #print("\nOther:\n", get_other())
