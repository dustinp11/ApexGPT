# Apex Legends Meta Bot

Discord bot that analyzes Apex Legends patch notes and provides meta insights.

## Commands

- `!legends` - Legend changes
- `!weapons` - Weapon changes  
- `!other` - Map and gamemode changes
- `!ask <question>` - Ask questions about patch notes (answers with RAG)

## Setup

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

2. Create `.env` file
   ```env
   DISCORD_TOKEN=your_discord_bot_token
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Fetch and embed patch notes
   ```bash
   python3 fetch_patch_notes.py
   python3 embed_patch_notes.py
   ```

4. Start bot
   ```bash
   python3 discord_bot.py
   ```

## Files

- `fetch_patch_notes.py` - Fetches latest patch notes
- `embed_patch_notes.py` - Chunks and embeds into ChromaDB
- `gpt_bot.py` - AI analysis functions
- `discord_bot.py` - Discord bot commands

## Update Process

To update with new patch notes:
```bash
python3 fetch_patch_notes.py
python3 embed_patch_notes.py
```