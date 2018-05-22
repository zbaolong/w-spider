# encoding:utf-8

class DataCleanUtil:

    @staticmethod
    def listJoinToStringBynewline(list):
        return '\n'.join(list)

    @staticmethod
    def sliceByColon(value):
        colonIndex = value.find("：")
        return value[colonIndex+1:]


if __name__ == '__main__':
    print(DataCleanUtil.sliceByColon('来源： 原创'))
    print(DataCleanUtil.listJoinToStringBynewline(['\u3000\u30002018年5曰5日下午，二十里铺小学舞蹈社团18名小精灵很荣幸被邀请到河北美术学院参加第六届中国微电影大典启动仪式。', '\u3000\u3000启动仪式上，二十里铺小学《中华家训代代传》节目以舞蹈、诵读相结合的形式，展现青少年对儒家文化的学习、立身之道的弘扬。孩子们的精彩表现，让老师们感动的热泪盈眶，所有的付出在那一刻都得到收获。同时微电影大典还邀请了上过央视春晚的俏夕阳皮影舞蹈团队，老奶奶们舞姿俏皮、情怀如水的皮影舞蹈深深吸引了孩子们，让孩子们大开眼界，学习到了中国优秀传统文化。', '\u3000\u3000在李校长的鼓舞引领下，二十里铺小学音乐组的老师们凭着对艺术的执着追求，凭着对艺术的热爱和干劲，不断用自己优秀的艺术作品向众人展现着二十里铺小学的新风貌。', '■文并摄/河北青年报实习记者周欣怡', '版权归河北河青传媒有限责任公司所有，未经许可不得转载']))