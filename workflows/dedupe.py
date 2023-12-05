from aggregate import get_file_paths
from utils import File, Log, TSVFile

from lk_eroc import Company

log = Log('dedupe')


def dedupe_file(file_path):
    assert file_path.endswith('.tsv')

    txt_file = File(file_path)
    lines = txt_file.read_lines()
    lines = [line for line in lines if line.strip() != '']
    if len(lines) == 0:
        return

    tsv_file = TSVFile(file_path)
    d_list = tsv_file.read()
    company_list = [Company(**d) for d in d_list]
    company_list = sorted(Company.dedupe(company_list))
    d_list = [company.to_dict() for company in company_list]
    tsv_file.write(d_list)

    txt_file = File(file_path)
    lines = txt_file.read_lines()
    lines = [line for line in lines if line.strip() != '']
    txt_file.write_lines(lines)
    log.info(f'✅ Deduped & Sorted {file_path}.')


def dedupe():
    file_paths = get_file_paths()
    for file_path in file_paths:
        dedupe_file(file_path)


if __name__ == '__main__':
    dedupe()
