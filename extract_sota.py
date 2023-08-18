import json
import argparse
import requests

from bs4 import BeautifulSoup

URL_BASE = 'https://paperswithcode.com'
SOTA_PATHNAME = '/sota'
DEBUG = False


def gen_url(pathname):
    if DEBUG: print(pathname)
    return URL_BASE + pathname


def extract_tileset(tileset):
    hrefs = [a_el['href'] for a_el in tileset.find_all('a')]
    names = [a_el.text.strip() for a_el in tileset.find_all('h1')]
    return {name:href for name, href in zip(names, hrefs)}


def get_soup(path):
    response = requests.get(path)
    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    
    print('Failed to retrieve the page. Status code:', response.status_code)
    raise Exception('Failed to extract sotas')


def get_tree(path, root=True):
    header_type = 'h4' if root else 'h2'
    soup = get_soup(path)

    subcat_names = [div.text.strip() for div in soup.find_all(header_type)]
    subcat_tilesets = soup.find_all('div', class_='infinite-item')

    subcat_pathnames = []
    for idx, div in enumerate(soup.find_all('div', class_='sota-all-tasks')):
        a_element = div.find('a')

        if a_element == None:
            subcat_pathnames.append(extract_tileset(subcat_tilesets[idx]))
            continue
        subcat_pathnames.append(a_element['href'])

    sotas = {
        name:pathname
        for name, pathname in zip(subcat_names, subcat_pathnames)
    }
    
    return sotas


def get_tasks_all(cats):
    return {
        name:get_tree(gen_url(pathname), root=False)
        for name, pathname in cats.items()
    }


def get_subtasks(path):
    soup = get_soup(path)
    tilesets = soup.find_all('div', class_='infinite-item')

    tree = {}
    for tileset in tilesets:
        tree.update(extract_tileset(tileset))
    return tree


def get_subtasks_all(tree):
    for _, tasks in tree.items():
        for task_name, href in tasks.items():
            if type(href) != str:
                continue
            tasks[task_name] = get_subtasks(gen_url(href))
    return tree


def parse_args():
    parser = argparse.ArgumentParser(description="Example script with a debug flag.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    return parser.parse_args()


def main():
    args = parse_args()

    global DEBUG
    DEBUG = args.debug

    tree = get_tree(gen_url(SOTA_PATHNAME))
    tree = get_tasks_all(tree)
    tree = get_subtasks_all(tree)

    with open('tree.json', 'w') as f:
        json.dump(tree, f)


if __name__ == '__main__':
    main()
