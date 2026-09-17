# Synthetic Identity test pack

Extract the entire ZIP first, then double-click **Start_Test_Bed.cmd**. It starts a local server and opens the test bed in your default browser. You can open **http://127.0.0.1:8769/** in Chrome or Edge while that server is running. Python 3 is required; the launcher automatically finds the installed project or bundled runtime on this machine. Keep the videos folder alongside the HTML page. No internet upload is involved; the server binds only to this computer.

The player now explicitly loads each selected clip and provides Play / pause, Restart, Reload video, and visible loading/error messages. Previous/Next follows the selected filters. If the video fails, use its Open video file link and check that the complete videos folder was extracted. The original reported Chrome/Edge failure was not reproduced; browser verification used the local server in the available Chromium-based in-app browser.

Existing results saved from a directly opened HTML file remain in that browser's original storage. Export them from the old page and import them into the local-server page; browser storage is separate for each address. Always export a backup before moving the pack or changing browsers.

Read **PROVENANCE_AND_GENERATION.md** for the review-ready source and generation record. **provenance.json** retains detailed prompts, generation settings, references, and hashes for all ten persona sets.

Read `TEST_PROTOCOL.md` for the complete matrix, expected results and run procedure. `asset_manifest.json` identifies file availability, hashes, sources and known limitations. `SOURCE_CREDITS.md` must accompany copied or redistributed media. `media_qa.json` reports technical checks, not detector results. The `previews` folder provides contact sheets from all 30 master clips.

## Run order

1. Review the selected clip with sound. Confirm the intended speaker/accent and usable lip motion. Accent labels are targets or source assignments, not verified listening judgments.
2. Load its MP4 into an OBS Media Source. Disable looping, select OBS Virtual Camera in Teams, and route media audio separately to the meeting microphone through a configured virtual audio device.
3. Confirm picture and sound at the receiving end. Add the detector bot, wait for readiness, restart the clip at zero and play its full 30 seconds.
4. Record the actual bot label and score, timing, environment, evidence reference and notes. Use a separate run ID for each attempt. Keep failures and reruns.
5. Export results JSON from the review page. Browser storage is a convenience, not the only copy of your results. An empty `results_template.json` is also supplied for another recording workflow.

## Outcome rules

- Genuine: expected **Not fake**. Fake is a false positive; Inconclusive is a separate unexpected outcome.
- Cloned and Fully synthetic: expected **Fake or Inconclusive**. Record these separately. Not fake is a false negative.
- Missing output or technical failure: **Run error**, not Inconclusive.
- Any error rate is acceptable if documented. No detector runs have been performed during asset production.

## What the files contain

- T01-T30: real recordings, with original face/voice retained.
- T31-T60: representations of those real people using cloned speech and generated lip motion. The generated statements were not made by those people.
- T61-T90: invented portraits, designed voices and generated lip motion. Outside the animated face area, the portrait is still. This is the group originally labelled Deepfake.
- Each three-case block is Good, Patchy, Degraded. Compression, frame-rate reduction and frame holds are baked into the files. No live packet-loss/latency simulation occurs; audio stays continuous. The test protocol contains exact settings.
- Source quality, camera framing and scripts vary. Genuine Irish male material includes brief interviewer interjections. The English male source is Cumbrian and discusses dialect vocabulary. These limitations are recorded in the manifest.

The media are controlled test material. Source-person names and credits describe provenance; they do not imply endorsement. Fully synthetic accents come from voice-generation prompts, not from the appearance of the portraits.

## Production files

The enclosing project also retains source recordings, reference audio, master videos, generation prompts, scripts, downloaded model files and `PROJECT_STATE.md` for resuming work. These are not needed to play the exported MP4s. Keep the entire output folder together so review-page links continue to work.
