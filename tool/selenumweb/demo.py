from selenium import webdriver
import lxml.html
import re
wd = webdriver.Edge()
url = "https://www.baidu.com/s?wd=Atri"
class ServiceConfige():
    def search(self,url):
        wd.get(url)
        html_source = wd.page_source

        html = lxml.html.fromstring(html_source)
        # 获取标签下所有文本
        print(html)
        items = html.xpath("//div[@id='y_prodsingle']//text()")
        # 正则 匹配以下内容 \s+ 首空格 \s+$ 尾空格 \n 换行
        pattern = re.compile("^\s+|\s+$|\n")
        
        clause_text = ""
        for item in items:
            # 将匹配到的内容用空替换，即去除匹配的内容，只留下文本
            line = re.sub(pattern, "", item)
            if len(line) > 0:
                clause_text += line + "\n"
            #
        #
        print(clause_text)
if __name__ == "__main__":
    sc = ServiceConfige()
    sc.search(url)