from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'reel_0080_social_buffering_what_studies_measure_captions_hi.srt'

CUES = [
    'क्या साथ होने से तनाव हमेशा घटता है? शोध में जवाब इतना सीधा नहीं।',
    'सामाजिक बफ़रिंग research label है: किसी तय challenge के दौरान social condition के साथ stress response में बदलाव।',
    'पहले stressor और social condition तय होते हैं।',
    'presence, assistance, perceived support और received support अलग constructs हैं।',
    'perceived support संभावित access है; received support किसी समय मिला support है।',
    'प्रयोगशाला में Trier Social Stress Test जैसे social-evaluation tasks हो सकते हैं।',
    'तब saliva cortisol, cardiovascular reactivity और stress या calmness की self-report मापी जा सकती है।',
    'एक human experiment ने best-friend support, oxytocin condition और no-support की तुलना में cortisol, calmness और anxiety देखी।',
    'तैयारी के दौरान support और task के दौरान support अलग exposure हैं।',
    'रोज़मर्रा में experience sampling smartphone prompts से context, mood और stress बार-बार पूछ सकता है।',
    'इससे timing बेहतर दिखती है, causation साबित नहीं होती।',
    'इसलिए sample, task, support type, measure और time window देखें।',
    'एक biomarker से mental health तय नहीं होती।',
    'support का असर हर व्यक्ति और हर context में एक जैसा मानना सुरक्षित नहीं।',
    'यह AI-सहायित शैक्षिक reel है; व्यक्तिगत सलाह नहीं।',
]
DURATIONS_MS = [4300, 6100, 2500, 4300, 4300, 4500, 5300, 6500, 4400, 5200, 3900, 4500, 3300, 4400, 7660]


def stamp(ms: int) -> str:
    hours, rem = divmod(ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    seconds, millis = divmod(rem, 1_000)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}'


def main() -> None:
    assert len(CUES) == 15
    assert len(DURATIONS_MS) == len(CUES)
    assert sum(DURATIONS_MS) == 71_160
    cursor = 0
    blocks: list[str] = []
    for index, (cue, duration) in enumerate(zip(CUES, DURATIONS_MS), 1):
        start = cursor
        cursor += duration
        blocks.append(f'{index}\n{stamp(start)} --> {stamp(cursor)}\n{cue}\n')
    assert cursor == 71_160
    OUT.write_text('\n'.join(blocks), encoding='utf-8')
    print(f'{OUT} cues={len(CUES)} duration_ms={cursor}')


if __name__ == '__main__':
    main()
