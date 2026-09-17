# Production QA

- 90 exported videos checked: duration, dimensions, H.264/AAC formats, frame rates, matching hashes and full-file decoding.
- Twenty generated speech files automatically transcribed. The Scottish female cloned speech was regenerated after an incomplete first attempt; the repaired file is the delivered version.
- Automatic transcript word differences range from 0 to 2 against the 83-word script. These differences do not establish which words were actually spoken incorrectly.
- All ten genuine and ten fully synthetic masters visually inspected at 5 and 20 seconds. Cloned master visual review status is recorded separately in visual_qa.json.
- Reference freeze checks on the genuine Indian male variants found approximately 0.53-second Patchy holds at 10 and 20 seconds and 2-second Degraded holds at 8, 16 and 24 seconds. All variants use the same rendering recipe.
- Review-page JavaScript syntax, 90 unique case IDs and outcome-classification logic checked. Local-server browser verification is recorded below.

## Not verified
- Human listening: intended accents, voice resemblance, naturalness and audio quality.
- Continuous audiovisual synchronization and every frame of facial animation.
- Actual OBS audio routing, Teams reception, detector bot readiness or detector outputs.
- Statistical confidence or real-network response; these are outside the agreed production scope.

No detector results are invented or pre-filled. Technical checks apply to media files, not detection accuracy.

## Test-bed verification — 2026-09-16

- All 90 video paths returned correct MP4 content types, file lengths and byte-range bodies through the loopback server. Missing paths, invalid ranges and foreign origins were rejected as expected.
- In the available Chromium-based in-app browser, T01-T03, T31-T33, T61-T63 and T90 loaded with 30-second duration, expected dimensions, readyState 4 and no media error. Genuine, cloned and synthetic pictures were visibly rendered; playback advanced for each identity type.
- Play/pause and restart were exercised; selecting filters changed to matching cases and Next respected the filter. Reloading the page preserved an isolated UI test record; duplicate IDs were rejected. The normal results view remained empty. No detector result was fabricated.
- No browser console errors were observed. Chrome and Edge themselves were not available to the browser tool, so their direct-file behavior and the user's original failure remain unconfirmed. Use Start_Test_Bed.cmd and the local address as the supported launch path.
- Export/import controls were retained but were not exercised in this browser pass. Human audio/lip-sync review and OBS/Teams/bot execution remain outstanding.
