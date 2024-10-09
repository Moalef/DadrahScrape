import requests
import pandas as pd
from bs4 import BeautifulSoup

address = "https://www.dadrah.ir/related-consulting.php?tags=%D8%AA%D8%AC%D8%A7%D9%88%D8%B2%20%DA%AF%D8%B1%D9%88%D9%87%DB%8C-%D8%AA%D8%AC%D8%A7%D9%88%D8%B2%20%D8%AC%D9%86%D8%B3%DB%8C-%D8%B4%DA%A9%D8%A7%DB%8C%D8%AA%20%D8%AA%D8%AC%D8%A7%D9%88%D8%B2-%D8%AA%D8%AC%D8%A7%D9%88%D8%B2&page="
max_page_num = 52

df = pd.DataFrame(columns=['Title', 'Link', 'Question', 'Tags', 'Date'])

def letters_ar_to_fa(s: str):
    output = [ch if ch != 'ي' else 'ی' for ch in s]
    output = [ch if ch != 'ك' else 'ک' for ch in output]
    return "".join(output)


for i in range(1, max_page_num + 1):
    address_page_number =  address + str(i)
    response = requests.get(address_page_number)
    soup = BeautifulSoup(response.content, 'html.parser')
    topics = soup.find_all(attrs={"class": "media-body"})
    
    for body in topics:       
        case_title = body.find("h5").get_text().strip()
        case_address = "https://www.dadrah.ir" + body.find("a")["href"]
        response1 = requests.get(case_address)
        soup1 = BeautifulSoup(response1.content, 'html.parser')
        try:
            body1 = soup1.find("div", attrs={"class": "mediaQuestion bg-success"}).find("p").get_text()
        except:
            body1 = body.find("div", { "class" : "col-lg-12 text-align-right" }).get_text()

        try:
            date = soup1.find("div", attrs={"class": "media response"}).\
                find("div", attrs={"class": "media-body"}).\
                find("p" , attrs={"class": "text-left"}).\
                get_text().split(" ")[-2]
        except:
            date = ""

        try:
            tags = " - ".join([tag.get_text() for tag in soup1.\
                               find_all("a", attrs={"class": "btn btn-info tags"})])
        except Exception as e:
            print(e)
            tags = ""

        df.loc[len(df.index)] = [letters_ar_to_fa(case_title),
                                  case_address, body1, letters_ar_to_fa(tags), date]
    print("\nPage" , i , "Parsed and added")


df.to_excel("Dadrah.xlsx", sheet_name='Questions', index= False)
