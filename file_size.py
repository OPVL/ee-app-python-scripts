import argparse
import os


def get_files(
    directory: str,
    include: list[str] | None = None,
    exclude: list[str] | None = None,
) -> list[str]:
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if include and not any(inc in file for inc in include):
                continue
            if exclude and any(exc in file for exc in exclude):
                continue
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            file_list.append((file_path, file_size))
    return file_list


def human_readable_size(size: int | float) -> str | None:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Get top 25 largest files in a directory"
    )
    parser.add_argument("directory", help="Directory to search files in")
    parser.add_argument("--include", help="Comma separated list of patterns to include")
    parser.add_argument("--exclude", help="Comma separated list of patterns to exclude")

    args = parser.parse_args()

    include_patterns = args.include.split(",") if args.include else None
    exclude_patterns = args.exclude.split(",") if args.exclude else None

    files = get_files(args.directory, include_patterns, exclude_patterns)
    sorted_files = sorted(files, key=lambda x: x[1], reverse=True)[:25]

    print(f"{'File Path':<100} {'Size':>10}")
    print("=" * 110)
    for file, size in sorted_files:
        print(f"{file:<100} {human_readable_size(int(size)):>10}")


if __name__ == "__main__":
    main()
