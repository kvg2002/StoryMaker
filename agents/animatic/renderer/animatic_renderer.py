#!/usr/bin/env python3
"""animatic_renderer.py — 타임라인 JSON → 애니매틱 mp4
사용법: python3 animatic_renderer.py timeline.json output.mp4
zoompan 떨림 방지: 입력 이미지를 초고해상도로 업스케일 후 zoompan 적용
"""
import json, subprocess, sys, os, math

FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
W, H = 1280, 720
UPSCALE_W = 6400  # 떨림 방지용 업스케일 폭 (출력의 5배)

def esc(t):
    return (t or "").replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'").replace(",", "\\,").replace("%","\\%")

def motion_filter(motion, dur, fps):
    """movement 타입 → zoompan 필터. 업스케일 전제."""
    frames = int(dur * fps)
    m = (motion or {}).get("type", "static")
    base = f"zoompan=d={frames}:s={W}x{H}:fps={fps}"
    cx, cy = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
    if m == "static":
        return None  # zoompan 불필요
    if m in ("dolly-in", "zoom-in"):
        # 1.0 → 1.15 선형 (프레임 기반 보간이 떨림 없음)
        return f"{base}:z='1+0.15*on/{frames}':x='{cx}':y='{cy}'"
    if m in ("dolly-out", "zoom-out"):
        return f"{base}:z='1.15-0.15*on/{frames}':x='{cx}':y='{cy}'"
    if m in ("pan-right", "pan"):
        return f"{base}:z=1.1:x='(iw-iw/zoom)*on/{frames}':y='{cy}'"
    if m == "pan-left":
        return f"{base}:z=1.1:x='(iw-iw/zoom)*(1-on/{frames})':y='{cy}'"
    if m in ("tilt-up", "tilt"):
        return f"{base}:z=1.1:x='{cx}':y='(ih-ih/zoom)*(1-on/{frames})'"
    if m == "tilt-down":
        return f"{base}:z=1.1:x='{cx}':y='(ih-ih/zoom)*on/{frames}'"
    if m == "tracking":
        return f"{base}:z=1.12:x='(iw-iw/zoom)*on/{frames}':y='{cy}'"
    if m == "handheld":
        # 미세 사인파 흔들림 (±0.3% — 절제)
        return (f"{base}:z=1.06:"
                f"x='{cx}+iw*0.003*sin(on/3)':y='{cy}+ih*0.003*sin(on/2.3)'")
    return None

def overlay_filters(ov):
    f = []
    if ov.get("info"):
        f.append(f"drawtext=fontfile={FONT}:text='{esc(ov['info'])}':fontcolor=white@0.85:fontsize=26:x=30:y=26:box=1:boxcolor=black@0.45:boxborderw=10")
    if ov.get("caption"):
        f.append(f"drawtext=fontfile={FONT}:text='{esc(ov['caption'])}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=h-110:box=1:boxcolor=black@0.6:boxborderw=14")
    if ov.get("audio_note"):
        f.append(f"drawtext=fontfile={FONT}:text='♪ {esc(ov['audio_note'])}':fontcolor=white@0.7:fontsize=24:x=(w-text_w)/2:y=h-52:box=1:boxcolor=black@0.4:boxborderw=8")
    return f

def title_card(text, dur, fps, out):
    vf = f"drawtext=fontfile={FONT}:text='{esc(text)}':fontcolor=white:fontsize=44:x=(w-text_w)/2:y=(h-text_h)/2"
    run(["ffmpeg","-y","-f","lavfi","-i",f"color=black:s={W}x{H}:r={fps}","-t",str(dur),
         "-vf",vf,"-c:v","libx264","-pix_fmt","yuv420p",out])

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR:", r.stderr[-600:]); sys.exit(1)

def main(timeline_path, output):
    tl = json.load(open(timeline_path, encoding="utf-8"))
    fps = tl.get("fps", 24)
    os.makedirs("_clips", exist_ok=True)
    clips = []
    idx = 0

    for cut in tl["cuts"]:
        # 씬 타이틀 카드
        if cut.get("title_card"):
            out = f"_clips/c{idx:03d}.mp4"; idx += 1
            title_card(cut["title_card"], cut.get("duration", 1.5), fps, out)
            clips.append(out); continue

        dur = float(cut["duration"])
        mf = motion_filter(cut.get("motion"), dur, fps)
        vf_parts = []
        if mf:
            # 업스케일 → zoompan (떨림 방지 핵심)
            vf_parts.append(f"scale={UPSCALE_W}:-2")
            vf_parts.append(mf)
        else:
            vf_parts.append(f"scale={W}:{H}:force_original_aspect_ratio=decrease")
            vf_parts.append(f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2:color=black")
        vf_parts += overlay_filters(cut.get("overlays", {}))
        out = f"_clips/c{idx:03d}.mp4"; idx += 1
        cmd = ["ffmpeg","-y","-loop","1","-i",cut["image"],"-t",str(dur),
               "-vf",",".join(vf_parts),"-r",str(fps),
               "-c:v","libx264","-pix_fmt","yuv420p",out]
        run(cmd)
        clips.append(out)

    # 전환: 현재 버전은 하드컷 concat (디졸브는 xfade로 확장 가능)
    with open("_clips/concat.txt","w") as f:
        for c in clips: f.write(f"file '{os.path.abspath(c)}'\n")
    run(["ffmpeg","-y","-f","concat","-safe","0","-i","_clips/concat.txt","-c","copy",output])
    dur = subprocess.run(["ffprobe","-v","quiet","-show_entries","format=duration","-of","csv=p=0",output],
                         capture_output=True, text=True).stdout.strip()
    print(f"OK: {output} ({float(dur):.1f}s, cuts={len(clips)})")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
