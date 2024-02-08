# EVAagiTool 集成开发范式

## 结构事例
```python
class Tool(args):
    def __init__(self,args):
        self.description = "<Tool name> the function of this tool, its input and its output"
        self.jsonloadF = """
        {
            "args1": "what args1 should be..."
            "atgs2": "what args2 should be..."
            ...
            "argsN": "what argsN should be..."
        }
        """
    def description(self):
        return self.description
    def jsonload(self):
        return self.jsonloadF
    def jsonrun(self,json):
        args1 = json['args1']
        args2 = json['args2']
        return Tool.run(args)
    @staticmethod
    def run(args):
        # just DIY the function for what you want
        return output
```
==在函数进行调用的时候会输入== Tool.jsonrun(json)其中json的形式与上述的jsonload的形式一致
## 注意事项
* 请写清楚api的输入输出的要求(What AI should know before using this api and would know after using this api)
* 一个文件只能对应一个方法，一个类
* 尽量写一些基础的任务(寻找文件，读写文件，搜索芝士，看B站💦，发邮件等等)
* 高级的任务尽量写成脚本的形式，以api的形式调用
