import json
from pathlib import Path

messages = json.loads(Path("../../stats_app/start_messages.json").read_text())
path = Path("/home/hamza/.burr/EXP/annotations.jsonl")
ann = [json.loads(line) for line in path.read_text().split("\n") if line.strip()]
Path("annotations.json").write_text(json.dumps(ann, indent=2))
print(ann)
print(messages)