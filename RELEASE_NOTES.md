## Assets-only packaging fix

The release now contains only 90 videos and their 90 metadata files. UI, launchers, code and documentation stay in Git.

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

Validation: all 90 video hashes match the manifest; archive CRC checks pass; no archive path overlaps a tracked file when extracted into output/. The accompanying SHA256 file verifies the download.

Human listening/lip-sync review and actual detector execution remain pending. No detector outcomes are included. Preserve the repository's source credits and provenance with copied media.
