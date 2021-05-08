from dataclasses import replace
import logging
from typing import final
from NHentai import NHentai as NH
import re


def homepage():
    nh = NH()
    main_c = []
    pages = 2
    for i in range(1, pages+1):
        HomePage = nh.get_pages(page=i)
        hp = HomePage.__dict__
        h = hp["doujins"]
        main_c.extend(h)
    return main_c


def search_q(query):
    nh = NH()
    main_c = []
    pages = 2
    rf = re.findall(r"^[0-9]+$", string=query)
    if len(rf) > 0:
        return main_c
    for i in range(1, pages+1):
        search = nh.search(query=query, sort='popular', page=i)
        s_r = search.__dict__
        h = s_r["doujins"]
        main_c.extend(h)
    return main_c


def id_search_q(query):
    nh = NH()
    rf = re.findall(r"^(#)?([0-9]+)$", string=query)
    id = {}
    if len(rf) > 0:
        try:
            query = query.replace('#', '')
            id = nh._get_doujin(id=query).__dict__
            # id store dict obeject with keys: id, title, secondary title, tags(list), artist(list), lang(list), categories(list)
            #                                 characters(list), parodies(list), groups(list), images(list), total page
        except AttributeError:
            logging.error("No result found")
        return id
    else:
        return id


print(len(id_search_q("999")["images"]))
