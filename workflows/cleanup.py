import os

from utils import Log

from workflows.aggregate import get_file_paths
from workflows.scrape import DIR_INDEX, get_file_path, get_search_text_list

log = Log('cleanup')


def cleanup_files():
    search_text_list = get_search_text_list()
    valid_file_path_list = set(
        [get_file_path(search_text) for search_text in search_text_list]
    )
    existing_file_paths = get_file_paths()
    n = len(existing_file_paths)
    n_removed = 0
    for file_path in existing_file_paths:
        if file_path not in valid_file_path_list:
            log.warning(f'Invalid: {file_path}. Deleting!')
            os.remove(file_path)
            n_removed += 1

    log.info(f'✅ Removed {n_removed}/{n} files.')

def cleanup_dirs():
    n = 0
    n_removed = 0
    for dir_only in os.listdir(DIR_INDEX):
        dir_path = os.path.join(DIR_INDEX, dir_only)
        if not os.path.isdir(dir_path):
            continue
        for dir2_only in os.listdir(dir_path):
            dir2_path = os.path.join(dir_path, dir2_only)
            if not os.path.isdir(dir2_path):
                continue
            n += 1
            data_file_list = [
                x
                for x in os.listdir(os.path.join(dir2_path))
                if x.endswith('.tsv')
            ]
            n_data_files = len(data_file_list)
            if n_data_files == 0:
                log.warning(f'Empty: {dir2_path}. Deleting!')
                os.rmdir(dir2_path)
                n_removed += 1
    log.info(f'✅ Removed {n_removed}/{n} dirs.')
    
def cleanup():
    cleanup_files()
    cleanup_dirs()

if __name__ == '__main__':
    cleanup()
