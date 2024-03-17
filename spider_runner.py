from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from book_scrapy.spiders import (best_seller_spider, best_spider, biography_spider, children_spider, classics_spider,
                                 contemporary_spider, covers_spider, fantasy_spider, fiction_spider, gay_spider,
                                 historical_fiction_spider, historical_romance_spider, history_spider, horror_spider,
                                 lgbt_spider, love_spider, middle_grade_spider, mystery_spider, non_fiction_spider,
                                 paranormal_spider, queer_spider, romance_spider, series_spider, thriller_spider,
                                 titles_spider, women_spider, young_adult_spider)
import os

settings = get_project_settings()
process = CrawlerProcess(settings)
# process.crawl(best_seller_spider.BestSellerSpider)
# process.crawl(best_spider.BestSpider)
# process.crawl(biography_spider.BiographySpider)
process.crawl(children_spider.ChildrenSpider)
process.crawl(classics_spider.ClassicsSpider)
process.crawl(contemporary_spider.ContemporarySpider)
process.crawl(fantasy_spider.FantasySpider)
process.crawl(fiction_spider.FictionSpider)
process.crawl(horror_spider.HorrorSpider)
process.crawl(romance_spider.RomanceSpider)
process.crawl(thriller_spider.ThrillerSpider)
process.crawl(mystery_spider.MysterySpider)
process.crawl(history_spider.HistorySpider)
# process.crawl(covers_spider.CoversSpider)
# process.crawl(gay_spider.GaySpider)
# process.crawl(historical_fiction_spider.HistoricalFictionSpider)
# process.crawl(historical_romance_spider.HistoricalRomanceSpider)
# process.crawl(lgbt_spider.LgbtSpider)
# process.crawl(love_spider.LoveSpider)
# process.crawl(middle_grade_spider.MiddleGradeSpider)
# process.crawl(non_fiction_spider.NonFictionSpider)
# process.crawl(paranormal_spider.ParanormalSpider)
# process.crawl(queer_spider.QueerSpider)
# process.crawl(series_spider.SeriesSpider)
# process.crawl(titles_spider.TitlesSpider)
# process.crawl(women_spider.WomenSpider)
# process.crawl(young_adult_spider.YoungAdultSpider)

process.start()