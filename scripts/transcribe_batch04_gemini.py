#!/usr/bin/env python3
"""Transcribe the actual Batch 04 assembled narration track with Gemini."""

from pathlib import Path
import os
from google import genai

AUDIO = Path("/home/ubuntu/reels_ops/audio/batch04_evening_screens_full_narration.wav")
OUTPUT = Path("/home/ubuntu/reels_ops/work/batch04_evening_screens/gemini_actual_narration_transcript.txt")

prompt = """Transcribe only the speech in this audio track. Preserve words as actually spoken,
including Hindi-English code switching. Provide exactly the spoken sequential segments with start
and end timestamps in MM:SS, followed by each segment's speech. Use Devanagari where Hindi is
spoken. Do not translate, summarize, interpret, correct wording, add health advice, or invent content.
Do not create a segment for silence."""

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
uploaded = client.files.upload(file=str(AUDIO))
interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input=[
        {"type": "text", "text": prompt},
        {"type": "audio", "uri": uploaded.uri, "mime_type": uploaded.mime_type},
    ],
)
OUTPUT.write_text(interaction.output_text or "", encoding="utf-8")
print(f"Saved transcription to {OUTPUT}")
