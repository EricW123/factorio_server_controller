电磁工厂插件数量 = 5
回收机插件数量 = 4
插件概率 = 0.062

原料 = [10000] + [0] * 4
成品 = [0] * 5

def 制作(等级):
    global 原料, 成品
    输出 = 原料[等级]
    t = 输出
    if 等级 < 4:
        成品[等级 + 1] += 输出 * 电磁工厂插件数量 * 插件概率
        t -= 输出 * 电磁工厂插件数量 * 插件概率
    if 等级 < 3:
        成品[等级 + 2] += 输出 * 电磁工厂插件数量 * 插件概率 / 10
        t -= 输出 * 电磁工厂插件数量 * 插件概率 / 10
    if 等级 < 2:
        成品[等级 + 3] += 输出 * 电磁工厂插件数量 * 插件概率 / 100
        t -= 输出 * 电磁工厂插件数量 * 插件概率 / 100
    if 等级 < 1:
        成品[等级 + 4] += 输出 * 电磁工厂插件数量 * 插件概率 / 1000
        t -= 输出 * 电磁工厂插件数量 * 插件概率 / 1000
    成品[等级] += 输出 - t
    原料[等级] = 0

def 回收(等级):
    global 原料, 成品
    输出 = 成品[等级]
    t = 输出
    if 等级 > 0:
        原料[等级 - 1] += 输出 * 回收机插件数量 * 插件概率
        t -= 输出 * 回收机插件数量 * 插件概率
    if 等级 > 1:
        原料[等级 - 2] += 输出 * 回收机插件数量 * 插件概率 / 10
        t -= 输出 * 回收机插件数量 * 插件概率 / 10
    if 等级 > 2:
        原料[等级 - 3] += 输出 * 回收机插件数量 * 插件概率 / 100
        t -= 输出 * 回收机插件数量 * 插件概率 / 100
    if 等级 > 3:
        原料[等级 - 4] += 输出 * 回收机插件数量 * 插件概率 / 1000
        t -= 输出 * 回收机插件数量 * 插件概率 / 1000
    原料[等级] += 输出 - t
    成品[等级] = 0


def 计算():
    global 原料, 成品
    for i in range(4):
        制作(i)
    # print(成品)
    for i in range(5):
        回收(i)
    # print(原料)
    
def 循环():
    global 原料, 成品
    for i in range(1000):cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
        计算()ccccccccccccccccc
    print(原料)cccccc
    print(成品)
    
# 计算()
循环()
