#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-06 (Thu) Edition"""
import json, os, subprocess, re, time
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-06'
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
# TODAY'S ARTICLES — 2026-08-06
# ==================================================================
articles = []
articles += [
    {
        "slug": "taifuu13-okinawa-sekken",
        "title": "台風13号、7日昼過ぎに沖縄本島へ最接近 暴風や高波に厳重警戒",
        "subtitle": "from tenki.jp",
        "paras": [
            {
                "ja": "大型で強い台風13号は、6日午前5時には南大東島の東約350キロの海上にあり、1時間に約20キロの速さで西北西に進んでいます。中心付近の最大風速は40メートル、最大瞬間風速は60メートルと、猛烈な風が吹いています。台風は強い勢力を保ったまま、6日夜遅くに大東島地方へ、7日昼過ぎには沖縄本島地方に最接近する見込みです。",
                "en": "Large and powerful Typhoon No. 13 was over the sea about 350 km east of Minami-Daito Island at 5 a.m. on the 6th, moving west-northwest at about 20 km per hour. With a maximum wind speed of 40 m/s near the center and gusts up to 60 m/s, ferocious winds are blowing. The typhoon is expected to make its closest approach to the Daito Islands late on the night of the 6th, and to the main island of Okinawa after noon on the 7th, while maintaining its strength.",
                "literal": "大型且强劲的台风13号，6日上午5点位于南大东岛以东约350公里的海面上，以每小时约20公里的速度向西北偏西方向前进。中心附近最大风速40米，最大瞬间风速60米，刮着猛烈的风。台风在保持强劲势力的同时，预计6日深夜接近大东岛地区，7日下午过后来到冲绳本岛地区附近（最接近）。",
                "grammar": "「〜にあり、〜進んでいます」— 位于…、正在…前进（并列）。例：海上にあり、西北西に進んでいます（位于海面上，正向西北偏西前进）。\n「〜と、〜が吹いています」— 与…并列，正刮着…。例：最大瞬間風速60メートルと、猛烈な風が吹いています（最大瞬间风速60米，正刮着猛烈的风）。\n「〜見込みです」— 预计…。例：最接近する見込みです（预计最接近）。",
                "vocab": [
                    ["台風", "たいふう", "台风"],
                    ["最接近", "さいせっきん", "最接近"],
                    ["最大風速", "さいだいふうそく", "最大风速"],
                    ["猛烈", "もうれつ", "猛烈、凶猛"],
                    ["勢力", "せいりょく", "势力、强度"],
                    ["見込み", "みこみ", "预计、预料"]
                ]
            },
            {
                "ja": "台風は8日にかけても強い勢力を維持したまま沖縄に接近するため、速度が遅くなるぶん影響が長引きそうです。沖縄と奄美では9日ごろにかけて、うねりを伴った高波と暴風に厳重に警戒してください。7日から8日にかけては土砂災害にも注意が必要で、沖縄では7日に高潮への厳重な警戒も呼びかけられています。",
                "en": "The typhoon will continue approaching Okinawa through the 8th while maintaining its strength, so the impact is likely to last longer because its speed will slow down. In Okinawa and Amami, be on high alert through around the 9th for high waves with swells and violent winds. From the 7th to the 8th, caution is also needed for sediment disasters, and on the 7th Okinawa is also being urged to be on high alert for storm surges.",
                "literal": "台风到8日为止也会在维持强劲势力的同时接近冲绳，因此由于速度变慢的这部分，影响似乎会拖长。冲绳和奄美到9日前后，请对伴随涌浪的巨浪和暴风严加警戒。7日到8日期间也需要警惕泥沙灾害，冲绳7日也被呼吁要严加警戒风暴潮。",
                "grammar": "「〜にかけても」— 一直到…为止也。例：8日にかけても接近する（到8日为止也会接近）。\n「〜ぶん」— …的那部分、相应地。例：速度が遅くなるぶん影響が長引く（速度变慢的部分影响会拖长）。\n「〜に警戒してください」— 请警戒…。例：高波と暴風に厳重に警戒してください（请严加警戒巨浪和暴风）。",
                "vocab": [
                    ["維持", "いじ", "维持"],
                    ["長引く", "ながびく", "拖长、拖延"],
                    ["うねり", "うねり", "涌浪"],
                    ["高波", "たかなみ", "巨浪、大浪"],
                    ["土砂災害", "どしゃさいがい", "泥沙灾害、塌方"],
                    ["高潮", "たかしお", "风暴潮、涨潮"]
                ]
            },
            {
                "ja": "気象庁は、明るいうちに頑丈な建物へ移動し、食料や水を確保しておくよう呼びかけています。一部の住家が倒壊するおそれもあるほどの猛烈な風が吹く予想で、停電に備えて懐中電灯の準備やモバイルバッテリーの充電をしておくと良いでしょう。",
                "en": "The Japan Meteorological Agency is urging people to move to sturdy buildings while it is still light and to secure food and water in advance. Winds ferocious enough to possibly topple some houses are forecast, so it would be good to prepare flashlights and charge mobile batteries in case of power outages.",
                "literal": "气象厅呼吁在还亮着的时候转移到坚固的建筑物，并提前确保食物和水。预计会刮猛烈到部分住宅有倒塌危险的强风，为停电做好准备，事先准备好手电筒、给充电宝充满电比较好。",
                "grammar": "「〜おそれがある」— 有…的危险/可能。例：住家が倒壊するおそれもある（住宅也有倒塌的危险）。\n"+"「〜に備えて」— 为…做准备。例：停電に備えて準備をする（为停电做准备）。\n「〜ておくと良い」— 事先…比较好。例：充電をしておくと良いでしょう（事先充好电比较好）。",
                "vocab": [
                    ["頑丈", "がんじょう", "坚固、结实"],
                    ["確保", "かくほ", "确保、保证"],
                    ["倒壊", "とうかい", "倒塌"],
                    ["停電", "ていでん", "停电"],
                    ["懐中電灯", "かいちゅうでんとう", "手电筒"],
                    ["充電", "じゅうでん", "充电"]
                ]
            }
        ]
    },
    {
        "slug": "shokuhin-zei-1-paasento",
        "title": "飲食料品消費税1％へ、外食に「割高感」も 農家にも打撃の恐れ 政府、対策を検討",
        "subtitle": "from 産経新聞",
        "paras": [
            {
                "ja": "飲食料品の消費税率が来年4月から2年間、8％から1％に下がります。消費者には買い物の際に値段が下がる恩恵がありますが、一部の事業者には打撃となりかねません。外食産業は税率10％のまま維持され、1％となる弁当や総菜などに客足が流れる恐れがあります。",
                "en": "The consumption tax rate on food and beverages will drop from 8% to 1% for two years starting next April. While consumers benefit from lower prices when shopping, it could be a blow to some businesses. The restaurant industry will remain at the 10% rate, and there is a risk that customers will drift toward bento boxes and prepared foods, which will be taxed at 1%.",
                "literal": "饮食类商品的消费税税率从明年4月起两年内，从8%降至1%。消费者在购物时虽然享有价格下降的恩惠，但对一部分经营者来说可能成为打击。餐饮产业的税率维持10%不变，客人可能会流向税率为1%的便当和熟食等。",
                "grammar": "「〜から〜に下がります」— 从…降到…。例：8％から1％に下がります（从8%降到1%）。\n「〜かねません」— 有可能…（负面）。例：打撃となりかねません（有可能成为打击）。\n「〜恐れがあります」— 有…的担心/风险。例：客足が流れる恐れがあります（客人有流失的风险）。",
                "vocab": [
                    ["飲食料品", "いんしょくりょうひん", "饮食食品"],
                    ["消費税", "しょうひぜい", "消费税"],
                    ["恩恵", "おんけい", "恩惠、好处"],
                    ["事業者", "じぎょうしゃ", "经营者、企业"],
                    ["外食産業", "がいしょくさんぎょう", "餐饮产业"],
                    ["客足", "きゃくあし", "客流、客人光顾"]
                ]
            },
            {
                "ja": "外食大手ゼンショーホールディングスの小川洋平社長は「これほどリスクの高い判断が強行されたことは遺憾だ。大義なき決断だ」と批判しました。外食各社は、税率が1％となるテイクアウトや宅配の需要拡大を見込んで、取り組みを強化しています。一方、農業では、売上高が年間1000万円以下で消費税の納税義務を免除されている事業者の「益税」が減少し、収益が圧迫される可能性があります。",
                "en": "Yohei Ogawa, president of major restaurant operator Zensho Holdings, criticized the move, saying, \"It is regrettable that such a high-risk decision was forced through. It is a decision without justification.\" Restaurant companies are strengthening their efforts in anticipation of growing demand for takeout and delivery, which will be taxed at 1%. Meanwhile, in agriculture, the \"benefit tax\" of operators exempted from consumption tax payment obligations — those with annual sales of 10 million yen or less — will shrink, potentially squeezing their profits.",
                "literal": "餐饮巨头善商控股的小川洋平社长批评说「如此高风险的决定被强行推进令人遗憾。这是没有大义的决定」。各家餐饮公司看好税率为1%的外带和外卖需求扩大，正在加强举措。另一方面，在农业方面，年销售额1000万日元以下、被免除消费税纳税义务的经营者的「益税」将减少，收益有可能受到挤压。",
                "grammar": "「〜と批判しました」— 批评说…。例：大義なき決断だと批判しました（批评说是没有大义的决定）。\n「〜を見込んで」— 预期、看好…。例：需要拡大を見込んで（看好需求扩大）。\n「〜可能性があります」— 有…的可能性。例：収益が圧迫される可能性があります（收益有可能受到挤压）。",
                "vocab": [
                    ["大手", "おおて", "大型企业、巨头"],
                    ["強行", "きょうこう", "强行"],
                    ["遺憾", "いかん", "遗憾"],
                    ["大義", "たいぎ", "大义、正当理由"],
                    ["テイクアウト", "ていくあうと", "外带、打包"],
                    ["圧迫", "あっぱく", "压迫、挤压"]
                ]
            },
            {
                "ja": "政府は今後、外食産業や農家の支援を検討する方針です。外食産業向けには、新型コロナ禍で実施した「GoToイート」を参考にする可能性があります。農業団体は、中小農家が簡易な手続きで補填を受けられるよう検討することを求めており、関係者は議論の行方を注視しています。",
                "en": "The government plans to consider support for the restaurant industry and farmers going forward. For the restaurant industry, it may draw on \"GoTo Eat,\" the demand-stimulus program implemented during the COVID-19 pandemic. Agricultural organizations are asking the government to consider allowing small and medium-sized farmers to receive compensation through simple procedures, and stakeholders are closely watching how the discussions unfold.",
                "literal": "政府今后计划探讨对餐饮产业和农户的支援。面向餐饮产业，有可能参考新冠疫情期间实施的「GoTo Eat」政策。农业团体要求探讨让中小农户能通过简便手续获得填补，相关人士正在密切关注讨论的走向。",
                "grammar": "「〜方針です」— 方针是…。例：支援を検討する方針です（方针是探讨支援）。\n「〜を参考にする」— 参考…。例：GoToイートを参考にする（参考GoTo Eat）。\n「〜を求めています」— 要求…。例：検討することを求めています（要求进行探讨）。",
                "vocab": [
                    ["支援", "しえん", "支援、支持"],
                    ["新型コロナ", "しんがたころな", "新冠病毒"],
                    ["参考", "さんこう", "参考"],
                    ["農業団体", "のうぎょうだんたい", "农业团体"],
                    ["補填", "ほてん", "填补、补贴"],
                    ["注視", "ちゅうし", "密切关注"]
                ]
            }
        ]
    },
    {
        "slug": "genbaku-touka-81-nen",
        "title": "原爆投下81年、高まる核リスク 被爆者減る中、広島から平和訴え",
        "subtitle": "from 毎日新聞",
        "paras": [
            {
                "ja": "広島は6日、米国による原爆投下から81年となりました。米国のイランへの攻撃をはじめ、各地で戦争や紛争が後を絶たず、核兵器使用のリスクが現実味を帯びています。広島市中区の平和記念公園では午前8時から平和記念式典が開かれ、松井一実市長は平和宣言で、核兵器廃絶を理想で終わらせないための行動を起こすよう市民一人一人に呼びかけました。",
                "en": "On the 6th, Hiroshima marked 81 years since the U.S. atomic bombing. Wars and conflicts continue unabated in various places, from the U.S. attack on Iran to elsewhere, and the risk of nuclear weapons being used is becoming increasingly real. A peace memorial ceremony was held from 8 a.m. at the Peace Memorial Park in Naka Ward, Hiroshima City, where Mayor Kazumi Matsui, in his peace declaration, called on each citizen to take action so that the abolition of nuclear weapons does not remain merely an ideal.",
                "literal": "广岛在6日迎来了美国投下原子弹81周年。以美国对伊朗的攻击为首，各地战争和冲突接连不断，核武器使用的风险越来越带有现实感。广岛市中区的和平纪念公园从上午8点起举行了和平纪念仪式，松井一实市长在和平宣言中呼吁每一位市民采取行动，不要让废除核武器止步于理想。",
                "grammar": "「〜をはじめ」— 以…为首。例：米国のイランへの攻撃をはじめ（以美国对伊朗的攻击为首）。\n「〜が後を絶たず」— …接连不断。例：戦争や紛争が後を絶たず（战争和冲突接连不断）。\n「〜よう呼びかけました」— 呼吁…。例：行動を起こすよう呼びかけました（呼吁采取行动）。",
                "vocab": [
                    ["原爆", "げんばく", "原子弹"],
                    ["紛争", "ふんそう", "冲突、纷争"],
                    ["核兵器", "かくへいき", "核武器"],
                    ["現実味", "げんじつみ", "现实感、真实感"],
                    ["廃絶", "はいぜつ", "废除、灭绝"],
                    ["呼びかける", "よびかける", "呼吁"]
                ]
            },
            {
                "ja": "世界では分断と対立が深まっています。4～5月にニューヨークで開かれた核拡散防止条約（NPT）再検討会議は、過去2回に続いて成果文書を採択できませんでした。国内では、年末に予定される安全保障関連3文書の改定を巡り、非核三原則の見直しや核共有が取り沙汰され、被爆地を中心に懸念の声が上がっています。",
                "en": "Around the world, division and confrontation are deepening. The Review Conference of the Treaty on the Non-Proliferation of Nuclear Weapons (NPT) — the only nuclear disarmament framework in which both nuclear and non-nuclear states participate — held in New York in April and May, failed to adopt an outcome document for the third consecutive time. Domestically, amid planned revisions to the three security-related documents at the end of the year, a review of the Three Non-Nuclear Principles and nuclear sharing have been discussed, and voices of concern are rising, mainly in the bombed areas.",
                "literal": "世界上分裂和对立正在加深。4至5月在纽约召开的《不扩散核武器条约》（NPT）再审议会议，继过去两次之后仍未能通过成果文件。在国内，围绕年末预定进行的安全保障相关3份文件的修订，「非核三原则」的重新审视和「核共享」被议论纷纷，以被爆地为中心出现了担忧的声音。",
                "grammar": "「〜に続いて」— 继…之后。例：過去2回に続いて（继过去两次之后）。\n「〜を巡り」— 围绕…。例：改定を巡り（围绕修订）。\n「〜が取り沙汰され」— …被议论、被提起。例：核共有が取り沙汰され（核共享被议论）。",
                "vocab": [
                    ["分断", "ぶんだん", "分裂、割裂"],
                    ["核拡散防止条約", "かくかくさんぼうしじょうやく", "不扩散核武器条约"],
                    ["成果文書", "せいかぶんしょ", "成果文件"],
                    ["安全保障", "あんぜんほしょう", "安全保障"],
                    ["非核三原則", "ひかくさんげんそく", "非核三原则"],
                    ["懸念", "けねん", "担忧、忧虑"]
                ]
            },
            {
                "ja": "被爆者健康手帳を持つ被爆者は2025年度末時点で9万1105人と、過去最少を更新しました。平均年齢は86.66歳です。長年にわたり核兵器廃絶を訴えてきた日本被団協は、10日で結成70年を迎えます。高齢化が進む中、組織を2世、3世らに引き継ぐか、将来的に解散するかについて議論が始まっています。平和記念式典には過去最多の123カ国・地域が参列を予定しています。",
                "en": "As of the end of fiscal 2025, the number of hibakusha holding Atomic Bomb Survivor's Certificates was 91,105 — the lowest figure on record. Their average age is 86.66. The Japan Confederation of A- and H-Bomb Sufferers Organizations (Nihon Hidankyo), which has long campaigned for the abolition of nuclear weapons, will mark its 70th anniversary on the 10th. As aging progresses, debate has begun over whether the organization should be handed over to second- and third-generation members or eventually disbanded. A record 123 countries and regions are scheduled to attend the peace memorial ceremony.",
                "literal": "持有被爆者健康手册的被爆者截至2025年度末为9万1105人，刷新了历史最少纪录。平均年龄86.66岁。多年来一直呼吁废除核武器的日本被团协将在10日迎来成立70周年。在老龄化不断加剧的情况下，关于组织是交给二世、三世等后代，还是将来解散，讨论已经开始。和平纪念仪式预计有历史最多的123个国家和地区参加。",
                "grammar": "「〜時点で」— 截至…时点。例：2025年度末時点で（截至2025年度末）。\n「〜にわたり」— 长达…、持续…。例：長年にわたり訴えてきた（多年来一直在呼吁）。\n「〜か、〜かについて」— 关于是…还是…。例：引き継ぐか、解散するかについて（关于是继承还是解散）。",
                "vocab": [
                    ["被爆者", "ひばくしゃ", "原子弹爆炸受害者"],
                    ["手帳", "てちょう", "手册、证件"],
                    ["過去最少", "かこさいしょう", "历史最少"],
                    ["平均年齢", "へいきんねんれい", "平均年龄"],
                    ["引き継ぐ", "ひきつぐ", "继承、接替"],
                    ["参列", "さんれつ", "出席、参加（仪式）"]
                ]
            }
        ]
    },
    {
        "slug": "spacex-rocket-tsuki-shoutotsu",
        "title": "スペースXのロケット残骸、月面に衝突か ファルコン9の上段",
        "subtitle": "from ロイター",
        "paras": [
            {
                "ja": "米宇宙企業スペースXが打ち上げたロケットの残骸が、5日未明に高速で月面に衝突したとみられます。スクールバスほどの大きさのこの物体は、ロケット「ファルコン9」の上段機体で、2025年1月に月着陸船を打ち上げた際に使われました。機体の重さは4トンで、日本時間5日午後3時35分ごろ、時速8690キロで月面に衝突する見通しでした。",
                "en": "Debris from a rocket launched by U.S. space company SpaceX is believed to have struck the moon's surface at high speed in the early hours of the 5th. The object, about the size of a school bus, is the upper stage of SpaceX's Falcon 9 rocket, used in January 2025 to launch a lunar lander. Weighing 4 tons, it was expected to hit the lunar surface at 8,690 km/h at around 3:35 p.m. Japan time on the 5th.",
                "literal": "美国航天企业SpaceX发射的火箭残骸，据认为在5日凌晨以高速撞击了月球表面。这个约有一辆校车大小的物体是火箭「猎鹰9号」的上面级机体，是2025年1月发射月球着陆器时使用的。机体重量4吨，预计在日本时间5日下午3点35分左右，以时速8690公里撞击月球表面。",
                "grammar": "「〜とみられます」— 据认为…。例：月面に衝突したとみられます（据认为撞击了月面）。\n「〜ほど」— 大约…（程度）。例：スクールバスほどの大きさ（约校车大小）。\n「〜見通しでした」— 预计会…。例：衝突する見通しでした（预计会撞击）。",
                "vocab": [
                    ["残骸", "ざんがい", "残骸、碎片"],
                    ["月面", "げつめん", "月面、月球表面"],
                    ["上段", "じょうだん", "上面级（火箭）"],
                    ["機体", "きたい", "机体、机身"],
                    ["着陸船", "ちゃくりくせん", "着陆器"],
                    ["時速", "じそく", "时速"]
                ]
            },
            {
                "ja": "ロケットの一部は、地球から見えにくい月の西縁にあるアインシュタインクレーターに衝突すると予想されていました。科学者が望遠鏡の画像を解析し、衝突を確認するまでには少なくとも数時間かかる見通しです。スペースXによると、衝突は意図したものではありませんでした。",
                "en": "Part of the rocket was predicted to strike the Einstein crater on the moon's western limb, which is difficult to see from Earth. Scientists analyzing telescope images are expected to need at least several hours to confirm the impact. According to SpaceX, the collision was not intentional.",
                "literal": "火箭的一部分被预测会撞击位于从地球难以看到的月球西缘的「爱因斯坦」环形山。科学家解析望远镜图像、确认撞击预计至少需要数小时。据SpaceX称，撞击并不是有意图的。",
                "grammar": "「〜と予想されていました」— 曾被预测…。例：衝突すると予想されていました（曾被预测会撞击）。\n「〜までには」— 到…之前（需要时间）。例：確認するまでには数時間かかる（到确认为止需要数小时）。\n「〜によると」— 据…称。例：スペースXによると（据SpaceX称）。",
                "vocab": [
                    ["西縁", "にしぶち", "西缘、西侧边缘"],
                    ["クレーター", "くれーたー", "环形山、陨石坑"],
                    ["望遠鏡", "ぼうえんきょう", "望远镜"],
                    ["解析", "かいせき", "解析、分析"],
                    ["意図", "いと", "意图"],
                    ["衝突", "しょうとつ", "撞击、碰撞"]
                ]
            },
            {
                "ja": "こうしたロケットの一部は通常、搭載物を軌道上の正確な位置まで運んだ後、地球の大気圏に再突入して燃え尽きるか、海に落下します。しかし、今回のミッションでは大きな推力が必要だったため、宇宙空間に残り、宇宙ごみとして漂い続けました。残っていた燃料は放出され、機体は制御できない状態だったといいます。",
                "en": "Parts of rockets like this usually re-enter Earth's atmosphere and burn up, or fall into the ocean, after delivering their payload to the correct position in orbit. However, because this mission required great thrust, this stage remained in space, drifting as space junk. The remaining fuel was vented, and the vehicle was in an uncontrollable state, according to reports.",
                "literal": "这样的火箭部件通常会在把搭载物运送到轨道上的准确位置后，重新进入地球大气层烧尽，或者坠入海中。但是，由于这次任务需要很大的推力，所以留在了宇宙空间，作为太空垃圾持续漂浮。据称残留的燃料被排放掉，机体处于无法控制的状态。",
                "grammar": "「〜た後」— …之后。例：運んだ後（运送之后）。\n「〜か、〜します」— …或者…。例：燃え尽きるか、海に落下します（烧尽或者坠入海中）。\n「〜ため」— 因为…。例：大きな推力が必要だったため（因为需要很大的推力）。",
                "vocab": [
                    ["搭載物", "とうさいぶつ", "搭载物、有效载荷"],
                    ["軌道", "きどう", "轨道"],
                    ["大気圏", "たいきけん", "大气层"],
                    ["再突入", "さいとつにゅう", "再入（大气层）"],
                    ["宇宙ごみ", "うちゅうごみ", "太空垃圾"],
                    ["放出", "ほうしゅつ", "排放、释放"]
                ]
            }
        ]
    },
    {
        "slug": "shime-ramen-yokkyuu-no-genin",
        "title": "飲酒後の「締めのラーメン欲」の原因は？ 脳の錯覚と真実【医師解説】",
        "subtitle": "from メディカルドック",
        "paras": [
            {
                "ja": "焼き肉や飲み会のあと、満腹のはずなのに不思議と食べたくなる「締めのラーメン」。じつはこの欲求には、血糖値や脳の働きなど、体の仕組みが深く関係しています。高石内科循環器クリニック院長の高石博史先生に、その理由を聞きました。",
                "en": "After yakiniku or a drinking party, you should be full, yet you mysteriously crave the \"closing ramen.\" In fact, this craving is deeply related to bodily mechanisms such as blood sugar levels and brain function. We asked Dr. Hiroshi Takaishi, director of the Takaishi Internal Medicine and Cardiology Clinic, about the reason.",
                "literal": "烤肉或聚会之后，明明应该饱了，却不可思议地想吃「收尾拉面」。其实这种欲望与血糖值和大脑的功能等身体机制密切相关。我们向高石内科循环器诊所院长高石博史医生询问了原因。",
                "grammar": "「〜のはずなのに」— 明明应该…却…。例：満腹のはずなのに食べたくなる（明明应该饱了却想吃）。\n"+"「〜に聞きました」— 向…询问。例：先生に理由を聞きました（向医生询问了原因）。\n「〜が深く関係しています」— 与…密切相关。例：体の仕組みが深く関係しています（与身体机制密切相关）。",
                "vocab": [
                    ["締め", "しめ", "收尾、结束（最后一道）"],
                    ["欲求", "よっきゅう", "欲望、需求"],
                    ["血糖値", "けっとうち", "血糖值"],
                    ["仕組み", "しくみ", "机制、构造"],
                    ["院長", "いんちょう", "院长"],
                    ["循環器", "じゅんかんき", "循环系统、心血管"]
                ]
            },
            {
                "ja": "肝臓は本来、血糖値を一定に保つ働きをしていますが、飲酒時はアルコールの分解を優先するため、血糖値の維持機能が一時的に低下します。その結果、血糖値が下がりやすくなり、体は低血糖状態に陥ります。脳はこのエネルギー不足を察知し、「すぐエネルギーになる炭水化物を摂れ」と強力な指令を出します。このメカニズムが、飲んだあとにラーメンを欲してしまう正体です。",
                "en": "The liver normally works to keep blood sugar levels constant, but when drinking, it prioritizes breaking down alcohol, so its blood-sugar-maintaining function temporarily declines. As a result, blood sugar levels drop easily, and the body falls into a state of low blood sugar. The brain detects this energy shortage and issues a strong command: \"Consume carbohydrates that quickly become energy.\" This mechanism is the true culprit behind craving ramen after drinking.",
                "literal": "肝脏本来具有保持血糖值稳定的功能，但饮酒时会优先分解酒精，因此维持血糖值的功能暂时下降。结果，血糖值容易下降，身体陷入低血糖状态。大脑察觉到这种能量不足，发出「摄取能立刻转化为能量的碳水化合物」的强大指令。这个机制就是饮酒后想吃拉面的真面目。",
                "grammar": "「〜働きをしています」— 具有…的功能。例：血糖値を保つ働きをしています（具有保持血糖值的功能）。\n「〜ため」— 因为…。例：分解を優先するため（因为优先分解）。\n「〜に陥ります」— 陷入…。例：低血糖状態に陥ります（陷入低血糖状态）。",
                "vocab": [
                    ["肝臓", "かんぞう", "肝脏"],
                    ["アルコール", "あるこーる", "酒精"],
                    ["分解", "ぶんかい", "分解"],
                    ["低下", "ていか", "下降、降低"],
                    ["低血糖", "ていけっとう", "低血糖"],
                    ["炭水化物", "たんすいかぶつ", "碳水化合物"]
                ]
            },
            {
                "ja": "また、アルコールには強い利尿作用があるため、お酒を飲むと体内の水分とともにナトリウムやカリウムといった電解質が大量に排出されます。体は脱水傾向とミネラル不足の状態に陥り、失われた塩分を補おうとする生体反応が起こります。そのため、濃いスープのラーメンが欲しくなるのです。さらに、「飲んだあとは締めのラーメン」という習慣が脳にインプットされているという側面もあるかもしれません。",
                "en": "Moreover, alcohol has a strong diuretic effect, so when you drink, large amounts of electrolytes — such as sodium and potassium — are excreted along with water from the body. The body falls into a state of dehydration tendency and mineral deficiency, triggering a biological reaction to replenish the lost salt. That is why you crave ramen with a rich soup. Furthermore, there may also be the aspect that the habit of \"after drinking, closing ramen\" is ingrained in the brain.",
                "literal": "另外，酒精有很强的利尿作用，所以喝酒后体内的水分会连同钠和钾等电解质一起被大量排出。身体陷入脱水倾向和矿物质不足的状态，产生试图补充失去的盐分的生物反应。因此，就会想喝浓汤拉面。而且，也许还有「喝完酒就要吃收尾拉面」这一习惯被灌输进大脑的一面。",
                "grammar": "「〜とともに」— 与…一起。例：水分とともに排出されます（与水分一起被排出）。\n「〜ようとする」— 试图…。例：塩分を補おうとする反応（试图补充盐分的反应）。\n「〜かもしれません」— 也许…。例：側面もあるかもしれません（也许也有这样的一面）。",
                "vocab": [
                    ["利尿作用", "りにょうさよう", "利尿作用"],
                    ["電解質", "でんかいしつ", "电解质"],
                    ["ナトリウム", "なとりうむ", "钠"],
                    ["カリウム", "かりうむ", "钾"],
                    ["脱水", "だっすい", "脱水"],
                    ["インプット", "いんぷっと", "输入、灌输"]
                ]
            }
        ]
    },
    {
        "slug": "higashihiroshima-zenkai-kaji",
        "title": "「家の中から叫び声」焼け跡から4人の遺体 家族4人全員死亡か 東広島市の住宅火災",
        "subtitle": "from テレビ新広島",
        "paras": [
            {
                "ja": "5日未明、広島県東広島市の住宅が全焼する火事があり、焼け跡から4人の遺体が見つかりました。警察と消防によりますと、5日午前3時半ごろ、東広島市黒瀬楢原東で「建物が燃えている」と付近の住民から消防に通報がありました。",
                "en": "In the early hours of the 5th, a house in Higashihiroshima City, Hiroshima Prefecture, burned down completely, and four bodies were found in the ruins. According to police and firefighters, at around 3:30 a.m. on the 5th, a nearby resident called the fire department in Higashihiroshima City's Kurose-Narahara Higashi area, reporting that \"a building is on fire.\"",
                "literal": "5日凌晨，广岛县东广岛市发生住宅被完全烧毁的火灾，烧毁现场发现了4具遗体。据警方和消防称，5日凌晨3点半左右，在东广岛市黑濑�原东，附近居民向消防通报称「建筑物着火了」。",
                "grammar": "「〜によりますと」— 据…称。例：警察と消防によりますと（据警方和消防称）。\n「〜ごろ」— …左右（时间）。例：午前3時半ごろ（凌晨3点半左右）。\n「〜と通報がありました」— 接到了…的通报。例：燃えていると通報がありました（接到了着火的通报）。",
                "vocab": [
                    ["未明", "みめい", "凌晨、拂晓前"],
                    ["全焼", "ぜんしょう", "全部烧毁"],
                    ["焼け跡", "やけあと", "火灾废墟"],
                    ["遺体", "いたい", "遗体"],
                    ["通報", "つうほう", "通报、报警"],
                    ["付近", "ふきん", "附近"]
                ]
            },
            {
                "ja": "朝になり、あらわになった現場の住宅は、黒く焼け焦げ、骨組みが剥き出しになっていました。近隣住民の中には、叫び声が聞こえて異変に気づいて起きたという人や、炎の勢いが激しく、何かが爆発するような音が聞こえたと話す人もいました。",
                "en": "By morning, the house at the scene, now exposed, was charred black with its frame laid bare. Among nearby residents, some said they were woken by screams and realized something was wrong, while others said the flames were so fierce that they heard a sound like something exploding.",
                "literal": "到了早晨，暴露出来的现场住宅被烧得焦黑，骨架裸露在外。附近居民中，有人说是听到惨叫声察觉到异常而醒来的，也有人说火势非常猛烈，听到了像什么东西爆炸一样的声音。",
                "grammar": "「〜になり」— 变成…。例：朝になり（到了早晨）。\n「〜という人や、〜と話す人もいました」— 有说…的人，也有说…的人。例：起きたという人や、聞こえたと話す人（说醒来了的人、说听到了的人）。\n「〜ような」— 像…一样的。例：爆発するような音（像爆炸一样的声音）。",
                "vocab": [
                    ["焼け焦げる", "やけこげる", "烧焦"],
                    ["骨組み", "ほねぐみ", "骨架、框架"],
                    ["剥き出し", "むきだし", "裸露、暴露"],
                    ["近隣", "きんりん", "近邻、邻近"],
                    ["異変", "いへん", "异常、变故"],
                    ["勢い", "いきおい", "势头、气势"]
                ]
            },
            {
                "ja": "火は通報からおよそ4時間20分後に消し止められましたが、2階建ての住宅が全焼し、焼け跡から4人の遺体が見つかりました。この家に住む10代の女性と40代の両親、70代の祖父の家族4人全員と連絡が取れておらず、警察は遺体がこの家族であるとみて、身元の確認を急いでいます。",
                "en": "The fire was brought under control about 4 hours and 20 minutes after the report, but the two-story house burned down completely and four bodies were found in the ruins. Contact has not been established with all four family members living there — a woman in her teens, her parents in their 40s, and a grandfather in his 70s — and police, believing the bodies are those of the family, are rushing to confirm their identities.",
                "literal": "火在通报后约4小时20分钟后被扑灭，但两层住宅被全部烧毁，废墟中发现了4具遗体。住在这栋房子里的一名10多岁的女性和40多岁的父母、70多岁的祖父——4名家人全部无法取得联系，警方认为遗体就是这家人，正在加紧确认身份。",
                "grammar": "「〜からおよそ〜後」— 从…后大约…。例：通報からおよそ4時間20分後（通报后约4小时20分）。\n「〜と連絡が取れておらず」— 未能与…取得联系。例：家族4人全員と連絡が取れておらず（未能与4名家人取得联系）。\n「〜とみて」— 认为…、判断…。例：遺体がこの家族であるとみて（认为遗体就是这家人）。",
                "vocab": [
                    ["消し止める", "けしとめる", "扑灭"],
                    ["両親", "りょうしん", "父母、双亲"],
                    ["祖父", "そふ", "祖父、爷爷"],
                    ["連絡が取れる", "れんらくがとれる", "取得联系"],
                    ["身元", "みもと", "身份"],
                    ["確認を急ぐ", "かくにんをいそぐ", "加紧确认"]
                ]
            }
        ]
    },
    {
        "slug": "nippon-seishi-hachioji-koujou",
        "title": "9人が犠牲の日本製紙八代工場、社長ら初会見 工場長「正直何もできなかった」",
        "subtitle": "from 読売新聞オンライン",
        "paras": [
            {
                "ja": "「本当にこれ以上ない悲しく、つらい出来事」。7月28日の地震で煙突が倒壊し、従業員ら9人が犠牲になった日本製紙八代工場（熊本県八代市）。5日、地震後初めての記者会見で、同社の瀬辺明社長は沈痛な表情を浮かべました。会見に同席した山辺義貞工場長は「正直、何もできなかった」と振り返りました。",
                "en": "\"A truly heartbreaking and painful event like no other.\" At the Nippon Paper Yatsushiro mill (Yatsushiro City, Kumamoto Prefecture), where a chimney collapsed in the July 28 earthquake, killing nine people including employees, President Akira Sebe appeared grim at the company's first press conference since the quake on the 5th. Factory manager Yoshisada Yamabe, who attended the conference, looked back and said, \"Honestly, there was nothing I could do.\"",
                "literal": "「真的是再没有比这更悲伤、更痛苦的事情」。在7月28日地震中烟囱倒塌、包括员工在内9人遇难的日本制纸八代工厂（熊本县八代市）。5日，在地震后首次记者会上，该公司社长�辺明露出沉痛的表情。一同出席的工厂长山边义贞回顾说「说实话，什么也没能做到」。",
                "grammar": "「〜これ以上ない」— 没有比这更…的。例：これ以上ない悲しく、つらい出来事（再没有比这更悲伤痛苦的事）。\n「〜で」— 因…（原因）。例：地震で煙突が倒壊し（因地震烟囱倒塌）。\n「〜と振り返りました」— 回顾说…。例：何もできなかったと振り返りました（回顾说没能做什么）。",
                "vocab": [
                    ["犠牲", "ぎせい", "牺牲、遇难"],
                    ["煙突", "えんとつ", "烟囱"],
                    ["倒壊", "とうかい", "倒塌"],
                    ["記者会見", "きしゃかいけん", "记者会"],
                    ["沈痛", "ちんつう", "沉痛"],
                    ["工場長", "こうじょうちょう", "工厂长"]
                ]
            },
            {
                "ja": "同社によると、地震発生時、工場内では従業員や関連会社、取引先の社員ら計414人が働いていました。激しい揺れで電源が失われ、煙突の倒壊で従業員らは2階建ての事務所に閉じ込められましたが、110番も119番もつながりませんでした。約40分後、被害を免れた従業員が消防に勤務する親族に救助を要請しました。駆けつけた消防や自衛隊員らが手作業でがれきを取り除き、閉じ込められた11人を救助しましたが、うち9人の死亡が確認されました。",
                "en": "According to the company, 414 people in total — employees, workers from affiliated companies, and staff from business partners — were working at the mill when the earthquake struck. The violent shaking knocked out power, and the collapsing chimney trapped workers in a two-story office building, but neither 110 nor 119 calls would connect. About 40 minutes later, an employee who had escaped harm requested rescue from a relative working in the fire department. Firefighters and Self-Defense Force members who rushed in removed debris by hand and rescued 11 trapped people, but the deaths of nine of them were confirmed.",
                "literal": "据该公司称，地震发生时，工厂内有员工、关联公司和客户的员工等共计414人在工作。剧烈的摇晃导致断电，烟囱倒塌使员工们被困在两层办公楼里，但110和119都打不通。约40分钟后，幸免于难的员工向在消防工作的亲属请求了救助。赶到的消防员和自卫队员等徒手清除瓦砾，救出了被困的11人，但其中9人的死亡得到确认。",
                "grammar": "「〜によると」— 据…称。例：同社によると（据该公司称）。\n「〜が失われ」— …丧失。例：電源が失われ（电源丧失）。\n「〜ましたが、うち〜が」— …了，但其中…。例：11人を救助しましたが、うち9人の死亡が確認されました（救出11人，但其中9人死亡被确认）。",
                "vocab": [
                    ["関連会社", "かんれんがいしゃ", "关联公司"],
                    ["取引先", "とりひきさき", "客户、交易对象"],
                    ["閉じ込める", "とじこめる", "关在里面、困住"],
                    ["要請", "ようせい", "请求、要求"],
                    ["がれき", "がれき", "瓦砾、废墟"],
                    ["自衛隊", "じえいたい", "自卫队"]
                ]
            },
            {
                "ja": "同社によると、80メートルの煙突は日常的にひびやサビの有無を目視で確認していましたが、大がかりな点検は2006年が最後でした。工場にある5本の煙突のうち、鉄筋コンクリート製の70メートルのものも倒れ、110メートルの煙突も損傷しました。同社は煙突の耐震性などについて「調査中」と回答し、調査委員会を通じて明らかにする意向を示しました。",
                "en": "According to the company, the 80-meter chimney was routinely checked visually for cracks and rust, but the last large-scale inspection was in 2006. Of the five chimneys at the mill, a 70-meter reinforced-concrete one also toppled, and the 110-meter chimney was also damaged. The company responded that it is \"under investigation\" regarding the chimneys' earthquake resistance and indicated its intention to clarify the matter through an investigation committee.",
                "literal": "据该公司称，80米的烟囱日常通过目视确认有无裂缝和锈迹，但大规模检查最后一次是在2006年。工厂内5根烟囱中，钢筋混凝土制的70米烟囱也倒了，110米的烟囱也受损。该公司就烟囱的抗震性等回答称「正在调查中」，并表示有意通过调查委员会予以公布。",
                "grammar": "「〜が最後でした」— …是最后一次。例：大がかりな点検は2006年が最後でした（大规模检查最后一次是2006年）。\n「〜のうち」— 在…之中。例：5本の煙突のうち（在5根烟囱之中）。\n「〜意向を示しました」— 表示…的意向。例：明らかにする意向を示しました（表示要公布的意向）。",
                "vocab": [
                    ["日常的", "にちじょうてき", "日常的"],
                    ["ひび", "ひび", "裂缝"],
                    ["サビ", "さび", "锈"],
                    ["目視", "もし", "目视、用眼观察"],
                    ["大がかり", "おおがかり", "大规模"],
                    ["耐震性", "たいしんせい", "抗震性"]
                ]
            }
        ]
    },
    {
        "slug": "mercari-nashi-tenbai-giwaku",
        "title": "メルカリ、梨の転売疑惑を否定「誹謗中傷はやめて」 生産者を現地確認",
        "subtitle": "from Impress Watch",
        "paras": [
            {
                "ja": "メルカリで「梨の転売」が疑われた事件について、メルカリは盗品の出品疑惑を否定しました。現地調査を実施し、出品状況や生産実態を確認した結果、実在の生産者による出品であることが確認されたといいます。現時点では、盗品など不正な経路で入手した商品の出品は確認されていないとしています。",
                "en": "Regarding the incident in which \"reselling of pears\" on Mercari was suspected, Mercari denied the suspicion of listings of stolen goods. After conducting on-site investigations to confirm listing status and actual production conditions, it says it was confirmed that the listings were by real producers. At present, it states that no listings of goods obtained through illicit channels such as stolen items have been confirmed.",
                "literal": "关于在Mercari上被怀疑「转卖梨」的事件，Mercari否认了上架赃物的嫌疑。实施现场调查、确认上架情况和生产实际情况的结果，据称已确认是真实存在的生产者上架的。该公司表示，目前没有确认到通过盗窃等不正当渠道获得的商品上架。",
                "grammar": "「〜について」— 关于…。例：梨の転売が疑われた事件について（关于被怀疑转卖梨的事件）。\n「〜結果」— …的结果。例：現地調査を実施した結果（实施现场调查的结果）。\n「〜としています」— 表示…、声称…。例：確認されていないとしています（表示未被确认）。",
                "vocab": [
                    ["転売", "てんばい", "转卖、倒卖"],
                    ["盗品", "とうひん", "赃物"],
                    ["出品", "しゅっぴん", "上架、发布商品"],
                    ["現地調査", "げんちちょうさ", "现场调查"],
                    ["実態", "じったい", "实际情况"],
                    ["不正", "ふせい", "不正当、非法"]
                ]
            },
            {
                "ja": "この問題は、7月に福岡県で起きた「梨の盗難」事件に起因します。同じ農園が大量の盗難被害に遭い、廃業を余儀なくされたという事件で、テレビやネットニュースでも話題となりました。その後、盗品の梨がメルカリで転売されているという疑惑がソーシャルメディア上で拡散し、出品者に対し、多くの抗議や誹謗中傷が行われました。",
                "en": "This issue stems from the \"pear theft\" incident that occurred in Fukuoka Prefecture in July. In that incident, the same orchard suffered massive theft damage and was forced to go out of business, making headlines on TV and online news. Afterward, the suspicion that the stolen pears were being resold on Mercari spread on social media, and sellers were subjected to many protests and defamatory comments.",
                "literal": "这个问题起因于7月发生在福冈县的「梨被盗」事件。这是同一果园遭遇大量被盗损失、被迫停业的事件，在电视和网络新闻上也成为话题。此后，「被盗的梨在Mercari上被转卖」的嫌疑在社交媒体上扩散，上架者遭到了大量抗议和诽谤中伤。",
                "grammar": "「〜に起因します」— 起因于…。例：梨の盗難事件に起因します（起因于梨被盗事件）。\n「〜を余儀なくされた」— 被迫…。例：廃業を余儀なくされた（被迫停业）。\n「〜に対し」— 对…。例：出品者に対し、抗議が行われました（对上架者进行了抗议）。",
                "vocab": [
                    ["起因", "きいん", "起因"],
                    ["盗難", "とうなん", "被盗、失窃"],
                    ["農園", "のうえん", "果园、农场"],
                    ["廃業", "はいぎょう", "停业、歇业"],
                    ["拡散", "かくさん", "扩散、传播"],
                    ["誹謗中傷", "ひぼうちゅうしょう", "诽谤中伤"]
                ]
            },
            {
                "ja": "一方で、出品者は盗品の出品を強く否定していました。メルカリは、梨の取引がある複数の出品者を対象に、農園や作業場、保管場所などの実地調査を行いました。また、「根拠のない情報をもとに特定の出品者を攻撃するような誹謗中傷はやめてほしい」と訴えています。",
                "en": "Meanwhile, the sellers strongly denied listing stolen goods. Mercari conducted on-site inspections — of orchards, workplaces, storage locations, and more — targeting multiple sellers with pear transactions. It also appeals, \"Please stop defamatory attacks on specific sellers based on unfounded information.\"",
                "literal": "另一方面，上架者强烈否认上架了赃物。Mercari以有梨交易的多名上架者为对象，进行了果园、作业场所、保管场所等的实地调查。并且呼吁「请停止基于没有根据的信息攻击特定上架者的诽谤中伤」。",
                "grammar": "「〜を対象に」— 以…为对象。例：複数の出品者を対象に調査（以多名上架者为对象的调查）。\n「〜をもとに」— 基于…。例：根拠のない情報をもとに（基于没有根据的信息）。\n「〜てほしい」— 希望（对方）…。例：やめてほしいと訴えています（呼吁希望停止）。",
                "vocab": [
                    ["否定", "ひてい", "否定、否认"],
                    ["複数", "ふくすう", "多个、复数"],
                    ["作業場", "さぎょうば", "作业场所"],
                    ["保管場所", "ほかんばしょ", "保管场所"],
                    ["実地調査", "じっちちょうさ", "实地调查"],
                    ["根拠", "こんきょ", "根据、依据"]
                ]
            }
        ]
    },
    {
        "slug": "neko-ga-pan-wo-koneru",
        "title": "なぜ猫は「パンをこねる」のか？ 前足で飼い主をもむ習性を生物学者が解説",
        "subtitle": "from Forbes JAPAN",
        "paras": [
            {
                "ja": "猫が柔らかい毛布やクッションなどの上で前足をゆっくり交互に踏みしめる──俗に「ふみふみ」や「もみもみ」と呼ばれるこの動作は、飼い猫に最もよく見られる行動のひとつです。日本語で「パンをこねる」とも言われるこの動作を、英語圏の飼い主たちは「ビスケット作り」と呼びます。人間が手で生地をこねる様子になぞらえた表現です。",
                "en": "Cats slowly pressing their front paws alternately on soft blankets, cushions, and the like — this behavior, colloquially called \"fumifumi\" or \"momimomi,\" is one of the most commonly seen actions in pet cats. This motion, also called \"kneading bread\" in Japanese, is referred to as \"making biscuits\" by English-speaking cat owners. It is an expression likened to a person kneading dough by hand.",
                "literal": "猫在柔软的毛毯、靠垫等上面用前爪慢慢地交替踩踏——俗称为「fumifumi」「momimomi」的这个动作，是家猫最常见的行为之一。在日语中也被称为「揉面包」的这个动作，英语圈的饲主们称之为「做饼干」。这是比作人用手揉捏面团样子的表达。",
                "grammar": "「〜と〜」— 叫做…。例：俗に「ふみふみ」と呼ばれる（俗称为fumifumi）。\n「〜とも言われる」— 也被称为…。例：「パンをこねる」とも言われる（也被称为揉面包）。\n「〜になぞらえた」— 比作…的。例：生地をこねる様子になぞらえた表現（比作揉面团样子的表达）。",
                "vocab": [
                    ["前足", "まえあし", "前爪、前足"],
                    ["交互に", "こうごに", "交替地、轮流地"],
                    ["踏みしめる", "ふみしめる", "用力踩踏"],
                    ["飼い猫", "かいねこ", "家猫、宠物猫"],
                    ["生地", "きじ", "面团"],
                    ["なぞらえる", "なぞらえる", "比作、比拟"]
                ]
            },
            {
                "ja": "生まれたばかりの子猫の場合、「ふみふみ」には明確な意味があります。授乳中の母猫の腹をリズミカルに押すことで、母乳がよく出るように促しているのです。この行動は生後数日で現れる反射反応で、離乳すると動機が失われ、運動パターンも変わります。しかし、飼い猫はそうでない場合が多いのです。",
                "en": "In the case of newborn kittens, \"fumifumi\" has a clear meaning. By rhythmically pressing the belly of the nursing mother cat, they encourage milk to flow well. This behavior is a reflex that appears within days after birth, and once weaned, the motivation is lost and the movement pattern changes too. However, pet cats often do not follow that pattern.",
                "literal": "刚出生的幼猫的情况，「fumifumi」有明确的意义。通过有节奏地按压正在哺乳的母猫的肚子，促进母乳更好地分泌。这个行为是出生后几天内出现的反射反应，断奶后动机消失，运动模式也会改变。但是，家猫大多不是这样。",
                "grammar": "「〜の場合」— …的情况。例：子猫の場合（幼猫的情况）。\n「〜ことで」— 通过…。例：腹を押すことで促しています（通过按压肚子来促进）。\n「〜と」— 一…就…。例：離乳すると動機が失われ（一断奶动机就消失）。",
                "vocab": [
                    ["子猫", "こねこ", "幼猫、小猫"],
                    ["授乳", "じゅにゅう", "哺乳、喂奶"],
                    ["リズミカル", "りずみかる", "有节奏的"],
                    ["反射反応", "はんしゃはんのう", "反射反应"],
                    ["離乳", "りにゅう", "断奶"],
                    ["動機", "どうき", "动机"]
                ]
            },
            {
                "ja": "乳離れして10年以上が経過した成猫でさえ、乳が出るはずもない毛布や飼い主の膝の上でふみふみします。生物学者がここで注目するのが「ネオテニー（幼形成熟）」という概念です。幼若期の特徴が成体になっても残っていることをいい、発達段階をとっくに過ぎても残っている子猫期の行動のひとつの例とされています。",
                "en": "Even adult cats more than a decade past weaning knead on blankets where milk could never come, or on their owner's lap. What biologists focus on here is the concept of \"neoteny.\" It refers to juvenile characteristics persisting into adulthood, and this behavior is considered one example of kittenhood behaviors that remain long after the developmental stage has passed.",
                "literal": "即使是断奶10年以上的成年猫，也会在没有可能出奶的毛毯或饲主的膝盖上做「fumifumi」。生物学家在这里关注的是「幼态延续（neoteny）」这一概念。它指的是幼年期的特征到成年后仍然保留，被认为是早已过了发育阶段却仍然保留的幼猫期行为的一个例子。",
                "grammar": "「〜でさえ」— 连…都。例：成猫でさえふみふみします（连成年猫都会fumifumi）。\n「〜はずもない」— 不可能…。例：乳が出るはずもない毛布（不可能出奶的毛毯）。\n「〜とされています」— 被认为是…。例：ひとつの例とされています（被认为是一个例子）。",
                "vocab": [
                    ["乳離れ", "ちばなれ", "断奶、离乳"],
                    ["成猫", "せいねこ", "成年猫"],
                    ["膝", "ひざ", "膝盖"],
                    ["幼形成熟", "ようけいせいじゅく", "幼态延续（neoteny）"],
                    ["幼若期", "ようじゃくき", "幼年期"],
                    ["とっくに", "とっくに", "早就、老早"]
                ]
            }
        ]
    },
    {
        "slug": "tai-de-shinshu-kyouryuu",
        "title": "体長27m・体重27tの新種恐竜をタイで発見 東南アジア最大か、なぜ巨大に進化できた？",
        "subtitle": "from ナショナル ジオグラフィック日本版",
        "paras": [
            {
                "ja": "かつてタイには、巨大な恐竜がいました。ナショナルジオグラフィックの探求者、シタ・マニットクーン氏が率いる研究チームによって、体長約27メートル、体重約27トンと推定される首の長い恐竜が発見されました。「発掘した骨の一次測定結果によると、東南アジア最大の恐竜となる可能性があります」とマニットクーン氏は述べています。",
                "en": "Once, giant dinosaurs lived in Thailand. A research team led by National Geographic Explorer Sita Manitkoon has discovered a long-necked dinosaur estimated to be about 27 meters long and weighing about 27 tons. \"According to the preliminary measurements of the excavated bones, it could be the largest dinosaur in Southeast Asia,\" Manitkoon said.",
                "literal": "从前，泰国曾有巨大的恐龙。由《国家地理》探索者西塔·马尼特昆率领的研究团队，发现了推定体长约27米、体重约27吨的长颈恐龙。马尼特昆表示「根据发掘出的骨骼的初步测量结果，有可能成为东南亚最大的恐龙」。",
                "grammar": "「〜が率いる」— 由…率领的。例：研究チームが率いる（率领的研究团队）。\n「〜と推定される」— 被推定为…。例：体重約27トンと推定される（被推定约27吨）。\n「〜と述べています」— 表示…。例：可能性がありますと述べています（表示有可能）。",
                "vocab": [
                    ["恐竜", "きょうりゅう", "恐龙"],
                    ["探求者", "たんきゅうしゃ", "探索者"],
                    ["体長", "たいちょう", "体长"],
                    ["推定", "すいてい", "推定、推算"],
                    ["発掘", "はっくつ", "发掘"],
                    ["一次測定", "いちじそくてい", "初步测量"]
                ]
            },
            {
                "ja": "この骨がタイ北東部のチャイヤプーム県で見つかったのは2016年のこと。近くに住むタノーム・ルアンナン氏が、公共の池の岸辺で「奇妙な岩のようなもの」を見つけ、タイ鉱物資源局に報告しました。それはのちに恐竜の骨だとわかり、東南アジアの民話に登場する巨大生物「ナーガ」にちなんで「ナガティタン・チャイヤプーメンシス」と名付けられました。",
                "en": "The bones were found in Chaiyaphum Province in northeastern Thailand in 2016. A nearby resident, Thanom Ruanan, found \"something like a strange rock\" on the shore of a public pond and reported it to Thailand's Department of Mineral Resources. It later turned out to be dinosaur bones, and the creature was named \"Nagatitan chaiyaphumensis,\" after the Naga, a giant serpent-like mythical creature from Southeast Asian folklore.",
                "literal": "这些骨骼于2016年在泰国东北部的猜也奔府被发现。住在附近的塔农·鲁安南在公共池塘岸边发现了「像奇怪岩石一样的东西」，并向泰国矿产资源局报告。那后来被确认是恐龙的骨骼，以东南亚民间故事中出现的巨大生物「那伽」命名，被称为「Nagatitan chaiyaphumensis」。",
                "grammar": "「〜のこと」— 是…时候的事。例：見つかったのは2016年のこと（被发现是2016年的事）。\n「〜にちなんで」— 因…而得名。例：ナーガにちなんで名付けられました（因那伽而得名）。\n「〜とわかり」— 查明是…。例：恐竜の骨だとわかり（查明是恐龙的骨骼）。",
                "vocab": [
                    ["北東部", "ほくとうぶ", "东北部"],
                    ["池", "いけ", "池塘"],
                    ["岸辺", "きしべ", "岸边"],
                    ["鉱物資源局", "こうぶつしげんきょく", "矿产资源局"],
                    ["民話", "みんわ", "民间故事"],
                    ["名付ける", "なづける", "命名"]
                ]
            },
            {
                "ja": "ナガティタンの椎骨や肋骨などの骨の破片は、1億1300万年前の岩石から見つかりました。右の前肢は、近年見つかった巨大竜脚類の肢よりも長かったといいます。竜脚類の恐竜は、1億年以上かけて30回以上にわたって巨大な体を進化させてきましたが、ナガティタンも、時代や場所が異なる巨大恐竜たちとは別々に進化を遂げてきたと推測されています。",
                "en": "Fragments of Nagatitan's vertebrae, ribs, and other bones were found in rocks dating back 113 million years. Its right forelimb was reportedly longer than the limbs of giant sauropods discovered in recent years. Sauropod dinosaurs evolved enormous bodies more than 30 times over 100 million years, and Nagatitan is also inferred to have evolved separately from the giant dinosaurs of different eras and places.",
                "literal": "纳加提坦的椎骨、肋骨等骨骼碎片，是在1亿1300万年前的岩石中发现的。据称其右前肢比近年发现的巨大蜥脚类恐龙的肢骨还要长。蜥脚类恐龙在1亿多年的时间里、超过30次进化出巨大的身体，但据推测，纳加提坦也与时代和地点不同的巨型恐龙们分别完成了进化。",
                "grammar": "「〜といいます」— 据说…。例：肢よりも長かったといいます（据说比肢骨还长）。\n「〜にわたって」— 长达…、遍及…。例：30回以上にわたって進化（超过30次地进化）。\n「〜と推測されています」— 被推测…。例：進化を遂げてきたと推測されています（被推测完成了进化）。",
                "vocab": [
                    ["椎骨", "ついこつ", "椎骨"],
                    ["肋骨", "ろっこつ", "肋骨"],
                    ["破片", "はへん", "碎片"],
                    ["岩石", "がんせき", "岩石"],
                    ["竜脚類", "りゅうきゃくるい", "蜥脚类恐龙"],
                    ["推測", "すいそく", "推测"]
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
