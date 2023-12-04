import argparse
import os
import random
import time

from utils import Log, SECONDS_IN

from lk_eroc import Company

DIR_DATA = 'data'
DIR_INDEX = os.path.join(DIR_DATA, 'index')
SPACE = ' '
SPACE_REPLACE = '_' * 2
RESERVED_WORD_SUFFIX = '_'
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
MAX_SCRAPE_TIME = SECONDS_IN.MINUTE * 10

log = Log('scraper')

log.debug(f'⏱{MAX_SCRAPE_TIME=}')


def get_search_text_list() -> list[str]:
    search_text_list = []
    for c1 in ALPHA:
        for c2 in ALPHA:
            for c3 in ALPHA:
                search_text_list.append(c1 + c2 + c3)
                search_text_list.append(c1 + SPACE + c2 + c3)
                search_text_list.append(c1 + c2 + SPACE + c3)
    return search_text_list


def get_file_prefix(search_text: str) -> str:
    file_prefix = search_text.replace(SPACE, SPACE_REPLACE)
    if file_prefix in ['AUX', 'CON', 'PRN']:
        return file_prefix + RESERVED_WORD_SUFFIX
    return file_prefix


def scrape_for_search_text(search_text: str, eroc_token: str) -> bool:
    file_prefix = get_file_prefix(search_text)
    dir_path = os.path.join(DIR_INDEX, file_prefix[0:1], file_prefix[1:2])
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    path = os.path.join(dir_path, file_prefix + '.tsv')

    if os.path.exists(path):
        log.warning(f"☑️ {path} exists. Skipping.")
        return False

    company_list = Company.list_from_search(search_text, eroc_token)
    Company.write_list(company_list, path)
    n_company_list = len(company_list)
    log.info(f"✅ Wrote {n_company_list} companies to {path}.")

    return True


def scrape(eroc_token: str):
    n_completed = 0
    time_start = time.time()
    search_text_list = get_search_text_list()
    for search_text in search_text_list:
        if scrape_for_search_text(search_text, eroc_token):
            n_completed += 1
            delta_time = time.time() - time_start
            log.debug(f'⏱ {n_completed} completed) {delta_time:.1f}s elapsed.')
            if delta_time > MAX_SCRAPE_TIME:
                break
            random_t = random.random() * 5 + 1
            log.debug(f'😴 Sleeping {random_t:.1f}s...')
            time.sleep(random_t)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--eroc_token', required=True)
    args = parser.parse_args()
    eroc_token = args.eroc_token

    scrape(eroc_token)
