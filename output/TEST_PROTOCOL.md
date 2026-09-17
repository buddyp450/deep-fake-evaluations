# Synthetic identity evaluation protocol

This document describes the delivered candidate media and how to record evaluation runs. It makes no claim of detection accuracy or statistical confidence.

## Test cases

The 90 cases cover three identity types, two gender labels, five accent targets and three connection profiles. IDs and file hashes are recorded in [asset_manifest.json](asset_manifest.json).

- T01-T30: genuine recordings, original face and voice retained.
- T31-T60: cloned representations of real people, with generated speech and replaced lip motion.
- T61-T90: fully synthetic people, with invented portraits, designed voices and generated mouth motion.
- Within each group: Male then Female; UK-Irish, UK-British, UK-Scottish, American and Indian accent targets. Each persona has Good, Patchy and Degraded variants, in that order.

Accent and gender values are test labels. Human listening review remains pending. Source recordings vary in framing, lighting, script and quality.

## Connection-effect presets

| Profile | Dimensions | Frame rate | Target video bitrate | Frame holds |
|---|---|---|---|---|
| Good | 1280 x 720 | 30 fps | 2500 kbps | None inserted |
| Patchy | 854 x 480 | 15 fps | 600 kbps | 10-10.5s and 20-20.5s, about 0.53s after quantization |
| Degraded | 640 x 360 | 10 fps | 200 kbps | 8-10s, 16-18s and 24-26s |

All clips are 30 seconds, H.264 video with AAC audio at 128 kbps / 48 kHz. Audio continues through frame holds. These effects approximate visible connection degradation; they do not apply live packet loss, latency or Teams network adaptation. Bitrates are encoder targets.

## Run procedure

1. Select a case and review picture and sound. Record its ID and file hash.
2. Load the MP4 as an OBS Media Source with looping disabled. Select OBS Virtual Camera in Teams.
3. Route the media audio separately into the meeting microphone using the configured audio route. Confirm the receiving endpoint gets picture and sound.
4. Add the detection bot, wait for readiness, restart the clip at zero and play all 30 seconds.
5. Record the raw detector label, score and scale if supplied, timing, evidence, tester, environment and a unique run ID. Preserve failed and repeated attempts.
6. Export results JSON. Browser storage alone is not a portable backup.

## Outcome recording

- Genuine: expected Not fake; Fake is a false positive; Inconclusive is a separate unexpected result.
- Cloned / Fully synthetic: Fake or Inconclusive are allowed outcomes, recorded separately; Not fake is a false negative.
- Missing output, failed playback or technical failure: Run error, not Inconclusive.
- Report all observed errors and counts with denominators. No minimum accuracy threshold is specified for this pack. Keep not-run cases separate.

## Scope and limitations

Real-time face swaps, mixed human/AI avatars and mid-call identity switching are not explicitly covered. Generated portraits have still backgrounds and bodies. Accent, voice likeness and continuous lip synchronization require human review. Actual OBS/Teams/bot execution remains unverified.

See [provenance](PROVENANCE_AND_GENERATION.md), [source credits](SOURCE_CREDITS.md) and [QA records](QA_REPORT.md). Preserve those records with the media.
