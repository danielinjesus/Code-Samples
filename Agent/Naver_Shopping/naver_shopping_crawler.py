import requests
def crawl(keyword):
    url="https://search.shopping.naver.com/ns/search?query=%EC%96%91%EB%A7%90&prevQuery=%EC%88%A8%EC%85%94%EB%B0%94%EC%9A%94"
    data=requests.get(url)
    print(data.status_code, url)
    return data.content