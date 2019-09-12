# Список женщин-режиссеров

За основу был взят [List of female film and television directors](https://en.wikipedia.org/wiki/List_of_female_film_and_television_directors) c Wikipedia. В нём на момент парсинга значился 991 человек: полное имя и ссылка на wiki-статью. Наивная попытка парсинга кортежей вида <Имя, Фамилия, ссылка> показала, что многие интуитивные предположения л полных именах европейских режиссеров неверны:

1) Требуется учитывать символы всех европейских языков: Agnès Varda, Jasmila Žbanić и тд
2) Не все "фамилии" начинаю с большой буквы: Haifaa al-Mansour и тд
3) Некоторые полные имена состоят из трех слов: Ajita Suchitra Veera, Margarethe von Trotta и тд. Или даже из четырех: Daisy von Scherler Mayer. Больше не попадалось :)

Для учета этих условий использовали следующие регулярные выражения:
```
# accepts over 70 European characters
name_regexp  = fr"[-A-z\u00c0-\u017e]+"
title_regexp = fr"^(\s*{name_regexp}){{2,4}}$"
```

Помимо прочего в [финальные списки режииссеров](https://github.com/GimmeDanger/cinema-studies/tree/master/data/director_lists/wiki) были добавлены латинизированные версии их полных имен (Pedro Almodóvar -> Pedro Almodovar), поскольку рассматриваемые англоязычные СМИ зачастую используют именно такую форму в своих текстах.

На Wikipedia не оказалось "чисто мужского" списка аналогичного рассмотренному выше "женскому". Зато был [List of film and television directors](https://en.wikipedia.org/wiki/List_of_film_and_television_directors) -- список, так сказать, "настоящих" режиссеров, в котором были перечисленны и женщины, и мужчины при подавляющем большинстве последних. На его основе был составлен список "чисто мужской" список.
