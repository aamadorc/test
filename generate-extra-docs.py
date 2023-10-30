import subprocess

REPO_URL_BASE = "https://github.com/aamadorc/test"
OUTPUT_DIR = "./docs"

print("# Chronological File Changes\n")

files_report = ["data.html", "README.md"]
command = [
    "git",
    "log",
    "--oneline",
    "--name-only",
    "--format=%H%x00%s%x00%aD",
    "refs/heads/master",
]
command.extend(files_report)
result = subprocess.run(
    command,
    input=None,
    capture_output=True,
    encoding="UTF-8",
)
commits = []
files = []
for line in result.stdout.splitlines():
    line = line.rstrip()
    if line == "":
        continue
    _ = line.split("\0")
    if len(_) == 3:
        if len(files) > 0:
            commits[-1].append(files)
            files = []
        commits.append(_)
    else:
        files.append(line)
if len(files) > 0:
    commits[-1].append(files)
    files = []

print("| Commit | Message | Files Changed |")
print("|:---:|:---:|:---:|")

for c in commits:
    row = f"| [{c[2]}]({REPO_URL_BASE}/commit/{c[0]}) |"
    row += f"[{c[2]}]({REPO_URL_BASE}/commit/{c[0]}) |"
    links = []
    for f in files_report:
        if f in c[3]:
            fn=f"{c[0]}-{f}"
            with open(f"{OUTPUT_DIR}/{fn}", "w") as fd:
                result = subprocess.run(
                    ["git", "show", f"{c[0]}:{f}"],
                    input=None,
                    stdout=fd,
                    encoding="UTF-8",
                )
            links.append(f"[{f}]({fn})")
    row += f" {'</br>'.join(links)} |"
    print(row)
