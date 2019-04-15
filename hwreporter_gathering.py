from utils import parse_formats
from utils import parse_tools

tags = [
  "film",
  "director",
  "cameraman",
  "cinematographer",
  "photographer",
  "writer",
  "female%20director",
  "female%20cameraman",
  "female%20cinematographer",
  "female%20photographer",
  "female%20writer",
  "woman%20director",
  "woman%20cameraman",
  "woman%20cinematographer",
  "woman%20photographer",
  "woman%20writer"  
  ]

tags_name = [
  "film",
  "director",
  "cameraman",
  "cinematographer",
  "photographer",
  "writer",
  "female_director",
  "female_cameraman",
  "female_cinematographer",
  "female_photographer",
  "female_writer",
  "woman_director",
  "woman_cameraman",
  "woman_cinematographer",
  "woman_photographer",
  "woman_writer"  
  ]

def parse_for_tag(tag, tag_name):
  site_format = parse_formats.HWReporterParseFormat(searching_tag=tag)
  
  print(f"\nScript for '{site_format.host_name}' parsing.\n")
  print(f"Parsing for tag {tag_name} begins!")

  uid = 0
  delta_page = 150
  for min_page in range(site_format.min_page_num, site_format.max_page_num, delta_page):  
    urls = parse_tools.gather_site_pages(
      min_page_num=min_page, max_page_num=min(min_page+delta_page,site_format.max_page_num),
      categories=site_format.categories, needle_URL_regexp=site_format.needle_URL_regexp,
      hay_page_URL=site_format.hay_page_URL)

    dump_cond = False
    for cat_name in site_format.categories:
      if len(urls[cat_name]) != 0:
        dump_cond = True
        break;
    
    if dump_cond:
      uid = parse_tools.dump_parsed_data_as_csv(
        output_filename=f"{site_format.name}_{tag_name}_urls_records.csv",
        categories=site_format.categories, urls_by_categories=urls, uid_begin=uid)
    else:
      break
  print(f"Parsing for tag {tag_name} finishes!")
  
for index, tag in enumerate(tags):
  parse_for_tag(tag, tags_name[index])
