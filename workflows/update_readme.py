import random

from utils import TIME_FORMAT_TIME, File, Time, TSVFile

from lk_eroc import Company
from workflows.aggregate import ALL_PATH
from workflows.build_word_cloud import WORD_CLOUD_PATH

README_PATH = 'README.md'
N_RANDOM_DISPLAY = 30
N_EARLY_DISPLAY = 30


def main():
    lines = [
        '# Registrar of Companies - Sri Lanka',
        '',
        'Data Scraped from Registrar of Companies'
        + ' - Sri Lanka (https://eroc.drc.gov.lk)',
        '',
        f'![word-cloud]({WORD_CLOUD_PATH})',
        '',
    ]

    # random companies
    company_list = [Company(**d) for d in TSVFile(ALL_PATH).read()]
    company_list = Company.dedupe(company_list)

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
        lines.append(f'* {company.name} - {company.registration_no}')

    # early registrations
    early_company_list = sorted(
        company_list, key=lambda c: c.registration_no_only
    )

    lines.extend(
        [
            '',
            '## List of Early Registrations',
            '',
        ]
    )
    for company in early_company_list[:N_EARLY_DISPLAY]:
        lines.append(f'* {company.registration_no} - {company.name} ')

    File(README_PATH).write_lines(lines)


if __name__ == '__main__':
    main()
