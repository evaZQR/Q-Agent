import requests, re

url = 'https://www.baidu.com/s'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',}
r = re.compile('<h3[\s\S]*?<a[^>]*?href[^>]*?"(.*?)"[^>]*?>(.*?)</a>')

def baidu_search(keyword):
    params = {'wd': keyword, 'pn': 0, 'ie': 'utf-8'}
    try:
        while 1:
            for i in r.findall(requests.get(url, params, headers = headers).content):
                yield (re.compile('<.*?>').sub('', i[1]).decode('utf8'), i[0])
            params['pn'] += 10
    except GeneratorExit:
        pass
    except:
        while 1: yield ('', '')

for i, result in enumerate(baidu_search(u'知乎')):
    if 30 < i: break
    print('%s: %s'%result)