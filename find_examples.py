import copy

import requests
import bs4
from markdownify import markdownify


def find_section_examples(soup: bs4.BeautifulSoup):

    sections: list[bs4.element.Tag] = soup.find_all('section')
    name_conflicts = []

    for section_idx, section in enumerate(sections):
        childs: list[bs4.element.Tag] = [
            child for child in section.children if child != '\n'
        ]

        if childs[0].name != 'h4' or 'id' not in childs[0].attrs:
            continue

        # find the <div class='example'> blocks, and prepend a "> " to each string
        # to represent a quote block
        for child_idx, child in enumerate(childs):
            if isinstance(child, bs4.element.Tag) and \
                'class' in child.attrs and \
                'example' in child.attrs['class']:
                    for ch_idx, ch in enumerate(child):
                        if isinstance(ch, bs4.element.NavigableString):
                            new_ch = ch.replace("\n", "> ")
                            if new_ch[0] != '>':
                                child.contents[ch_idx].replace_with(f'> {new_ch}')
                            else:
                                child.contents[ch_idx].replace_with(f'{new_ch}')
                        if ch_idx == len(child) - 1:
                            child.contents[ch_idx].replace_with(f'{child.contents[ch_idx]}\n')
                    # add a new line to end of quotation block
                    placeholder = bs4.element.NavigableString(">")
                    childs[child_idx].contents = child.contents + [placeholder]
        sections[section_idx].contents = childs

    for section in sections:
        childs: list[bs4.element.Tag] = [
            child for child in section.children if child != '\n'
        ]

        if childs[0].name != 'h4' or 'id' not in childs[0].attrs:
            continue

        fname = childs[0].attrs['id']

        section_raw: str = section.encode_contents().decode()
        section_md: str = markdownify(section_raw)

        if fname in name_conflicts:
            fname = f'{fname}_1'

        with open(f'./data/{fname}.md', 'w') as f:
            f.write(section_md)

        name_conflicts.append(fname)

def main():
    URL = 'https://sakubi.neocities.org/'
    j = requests.get(URL)
    j.encoding = 'utf-8'
    soup = bs4.BeautifulSoup(j.text, "html.parser")
    find_section_examples(soup)

if __name__ == '__main__':
    main()
