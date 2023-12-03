import os
import random

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from utils import Log, TSVFile
from wordcloud import WordCloud

from lk_eroc import Company
from workflows.aggregate import ALL_PATH

log = Log('build_word_cloud')

WORD_CLOUD_PATH = os.path.join("data", "word_cloud.png")
LK_PNG_PATH = os.path.join("data", "lk.png")
LK_COLOR_LIST = [
    '#ffbe29',
    '#8d153a',
    '#eb7400',
    '#00534e',
]


def clean_word(word: str) -> str:
    return word.strip().lower()


def lk_color_func(**_):
    n = len(LK_COLOR_LIST)
    i = random.randint(0, n - 1)
    return LK_COLOR_LIST[i]


def get_words():
    company_list = [Company(**d) for d in TSVFile(ALL_PATH).read()]
    words_all = []
    for company in company_list:
        words = company.name.split()
        words = [clean_word(w) for w in words]
        words_all.extend(words)
    log.debug(f'Found {len(words_all):,} words.')
    return words_all


def build_word_cloud():
    words = get_words()
    text = " ".join(words)

    mask = np.array(Image.open(LK_PNG_PATH))

    wc = WordCloud(
        background_color="white",
        repeat=True,
        mask=mask,
        width=200,
        height=300,
    )
    wc.generate(text)
    wc.recolor(color_func=lk_color_func)

    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.gcf().set_size_inches(8, 12)

    plt.savefig(WORD_CLOUD_PATH, dpi=300, bbox_inches='tight')
    log.info(f"✅ Wrote word cloud to {WORD_CLOUD_PATH}.")


if __name__ == '__main__':
    build_word_cloud()
