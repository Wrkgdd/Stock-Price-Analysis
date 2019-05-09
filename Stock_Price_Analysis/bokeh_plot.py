from bokeh.transform import linear_cmap

import Data_Bokeh
from bokeh.plotting import figure, show, output_file
import pandas as pd
from bokeh.layouts import column
from pyti.bollinger_bands import upper_bollinger_band as bb_up
from pyti.bollinger_bands import lower_bollinger_band as bb_low
from pyti.bollinger_bands import middle_bollinger_band as bb_mid
from bokeh.layouts import layout
from bokeh.models import Toggle, BoxAnnotation, CustomJS
import holoviews as hv
import numpy as np
from bokeh.models import RangeTool
from bokeh.models import Band, ColumnDataSource


# グラフ化
def Plot_Data():
    output_file("Output_" + s.C_num + ".html")

    # 株価と平均移動線のプロット
    p1 = figure(width=800, height=400, x_axis_type='datetime', title="【{}】Stock Closing Price".format(s.C_num))
    x = pd.to_datetime(s.dfs_2['日付'])
    p1.line(x, s.dfs_2['終値'], color='lightblue', legend='{}'.format(s.C_num), line_width=1.5)
    y = s.dfs_2['終値']
    sma5 = s.dfs_2['終値'].rolling(5).mean()
    p1.line(x, sma5, color='tomato', legend='5日移動平均')
    sma25 = s.dfs_2['終値'].rolling(25).mean()
    p1.line(x, sma25, color='orange', legend='25日移動平均')
    sma75 = s.dfs_2['終値'].rolling(75).mean()
    p1.line(x, sma75, color='grey', legend='75日移動平均')

    # ボリンジャーバンドとシグマのプロット
    y1 = bb_up(s.dfs_2["終値"], 25)
    y2 = bb_low(s.dfs_2["終値"], 25)
    sigma_n = s.dfs_2['終値'].rolling(window=5).std(ddof=0)
    y3 = s.dfs_2['終値'] + sigma_n * 2
    y4 = s.dfs_2['終値'] - sigma_n * 2
    y5 = s.dfs_2['終値'] + sigma_n * 3
    y6 = s.dfs_2['終値'] - sigma_n * 3
    p1.line(x, y1, color='powderblue', line_dash="dotted", legend='ボリンジャー',
            line_width=5, line_alpha=0.3)
    p1.line(x, y2, color='powderblue', line_dash="dotted", legend='ボリンジャー',
            line_width=5, line_alpha=0.3)
    p1.line(x, y3, color='lawngreen', legend='σ2',
            line_width=2, line_alpha=0.2)
    p1.line(x, y4, color='lawngreen', legend='σ2',
            line_width=2, line_alpha=0.2)
    p1.line(x, y5, color='lawngreen', legend='σ3',
            line_width=2, line_alpha=0.2)
    p1.line(x, y6, color='lawngreen', legend='σ3',
            line_width=2, line_alpha=0.2)

    # 移動平均乖離線のプロット
    p2 = figure(width=800, height=170, x_axis_type='datetime', x_range=p1.x_range)
    df2 = pd.DataFrame((s.dfs_2["終値"] - s.dfs_2["終値"].rolling(25).mean()) * 100 / s.dfs_2["終値"].rolling(25).mean())
    df3 = pd.DataFrame((s.dfs_2["終値"] - s.dfs_2["終値"].rolling(5).mean()) * 100 / s.dfs_2["終値"].rolling(5).mean())
    p2.line(x, df2["終値"], color='lightblue', legend='25-移動平均乖離率')
    p2.line(x, df3["終値"], color='lemonchiffon', legend='5-移動平均乖離率')
    p2.line(x, 0, color='tomato', line_width=2)


    # グラフの位置とクリックポリシーの設定
    p1.legend.location = 'top_left'
    p1.legend.click_policy = "hide"
    p2.legend.location = 'top_left'
    p2.legend.click_policy = "hide"

    # グラフ背景設定
    p1.background_fill_color = "black"
    p1.grid.grid_line_color = "darkslategray"
    p1.grid.grid_line_alpha=0.6
    p2.background_fill_color = "black"
    p2.grid.grid_line_color = "darkslategray"
    p2.grid.grid_line_alpha=0.6
    # legendの文字サイズ
    p1.legend.label_text_font_size = "5pt"
    p2.legend.label_text_font_size = "5pt"

    """
    source = ColumnDataSource(y.reset_index())
    band = Band(base='x', lower='y6', upper='y5', source=source,
                level='underlay', fill_alpha=1.0, line_width=1, line_color='black')
    p1.add_layout(band)
    """

    # ローソク足チャートをプロット
    inc = s.dfs_2['終値'] > s.dfs_2['始値']
    dec = s.dfs_2['始値'] > s.dfs_2['終値']
    w = 12 * 60 * 60 * 1000 * 2 # half day in ms

    p1.segment(x, s.dfs_2['高値'], x, s.dfs_2['安値'], color="white", line_alpha=0.5)
    p1.vbar(x[inc], w, s.dfs_2['始値'][inc], s.dfs_2['終値'][inc], fill_color="blue", fill_alpha=0.5, line_alpha=0.5)
    p1.vbar(x[dec], w, s.dfs_2['始値'][dec], s.dfs_2['終値'][dec], fill_color="crimson", fill_alpha=0.5, line_alpha=0.5)


    show(column(p1, p2))



if __name__ == '__main__':
    s = Data_Bokeh
    Data_Bokeh.Stock_Data_Get()
    Data_Bokeh.Data_Soup()
    Plot_Data()





