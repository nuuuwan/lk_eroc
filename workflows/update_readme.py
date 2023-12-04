import random

from utils import TIME_FORMAT_TIME, File, Time, TSVFile

from lk_eroc import Company
from workflows.aggregate import ALL_PATH
from workflows.build_word_cloud import WORD_CLOUD_PATH

README_PATH = 'README.md'
N_RANDOM_DISPLAY = 30


def header_lines() -> list[str]:
    return [
        '# Registrar of Companies - Sri Lanka',
        '',
        'Data Scraped from Registrar of Companies'
        + ' - Sri Lanka (https://eroc.drc.gov.lk)',
        '',
        f'![word-cloud]({WORD_CLOUD_PATH})',
        '',
    ]


def summary_lines(company_list: list[Company]) -> list[str]:
    n_companies = len(company_list)
    time_str = TIME_FORMAT_TIME.stringify(Time.now())
    return [
        f'Scraped **{n_companies:,}** Companies as of *{time_str}*.',
        '',
    ]


def first_and_last_lines(company_list: list[Company]) -> list[str]:
    first = company_list[0]
    last = company_list[-1]

    return [
        f'From "{first.name}" to "{last.name}".',
        '',
    ]


def random_company_lines(company_list: list[Company]) -> list[str]:
    n_companies = len(company_list)
    if n_companies <= N_RANDOM_DISPLAY:
        random_company_list = company_list
    else:
        random_company_list = random.sample(company_list, N_RANDOM_DISPLAY)
    random_company_list = sorted(random_company_list, key=lambda c: c.name)

    lines = [
        '',
        f'## List of {N_RANDOM_DISPLAY} Random Companies',
        '',
    ]

    for company in random_company_list:
        lines.append(f'* {company.name} - {company.registration_no}')
    return lines


def main():
    lines = header_lines()

    # summary
    company_list = [Company(**d) for d in TSVFile(ALL_PATH).read()]
    company_list = Company.dedupe(company_list)

    lines.extend(summary_lines(company_list))
    lines.extend(first_and_last_lines(company_list))
    lines.extend(random_company_lines(company_list))

    File(README_PATH).write_lines(lines)


if __name__ == '__main__':
    main()
