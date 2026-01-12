#!/usr/bin/env python3
"""
speak - Voice cloning CLI for Mac (Apple Silicon)

Usage:
    speak --add-profile <name> --voice <audio.wav> --text <reference.txt>
    speak <profile> "Text to speak"
    speak --list
    speak --play <file.wav>

Profiles stored in: ~/.speak/profiles/<name>/
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

# Config
PROFILES_DIR = Path.home() / ".speak" / "profiles"


def get_profile_dir(name: str) -> Path:
    return PROFILES_DIR / name


def add_profile(name: str, voice_file: str, text_file: str):
    """Add a new voice profile."""
    profile_dir = get_profile_dir(name)
    profile_dir.mkdir(parents=True, exist_ok=True)

    # Copy files
    shutil.copy(voice_file, profile_dir / "reference.wav")
    shutil.copy(text_file, profile_dir / "reference.txt")

    print(f"✅ Profile '{name}' created at {profile_dir}")


def list_profiles():
    """List all available profiles."""
    if not PROFILES_DIR.exists():
        print("No profiles found. Create one with --add-profile")
        return

    profiles = [d.name for d in PROFILES_DIR.iterdir() if d.is_dir()]
    if profiles:
        print("Available profiles:")
        for p in sorted(profiles):
            print(f"  • {p}")
    else:
        print("No profiles found.")


def speak(profile: str, text: str, output: str = None):
    """Generate speech using a voice profile."""
    profile_dir = get_profile_dir(profile)

    if not profile_dir.exists():
        print(f"❌ Profile '{profile}' not found. Use --list to see available profiles.")
        sys.exit(1)

    voice_file = profile_dir / "reference.wav"
    text_file = profile_dir / "reference.txt"

    if not voice_file.exists() or not text_file.exists():
        print(f"❌ Profile '{profile}' is missing reference files.")
        sys.exit(1)

    ref_text = text_file.read_text().strip()

    print("🔄 Loading F5-TTS...")
    from f5_tts_mlx.generate import generate

    print(f"🎤 Generating speech ({len(text)} chars)...")

    # Generate - if output is None, plays directly without saving
    generate(
        generation_text=text,
        ref_audio_path=str(voice_file),
        ref_audio_text=ref_text,
        output_path=output,
    )

    if output:
        print(f"✅ Saved: {output}")


def play_audio(file_path: Path):
    """Play audio file on Mac."""
    print("🔊 Playing...")
    subprocess.run(["afplay", str(file_path)], check=True)


def main():
    parser = argparse.ArgumentParser(
        description="Voice cloning CLI for Mac",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  speak --add-profile daniel --voice ~/voice.wav --text-file ~/reference.txt
  speak daniel "Hello, this is a test!"
  speak daniel "Save this" --output ~/Desktop/output.wav
  speak --list
        """
    )

    parser.add_argument("profile", nargs="?", help="Profile name to use")
    parser.add_argument("text", nargs="?", help="Text to speak")
    parser.add_argument("--add-profile", metavar="NAME", help="Create a new profile")
    parser.add_argument("--voice", "-v", help="Voice reference audio file (WAV)")
    parser.add_argument("--text-file", "-t", dest="text_ref", help="Reference text file")
    parser.add_argument("--output", "-o", help="Save to WAV file (default: play only, don't save)")
    parser.add_argument("--list", "-l", action="store_true", help="List profiles")
    parser.add_argument("--play", "-p", help="Play a WAV file")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    args = parser.parse_args()

    # Handle commands
    if args.list:
        list_profiles()
    elif args.play:
        play_audio(Path(args.play))
    elif args.add_profile:
        if not args.voice or not args.text_ref:
            print("❌ --add-profile requires --voice and --text-file")
            sys.exit(1)
        add_profile(args.add_profile, args.voice, args.text_ref)
    elif args.profile and args.text:
        speak(args.profile, args.text, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

