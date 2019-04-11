from utils import parse_formats
from utils import parse_tools

site_format = parse_formats.FilmcommentParseFormat()
print(f"\nScript for '{site_format.host_name}' parsing.\n")

#read category name to parse
#need this for easy parallel run
#for different categories
print("Insert category to parse:")
cat_name = input()

uid = 0
delta_page = 150

for min_page in range(site_format.min_page_num, site_format.max_page_num, delta_page):
  
  urls = parse_tools.gather_site_pages(min_page_num=min_page, max_page_num=min(min_page+delta_page,site_format.max_page_num),
                                       categories=[cat_name], needle_URL_regexp=site_format.needle_URL_regexp,
                                       hay_page_URL=site_format.hay_page_URL)

  uid = parse_tools.dump_parsed_data_as_csv(output_filename=f"{site_format.name}_{cat_name}_urls_records.csv",
                                            categories=[cat_name], urls_by_categories=urls, uid_begin=uid)

print("Parsing finished!")