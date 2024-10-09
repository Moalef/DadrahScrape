import pandas as pd
from khayyam import JalaliDate
import matplotlib.pyplot as plt



df = pd.read_excel("Dadrah.xlsx")


def double_digit_str_maker(i: int):
    if i < 10:
        return "0" + str(i)
    else:
        return str(i)


def greg_date (df):
    greg_date_list = []
    greg_date_YearMonth_list = []
    for date in df['Date']:
        try:
            greg_date = JalaliDate(*(date.split("/"))).todate()
            greg_date_YearMonth = str(greg_date.year) + "/" + double_digit_str_maker(greg_date.month)
        except Exception as e:
            print(e)
            greg_date = None
            greg_date_YearMonth = None

        greg_date_list.append(greg_date)
        greg_date_YearMonth_list.append(greg_date_YearMonth)

    df['Date_Greg'] = greg_date_list
    df['Date_Greg_YM'] = greg_date_YearMonth_list



def barChart_dates(df):
    xy = df['Date_Greg_YM'].value_counts().sort_index()
    x = []
    for y in range (int(xy.index[1][:4]), int(xy.index[-1][:4])+1):
        for m in range(1, 13):
            x.append(str(y) + "/" + double_digit_str_maker(m))

    h = [xy[date] if date in xy.index else 0 for date in x]
    
    def addlabels(x,y):
        for i in range(len(x)):
            if h[i]> 1:
                plt.text(i, h[i]+1, h[i], ha = 'center')
            else:
                plt.text(i, h[i]+1, "", ha = 'center')

    plt.bar(x, h)
    addlabels(x, h)
    plt.xlabel("Year/Month")
    plt.ylabel("Number of Questions")
    plt.title("Monthly Number of Relevant Questions")
    plt.xticks(rotation = 90)
    plt.show()
    

def stacked_chart(df):
    df_tags_dates = pd.DataFrame(columns=['Tag' , 'Date_YM'])
    for ind in df.index:
        try:
            for tag in df.at[ind, 'Tags'].split("-"):
                df_tags_dates.loc[len(df_tags_dates.index)] = [tag.strip() , df.at[ind, 'Date_Greg_YM']]
        except:
            pass

    xy = df['Date_Greg_YM'].value_counts().sort_index()
    x = []
    for y in range (int(xy.index[1][:4]), int(xy.index[-1][:4])+1):
        for m in range(1, 13):
            x.append(str(y) + "/" + double_digit_str_maker(m))

    y1, y2, y3, y4, y5, y6, y7, y8, y9, y10 = ([] for i in range(10))
    x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = (df_tags_dates['Tag'].value_counts().index[i] for i in range(10))
    
    for date_ym in x:
        y1.append(len(df_tags_dates[(df_tags_dates['Date_YM'] == date_ym) & (df_tags_dates['Tag'] == x1)]))
        y2.append(len(df_tags_dates[(df_tags_dates['Date_YM'] == date_ym) & (df_tags_dates['Tag'] == x2)]))
        y3.append(len(df_tags_dates[(df_tags_dates['Date_YM'] == date_ym) & (df_tags_dates['Tag'] == x3)]))
        y4.append(len(df_tags_dates[(df_tags_dates['Date_YM'] == date_ym) & (df_tags_dates['Tag'] == x4)]))
        y5.append(len(df_tags_dates[(df_tags_dates['Date_YM'] == date_ym) & (df_tags_dates['Tag'] == x5)]))
        y6.append(len(df_tags_dates[(df_tags_dates['Date_YM'] == date_ym) & (df_tags_dates['Tag'] == x6)]))
        y7.append(len(df_tags_dates[(df_tags_dates['Date_YM'] == date_ym) & (df_tags_dates['Tag'] == x7)]))
        y8.append(len(df_tags_dates[(df_tags_dates['Date_YM'] == date_ym) & (df_tags_dates['Tag'] == x8)]))
        y9.append(len(df_tags_dates[(df_tags_dates['Date_YM'] == date_ym) & (df_tags_dates['Tag'] == x9)]))
        y10.append(len(df_tags_dates[(df_tags_dates['Date_YM'] == date_ym) & (df_tags_dates['Tag'] == x10)]))

    
    labels=('Sexual Assault', 'Rape', 'Sexual Assault Claim',
            'Forced Sexual Intercourse', 'Threat',
            'Evidence and Proof for Sexual Assault',
             'The Iranian Legal Medicine Organization', 'Sexual Harassment',
             'Abduction', 'Sodomy')
    
    plt.stackplot(x, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, labels= labels)
    
    plt.xlabel('Year/Month')
    plt.ylabel('Number of Subject Tags')
    plt.xticks(x, rotation= 'vertical')
    plt.title('Monthly Number of occurrence for each Subject')

    plt.legend()
    plt.show()

greg_date(df)
#barChart_dates(df)
stacked_chart(df)
