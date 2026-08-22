#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-23 (Sun) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-23'
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
        ['/home/horse/.local/bin/edge-tts', '--voice', 'ja-JP-NanamiNeural',
         '--text', text, '--write-media', outpath],
        capture_output=True, timeout=180)
    return os.path.exists(outpath) and os.path.getsize(outpath) > 1000


articles = []
articles += [
    {
        "slug": "kanto-jishin-shindo5jaku",
        "title": "関東で最大震度5弱の地震 津波なし 1都3県で観測",
        "subtitle": "from TBS NEWS DIG",
        "paras": [
            {
                "ja": "23日午前2時ごろ、茨城県、埼玉県、千葉県、東京都で最大震度5弱を観測する強い地震がありました。気象庁によりますと、震源地は茨城県南部で、震源の深さはおよそ70km、地震の規模を示すマグニチュードは5.9と推定されます。この地震による津波の心配はありません。",
                "en": "Around 2 a.m. on the 23rd, a strong earthquake with a maximum seismic intensity of lower 5 was observed in Ibaraki, Saitama, Chiba, and Tokyo prefectures. According to the Japan Meteorological Agency, the epicenter was in southern Ibaraki Prefecture, with a focal depth of about 70 km, and the magnitude indicating the scale of the quake is estimated at 5.9. There is no concern of a tsunami from this earthquake.",
                "literal": "23日凌晨2点左右，茨城县、埼玉县、千叶县、东京都观测到最大震度5弱（日本气象厅震度等级，相当于中国烈度约6度）的强地震。据气象厅称，震源在茨城县南部，震源深度约70公里，表示地震规模的震级推测为5.9。此次地震无需担心海啸。",
                "grammar": "「〜によりますと」— 根据…（新闻报道用语）。例：気象庁によりますと（据气象厅称）。\n「〜と推定されます」— 被推测为…。例：マグニチュードは5.9と推定されます（震级推测为5.9）。\n「〜の心配はありません」— 无需担心…。例：津波の心配はありません（无需担心海啸）。",
                "vocab": [["震度", "しんど", "震度（烈度）"], ["震源地", "しんげんち", "震中"], ["津波", "つなみ", "海啸"], ["マグニチュード", "まぐにちゅーど", "震级"], ["推定", "すいてい", "推测、推定"], ["観測", "かんそく", "观测"]]
            },
            {
                "ja": "最大震度5弱を観測したのは、茨城県の小美玉市、茨城古河市、龍ケ崎市などのほか、埼玉県の川口市、蕨市、戸田市、千葉県の浦安市、印西市、東京都の足立区です。震度4は関東の広い範囲で観測されました。また、長周期地震動の「階級2」を東京23区、千葉県北西部、埼玉県南部で観測しています。",
                "en": "Lower 5 intensity was observed in Omitama, Ibaraki-Koga, and Ryugasaki cities in Ibaraki Prefecture, as well as Kawaguchi, Warabi, and Toda cities in Saitama, Urayasu and Inzai cities in Chiba, and Adachi Ward in Tokyo. Intensity 4 was observed across a wide area of the Kanto region. In addition, long-period ground motion of \"class 2\" was observed in Tokyo's 23 wards, northwestern Chiba, and southern Saitama.",
                "literal": "观测到最大震度5弱的有茨城县的小美玉市、茨城古河市、龙崎市等，此外还有埼玉县的川口市、蕨市、户田市，千叶县的浦安市、印西市，东京都的足立区。震度4在关东广大地区被观测到。另外，在东京23区、千叶县西北部、埼玉县南部观测到了长周期地震动的「等级2」。",
                "grammar": "「〜のほか」— 除…之外。例：小美玉市などのほか（除小美玉市等之外）。\n「〜では…を観測しました」— 在…观测到了…。例：東京23区で観測しています（在东京23区观测到）。\n「〜また、」— 另外…（连接补充）。例：また、長周期地震動の「階級2」を…（另外，长周期地震动的「等级2」…）。",
                "vocab": [["長周期地震動", "ちょうしゅうきじしんどう", "长周期地震动"], ["階級", "かいきゅう", "等级"], ["広い範囲", "ひろいはんい", "广大范围"], ["震源", "しんげん", "震源"], ["深さ", "ふかさ", "深度"], ["規模", "きぼ", "规模"]]
            },
            {
                "ja": "これまでに9人がけがをしています。気象庁は、揺れが強かった地域では、1週間程度は最大震度5弱程度の揺れを伴う地震に注意するよう呼びかけています。地震のあとは、家具などが倒れてくる危険性があるため、高所の物を確認するなど、安全に十分注意してください。",
                "en": "So far, nine people have been injured. The Japan Meteorological Agency is urging people in areas where the shaking was strong to be cautious of earthquakes accompanied by shaking of around lower 5 on the intensity scale for about a week. After an earthquake, there is a risk of furniture and other items toppling over, so please check items in high places and take sufficient care for your safety.",
                "literal": "截至目前已有9人受伤。气象厅呼吁摇晃强烈的地区在约一周内注意伴随最大震度5弱左右摇晃的地震。地震之后，由于存在家具等倒下的危险性，请确认高处物品等，充分注意安全。",
                "grammar": "「〜程度」— …左右、…程度。例：1週間程度（约一周）。\n「〜よう呼びかけています」— 呼吁…。例：注意するよう呼びかけています（呼吁注意…）。\n「〜ため、」— 因为…。例：倒れてくる危険性があるため（因为有倒下的危险性）。",
                "vocab": [["けが", "けが", "受伤"], ["伴う", "ともなう", "伴随"], ["呼びかける", "よびかける", "呼吁"], ["家具", "かぐ", "家具"], ["危険性", "きけんせい", "危险性"], ["高所", "こうしょ", "高处"], ["安全", "あんぜん", "安全"]]
            },
        ]
    },
    {
        "slug": "syuin-hirei-sainragu-shiki",
        "title": "衆院比例に「サンラグ式」案浮上 小政党に議席配分しやすく",
        "subtitle": "from 西日本新聞",
        "paras": [
            {
                "ja": "衆院の選挙制度を巡り、比例代表の新たな議席配分方式「サンラグ式」の導入が検討材料になっています。現行の「ドント式」に比べて小政党に議席を配分しやすいのが特徴です。与党は秋の臨時国会で比例定数を45削減する法案の成立を目指しており、野党の反発を和らげる狙いも透けます。",
                "en": "Regarding the House of Representatives election system, the introduction of the \"Sainte-Laguë method,\" a new seat allocation formula for proportional representation, is being considered. Its characteristic is that it allocates seats to smaller parties more easily than the current \"d'Hondt method.\" The ruling parties aim to pass a bill in the autumn extraordinary Diet session to cut proportional seats by 45, and the aim of softening opposition parties' resistance is also visible.",
                "literal": "围绕众议院选举制度，比例代表新的议席分配方式「圣拉古式」的引进正成为讨论议题。其特征是与现行的「顿特式」相比更容易向小政党分配议席。执政党以在秋季临时国会通过削减比例定额45个的法案为目标，缓和在野党反对的意图也隐约可见。",
                "grammar": "「〜を巡り」— 围绕…。例：選挙制度を巡り（围绕选举制度）。\n「〜に比べて」— 与…相比。例：ドント式に比べて（与顿特式相比）。\n「〜ており」— …着（正式书面语）。例：成立を目指しており（以成立为目标）。",
                "vocab": [["衆院", "しゅういん", "众议院"], ["選挙制度", "せんきょせいど", "选举制度"], ["比例代表", "ひれいだいひょう", "比例代表制"], ["議席", "ぎせき", "议席"], ["配分", "はいぶん", "分配"], ["与党", "よとう", "执政党"], ["反発", "はんぱつ", "反对、反弹"]]
            },
            {
                "ja": "両方式の違いは、各政党の得票数を割る「数」にあります。ドント式は得票数を1、2、3…と自然数で順に割っていき、計算した数が大きい政党順に議席を振り分けます。一方のサンラグ式は1、3、5…と奇数で割るため、大政党の2、3議席目よりも中小政党の1、2議席目が上回りやすくなります。死票を減らして多様な民意を反映する効果が期待されています。",
                "en": "The difference between the two methods lies in the \"numbers\" by which each party's vote totals are divided. The d'Hondt method divides vote totals successively by natural numbers 1, 2, 3..., allocating seats to parties in order of the largest calculated figures. The Sainte-Laguë method, by contrast, divides by odd numbers 1, 3, 5..., so the 1st and 2nd seats of small and mid-sized parties tend to exceed the 2nd and 3rd seats of large parties. It is expected to reduce wasted votes and reflect diverse public opinion.",
                "literal": "两种方式的区别在于除以各政党得票数的「数」。顿特式用1、2、3…这样的自然数依次除得票数，按算出的数大的政党顺序分配议席。而圣拉古式用1、3、5…这样的奇数去除，因此中小政党的第1、2议席比大政党的第2、3议席更容易胜出。减少死票、反映多样民意的效果备受期待。",
                "grammar": "「〜にあります」— 在于…。例：違いは…にあります（区别在于…）。\n「〜ていき」— 依次…下去。例：順に割っていき（依次除下去）。\n「〜ため、」— 因为…。例：奇数で割るため（因为用奇数除）。",
                "vocab": [["得票数", "とくひょうすう", "得票数"], ["自然数", "しぜんすう", "自然数"], ["振り分ける", "ふりわける", "分配、分派"], ["奇数", "きすう", "奇数"], ["中小政党", "ちゅうしょうせいとう", "中小政党"], ["死票", "しひょう", "死票"], ["民意", "みんい", "民意"]]
            },
            {
                "ja": "新聞社の試算では、自民党が9議席減の58議席となり、減少幅が最大になりました。中規模政党の多くも議席を減らす一方、小政党では5党が議席を増やす結果となりました。自民党には不利になる方式ですが、定数削減を実現する上では「野党対策として有用」との見方もあります。",
                "en": "According to a newspaper's estimate, the Liberal Democratic Party would drop 9 seats to 58, the largest decrease. While many mid-sized parties would also lose seats, five smaller parties would gain seats. Although the method is disadvantageous to the LDP, there is also a view that it is \"useful as a measure against the opposition\" in achieving the seat reduction.",
                "literal": "据报社试算，自民党减少9个议席变为58席，减幅最大。中规模政党多数也减少议席，另一方面，小政党中有5个党增加议席。虽然是对自民党不利的方式，但在实现削减定额上也有「作为对付在野党的对策很有用」的看法。",
                "grammar": "「〜では」— 在…方面、根据…。例：試算では（据试算）。\n「〜一方、」— 另一方面…。例：議席を減らす一方（另一方面减少议席）。\n「〜との見方もあります」— 也有…的看法。例：有用との見方もあります（也有认为有用的看法）。",
                "vocab": [["試算", "しさん", "试算、估算"], ["減少幅", "げんしょうはば", "减少幅度"], ["中規模", "ちゅうきぼ", "中等规模"], ["不利", "ふり", "不利"], ["定数削減", "ていすうさくげん", "削减定额"], ["実現", "じつげん", "实现"], ["対策", "たいさく", "对策"]]
            },
            {
                "ja": "とはいえ、実際の選挙で小政党に有利に働くかは見通せず、野党側は態度を保留しています。そもそも野党の多くは選挙制度の抜本的な改革を主張しており、現行制度を維持したままの比例定数削減には否定的です。今後の与野党協議が焦点となります。",
                "en": "That said, whether it will work to the advantage of smaller parties in an actual election is unclear, and the opposition side is reserving its stance. In the first place, many opposition parties advocate fundamental reform of the election system and are negative about cutting proportional seats while maintaining the current system. The focus will be on future negotiations between the ruling and opposition parties.",
                "literal": "话虽如此，在实际选举中是否对小政党有利尚难预料，在野党方面保留态度。本来在野党多数主张选举制度的根本性改革，对维持现行制度的同时削减比例定额持否定态度。今后的朝野党首协商将成为焦点。",
                "grammar": "「〜とはいえ」— 话虽如此、虽说…。例：とはいえ、実際の選挙では（话虽如此，在实际选举中）。\n「〜たまま」— 维持…的状态。例：維持したままの（在维持…的状态下）。\n「〜が焦点となります」— …将成为焦点。例：協議が焦点となります（协商将成为焦点）。",
                "vocab": [["有利", "ゆうり", "有利"], ["態度", "たいど", "态度"], ["保留", "ほりゅう", "保留"], ["抜本的", "ばっぽんてき", "根本性的"], ["改革", "かいかく", "改革"], ["維持", "いじ", "维持"], ["焦点", "しょうてん", "焦点"]]
            },
        ]
    },
    {
        "slug": "tokyoeki-douro-ana-gouu",
        "title": "東京駅近くで道路に穴 掘削現場に水流れ込む 関東南部で豪雨",
        "subtitle": "from 毎日新聞",
        "paras": [
            {
                "ja": "暖かく湿った空気などの影響で大気の状態が不安定となり、関東地方南部では22日午後に猛烈な雨が降りました。東京都内では豊島区や板橋区、北区で「記録的短時間大雨情報」が発表され、いずれも1時間に約100～120ミリの雨が降ったとみられます。",
                "en": "Due to the influence of warm, humid air and other factors, atmospheric conditions became unstable, and torrential rain fell in the southern Kanto region on the afternoon of the 22nd. In Tokyo, \"record-short-term heavy rain information\" was issued for Toshima, Itabashi, and Kita wards, and about 100 to 120 mm of rain is believed to have fallen per hour in each.",
                "literal": "受温暖潮湿空气等的影响大气状态变得不稳定，关东地区南部22日下午降下猛烈暴雨。东京都内丰岛区、板桥区、北区发布了「创纪录短时间大雨信息」，各地被认为1小时降了约100～120毫米的雨。",
                "grammar": "「〜により」— 由于…。例：暖かく湿った空気などの影響で（由于温暖潮湿空气等的影响）。\n「〜とみられます」— 被认为…。例：雨が降ったとみられます（被认为下了雨）。\n「〜いずれも」— 无论哪个都…。例：いずれも1時間に（无论哪个都是每小时…）。",
                "vocab": [["湿った", "しめった", "潮湿的"], ["大気", "たいき", "大气"], ["不安定", "ふあんてい", "不稳定"], ["猛烈", "もうれつ", "猛烈"], ["記録的", "きろくてき", "创纪录的"], ["大雨", "おおあめ", "大雨"]]
            },
            {
                "ja": "警視庁によると、北区の区道では「冠水した道路に入って車が動かなくなった」と運転手から110番がありました。男性は自力で脱出し、無事でした。JR東京駅近くでは「掘削工事中に雨水が入ってきて道路が陥没しそうだ」と工事関係者から110番があり、警察官が駆け付けると、道路に穴が開いていました。けが人はいませんでした。",
                "en": "According to the Tokyo Metropolitan Police, in a ward road in Kita Ward there was a 110 call from a driver saying, \"I entered a flooded road and my car stopped moving.\" The man escaped on his own and was safe. Near JR Tokyo Station, a construction worker called 110 saying \"rainwater is coming into an excavation site and the road looks about to collapse.\" When police officers rushed there, a hole had opened in the road. There were no injuries.",
                "literal": "据警视厅称，在北区的区道上，有司机拨打110称「进入积水的道路后车子动不了了」。男子自行脱出，平安无事。JR东京站附近，有施工人员拨打110称「挖掘施工中雨水流入，道路似乎要塌陷」。警察赶到后发现道路开了一个洞。没有受伤者。",
                "grammar": "「〜によると」— 根据…。例：警視庁によると（据警视厅称）。\n「〜そうだ」— 好像要…（样态）。例：陥没しそうだ（好像要塌陷）。\n「〜駆け付けると」— 赶到一看…。例：駆け付けると、穴が開いていました（赶到后发现开了洞）。",
                "vocab": [["警視庁", "けいしちょう", "警视厅"], ["冠水", "かんすい", "积水"], ["自力", "じりょく", "自力"], ["脱出", "だっしゅつ", "脱出、逃出"], ["掘削", "くっさく", "挖掘"], ["陥没", "かんぼつ", "塌陷"], ["けが人", "けがにん", "受伤者"]]
            },
            {
                "ja": "雨雲は南に抜けましたが、気象庁は低い土地や地下施設への浸水、河川の増水や氾濫に警戒するよう呼びかけています。大雨のあとは、道路の冠水やがけ崩れなどにも十分注意が必要です。",
                "en": "The rain clouds have moved south, but the Japan Meteorological Agency is urging caution against flooding of low-lying land and underground facilities, and rising and overflowing rivers. After heavy rain, sufficient caution is also needed against road flooding and landslides.",
                "literal": "雨云虽然已向南方移出，但气象厅呼吁警戒低洼地和地下设施的浸水、河川的涨水和泛滥。大雨过后，也需要充分注意道路积水和塌方等。",
                "grammar": "「〜が、」— 虽然…但是…。例：雨雲は南に抜けましたが（雨云虽已移向南方）。\n「〜への」— 对…的。例：地下施設への浸水（对地下设施的浸水）。\n「〜に警戒するよう呼びかけています」— 呼吁警惕…。例：氾濫に警戒するよう呼びかけています（呼吁警惕泛滥）。",
                "vocab": [["雨雲", "あまぐも", "雨云"], ["浸水", "しんすい", "浸水"], ["河川", "かせん", "河川"], ["増水", "ぞうすい", "涨水"], ["氾濫", "はんらん", "泛滥"], ["がけ崩れ", "がけくずれ", "塌方、崖崩"]]
            },
        ]
    },
    {
        "slug": "nogizaka-rakurai-nyuujou-syakai",
        "title": "乃木坂46 落雷で避難の客の入場前に開始 公式サイトで謝罪",
        "subtitle": "from スポニチアネックス",
        "paras": [
            {
                "ja": "アイドルグループ「乃木坂46」は22日、東京・明治神宮野球場で開催した全国ツアーで、落雷により一時的に入場を制限した際、入場再開後に周辺施設へ一時避難した一部の観客の入場が終えていない状況で、公演を開始したことを公式サイトで謝罪しました。",
                "en": "The idol group Nogizaka46 apologized on its official website on the 22nd that, during its national tour held at Meiji Jingu Stadium in Tokyo, when entry was temporarily restricted due to lightning, the performance was started while some spectators who had taken temporary refuge at surrounding facilities had not yet finished re-entering after entry resumed.",
                "literal": "偶像组合「乃木坂46」22日在东京・明治神宫棒球场举办的全国巡演中，因落雷暂时限制入场时，在入场重新开放后，部分到周边设施临时避难的观众尚未完成入场的情况下就开始了公演，官方网站对此道歉。",
                "grammar": "「〜により」— 由于…。例：落雷により（由于落雷）。\n「〜際」— …的时候。例：入場を制限した際（限制入场时）。\n「〜ない状況で」— 在尚未…的情况下。例：終えていない状況で（在尚未完成的情况下）。",
                "vocab": [["アイドル", "あいどる", "偶像"], ["全国ツアー", "ぜんこくつあー", "全国巡演"], ["落雷", "らくらい", "落雷"], ["制限", "せいげん", "限制"], ["一時避難", "いちじひなん", "临时避难"], ["観客", "かんきゃく", "观众"], ["謝罪", "しゃざい", "道歉"]]
            },
            {
                "ja": "公式サイトは「入場時間中に落雷の危険が予想されたため、会場の規定に則り、ご来場中のお客様には周辺施設への一時避難をご案内いたしました」と説明しました。その上で「避難先から会場へ戻られた一部のお客様が入場を終えていない状況で、公演を開始いたしました」と明かし、スタッフ間で状況が適切に共有されないまま開演を判断したことによる不手際だったと認めました。",
                "en": "The official website explained, \"Because the danger of lightning was anticipated during the entry period, in accordance with venue regulations, we directed guests present to take temporary refuge at surrounding facilities.\" It then revealed that \"the performance was started while some guests who had returned from the refuge had not finished entering,\" admitting it was a blunder caused by deciding to begin the show without the situation being properly shared among staff.",
                "literal": "官方网站说明「由于入场时间内预料到落雷危险，按照会场规定，已引导到场内的顾客到周边设施临时避难」。在此基础上坦承「从避难处返回会场的一部分顾客尚未完成入场时就开始了公演」，并承认这是工作人员之间未适当共享状况就判断开演的失误。",
                "grammar": "「〜に則り」— 按照、依据…。例：会場の規定に則り（按照会场规定）。\n「〜ないまま」— 在未…的状态下。例：共有されないまま（在未共享的状态下）。\n「〜によるもの」— 由…造成的。例：不手際だったと認めました（承认是由此造成的失误）。",
                "vocab": [["危険", "きけん", "危险"], ["予想", "よそう", "预料"], ["規定", "きてい", "规定"], ["案内", "あんない", "引导、通知"], ["明かす", "あかす", "坦白、揭示"], ["適切", "てきせつ", "适当"], ["不手際", "ふてぎわ", "失误、处理不当"]]
            },
            {
                "ja": "グループは「本公演を楽しみにご来場いただいた皆様に、多大なるご迷惑をおかけしましたことを、心より深くお詫び申し上げます」と謝罪するとともに、「今回の事態を重く受け止め、情報共有と開演判断の手順を見直し、再発防止を徹底してまいります」としました。また、荒天のため来場を取りやめた人のうち、未使用のチケットの払い戻しも行うとしています。",
                "en": "The group apologized, \"We sincerely and deeply apologize for the great inconvenience caused to everyone who came looking forward to this performance,\" and added, \"We will take this situation seriously, review the procedures for information sharing and the decision to begin the show, and thoroughly prevent a recurrence.\" It also said it will refund unused tickets for those who canceled their visit due to the stormy weather.",
                "literal": "组合在道歉「向期待本公演莅临的各位致以衷心的深深歉意」的同时表示「将严肃对待此次事态，重新审视信息共享和开演判断的流程，彻底防止再次发生」。另外，因暴风雨天气而取消到场的观众中，未使用门票也将予以退款。",
                "grammar": "「〜とともに」— 在…的同时。例：謝罪するとともに（在道歉的同时）。\n「〜を重く受け止め」— 严肃对待…。例：事態を重く受け止め（严肃对待事态）。\n「〜としています」— 表示…（计划/方针）。例：払い戻しも行うとしています（表示将进行退款）。",
                "vocab": [["多大", "ただい", "巨大的"], ["迷惑", "めいわく", "麻烦、困扰"], ["お詫び", "おわび", "道歉"], ["見直す", "みなおす", "重新审视"], ["再発防止", "さいはつぼうし", "防止再次发生"], ["荒天", "こうてん", "暴风雨天气"], ["払い戻し", "はらいもどし", "退款"]]
            },
        ]
    },
    {
        "slug": "fujisan-okizari-7sai",
        "title": "富士山で7歳男の子を置き去りにした父親 警察が厳しく注意",
        "subtitle": "from 静岡放送（SBS）",
        "paras": [
            {
                "ja": "8月20日、富士山で父親に置き去りにされた7歳の男の子が警察に救助された事案で、父親はもう1人の息子が1人で先へ進んでしまったため、ぐずった男の子を置いて登山を続けたことが分かりました。",
                "en": "In an incident on August 20 in which a 7-year-old boy left behind by his father on Mount Fuji was rescued by police, it has been learned that the father continued climbing, leaving the whining boy behind, because his other son had gone ahead alone.",
                "literal": "8月20日，在富士山上被父亲遗弃的7岁男孩被警察救助的案件中，据悉父亲是因为另一个儿子一个人先往前走了，所以丢下闹脾气的男孩继续登山。",
                "grammar": "「〜てしまった」— …了（表示已完成/遗憾）。例：先へ進んでしまった（先走了）。\n「〜ため、」— 因为…。例：先へ進んでしまったため（因为先走了）。\n「〜ことが分かりました」— 得知…。例：登山を続けたことが分かりました（得知继续登山）。",
                "vocab": [["置き去り", "おきざり", "丢弃、遗弃"], ["救助", "きゅうじょ", "救助"], ["事案", "じあん", "案件、事件"], ["ぐずる", "ぐずる", "闹脾气、磨蹭"], ["登山", "とざん", "登山"], ["続ける", "つづける", "继续"]]
            },
            {
                "ja": "20日午前、富士山6合目の山小屋付近で「子どもが1人で置き去りになっている」と通報があり、小学2年生の7歳の男の子が警察に救助されました。男の子は、愛知県名古屋市から父親と兄と3人で登山に訪れていて、けがはありませんでした。",
                "en": "On the morning of the 20th, a report came in near a mountain hut at the 6th station of Mount Fuji that \"a child has been left alone,\" and the 7-year-old boy, a second grader in elementary school, was rescued by police. The boy had come climbing with his father and older brother, three of them from Nagoya City, Aichi Prefecture, and was not injured.",
                "literal": "20日上午，在富士山6合目的山间小屋附近接到「有孩子一个人被丢下」的报警，小学二年级的7岁男孩被警察救助。男孩与父亲和哥哥三人从爱知县名古屋市前来登山，没有受伤。",
                "grammar": "「〜付近で」— 在…附近。例：山小屋付近で（在山间小屋附近）。\n「〜と通報がありました」— 接到了…的报警。例：置き去りになっていると通報がありました（接到了「被丢下」的报警）。\n「〜ていて」— …着（状态）。例：登山に訪れていて（前来登山）。",
                "vocab": [["山小屋", "やまごや", "山间小屋"], ["通報", "つうほう", "报警、通报"], ["小学2年生", "しょうがくにねんせい", "小学二年级"], ["訪れる", "おとずれる", "到访"], ["けが", "けが", "受伤"], ["1人で", "ひとりで", "独自"]]
            },
            {
                "ja": "警察によりますと、48歳の父親は、男の子が「疲れた」などとぐずり、兄が1人で先に進んでしまったため、男の子に「ここで8時間くらい待っていろ」などと伝え、登山を続けたということです。当時、富士山の6合目では雨が降っていて霧も発生しており、山小屋の関係者が男の子を見守っていました。",
                "en": "According to police, the 48-year-old father told the boy, who was whining saying \"I'm tired\" and such, to \"wait here for about eight hours\" and continued climbing, because the older brother had gone ahead alone. At the time, it was raining at the 6th station of Mount Fuji and fog had also formed, and people at the mountain hut were watching over the boy.",
                "literal": "据警方称，48岁的父亲因男孩说「累了」等闹脾气，且哥哥一个人先往前走了，便对男孩说「在这里等8个小时左右」等，然后继续登山。当时富士山6合目下着雨，还起了雾，山间小屋的相关人员一直守望着男孩。",
                "grammar": "「〜によりますと」— 根据…。例：警察によりますと（据警方称）。\n「〜ということです」— 据说…。例：登山を続けたということです（据说继续登山了）。\n「〜ていました」— 一直…（持续状态）。例：見守っていました（一直守护着）。",
                "vocab": [["疲れる", "つかれる", "疲劳、累"], ["伝える", "つたえる", "转告、传达"], ["霧", "きり", "雾"], ["発生", "はっせい", "发生"], ["関係者", "かんけいしゃ", "相关人员"], ["見守る", "みまもる", "守护、照看"]]
            },
            {
                "ja": "警察は男の子を救助したあと、8合目付近まで登っていた父親に電話で連絡しました。警察は父親に「子どもを置いていくなんてありえません」と厳しく注意しました。父親は「軽率な行動でした。申し訳ありません」と反省しているということです。",
                "en": "After rescuing the boy, police contacted the father, who had climbed to around the 8th station, by phone. The police sternly admonished the father, saying \"Leaving a child behind is absolutely unthinkable.\" The father is said to be reflecting, saying \"It was a reckless act. I am truly sorry.\"",
                "literal": "警察救助男孩之后，用电话联系了已登上8合目附近的父亲。警察严厉告诫父亲「丢下孩子这种事绝不可能发生」。据说父亲正在反省「是轻率的行动。非常抱歉」。",
                "grammar": "「〜たあと」— …之后。例：救助したあと（救助之后）。\n「〜なんてありえません」— …绝不可能。例：置いていくなんてありえません（丢下孩子绝不可能）。\n「〜と厳しく注意しました」— 严厉告诫…。例：厳しく注意しました（严厉告诫）。",
                "vocab": [["連絡", "れんらく", "联系"], ["厳しい", "きびしい", "严厉的"], ["注意", "ちゅうい", "告诫、提醒"], ["軽率", "けいそつ", "轻率"], ["行動", "こうどう", "行动"], ["反省", "はんせい", "反省"]]
            },
        ]
    },
]

# ==================================================================
# PROCESS
# ==================================================================
processed = []
for art in articles:
    slug = art['slug']
    title = art['title']
    print(f"\n{'='*60}")
    print(f"📰 {title}")
    print(f"   slug: {slug}")

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

    os.makedirs(f'{BASE}/assets/readings', exist_ok=True)
    with open(f'{BASE}/assets/readings/{slug}.json', 'w', encoding='utf-8') as f:
        json.dump(reading, f, ensure_ascii=False, indent=2)
    print(f"   ✅ JSON saved")

    os.makedirs(f'{BASE}/assets/audio/{slug}', exist_ok=True)
    for i, p in enumerate(art['paras']):
        outpath = f'{BASE}/assets/audio/{slug}/p{i+1}.mp3'
        if gen_mp3(p['ja'], outpath):
            sz = os.path.getsize(outpath)
            print(f"   🔊 MP3 P{i+1} ({sz//1024}KB)")
        else:
            print(f"   ❌ MP3 P{i+1} FAILED")

    ja_text = '\n\n'.join([p['ja'] for p in art['paras']])
    post = f"""---
title: {title}
date: {TODAY} 11:30:00 +0900
categories: [ニュース]
tags: [ニュース]
---

{ja_text}

<div class="mt-4 p-3" style="background:#f0f4f8;border-radius:8px;text-align:center;">
  <a href="/asanews/reading-room/?read={slug}" class="btn btn-danger" style="color:#fff;padding:10px 24px;border-radius:6px;font-weight:bold;">
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
        if audio_ok:
            ok += 1
            print(f"   ✅ {slug}: {pc} paragraphs, audio OK")
        else:
            print(f"   ⚠️ {slug}: audio missing")
print(f"\n{ok}/{len(processed)} articles verified")