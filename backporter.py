import argparse
import difflib
import os
import sys


def print_stderr(*args: str, **kwargs) -> None:
    print(*args, file=sys.stderr, **kwargs)


def print_stdout(*args: str, **kwargs) -> None:
    print(*args, file=sys.stdout, **kwargs, end="")


BEFORE_FILE_DIFF_1_START_LIST = {"    ", "  - ", "- - ", "-   "}
BEFORE_FILE_DIFF_2_START_LIST = {"    ", "  - ", "+ - ", "+   "}
TARGET_FILE_DIFF_START_LIST = {"    ", "  + ", "+ + ", "+   "}
AFTER_FILE_DIFF_START_LIST = {"    ", "  + ", "- + ", "-   "}


def apply_backport_patch(
    before_filepath: str,
    after_filepath: str,
    target_filepath: str,
):
    print_stderr("Applying patch to target {}".format(target_filepath))
    for f in (before_filepath, after_filepath, target_filepath):
        if not os.path.isfile(f):
            print_stderr(f"{f} is not a file")
            raise SystemExit(1)
    with open(before_filepath, "r") as before_file, open(
        after_filepath, "r"
    ) as after_file, open(target_filepath, "r") as target_file:
        before_file_content = before_file.readlines()
        after_file_content = after_file.readlines()
        target_file_content = target_file.readlines()

    diff1 = list(difflib.ndiff(before_file_content, after_file_content))
    diff2 = list(difflib.ndiff(before_file_content, target_file_content))
    diff3_gen = difflib.ndiff(diff1, diff2)

    target_file_line_cursor = 0
    before_file_line_cursor_2 = 0
    after_file_line_cursor = 0
    before_file_line_cursor_1 = 0
    patched_target_file_line_cursor = 0

    # lines in difflib goes in the order of minus first then plus
    # so, after "+ - ", we await for "+   " or "+ - " or "+ + " or "-   "

    # left side (changes from target) is +
    # right side (patched changes) is -
    right_changes = ""
    left_changes = ""
    for diff_line in diff3_gen:
        diff_line_start = diff_line[:4]
        if "?" in diff_line_start:
            # junk
            continue
        line = diff_line[4:]
        after_file_line_cursor += int(diff_line_start in AFTER_FILE_DIFF_START_LIST)
        target_file_line_cursor += int(diff_line_start in TARGET_FILE_DIFF_START_LIST)
        before_file_line_cursor_1 += int(
            diff_line_start in BEFORE_FILE_DIFF_1_START_LIST
        )
        before_file_line_cursor_2 += int(
            diff_line_start in BEFORE_FILE_DIFF_2_START_LIST
        )

        if diff_line_start in ("    ", "+ + ", "- + ", '  + '):
            if right_changes and left_changes:
                if right_changes != left_changes or diff_line_start == "+ + ":
                    if not (
                        diff_line_start == "+ + "
                        and right_changes == left_changes
                        and line == left_changes
                    ):
                        print_stderr(
                            f"CONFLICT: patching conflict (line {patched_target_file_line_cursor})"
                        )
                        print_stderr(f"CONFLICT: >> {line}", end="")
                        _after_file_line_cursor_from = after_file_line_cursor - (len(left_changes.split('\n')) - 2)
                        print_stderr(
                            (f"CONFLICT: patch changes ({after_filepath} line {f'{_after_file_line_cursor_from} - ' if _after_file_line_cursor_from != after_file_line_cursor else ''}{after_file_line_cursor}):")
                        )
                        formatted_left_changes_err = '\nCONFLICT: >> '.join(filter(lambda x: x, left_changes.split('\n')))
                        print_stderr(f"CONFLICT: >> {formatted_left_changes_err}")
                        if right_changes != left_changes:
                            print_stderr("CONFLICT: Changes from right:")
                            print_stderr(f"CONFLICT: >> {right_changes}", end="")
                        print_stderr("CONFLICT:")
                else:
                    print_stdout(right_changes)
                    patched_target_file_line_cursor += len(right_changes.split("\n"))
            if diff_line_start == '- + ':
                print_stderr(f"PATCHED: line {patched_target_file_line_cursor}, from line {after_file_line_cursor}")
            print_stdout(line)
            patched_target_file_line_cursor += 1
            if right_changes or left_changes:
                right_changes = ""
                left_changes = ""
        elif diff_line_start in ("-   ",):
            if line != "\n" or right_changes or left_changes:
                right_changes += line
        elif diff_line_start in ("+ - ",):
            if line != "\n" or left_changes or right_changes:
                left_changes += line
    print_stderr("Successfully applied patch {}".format(target_filepath))


def cli():
    parser = argparse.ArgumentParser(
        description="Apply Patch to .c Files",
        epilog="This script applies a patch to a target .c file using diff between the "
        "patched and source .c files.",
    )

    parser.add_argument(
        "before", type=str, help="Path to the original file before the patch (.c)"
    )
    parser.add_argument("after", type=str, help="Path to the patched version (.c)")
    parser.add_argument(
        "target",
        type=str,
        help="Path to the old version of the same file to apply the patch to (.c)",
    )

    args = parser.parse_args()
    apply_backport_patch(args.before, args.after, args.target)


if __name__ == "__main__":
    cli()
