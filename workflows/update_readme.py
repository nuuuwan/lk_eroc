from utils import TIME_FORMAT_TIME, File, Log, Time, TSVFile

from lk_eroc import Company
from workflows.aggregate import ALL_PATH
from workflows.build_word_cloud import WORD_CLOUD_PATH

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


def company_list_lines(company_list: list[Company]) -> list[str]:
    n_companies = len(company_list)
    n_display = min(N_EXAMPLES_DISPLAY, n_companies)
    lines = ['']
    for i in range(0, n_display):
        j = int(i * (n_companies - 1) / (n_display - 1))
        company = company_list[j]
        lines.append(
            f'* ({j+1:,}) {company.registration_no} - **{company.name}**'
        )
    return lines

def example_company_lines(company_list: list[Company]) -> list[str]:
    lines = [
    
        f'## Selection of {N_EXAMPLES_DISPLAY} Companies',

    ]

    lines.extend(company_list_lines(company_list))
    return lines

def group_by_type_lines(company_list: list[Company]) -> list[str]:
    group_to_company_list = Company.group_by_type(company_list)
    lines = ['','## Selection for Companies by Type']
    sorted_group_and_company_list = sorted(group_to_company_list.items(), key=lambda x: len(x[1]), reverse=True)
    for group, company_list_for_group in sorted_group_and_company_list:
        lines.extend(['', f'### Sample from "{group}" ({len(company_list_for_group):,})'])
        lines.extend(company_list_lines(company_list_for_group))

    lines.append('')
    return lines
    
def main():
    lines = header_lines()

    company_list = [Company(**d) for d in TSVFile(ALL_PATH).read()]

    lines.extend(summary_lines(company_list))

    lines.extend(example_company_lines(company_list))

    lines.extend(group_by_type_lines(company_list))
    
    File(README_PATH).write_lines(lines)
    log.info(f'✅ Wrote {README_PATH}.')


if __name__ == '__main__':
    main()
