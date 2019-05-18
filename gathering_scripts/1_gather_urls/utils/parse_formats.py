class VarietyParseFormat:
    name = "variety"
    host_name = f"https://{name}.com"
    categories = ["news", "reviews", "columns"]
    min_page_num = 1
    max_page_num = 100000 #inf
    def hay_page_URL(self, cat_name, page_num):
        return f"{self.host_name}/v/film/{cat_name}/page/{page_num}"
    def needle_URL_regexp(self, cat_name):
        return f"^{self.host_name}/\d*/film/{cat_name}"

class DeadlineParseFormat:
    name = "deadline"
    host_name = f"https://{name}.com"
    categories = ["film"]
    min_page_num = 1
    max_page_num = 100000 #inf
    def hay_page_URL(self, cat_name, page_num):
        return f"{self.host_name}/v/{cat_name}/page/{page_num}"
    def needle_URL_regexp(self, cat_name=''):
        return f"^{self.host_name}/\d*/\d*/[-\w]*"

class FilmcommentParseFormat:
    name = "filmcomment"
    host_name = f"https://www.{name}.com"
    categories = ["blog"]
    min_page_num = 1
    max_page_num = 100000 #inf
    def hay_page_URL(self, cat_name, page_num):
        return f"{self.host_name}/{cat_name}/page/{page_num}/"
    def needle_URL_regexp(self, cat_name):
        return f"^{self.host_name}/{cat_name}/[-\w]+/"

class HWReporterParseFormat:
    def __init__(self, searching_tag):
      self.searching_tag = searching_tag
    name = "hollywoodreporter"
    host_name = f"https://www.{name}.com"
    categories = ["news", "review"]
    min_page_num = 1
    max_page_num = 100000 #inf
    def hay_page_URL(self, cat_name, page_num):
        return f"{self.host_name}/search/{self.searching_tag}?page={page_num}&filters=type:{cat_name}%20tid:59"
    def needle_URL_regexp(self, cat_name=""):
        #something like: "/features/felicity-jones-rogue-one-reshoots-937569"
        return f"^/[\w]+/[-\w]+[\d]+"

#TODO:
#Entertainment Weekly ( https://ew.com/ )
#https://ew.com/search?q=woman%20director&page=5
