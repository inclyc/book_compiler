from bs4 import BeautifulSoup
from typing import List, Tuple


def content(doc: str) -> str:
	ret = ""
	soup = BeautifulSoup(doc, 'html.parser').find(id='acontent')

	for p in soup.find_all('p'):  # type: ignore
		if isinstance(p.next, str):
			ret += p.next
			ret = ret.replace('\r', '')
			ret += '\n\n'  # Latex 换行需要两个 \n

	return ret


def index(doc: str) -> List[Tuple[str, str]]:
    soup = BeautifulSoup(doc, 'html.parser')
    return [(x.a.attrs['href'], x.a.next.next) for x in soup.find_all('li', class_='chapter-li jsChapter')]
