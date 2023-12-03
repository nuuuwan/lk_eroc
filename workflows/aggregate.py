import os

from utils import Log, TSVFile

from workflows.scrape import DIR_DATA, DIR_INDEX

log = Log('aggregate')

ALL_PATH = os.path.join(DIR_DATA, 'companies.tsv')


def get_file_paths() -> list[str]:
    file_path_list = []
    for root, _, files in os.walk(DIR_INDEX):
        for file in files:
            file_path = os.path.join(root, file)
            file_path_list.append(file_path)
    log.debug(f"Found {len(file_path_list)} files.")
    return file_path_list


def aggregate():
    file_path_list = get_file_paths()
    if not file_path_list:
        log.warning("No files found. Aborting.")
        return

    data_list = []
    for file_path in file_path_list:
        data_list += TSVFile(file_path).read()
    data_list.sort(key=lambda d: d['name'])
    TSVFile(ALL_PATH).write(data_list)
    log.info(f"✅ Wrote {len(data_list)} companies to {ALL_PATH}.")


if __name__ == '__main__':
    aggregate()
