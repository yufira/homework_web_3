import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse


def copy_file(file_path, target_dir):
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, target_dir / file_path.name)
    except Exception as e:
        print(f'Error occurred when copying file {file_path}: {e}')


def process_directory(directory, base_dir):
    with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        futures = []
        for entry in directory.iterdir():
            if entry.is_dir():
                futures.append(executor.submit(process_directory, entry, base_dir))
            elif entry.is_file():
                ext = entry.suffix.lower()
                target_dir = base_dir / ext[1:]
                futures.append(executor.submit(copy_file, entry, target_dir))
                               
        for future in futures:
            future.result()


def main(source_dir, target_dir):
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    process_directory(source_path, target_path)


if __name__== "__main__":
    parser = argparse.ArgumentParser(description="Sort files by extension from source to target directory.")
    parser.add_argument("source", help="Path to the source directory with files to process.")
    parser.add_argument("target", nargs='?', default="dist", help="Path to the target directory where sorted files will be placed. Defaults to 'dist'.")
    args = parser.parse_args()
   
    main(args.source, args.target)
