#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-07 (Fri) Edition"""
import json, os, subprocess, re, time
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-07'
tok = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C

def kata_to_hira(s):
    r = []
    for ch in s:
        if 'カ' <= ch <= 'ン': r.append(chr(ord(ch) - ord('カ') + ord('か')))
        elif 'ア' <= ch <= 'オ': r.append(chr(ord(ch) - ord('ア') + ord('あ')))
        elif 'ヴ' == ch: r.append('ゔ')
        else: r.append(ch)
    return ''.join(r)

POS_MAP = {
    '名詞': 'noun', '動詞': 'verb', '助詞': 'particle',
    '形容詞': 'adj', '連体詞': 'adj', '副詞': 'adverb',
    '接続詞': 'connector', '接頭辞': 'connector', '接尾辞': 'connector',
    '助動詞': 'grammar', '感動詞': 'connector'
}

def map_pos(parts):
    return POS_MAP.get(parts[0], '') if parts else ''

def tokenize_text(text):
    words = []
    for t in tok.tokenize(text, mode):
        p = t.part_of_speech()
        r = t.reading_form() or ''
        if r: r = kata_to_hira(r)
        di = t.dictionary_form()
        words.append({
            's': di if di != '*' else t.surface(),
            'r': r if r and r != t.surface() else '',
            'p': map_pos(p)
        })
    return words

def gen_mp3(text, outpath):
    if os.path.exists(outpath) and os.path.getsize(outpath) > 1000:
        return True
    subprocess.run(
        ['edge-tts', '--voice', 'ja-JP-NanamiNeural',
         '--text', text, '--write-media', outpath],
        capture_output=True, timeout=180)
    return os.path.exists(outpath) and os.path.getsize(outpath) > 1000

# ==================================================================
# TODAY'S ARTICLES — 2026-08-07
# ==================================================================
articles = []
articles += [
    {
        "slug": "taifuu13-okinawa-amami-sekken",
        "title": "台風13号、沖縄・奄美に最接近 線状降水帯発生のおそれ 長時間の暴風・高波に警戒",
        "subtitle": "from tenki.jp",
        "paras": [
            {
                "ja": "今日7日は、台風13号が沖縄や奄美に最接近するでしょう。沖縄と奄美では猛烈な風や猛烈なしけとなる所があり、線状降水帯が発生するおそれもあります。台風13号は、強い勢力を維持したまま明日8日(土)にかけて南西諸島を西よりに進み、暴風や大雨など影響を受ける時間が長くなるでしょう。",
                "en": "Today, the 7th, Typhoon No. 13 is expected to make its closest approach to Okinawa and Amami. In Okinawa and Amami, some areas will experience ferocious winds and violent seas, and there is also a risk of linear rainbands forming. Typhoon No. 13 will continue moving westward across the Nansei Islands through tomorrow, the 8th (Saturday), while maintaining its strong strength, so the period affected by violent winds and heavy rain will become longer.",
                "literal": "今天7日，台风13号将最接近冲绳和奄美吧。冲绳和奄美有些地方会刮猛烈的风、出现猛烈的浪，也有发生线状降水带的危险。台风13号在维持强劲势力的状态下，到明天8日（周六）为止将向南西诸岛偏西方向前进，受到暴风和大雨等影响的时间将会变长吧。",
                "grammar": "「〜最接近するでしょう」— 将最接近…吧（推量）。例：沖縄や奄美に最接近するでしょう（将最接近冲绳和奄美）。\n「〜おそれもあります」— 也有…的危险。例：線状降水帯が発生するおそれもあります（也有发生线状降水带的危险）。\n「〜に進み、〜なるでしょう」— 向…前进，将变得…（并列+推量）。例：西よりに進み、影響を受ける時間が長くなるでしょう（向偏西方向前进，受影响的时间将变长）。",
                "vocab": [
                    ["最接近", "さいせっきん", "最接近"],
                    ["猛烈", "もうれつ", "猛烈、凶猛"],
                    ["しけ", "しけ", "风浪、波涛汹涌"],
                    ["線状降水帯", "せんじょうこうすいたい", "线状降水带"],
                    ["勢力", "せいりょく", "势力、强度"],
                    ["南西諸島", "なんせいしょとう", "南西诸岛"]
                ]
            },
            {
                "ja": "大型で強い台風13号は、今日7日(金)午前5時には沖永良部島の東およそ140キロにあって、1時間におよそ20キロの速さで西北西へ進んでいます。奄美大島や沖縄本島の一部が風速25メートル以上の暴風域に入っています。このあと、強い勢力を維持したまま南西諸島を西よりに進み、沖縄本島地方には今日7日(金)の昼過ぎに最接近する予想です。",
                "en": "The large and powerful Typhoon No. 13 was located about 140 km east of Okinoerabu Island at 5 a.m. today, the 7th (Friday), moving west-northwest at a speed of about 20 km per hour. Parts of Amami-Oshima and the main island of Okinawa have entered the storm zone with wind speeds of 25 m/s or more. After this, it will continue moving westward across the Nansei Islands while maintaining its strong strength, and is forecast to make its closest approach to the Okinawa main island region after noon today, the 7th (Friday).",
                "literal": "大型且强劲的台风13号，今天7日（周五）上午5点位于冲永良部岛以东约140公里处，以每小时约20公里的速度向西北偏西方向前进。奄美大岛和冲绳本岛的一部分已进入风速25米以上的暴风区域。之后，在维持强劲势力的状态下向南西诸岛偏西方向前进，预计今天7日（周五）午后过后来到冲绳本岛地区附近（最接近）。",
                "grammar": "「〜にあって」— 位于…（书面语）。例：沖永良部島の東およそ140キロにあって（位于冲永良部岛以东约140公里处）。\n"+"「〜に入っています」— 已进入…。例：暴風域に入っています（已进入暴风区域）。\n「〜予想です」— 预计…。例：昼過ぎに最接近する予想です（预计午后过后来到最近处）。",
                "vocab": [
                    ["大型", "おおがた", "大型"],
                    ["およそ", "およそ", "大约、大致"],
                    ["西北西", "せいほくせい", "西北偏西"],
                    ["暴風域", "ぼうふういき", "暴风区域"],
                    ["維持", "いじ", "维持"],
                    ["予想", "よそう", "预测、预计"]
                ]
            },
            {
                "ja": "沖縄や奄美では一部の住家が倒壊するおそれもある猛烈な風が吹き、猛烈なしけや大しけとなる所がありそうです。暴風やうねりを伴った高波に厳重に警戒してください。また、台風本体や周辺の発達した雨雲がかかり、局地的には滝のような非常に激しい雨が降りそうです。線状降水帯が発生して、大雨災害の危険度が急激に高まる可能性があります。",
                "en": "In Okinawa and Amami, ferocious winds that could topple some houses are blowing, and some areas are likely to experience violent seas or very high waves. Please be on high alert for violent winds and high waves accompanied by swells. In addition, the typhoon itself and developed rain clouds around it will cover the region, and locally, extremely intense rain like a waterfall is likely to fall. If linear rainbands form, the risk of heavy-rain disasters could rise rapidly.",
                "literal": "冲绳和奄美会刮有部分住宅倒塌危险的猛烈强风，有些地方可能会出现猛烈风浪或大浪。请对伴随涌浪的暴风和巨浪严加警戒。另外，台风主体和周边发展旺盛的雨云会笼罩过来，局部地区可能会下像瀑布一样的极强暴雨。如果发生线状降水带，大雨灾害的危险度可能会急剧升高。",
                "grammar": "「〜おそれもある」— 也有…的危险。例：住家が倒壊するおそれもある（也有住宅倒塌的危险）。\n「〜に警戒してください」— 请警戒…。例：暴風や高波に厳重に警戒してください（请严加警戒暴风和巨浪）。\n「〜可能性があります」— 有…的可能性。例：危険度が急激に高まる可能性があります（危险度有可能急剧升高）。",
                "vocab": [
                    ["倒壊", "とうかい", "倒塌"],
                    ["うねり", "うねり", "涌浪"],
                    ["高波", "たかなみ", "巨浪、大浪"],
                    ["発達", "はったつ", "发展、发达"],
                    ["局地的", "きょくちてき", "局部地区性的"],
                    ["危険度", "きけんど", "危险度"]
                ]
            }
        ]
    },
    {
        "slug": "hinanjo-kakusa-kumamoto-jishin",
        "title": "避難所めぐる“格差” 男女同室で「着替えられない」 雑魚寝続く被災地 専門家「標準化されていない」",
        "subtitle": "from FNNプライムオンライン",
        "paras": [
            {
                "ja": "熊本地震から6日で10日目です。今も多くの人が避難所での生活を余儀なくされていますが、そこで聞こえてくるのは「プライバシーが確保できない」という声です。震度7を記録した宇城市の避難所では、被災者たちはいまだに「雑魚寝」やソファでの生活を強いられていて、パーティションもなく、プライバシーは守られていません。",
                "en": "Ten days have passed since the Kumamoto earthquake, counting the 6th as day 10. Many people are still forced to live in evacuation shelters, and the voices heard there are complaints that \"privacy cannot be secured.\" At a shelter in Uki City, which recorded seismic intensity 7, evacuees are still forced to sleep crammed together on the floor or on sofas, with no partitions, and their privacy is not protected.",
                "literal": "熊本地震到6日为止已是第10天。现在仍有很多人被迫过着避难所的生活，但那里听到的是「无法确保隐私」的声音。在记录到震度7的宇城市的避难所，受灾者们至今仍被迫过着「挤在一起睡」或睡沙发的日子，没有隔板，隐私得不到保护。",
                "grammar": "「〜余儀なくされています」— 被迫…（书面语）。例：避難所での生活を余儀なくされています（被迫过避难所生活）。\n「〜強いられていて」— 正被迫…。例：雑魚寝やソファでの生活を強いられていて（被迫过着挤睡或睡沙发的日子）。\n「〜守られていません」— 没有被保护（被动否定）。例：プライバシーは守られていません（隐私没有得到保护）。",
                "vocab": [
                    ["避難所", "ひなんじょ", "避难所"],
                    ["余儀なく", "よぎなく", "被迫、不得已"],
                    ["確保", "かくほ", "确保"],
                    ["震度", "しんど", "地震烈度"],
                    ["雑魚寝", "ざこね", "挤在一起睡、大通铺"],
                    ["パーティション", "ぱーてぃしょん", "隔板、隔断"]
                ]
            },
            {
                "ja": "さらに、高市総理が視察した熊本・氷川町の中学校では「段ボールベッド」が発災から5日後に届き、パーティションも設置されていますが、男女が同じ教室で過ごしていてパーティションも低いため、22歳の女性は「家とは違うので、すぐに着替えられない」と話します。周囲の目が気になり着替えもままならない状況は、発災から10日目となった今も続いています。",
                "en": "Furthermore, at a junior high school in Hikawa Town, Kumamoto, which Prime Minister Takaichi inspected, \"cardboard beds\" arrived five days after the disaster and partitions were installed, but men and women are spending time in the same classroom, and since the partitions are low, a 22-year-old woman says, \"It's different from home, so I can't change clothes easily.\" The situation where people cannot change clothes freely because they worry about the eyes of those around them continues even now, ten days after the disaster.",
                "literal": "而且，在高市总理视察过的熊本·冰川町的中学里，「纸板床」在灾害发生5天后才送到，虽然也设置了隔板，但因为男女在同一个教室里生活、隔板也很低，22岁的女性说「和家里不一样，不能马上换衣服」。在意周围目光、连换衣服都不能随心所欲的状况，到灾害发生第10天的现在仍在持续。",
                "grammar": "「〜ため、〜」— 因为…，所以…。例：パーティションも低いため、着替えられない（因为隔板也低，所以不能换衣服）。\n「〜と話します」— 说…（引用）。例：すぐに着替えられないと話します（说不能马上换衣服）。\n「〜ままならない」— 不能随心所欲、无法如愿。例：着替えもままならない（连换衣服都无法如愿）。",
                "vocab": [
                    ["視察", "しさつ", "视察"],
                    ["段ボール", "だんぼーる", "瓦楞纸板"],
                    ["発災", "はっさい", "灾害发生"],
                    ["設置", "せっち", "设置、安装"],
                    ["着替える", "きがえる", "换衣服"],
                    ["ままならない", "ままならない", "不能如愿、无法随心所欲"]
                ]
            },
            {
                "ja": "避難所・避難生活学会の水谷嘉浩代表理事は「（日本は）『災害対策基本法』によって、被災した市町村が被災者を支援しなさいと。私は“避難所ガチャ”と言っているが、標準化されていないので、同じ市内でも避難所によってバラバラのやり方になる」と話しました。一方でイタリアは、国の方針に従い、被災した自治体に代わって、他の州が避難所運営を担うことで均一化されているといいます。長引く避難生活の負担を軽減するため、制度の改革が急務だということです。",
                "en": "Yoshihiro Mizutani, representative director of the Japan Society for Evacuation and Evacuation Life, said, \"Under the Basic Act on Disaster Control Measures, Japan tells affected municipalities to support victims. I call it the 'shelter gacha,' but because things are not standardized, even within the same city, each shelter operates in its own way.\" Meanwhile, in Italy, it is said that shelters are made uniform because, following national policy, other regions run shelter operations on behalf of the affected local governments. To reduce the burden of prolonged evacuation life, reforming the system is an urgent task.",
                "literal": "避难所·避难生活学会的理事长水谷嘉浩说「（日本）根据《灾害对策基本法》，要求受灾的市町村去支援受灾者。我称之为“避难所抽卡”，因为没有标准化，所以即使在同一个市内，也因避难所不同而做法各异」。另一方面，据说意大利遵循国家方针，由其他州代替受灾地方政府承担避难所运营，从而实现了一体化。为了减轻长期避难生活的负担，制度改革是当务之急。",
                "grammar": "「〜によって、〜」— 根据…、通过…。例：災害対策基本法によって支援しなさいと（根据灾害对策基本法要求支援）。\n「〜に代わって」— 代替…。例：被災した自治体に代わって、他の州が担う（由其他州代替受灾地方政府承担）。\n「〜が急務だ」— …是当务之急。例：制度の改革が急務だ（制度改革是当务之急）。",
                "vocab": [
                    ["代表理事", "だいひょうりじ", "代表理事、董事长"],
                    ["支援", "しえん", "支援、支持"],
                    ["標準化", "ひょうじゅんか", "标准化"],
                    ["バラバラ", "ばらばら", "各不相同、零散"],
                    ["自治体", "じちたい", "地方自治体、地方政府"],
                    ["急務", "きゅうむ", "当务之急"]
                ]
            }
        ]
    },
    {
        "slug": "aeon-kumamoto-bakuhatsu-lpg",
        "title": "イオンモール熊本の爆発事故 LPガス供給会社「調査に全面的に協力」 経産省「LPガス爆発の可能性高い」",
        "subtitle": "from RKB毎日放送",
        "paras": [
            {
                "ja": "この事故は7月28日、熊本県で最大震度7を観測する地震が発生した後、嘉島町にあるイオンモール熊本で爆発が起き、7人が死亡、5人が軽傷を負ったものです。",
                "en": "In this incident, after an earthquake with a maximum seismic intensity of 7 was observed in Kumamoto Prefecture on July 28, an explosion occurred at Aeon Mall Kumamoto in Kashima Town, killing seven people and lightly injuring five.",
                "literal": "这起事故是7月28日，熊本县发生最大震度7的地震之后，位于嘉岛町的永旺商城熊本店发生爆炸，造成7人死亡、5人受轻伤的事故。",
                "grammar": "「〜後、〜が起き」— 在…之后，发生了…。例：地震が発生した後、爆発が起き（地震发生后，发生了爆炸）。\n「〜を負ったものです」— 是受了…的（事）。例：5人が軽傷を負ったものです（是5人受轻伤的事故）。",
                "vocab": [
                    ["爆発", "ばくはつ", "爆炸"],
                    ["最大震度", "さいだいしんど", "最大地震烈度"],
                    ["観測", "かんそく", "观测"],
                    ["死亡", "しぼう", "死亡"],
                    ["軽傷", "けいしょう", "轻伤"]
                ]
            },
            {
                "ja": "経済産業省は5日、事故の原因について、警察や消防との合同調査の結果、「LPガス爆発の可能性が高い」という見解で一致したと発表しました。",
                "en": "On the 5th, the Ministry of Economy, Trade and Industry announced that, regarding the cause of the accident, the results of a joint investigation with the police and fire department had led to agreement on the view that \"the possibility of an LP gas explosion is high.\"",
                "literal": "经济产业省于5日就事故原因宣布，与警察和消防联合调查的结果表明，「LP燃气爆炸的可能性很高」这一见解已达成一致。",
                "grammar": "「〜について、〜」— 关于…，…。例：事故の原因について、合同調査の結果（关于事故原因，联合调查的结果）。\n「〜見解で一致した」— 在…见解上达成一致。例：「LPガス爆発の可能性が高い」という見解で一致した（在“LP燃气爆炸可能性很高”的见解上达成一致）。\n「〜と発表しました」— 宣布…。例：一致したと発表しました（宣布已达成一致）。",
                "vocab": [
                    ["経済産業省", "けいざいさんぎょうしょう", "经济产业省"],
                    ["合同調査", "ごうどうちょうさ", "联合调查"],
                    ["可能性", "かのうせい", "可能性"],
                    ["見解", "けんかい", "见解、看法"],
                    ["一致", "いっち", "一致、达成一致"]
                ]
            },
            {
                "ja": "LPガスを供給していたのは、久留米市に本社を置く「福岡酸素」で、5日、熊本県を通じて経産省に事故を報告したということです。福岡酸素は6日、「大変重く受け止めている。関係当局の調査に全面的に協力し、誠実に対応していく」とのコメントを発表しました。",
                "en": "The company that supplied the LP gas was \"Fukuoka Oxygen,\" headquartered in Kurume City, and it is said that on the 5th it reported the accident to METI through Kumamoto Prefecture. On the 6th, Fukuoka Oxygen released a comment saying, \"We take this extremely seriously. We will fully cooperate with the investigation by the relevant authorities and respond with sincerity.\"",
                "literal": "供应LP燃气的是总部设在久留米市的「福冈氧气」，据说5日通过熊本县向经产省报告了事故。福冈氧气于6日发表了「我们非常沉重地对待此事。将全面配合相关当局的调查，诚恳应对」的评论。",
                "grammar": "「〜に本社を置く」— 总部设在…。例：久留米市に本社を置く「福岡酸素」（总部设在久留米市的“福冈氧气”）。\n「〜を通じて」— 通过…。例：熊本県を通じて報告した（通过熊本县进行了报告）。\n「〜とのコメントを発表しました」— 发表了…的评论。例：誠実に対応していくとのコメントを発表しました（发表了将诚恳应对的评论）。",
                "vocab": [
                    ["供給", "きょうきゅう", "供应、供给"],
                    ["本社", "ほんしゃ", "总公司、总部"],
                    ["報告", "ほうこく", "报告"],
                    ["受け止める", "うけとめる", "对待、承受"],
                    ["全面的", "ぜんめんてき", "全面的"],
                    ["誠実", "せいじつ", "诚恳、诚实"]
                ]
            }
        ]
    },
    {
        "slug": "zaimushou-jinji-iten-haran",
        "title": "エース級の財務官僚が異例転出へ 官邸幹部「協力的でなかったから」 消費減税巡り対立か",
        "subtitle": "from 朝日新聞",
        "paras": [
            {
                "ja": "7日発表予定の財務省人事が波紋を呼んでいる。将来の次官候補と言われている一松旬・主計局次長が東京税関長に転出する案で、エース級の財務官僚がこのポストに就くのは異例。消費減税などで意見が対立した高市政権の強い意向があったとされ、官邸幹部は人事について「（一松氏は）政権にあまり協力的でなかったから」と語った。",
                "en": "The Ministry of Finance personnel changes scheduled to be announced on the 7th are causing a stir. Under the plan, Jun Hitomatsu, deputy director-general of the Budget Bureau, who is said to be a future candidate for vice minister, will be transferred to the post of Tokyo Customs chief — it is unusual for a top-class finance bureaucrat to take this position. It is said that the Takaichi administration, with which he clashed over the food consumption tax cut and other matters, exerted strong influence, and a senior government official said of the personnel change, \"(Hitomatsu) was not very cooperative with the administration.\"",
                "literal": "预定7日公布的财务省人事引发波澜。被称为未来次官候选人的一松旬·主计局次长将调任东京海关关长的方案中，王牌级财务官僚就任这一职位实属罕见。据说与高市政权因消费税减税等意见对立，政权方面有强烈意向，官邸干部就人事问题说「（一松氏）对政权不太配合」。",
                "grammar": "「〜と言われている」— 被称为…、据说…。例：将来の次官候補と言われている（被称为未来的次官候选人）。\n「〜とされ」— 被认为是…、据说…。例：強い意向があったとされ（据说有强烈的意向）。\n「〜から」— 因为…。例：協力的でなかったから（因为不太配合）。",
                "vocab": [
                    ["人事", "じんじ", "人事、人事变动"],
                    ["波紋", "はもん", "波澜、波纹"],
                    ["次官", "じかん", "次官、副部长"],
                    ["異例", "いれい", "罕见、破例"],
                    ["対立", "たいりつ", "对立"],
                    ["幹部", "かんぶ", "干部、高层"]
                ]
            },
            {
                "ja": "一松氏は1995年に入省。予算編成を行う主計局の社会保障担当や予算全体を指揮する企画担当の主計官、岸田文雄首相（当時）の秘書官などを歴任し、「10年に1度の大物財務官僚」との呼び声が高かった。昨年10月から主計局次長として、政権肝いりの給付付き税額控除の実務を取り仕切ってきた。",
                "en": "Hitomatsu joined the ministry in 1995. He served in a series of posts, including budget examiner in charge of social security in the Budget Bureau, which drafts the budget, budget examiner in charge of planning overseeing the entire budget, and secretary to then-Prime Minister Fumio Kishida, and he was increasingly hailed as \"a once-in-a-decade heavyweight finance bureaucrat.\" Since last October, as deputy director-general of the Budget Bureau, he has been in charge of the practical work of the refundable tax credit, a pet project of the administration.",
                "literal": "一松氏1995年进入省厅。历任编制预算的主计局的社会保障负责人、指挥整个预算的企划负责人主计官、岸田文雄首相（当时）的秘书官等职务，「10年一遇的大人物财务官僚」的呼声很高。从去年10月起担任主计局次长，一直掌管政权力推的返还型税额扣除的实务。",
                "grammar": "「〜を歴任し」— 历任…。例：秘書官などを歴任し（历任秘书官等职务）。\n「〜との呼び声が高かった」— …的呼声很高。例：大物財務官僚との呼び声が高かった（大人物财务官僚的呼声很高）。\n「〜を取り仕切ってきた」— 一直掌管…。例：実務を取り仕切ってきた（一直掌管实务）。",
                "vocab": [
                    ["入省", "にゅうしょう", "进入省厅工作"],
                    ["予算編成", "よさんへんせい", "预算编制"],
                    ["歴任", "れきにん", "历任"],
                    ["大物", "おおもの", "大人物、重量级人物"],
                    ["肝いり", "きもいり", "热心推动、力推"],
                    ["実務", "じつむ", "实务、实际工作"]
                ]
            },
            {
                "ja": "一松氏は強い財政再建論者で、政治家に直言することで知られている。官邸幹部は「（一松氏は）初めての挫折を味わっているんじゃないか」と「左遷」含みの人事であることを認めた。「官庁の中の官庁」とされる財務省では、人事をめぐって官邸の意向が露骨に反映されることはなかった。",
                "en": "Hitomatsu is a strong advocate of fiscal reconstruction and is known for speaking frankly to politicians. The senior government official acknowledged that the personnel change smacks of \"demotion,\" saying, \"(Hitomatsu) must be tasting his first setback.\" In the Ministry of Finance, known as \"the ministry among ministries,\" the government's intentions had never been so blatantly reflected in personnel matters.",
                "literal": "一松氏是坚定的财政重建论者，以向政治家直言不讳而闻名。官邸干部承认这是带「降职」意味的人事安排，说「（一松氏）是不是在品尝第一次挫折」。在被称为「官厅中的官厅」的财务省，围绕人事，官邸的意向从未如此露骨地被反映过。",
                "grammar": "「〜ことで知られている」— 因…而闻名。例：直言することで知られている（以直言而闻名）。\n「〜んじゃないか」— 是不是…呢（推测）。例：挫折を味わっているんじゃないか（是不是正在品尝挫折）。\n「〜ことはなかった」— 从未…过。例：露骨に反映されることはなかった（从未被露骨地反映过）。",
                "vocab": [
                    ["財政再建", "ざいせいさいけん", "财政重建"],
                    ["直言", "ちょくげん", "直言、直说"],
                    ["挫折", "ざせつ", "挫折"],
                    ["左遷", "させん", "降职、贬谪"],
                    ["露骨", "ろこつ", "露骨、毫不掩饰"],
                    ["反映", "はんえい", "反映"]
                ]
            }
        ]
    },
    {
        "slug": "taiyou-hyoumen-saikou-kaizoudo",
        "title": "太陽表面を過去最高の解像度で観測、磁気にまつわる謎が明らかに 米研究チーム",
        "subtitle": "from CNN.co.jp",
        "paras": [
            {
                "ja": "世界で最も強力な太陽望遠鏡が、太陽の可視表面をこれまでで最高の解像度で捉えることに成功した。その結果、太陽の活動を促す隠れたプロセスの存在が明らかになった。科学者たちは、ハワイ・マウイ島の火山ハレアカラ山頂近くに設置された米国立科学財団（NSF）のダニエル・K・イノウエ太陽望遠鏡を用いて、磁気活動が活発な黒点付近を詳細に観測した。",
                "en": "The world's most powerful solar telescope has succeeded in capturing the visible surface of the Sun at the highest resolution ever achieved. As a result, the existence of hidden processes that drive solar activity has been revealed. Using the National Science Foundation's (NSF) Daniel K. Inouye Solar Telescope, installed near the summit of the volcano Haleakala on the island of Maui, Hawaii, scientists observed in detail the area around sunspots, where magnetic activity is vigorous.",
                "literal": "世界上最强力的太阳望远镜，成功以迄今最高的分辨率捕捉到了太阳的可见表面。其结果，促使太阳活动的隐藏过程的存在变得明朗。科学家们使用设置在夏威夷毛伊岛火山哈雷阿卡拉山顶附近的美国国家科学基金会（NSF）的丹尼尔·K·井上太阳望远镜，对磁活动活跃的黑点附近进行了详细观测。",
                "grammar": "「〜ことに成功した」— 成功做到了…。例：捉えることに成功した（成功捕捉到了）。\n「〜が明らかになった」— …变得明确。例：存在が明らかになった（存在变得明确）。\n「〜を用いて」— 使用…。例：太陽望遠鏡を用いて観測した（使用太阳望远镜进行了观测）。",
                "vocab": [
                    ["太陽", "たいよう", "太阳"],
                    ["解像度", "かいぞうど", "分辨率"],
                    ["可視表面", "かしひょうめん", "可见表面"],
                    ["黒点", "こくてん", "太阳黑子"],
                    ["活発", "かっぱつ", "活跃、旺盛"],
                    ["詳細", "しょうさい", "详细"]
                ]
            },
            {
                "ja": "詳細な画像とコンピューターシミュレーションを組み合わせた結果、研究者たちは太陽物理学における画期的な知見を獲得した。具体的には、太陽表面に見られる小さな渦の特徴を特定した。この渦は地球上の生活にも直接影響を及ぼす可能性がある。ケルビン・ヘルムホルツ不安定性（KHI）として知られるこの渦巻き状のパターンから、長年にわたる太陽の謎を説明できるかもしれません。",
                "en": "By combining detailed images with computer simulations, the researchers gained groundbreaking insights in solar physics. Specifically, they identified the characteristics of small vortices seen on the Sun's surface. These vortices could directly affect life on Earth. This spiral pattern, known as the Kelvin-Helmholtz instability (KHI), may help explain long-standing mysteries of the Sun.",
                "literal": "将详细图像与计算机模拟相结合的结果，研究者们获得了太阳物理学中划时代的见解。具体来说，特定了太阳表面可见的小漩涡的特征。这个漩涡有可能对地球上的生活也产生直接影响。从被称为开尔文-亥姆霍兹不稳定性（KHI）的这一漩涡状图案，也许能解释长达多年的太阳之谜。",
                "grammar": "「〜を組み合わせた結果」— 将…结合的结果。例：画像とシミュレーションを組み合わせた結果（将图像与模拟结合的结果）。\n「〜における」— 在…中的。例：太陽物理学における画期的な知見（太阳物理学中的划时代见解）。\n「〜かもしれません」— 也许…。例：説明できるかもしれません（也许能解释）。",
                "vocab": [
                    ["組み合わせる", "くみあわせる", "组合、结合"],
                    ["画期的", "かっきてき", "划时代的"],
                    ["知見", "ちけん", "见解、知识"],
                    ["渦", "うず", "漩涡"],
                    ["特定", "とくてい", "确定、特定"],
                    ["パターン", "ぱたーん", "图案、模式"]
                ]
            },
            {
                "ja": "また、これらの渦は太陽の磁気エネルギーの蓄積を促進し、太陽フレアやコロナ質量放出（CME）を引き起こす要因にもなり得る。これらの太陽活動が地球に向かうと、放出された粒子が人工衛星や送電網、その他の通信インフラに障害を引き起こす恐れがある。5日付の学術誌ネイチャーに掲載された今回の研究成果は、予測が難しい太陽の挙動や活動について、科学者たちの理解を深める助けとなる可能性がある。",
                "en": "Moreover, these vortices promote the accumulation of magnetic energy on the Sun and could also be a factor triggering solar flares and coronal mass ejections (CMEs). When this solar activity is directed toward Earth, the released particles could cause disruptions to satellites, power grids, and other communications infrastructure. The findings, published in the academic journal Nature on the 5th, could help scientists deepen their understanding of the Sun's behavior and activity, which are difficult to predict.",
                "literal": "另外，这些漩涡促进太阳磁能积蓄，也可能成为引发太阳耀斑和日冕物质抛射（CME）的因素。当这些太阳活动朝向地球时，释放出的粒子有可能对人造卫星、输电网和其他通信基础设施造成故障。5日刊登在学术杂志《自然》上的这项研究成果，有可能帮助科学家加深对难以预测的太阳行为和活动的理解。",
                "grammar": "「〜なり得る」— 可能成为…。例：要因にもなり得る（也可能成为因素）。\n「〜恐れがある」— 有…的担心/危险。例：障害を引き起こす恐れがある（有可能造成故障）。\n「〜助けとなる」— 成为…的帮助。例：理解を深める助けとなる（成为加深理解的帮助）。",
                "vocab": [
                    ["蓄積", "ちくせき", "积蓄、积累"],
                    ["促進", "そくしん", "促进"],
                    ["人工衛星", "じんこうえいせい", "人造卫星"],
                    ["送電網", "そうでんもう", "输电网"],
                    ["障害", "しょうがい", "故障、障碍"],
                    ["掲載", "けいさい", "刊登、登载"]
                ]
            }
        ]
    },
    {
        "slug": "sanseitou-kamiya-gusaku",
        "title": "参政党の神谷代表、食料品の消費減税「天下の愚策」と批判 「一律減税でないと後押しにならない」",
        "subtitle": "from 時事通信",
        "paras": [
            {
                "ja": "参政党の神谷宗幣代表は6日、食料品の消費税減税について「天下の愚策だ」と批判した。「税率が複雑になり、手続きが増える。景気にマイナスになるのではないか」と指摘した。",
                "en": "Souhei Kamiya, leader of the Sanseito party, criticized the consumption tax cut on food products on the 6th, calling it \"a policy of folly under heaven.\" He pointed out that \"the tax rate will become complicated and procedures will increase. It may have a negative impact on the economy.\"",
                "literal": "参政党代表神谷宗币于6日就食品消费税减税批评说「是天下最愚蠢的政策」。他指出「税率会变得复杂，手续会增加。会不会对景气产生负面影响」。",
                "grammar": "「〜について、〜と批判した」— 就…批评说…。例：消費税減税について「天下の愚策だ」と批判した（就消费税减税批评说“是天下最愚蠢的政策”）。\n「〜のではないか」— 会不会…呢（委婉推测）。例：景気にマイナスになるのではないか（会不会对景气不利）。",
                "vocab": [
                    ["消費税", "しょうひぜい", "消费税"],
                    ["減税", "げんぜい", "减税"],
                    ["愚策", "ぐさく", "愚蠢的政策"],
                    ["批判", "ひはん", "批评、批判"],
                    ["税率", "ぜいりつ", "税率"],
                    ["景気", "けいき", "景气、经济状况"]
                ]
            },
            {
                "ja": "その上で「5％くらいの一律減税でないと経済の後押しにならない」と主張した。山口県下関市で記者団に語った。",
                "en": "Furthermore, he asserted that \"unless it is a uniform tax cut of around 5%, it will not boost the economy.\" He said this to reporters in Shimonoseki City, Yamaguchi Prefecture.",
                "literal": "在此基础上，他主张「如果不是5%左右的统一减税，就无法推动经济」。他在山口县下关市对记者团说了这番话。",
                "grammar": "「〜その上で」— 在此基础上、而且。例：その上で「一律減税でないと」と主張した（在此基础上主张“如果不是统一减税”）。\n「〜でないと〜ない」— 如果不…就不…。例：一律減税でないと後押しにならない（如果不是统一减税就无法推动）。\n「〜に語った」— 对…说了。例：記者団に語った（对记者团说了）。",
                "vocab": [
                    ["一律", "いちりつ", "一律、统一"],
                    ["後押し", "あとおし", "推动、助推"],
                    ["主張", "しゅちょう", "主张"],
                    ["記者団", "きしゃだん", "记者团"],
                    ["語る", "かたる", "说、讲述"]
                ]
            }
        ]
    },
    {
        "slug": "reiwa-inochi-no-tou-meishou",
        "title": "れいわ新選組が「いのちの党」に党名変更 “脱・山本太郎”へ 山本譲司新代表のもと臨時総会",
        "subtitle": "from FNNプライムオンライン",
        "paras": [
            {
                "ja": "れいわ新選組は6日、党名を「いのちの党」に変更すると発表した。れいわ新選組は、6日の臨時総会で綱領を改正し、臨時役員会で規約を改正し、党名変更に必要な手続きを行った。",
                "en": "Reiwa Shinsengumi announced on the 6th that it would change its party name to \"Inochi no To\" (Party of Life). At an extraordinary general meeting on the 6th, Reiwa Shinsengumi revised its party platform, and at an extraordinary executive meeting it revised its rules, completing the procedures necessary for the name change.",
                "literal": "令和新选组于6日宣布将党名改为「生命党」。令和新选组在6日的临时大会上修改了纲领，在临时干部会上修改了规章，办理了党名变更所需的各项手续。",
                "grammar": "「〜に変更すると発表した」— 宣布将变更为…。例：党名を「いのちの党」に変更すると発表した（宣布将党名变更为“生命党”）。\n「〜手続きを行った」— 办理了…手续。例：党名変更に必要な手続きを行った（办理了党名变更所需的手续）。",
                "vocab": [
                    ["党名", "とうめい", "党名"],
                    ["変更", "へんこう", "变更、更改"],
                    ["臨時総会", "りんじそうかい", "临时大会"],
                    ["綱領", "こうりょう", "纲领"],
                    ["規約", "きやく", "规章、章程"],
                    ["手続き", "てつづき", "手续、程序"]
                ]
            },
            {
                "ja": "新たな党名は「いのちの党」で、略称は「いのち」。今後、総務省に対し、党名変更の届け出を速やかに行う予定。新たなロゴなどは、8月下旬に記者会見を開催し発表するとしている。",
                "en": "The new party name is \"Inochi no To,\" with the abbreviation \"Inochi.\" Going forward, the party plans to promptly file a notification of the name change with the Ministry of Internal Affairs and Communications. It says that the new logo and other items will be announced at a press conference to be held in late August.",
                "literal": "新的党名是「生命党」，简称「生命」。今后，预定尽快向总务省办理党名变更的申报。新的标志等，将于8月下旬召开记者会公布。",
                "grammar": "「〜に対し、〜予定」— 向…，预定…。例：総務省に対し、届け出を行う予定（预定向总务省办理申报）。\n「〜としている」— 表示…、据称将…。例：発表するとしている（表示将公布）。",
                "vocab": [
                    ["略称", "りゃくしょう", "简称"],
                    ["総務省", "そうむしょう", "总务省"],
                    ["届け出", "とどけで", "申报、登记"],
                    ["速やか", "すみやか", "迅速、尽快"],
                    ["ロゴ", "ろご", "标志、标识"],
                    ["記者会見", "きしゃかいけん", "记者招待会"]
                ]
            },
            {
                "ja": "れいわ新選組は、山本太郎氏の代表辞任に伴い、7月31日に山本譲司衆院議員が新代表に選出されており、2019年の発足後、大きな転機を迎えることになった。",
                "en": "Reiwa Shinsengumi, following the resignation of Taro Yamamoto as party leader, elected House of Representatives member Joji Yamamoto as the new leader on July 31, and the party now faces a major turning point since its founding in 2019.",
                "literal": "令和新选组伴随山本太郎的代表辞职，于7月31日选出了众议院议员山本让司为新代表，自2019年成立以来，迎来了重大转折点。",
                "grammar": "「〜に伴い」— 伴随…。例：代表辞任に伴い（伴随代表辞职）。\n「〜に選出されており」— 已被选为…。例：新代表に選出されており（已被选为新代表）。\n「〜ことになった」— 变成了…、迎来…。例：大きな転機を迎えることになった（迎来了重大转折点）。",
                "vocab": [
                    ["辞任", "じにん", "辞职"],
                    ["衆院議員", "しゅういんぎいん", "众议院议员"],
                    ["選出", "せんしゅつ", "选出"],
                    ["発足", "ほっそく", "成立、发起"],
                    ["転機", "てんき", "转折点"],
                    ["迎える", "むかえる", "迎来、迎接"]
                ]
            }
        ]
    },
    {
        "slug": "mukikei-karikiyaku-4nin",
        "title": "無期刑の仮釈放、2025年は「わずか4人」 2024年は32人が獄中死 「終身刑化」の傾向続く",
        "subtitle": "from 弁護士ドットコムニュース",
        "paras": [
            {
                "ja": "無期懲役刑（無期拘禁刑）の受刑者のうち、2025年に仮釈放されたのは4人だったことが、法務省の最新の統計でわかった。2024年の1人からは増えたものの、依然として極めて低い水準にとどまっている。",
                "en": "According to the latest statistics from the Ministry of Justice, only four inmates serving life imprisonment (indeterminate imprisonment) were released on parole in 2025. Although this is an increase from one person in 2024, the number remains at an extremely low level.",
                "literal": "在无期徒刑（无期拘禁刑）的服刑人员中，2025年被假释的只有4人，这一点从法务省的最新统计中可以得知。虽然比2024年的1人有所增加，但仍停留在极低的水平。",
                "grammar": "「〜ことが、〜でわかった」— 从…得知…。例：統計でわかった（从统计中得知）。\n「〜ものの」— 虽然…但是…。例：増えたものの、依然として低い（虽然增加了，但仍然很低）。\n「〜にとどまっている」— 停留在…。例：低い水準にとどまっている（停留在低水平）。",
                "vocab": [
                    ["無期懲役", "むきちょうえき", "无期徒刑"],
                    ["受刑者", "じゅけいしゃ", "服刑人员"],
                    ["仮釈放", "かりしゃくほう", "假释"],
                    ["法務省", "ほうむしょう", "法务省"],
                    ["依然", "いぜん", "依然、仍然"],
                    ["水準", "すいじゅん", "水平、水准"]
                ]
            },
            {
                "ja": "刑法28条は、無期刑の受刑者について、刑の執行開始から10年を経過し、本人に罪を悔い改める「改悛の状」がある場合には、仮釈放できると定めている。ただし、2005年の法改正で有期刑の上限が20年から30年に引き上げられて以降、無期刑受刑者も実際には30年以上服役した後に仮釈放されるケースが一般的となっている。",
                "en": "Article 28 of the Penal Code stipulates that life-sentence inmates can be released on parole if 10 years have passed since the start of their sentence and they show \"signs of repentance.\" However, since the 2005 law revision raised the upper limit of fixed-term imprisonment from 20 to 30 years, it has become common for life-sentence inmates to actually serve more than 30 years before being paroled.",
                "literal": "刑法第28条规定，对于无期徒刑的服刑人员，从刑罚执行开始经过10年、本人有悔改之意的「改悔之状」的情况下，可以假释。但是，2005年法律修订将有期刑上限从20年提高到30年之后，无期徒刑服刑人员实际上也大多在服刑30年以上后才被假释，这种情况已变得普遍。",
                "grammar": "「〜と定めている」— 规定…。例：仮釈放できると定めている（规定可以假释）。\n「〜て以降」— …之后。例：引き上げられて以降（被提高之后）。\n「〜ケースが一般的となっている」— …的情况已变得普遍。例：30年以上服役した後に仮釈放されるケースが一般的となっている（服刑30年以上后被假释的情况已变得普遍）。",
                "vocab": [
                    ["刑法", "けいほう", "刑法"],
                    ["執行", "しっこう", "执行"],
                    ["改悛", "かいしゅん", "悔改"],
                    ["法改正", "ほうかいせい", "法律修订"],
                    ["上限", "じょうげん", "上限"],
                    ["服役", "ふくえき", "服刑、服役"]
                ]
            },
            {
                "ja": "無期刑の仮釈放者数は、2021年9人、2022年6人、2023年8人、2024年1人と推移しており、2025年の4人はこの5年間で2番目に少ない。2024年末時点で、全国の刑事施設に収容されている無期刑受刑者は1650人で、全受刑者の約5％を占めた。この年は32人が獄中で死亡しており、その数は仮釈放された受刑者を大きく上回る。",
                "en": "The number of life-sentence inmates paroled was nine in 2021, six in 2022, eight in 2023, and one in 2024; the four in 2025 were the second fewest in the past five years. As of the end of 2024, 1,650 life-sentence inmates were held in penal institutions nationwide, accounting for about 5% of all inmates. In that year, 32 inmates died in prison — a number far exceeding those who were paroled.",
                "literal": "无期徒刑的假释人数，2021年9人、2022年6人、2023年8人、2024年1人这样推移，2025年的4人是这5年中第二少的。截至2024年底，全国刑事设施收容的无期徒刑服刑人员为1650人，约占全部服刑人员的5%。这一年有32人在狱中死亡，这个数字远远超过被假释的服刑人员数。",
                "grammar": "「〜と推移しており」— 如此推移着。例：9人、6人…と推移しており（按9人、6人…推移）。\n「〜時点で」— 截至…时点。例：2024年末時点で（截至2024年底）。\n「〜を上回る」— 超过…。例：仮釈放された受刑者を大きく上回る（远远超过被假释的服刑人员）。",
                "vocab": [
                    ["推移", "すいい", "推移、变化"],
                    ["刑事施設", "けいじしせつ", "刑事设施、监狱"],
                    ["収容", "しゅうよう", "收容、关押"],
                    ["占める", "しめる", "占、占据"],
                    ["獄中", "ごくちゅう", "狱中"],
                    ["上回る", "うわまわる", "超过、超出"]
                ]
            }
        ]
    },
    {
        "slug": "shakaihosho-zaigen-5chouen",
        "title": "日本の社会保障、岐路に 消費減税で財源5兆円の穴 手当てする具体策見えず",
        "subtitle": "from 時事通信",
        "paras": [
            {
                "ja": "政府は食料品の消費税率を来年4月から1％に引き下げることを決めた。中・低所得者への1％相当分の給付も開始し、財政負担は年間で計約5兆円に上る見通しだ。消費税収は年金や医療などの社会保障費を支える重要財源だが、減収分を手当てする具体策はまだ見えない。深刻化する日本の社会保障は、岐路に立たされている。",
                "en": "The government has decided to lower the consumption tax rate on food products to 1% starting next April. It will also begin payments equivalent to 1% to middle- and low-income earners, and the fiscal burden is expected to total about 5 trillion yen per year. Consumption tax revenue is an important source of funds supporting social security expenditures such as pensions and medical care, but no concrete measures to cover the revenue shortfall are yet in sight. Japan's social security system, which is facing deepening problems, stands at a crossroads.",
                "literal": "政府决定将食品的消费税率从明年4月起降至1%。对中低收入者的相当于1%的给付也将开始，财政负担预计每年合计约5万亿日元。消费税收入是支撑养老金和医疗等社会保障费用的重要财源，但填补减收部分的具体对策还看不到。日益深刻化的日本社会保障，正站在岔路口上。",
                "grammar": "「〜ことを決めた」— 决定…。例：引き下げることを決めた（决定下调）。\n「〜見通しだ」— 预计…。例：約5兆円に上る見通しだ（预计达约5万亿日元）。\n「〜岐路に立たされている」— 正站在岔路口。例：社会保障は、岐路に立たされている（社会保障正站在岔路口）。",
                "vocab": [
                    ["引き下げる", "ひきさげる", "下调、降低"],
                    ["給付", "きゅうふ", "给付、发放"],
                    ["財政負担", "ざいせいふたん", "财政负担"],
                    ["社会保障", "しゃかいほしょう", "社会保障"],
                    ["財源", "ざいげん", "财源"],
                    ["岐路", "きろ", "岔路口、歧路"]
                ]
            },
            {
                "ja": "高市早苗首相は5日、「社会保障にも影響が出ないようにしっかりと対応する」と強調した。財源としては、外国為替資金特別会計（外為特会）の剰余金や日銀が利益の一部を国庫に納める納付金などの税外収入が挙がる。片山さつき財務相は同日、「さらなる歳入確保の取り組みをゼロベースで進める」と指摘した。",
                "en": "Prime Minister Sanae Takaichi emphasized on the 5th, \"We will respond thoroughly so that there is no impact on social security.\" As sources of funds, non-tax revenues such as surplus funds in the Foreign Exchange Fund Special Account and payments the Bank of Japan makes to the national treasury from a portion of its profits have been cited. Finance Minister Satsuki Katayama noted the same day, \"We will pursue further efforts to secure revenue from a zero base.\"",
                "literal": "高市早苗首相于5日强调「要妥善应对，使社会保障不受到影响」。作为财源，可举出外汇资金特别会计（外汇特会）的盈余、日银将利润的一部分缴纳国库的缴纳金等税外收入。财务相片山皋月当天指出「将以零基础推进进一步的确保岁入的举措」。",
                "grammar": "「〜ようにしっかりと対応する」— 妥善应对以…。例：影響が出ないように対応する（妥善应对使不受影响）。\n「〜としては、〜が挙がる」— 作为…，可举出…。例：財源としては、税外収入が挙がる（作为财源，可举出税外收入）。\n「〜をゼロベースで進める」— 以零基础推进…。例：歳入確保の取り組みをゼロベースで進める（以零基础推进确保岁入的举措）。",
                "vocab": [
                    ["強調", "きょうちょう", "强调"],
                    ["剰余金", "じょうよきん", "盈余资金"],
                    ["国庫", "こっこ", "国库"],
                    ["税外収入", "ぜいがいしゅうにゅう", "税外收入"],
                    ["歳入", "さいにゅう", "岁入、年度收入"],
                    ["取り組み", "とりくみ", "举措、努力"]
                ]
            },
            {
                "ja": "今回の減税と給付措置は、2029年度に本格導入する所得連動給付の「つなぎ」の位置付け。しかし、2年後に消費税率を元に戻せるのか懸念の声は強い。片山財務相は、財源具体化には来年度予算編成のめどが立つ今年12月までかかるとの見通しを示した。その上で、市場の動揺を抑えるため、「市場との対話を今まで以上に考えたい」と述べた。",
                "en": "This tax cut and the payment measures are positioned as a \"bridge\" to the income-linked benefit to be fully introduced in fiscal 2029. However, there are strong concerns about whether the consumption tax rate can be restored after two years. Finance Minister Katayama indicated that it will take until December of this year, when the framework for next fiscal year's budget compilation takes shape, to finalize the funding. On top of that, to calm market unrest, she said, \"I want to consider dialogue with the market more than ever.\"",
                "literal": "这次的减税和给付措施，被定位为2029年度正式引入的所得联动给付的「过渡衔接」。但是，2年后能否恢复消费税率，担忧的声音很强。片山财务相表示，财源具体化预计要到下年度预算编制眉目形成的今年12月为止。在此基础上，为了抑制市场动摇，她表示「想比以往更加考虑与市场的对话」。",
                "grammar": "「〜の位置付け」— 定位为…。例：「つなぎ」の位置付け（定位为过渡衔接）。\n「〜のか懸念の声は強い」— 能否…的担忧很强。例：元に戻せるのか懸念の声は強い（能否恢复的担忧很强）。\n「〜ため、〜」— 为了…，…。例：市場の動揺を抑えるため、述べた（为了抑制市场动摇而表示）。",
                "vocab": [
                    ["措置", "そち", "措施"],
                    ["本格導入", "ほんかくどうにゅう", "正式引入"],
                    ["つなぎ", "つなぎ", "过渡、衔接"],
                    ["懸念", "けねん", "担忧、忧虑"],
                    ["予算編成", "よさんへんせい", "预算编制"],
                    ["動揺", "どうよう", "动摇、波动"]
                ]
            }
        ]
    },
    {
        "slug": "shiroi-zarigani-tenji",
        "title": "白いザリガニ発見 遺伝的変異の可能性 親子が捕まえ岡山の科学館に寄贈 「赤青白」3色そろう",
        "subtitle": "from 山陽新聞デジタル",
        "paras": [
            {
                "ja": "岡山市北区伊島町の人と科学の未来館サイピアに、白色のアメリカザリガニが仲間入りした。同学南町の用水路で近所の親子が捕まえ、寄贈した。自然界では珍しい色だといい、同館では「赤青白の3色のザリガニがそろった。見比べて自然の神秘を感じてほしい」としている。",
                "en": "A white American crayfish has joined the collection at Sci-pia: The Museum of People and Science in Ijima-cho, Kita Ward, Okayama City. A parent and child from the neighborhood caught it in an irrigation canal in Gakunan-cho, Okayama City, and donated it. The color is said to be rare in nature, and the museum says, \"Now we have crayfish in three colors: red, blue, and white. We hope visitors will compare them and feel the mystery of nature.\"",
                "literal": "位于冈山市北区伊岛町的人与科学未来馆Sci-pia，迎来了白色美国小龙虾的加入。附近的一对亲子在学南町的灌溉水渠里抓到并捐赠了它。据说在自然界中是罕见的颜色，该馆表示「红色、蓝色、白色3种颜色的小龙虾凑齐了。希望大家对比观赏，感受大自然的神秘」。",
                "grammar": "「〜に仲間入りした」— 加入了…的行列。例：サイピアに仲間入りした（加入了Sci-pia的行列）。\n「〜だといい」— 据说…。例：自然界では珍しい色だといい（据说在自然界是罕见的颜色）。\n「〜てほしい」— 希望…。例：自然の神秘を感じてほしい（希望大家感受自然的神秘）。",
                "vocab": [
                    ["用水路", "ようすいろ", "灌溉水渠"],
                    ["寄贈", "きぞう", "捐赠"],
                    ["自然界", "しぜんかい", "自然界"],
                    ["珍しい", "めずらしい", "稀奇的、罕见的"],
                    ["神秘", "しんぴ", "神秘"],
                    ["見比べる", "みくらべる", "对比观看"]
                ]
            },
            {
                "ja": "白いザリガニは体長約5センチ。26日午前7時ごろ、学南町地区に住む保育園児の影山蓮ちゃん（5）が父の敦さん（48）と散歩中に用水路で発見した。その場で捕獲し、自宅で飼おうと持ち帰った。敦さんが調べたところ、珍しい個体ではないかと思い「ちゃんとした場所で飼育して、展示してもらいたい」と28日に2人でサイピアを訪れ、寄贈したという。",
                "en": "The white crayfish is about 5 cm long. Around 7 a.m. on the 26th, Ren Kageyama (5), a kindergarten child living in the Gakunan-cho area, discovered it in an irrigation canal while taking a walk with her father Atsushi (48). They caught it on the spot and took it home intending to keep it. After Atsushi researched it and thought it might be a rare specimen, the two visited Sci-pia on the 28th and donated it, asking, \"We want it raised in a proper place and displayed.\"",
                "literal": "白色小龙虾体长约5厘米。26日上午7点左右，住在学南町地区的幼儿园小朋友影山莲（5岁）和父亲敦（48岁）散步时在水渠里发现了它。当场捕获，带回家想自己饲养。敦调查后发现可能是稀有个体，心想「希望在正规的地方饲养并展示」，28日两人一起造访了Sci-pia并捐赠。",
                "grammar": "「〜ごろ」— …左右（时间）。例：午前7時ごろ（上午7点左右）。\n「〜たところ」— 一…发现…。例：調べたところ、珍しい個体ではないかと思い（一调查，觉得可能是稀有个体）。\n「〜てもらいたい」— 希望（对方）…。例：展示してもらいたい（希望对方展示）。",
                "vocab": [
                    ["体長", "たいちょう", "体长"],
                    ["保育園児", "ほいくえんじ", "幼儿园小朋友"],
                    ["散歩", "さんぽ", "散步"],
                    ["捕獲", "ほかく", "捕获"],
                    ["個体", "こたい", "个体"],
                    ["飼育", "しいく", "饲养"]
                ]
            },
            {
                "ja": "岡山大学術研究院の中田和義教授（保全生態学）によると、遺伝的な変異によって生まれつき体の色素が少ない可能性が高いという。「白色は目立つので捕食されやすく、自然界で見られるのは珍しい」と話す。市内の別の用水路では6月に青いザリガニが見つかっており、白と青の2匹は一緒にサイピア2階の水生生物展示スペースで飼育中だ。",
                "en": "According to Kazuyoshi Nakata, a professor of conservation ecology at Okayama University, it is highly likely that the crayfish was born with little body pigment due to a genetic mutation. \"White is conspicuous, making them easy prey, so it is rare to see them in nature,\" he says. A blue crayfish was found in another irrigation canal in the city in June, and the white and blue crayfish are currently being raised together in the aquatic life exhibition space on the second floor of Sci-pia.",
                "literal": "据冈山大学学术研究院的中田和义教授（保全生态学）称，由于遗传变异，天生体内色素较少的可能性很高。他说「白色很显眼，容易被捕食，在自然界中很少见」。市内的另一条水渠6月发现了蓝色小龙虾，白色和蓝色两只目前一起在Sci-pia二楼的水生生物展示区饲养中。",
                "grammar": "「〜によると、〜という」— 据…说，…。例：教授によると、可能性が高いという（据教授说，可能性很高）。\n「〜やすく」— 容易…。例：捕食されやすく（容易被捕食）。\n「〜飼育中だ」— 正在饲养中。例：展示スペースで飼育中だ（正在展示区饲养）。",
                "vocab": [
                    ["遺伝的", "いでんてき", "遗传性的"],
                    ["変異", "へんい", "变异"],
                    ["色素", "しきそ", "色素"],
                    ["目立つ", "めだつ", "显眼、醒目"],
                    ["捕食", "ほしょく", "捕食"],
                    ["水生生物", "すいせいせいぶつ", "水生生物"]
                ]
            }
        ]
    },
]

processed = []

for art in articles:
    slug = art['slug']
    title = art['title']
    print(f"\n{'='*60}")
    print(f"📰 {title}")
    print(f"   slug: {slug}")

    # 1. Build JSON
    reading = [{
        "id": slug,
        "title": title,
        "subtitle": art.get('subtitle', ''),
        "level": "中級",
        "length": len(art['paras']),
        "date": TODAY,
        "paragraphs": []
    }]

    for i, p in enumerate(art['paras']):
        print(f"   🔤 Tokenizing P{i+1}...")
        words = tokenize_text(p['ja'])
        reading[0]['paragraphs'].append({
            "id": f"p{i+1}",
            "ja": p['ja'],
            "en": p['en'],
            "literal": p['literal'],
            "grammar": p.get('grammar', ''),
            "vocab": p.get('vocab', []),
            "words": words,
            "audio": f"assets/audio/{slug}/p{i+1}.mp3"
        })

    # 2. Write JSON
    os.makedirs(f'{BASE}/assets/readings', exist_ok=True)
    with open(f'{BASE}/assets/readings/{slug}.json', 'w', encoding='utf-8') as f:
        json.dump(reading, f, ensure_ascii=False, indent=2)
    print(f"   ✅ JSON saved")

    # 3. Generate MP3s
    os.makedirs(f'{BASE}/assets/audio/{slug}', exist_ok=True)
    for i, p in enumerate(art['paras']):
        outpath = f'{BASE}/assets/audio/{slug}/p{i+1}.mp3'
        if gen_mp3(p['ja'], outpath):
            sz = os.path.getsize(outpath)
            print(f"   🔊 MP3 P{i+1} ({sz//1024}KB)")
        else:
            print(f"   ❌ MP3 P{i+1} FAILED")

    # 4. Blog post
    ja_text = '\n\n'.join([p['ja'] for p in art['paras'][:3]])
    post = f"""---
title: {title}
date: {TODAY} 11:30:00 +0900
categories: [ニュース]
tags: [ニュース]
---

{ja_text}

<div class=\"mt-4 p-3\" style=\"background:#f0f4f8;border-radius:8px;text-align:center;\">
  <a href=\"/asanews/reading-room/?read={slug}\" class=\"btn btn-danger\" style=\"color:#fff;padding:10px 24px;border-radius:6px;font-weight:bold;\">
    📖 読解ルームで詳しく読む
  </a>
</div>
"""
    os.makedirs(f'{BASE}/_posts', exist_ok=True)
    with open(f'{BASE}/_posts/{TODAY}-{slug}.md', 'w', encoding='utf-8') as f:
        f.write(post)
    print(f"   ✅ Blog post")

    processed.append(slug)

# ==================================================================
# UPDATE index.json
# ==================================================================
index_path = f'{BASE}/assets/readings/index.json'
existing_index = []
if os.path.exists(index_path):
    with open(index_path, 'r') as f:
        existing_index = json.load(f)

new_entries = []
for art in articles:
    new_entries.append({
        "id": art['slug'],
        "title": art['title'],
        "level": "中級",
        "length": len(art['paras']),
        "date": TODAY,
        "file": f"assets/readings/{art['slug']}.json"
    })

updated_index = new_entries + existing_index

with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(updated_index, f, ensure_ascii=False, indent=2)
print(f"\n✅ index.json: {len(updated_index)} articles total ({len(new_entries)} new)")

# ==================================================================
# UPDATE reading-room.js READING_LIST
# ==================================================================
js_path = f'{BASE}/assets/js/reading-room.js'

with open(js_path, 'r') as f:
    js = f.read()

js_list = []
for item in new_entries:
    escaped_title = item['title'].replace("'", "\\'")
    js_list.append(f"    {{\n      id: '{item['id']}',\n      title: '{escaped_title}',\n      kicker: '中級',\n      desc: '',\n      badge: '{item['length']}段落',\n      file: '/asanews/assets/readings/{item['id']}.json'\n    }}")

existing_ids = {a['id'] for a in new_entries}
existing_entries = []
for item in existing_index:
    if item['id'] not in existing_ids:
        escaped = item['title'].replace("'", "\\'")
        existing_entries.append(f"    {{\n      id: '{item['id']}',\n      title: '{escaped}',\n      kicker: '中級',\n      desc: '',\n      badge: '{item['length']}段落',\n      file: '/asanews/assets/readings/{item['id']}.json'\n    }}")

all_js_list = js_list + existing_entries
js_replace = "        const READING_LIST = [\n" + ",\n".join(all_js_list) + "\n    ];"

js_new = re.sub(
    r'const READING_LIST = \[.*?\];',
    js_replace,
    js,
    flags=re.DOTALL
)

with open(js_path, 'w') as f:
    f.write(js_new)
print(f"✅ reading-room.js READING_LIST updated")

# ==================================================================
# VERIFY
# ==================================================================
print(f"\n{'='*60}")
print(f"📋 VERIFICATION")
ok = 0
for slug in processed:
    jp = f'{BASE}/assets/readings/{slug}.json'
    pp = f'{BASE}/_posts/{TODAY}-{slug}.md'
    if os.path.exists(jp) and os.path.exists(pp):
        with open(jp) as f:
            d = json.load(f)
        pc = len(d[0]['paragraphs'])
        audio_ok = True
        for i in range(pc):
            ap = f'{BASE}/assets/audio/{slug}/p{i+1}.mp3'
            if not os.path.exists(ap):
                audio_ok = False
                break
        status = '✅' if audio_ok else '⚠️'
        print(f"  {status} {slug:40s} | {pc} paras")
        ok += 1
    else:
        print(f"  ❌ {slug} MISSING!")

print(f"\n🎉 {ok}/{len(processed)} articles processed successfully!")
print(f"{'='*60}")
