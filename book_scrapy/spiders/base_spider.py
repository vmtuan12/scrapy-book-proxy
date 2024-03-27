from typing import Any
from unidecode import unidecode
import scrapy
from book_scrapy.items import BookScrapyItem
from book_scrapy import constants
import re
import time

from scrapy.http import Request, Response

class BaseSpider(scrapy.Spider):

    number_regex = r"\d+(,\d+)*"
    year_regex = r"\d{4}"
    extra_space_regex = r" {2,}"

    domain_name = "https://www.goodreads.com"

    special_chars_set = {'+', '-', '=', '&', '|', '|', '>', 
                         '<', '!', '(', ')', '{', '}', '[', ']', 
                         '^', '"', '~', '*', '?', ':', '\\', '/', 
                         ',', '.', '#', '%', '$', '@', '!'}

    start_list = {
        "best_seller": "https://www.goodreads.com/list/tag/bestseller?fbclid=IwAR3ewJKEpxsTUq1Ut4aVKVUMFwKprmSnn0vgVJOVFJkRCgQ-JN6uqMvgmf4",
        "romance": "https://www.goodreads.com/list/tag/romance",
        "fiction": "https://www.goodreads.com/list/tag/fiction",
        "young_adult": "https://www.goodreads.com/list/tag/young-adult",
        "fantasy": "https://www.goodreads.com/list/tag/fantasy",
        "non_fiction": "https://www.goodreads.com/list/tag/non-fiction",
        "children": "https://www.goodreads.com/list/tag/children",
        "history": "https://www.goodreads.com/list/tag/history",
        "mystery": "https://www.goodreads.com/list/tag/mystery",
        "covers": "https://www.goodreads.com/list/tag/covers",
        "horror": "https://www.goodreads.com/list/tag/horror",
        "historical_fiction": "https://www.goodreads.com/list/tag/historical-fiction",
        "gay": "https://www.goodreads.com/list/tag/gay",
        "best": "https://www.goodreads.com/list/tag/best",
        "titles": "https://www.goodreads.com/list/tag/titles",
        "paranormal": "https://www.goodreads.com/list/tag/paranormal",
        "middle_grade": "https://www.goodreads.com/list/tag/middle-grade",
        "love": "https://www.goodreads.com/list/tag/love",
        "queer": "https://www.goodreads.com/list/tag/queer",
        "historical_romance": "https://www.goodreads.com/list/tag/historical-romance",
        "lgbt": "https://www.goodreads.com/list/tag/lgbt",
        "contemporary": "https://www.goodreads.com/list/tag/contemporary",
        "thriller": "https://www.goodreads.com/list/tag/thriller",
        "women": "https://www.goodreads.com/list/tag/women",
        "biography": "https://www.goodreads.com/list/tag/biography",
        "series": "https://www.goodreads.com/list/tag/series",
        "classics": "https://www.goodreads.com/list/tag/classics",
    }

    def start_requests(self):
        pass

    def parse_link(self, response):
        list_link = response.xpath(constants.GOODREADS_LIST_TITLE_LINK + '/@href').getall()
        for href in list_link:
            yield scrapy.Request(url=(self.domain_name + href), 
                                callback=self.parse_pages)
    
    def parse_pages(self, response):
        last_page = response.xpath(constants.GOODREADS_LAST_PAGE_CATE_XPATH + '/text()').get()
        if last_page == None:
            return
        
        last_page_num = int(last_page.strip())
        for page in range(1, last_page_num + 1):
            yield scrapy.Request(url=(response.url + f"?page={page}"), 
                                callback=self.parse_list_book)
    
    def parse_list_book(self, response):
        list_book = response.xpath(constants.GOODREADS_LIST_BOOK_XPATH + '/@href').getall()
        
        set_book = set(list_book)
        for book in set_book:
            yield scrapy.Request(url=(self.domain_name + book), 
                                callback=self.parse_book,
                                meta={"source": (response.url)})

    def parse_book(self, response: Response, **kwargs: Any):
        result = self.make_book(response=response)
        if len(result["author"]) > 0:
            yield result

    def _extract_title(self, response: Response) -> str | None:
        title = response.xpath(constants.GOODREADS_TITLE_XPATH + "//text()").get()
        if title == None:
            return ""
        return self._sub_space(title.strip())
        
    def _extract_author(self, response: Response) -> list[str]:
        authors = response.xpath(constants.GOODREADS_AUTHOR_XPATH + "//text()").getall()
        result = set()

        for author in authors:
            result.add(self._sub_space(author.strip()))

        return list(result)
    
    def _extract_description(self, response: Response) -> str | None:
        description = response.xpath(constants.GOODREADS_DESCRIPTION_XPATH + "//text()").getall()

        merged_description = ""
        for des in description:
            merged_description += (des.strip() + " ")
        merged_description = merged_description.strip()

        return self._sub_space(merged_description) if merged_description != "" else None
    
    def _extract_genres(self, response: Response) -> list[str] | None:
        genre_list = response.xpath(constants.GOODREADS_GENRE_LIST_XPATH + "//text()").getall()
        genres = []
        for genre in genre_list:
            genres.append(genre)

        return genres if len(genres) != 0 else None
    
    def _extract_series(self, response: Response) -> str | None:
        series = response.xpath(constants.GOODREADS_SERIES_XPATH + "//text()").get()
        if series == None:
            return None
        return self._sub_space(series.strip())
    
    def _extract_published_year(self, response: Response) -> int | None:
        year = response.xpath(constants.GOODREADS_BOOK_PUBLISH_YEAR + "//text()").get()
        if year == None:
            return None
        
        match = re.search(self.year_regex, year)
        return int(match.group()) if match != None else None
    
    def _extract_language(self, response: Response) -> str | None:
        # btn_expand_edition = self.find_element_xpath(xpath=constants.GOODREADS_BOOK_BTN_EXPAND_EDITION)
        # if btn_expand_edition != None:
        #     try:
        #         btn_expand_edition.click()
        #     except WebDriverException:
        #         pass

        # language_element = self.find_element_xpath(xpath=constants.GOODREADS_BOOK_LANGUAGE)
        # if language_element == None:
        #     return None
        
        # return language_element.get_attribute("innerText")
        return "English"

    def _extract_average_rating(self, response: Response) -> float | None:
        avg_rating_element = response.xpath(constants.GOODREADS_BOOK_RATING + "//text()").get()
        if avg_rating_element == None:
            return None
        
        return float(avg_rating_element)

    def _extract_review_counts(self, response: Response) -> int | None:
        rating_count_element = response.xpath(constants.GOODREADS_BOOK_RATING_COUNT + "//text()").get()
        if rating_count_element == None:
            return None
        
        rating_count = self._find_number_within_text(text=rating_count_element)
        if rating_count == None:
            return None
        
        return rating_count

    def _extract_num_page(self, response: Response) -> int | None:
        num_page_line = response.xpath(constants.GOODREADS_BOOK_NUM_PAGE + "//text()").get()
        if num_page_line == None:
            return None
        
        return self._find_number_within_text(text=num_page_line)

    def _find_number_within_text(self, text: str) -> int | None:
        match = re.search(self.number_regex, text)
        return int(match.group().replace(',', '')) if match != None else None

    def _sub_space(self, text: str) -> str:
        result = re.sub(self.extra_space_regex, " ", text)
        return result

    def _generate_record_id(self, name):
        normalized_name = unidecode(name, "utf-8")
        result = ""

        for char in normalized_name:
            if 'A' <= char <= 'Z':
                result += chr(ord(char) + 32)
            elif char == ' ':
                if result[len(result) - 1] != '-':
                    result += '-'
            else:
                if char not in self.special_chars_set:
                    result += char
        
        return result
    
    def make_book(self, response: Response):
        book = BookScrapyItem()
        book["title"] = self._extract_title(response)
        book["author"] = self._extract_author(response)
        book["description"] = self._extract_description(response)
        book["pages"] = self._extract_num_page(response)
        book["publish_year"] = self._extract_published_year(response)
        book["language"] = self._extract_language(response)
        book["rating"] = self._extract_average_rating(response)
        book["genres"] = self._extract_genres(response)
        book["review_counts"] = self._extract_review_counts(response)

        series = self._extract_series(response)
        if series != None:
            book["title"] += f" ({series})"

        book["id"] = self._generate_record_id(book["title"])
        book["source"] = response.meta.get("source")

        return book