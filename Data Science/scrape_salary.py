from bs4 import BeautifulSoup
import requests
import pandas as pd

PAGE_ROOT = "https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page"

# print(result_page)

df = pd.DataFrame(columns=['Major', 'Early Career Pay', 'Mid Career Pay'])

for n in range(1, 32):
    print(f'Page {n}')
    result_page = requests.get(f'{PAGE_ROOT}/{n}').text
    soup = BeautifulSoup(result_page, 'html.parser')
    row_tags = soup.select('.data-table__row')
    for row_tag in row_tags:
        # print(row_tag.getText())
        major_tags = row_tag.select('.data-table__value')
        # for i, mj in enumerate(major_tags):
        #     print(f'{i}:  {mj.getText()}')
        df.loc[len(df)] = [major_tags[1].getText(), 
                        int(major_tags[3].getText().replace("$", "").replace(",", "")), 
                            int(major_tags[4].getText().replace("$", "").replace(",", ""))]
    

df.to_csv('payscale.csv', index=False)
print(df.head())