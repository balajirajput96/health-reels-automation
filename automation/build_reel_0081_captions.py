from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'reel_0081_stress_and_attention_what_studies_measure_captions_hi.srt'

CUES = [
    'क्या stress attention को हमेशा कमजोर करता है? जवाब सीधा नहीं।',
    'Study ने stressor मापा या subjective appraisal?',
    'Exam, social evaluation और cold pressor अलग exposures हैं।',
    '“मैं stressed हूँ” self-report है, attention meter नहीं।',
    'Attention Network Test alerting, orienting और executive control अलग करता है।',
    'Response time, accuracy और errors task performance बताते हैं।',
    'Congruent और incongruent targets conflict processing दिखा सकते हैं।',
    'EEG के N1, N2 और P3 neural correlates हैं।',
    'Cortisol और alpha-amylase physiological response के संकेतक हैं।',
    'Biomarker और reported feeling एक layer नहीं।',
    'Sänger study ने acute stress और visual distractors compare किए।',
    'Liu study ने chronic-stress group में task और EEG compare किए।',
    'ये group और task findings हैं, individual forecast नहीं।',
    'Stressor, task, measure, timing और sample साथ पढ़ें; association causation नहीं।',
    'यह AI-सहायित शैक्षिक reel है; diagnosis, treatment या व्यक्तिगत सलाह नहीं।',
]
DURATIONS_MS = [5100, 3000, 3400, 3400, 5500, 3800, 3900, 3600, 3800, 3000, 5300, 4100, 3700, 6000, 6840]


def stamp(ms: int) -> str:
    hours, rem = divmod(ms, 3_600_000)
    minutes, rem = divmod(rem, 60_000)
    seconds, millis = divmod(rem, 1_000)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}'


def main() -> None:
    assert len(CUES) == 15
    assert len(DURATIONS_MS) == len(CUES)
    assert sum(DURATIONS_MS) == 64_440
    cursor = 0
    blocks: list[str] = []
    for index, (cue, duration) in enumerate(zip(CUES, DURATIONS_MS), 1):
        start = cursor
        cursor += duration
        blocks.append(f'{index}\n{stamp(start)} --> {stamp(cursor)}\n{cue}\n')
    assert cursor == 64_440
    OUT.write_text('\n'.join(blocks), encoding='utf-8')
    print(f'{OUT} cues={len(CUES)} duration_ms={cursor}')


if __name__ == '__main__':
    main()
