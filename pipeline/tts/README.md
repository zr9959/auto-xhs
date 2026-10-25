[中文](README.zh-CN.md) | English

# How voiceover works

## The interface, in one line

Segmented text goes in, audio files plus durations come out.

What goes in is `scripts.txt`, one segment per line, in the format `name|the words to read`, for example:

```
open|Here's something common: jolted awake by the alarm in the morning, and the whole day never recovers.
step1|Let me count it for you. One charge lasts thirty days, and the brightness has twelve levels.
```

What comes out is one audio file per segment (named like `open.mp3`, `step1.mp3`), plus each segment's duration in seconds. The durations are required — the stitching step later uses them to line up picture and sound, and a mismatch means sound and picture drift apart. Any voiceover provider works, as long as this in-out format holds — nothing else in the pipeline needs to change.

## Two free routes

| | edge-tts | sherpa-onnx + MeloTTS |
|---|---|---|
| Online or not | Online — the voice is generated on Microsoft's side | Offline — download the models locally and it reads with no connection |
| Voices | Many, men and women, all ages, pick on the spot | Follows the model — changing voices means changing models |
| Getting started | Fast, install one package and go | A bit slower, download the model files first |
| Suits who | People getting the flow working first, or with small volume | People who don't want to depend on an outside service, or with large volume |

Advice: get the whole flow working with edge-tts first. If it turns flaky, or the volume grows, switch to the local route.

Installing edge-tts: `pip install edge-tts`, and the `edge-tts` command is ready after that. Pick a voice with `--voice` — common Chinese ones are `zh-CN-XiaoxiaoNeural` (female) and `zh-CN-YunyangNeural` (male); the full list comes from `edge-tts --list-voices`.

The local route, roughly: install the sherpa-onnx runtime package, download the MeloTTS Chinese model, feed text in the way its docs describe to get wav, convert to mp3, and measure durations with ffprobe. The details move with the model version, so the exact steps aren't pinned here — read the model page when you install it.

## Smoke-test before real work

Before real synthesis, run the smoke script once to settle which engine this round uses:

```bash
bash pipeline/tts/tts-smoke.sh
```

It reads `config.yaml` for `tts.command` (main engine) and `tts.fallback_command` (backup engine), and test-synthesizes one short line with each. The last line prints the verdict: `LIVE=primary` means the main engine works; `LIVE=fallback` means the main engine failed and the round switches to the backup — use the backup for this round's video and say so on the acceptance checklist; `LIVE=NONE` means neither works — stop and report back with the four required items, don't force a synthesis. An engine only counts as failed on the actual failed call output — never conclude from a feeling like "this service probably isn't there".

## The bundled example script

`tts-edge-example.py` is the smallest example written to the interface above:

```bash
python3 tts-edge-example.py scripts.txt audio-directory
```

It calls edge-tts segment by segment to produce mp3s, prints each segment's duration, and gives a total at the end. Change the voice with an environment variable: `TTS_VOICE=zh-CN-YunyangNeural python3 tts-edge-example.py scripts.txt audio-directory`.

## What to do when one segment's voiceover breaks

A broken segment is common: its duration is clearly longer than the rest of the batch, or a long stretch in the middle has no sound. Don't wait until the whole video is stitched to find out — work through this order:

1. After each segment is generated, measure its duration, then check its silence distribution (the script flags it for you; by hand, use `ffmpeg -i this-segment.mp3 -af silencedetect=noise=-45dB:d=1.5 -f null -`). Any silence over 1 second inside a segment means don't use that segment yet.
2. Retrying the exact same line is allowed exactly 1 time. Past that, it's usually not bad luck — retrying will hand back the same broken result.
3. If it still fails, split the line in half by meaning, generate each half separately, and check each half's duration and silence the same way.
4. Only after splitting still fails, touch the wording: rephrase or change punctuation and generate again. Numbers and facts must not change along with it.
5. Every segment must end up lined up with its picture: know how far apart the picture duration and the voiceover duration are, and if the gap passes half a second, adjust the picture duration — don't leave a dead gap.
