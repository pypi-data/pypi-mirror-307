import GGanalysis.games.alchemy_stars as AS
from GGanalysis.gacha_plot import QuantileFunction, DrawDistribution
from GGanalysis import FiniteDist
import matplotlib.cm as cm
import numpy as np
import time

def AS_character(x):
    return '抽取'+str(x)+'个'

# 白夜极光 UP6星光灵
AS_fig = QuantileFunction(
        AS.up_6star(5, multi_dist=True),
        title='白夜极光UP六星光灵抽取概率',
        item_name='UP六星光灵',
        text_head='采用官方公示模型\n获取1个UP六星光灵最多270抽',
        text_tail='@一棵平衡树 '+time.strftime('%Y-%m-%d',time.localtime(time.time())),
        max_pull=1400,
        mark_func=AS_character,
        line_colors=cm.YlOrBr(np.linspace(0.4, 0.9, 5+1)),  # cm.OrAKges(np.linspace(0.5, 0.9, 6+1)),
        y_base_gap=25,
        y2x_base=2,
        is_finite=True)
AS_fig.show_figure(dpi=300, savefig=True)

# 白夜极光 获取6星光灵
AS_fig = DrawDistribution(
    dist_data=AS.common_6star(1),
    title='白夜极光获取六星光灵',
    text_head='采用官方公示模型',
    text_tail='@一棵平衡树 '+time.strftime('%Y-%m-%d',time.localtime(time.time())),
    item_name='六星光灵',
    is_finite=True,
)
AS_fig.show_dist(dpi=300, savefig=True)

# 白夜极光 获取UP6星光灵
AS_fig = DrawDistribution(
    dist_data=AS.up_6star(1),
    title='白夜极光获取UP六星光灵',
    text_head='采用官方公示模型\n获取UP6星光灵最多需要抽3个六星\n保底进度跨池继承',
    text_tail='@一棵平衡树 '+time.strftime('%Y-%m-%d',time.localtime(time.time())),
    item_name='UP六星光灵',
    description_pos=180,
    is_finite=True,
)
AS_fig.show_dist(dpi=300, savefig=True)