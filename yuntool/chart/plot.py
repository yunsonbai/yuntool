# coding=utf-8
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt


def draw_curve(
        x, y, xlabel=[], ylabel=[], title=[], dpi=100, y_num=None,
        xticklabels=[], yticklabels=[]):
    '''
    parameter:
        x: X axis data [[int], [int]]
        y: Y axis data [[int/float], [int/float]]
        xlabel: xlabel [[], []]
        ylabel: ylabel [[], []]
        title:  title [[], []]
        dpi: dpi defualt 100
    '''
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
        sub_y = np.arange(0, len(sub_y), 1) * 0.0 + sub_y
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
        if xticklabels:
            # xticklabels = [0] + xticklabels
            ax.set_xticklabels(xticklabels[i - 1], rotation=15)
        if yticklabels:
            ax.set_yticklabels(yticklabels[i - 1], rotation=15)
        i += 1
    output = BytesIO()
    plt.savefig(output, dpi=dpi)
    output.seek(0)
    return output


def draw_bar(
        x, y, xlabel=[], ylabel=[], title=[],
        dpi=500, y_num=None, merge=False):
    '''
    parameter:
        x: X axis data [[], []]
        y: Y axis data [[], []]
        xlabel: xlabel [[], []]
        ylabel: ylabel [[], []]
        title:  title [[], []]
        dpi: dpi defualt 100
        merge: Combination chart  default False
    '''
    width = 0.35
    if not y_num:
        num = len(y)
    else:
        num = y_num
    if not title:
        title = range(num)
    i = 1
    color = ['b', 'r', 'y']
    color_i = 0
    len_color = len(color)
    for sub_y in y:
        r_x = np.arange(0, len(sub_y), 1)
        sub_y = np.arange(0, len(sub_y), 1) * 0 + sub_y
        if merge:
            if i == 1:
                fig, ax = plt.subplots()
                chart = []
                cutline = []
            chart.append(ax.bar(
                r_x + (i - 1) * width, sub_y, width, color=color[color_i]))
            cutline.append(title[i - 1])
        else:
            ax = plt.subplot(num, 1, i)
            ax.bar(r_x, sub_y, width, color=color[color_i])
        plt.ylabel(ylabel[i - 1])
        ax.set_title(title[i - 1])
        if i == num:
            plt.xlabel(xlabel[i - 1])
        ax.set_xticklabels(x[i - 1], rotation=15)
        i += 1
        color_i += 1
        if color_i == len_color:
            color_i = 0
    if merge:
        ax.legend(chart, cutline)
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
    # picture = draw_curve(
    #     x, y, xlabel=['date', 'date'], ylabel=['num', 'num1'])
    picture = draw_bar(
        x, y, xlabel=['date', 'date'], ylabel=['num', 'num1'],
        merge=True)
    print(picture)
