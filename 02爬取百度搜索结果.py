import gzip
import re
import urllib.request

def OpenUrl(url):
    url = urllib.request.Request(url)
    url.add_header(r'Accept' ,r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
    url.add_header(r'Accept-Encoding' ,r'gzip, deflate, br')
    url.add_header(r'Accept-Language' ,r'zh-CN,zh;q=0.9,zh-HK;q=0.8,ja;q=0.7')
    url.add_header(r'Connection' ,r'keep-alive')
    url.add_header(r'Host' ,r'www.baidu.com')
    url.add_header(r'Referer' ,r'https://www.baidu.com/s?wd=python&pn=30')
    url.add_header(r'Sec-Fetch-Mode' ,r'navigate')
    url.add_header(r'Sec-Fetch-Site' ,r'same-origin')
    url.add_header(r'Sec-Fetch-User' ,r'?1')
    url.add_header(r'Upgrade-Insecure-Requests' ,r'1')
    url.add_header(r'User-Agent' ,r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')
    return gzip.decompress(urllib.request.urlopen(url).read()) 

def main():
    originurl = "https://www.baidu.com/s?wd="
    keyword = input("请输入关键字:")
    keyword = urllib.request.quote(keyword)
    page    = input("请输入页数:")
    for i in range(1,int(page) + 1):
        url  = originurl + keyword + "&pn=" + str((i - 1) * 10)
        html = OpenUrl(url)
        html = html.decode("utf-8")
        with open(str(i) + ".html","w") as f:
            f.write(html)
        res = re.findall(r'{"title":"(.+?)"',html)
        res2 = re.findall(r"{'title':'(.+?)'",html)
        for each in res:
            print(each)


if __name__ == '__main__':
    main()
