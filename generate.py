import json
import urllib.request
import os
from datetime import datetime

TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = "luqmanfadlli/NuvioMobile-iOS"
API_URL = f"https://api.github.com/repos/{REPO}/releases"

headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
}
if TOKEN:
    headers["Authorization"] = f"Bearer {TOKEN}"

req = urllib.request.Request(API_URL, headers=headers)
with urllib.request.urlopen(req) as resp:
    releases = json.loads(resp.read())

versions = []
for release in releases:
    ipa_asset = next(
        (a for a in release.get("assets", []) if a["name"].endswith(".ipa")), None
    )
    if not ipa_asset:
        continue
    versions.append({
        "version": release["tag_name"].lstrip("v"),
        "date": release["published_at"][:10],
        "localizedDescription": (release.get("body") or "").strip()[:300],
        "downloadURL": ipa_asset["browser_download_url"],
        "size": ipa_asset["size"],
    })

source = {
    "name": "Nuvio Mobile",
    "identifier": "com.nuviomobile.source",
    "apiVersion": "v2",
    "subtitle": "Unofficial Nuvio Mobile IPA source",
    "description": "Auto-updated Nuvio Mobile builds from luqmanfadlli's GitHub releases.",
    "iconURL": "https://github.com/NuvioMedia/NuvioMobile/raw/main/NuvioMobile/Assets.xcassets/AppIcon.appiconset/1024.png",
    "apps": [
        {
            "name": "Nuvio Mobile",
            "bundleIdentifier": "com.nuviomedia.nuviomobile",
            "developerName": "luqmanfadlli",
            "subtitle": "Unofficial full-featured Nuvio build",
            "localizedDescription": "An unofficial build of Nuvio Mobile for iOS with full features enabled.",
            "iconURL": "https://github.com/NuvioMedia/NuvioMobile/raw/main/NuvioMobile/Assets.xcassets/AppIcon.appiconset/1024.png",
            "tintColor": "000000",
            "screenshotURLs": [],
            "versions": versions,
        }
    ],
    "news": [],
}

with open("apps.json", "w") as f:
    json.dump(source, f, indent=2)

print(f"Written {len(versions)} versions.")
