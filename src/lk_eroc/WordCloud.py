import os
import random
from functools import cached_property

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from utils import Log
from wordcloud import WordCloud as WordCloudInner

from lk_eroc.Company import Company

log = Log('build_word_cloud')

DIR_WORD_CLOUDS = os.path.join('data', 'word_clouds')
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


class WordCloud:
    MIN_COMPANIES_FOR_WORD_CLOUD = 100

    def __init__(self, company_list: list[Company], label: str):
        self.company_list = company_list
        self.label = label

    @cached_property
    def words(self):
        words_all = []
        for company in self.company_list:
            words = company.name.split()
            words = [clean_word(w) for w in words]
            words_all.extend(words)
        log.debug(f'Found {len(words_all):,} words.')
        return words_all

    def write(self) -> str:
        text = " ".join(self.words)

        mask = np.array(Image.open(LK_PNG_PATH))

        wc = WordCloudInner(
            background_color="white",
            repeat=True,
            mask=mask,
            width=2000,
            height=3000,
        )
        wc.generate(text)
        wc.recolor(color_func=lk_color_func)

        plt.figure()
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.gcf().set_size_inches(4, 6)

        if not os.path.exists(DIR_WORD_CLOUDS):
            os.makedirs(DIR_WORD_CLOUDS)
        image_path = os.path.join(
            DIR_WORD_CLOUDS, f"word_cloud_{self.label}.png"
        )
        plt.savefig(image_path, dpi=150, bbox_inches='tight')
        log.info(f"✅ Wrote word cloud to {image_path}.")
        return image_path
