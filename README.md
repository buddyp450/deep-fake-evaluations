# Deep-fake evaluations

A 90-case working test pack for evaluating genuine, cloned and fully synthetic identities through OBS, Microsoft Teams and a detection bot.

## Download and run

1. Clone this repository, or update an existing checkout with `git pull --ff-only` after reviewing local changes.
2. Open [the latest release](https://github.com/buddyp450/deep-fake-evaluations/releases/latest) and download **Synthetic_Identity_Assets.zip**.
3. Extract it into the repository's **output** folder. It contains only `videos/`: 90 MP4s and 90 metadata files. Tracked UI, code and documentation are not included or overwritten.
4. With Python 3 installed, run **output/Start_Test_Bed.cmd**, or `python output/serve_test_bed.py --open` from the repository root. Open http://127.0.0.1:8769/.
5. Read **output/START_HERE.md** before running the clips through OBS/Teams. Meeting audio needs its own route; OBS Virtual Camera carries video only.

With GitHub CLI installed, from the repository root:

```powershell
gh release download v1.0.1 --pattern "Synthetic_Identity_Assets.zip"
Expand-Archive .\Synthetic_Identity_Assets.zip -DestinationPath .\output -Force
```

This asset ZIP requires the repository; it is not a standalone app. GitHub's automatic Source code archives do not contain videos.

If you already extracted the old full pack, the videos are unchanged and need no redownload. Inspect `git diff -- output/`; only if you have no changes of your own there, use `git restore --source=HEAD --worktree -- output/` to restore tracked files. Ignored videos remain untouched.

No GPU, generation model, or internet connection is needed to play the downloaded videos. The local server binds only to 127.0.0.1 and serves an explicit list of pack files.

The release also includes a SHA256 checksum file. In PowerShell, compare it with `Get-FileHash .\Synthetic_Identity_Assets.zip -Algorithm SHA256`.

## Contents

- T01–T30: genuine recordings of ten real people.
- T31–T60: cloned representations of those people, using generated speech and replaced lip motion.
- T61–T90: invented identities, using generated portraits, designed voices and animated mouth motion. The original matrix called this group “Deepfake.”
- Each persona has Good, Patchy and Degraded variants, giving 90 thirty-second MP4s.
- Connection effects are baked compression, reduced frame rates/resolution and frame holds. They do not reproduce live network packet loss or Teams adaptation. Audio remains continuous.

Genuine cases should return **Not fake**. Cloned and fully synthetic cases may return **Fake** or **Inconclusive**, recorded separately. Technical failures are **Run error**. No actual detector runs have been performed or prefilled.

## Review documentation

- [Sources and generation methods](output/PROVENANCE_AND_GENERATION.md)
- [Detailed provenance, prompts and hashes](output/provenance.json)
- [Source credits and licenses](output/SOURCE_CREDITS.md)
- [Test protocol](output/TEST_PROTOCOL.md)
- [QA and remaining limitations](output/QA_REPORT.md)
- [Run instructions](output/START_HERE.md)

Source-person credits do not imply endorsement. Generated statements were not made by the depicted people. Keep the attribution and provenance documents with copied media; source and model licenses are documented separately.

## Code and development

`output/` contains the test-bed HTML, Python server, launcher and review records. `production/` contains the custom acquisition, voice-generation, lip-animation, variant-rendering and validation scripts used during production.

For development, extract the release ZIP **into the repository's output folder** so that the clips live at `output/videos/`. Run `python output/serve_test_bed.py` and open the local address above. Do not commit videos or browser results to Git.

The production scripts are historical working scripts, not a one-command rebuild installer. Regeneration additionally requires FFmpeg, appropriate Python environments, upstream repositories/model weights, source recordings, reference audio and synthetic portraits. These large dependencies and inputs are not in Git. Consult provenance for exact references and model revisions. Generated outputs may vary on regeneration.

Human listening, voice-likeness/accent assessment, continuous lip-sync review and actual OBS/Teams/bot testing remain outstanding. Browser QA used the available Chromium-based in-app browser, not independent Chrome and Edge sessions.

Browser results remain on the computer/browser where recorded. Export results JSON to retain a portable copy; moving from file:// to the local server does not automatically move earlier browser records.
