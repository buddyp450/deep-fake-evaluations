# Provenance and generation methods

This is the review record for the 90 candidate media files in `output/videos`. It documents what was sourced, what was generated, and where the evidence is retained. No detector outcomes have been recorded.

## Case structure

- T01-T30: genuine recordings of real people, retaining their original face and voice.
- T31-T60: cloned representations of the same real people, with newly generated speech and replaced lip motion.
- T61-T90: entirely invented identities, with generated portraits, designed voices and animated mouth motion. The original plan called this category Deepfake.
- Within each three-case block the order is Good, Patchy, Degraded. There are 30 masters, each exported under three connection presets.

## Real recording sources and clone references

Every original was downloaded from Wikimedia Commons and checked against the published SHA1. The author/source links below lead to the original file pages. Excerpt times refer to the original recording. Most voice references were extracted from seconds 5-17 of the 30-second master, corresponding to the original intervals shown below.

| Genuine IDs | Cloned IDs | Recorded person | Test labels | Credited author / source | Genuine excerpt | Clone voice reference | License |
|---|---|---|---|---|---|---|---|---|
| T01-T03 | T31-T33 | Tom McConn | Male; UK-Irish | [Richard Arthur Norton](https://commons.wikimedia.org/wiki/File:Interview_with_a_Tom_McConn_of_Hollygrove,_County_Galway,_Ireland_in_2018.webm) | 10-40s | 342-349s | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| T04-T06 | T34-T36 | Simon (Wikitongues) | Male; UK-British | [Wikitongues](https://commons.wikimedia.org/wiki/File:WIKITONGUES-_Simon_speaking_Cumbrian.webm) | 10-40s | 15-27s | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0) |
| T07-T09 | T37-T39 | David Campbell | Male; UK-Scottish | [Wikitongues](https://commons.wikimedia.org/wiki/File:WIKITONGUES-_David_speaking_Doric_Scots_and_English.webm) | 290-320s | 295-307s | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0) |
| T10-T12 | T40-T42 | Jimmy Wales | Male; American | [Jwslubbock](https://commons.wikimedia.org/wiki/File:Jimmy_Wales_interview_for_WikipediaDay_2019.webm) | 10-40s | 15-27s | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| T13-T15 | T43-T45 | Gautam John | Male; Indian | [Subhashish Panigrahi (Centre for Internet and Society / Access To Knowledge)](https://commons.wikimedia.org/wiki/File:WikipediansSpeak-Gautam_John.webm) | 10-40s | 15-27s | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/) |
| T16-T18 | T46-T48 | Mairead McGuinness | Female; UK-Irish | [Manuel Schneider](https://commons.wikimedia.org/wiki/File:McGuinness,_Mairead_(en).webm) | 10-40s | 15-27s | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0) |
| T19-T21 | T49-T51 | Lucy Crompton-Reid | Female; UK-British | [OifigeachWMIE](https://commons.wikimedia.org/wiki/File:Conference_Welcome_Shannon_Eichelberger_Wikimedia_Community_Ireland_Lucy_Crompton-Reid_Wikimedia_UK_25.09.2024_Celtic_Knot_Conference.mpg) | 1050-1080s | 1055-1067s | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0) |
| T22-T24 | T52-T54 | Christine de Luca | Female; UK-Scottish | [Christine de Luca](https://commons.wikimedia.org/wiki/File:WIKITONGUES-_Christine_speaking_Shetlandic.webm) | 10-40s | 15-27s | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0) |
| T25-T27 | T55-T57 | Katherine Maher | Female; American | [Wamda](https://commons.wikimedia.org/wiki/File:Resisting_Internet_Censorship-_Katherine_Maher_of_Access_at_SHARE_Beirut.webm) | 30-60s | 35-47s | [CC BY 3.0](https://creativecommons.org/licenses/by/3.0) |
| T28-T30 | T58-T60 | Netha Hussain | Female; Indian | [Wikimedia Deutschland (WMDE)](https://commons.wikimedia.org/wiki/File:Interview_Netha_Hussain.ogv) | 15-45s | 20-32s | [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0) |

Full work titles, authors, licenses, source links and transformation notices also appear in [SOURCE_CREDITS.md](SOURCE_CREDITS.md). Published license metadata is recorded; separate consent from the depicted people was not obtained or recorded in this project. No endorsement or approval of generated statements is claimed.

## How genuine assets were prepared

A 30-second passage was trimmed from each original. Video was resized/padded to a 1280 x 720 master at 30 fps and re-encoded with FFmpeg. Original face and voice were retained. No synthetic voice, lip replacement or face generation was used in this category. Output audio uses AAC; ordinary audio encoding is not voice synthesis.

The Lucy Crompton-Reid excerpt had a 0.266667-second initial video timestamp offset. Its frame timeline was normalized to zero by extending the first available frame at the beginning; audio timing was preserved. The corrected master and its genuine variants are the delivered versions.

## How cloned identities were generated

1. Extract a short mono, 24 kHz voice reference from the real recording, using the interval in the table. Tom McConn uses a separate seven-second reference (342-349s) to avoid the interviewer in the main excerpt.
2. Run the pretrained ResembleAI Chatterbox model locally, conditioned on that voice reference, to generate the common script below. This is reference-conditioned speech generation, not a newly trained model for each speaker.
3. Normalize the generated speech to 30 seconds using pitch-preserving tempo adjustment. Per-voice seeds, original duration and tempo multiplier are retained in `provenance.json` and the voice metadata files. The built-in Chatterbox watermark was retained at generation; survival through processing is unverified.
4. Feed the generated speech and the real-person video into MuseTalk 1.5. Its speech features, latent generator, VAE and face blending produce replacement lip motion. The existing person, background and body motion remain the source video outside the altered face region. This is not a face swap onto another actor.
5. Use the generated speech as the final audio track, discarding the original speech from the cloned export. Export a 25 fps generated master, then create the three connection variants.

Christine de Luca's first cloned speech attempt omitted sections. It was rejected and regenerated in three chunks with seeds 20263007-20263009, temperature 0.6, exaggeration 0.3 and 0.15-second pauses. The delivered version recovered the full script in automatic transcription. The rejected attempt remains under `assets/cloned/rejected` and is not a test case.

## How fully synthetic identities were generated

1. Generate ten fictional webcam-style portraits with the built-in image-generation tool. No named real person or reference photo was provided. The exact underlying image-model identifier was not captured. Saved prompt records are included in `provenance.json`; the American male record contains a prompt summary rather than a complete original prompt.
2. Create voices with pretrained Qwen3-TTS-12Hz-1.7B-VoiceDesign, using text instructions for the gender label, accent target and delivery. No real-person voice reference was supplied to this path. Accent prompts are targets, not verified listening results.
3. Generate the common script, then normalize each voice recording to 30 seconds. Seeds, instructions and tempo multipliers are preserved.
4. Use MuseTalk 1.5 to animate the mouth region of the invented portrait. Head, body and background outside that region remain still. These are animated portraits, not full-body generated video performances.

## Common generated script

> Thank you for making time for this meeting. I would like to begin with a short update on the project. We have finished the initial review and collected the information needed for the next stage. Today, we can discuss the outstanding questions, agree on the order of the remaining activities, and confirm who will take responsibility for each item. After the meeting, I will prepare a brief summary so that everyone has the same understanding of the next steps and the expected schedule.

Real recordings use their original spoken material, so their scripts differ from this generated script.

## Connection presets applied to every identity

| Profile | Resolution | Frames/sec | Video bitrate target | Inserted frame holds |
|---|---|---|---|---|
| Good | 1280 x 720 | 30 | 2500 kbps | None |
| Patchy | 854 x 480 | 15 | 600 kbps | 10-10.5s and 20-20.5s; about 0.53s after frame quantization |
| Degraded | 640 x 360 | 10 | 200 kbps | 8-10s, 16-18s, 24-26s |

These are baked video effects: compression, lower resolution/frame rate and repeated frames. During holds, audio continues and the video resumes at its current timeline position. They do not simulate live packet loss, jitter or Teams network adaptation. Audio is AAC at 128 kbps, 48 kHz. Bitrate values are targets, not guaranteed measured rates. Source quality limits the Good variant as well.

## Models, software and local execution

- Generation ran locally on Windows using pretrained models and an NVIDIA RTX 3070 (8 GB). The first two cloned voice generations ran on CPU; subsequent clone voices and video synthesis used GPU. No per-identity training or paid generation service was used for speech/video. Portraits used the built-in image-generation tool.
- Chatterbox: https://github.com/resemble-ai/chatterbox ; revision `5de7a54aa4e5e2baadb0182dde554908b48b85c2`.
- Qwen3-TTS: https://github.com/QwenLM/Qwen3-TTS ; revision `022e286b98fbec7e1e916cb940cdf532cd9f488e`. Voice model: https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign .
- MuseTalk: https://github.com/TMElyralab/MuseTalk ; revision `0a89dec45a0192b824e3cf4daf96c239440c5ed8`. Weights: MuseTalk 1.5.
- Features: `openai/whisper-tiny`; VAE: `stabilityai/sd-vae-ft-mse`. Upstream code/model/component licenses apply separately.
- The custom video runner uses OpenCV face detection and smoothed boxes; later renders reject implausible tracking jumps. Katherine Maher's profile-angle clip uses a manually reviewed fixed box. Still-portrait face masks are cached. One-frame source deficits are handled by holding the final frame.

## Evidence index

| Record | Location |
|---|---|
| Complete per-identity provenance, prompts, seeds, inputs, hashes and generation metadata | [provenance.json](provenance.json) |
| Each exported test file and SHA256 | [asset_manifest.json](asset_manifest.json) and `videos/T*.json` |
| Attribution and source licenses | [SOURCE_CREDITS.md](SOURCE_CREDITS.md) |
| Model revisions | [production_versions.json](production_versions.json) |
| Technical and visual QA | [QA_REPORT.md](QA_REPORT.md), `media_qa.json`, `visual_qa.json`, `speech_qa.json` |
| Original recordings and source metadata (full project) | `assets/sources/` |
| Portraits and prompt records (full project) | `assets/synthetic/` |
| Generated audio and per-voice records (full project) | `assets/cloned/voices/` and `assets/synthetic/voices/` |
| Master videos and per-master records (full project) | `assets/masters/` |
| Production and transformation code (full project) | `production/` |

Paths beginning `assets/` or `production/` are relative to the project root and are retained in the full project, not duplicated in the delivery ZIP. The portable `provenance.json` includes their relevant metadata and hashes.

## Review limits

- All 90 exports passed technical decoding/format checks. Frames at 5s and 20s were inspected for all 30 masters. This does not establish continuous lip synchronization or absence of transient artifacts.
- Twenty generated speech tracks were automatically transcribed; final transcripts differ from the script by at most two words. That is not a listening, accent, voice-likeness or naturalness assessment.
- The genuine Irish male excerpt contains interviewer interjections. The British male source is Cumbrian regional English and discusses dialect vocabulary. Labels retain the original matrix terminology.
- Cameras, lighting, scripts, face size and microphone occlusion vary across genuine sources. Generated portraits have still bodies/backgrounds.
- No detector result, accuracy level, subject consent or statistical confidence is implied by the presence of these files.
