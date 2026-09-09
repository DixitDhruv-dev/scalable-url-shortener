from pathlib import Path


def create_core_structure():
    root = Path.cwd()

    directories = [
        root / "app" / "core",
    ]

    files = [
        root / "app" / "core" / "__init__.py",
        root / "app" / "core" / "config.py",
    ]

    print(f"Working directory: {root}")
    print()

    # Create directories
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"[DIR]  {directory.relative_to(root)}")

    # Create files without overwriting existing files
    for file in files:
        if file.exists():
            print(f"[SKIP] {file.relative_to(root)} already exists")
        else:
            file.touch()
            print(f"[FILE] {file.relative_to(root)}")

    print("\nCore structure created successfully.")


if __name__ == "__main__":
    create_core_structure()