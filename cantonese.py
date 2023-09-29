# %%
#!/usr/bin/env python3

"""
Basic example of edge_tts usage.
"""

import asyncio
import pathlib
import edge_tts
import edge_tts.util

TEXT = "暑假裏,真快樂。\
我們有時去旅行 \
有時去游泳, \
也有時溫習功課 \
"
VOICE = "zh-HK-HiuGaaiNeural"
OUTPUT_FILE = "test.mp3"

async def tts(file_name):
    if not ".txt" in file_name.suffix:
        return
    
    # Read text, put it through text to speech engine, save as mp3
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(str(file_name).replace('.txt', '.mp3'))

async def amain() -> None:
    # """Main function"""
    # communicate = edge_tts.Communicate(TEXT, VOICE)
    # await communicate.save(OUTPUT_FILE)
    
    # All text files, processed in parallel
    all_text_files = list(pathlib.Path('data').glob("*.txt"))
    tasks = [asyncio.create_task(tts(file_name)) for file_name in all_text_files[:]]
    await asyncio.gather(*tasks)

#%%
async def _print_voices(*, proxy: str) -> None:
    """Print all available voices."""
    voices = await edge_tts.util.list_voices(proxy=proxy)
    voices = sorted(voices, key=lambda voice: voice["ShortName"])
    for idx, voice in enumerate(voices):
        if idx != 0:
            print()

        for key in voice.keys():
            if key in (
                "SuggestedCodec",
                "FriendlyName",
                "Status",
                "VoiceTag",
                "Name",
                "Locale",
            ):
                continue
            pretty_key_name = key if key != "ShortName" else "Name"
            print(f"{pretty_key_name}: {voice[key]}")


# %%
if __name__ == "__main__":
    # loop = asyncio.get_event_loop_policy().get_event_loop()
    # try:
    #     loop.run_until_complete(amain())
    #     # loop.run_until_complete(_print_voices(proxy=""))
    # finally:
    #     loop.close()
    asyncio.run(amain())
# %%
