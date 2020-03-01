import urllib
import re
import urllib.request

def main():
    url="http://top.baidu.com/"
    req = urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36")
    html = urllib.request.urlopen(req)
    html = html.read().decode("gbk")
    zz = r'<a target="_blank" title="(.+?)" data="1|1" class="list-title"'
    res = re.findall(zz,html)
    for echo in res:
        print(echo)
if __name__ == '__main__':
    main()
