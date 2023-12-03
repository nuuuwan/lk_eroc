import random

from utils import TIME_FORMAT_TIME, File, Time, TSVFile

from lk_eroc import Company
from workflows.aggregate import ALL_PATH

README_PATH = 'README.md'
N_RANDOM_DISPLAY = 30


def main():
    lines = [
        '# Registrar of Companies - Sri Lanka',
        '',
        'Data Scraped from Registrar of Companies'
        + ' - Sri Lanka (https://eroc.drc.gov.lk)',
        '',
    ]
    company_list = [Company(**d) for d in TSVFile(ALL_PATH).read()]
    n_companies = len(company_list)
    time_str = TIME_FORMAT_TIME.stringify(Time.now())
    lines.extend(
        [
            f'Scraped **{n_companies:,}** Companies as of *{time_str}*.',
            '',
            f'## List of {N_RANDOM_DISPLAY} Random Companies',
            '',
        ]
    )
    if n_companies <= N_RANDOM_DISPLAY:
        random_company_list = company_list
    else:
        random_company_list = random.sample(company_list, N_RANDOM_DISPLAY)
    random_company_list = sorted(random_company_list, key=lambda c: c.name)
    for company in random_company_list:
        lines.append(f'* {company.name} ({company.registration_no})')

    File(README_PATH).write_lines(lines)


if __name__ == '__main__':
    main()
