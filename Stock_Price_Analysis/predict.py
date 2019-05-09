
from fbprophet import Prophet  # 時系列予測ライブラリ
import Data_Bokeh
import pandas as pd
import matplotlib.pyplot as plt

def fb():

    dfs_3 = pd.DataFrame()
    dfs_3['ds'] = s.dfs_2['日付']
    dfs_3['y'] = s.dfs_2['終値']
    print(dfs_3.head())

    # モデル作成
    model = Prophet()
    model.fit(dfs_3)

    # 描画の設定,何日分出力する、など
    future_df = model.make_future_dataframe(50)
    forecast_df = model.predict(future_df)
    model.plot(forecast_df)
    model.plot_components(forecast_df)
    plt.show()


if __name__ == '__main__':
    s = Data_Bokeh
    Data_Bokeh.Stock_Data_Get()
    Data_Bokeh.Data_Soup()
    fb()