from GGanalysis.distribution_1d import *
from GGanalysis.gacha_layers import *
from GGanalysis.basic_models import *

__all__ = [
    'PITY_6STAR',
    'P_5',
    'P_4',
    'P_3',
    'P_2',
    'P_6s',
    'P_5s',
    'P_4s',
    'P_3s',
    'P_2s',
    'common_6star',
    'common_5star',
    'common_4star',
    'common_3star',
    'common_2star',
    'up_6star',
    'specific_up_5star',
    'specific_stander_6star',
    'both_up_5star',
    'stander_charactor_collection',
    'dual_up_specific_6star',
    'dual_up_both_6star',
    'triple_pool_6star',
]

# 重返未来1999普通6星保底概率表
PITY_6STAR = np.zeros(71)
PITY_6STAR[1:61] = 0.015
PITY_6STAR[61:71] = np.arange(1, 11) * 0.025 + 0.015
PITY_6STAR[70] = 1
# 其他无保底物品初始概率
P_5 = 0.085
P_4 = 0.4
P_3 = 0.45
P_2 = 0.05
# 按照 stationary_p.py 的计算结果修订
P_6s = 0.0235922
P_5s = 0.08479687
P_4s = 0.40130344
P_3s = 0.44340267
P_2s = 0.04690482
# 定义获取星级物品的模型
common_6star = PityModel(PITY_6STAR)
common_5star = BernoulliGachaModel(P_5s)
common_4star = BernoulliGachaModel(P_4s)
common_3star = BernoulliGachaModel(P_3s)
common_2star = BernoulliGachaModel(P_2s)
# 定义获取UP物品模型
up_6star = DualPityModel(PITY_6STAR, [0, 0.5, 1])
specific_up_5star = BernoulliGachaModel(P_5s/4)
# 定义集齐两个UP五星模型
both_up_5star = GeneralCouponCollectorModel([P_5s/4, P_5s/4], ['up5star1', 'up5star2'])
# 常驻获取特定6星角色
specific_stander_6star = PityBernoulliModel(PITY_6STAR, 1/11)
# 定义集齐常驻
stander_charactor_collection = PityCouponCollectorModel(PITY_6STAR, 11)
# 常驻自选六星角色池抽到特定自选六星角色模型
dual_up_specific_6star = DualPityBernoulliModel(PITY_6STAR, [0, 0.7, 1], 1/2)
dual_up_both_6star = DualPityCouponCollectorModel(PITY_6STAR, [0, 0.7, 1], 2)
# 常驻三池选一卡池模型
triple_pool_6star = PityBernoulliModel(PITY_6STAR, 1/3)

if __name__ == '__main__':
    # print(PITY_6STAR)
    print(common_6star(1).exp, 1/common_6star(1).exp)
    # print(stander_charactor_collection(target_types=2).exp)
    print(dual_up_specific_6star(1).exp)
    print(dual_up_both_6star().exp)