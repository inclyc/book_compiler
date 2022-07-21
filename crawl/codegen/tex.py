import os
import concurrent.futures
import re
from loguru import logger

SECTIONS = 'sections'


def _tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    regex = re.compile('|'.join(re.escape(str(key))
                       for key in sorted(conv.keys(), key=lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)


def _chapter_file(title, content) -> str:
    return r"""\section{{{}}}
    {}
    """.format(title, _tex_escape(content))


def _chapter_input(title) -> str:
    return r'''\input{{{0}}}
    '''.format('{}/{}'.format(SECTIONS, title))


def _preamble() -> str:
    return r"""\documentclass{ctexart}
\title{伪圣女}
    """


def _document(titles) -> str:
    ret = r'\begin{document}'
    ret += '\n'
    ret += r'\maketitle'
    for title in titles:
        ret += _chapter_input(title)
    ret += '\n'
    ret += r'\end{document}'
    return ret


def generate(out, titles, contents):
    sections_out = os.path.join(out, SECTIONS)
    if not os.path.exists(sections_out):
        os.makedirs(sections_out)

    def chapter_files(title, content):
        with open(os.path.join(sections_out, title + '.tex'), 'w') as f:
            f.write(_chapter_file(title, content))

    logger.info("Generating tex sections")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(chapter_files, title, contents[title]): title
                   for title in contents}

        for future in concurrent.futures.as_completed(futures):
            future.result()

    logger.info("Generating main tex")

    with open(os.path.join(out, 'main.tex'), 'w') as f:
        f.write(_preamble() + _document(titles))

    logger.info("Done")
