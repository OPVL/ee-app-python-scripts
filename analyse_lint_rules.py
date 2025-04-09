import json
import logging
import os
import sys

import yaml

_LOGGER = logging.getLogger(__name__)


def find_analysis_options_files(directory: str) -> list[str]:
    analysis_options_files: list[str] = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "analysis_options.yaml":
                analysis_options_files.append(os.path.join(root, file))
    return analysis_options_files


def print_tree(files: list[str]) -> None:
    """Prints the directory tree of the given files."""
    tree = {}
    for file in files:
        parts = file.split(os.sep)
        current_level = tree
        for part in parts:
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]

    def print_dict(d, indent: int = 0):
        for key, value in d.items():
            print(" " * indent + key)
            print_dict(value, indent + 2)

    print_dict(tree)


def load_yaml_rules(file_path: str) -> dict[str, dict]:
    """Load YAML file and convert it to a dictionary."""
    with open(file_path, "r") as file:
        yaml_content = yaml.safe_load(file)

    rules_dict: dict[str, dict[str, str]] = {}
    for key, value in yaml_content.items():
        if isinstance(value, dict):
            rules_dict[key] = value
        else:
            rules_dict[key] = {"rule": value}

    return rules_dict


if __name__ == "__main__":
    _LOGGER.setLevel(logging.DEBUG)
    if len(sys.argv) != 2:
        print("Usage: python analyse_lint_rules.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    files = find_analysis_options_files(directory)
    print_tree(files)
    print(f"Gathered {len(files)} analysis_options.yaml")

    root_rules = load_yaml_rules(files.pop(0))
    root_lint_rules = root_rules["linter"]["rules"]

    with open("root.json", "w") as f:
        json.dump(root_rules, f)
        f.close()

    child = str(files[-1])
    ex_child_rules = load_yaml_rules(child)
    name = child.replace("./", "").replace("/", "-")
    with open(f"{name}.json", "w") as f:
        json.dump(ex_child_rules, f)
        f.close()

    empty = 0
    no_lint_rules = 0
    no_unique_lint_rules = 0

    for child in files:
        child = str(child)
        rules_filename = child.replace("./", "").replace("/", "-")

        try:
            rules = load_yaml_rules(child)
        except AttributeError as e:
            _LOGGER.error(f"analysing ({child}) failed")
            empty += 1
            os.remove(child)
            continue

        try:
            lint_rules = rules["linter"]["rules"]
        except KeyError as e:
            _LOGGER.warning(f"{child} has no lint rules")
            no_lint_rules += 1
            os.remove(child)
            continue

        if not lint_rules:
            _LOGGER.warning(f"{child} has no lint rules")
            no_lint_rules += 1
            os.remove(child)
            continue

        print(lint_rules, type(lint_rules))

        duplicate_rules = []

        for rule, value in lint_rules.items():
            print(rule)
            try:
                found = root_lint_rules[rule]
                if found == value:
                    print(f"found duplicate rule in child: {child}")
                    print(f"{rule}:{value}")
                    duplicate_rules.append(rule)

            except KeyError:
                pass

        for dupe in duplicate_rules:
            lint_rules.pop(dupe)

        if len(lint_rules) < 1:
            print(f"no unique rules found in {child}")
            no_unique_lint_rules += 1
            os.remove(child)

    print(f"found {empty} empty analyis files")
    print(f"{(empty / len(files)) * 100}% of all analysis files")

    print(f"found {no_lint_rules} analyis files with no lint rules")
    print(f"{(no_lint_rules / len(files)) * 100}% of all collected analysis files")

    print(f"{no_unique_lint_rules} files contained no unique lint rules")
    print(
        f"{(no_unique_lint_rules / len(files)) * 100}% of all collected analysis files"
    )
