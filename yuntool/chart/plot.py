# coding=utf-8
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt


def draw_curve(x, y, xlabel=[], ylabel=[], title=[], dpi=100, y_num=None):
    if not y_num:
        num = len(y)
    else:
        num = y_num
    if not title:
        title = range(num)
    i = 1
    for sub_y in y:
        ax = plt.subplot(num, 1, i)
        r_x = np.arange(0, len(sub_y), 1)
        sub_y = np.arange(0, len(sub_y), 1) * 0 + sub_y
        ax.plot(r_x, sub_y, 'b-')
        plt.xlabel(xlabel[i - 1])
        plt.ylabel(ylabel[i - 1])
        y_min = sub_y.min()
        y_max = sub_y.max()
        diff = y_max - y_min
        plt.ylim(y_min - diff, y_max + diff)
        plt.title(title[i - 1])
        plt.tight_layout(pad=0.1, h_pad=0, w_pad=0.2, rect=None)
        plt.grid(True)
        ax.set_xticklabels(x[i - 1], rotation=15)
        i += 1
    output = BytesIO()
    plt.savefig(output, dpi=dpi)
    output.seek(0)
    return output


if __name__ == '__main__':
    x = [
        ['2016-06-28', '2016-06-29', '2016-06-30',
         '2016-07-01', '2016-07-02', '2016-07-03', '2016-07-04'
         ],
        ['2016-06-28', '2016-06-29', '2016-06-30', '2016-07-01',
         '2016-07-02', '2016-07-03', '2016-07-04']]
    y = [
        [270, 279, 288, 273, 248, 232, 293],
        [2482, 1890, 2359, 7506, 14561, 14741, 16191]]
    picture = draw_curve(
        x, y, xlabel=['date', 'date'], ylabel=['num', 'num1'])
    print(picture)
