from urllib.request import urlopen
import codecs

url = "https://zhuanlan.zhihu.com/p/174666017"
resp = urlopen(url)

print(resp.read().decode("utf-8"))