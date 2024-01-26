import wikipediaapi

class WikipediaSummaryTool:
    def __init__(self, args):
        self.description = "Wikipedia Summary Tool: Fetches the summary of a Wikipedia page, takes language and title as input, and outputs the first 60 characters of the page summary."
        self.jsonload = """
        {
            "language": "The language of the page content (e.g., 'en' for English)",
            "title": "The title of the Wikipedia page"
        }
        """
    def description(self):
        return self.description
    def jsonload(self):
        return self.jsonload
    def jsonrun(self, json):
        language = json['language']
        title = json['title']
        return WikipediaSummaryTool.run(language, title)
    @staticmethod
    def run(language, title):
        wiki = wikipediaapi.Wikipedia(
            user_agent='MyProjectName (merlin@example.com)',
            language=language,
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
        lpage = wiki.page(title, language)
        summary = "\n".join(lpage.summary.split('\n')[:1]) if lpage.exists() else "Page does not exist."
        return summary
if __name__ == "__main__":
    # Example usage
    tool = WikipediaSummaryTool(None)  # Since we don't use 'args' in __init__, we can pass None
    json_input = {
        "language": "en",
        "title": "sakura"
    }
    result = tool.jsonrun(json_input)
    print(result)  # Outputs the first 60 characters of the Wikipedia page summary
