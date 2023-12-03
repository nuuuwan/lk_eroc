import json
from dataclasses import dataclass

from utils import Log, TSVFile

from utils_future import WWW

log = Log('Company')


@dataclass
class Company:
    name: str
    registration_no: str

    def __str__(self) -> str:
        return f"Company({self.name} - {self.registration_no})"

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
        data = json.loads(content)
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

        return company_list

    @staticmethod
    def write_list(company_list, path):
        d_list = [
            dict(name=company.name, registration_no=company.registration_no)
            for company in company_list
        ]
        TSVFile(path).write(d_list)
