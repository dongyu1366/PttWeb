from crawler.handler.ptt_crawler import BeautyCrawler


def get_all_beauty_article():
    print('================================')
    print('Start to Fetch all Beauty articles')
    print('================================')

    spider = BeautyCrawler()
    spider.get_all()

    print('Fetch task complete!')


def update_beauty_article():
    print('================================')
    print('Start to Update Beauty articles')
    print('================================')

    spider = BeautyCrawler()
    spider.update(pages=10)

    print('Update task complete!')
