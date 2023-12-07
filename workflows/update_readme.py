import os

from utils import TIME_FORMAT_TIME, File, Log, Time, TSVFile

from lk_eroc import Company, WordCloud
from workflows.aggregate import ALL_PATH

README_PATH = 'README.md'
N_EXAMPLES_DISPLAY = 10


log = Log('update_readme')


def header_lines() -> list[str]:
    return [
        '# Registrar of Companies - Sri Lanka',
        '',
        'Data Scraped from Registrar of Companies'
        + ' - Sri Lanka (https://eroc.drc.gov.lk)',
        '',
    ]


def summary_lines(company_list: list[Company]) -> list[str]:
    n_companies = len(company_list)
    file_size = os.path.getsize(ALL_PATH)
    file_size_m = file_size / 1_000_000
    time_str = TIME_FORMAT_TIME.stringify(Time.now())
    return [
        f'Scraped **{n_companies:,}** Companies ([{file_size_m:.2f}MB]({ALL_PATH})) as of *{time_str}*.',
        '',
    ]


def latest_company_lines(company_list: list[Company]) -> list[str]:
    N_LATEST = 1_000
    sorted_by_latest = sorted(
        company_list,
        key=lambda x: x.registration_no_digits_int,
    )[-N_LATEST:]
    lines = (
        [
            '',
            f'## Latest {N_LATEST:,} Companies',
        ]
        + company_list_lines(sorted_by_latest, 'latest')
        + ['']
    )
    return lines


def company_list_lines(company_list: list[Company], label: str) -> list[str]:
    n_companies = len(company_list)
    n_display = min(N_EXAMPLES_DISPLAY, n_companies)

    lines = []
    if n_display < n_companies:
        lines = [f'*Sample of {n_display}/{n_companies}*']
    if n_companies > WordCloud.MIN_COMPANIES_FOR_WORD_CLOUD:
        wc = WordCloud(company_list, label)
        wc_path = wc.write()
        lines.append(f'![{wc_path}]({wc_path})')

    for i in range(0, n_display):
        if n_display == 1:
            j = 0
        else:
            j = int(i * (n_companies - 1) / (n_display - 1))
        company = company_list[j]
        lines.append(
            f'* ({j+1:,}) {company.registration_no} - **{company.name}**'
        )
    return lines


def example_company_lines(company_list: list[Company]) -> list[str]:
    lines = [
        '## Selection of Companies',
    ]

    lines.extend(company_list_lines(company_list, 'all'))
    return lines


def group_by_type_lines(company_list: list[Company]) -> list[str]:
    group_to_company_list = Company.group_by_type(company_list)
    lines = ['', '## Selection for Companies by Type']
    sorted_group_and_company_list = sorted(
        group_to_company_list.items(), key=lambda x: len(x[1]), reverse=True
    )
    for group, company_list_for_group in sorted_group_and_company_list:
        lines.extend(
            [
                '',
                f'### "{group}"',
            ]
        )
        lines.extend(company_list_lines(company_list_for_group, group))

    lines.append('')
    return lines


def main():
    lines = header_lines()

    company_list = [Company(**d) for d in TSVFile(ALL_PATH).read()]

    lines.extend(summary_lines(company_list))

    lines.extend(example_company_lines(company_list))

    lines.extend(latest_company_lines(company_list))

    lines.extend(group_by_type_lines(company_list))

    File(README_PATH).write_lines(lines)
    log.info(f'✅ Wrote {README_PATH}.')


if __name__ == '__main__':
    main()
