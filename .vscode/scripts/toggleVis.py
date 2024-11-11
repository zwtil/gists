import json
import sys

visTarget = sys.argv[1]

with open(".vscode/settings.json", "r") as f:
    settings = json.load(f)
    settings["files.exclude"][visTarget] = not settings["files.exclude"][visTarget]

with open(".vscode/settings.json", "w") as f:
        json.dump(settings, f, indent=4)


