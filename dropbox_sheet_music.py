#!/usr/bin/env python3

"""
Speed up GGPB sheet music downloading 
otherwise it's so much damn clicking!
Tested with Clar 2 & Trumpet 2 and on
3 different macs, but should work for
any instrument and part. 4.26.2026 
ST, vibe-coded w Claude.

Directory structure assumed:
    week > pieces > sections > pdf parts

First Get a token (expires after ~4 hours):
    1. Go to https://dropbox.github.io/dropbox-api-v2-explorer/#files_list_folder
    2. Click "Get Token" (top right) — log in with any Dropbox account, even a free one
    3. Copy the full token string
    4. Either pass it as --token or set env var DROPBOX_TOKEN in your shell of choice
    e.g. in bash: export DROPBOX_TOKEN="sl.u.AbCdEf...reallylongstring..."

Then go to the dropbox folder with the GGPB music, navigate to the level of 
week of interest, then copy that url to paste as an option.

Options:
    --url            (required) Dropbox shared folder URL including rlkey param
    --search         (required) Filename string to match, e.g. "Clarinet 2"
    --section        Only descend into section folders matching this, e.g. "Woodwinds"
    --out            Local download directory (default: ./downloads)
    --token          Dropbox API token (or set env var DROPBOX_TOKEN)
    --case-sensitive Make filename matching case-sensitive (def: case-insensitive)
    --dry-run        List matching files without downloading
    --debug          Print raw API paths and responses for troubleshooting

Example Usages:

    python dropbox_sheet_music.py                   \
        --url "https://www.dropbox.com/scl/fo/..."  \
        --search "Clarinet 2"                       \
        --section "Woodwinds"                       \
        --dry-run

    python dropbox_sheet_music.py                   \
        --url "https://www.dropbox.com/scl/fo/..."  \
        --search "Clarinet 2"                       \
        --section "Woodwinds"                       \
        --out absolute/or/relative/path

"""

import argparse
import os
import re
import sys
import requests

API_LIST = "https://api.dropboxapi.com/2/files/list_folder"
API_CONT = "https://api.dropboxapi.com/2/files/list_folder/continue"
API_DL   = "https://content.dropboxapi.com/2/sharing/get_shared_link_file"

# ---------------------------------------------------------------------------
# Abbreviation expansions, in case of file name shortcuts
# ---------------------------------------------------------------------------
ABBREVS = {
    "clar": "clarinet",
    "cl":   "clarinet",
    "ob":   "oboe",
    "fl":   "flute",
    "bsn":  "bassoon",
    "bn":   "bassoon",
    "tpt":  "trumpet",
    "trp":  "trumpet",
    "tbn":  "trombone",
    "hn":   "horn",
    "perc": "percussion",
    "kbd":  "keyboard",
    "ww":   "woodwinds",
    "winds":"woodwinds",
}


def normalize(s):
    s = s.lower()
    s = re.sub(r"[-_\s]+", " ", s)
    s = s.strip()
    words = s.split()
    return " ".join(ABBREVS.get(w, w) for w in words)


def name_matches(name, pattern):
    return normalize(pattern) in normalize(name)


# ---------------------------------------------------------------------------
# Dropbox API helpers
# ---------------------------------------------------------------------------

def list_one_level(token, shared_url, path="", debug=False):
    """List a single folder. path is relative to the shared link root."""
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Content-Type": "application/json",
    }
    payload = {
        "path": path,
        "shared_link": {"url": shared_url},
        "limit": 2000,
    }
    if debug:
        print("\n  [DEBUG] listing path: {}".format(repr(path)))

    resp = requests.post(API_LIST, headers=headers, json=payload)

    if debug:
        names = [e.get("name","?") for e in resp.json().get("entries",[])] if resp.status_code == 200 else []
        print("  [DEBUG] status: {}  path: {}  files: {}".format(resp.status_code, path, names))

    if resp.status_code == 401:
        print("\nERROR: Token expired or invalid. Get a fresh one at:", file=sys.stderr)
        print("  https://dropbox.github.io/dropbox-api-v2-explorer/#files_list_folder", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        err = ""
        try:
            err = resp.json().get("error_summary", resp.text)
        except Exception:
            err = resp.text
        if "restricted_content" not in err:
            print("\n  WARNING listing '{}': {} {}".format(path or "/", resp.status_code, err), file=sys.stderr)
        return []

    data = resp.json()
    entries = data.get("entries", [])
    while data.get("has_more"):
        resp = requests.post(API_CONT, headers=headers, json={"cursor": data["cursor"]})
        data = resp.json()
        entries.extend(data.get("entries", []))
    return entries


def join_path(parent, child_name):
    """Build a Dropbox-style path: /parent/child."""
    parent = parent.rstrip("/")
    return "{}/{}".format(parent, child_name)


# ---------------------------------------------------------------------------
# Tree walker
# ---------------------------------------------------------------------------

def find_pdfs(token, shared_url, section_filter, search, case_sensitive, debug=False):
    """
    Walk three levels:
      root -> piece folders -> section folders -> pdf files
    """
    matched = []
    counters = {"pieces": 0, "sections": 0, "files": 0}

    root_entries = list_one_level(token, shared_url, "", debug=debug)
    pieces = [e for e in root_entries if e.get(".tag") == "folder"]
    print("  Found {} piece(s). Scanning sections...".format(len(pieces)))

    for piece in pieces:
        piece_name = piece.get("name", "")
        # Build path from name to avoid stale/relative path issues
        piece_path = "/{}".format(piece_name)
        counters["pieces"] += 1

        section_entries = list_one_level(token, shared_url, piece_path, debug=debug)
        sections = [e for e in section_entries if e.get(".tag") == "folder"]

        for section in sections:
            sec_name = section.get("name", "")
            if section_filter and not name_matches(sec_name, section_filter):
                continue

            sec_path = join_path(piece_path, sec_name)
            counters["sections"] += 1

            file_entries = list_one_level(token, shared_url, sec_path, debug=debug)
            for f in file_entries:
                if f.get(".tag") != "file":
                    continue
                fname = f.get("name", "")
                counters["files"] += 1
                if not fname.lower().endswith(".pdf"):
                    continue
                hit = (search in fname) if case_sensitive else name_matches(fname, search)
                if hit:
                    matched.append({
                        "name":    fname,
                        "piece":   piece_name,
                        "section": sec_name,
                        "path":    sec_path + "/" + fname,
                    })

        sys.stdout.write("\r  Scanned {}/{} piece(s), {} section(s), {} file(s)...".format(
            counters["pieces"], len(pieces), counters["sections"], counters["files"]))
        sys.stdout.flush()

    print()
    return matched, counters


# ---------------------------------------------------------------------------
# Downloader
# ---------------------------------------------------------------------------

def download_file(token, shared_url, dropbox_path, local_path):
    headers = {
        "Authorization": "Bearer {}".format(token),
        "Dropbox-API-Arg": '{{"url":"{}","path":"{}"}}'.format(shared_url, dropbox_path),
    }
    resp = requests.get(API_DL, headers=headers, stream=True)
    if resp.status_code != 200:
        print("  FAILED ({}): {}".format(resp.status_code, dropbox_path), file=sys.stderr)
        return False
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Download matching PDFs from a shared Dropbox folder.")
    parser.add_argument("--url",            required=True,
                        help="Full shared Dropbox folder URL (include rlkey param)")
    parser.add_argument("--search",         required=True,
                        help="Filename to match, e.g. 'Clarinet 2'")
    parser.add_argument("--section",        default=None,
                        help="Only look inside section folders matching this, e.g. 'Woodwinds'")
    parser.add_argument("--out",            default="./downloads",
                        help="Local output directory (default: ./downloads)")
    parser.add_argument("--token",          default=None,
                        help="Dropbox API token (or set DROPBOX_TOKEN env var)")
    parser.add_argument("--case-sensitive", action="store_true", default=False)
    parser.add_argument("--dry-run",        action="store_true",
                        help="List matching files without downloading")
    parser.add_argument("--debug",          action="store_true",
                        help="Print raw API paths and responses for troubleshooting")
    args = parser.parse_args()

    token = args.token or os.environ.get("DROPBOX_TOKEN")
    if not token:
        print("ERROR: Provide --token or set DROPBOX_TOKEN environment variable.", file=sys.stderr)
        print("Get a token at: https://dropbox.github.io/dropbox-api-v2-explorer/#files_list_folder",
              file=sys.stderr)
        sys.exit(1)

    out_dir = os.path.expanduser(args.out)

    if args.section:
        print("Searching for '{}' in '{}' sections...".format(args.search, args.section))
    else:
        print("Searching for '{}' in all sections...".format(args.search))

    matched, counters = find_pdfs(
        token, args.url, args.section, args.search, args.case_sensitive, debug=args.debug)

    print("Scanned {} piece(s), {} section(s), {} file(s) total.".format(
        counters["pieces"], counters["sections"], counters["files"]))

    if not matched:
        print("No files matching '{}' found.".format(args.search))
        return

    print("\nMatched {} file(s):".format(len(matched)))
    for f in matched:
        print("  [{}] [{}]  {}".format(f["piece"], f["section"], f["name"]))

    if args.dry_run:
        print("\n[Dry run — no files downloaded]")
        return

    print("\nDownloading to: {}".format(out_dir))
    for f in matched:
        local_path = os.path.join(out_dir, f["name"])
        print("  {}".format(f["name"]))
        download_file(token, args.url, f["path"], local_path)

    print("\nDone. Files saved to: {}".format(out_dir))


if __name__ == "__main__":
    main()
