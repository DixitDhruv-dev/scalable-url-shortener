from pathlib import Path


def create_db_structure():
    root = Path.cwd()

    db_dir = root / "app" / "db"

    files = [
        db_dir / "__init__.py",
        db_dir / "database.py",
        db_dir / "models.py",
    ]

    # Create directory
    db_dir.mkdir(parents=True, exist_ok=True)
    print(f"[DIR]  {db_dir.relative_to(root)}")

    # Create files
    for file in files:
        if file.exists():
            print(f"[SKIP] {file.relative_to(root)} already exists")
        else:
            file.touch()
            print(f"[FILE] {file.relative_to(root)}")

    print("\nDatabase structure created successfully.")


if __name__ == "__main__":
    create_db_structure()