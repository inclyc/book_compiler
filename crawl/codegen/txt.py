import os


def generate(out, titles, contents):
    if not os.path.exists(os.path.dirname(out)):
        os.makedirs(os.path.dirname(out))
    with open(out, 'w') as f:
        for title in titles:
            f.write(title)
            f.write('\n')
            f.write(contents[title])
