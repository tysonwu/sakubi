import requests
import bs4
from markdownify import markdownify


def find_sections(soup: bs4.BeautifulSoup):

    name_conflicts = []

    sections: list[bs4.element.Tag] = soup.find_all('section')
    for idx, section in enumerate(sections):
        title_element: bs4.element.Tag = [
            child for child in section.children if child != '\n'
        ][0]

        if title_element.attrs.get('id') == 'theend':
            fname = 'theend'
        else:
            if 'id' in title_element.attrs:
                fname = title_element['id']
            else:
                fname = title_element.string

        fname = '_'.join(fname.lower().split())
        fname = fname.replace('!', '')
        fname = fname.replace('\"', '')
        fname = fname.replace('\'', '')
        # fname = f'{str(idx).zfill(2)}_{fname}'

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
    find_sections(soup)

if __name__ == '__main__':
    main()
