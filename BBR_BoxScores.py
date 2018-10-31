from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
import requests

def get_soup(url):
	try:
		page_response = requests.get(url)
		if page_response.status_code == 200:
			content = page_response.content
			soup = BeautifulSoup(content, 'lxml')
			return soup
		else:
			print(page_response.status_code)
			# notify, try again
	except requests.Timeout as e:
		print("It is time to timeout")
		print(str(e))
	except:
		print('error') # other exception
		raise

def get_urls():
	urls = []
	url = 'https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=1947&year_max=2018&is_range=N&game_num_type=team&is_overtime=N&order_by=diff_off_rtg&offset=0'
	for i in range(0, 1000000, 100):
		url = 'https://www.basketball-reference.com/play-index/tgl_finder.cgi?request=1&match=game&lg_id=NBA&is_playoffs=N&team_seed_cmp=eq&opp_seed_cmp=eq&year_min=1947&year_max=2018&is_range=N&game_num_type=team&is_overtime=N&order_by=diff_off_rtg&offset=' + str(i)
		urls.append(url)
	return urls

urls = get_urls()
print(len(urls))


soup_df = pd.DataFrame()


count = 1
for url in urls:
	try:
		soup = get_soup(url)
		soup_df1 = pd.read_html(str(soup.find('table')))[0]
		soup_df = soup_df.append(soup_df1)
		print('page: ' + str(count))
		count += 1
	except ValueError as e:
		print(e)
		#raise
		break
	except:
		print("Oops something went wrong")
		raise
		break

df = soup_df.rename(columns={'Unnamed: 3_level_1': 'Home/Away'})
df.columns = df.columns.droplevel()
a = df.iloc[:,0:6]
b = df.iloc[:,7:12]
c = df.iloc[:,13:18]
d = df.iloc[:,19:24]
df = pd.concat([a,b,c,d], axis=1, keys=['Infomation','Team', 'Opponent', 'Differences'])
df[('Infomation','Home/Away')] = (df.loc[:,('Infomation','Home/Away')] == '@').astype(int)
df = df[df[('Infomation','Rk')] != 'Rk']


df.to_csv('df_Advanced.csv', sep = ',')
print("All done your beautiful table is ready Sir, also Tanay is a bum")