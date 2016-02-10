import requests
import github3 as gh
import bs4

url = "https://github.com/orgs/bmlltech/dashboard"

response = requests.get(url)
soup = bs4.BeautifulSoup(response.content, "html.parser")

print(soup.find_all("span"))