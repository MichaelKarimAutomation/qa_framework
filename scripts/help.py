"""Print a human-readable listing of every Makefile target along with its inline `#` comment and the shell commands it runs.

Used by `make help` so contributors can discover available commands without
reading the raw Makefile. Targets without a trailing comment are printed
header-only.
"""
import re
from pathlib import Path

makefile = Path(__file__).parent.parent / 'Makefile'
lines = makefile.read_text().splitlines()

target_pattern = re.compile(r'^([\w-]+):[^#]*(?:#\s*(.+))?')

entries = []
i = 0
while i < len(lines):
    match = target_pattern.match(lines[i])
    if match:
        target = match.group(1)
        comment = match.group(2)
        commands = []
        j = i + 1
        while j < len(lines) and lines[j].startswith('\t'):
            commands.append(lines[j].strip())
            j += 1
        entries.append((target, comment, commands))
    i += 1

col = max(len(t) for t, _, _ in entries) + 4

print('\n ===== Available Makefile Commands ===== \n')
for target, comment, commands in entries:
    header = f'{(target + ":"):<{col}}{comment}' if comment else target
    print(header)
    for cmd in commands:
        print(f'  {cmd}')
    print()
