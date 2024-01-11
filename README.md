# Backporter

---

## Install

---
```
python setup.py sdist bdist_wheel
pip install dist/backporter-0.1.tar.gz
```

## Usage

```
python3 -m backporter $BEFORE_FILE $AFTER_FILE $TARGET_FILE > $TARGET_FILE.patched.c 2>>examples.log
```


## Test examples

```
sh example.sh
```

---

## Objective:

Develop a small, efficient Python-based solution for backporting changes
from the recently updated C file to the old one.

Language & Tools: Python, with permissible use of common external tools
compatible with Ubuntu or other Linux OSes.

Format: Proof-of-concept. Focus on functionality and efficiency rather than
extensive development time.

## Task Description:

---
Script Functionality:
- Input: Accept three .c files as arguments (before, after, target) from the
Command Line Interface (CLI). before – the original file before the patch,
after – a patched version, target – an old version of the same file to apply
patch to.
- Primary Task:
- Find the difference (diff) between the “before” and “after” files
called the “patch”.
- Attempt to apply the patch to the third “target” .c file. This process
is known as "backporting".
- Handling Merge Conflicts:
- The script should recognize potential merge conflicts during
backporting.
- The script should automatically apply as many hunks from the
patch as possible.
- For hunks with merge conflicts, leave those parts of the file
unchanged.
- Log details about which hunks were successfully applied and which
had conflicts.
- Conflicts should be identified in the log by stating the start and end
lines of the conflicted hunks in the resultant file.

- Output:
resulting .c file with all or partially applied hunks, name the file
“result.c”.
A log file detailing the applied hunks and merge conflicts.
