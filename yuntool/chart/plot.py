# coding=utf-8
import sys
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt


def draw_curve(
        x, y, xlabel=[], ylabel=[], title=[], dpi=100, y_num=None,
        xticks=[], yticks=[], draw_one=False, label=[]):
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
    tmp = 0
    y_min = sys.maxsize
    y_max = -1 * sys.maxsize
    for sub_y in y:
        if not draw_one:
            ax = plt.subplot(num, 1, i)
        else:
            ax = plt.subplot(111)
        r_x = np.arange(0, len(sub_y), 1)
        sub_y = np.arange(0, len(sub_y), 1) * 0.0 + sub_y
        if label:
            ax.plot(r_x, sub_y, label=label[i - 1])
        else:
            ax.plot(r_x, sub_y)
        plt.xlabel(xlabel[i - 1])
        plt.ylabel(ylabel[i - 1])
        if xticks:
            plt.xticks(r_x, xticks[i - 1])
        if yticks:
            plt.yticks(sub_y, yticks[i - 1])
        if not draw_one:
            y_min = sub_y.min()
            y_max = sub_y.max()
        else:
            tmp = y_min
            y_min = sub_y.min()
            if tmp < y_min:
                y_min = tmp

            tmp = y_max
            y_max = sub_y.max()
            if tmp > y_max:
                y_max = tmp
        diff = y_max - y_min
        plt.ylim(y_min - diff, y_max + diff)
        plt.title(title[i - 1])
        plt.grid(True)
        i += 1
    plt.legend(bbox_to_anchor=(0.1, 1), loc=2, borderaxespad=0)
    output = BytesIO()
    plt.savefig(output, dpi=dpi)
    output.seek(0)
    plt.clf()
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
        ['2016-06-28', '2016-06-29', '2016-06-30'],
        ['2016-06-28', '2016-06-29', '2016-06-30']]
    y = [
        [270, 200, 288, 270, 200, 288, 270, 200, 288, 270, 200, 288],
        [2482, 1890, 2359, 2482, 1890, 2359, 2482, 1890, 2359, 2482, 1890, 2359]]
    # picture = draw_curve(
    #     x, y, xlabel=['date', 'date'], ylabel=['num', 'num1'])
    picture = draw_curve(
        x, y,
        # xticklabels=[
        #     ['a', 'b', 'c', 'e', 'f', 'j', 'a', 'b', 'c', 'e', 'f', 'j'],
        #     ['a', 'b', 'c', 'e', 'f', 'j', 'a', 'b', 'c', 'e', 'f', 'j']],
        xlabel=['date', 'date'], ylabel=['num', 'num1'], draw_one=True,
        label=['1', '2'])
    print(picture)
