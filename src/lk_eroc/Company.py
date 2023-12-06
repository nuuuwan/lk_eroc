import json
from dataclasses import dataclass
from functools import cached_property

from utils import File, Log, TSVFile

from utils_future import WWW

log = Log('Company')


@dataclass
class Company:
    name: str
    registration_no: str

    def __str__(self) -> str:
        return f"Company({self.name} - {self.registration_no})"

    def to_dict(self) -> dict:
        return dict(name=self.name, registration_no=self.registration_no)

    @cached_property
    def registration_no_digits(self) -> str:
        s = [c for c in self.registration_no if c.isdigit()]
        return ''.join(s)

    @cached_property
    def registration_no_alphas(self) -> str:
        s = [c for c in self.registration_no if c.isalpha()]
        return ''.join(s)

    def __lt__(self, other):
        return str(self) < str(other)

    def __hash__(self) -> int:
        return hash(str(self))

    @staticmethod
    def __search_page__(search_text: str, eroc_token: str, page: int):
        url = 'https://erocapiv2.drc.gov.lk/api/v1/eroc/name/search'

        content = WWW(url).post(
            dict(
                criteria="2",
                searchtext=search_text,
                page=page,
                token=eroc_token,
            )
        )
        try:
            data = json.loads(content)
        except Exception as e:
            log.error(f'Error parsing JSON: {e}')
            return [], 0

        company_list = [Company(**d) for d in data['availableData']['data']]
        meta = data['availableData']['meta']
        last_page = int(meta['last_page'])
        len(company_list)

        return company_list, last_page

    @staticmethod
    def list_from_search(search_text: str, eroc_token: str):
        page = 1
        company_list = []
        while True:
            company_list_for_page, last_page = Company.__search_page__(
                search_text, eroc_token, page
            )
            company_list += company_list_for_page
            if page == last_page:
                break
            page += 1

        company_list = sorted(Company.dedupe(company_list))
        return company_list

    @staticmethod
    def write_list(company_list, path):
        d_list = [
            dict(name=company.name, registration_no=company.registration_no)
            for company in company_list
        ]
        if len(company_list) > 0:
            TSVFile(path).write(d_list)
        else:
            File(path).write('')

    @staticmethod
    def dedupe(company_list: list['Company']) -> list['Company']:
        return list(set(company_list))

    @staticmethod
    def group_by_type(
        company_list: list['Company'],
    ) -> dict[str, list['Company']]:
        group_to_company_list = {}
        for company in company_list:
            group = company.registration_no_alphas
            if group not in group_to_company_list:
                group_to_company_list[group] = []
            group_to_company_list[group].append(company)
        return group_to_company_list
