from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/reel_0079_recovery_what_studies_measure_captions_hi.srt'
DURATION = 68.20
CUES = [
    ('“रिकवरी” सुनते ही क्या आप एक ही स्कोर की कल्पना करते हैं? शोध में ऐसा नहीं होता।', 4.75),
    ('शोधकर्ता तय करते हैं कि घटना से पहले और बाद में, किस समय पर तुलना होगी।', 4.75),
    ('प्रयोगशाला में baseline, stress-task और recovery window हो सकती है।', 3.60),
    ('माप में heart rate, HRV, skin conductance या cortisol शामिल हो सकते हैं।', 4.70),
    ('लेकिन ये शरीर के correlates हैं, मन की सीधी reading नहीं।', 3.75),
    ('self-report affect या stress के बारे में व्यक्ति का बताया अनुभव है।', 3.80),
    ('यह physiology या behavior का पूरा विकल्प नहीं।', 2.55),
    ('रोज़मर्रा की recovery देखने के लिए phone prompts या daily diaries mood, behavior और context बार-बार पूछ सकते हैं।', 7.80),
    ('कुछ studies recovery को समय के साथ affect में बदलाव के रूप में गिनती हैं।', 4.80),
    ('static resilience questionnaire अकेले dynamic process नहीं पकड़ता।', 3.55),
    ('एक peer-reviewed comparison में laboratory और daily-life measures अक्सर मज़बूती से match नहीं हुए।', 6.10),
    ('task, setting, sampling और outcome अलग हो सकते हैं।', 2.85),
    ('इसलिए “जल्दी recover” तभी स्पष्ट है, जब माप और समय बताए जाएँ।', 4.70),
    ('एक biomarker या observation से किसी व्यक्ति का mental health या resilience तय नहीं किया जा सकता।', 5.50),
    ('यह AI-सहायित शैक्षिक reel है। दावे चार peer-reviewed स्रोतों पर आधारित हैं; व्यक्तिगत सलाह नहीं।', 5.00),
]


def stamp(seconds: float) -> str:
    total_ms = round(seconds * 1000)
    hours, rem = divmod(total_ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    secs, millis = divmod(rem, 1000)
    return f'{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}'


cursor = 0.0
lines: list[str] = []
for index, (text, length) in enumerate(CUES, 1):
    start = cursor
    end = cursor + length
    lines.extend([str(index), f'{stamp(start)} --> {stamp(end)}', text, ''])
    cursor = end
assert abs(cursor - DURATION) < 0.001, cursor
OUT.write_text('\n'.join(lines), encoding='utf-8')
print(f'wrote {OUT} cues={len(CUES)} duration={cursor:.3f}')
