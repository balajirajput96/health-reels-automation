from pathlib import Path
import subprocess
from gtts import gTTS

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / 'production' / 'audio'
MP3 = OUT_DIR / 'reel0004_voice_full.mp3'
WAV = OUT_DIR / 'reel0004_voice_full.wav'

TEXT = (
    'क्या cognitive bias का मतलब है कि किसी व्यक्ति का दिमाग हमेशा गलत सोचता है? '
    'नहीं—study आम तौर पर एक खास task में response pattern मापती है। '
    'Cognitive bias यानी judgment में ऐसा systematic pattern जो किसी norm या accuracy benchmark से अलग दिख सकता है। '
    'Researchers इसे label से नहीं, operational definition से पकड़ते हैं। '
    'कुछ tasks में answer को base rate या सही calculation से compare करते हैं। '
    'कुछ में एक ही सवाल के दो versions देते हैं—जैसे framing बदलकर—और responses का फर्क देखते हैं। '
    'लेकिन एक task पूरी personality नहीं। Reviews बताते हैं कि अलग tasks को जोड़कर बना score कभी कम reliable हो सकता है; '
    'wording, response mode और context भी परिणाम बदल सकते हैं। '
    'एक study में dot-probe, AAT और IAT की reliability task और समय के साथ अलग रही। '
    'इसलिए सही सवाल है: इस sample में, इस design ने क्या मापा? '
    'यह general education है, medical advice नहीं। किसी personal concern के लिए qualified professional से बात करें। '
    'Narration में AI का उपयोग हुआ है; visuals procedural graphics हैं।'
)

OUT_DIR.mkdir(parents=True, exist_ok=True)
gTTS(text=TEXT, lang='hi', slow=False).save(str(MP3))
subprocess.run([
    'ffmpeg', '-y', '-i', str(MP3), '-filter:a', 'atempo=1.20', '-ac', '1', '-ar', '24000', '-c:a', 'pcm_s16le', str(WAV)
], check=True)
print(WAV)
