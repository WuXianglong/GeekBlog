#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import Image
import ImageDraw
import ImageFont
import random
import StringIO
from math import ceil
from django.http import HttpResponse

_DEFAULT_SESSION_KEY = 'django-verify-code'
_ENABLED_STRINGS = '0123456789abcdefghijklmnopqrstuvwxyz'
_DEFAULT_FONT_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DejaVuSans.ttf")
_CHINESE_CHARS = u"""
一乙二十丁厂七卜人入八九几儿了力乃刀又三于干亏士工土才寸下大丈与万上小口巾山千子
乞川亿个勺久凡及夕丸么广亡门义之尸弓己已卫也女飞刃习叉马乡予劝双书幻奶奴加召皮边
丰王井开夫天无元专云扎艺木五支厅不太犬区历尤友匹车巨牙屯比互切瓦止少日中冈贝内水
介父从今凶分乏公仓月氏勿欠风丹匀乌凤勾文六方火为斗忆订计户认心尺引丑巴孔队办以允
见午牛手毛气升长仁什片仆化仇币仍仅斤爪反玉刊示末未击打巧正扑扒功扔去甘世古节本术
汇头汉宁穴它讨写让礼训必议讯记永司尼民出汁丙左厉右石布龙平灭轧东卡北占业旧帅归且
旦目叶甲申叮电号田由史只央兄叼叫另叨叹四生失禾丘仗代仙们仪白仔他斥瓜乎丛令用甩可
印乐句匆册犯外处冬鸟务包饥主市立闪兰半辽式刑动扛寺吉扣考托老执巩圾扩扫地扬场耳共
芒亚芝朽朴机权过臣再协西压厌在有百存而页匠夸夺灰达列死成夹轨邪划迈毕至此贞师尘尖
劣光当早吐吓虫曲团同吊吃因吸吗屿帆岁回岂刚则肉网年朱先丢舌竹迁乔伟传乒乓休伍伏优
伐延件任伤价份华仰仿伙伪自血向似后行舟全会杀合兆企众爷伞创肌朵杂危旬旨负各名多争
色壮冲冰庄庆亦刘齐交次衣产决充妄闭问闯羊并关米灯州汗污江池汤忙兴宇守宅字安讲军许
论农讽设访寻那迅尽导异孙阵阳收阶阴防奸如寿弄麦形进戒吞远违运扶抚坛技坏扰拒找批扯
址走抄坝贡攻赤折抓扮抢孝均抛投坟抗坑坊抖护壳志扭块声把报却劫芽花芹芬苍芳严芦劳克
苏杆杠杜材村杏极李杨求更束豆两丽医辰励否还歼来连步坚旱盯呈时吴助县里呆园旷围呀吨
足邮男困吵串员听吩吹呜吧吼别岗帐财针钉告我乱利秃秀私每兵估体何但伸作伯伶佣低你住
位伴身皂佛近彻役返余希坐谷妥含邻岔肝肚肠龟免狂犹角删条卵岛迎饭饮系言冻状亩况床库
疗应冷这序辛弃冶忘闲间闷判灶灿弟汪沙汽沃泛沟没沈沉怀忧快完宋宏牢究穷灾良证启评补
初社识诉诊词译君灵即层尿尾迟局改张忌际陆阿陈阻附妙妖妨努忍劲鸡驱纯纱纳纲驳纵纷纸
纹纺驴纽发孕圣对台矛纠母幼丝妇好她妈戏羽观欢买红纤级约纪驰巡组细驶织终驻驼绍经贯
奉玩环武青责现表规抹拢拔拣担坦押抽拐拖拍者顶拆拥抵拘势抱垃拉拦拌幸招坡披拨择抬其
取苦若茂苹苗英范直茄茎茅林枝杯柜析板松枪构杰述枕丧或画卧事刺枣雨卖矿码厕奔奇奋态
欧垄妻轰顷转斩轮软到非叔肯齿些虎虏肾贤尚旺具果味昆国昌畅明易昂典固忠咐呼鸣咏呢岸
岩帖罗帜岭凯败贩购图钓制知垂牧物乖刮秆和季委佳侍供使例版侄侦侧凭侨佩货依的迫质欣
征往爬彼径所舍金命斧爸采受乳贪念贫肤肺肢肿胀朋股肥服胁周昏鱼兔狐忽狗备饰饱饲变京
享店夜庙府底剂郊废净盲放刻育闸闹郑券卷单炒炊炕炎炉沫浅法泄河沾泪油泊沿泡注泻泳泥
沸波泼泽治怖性怕怜怪学宝宗定宜审宙官空帘实试郎诗肩房诚衬衫视话诞询该详建肃录隶居
届刷屈弦承孟孤陕降限妹姑姐姓始驾参艰线练奏春帮珍玻毒型挂封持项垮挎城挠政赴赵挡挺
括拴拾挑指垫挣挤拼挖按挥挪某甚革荐巷带草茧茶荒茫荡荣故胡南药标枯柄栋相查柏柳柱柿
栏树要咸威歪研砖厘厚砌砍面耐耍牵残殃轻鸦适秒香种科重复竿段便俩贷顺修保促侮俭俗星
畏趴胃贵界虹虾蚁思蚂虽品咽骂哗咱响哈咬咳哪炭峡罚贱贴骨钞钟钢钥钩卸缸拜看矩怎牲选
俘信皇泉鬼侵追俊盾待律很须叙剑逃食盆胆胜胞胖脉勉狭狮独狡狱狠贸怨急饶蚀饺饼弯将奖
哀亭亮度迹庭疮疯疫疤姿亲音帝施闻阀阁差养美姜叛送类迷前首逆总炼炸炮烂剃洁洪洒浇浊
洞测洗活派洽染济洋洲浑浓津恒恢恰恼恨举觉宣室宫宪突穿窃客冠语扁袄祖神祝误诱说诵垦
退既屋昼费陡眉孩除险院娃姥姨姻娇怒架贺盈勇怠柔垒绑绒结绕骄绘给络骆绝绞统绣验继昨
耕耗艳泰珠班素蚕顽盏匪捞栽捕振载赶起盐捎捏埋捉捆捐损都哲逝捡换挽热恐壶挨耻耽恭莲
莫荷获晋恶真框桂档桐株桥桃格校核样根索哥速逗栗配翅辱唇夏础破原套逐烈殊顾轿较顿毙
致柴桌虑监紧党晒眠晓鸭晃晌晕蚊哨哭恩唤啊唉罢峰圆贼贿钱钳钻铁铃铅缺氧特牺造乘敌秤
租积秧秩称秘透笔笑笋债借值倚倾倒倘俱倡候俯倍倦健臭射躬息徒徐舰舱般航途拿爹爱颂翁
脆脂胸胳脏胶脑狸狼逢留皱饿恋桨浆衰高席准座脊症病疾疼疲效离唐资凉站剖竞部旁旅畜阅
羞瓶拳粉料益兼烤烘烦烧烛烟递涛浙涝酒涉消浩海涂浴流润浪浸涨烫涌悟悄悔悦害宽家宵绢
宴宾窄容宰案请朗诸读扇袜袖袍被祥课谁调冤谅谈谊剥恳展剧屑弱陵陶陷陪娱娘通能难预桑
球理捧堵描域掩捷排掉堆推掀授教掏掠培接控探据掘职基著勒黄萌萝菌菜萄菊萍菠营械梦梢
"""
_CHINESE_CHARS = _CHINESE_CHARS.replace('\n', '')


class VerifyCode(object):

    def __init__(self, request, c_type='operation', img_width=150, img_height=30, font_color='dark', font_path=None, session_key=None):
        """ 初始化对象信息. """
        self.django_request = request

        # 验证码类型：运算(operation), 字符串(string), 中文(chinese)
        self.code_type = c_type
        self.img_width = img_width
        self.img_height = img_height
        # 验证码字体颜色: black, darkblue, darkred
        self.font_color = font_color
        self.font_path = font_path or _DEFAULT_FONT_PATH
        self.session_key = session_key or _DEFAULT_SESSION_KEY

    def _generate_operation(self, max_value=50):
        """ 生成运算表达式验证码

        @max_value: 运算式中允许出现的最大数字, 默认为50
        """
        operators = ['-', '+']
        operand_x = random.randrange(1, max_value)
        operand_y = random.randrange(1, max_value)
        if operand_x < operand_y:
            operand_x, operand_y = operand_y, operand_x

        r = random.randrange(0, 2)
        code = "%s %s %s = ?" % (operand_x, operators[r], operand_y)
        result = eval("%s%s%s" % (operand_x, operators[r], operand_y))
        return code, result

    def _generate_string(self, length=4):
        """ 生成字符串验证码

        @length: 字符串验证码允许的长度, 默认为4
        """
        random_chars = [_ENABLED_STRINGS[random.randrange(0, len(_ENABLED_STRINGS))] for i in range(length)]
        code = ''.join(random_chars)
        return code, code

    def _generate_chinese(self, length=4):
        """ 生成中文验证码

        @length: 中文验证码允许的长度, 默认为4
        """
        random_chars = [_CHINESE_CHARS[random.randrange(0, len(_CHINESE_CHARS))] for i in range(length)]
        code = u''.join(random_chars)
        return code, code

    def _generate_verify_code(self):
        """ 生成验证码和答案 """
        generate_fun = getattr(self, '_generate_%s' % self.code_type, None)
        code, result = generate_fun() if callable(generate_fun) else self._generate_operation()
        self._set_session_value(result)

        return code

    def _set_session_value(self, value):
        """ 将验证码答案放在request session中 """
        self.django_request.session[self.session_key] = str(value)

    def _get_font_size(self):
        """ 将图片高度的80%作为字体大小 """
        s1 = int(self.img_height * 0.8)
        s2 = int(self.img_width / len(self.code))
        return int(min((s1, s2)) + max((s1, s2)) * 0.05)

    def display(self):
        """ 生成并返回验证码图片 """

        # 图片背景颜色
        self.img_background = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))
        # 生成图片
        im = Image.new('RGB', (self.img_width, self.img_height), self.img_background)

        # 得到验证码
        self.code = self._generate_verify_code()
        # 调整验证码字符大小
        self.font_size = self._get_font_size()
        # 创建画笔
        draw = ImageDraw.Draw(im)
        # 画随机干扰线,字数越少,干扰线越多
        line_num = 4

        for i in range(random.randrange(line_num - 2, line_num)):
            line_color = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
            xy = (
                random.randrange(0, int(self.img_width * 0.2)),
                random.randrange(0, self.img_height),
                random.randrange(3 * self.img_width / 4, self.img_width),
                random.randrange(0, self.img_height)
            )
            draw.line(xy, fill=line_color, width=int(self.font_size * 0.1))

        # 写验证码
        j = int(self.font_size * 0.3)
        k = int(self.font_size * 0.5)
        x = random.randrange(j, k)    # 起始位置
        for i in self.code:
            # 上下抖动量,字数越多,上下抖动越大
            m = int(len(self.code))
            y = random.randrange(1, 3)

            if i in ('+', '=', '?'):
                # 对计算符号等特殊字符放大处理
                m = ceil(self.font_size * 0.8)
            else:
                # 字体大小变化量,字数越少,字体大小变化越多
                m = random.randrange(0, int(45 / self.font_size) + int(self.font_size / 5))

            self.font = ImageFont.truetype(self.font_path.replace('\\', '/'), self.font_size + int(ceil(m)))
            draw.text((x, y), i, font=self.font, fill=random.choice(self.font_color))
            x += self.font_size * 0.9

        del x
        del draw
        buf = StringIO.StringIO()
        im.save(buf, 'gif')
        buf.closed
        return HttpResponse(buf.getvalue(), 'image/gif')

    def check(self, code):
        """ 检查用户输入的验证码是否正确 """
        _code = self.django_request.session.get(self.session_key) or ''
        if not _code:
            return False
        return _code.lower() == str(code).lower()
