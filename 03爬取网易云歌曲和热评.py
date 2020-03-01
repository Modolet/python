import urllib.request
import json
import urllib.parse
import re


headers = {
        'authority': 'music.163.com',
        'method': 'GET',
        'path': '/',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,ja;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://music.163.com/',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': "?1",
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
            }

def _openurl(url):
    req = urllib.request.Request(url,headers = headers)
    return urllib.request.urlopen(req).read()

def get_hot_comments(name, id):
    data = {
            "params" : "Uz0NbpMMAOk4vRp2gLvG5Yh2DlZ6/uvtpt/DVXKPc/SM0DB97Fu3wza/3SI0L5cPY1qXlWtBo+nt3lMmoKVob5guqt5h+MnfSq0RTjvOQ0n+mCItYAxJPWnxreke4g9fmxKbIl6KQnAZEEmZzjabZ68qnPO5RXjKiM03cOgthtWLpp2+W15AIjdhc+qX9gEowJuAz6MoXr0ROgSWv9Ftb/Ho3WY2NpX0/wz69Ui4gTA=",
            "encSecKey" : "91d085848753d8baba456f865db459fd69a34481e31ba72c2e504a79530e55215e7496cb0386f503b8b949373f47d7e6ae68d94b613d7fa1cf71996b705aebec5376938e0b3212bc22fd286b505f3c9685a82bc56323162726d5019ef9d68ce926b5e107a6685c294e0dbefe6197d17ccd67d9ed2fcebcab489ede546ebf87af"
            }
    data = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request("https://music.163.com/weapi/v1/resource/comments/R_SO_4_" + str(id) + "?csrf_token=35cd1a47ac037d7a04276793833907f3", data=data, headers=headers)
    url = urllib.request.urlopen(req)
    res = url.read().decode("utf-8")
    res = json.loads(res)
    with open("res/" + name + ".txt","w") as f:
        for each in res['hotComments']:
            #f.writelines(each['content'])
            #f.writelines(' ')
            f.write(each['content'] + '\n\n')


def main():
    songlist = input("请输入歌单id：")
    songlist = "https://music.163.com/playlist?id=" + str(songlist)
    html = _openurl(songlist).decode("utf-8")
    with open("songlist.html","w") as f:
        f.write(html)
    req = r'<li><a href="/song\?id=(.+?)">(.+?)</a></li>'
    data = re.findall(req,html)
    for each in data:
        try:
            name = str(each[1])
            get_hot_comments(name,each[0])
            print(name,each[0],"热评爬取成功")
        except:
            print(name,"爬取失败（名称非法）")
    for each in data:
        try:
            name = str(each[1])
            songurl = "http://music.163.com/song/media/outer/url?id=" + each[0] + ".mp3"
            urllib.request.urlretrieve(songurl,"res/" + name + ".mp3")
            print(each[1],each[0],"下载成功")
        except:
            print(name,"爬取失败（名称非法）")

if __name__ == '__main__':
    main()
