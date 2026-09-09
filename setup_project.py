from pathlib import Path


def create_project_structure():
    # Always work from the directory where this script is executed.
    root = Path.cwd()

    directories = [
        root / "app",
        root / "tests",
        root / ".github",
        root / ".github" / "workflows",
    ]

    files = [
        root / "app" / "__init__.py",
        root / "app" / "main.py",
        root / "tests" / "__init__.py",
        root / ".gitignore",
        root / ".env.example",
        root / "pyproject.toml",
        root / "README.md",
    ]

    print(f"Working directory: {root}")
    print()

    # Create directories.
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"[DIR]  {directory.relative_to(root)}")

    # Create files without overwriting existing files.
    for file in files:
        if file.exists():
            print(f"[SKIP] {file.relative_to(root)} already exists")
        else:
            file.touch()
            print(f"[FILE] {file.relative_to(root)}")

    print("\nProject structure created successfully.")


if __name__ == "__main__":
    create_project_structure()