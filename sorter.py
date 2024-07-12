import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASE_DIR = Path(r'C:\Users\User\Desktop\sort')

def move_file(file_path, target_dir):
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file_path), str(target_dir / file_path.name))
    except Exception as e:
        print(f'Error occurred when moving file {file_path}: {e}')


def process_directory(directory):
     with ThreadPoolExecutor(max_workers=os.cpu_count() * 2) as executor:
        futures = []
        for entry in directory.iterdir():
            if entry.is_dir():
                futures.append(executor.submit(process_directory, entry))
            elif entry.is_file():
                ext = entry.suffix.lower()
                target_dir = BASE_DIR / ext[1:]
                futures.append(executor.submit(move_file, entry, target_dir))
        
        for future in futures:
            future.result()


def main():
    process_directory(BASE_DIR)


if __name__== "__main__":
    main()
