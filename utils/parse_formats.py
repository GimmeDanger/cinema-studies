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

#TODO:
#The Hollywood Reporter ( https://www.hollywoodreporter.com/ )
#Entertainment Weekly ( https://ew.com/ )
#Film Comment ( https://www.filmcomment.com/ )
#BoxOffice ( https://www.boxofficepro.com )