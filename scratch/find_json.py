import os

root_dir = r"c:\Users\User\Desktop\Akademik İngilizce Uygulamaları"
json_files = []
for root, dirs, files in os.walk(root_dir):
    # Ignore node_modules, .git, etc.
    if any(ignore in root for ignore in ["node_modules", ".git", ".vercel", "scratch"]):
        continue
    for file in files:
        if file.endswith(".json"):
            json_files.append(os.path.join(root, file))

print(f"Total JSON files: {len(json_files)}")
for f in json_files:
    print(os.path.relpath(f, root_dir))
