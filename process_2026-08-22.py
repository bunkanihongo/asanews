#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-22 (Sat) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-22'
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


articles = []
articles += [
    {
        "slug": "tenki-22nichi-raiu-mousho",
        "title": "22日 西・東日本は急な雷雨に注意 東海〜九州は猛暑",
        "subtitle": "from ウェザーマップ",
        "paras": [
            {
                "ja": "22日(土)は西・北日本を中心に日差しが届く見込みです。午後は西・東日本を中心に急な雷雨に注意が必要です。日中は北海道でも30℃以上になる所があり、全国的に厳しい暑さです。東海～九州は猛暑でしょう。",
                "en": "On Saturday the 22nd, sunshine is expected mainly across western and northern Japan. In the afternoon, caution is needed against sudden thunderstorms mainly in western and eastern Japan. During the day, some places in Hokkaido will reach 30°C or higher, bringing severe heat nationwide. From Tokai to Kyushu, it will likely be extreme heat (mōshobi).",
                "literal": "22日（周六）预计以西部和北部日本为中心可见阳光。午后以西部和东部日本为中心需要注意突然的雷雨。白天北海道也有达到30度以上的地方，将是全国性酷暑。东海至九州大概是猛暑日吧。",
                "grammar": "「〜見込みです」— 预计…（预报用语）。例：日差しが届く見込みです（预计可见阳光）。\n「〜に注意が必要です」— 需要注意…。例：急な雷雨に注意が必要です（需要注意突然的雷雨）。\n「〜でしょう」— 大概会…（推测）。例：東海～九州は猛暑でしょう（东海至九州大概是酷暑）。",
                "vocab": [["日差し", "ひざし", "阳光"], ["雷雨", "らいう", "雷雨"], ["注意", "ちゅうい", "注意"], ["午後", "ごご", "下午"], ["厳しい", "きびしい", "严酷的、严厉的"], ["猛暑", "もうしょ", "酷暑、猛暑"]]
            },
            {
                "ja": "東日本や東北南部は朝から雲が多く、北陸や関東北部、東北南部付近で雨の降る所があるでしょう。関東南部でも一部でにわか雨がありそうです。日中は、西・東日本を中心に次第に大気の状態が不安定となる見込みです。特に内陸部や山沿いで雨雲・雷雲が発達しやすいでしょう。山や川のレジャーは空模様の変化に十分注意してください。九州南部や北海道は安定して晴れる所が多い見通しです。沖縄は先島諸島を中心に雨や風が強まるでしょう。強風や高波にも注意が必要です。",
                "en": "In eastern Japan and southern Tohoku, clouds will be numerous from morning, and rain is likely in Hokuriku, northern Kanto, and near southern Tohoku. Even in southern Kanto, scattered showers are likely. During the day, the atmosphere is expected to gradually become unstable mainly in western and eastern Japan. Rain clouds and thunderclouds are especially likely to develop inland and along mountain areas. For leisure in the mountains and rivers, please pay close attention to changes in the weather. In southern Kyushu and Hokkaido, many places are forecast to be stably sunny. In Okinawa, rain and wind will strengthen mainly around the Sakishima Islands. Caution is also needed against strong winds and high waves.",
                "literal": "东部日本和东北南部从早晨起云量多，北陆、关东北部、东北南部附近将有降雨的地方吧。关东南部也有一部分地区似会出现骤雨。白天以西部和东部日本为中心，大气状态将逐渐变得不稳定。特别是内陆和沿山地区雨云和雷云容易发展吧。山区和河川的休闲活动请充分注意天气变化。九州南部和北海道晴朗稳定的地方较多。冲绳以先岛群岛为中心雨和风将增强。也需要注意强风和大浪。",
                "grammar": "「〜ありそうです」— 看起来会有…。例：にわか雨がありそうです（看起来会有骤雨）。\n「〜やすいでしょう」— 容易…吧。例：発達しやすいでしょう（容易发展吧）。\n「〜てください」— 请…。例：十分注意してください（请充分注意）。",
                "vocab": [["雲", "くも", "云"], ["にわか雨", "にわかあめ", "骤雨"], ["大気", "たいき", "大气"], ["不安定", "ふあんてい", "不稳定"], ["発達", "はったつ", "发展、增强"], ["空模様", "そらもよう", "天气状况"], ["高波", "たかなみ", "大浪"]]
            },
            {
                "ja": "昼間は全国的に厳しい暑さです。予想最高気温は札幌31℃、旭川・帯広30℃と、北海道でも30℃以上の真夏日になる所があるでしょう。東海～九州では35℃以上の猛暑日になる所がある見込みです。日田(大分)39℃、久留米(福岡)・佐賀38℃、奈良・熊本37℃と危険な暑さになる所もある見通しです。23日(日)も東海から九州で猛暑が続く見込みです。この土日も熱中症対策を万全にしてお過ごしください。",
                "en": "During the day, it will be severely hot nationwide. Forecast maximum temperatures are 31°C in Sapporo and 30°C in Asahikawa and Obihiro, so even in Hokkaido some places will see midsummer days of 30°C or higher. From Tokai to Kyushu, some places are expected to see extreme heat days of 35°C or higher. Places such as Hita (Oita) at 39°C, Kurume (Fukuoka) and Saga at 38°C, and Nara and Kumamoto at 37°C are forecast to be dangerously hot. On Sunday the 23rd as well, extreme heat is expected to continue from Tokai to Kyushu. Please take complete heatstroke precautions this weekend too.",
                "literal": "白天全国性酷暑。预计最高气温札幌31度、旭川・带广30度，北海道也有达到30度以上的盛夏日吧。东海至九州预计有达到35度以上的猛暑日的地方。日田（大分）39度、久留米（福冈）・佐贺38度、奈良・熊本37度，也有地方预计将出现危险的炎热。23日（周日）东海至九州的酷暑也将持续。这个周末也请做好万全的防中暑对策度过。",
                "grammar": "「〜見込みです」— 预计…。例：猛暑日になる所がある見込みです（预计有出现猛暑日的地方）。\n「〜見通しです」— 预计、预料…。例：危険な暑さになる所もある見通しです（预计也有出现危险炎热的地方）。\n「〜てお過ごしください」— 请（敬语）…度过。例：万全にしてお過ごしください（请做好万全准备度过）。",
                "vocab": [["予想", "よそう", "预测"], ["最高気温", "さいこうきおん", "最高气温"], ["真夏日", "まなつび", "盛夏日（最高气温30度以上）"], ["危険", "きけん", "危险"], ["熱中症", "ねっちゅうしょう", "中暑"], ["対策", "たいさく", "对策"], ["万全", "ばんぜん", "万全"]]
            },
        ]
    },
    {
        "slug": "saitama-mouretsu-ame-suibotsu",
        "title": "埼玉で猛烈な雨 車水没訴える通報相次ぐ 記録的短時間大雨",
        "subtitle": "from 読売新聞オンライン",
        "paras": [
            {
                "ja": "暖かく湿った空気が前線に流れ込んだ影響で、埼玉県内は21日、1時間当たりの雨量が100ミリを超える猛烈な雨に見舞われた。道路の冠水が相次ぎ、車の水没を訴える110番が相次いだ。",
                "en": "Due to the influence of warm, humid air flowing into the front, Saitama Prefecture was hit on the 21st by torrential rain exceeding 100 millimeters per hour. Road flooding occurred one after another, and 110 emergency calls reporting submerged cars followed in succession.",
                "literal": "因温暖潮湿的空气流入锋面的影响，埼玉县内21日遭遇了每小时雨量超过100毫米的猛烈暴雨。道路积水接连发生，报告汽车被水淹的110报警接连不断。",
                "grammar": "「〜に見舞われた」— 遭受了…。例：猛烈な雨に見舞われた（遭受了猛烈暴雨）。\n「〜当たり」— 每…。例：1時間当たりの雨量（每小时的雨量）。\n「〜相次いだ」— 接连发生。例：冠水が相次ぎ（积水接连发生）。",
                "vocab": [["湿った", "しめった", "潮湿的"], ["前線", "ぜんせん", "锋面（气象）"], ["雨量", "うりょう", "雨量"], ["猛烈", "もうれつ", "猛烈、凶猛"], ["冠水", "かんすい", "积水、淹水"], ["水没", "すいぼつ", "淹没、浸水"]]
            },
            {
                "ja": "気象庁のレーダー解析によると、さいたま市周辺では21日午後4時20分までの1時間に110ミリの雨を観測。同庁は災害の危険性が高まっているとして、記録的短時間大雨情報を発表した。道路の冠水が相次いだのは、同県上尾市やさいたま市。県警によると、同日午後7時までに「車両が水没した」という趣旨の110番が22件あった。",
                "en": "According to the Japan Meteorological Agency's radar analysis, 110 mm of rain was observed in the vicinity of Saitama City in the one hour up to 4:20 p.m. on the 21st. The agency issued a record-breaking short-term heavy rain advisory, saying the danger of disaster was increasing. Roads flooded mainly in Ageo City and Saitama City in the prefecture. According to the prefectural police, by 7 p.m. that day there had been 22 emergency calls reporting that \"vehicles were submerged.\"",
                "literal": "根据气象厅的雷达解析，埼玉市周边21日下午4点20分之前的1小时内观测到110毫米降雨。该厅以灾害危险性正在升高为由，发布了创纪录短时间大雨信息。道路接连积水的是该县上尾市和埼玉市。据县警称，截至当天下午7点，以「车辆被水淹」为内容的110报警有22件。",
                "grammar": "「〜によると」— 根据…。例：レーダー解析によると（根据雷达解析）。\n「〜として」— 以…为由。例：危険性が高まっているとして（以危险性升高为由）。\n「〜という趣旨の」— 内容为…的。例：水没したという趣旨の110番（内容为被水淹的报警）。",
                "vocab": [["気象庁", "きしょうちょう", "气象厅"], ["レーダー", "れーだー", "雷达"], ["観測", "かんそく", "观测"], ["災害", "さいがい", "灾害"], ["記録的", "きろくてき", "创纪录的"], ["車両", "しゃりょう", "车辆"], ["県警", "けんけい", "县警察"]]
            },
            {
                "ja": "同市北区の埼玉新都市交通ニューシャトル吉野原駅前では、乗用車1台が水につかって動けなくなった。運転していた40歳代男性会社員によると、午後5時頃、突然激しい雨が降り始めたという。車がくぼんだ形状の地点にさしかかったところ、タイヤが水につかり始め、その後、エンジンが停止。ドアノブまで水位があったため、窓から外に飛び出たという。男性は「千葉の大雨が頭にあり、命の危険を感じた」と話した。",
                "en": "In front of Yoshinohara Station on the Saitama New Urban Transit New Shuttle in Kita Ward of the city, one passenger car got stuck in water and could not move. According to the male office worker in his 40s who was driving, heavy rain suddenly began to fall around 5 p.m. When the car reached a sunken spot in the road, the tires began to be submerged, and then the engine stopped. Because the water level reached the door handles, he jumped out through the window. The man said, \"The heavy rain in Chiba was on my mind, and I feared for my life.\"",
                "literal": "在该市北区埼玉新都市交通新穿梭吉野原站前，1辆轿车被水淹住无法动弹。据开车的40多岁男性公司职员称，下午5点左右突然下起了大雨。车子驶到凹陷形状的地点时，轮胎开始被水淹，之后引擎停止。因为水位到了车门把手，据称从车窗跳了出去。男子说「脑子里浮现千叶的大雨，感到了生命危险」。",
                "grammar": "「〜によると」— 根据…。例：男性会社員によると（据该男性公司职员称）。\n「〜ところ」— 正…的时候。例：さしかかったところ（正驶到…之时）。\n「〜ため」— 因为…。例：水位があったため（因为水位高）。",
                "vocab": [["乗用車", "じょうようしゃ", "轿车、乘用车"], ["会社員", "かいしゃいん", "公司职员"], ["激しい", "はげしい", "猛烈的"], ["くぼむ", "くぼむ", "凹陷"], ["タイヤ", "たいや", "轮胎"], ["エンジン", "えんじん", "引擎"], ["水位", "すいい", "水位"]]
            },
        ]
    },
    {
        "slug": "suimin-biyou-risuku-kennen",
        "title": "睡眠美容巡り 専門家らリスク懸念 睡眠薬処方の例も",
        "subtitle": "from 時事通信",
        "paras": [
            {
                "ja": "睡眠の質を高めて美肌を目指す―。SNSで「睡眠美容」と呼ばれる自由診療が、一部のクリニックで提供されている。依存性がある向精神薬などを処方するケースもあり、医療用医薬品の適正使用について専門家から懸念の声が上がっている。",
                "en": "Improving the quality of sleep to aim for beautiful skin — a self-paid treatment called \"sleep beauty\" on social media is being offered at some clinics. There are cases in which addictive psychotropic drugs and other medications are prescribed, and experts are raising concerns about the appropriate use of prescription medicines.",
                "literal": "提高睡眠质量以追求美肌——在SNS上被称为「睡眠美容」的自费诊疗正被一部分诊所提供。也存在处方有成瘾性的精神药物等的情况，关于医疗药品的适当使用，专家们的担忧之声正在高涨。",
                "grammar": "「〜を目指す」— 以…为目标。例：美肌を目指す（以美肌为目标）。\n「〜と呼ばれる」— 被称为…。例：「睡眠美容」と呼ばれる（被称为「睡眠美容」）。\n「〜ケースもあり」— 也有…的情况。例：処方するケースもあり（也有处方的情况）。",
                "vocab": [["質", "しつ", "质量"], ["美肌", "びはだ", "美肌、美丽肌肤"], ["自由診療", "じゆうしんりょう", "自费诊疗"], ["クリニック", "くりにっく", "诊所"], ["依存性", "いぞんせい", "成瘾性、依赖性"], ["向精神薬", "こうせいしんやく", "精神药物"], ["懸念", "けねん", "担忧"]]
            },
            {
                "ja": "睡眠美容に医学的な定義はなく、十分な睡眠によって肌の状態やホルモン分泌を整え、美容につなげる考え方を指す。近年は睡眠をキーワードにした化粧品やサプリメントなどの商品・サービスが相次ぎ、こうした流れを背景にクリニックでも自由診療として取り入れる動きが見られるようになった。一部のクリニックでは昨年ごろから「質の良い睡眠でキレイをつくる」などとうたい、睡眠薬や向精神薬を処方する例が出ている。",
                "en": "Sleep beauty has no medical definition; it refers to the idea of regulating skin condition and hormone secretion through sufficient sleep and linking that to beauty. In recent years, products and services such as cosmetics and supplements featuring sleep as a keyword have appeared one after another, and against this backdrop, clinics have come to adopt it as self-paid treatment. At some clinics, beginning around last year, examples have emerged of advertising slogans like \"Create beauty with quality sleep\" and prescribing sleeping pills and psychotropic drugs.",
                "literal": "睡眠美容没有医学定义，指的是通过充足的睡眠调整肌肤状态和荷尔蒙分泌、与美容相连接的想法。近年来以睡眠为关键词的化妆品和保健品等商品・服务接连出现，以这一潮流为背景，诊所也开始出现将其作为自费诊疗引入的动向。一部分诊所从去年左右起宣传「以优质睡眠创造美丽」等，出现处方安眠药和精神药物的例子。",
                "grammar": "「〜によって」— 通过…、根据…。例：十分な睡眠によって（通过充足的睡眠）。\n「〜を背景に」— 以…为背景。例：こうした流れを背景に（以这一潮流为背景）。\n「〜ようになった」— 变得…了。例：見られるようになった（变得能看到）。",
                "vocab": [["定義", "ていぎ", "定义"], ["ホルモン", "ほるもん", "荷尔蒙"], ["分泌", "ぶんぴつ", "分泌"], ["化粧品", "けしょうひん", "化妆品"], ["サプリメント", "さぷりめんと", "保健品、补充剂"], ["睡眠薬", "すいみんやく", "安眠药"], ["処方", "しょほう", "处方"]]
            },
            {
                "ja": "睡眠薬は本来、不眠症などの治療に用いられる。一部は向精神薬にも指定され、依存性や眠気、ふらつきなどの副作用に注意が必要だ。日本睡眠学会の診療ガイドラインでは、適正使用や漫然とした長期投与は避けるよう推奨している。",
                "en": "Sleeping pills are originally used to treat conditions such as insomnia. Some are also designated as psychotropic drugs, and caution is needed against side effects such as addiction, drowsiness, and light-headedness. The clinical guidelines of the Japan Sleep Society recommend appropriate use and avoiding careless long-term administration.",
                "literal": "安眠药本来用于失眠症等的治疗。一部分也被指定为精神药物，需要注意成瘾性、困倦、摇晃不稳等副作用。日本睡眠学会的诊疗指南推荐适当使用、避免漫不经心的长期给药。",
                "grammar": "「〜に用いられる」— 被用于…。例：治療に用いられる（被用于治疗）。\n「〜に指定され」— 被指定为…。例：向精神薬にも指定され（也被指定为精神药物）。\n「〜よう推奨している」— 推荐（那样做）。例：避けるよう推奨している（推荐避免…）。",
                "vocab": [["不眠症", "ふみんしょう", "失眠症"], ["治療", "ちりょう", "治疗"], ["眠気", "ねむけ", "困倦"], ["ふらつき", "ふらつき", "摇晃、头晕"], ["副作用", "ふくさよう", "副作用"], ["ガイドライン", "がいどらいん", "指南"], ["長期", "ちょうき", "长期"]]
            },
            {
                "ja": "同学会理事長の内村直尚・久留米大学長は「睡眠薬は不眠症の治療薬。治療でも、まず生活習慣の改善などを行い、改善しない場合に使用を検討するのが基本だ」と指摘。その上で「不適正な使い方をすると、依存性が生じたり、眠気や筋弛緩による転倒などの副作用につながったりする可能性がある。美容目的で安易に使用すべきではない」と注意を呼び掛けている。",
                "en": "Naohisa Uchimura, president of the society and president of Kurume University, pointed out, \"Sleeping pills are a treatment for insomnia. Even in treatment, the basic approach is to first improve lifestyle habits, and consider using them only when improvement is not seen.\" He added, \"If used inappropriately, it can lead to addiction or side effects such as drowsiness and falls due to muscle relaxation. They should not be used carelessly for beauty purposes,\" urging caution.",
                "literal": "该学会理事长・久留米大学校长内村直尚指出「安眠药是失眠症的治疗药物。即使是治疗，首先进行生活习惯的改善等，未改善的情况下才考虑使用，这是基本」。在此基础上呼吁注意「若使用方式不当，可能产生依赖性或导致困倦、因肌肉松弛而跌倒等副作用。不应以美容目的随意使用」。",
                "grammar": "「〜のが基本だ」— …是基本。例：使用を検討するのが基本だ（考虑使用是基本）。\n「〜たり、〜たりする」— …或…（列举）。例：生じたり、つながったりする（产生…或导致…）。\n「〜べきではない」— 不应该…。例：使用すべきではない（不应该使用）。",
                "vocab": [["理事長", "りじちょう", "理事长"], ["生活習慣", "せいかつしゅうかん", "生活习惯"], ["改善", "かいぜん", "改善"], ["不適正", "ふてきせい", "不当、不合适"], ["筋弛緩", "きんしかん", "肌肉松弛"], ["転倒", "てんとう", "跌倒"], ["安易", "あんい", "轻率、随意"]]
            },
        ]
    },
    {
        "slug": "houmushou-rabu-joutou-chuushi",
        "title": "法務省 「ラヴ上等」タイアップ取りやめ 批判相次ぎ",
        "subtitle": "from FNNプライムオンライン（フジテレビ系）",
        "paras": [
            {
                "ja": "法務省は、Netflixの恋愛リアリティショー「ラヴ上等」とタイアップしたポスターについて、批判が相次いだことなどから、タイアップを取りやめると発表しました。",
                "en": "The Ministry of Justice announced that it will cancel its tie-up with the Netflix romance reality show \"Love Jōtō,\" citing among other things the succession of criticism over the tie-up poster.",
                "literal": "法务省就与Netflix恋爱真人秀「ラヴ上等」合作的海报，以接连出现批判等为由，宣布中止合作。",
                "grammar": "「〜について」— 关于…。例：タイアップしたポスターについて（关于合作的海报）。\n「〜ことなどから」— 以…等为由。例：批判が相次いだことなどから（以批判接连不断等为由）。\n「〜と発表しました」— 宣布了…。例：取りやめると発表しました（宣布将中止）。",
                "vocab": [["法務省", "ほうむしょう", "法务省"], ["タイアップ", "たいあっぷ", "合作、联动"], ["ポスター", "ぽすたー", "海报"], ["批判", "ひはん", "批判、批评"], ["相次ぐ", "あいつぐ", "接连发生"], ["取りやめる", "とりやめる", "中止、取消"]]
            },
            {
                "ja": "Netflixの恋愛リアリティショー「ラヴ上等」は、いわゆる\"ヤンキー\"の男女たちが恋愛や友情を通じて過去と向き合い成長していく恋愛番組で、法務省保護局は「更生保護」の取り組みと「『ラヴ上等』シーズン2」とがタイアップしたポスターを8月上旬に発表しました。",
                "en": "\"Love Jōtō,\" Netflix's romance reality show, is a love program in which so-called \"yankee\" men and women confront their past through love and friendship and grow. The Ministry of Justice's Rehabilitation Bureau released the poster, a tie-up between its \"rehabilitation protection\" efforts and \"Love Jōtō Season 2,\" in early August.",
                "literal": "Netflix恋爱真人秀「ラヴ上等」是所谓\"不良少年少女\"的男女们通过恋爱和友情直面过去、不断成长的恋爱节目，法务省保护局于8月上旬发布了将「更生保护」举措与「『ラヴ上等』第二季」合作的海报。",
                "grammar": "「〜を通じて」— 通过…。例：恋愛や友情を通じて（通过恋爱和友情）。\n「〜と向き合い」— 直面…。例：過去と向き合い（直面过去）。\n「〜上旬に」— 在…上旬。例：8月上旬に発表しました（在8月上旬发布）。",
                "vocab": [["リアリティショー", "りありてぃしょー", "真人秀"], ["ヤンキー", "やんきー", "不良少年少女（混混风格）"], ["友情", "ゆうじょう", "友情"], ["向き合う", "むきあう", "面对、直面"], ["更生保護", "こうせいほご", "更生保护（对出狱者的援助）"], ["取り組み", "とりくみ", "举措、努力"], ["上旬", "じょうじゅん", "上旬"]]
            },
            {
                "ja": "このタイアップについて、法務省は「広く更生保護の取組を知っていただき、生きづらさを抱える人々の立ち直りを愛（ラヴ）を持って応援していただけることを願っています」としていましたが、その後、SNSなどで多くの反響を呼び「犯罪被害に遭われた方に不快感や割り切れない思いを抱かれるのではないか」などという批判が相次いだということです。",
                "en": "Regarding this tie-up, the Ministry of Justice had said, \"We hope that many people will learn about rehabilitation protection efforts and support with love the recovery of people struggling to live,\" but afterward it drew a large response on social media, and criticism followed one after another, such as \"Might victims of crime feel discomfort or unresolved feelings?\"",
                "literal": "关于这一合作，法务省此前表示「希望广泛地让大家了解更生保护的举措，怀着爱（LOVE）支持那些生活艰难之人的重新站起来」，但之后在SNS等引起大量反响，「会不会让遭遇犯罪受害的人感到不快或难以释怀」等批判接连不断。",
                "grammar": "「〜知っていただき」— 敬请（让您）知晓（敬语）。例：取組を知っていただき（敬请了解举措）。\n「〜を願っています」— 衷心希望…。例：応援していただけることを願っています（希望得到支持）。\n「〜のではないか」— 会不会…（委婉担忧）。例：抱かれるのではないか（会不会感到…）。",
                "vocab": [["生きづらさ", "いきづらさ", "生活艰难、难以生存"], ["立ち直り", "たちなおり", "重新振作、东山再起"], ["願う", "ねがう", "希望、祈愿"], ["反響", "はんきょう", "反响"], ["被害", "ひがい", "受害"], ["不快感", "ふかいかん", "不快感"], ["割り切れない", "わりきれない", "难以释怀、无法想通"]]
            },
            {
                "ja": "これを受けて法務省は21日午後、タイアップを取りやめると発表しました。全国の更生保護施設にポスターの張り出しをやめるよう周知したということです。今回の判断について、法務省は「この作品に出演されている皆様を始め、生きづらさを抱える方々が直面する困難や、過去に罪を犯した人の更生への取組を否定するものではない」としています。",
                "en": "In response, the Ministry of Justice announced on the afternoon of the 21st that it would cancel the tie-up. It notified rehabilitation protection facilities nationwide to stop posting the poster. Regarding this decision, the ministry stated, \"This is not a denial of the difficulties faced by people struggling to live, including everyone appearing in this work, or of the efforts toward rehabilitation of people who have committed crimes in the past.\"",
                "literal": "受此影响，法务省于21日下午宣布中止合作，并已通知全国更生保护设施停止张贴海报。关于此次判断，法务省表示「并非否定以出演本作品的各位为首、生活艰难的人们所面临的困难，以及过去犯罪之人的更生举措」。",
                "grammar": "「〜を受けて」— 受…影响、据此。例：これを受けて（受此影响）。\n「〜よう周知した」— 通知（让大家）…。例：やめるよう周知した（通知停止…）。\n「〜ものではない」— 并非…。例：否定するものではない（并非否定…）。",
                "vocab": [["施設", "しせつ", "设施"], ["張り出し", "はりだし", "张贴"], ["周知", "しゅうち", "通知、周知"], ["判断", "はんだん", "判断、决定"], ["出演", "しゅつえん", "出演"], ["困難", "こんなん", "困难"], ["罪を犯す", "つみをおかす", "犯罪"]]
            },
        ]
    },
    {
        "slug": "icc-syokuchou-seisai-europe",
        "title": "ICCの所長制裁に欧州各国が反発強める 対抗策求める声",
        "subtitle": "from 時事通信",
        "paras": [
            {
                "ja": "国際刑事裁判所（ICC、本部オランダ・ハーグ）の赤根智子所長らを対象としたトランプ米政権の制裁措置を巡り、欧州各国が反発を強めている。赤根氏らへの連帯を表明する国が相次ぎ、ICCの独立性を支持する声が拡大。欧州連合（EU）による制裁への対抗策も浮上するが、実施に踏み切れるかは不透明だ。",
                "en": "Over the sanctions imposed by the Trump administration targeting ICC President Tomoko Akane and others at the International Criminal Court (ICC, based in The Hague, Netherlands), European countries are increasingly pushing back. Nations expressing solidarity with Akane and her colleagues are appearing one after another, and voices supporting the ICC's independence are growing. Countermeasures against the sanctions by the European Union (EU) are emerging, but whether they can be implemented remains unclear.",
                "literal": "围绕以国际刑事法院（ICC、总部荷兰海牙）院长赤根智子等人为对象的特朗普美国政权制裁措施，欧洲各国正在加强反对。表明对赤根等人团结支持的国家接连出现，支持ICC独立性的声音在扩大。欧盟（EU）对制裁的对抗措施也在浮出水面，但能否付诸实施尚不明朗。",
                "grammar": "「〜を対象とした」— 以…为对象的。例：制裁措置を巡り（围绕制裁措施）。\n「〜を巡り」— 围绕…。例：制裁措置を巡り（围绕制裁措施）。\n「〜かは不透明だ」— 是否…尚不明朗。例：踏み切れるかは不透明だ（能否实施尚不明朗）。",
                "vocab": [["国際刑事裁判所", "こくさいけいじさいばんしょ", "国际刑事法院（ICC）"], ["制裁", "せいさい", "制裁"], ["措置", "そち", "措施"], ["反発", "はんぱつ", "反对、反弹"], ["連帯", "れんたい", "团结、连带"], ["独立性", "どくりつせい", "独立性"], ["対抗策", "たいこうさく", "对抗措施"]]
            },
            {
                "ja": "「ICCの独立性、完全性、公平性に対するあからさまな攻撃だ」。スペイン外務省は19日の声明で赤根氏らへの「全面的な連帯」を表明し、ICCの「解体」をもくろむトランプ政権を強く非難した。こうした動きはスペインにとどまらない。ベルギーのプレボ外相も20日、制裁は「（犯罪の責任を問われない）不処罰との世界的な闘いを弱める」と批判。ICC本部があるオランダのベーレンドセン外相も「国際裁判所・法廷は自由に任務を遂行できなければならない」と訴え、ICC支持を前面に出している。",
                "en": "\"This is a blatant attack on the ICC's independence, integrity, and impartiality.\" In a statement on the 19th, Spain's Foreign Ministry expressed \"full solidarity\" with Akane and others, strongly condemning the Trump administration, which aims at the \"dismantlement\" of the ICC. Such moves are not limited to Spain. Belgian Foreign Minister Prévot also criticized on the 20th that the sanctions \"weaken the global fight against impunity (where crimes go unpunished).\" The Dutch Foreign Minister, whose country hosts the ICC headquarters, also appealed that \"international courts and tribunals must be able to carry out their tasks freely,\" putting support for the ICC at the forefront.",
                "literal": "「这是对ICC独立性、完整性、公正性的公然攻击」。西班牙外交部在19日的声明中表明对赤根等人的「全面团结」，强烈谴责企图「解体」ICC的特朗普政权。此类动向不止于西班牙。比利时的普雷沃外相20日也批评制裁「削弱了（犯罪责任不被追究的）有罪不罚现象与世界的斗争」。拥有ICC总部的荷兰外相也呼吁「国际法院・法庭必须能自由执行任务」，将支持ICC摆在台前。",
                "grammar": "「〜に対する」— 对…的。例：公平性に対する攻撃（对公正性的攻击）。\n「〜にとどまらない」— 不止于…。例：スペインにとどまらない（不止于西班牙）。\n「〜なければならない」— 必须…。例：遂行できなければならない（必须能够执行）。",
                "vocab": [["完全性", "かんぜんせい", "完整性"], ["公平性", "こうへいせい", "公正性、公平性"], ["あからさま", "あからさま", "露骨的、公然的"], ["全面的", "ぜんめんてき", "全面的"], ["解体", "かいたい", "解体"], ["もくろむ", "もくろむ", "图谋、企图"], ["非難", "ひなん", "谴责、非难"]]
            },
            {
                "ja": "ICCはこれまで、ウクライナに侵攻したロシアのプーチン大統領や、パレスチナ自治区ガザを攻撃したイスラエルのネタニヤフ首相に対する逮捕状を発付。ネタニヤフ氏との密接な関係を築くトランプ大統領は強く反発し、ICCの裁判官や検察官らに制裁を相次いで科してきた。",
                "en": "The ICC has so far issued arrest warrants for Russian President Putin, who invaded Ukraine, and Israeli Prime Minister Netanyahu, who attacked Gaza in the Palestinian territory. President Trump, who has built a close relationship with Netanyahu, has strongly pushed back, repeatedly imposing sanctions on ICC judges and prosecutors.",
                "literal": "ICC迄今已对入侵乌克兰的俄罗斯总统普京、以及攻击巴勒斯坦自治区加沙的以色列总理内塔尼亚胡发出逮捕令。与内塔尼亚胡建立紧密关系的特朗普总统强烈反对，接连对ICC法官和检察官等施加制裁。",
                "grammar": "「〜に侵攻した」— 入侵了…的。例：ウクライナに侵攻した（入侵了乌克兰的）。\n「〜に対する」— 对…的。例：首相に対する逮捕状（对总理的逮捕令）。\n「〜てきた」— 一直…（持续至今）。例：科してきた（一直施加至今）。",
                "vocab": [["侵攻", "しんこう", "入侵"], ["大統領", "だいとうりょう", "总统"], ["逮捕状", "たいほじょう", "逮捕令"], ["発付", "はっぷ", "签发、发出"], ["密接", "みっせつ", "密切"], ["検察官", "けんさつかん", "检察官"], ["科する", "かする", "施加（刑罚等）"]]
            },
            {
                "ja": "今後は欧州各国が打ち出したICCへの支持を具体的な形として示せるかが焦点となる。欧州の一部では、米国など第三国の制裁がEU域内の企業や個人に及ぼす影響を抑える「ブロッキング規則」の発動を求める声も上がっている。だが、EUが対抗措置を講じれば、米国との亀裂が一層深まるのは必至。EU欧州委員会報道官は20日の記者会見で「最新の制裁の影響を注視している」と述べるにとどめ、ブロッキング規則の発動の可能性については言及を避けた。",
                "en": "Going forward, the focus will be on whether European countries can show their support for the ICC in concrete form. In parts of Europe, voices are rising calling for the activation of the \"Blocking Statute,\" which curbs the impact of sanctions by third countries such as the United States on companies and individuals within the EU. However, if the EU takes countermeasures, it is certain that the rift with the United States will deepen further. An EU Commission spokesperson, at a press conference on the 20th, only said that it is \"closely monitoring the impact of the latest sanctions,\" and avoided mentioning the possibility of activating the Blocking Statute.",
                "literal": "今后焦点在于欧洲各国能否以具体形式展示对ICC的支持。欧洲一部分地区也出现了要求发动「阻断规则」的声音，该规则用以抑制美国等第三国制裁对欧盟域内企业和个人的影响。但若EU采取对抗措施，与美国之间的裂痕必将进一步加深。欧盟委员会发言人20日在记者会上仅表示「正密切关注最新制裁的影响」，对发动阻断规则的可能性避而不谈。",
                "grammar": "「〜が焦点となる」— …成为焦点。例：示せるかが焦点となる（能否展示成为焦点）。\n「〜を求める声も上がっている」— 也出现了要求…的声音。例：発動を求める声も上がっている（也出现了要求发动的呼声）。\n「〜にとどめ」— 仅止于…。例：述べるにとどめ（仅止于述说）。",
                "vocab": [["具体的", "ぐたいてき", "具体的"], ["焦点", "しょうてん", "焦点"], ["第三国", "だいさんこく", "第三国"], ["及ぼす", "およぼす", "施加、波及"], ["発動", "はつどう", "发动、启动"], ["亀裂", "きれつ", "裂痕、裂口"], ["言及", "げんきゅう", "提及"]]
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