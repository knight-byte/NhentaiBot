from NHentai import NHentai as NH


def homepage():
    nh = NH()
    main_c = []
    pages = 3
    for i in range(1, pages+1):
        HomePage = nh.get_pages(page=i)
        hp = HomePage.__dict__
        h = hp["doujins"]
        main_c.extend(h)
    return main_c


def search_q(query):
    nh = NH()
    main_c = []
    pages = 3
    for i in range(1, pages+1):
        search = nh.search(query=query, sort='popular', page=i)
        s_r = search.__dict__
        h = s_r["doujins"]
        main_c.extend(h)
    return main_c
