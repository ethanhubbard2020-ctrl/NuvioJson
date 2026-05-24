import json
import urllib.request
import os

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

appstore_versions = []
full_versions = []

for release in releases:
    assets = release.get("assets", [])
    tag = release["tag_name"].lstrip("v")
    date = release["published_at"][:10]
    desc = (release.get("body") or "").strip()[:300]

    for asset in assets:
        if not asset["name"].endswith(".ipa"):
            continue
        entry = {
            "version": tag,
            "date": date,
            "localizedDescription": desc,
            "downloadURL": asset["browser_download_url"],
            "size": asset["size"],
        }
        if "AppStore" in asset["name"]:
            appstore_versions.append(entry)
        else:
            full_versions.append(entry)

icon = "https://github.com/NuvioMedia/NuvioMobile/raw/main/NuvioMobile/Assets.xcassets/AppIcon.appiconset/1024.png"

source = {
    "name": "Nuvio Mobile",
    "identifier": "com.nuvio.media.source",
    "apiVersion": "v2",
    "subtitle": "Unofficial Nuvio Mobile IPA source",
    "description": "Auto-updated Nuvio Mobile builds from luqmanfadlli's GitHub releases.",
    "iconURL": icon,
    "apps": [
        {
            "name": "Nuvio (AppStore)",
            "bundleIdentifier": "com.nuvio.media",
            "developerName": "luqmanfadlli",
            "subtitle": "AppStore variant",
            "localizedDescription": "AppStore build of Nuvio Mobile.",
            "iconURL": icon,
            "tintColor": "000000",
            "screenshotURLs": [],
            "versions": appstore_versions,
        },
        {
            "name": "Nuvio (Full)",
            "bundleIdentifier": "com.nuvio.media.full",
            "developerName": "luqmanfadlli",
            "subtitle": "Full variant with all features",
            "localizedDescription": "Full build of Nuvio Mobile with all features enabled.",
            "iconURL": icon,
            "tintColor": "000000",
            "screenshotURLs": [],
            "versions": full_versions,
        },
    ],
    "news": [],
}

with open("apps.json", "w") as f:
    json.dump(source, f, indent=2)

print(f"AppStore versions: {len(appstore_versions)}, Full versions: {len(full_versions)}")
