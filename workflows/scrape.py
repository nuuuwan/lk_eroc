import argparse
import os
import random
import time

from utils import Log

from lk_eroc import Company

DIR_DATA = 'data'
DIR_INDEX = os.path.join(DIR_DATA, 'index')
ALPHA = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ '
MAX_SCRAPES = 30

log = Log('scraper')


def get_search_text_list() -> list[str]:
    search_text_list = []
    for c1 in ALPHA:
        for c2 in ALPHA:
            for c3 in ALPHA:
                search_text_list.append(c1 + c2 + c3)
    return search_text_list


def scrape_for_search_text(search_text: str, eroc_token: str) -> bool:
    file_prefix = search_text.replace(" ", '_')
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
    search_text_list = get_search_text_list()
    n_scrapes = 0
    for search_text in search_text_list:
        if scrape_for_search_text(search_text, eroc_token):
            n_scrapes += 1
            if n_scrapes >= MAX_SCRAPES:
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
