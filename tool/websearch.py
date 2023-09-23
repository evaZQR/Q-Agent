# 集成了GoogleAPI 
# BingAPI
# baiduAPI
# DuckDuckGo Instant Answer API
class SearchEngine:
    def __init__(self, name, api_key):
        self.name = name
        self.api_key = api_key
        self.description = ""
        self.jsonload = """
        {
            "message": "something you want to search online"
        }
        """

    def search(self, query):
        raise NotImplementedError
    
if __name__ == "__main__":
    