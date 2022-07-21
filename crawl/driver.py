import re
import requests
import extractor
import codegen.tex
import codegen.txt
import os
from tqdm import tqdm
import concurrent.futures
from loguru import logger

HEADERS = {
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'}

SITE_ADDR = 'https://w.linovelib.com/'
OUT = os.path.join('..', 'generated')


def chapter_job(url):
    doc = requests.get(url, headers=HEADERS).text
    return extractor.content(doc)


def main():

    logger.info("Fetching index")

    doc = requests.get(
        '{}/novel/3005/catalog'.format(SITE_ADDR), headers=HEADERS).text
    index = extractor.index(doc)
    # 过滤广告等链接，只留下小说正文链接
    index = list(filter(lambda x: re.match('/novel', x[0]), index))
    titles = [title for _, title in index]
    contents = {}
    logger.info("Downloading {} chapters".format(len(index)))
    with tqdm(total=len(index)) as pbar:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {executor.submit(chapter_job, SITE_ADDR + url): title
                       for url, title in index}
            for future in concurrent.futures.as_completed(futures):
                title = futures[future]
                contents[title] = future.result()
                pbar.update(1)

    codegen.tex.generate(os.path.join(OUT, 'tex'), titles, contents)
    codegen.txt.generate(os.path.join(OUT, 'main.txt'), titles, contents)


if __name__ == '__main__':
    main()
