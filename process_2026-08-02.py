#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-02 (Sun) Edition"""
import json, os, subprocess, re, time
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-02'
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
# TODAY'S ARTICLES — 2026-08-02
# ==================================================================
articles = [
    {
        "slug": "moushobi-kumamoto-40do",
        "title": "2日は300超の地点で猛暑日か 週明けは熊本で統計史上初の40℃",
        "subtitle": "2日(日)は今年最多となる300を超える地点で猛暑日となる予想。九州や東海では40℃以上の酷暑日のおそれがあり、週明け3日(月)には熊本で統計史上初めて40℃に達する可能性がある。",
        "paras": [
            {
                "ja": "2日(日)は、今年最多となる300を超える地点で35℃以上の猛暑日になる予想です。九州や東海では40℃以上の酷暑日となるおそれもあります。1日(土)も西日本や東日本は猛烈な暑さとなり、静岡県天竜で39.7℃、宮崎県神門では39.5℃を観測しました。神門と西都では、統計史上1位の記録を更新しています。",
                "en": "On Sunday the 2nd, over 300 locations — the most this year — are expected to see temperatures of 35°C or higher (moshobi, \"torrid day\"). Kyushu and Tokai may even see 40°C-plus \"extreme heat days.\" Saturday the 1st was also fiercely hot in western and eastern Japan, with 39.7°C observed in Tenryu, Shizuoka Prefecture, and 39.5°C in Kando, Miyazaki Prefecture. Kando and Saito both updated their all-time records.",
                "literal": "2日（周日），预计今年最多的超过300个地点将达到35度以上的猛暑日。九州和东海也有达到40度以上酷暑日的可能。1日（周六）西日本和东日本也出现了猛烈的炎热，静冈县天龙观测到39.7度，宫崎县神门观测到39.5度。神门和西都更新了统计史上第一位的记录。",
                "grammar": "「〜となる予想です」— 预计将变成…。例：猛暑日になる予想です（预计将变成猛暑日）。\n「〜おそれもあります」— 也有…的危险。例：酷暑日となるおそれもあります（也有变成酷暑日的危险）。\n「〜では」— 在…（场所）。例：静岡県天竜では39.7℃（在静冈县天龙为39.7度）。",
                "vocab": [
                    ["猛暑日", "もうしょび", "猛暑日（35度以上）"],
                    ["酷暑日", "こくしょび", "酷暑日（40度以上）"],
                    ["地点", "ちてん", "地点"],
                    ["猛烈", "もうれつ", "猛烈、剧烈"],
                    ["観測", "かんそく", "观测"],
                    ["記録を更新", "きろくをこうしん", "刷新纪录"]
                ]
            },
            {
                "ja": "九州は週明け3日(月)にかけても酷暑日となる可能性があり、熊本では1890年からの統計史上初めて40℃に達するかもしれません。東海では、週後半に再び40℃以上の酷暑日が続出するおそれがあります。一方、関東では週明け以降、北東からの涼しい風が流れ込み、猛烈な暑さはおさまる見込みです。",
                "en": "Kyushu may remain at extreme-heat level into Monday the 3rd, and Kumamoto could reach 40°C for the first time in its statistics dating back to 1890. In Tokai, extreme heat days of 40°C or more may recur in the latter half of the week. In Kanto, meanwhile, cool breezes from the northeast are expected to flow in from early next week, easing the fierce heat.",
                "literal": "九州到下周初的3日（周一）也有持续酷暑日的可能性，熊本有可能达到1890年以来统计史上首次的40度。东海方面，下周后半段有再次接连出现40度以上酷暑日的危险。另一方面，关东从下周初开始，来自东北方向的凉风流入，猛烈的炎热预计将平息。",
                "grammar": "「〜かもしれません」— 也许、可能。例：40℃に達するかもしれません（也许会达到40度）。\n「〜一方」— 另一方面。例：一方、関東では（另一方面，在关东）。\n「〜見込みです」— 预计将…。例：おさまる見込みです（预计将平息）。",
                "vocab": [
                    ["可能性", "かのうせい", "可能性"],
                    ["統計史上", "とうけいしじょう", "统计史上"],
                    ["達する", "たっする", "达到"],
                    ["続出", "ぞくしゅつ", "接连出现"],
                    ["流れ込む", "ながれこむ", "流入"],
                    ["見込み", "みこみ", "预计、预期"]
                ]
            },
            {
                "ja": "まだまだ暑さのピークが続きます。周囲と声を掛け合いながら、こまめに水分や塩分を補給し、涼しい環境で過ごしましょう。熊本地震で揺れの大きかった熊本県では、十分な水が使えない場合、冷たいペットボトルや保冷剤で首や脇、手のひらを冷やすとよさそうです。",
                "en": "The peak of the heat will continue for a while. Let's call out to one another, frequently replenish fluids and salt, and spend time in cool environments. In Kumamoto Prefecture, where the shaking from the earthquake was strong, if sufficient water is unavailable, it seems a good idea to cool the neck, armpits, and palms with cold plastic bottles or cooling packs.",
                "literal": "炎热的顶峰还将持续。一边与周围人互相招呼，一边勤快地补充水分和盐分，在凉爽的环境中度过吧。在熊本地震中摇晃很大的熊本县，如果无法使用足够的水，用冰凉的塑料瓶或保冷剂冷却脖子、腋下和手掌似乎比较好。",
                "grammar": "「〜ながら」— 一边…一边…。例：声を掛け合いながら（一边互相招呼）。\n「〜ましょう」— 让我们…吧（劝诱）。例：過ごしましょう（度过吧）。\n「〜とよさそうです」— 好像…比较好。例：冷やすとよさそうです（似乎冷却比较好）。",
                "vocab": [
                    ["ピーク", "ぴーく", "顶峰、最高峰"],
                    ["声を掛け合う", "こえをかけあう", "互相招呼、互相提醒"],
                    ["こまめに", "こまめに", "勤快地、经常地"],
                    ["水分", "すいぶん", "水分"],
                    ["塩分", "えんぶん", "盐分"],
                    ["保冷剤", "ほれいざい", "保冷剂"]
                ]
            }
        ]
    },
    {
        "slug": "risai-shoumeisho-satsuei",
        "title": "熊本地震5日目 「片付ける前に撮影を」罹災証明書申請の注意点",
        "subtitle": "最大震度7の熊本地震から5日目。公的支援を受けるために必要な罹災証明書の申請が始まった。ポイントは「片付ける前に写真を撮ること」。",
        "paras": [
            {
                "ja": "最大震度7を観測した熊本地震から、初めての週末を迎えました。地震による死者は36人に上っています。地震から5日目を迎え、罹災証明の受付が宇城市などでは7月31日から、熊本市では8月1日から始まりました。8月1日も猛暑となる中、復旧に向けた動きも始まっています。",
                "en": "The first weekend has arrived since the Kumamoto earthquake, which recorded a maximum seismic intensity of 7. The death toll from the earthquake has risen to 36. Entering the fifth day since the quake, applications for disaster certificates (risai shomeisho) began on July 31 in Uki City and other municipalities, and on August 1 in Kumamoto City. Even as August 1 brought scorching heat, recovery efforts have begun to move.",
                "literal": "迎来了观测到最大震度7的熊本地震以来的第一个周末。地震造成的死者已达36人。迎来地震后第5天，罹灾证明的受理在宇城市等地从7月31日开始，在熊本市从8月1日开始。8月1日也处于酷暑之中，面向修复的动向也开始启动。",
                "grammar": "「〜を迎えました」— 迎来了…。例：初めての週末を迎えました（迎来了第一个周末）。\n「〜に上っています」— 达到…（数量）。例：死者は36人に上っています（死者达到36人）。\n「〜中」— 在…之中。例：猛暑となる中（在酷暑之中）。",
                "vocab": [
                    ["最大震度", "さいだいしんど", "最大震度"],
                    ["死者", "ししゃ", "死者"],
                    ["罹災証明", "りさいしょうめい", "受灾证明"],
                    ["受付", "うけつけ", "受理、接待"],
                    ["復旧", "ふっきゅう", "修复、恢复"],
                    ["猛暑", "もうしょ", "酷暑"]
                ]
            },
            {
                "ja": "罹災証明書は、住んでいる市町村に申請し、被害の程度を認定してもらう証明書です。税金や公共料金の減免、支援金の給付、仮設住宅への入居など、公的支援を受ける際に必要になります。申請の際には、身分証明書と、被害状況が分かる写真の提出が必要です。",
                "en": "A disaster certificate is a document you apply for from the municipality where you live, to have the extent of damage officially assessed. It is necessary when receiving public support such as reductions or exemptions of taxes and utility bills, payment of support money, and moving into temporary housing. When applying, you must submit identification and photos that show the damage.",
                "literal": "罹灾证明书是向居住的市町村申请、请其认定受害程度的证明书。在接受税金和公共费用的减免、支援金的发放、入住临时住宅等公共支援时是必要的。申请时需要提交身份证件和能看清受灾情况的照片。",
                "grammar": "「〜てもらう」— 请（别人）做…。例：認定してもらう証明書（请人认定的证明书）。\n「〜際に」— 在…的时候。例：公的支援を受ける際に（在接受公共支援时）。\n「〜が必要です」— 需要…。例：写真の提出が必要です（需要提交照片）。",
                "vocab": [
                    ["申請", "しんせい", "申请"],
                    ["認定", "にんてい", "认定"],
                    ["減免", "げんめん", "减免"],
                    ["支援金", "しえんきん", "支援金"],
                    ["仮設住宅", "かせつじゅうたく", "临时住宅"],
                    ["身分証明書", "みぶんしょうめいしょ", "身份证件"]
                ]
            },
            {
                "ja": "提出する写真は「片付ける前に撮影すること」がポイントです。被害認定は「地震でどれだけ壊れたか」を確認してから決まるため、片付けをする前に、できるだけ細かく写真を撮って被害の記録を残すことが大切です。",
                "en": "The key point about the photos you submit is to take them before you clean up. Because the damage assessment is determined after confirming \"how much was broken by the earthquake,\" it is important to photograph the damage in as much detail as possible before cleaning up, leaving a record of the damage.",
                "literal": "提交的照片，「在收拾之前拍摄」是要点。由于受灾认定是在确认「因地震损坏了多少」之后决定的，所以在收拾之前，尽可能细致地拍照留下受灾记录是很重要的。",
                "grammar": "「〜こと」— …这件事（名词化）。例：撮影すること（拍摄这件事）。\n「〜ため」— 因为…。例：確認してから決まるため（因为是在确认之后决定的）。\n「〜ことが大切です」— …是很重要的。例：記録を残すことが大切です（留下记录很重要）。",
                "vocab": [
                    ["片付ける", "かたづける", "收拾、整理"],
                    ["撮影", "さつえい", "拍摄"],
                    ["ポイント", "ぽいんと", "要点、关键"],
                    ["細かく", "こまかく", "细致地"],
                    ["記録を残す", "きろくをのこす", "留下记录"],
                    ["大切", "たいせつ", "重要"]
                ]
            }
        ]
    },
    {
        "slug": "en-kyuushin-nichibei-kainyuu",
        "title": "円急伸、日米で協調介入か 円安是正へ週明け方針表明",
        "subtitle": "日本政府・日銀が円買い介入を実施したことが判明。米ニューヨーク市場では円相場が一時1ドル＝157円24銭まで急伸し、日米両政府が週明けにも円安是正の方針を表明する。",
        "paras": [
            {
                "ja": "日本政府と日銀が1日早朝にかけて、円買い介入を実施したことが分かりました。米国時間では2日連続の介入で、7月31日のニューヨーク外国為替市場では円相場がドルに対し急伸し、一時1ドル＝157円24銭を付けました。これは5月中旬以来、約2カ月半ぶりの円高ドル安水準です。",
                "en": "It has emerged that the Japanese government and the Bank of Japan carried out yen-buying intervention in the early hours of the 1st. It was the second consecutive day of intervention in U.S. trading hours; in the New York foreign exchange market on July 31, the yen surged against the dollar, briefly reaching 157.24 yen per dollar. That was the strongest yen / weakest dollar level in about two and a half months, since mid-May.",
                "literal": "已判明日本政府和日银在1日清晨实施了买入日元的干预。在美国时间这是连续第2天的干预，7月31日的纽约外汇市场上日元兑美元急剧上升，一度达到1美元＝157.24日元。这是自5月中旬以来约2个半月来的日元升值美元贬值水平。",
                "grammar": "「〜にかけて」— 到…为止（时间范围）。例：1日早朝にかけて（到1日清晨为止）。\n「〜が分かりました」— 判明…。例：実施したことが分かりました（判明实施了）。\n「〜ぶり」— 时隔…。例：約2カ月半ぶり（约时隔两个半月）。",
                "vocab": [
                    ["日銀", "にちぎん", "日本银行（央行）"],
                    ["介入", "かいにゅう", "干预"],
                    ["円相場", "えんそうば", "日元汇率"],
                    ["急伸", "きゅうしん", "急剧上升"],
                    ["円高ドル安", "えんだかドルやす", "日元升值美元贬值"],
                    ["水準", "すいじゅん", "水平、水准"]
                ]
            },
            {
                "ja": "英紙フィナンシャル・タイムズは、日米協調介入だったと報じました。日米両政府が早ければ週明けにも、円安の是正に向けた方針を表明することも、当局関係者への取材で分かりました。実需に基づかない投機的な円安に対し、両政府が許容しない姿勢を示し、市場の安定を図る狙いとみられます。",
                "en": "The British newspaper Financial Times reported that it was coordinated Japan-U.S. intervention. It also emerged from interviews with authorities that both governments may announce a policy aimed at correcting the weak yen as early as next week. The move appears intended to show that both governments will not tolerate speculative yen weakness not based on real demand, and to stabilize the market.",
                "literal": "英国《金融时报》报道称这是日美协调干预。通过对当局相关人士的采访也了解到，日美两国政府最早在下周初就可能表明面向纠正日元贬值方针。对于并非基于实际需求的投机性日元贬值，两国政府显示出不容忍的姿态，被认为是谋求市场稳定的意图。",
                "grammar": "「〜と報じました」— 报道称…。例：協調介入だったと報じました（报道称是协调干预）。\n「〜に向けた」— 面向…的。例：是正に向けた方針（面向纠正的方针）。\n「〜とみられます」— 被认为是…。例：狙いとみられます（被认为是有此意图）。",
                "vocab": [
                    ["英紙", "えいし", "英国报纸"],
                    ["協調介入", "きょうちょうかいにゅう", "协调干预"],
                    ["是正", "ぜせい", "纠正、修正"],
                    ["当局", "とうきょく", "当局"],
                    ["実需", "じつじゅ", "实际需求"],
                    ["投機的", "とうきてき", "投机性的"]
                ]
            }
        ]
    },
    {
        "slug": "nisai-danji-yukuefumei",
        "title": "祖母の自宅に帰省中 京都府宇治市の2歳の男の子が行方不明 岡山・矢掛町",
        "subtitle": "岡山県矢掛町で祖母の自宅に帰省していた京都府宇治市の2歳の男の子、中川福仁ちゃんの行方が分からなくなっている。警察や消防など約70人態勢で捜索が行われた。",
        "paras": [
            {
                "ja": "警察によりますと、岡山県矢掛町で、祖母の自宅に帰省していた京都府宇治市の2歳の男の子、中川福仁ちゃんの行方が分からなくなっています。きょう1日午前10時ごろ、祖母が自宅付近で草取りをしていた際、付近で遊んでいる福仁ちゃんを確認していましたが、午前10時半ごろに確認した際、姿が見えなくなっていたということです。",
                "en": "According to police, a 2-year-old boy from Uji City, Kyoto Prefecture — Fukuto Nakagawa — who was visiting his grandmother's home in Yakage Town, Okayama Prefecture, has gone missing. Around 10 a.m. today (the 1st), while his grandmother was weeding near the house, she confirmed Fukuto was playing nearby, but when she checked again around 10:30 a.m., he had disappeared.",
                "literal": "据警方称，在冈山县矢挂町，回祖母家探亲的京都市宇治市的2岁男孩中川福仁的行踪不明。今天（1日）上午10点左右，祖母在自家附近除草时，确认了福仁在附近玩耍，但在上午10点半左右确认时，已经看不见身影了。",
                "grammar": "「〜によりますと」— 据…称。例：警察によりますと（据警方称）。\n「〜際」— 在…的时候。例：草取りをしていた際（在除草的时候）。\n「〜ということです」— 据说…。例：見えなくなっていたということです（据说已经看不见了）。",
                "vocab": [
                    ["帰省", "きせい", "回乡探亲"],
                    ["行方不明", "ゆくえふめい", "下落不明、失踪"],
                    ["草取り", "くさとり", "除草"],
                    ["確認", "かくにん", "确认"],
                    ["姿", "すがた", "身影、姿态"],
                    ["110番通報", "ひゃくとうばんつうほう", "拨打110报警"]
                ]
            },
            {
                "ja": "福仁ちゃんは、母親と2人できのう31日から祖母の自宅に帰省していました。祖母からの110番通報を受けて、警察や家族が行方を捜していますが、発見には至っていません。福仁ちゃんは身長90センチくらい、やせ型で、白色の半袖Tシャツと茶色の半ズボン、青色のスリッパを着用していたということです。",
                "en": "Fukuto had been visiting his grandmother's home with his mother since yesterday, the 31st. After the grandmother's 110 emergency call, police and family have been searching for him, but he has not yet been found. Fukuto is about 90 cm tall, slender, and was reportedly wearing a white short-sleeved T-shirt, brown shorts, and blue slippers.",
                "literal": "福仁和母亲两人从昨天（31日）起回祖母家探亲。接到祖母的110报警后，警方和家人正在搜寻其下落，但尚未找到。福仁身高约90厘米，偏瘦，据称穿着白色半袖T恤、茶色短裤和蓝色拖鞋。",
                "grammar": "「〜てくる」— 来…（表示动作的方向/持续）。例：帰省していました（来探亲了）。\n「〜を受けて」— 接到…之后。例：110番通報を受けて（接到110报警后）。\n「〜には至っていません」— 尚未达到…。例：発見には至っていません（尚未找到）。",
                "vocab": [
                    ["身長", "しんちょう", "身高"],
                    ["やせ型", "やせがた", "偏瘦体型"],
                    ["半袖", "はんそで", "半袖"],
                    ["半ズボン", "はんずぼん", "短裤"],
                    ["スリッパ", "すりっぱ", "拖鞋"],
                    ["着用", "ちゃくよう", "穿着"]
                ]
            },
            {
                "ja": "日中の捜索は警察や消防など約70人態勢で行われました。日没後は一旦規模を縮小し、引き続き福仁ちゃんの行方を捜しています。情報提供は井原警察署に連絡してほしいと呼びかけています。",
                "en": "The daytime search was conducted with a team of about 70 people including police and firefighters. After sunset, the operation was temporarily scaled down, and the search for Fukuto continues. Authorities are asking anyone with information to contact Ibara Police Station.",
                "literal": "白天的搜索以警察和消防等约70人的规模进行。日落后暂时缩小规模，继续搜寻福仁的下落。呼吁有信息提供的人联系井原警察署。",
                "grammar": "「〜態勢で」— 以…的体制。例：約70人態勢で行われました（以约70人的体制进行）。\n「〜一旦」— 暂时、暂且。例：一旦規模を縮小し（暂时缩小规模）。\n「〜てほしい」— 希望（别人）做…。例：連絡してほしい（希望联系）。",
                "vocab": [
                    ["捜索", "そうさく", "搜索"],
                    ["日没", "にちぼつ", "日落"],
                    ["規模", "きぼ", "规模"],
                    ["縮小", "しゅくしょう", "缩小"],
                    ["引き続き", "ひきつづき", "继续"],
                    ["情報提供", "じょうほうていきょう", "提供信息"]
                ]
            }
        ]
    },
    {
        "slug": "puruja-san-setsunai-shibou",
        "title": "著名登山家ニルマル・プルジャさん死亡確認 ブロードピークで雪崩遭遇",
        "subtitle": "ネパールの著名登山家ニルマル・プルジャさん（43）が、パキスタン北部のブロードピークで雪崩に遭い死亡が確認された。登山隊10人は全員死亡したとみられる。",
        "paras": [
            {
                "ja": "ネパールのメディアは1日、同国の著名登山家で、パキスタン北部カラコルム山脈のブロードピーク（8051メートル）で雪崩に遭遇したニルマル・プルジャさん（43）の死亡が確認されたと報じました。プルジャさんが設立した山岳ガイド会社も同日、SNS上で死去を報告しました。",
                "en": "Nepali media reported on the 1st that the death of Nirmal Purja (43), a renowned mountaineer from the country who was caught in an avalanche on Broad Peak (8,051 m) in the Karakoram range of northern Pakistan, had been confirmed. The mountain guiding company Purja founded also reported his death on social media the same day.",
                "literal": "尼泊尔媒体1日报道，该国著名登山家、在巴基斯坦北部喀喇昆仑山脉的布洛阿特峰（8051米）遭遇雪崩的尼尔马尔·普尔亚（43岁）的死亡已得到确认。普尔亚设立的登山向导公司同一天也在SNS上报告了死讯。",
                "grammar": "「〜と報じました」— 报道称…。例：死亡が確認されたと報じました（报道称死亡已确认）。\n「〜で」— 在…（场所）。例：ブロードピークで（在布洛阿特峰）。\n「〜を報告しました」— 报告了…。例：死去を報告しました（报告了死讯）。",
                "vocab": [
                    ["著名", "ちょめい", "著名"],
                    ["登山家", "とざんか", "登山家"],
                    ["雪崩", "なだれ", "雪崩"],
                    ["遭遇", "そうぐう", "遭遇"],
                    ["山岳", "さんがく", "山岳"],
                    ["ガイド会社", "がいどがいしゃ", "向导公司"]
                ]
            },
            {
                "ja": "プルジャさんら計10人から成る登山隊は、7月30日に頂上を目指して登山中、標高6600メートル付近で雪崩に襲われました。現地当局が捜索し、現場付近で複数の遺体を収容しました。登山隊は他にパキスタンや米国、中国などの出身者で構成されていて、生存者はいないということです。",
                "en": "The climbing team of 10 people including Purja was hit by an avalanche around 6,600 meters above sea level on July 30 while ascending toward the summit. Local authorities searched and recovered multiple bodies near the site. The team was otherwise made up of climbers from Pakistan, the United States, China and elsewhere, and there are reportedly no survivors.",
                "literal": "由普尔亚等共10人组成的登山队，7月30日在以山顶为目标登山途中，在海拔约6600米附近遭遇雪崩袭击。当地当局进行了搜索，在现场附近收容了多具遗体。登山队除此之外由巴基斯坦、美国、中国等出身的人构成，据说没有幸存者。",
                "grammar": "「〜から成る」— 由…组成。例：計10人から成る登山隊（由共10人组成的登山队）。\n「〜を目指して」— 以…为目标。例：頂上を目指して登山中（以山顶为目标登山中）。\n「〜に襲われました」— 遭到…袭击。例：雪崩に襲われました（遭到雪崩袭击）。",
                "vocab": [
                    ["頂上", "ちょうじょう", "山顶"],
                    ["標高", "ひょうこう", "海拔"],
                    ["襲う", "おそう", "袭击"],
                    ["当局", "とうきょく", "当局"],
                    ["遺体", "いたい", "遗体"],
                    ["生存者", "せいぞんしゃ", "幸存者"]
                ]
            }
        ]
    },
    {
        "slug": "dena-maki-baachan-homerun",
        "title": "DeNA・牧「ばあちゃんに打たせてもらった」 慶弔休暇明けに祖母へ捧げる本塁打",
        "subtitle": "DeNAの牧秀悟内野手が、慶弔休暇からの復帰戦で祖母の死去を乗り越えてソロ本塁打。「最後、顔が見られて良かった」と語った。",
        "paras": [
            {
                "ja": "「巨人7―8DeNA」（1日、東京ドーム）。DeNAの牧秀悟内野手（28）が三回、左越えにソロ本塁打を放ちました。牧選手は7月31日の巨人戦で、慶弔休暇の特例により出場選手登録を抹消され、この日試合に復帰しました。「母方のおばあちゃんが亡くなって。ずっと昔から世話になったので。最後、顔が見られて良かった」と、長野に住む祖母が86歳で亡くなったことを明かしました。",
                "en": "\"Giants 7-8 DeNA\" (the 1st, Tokyo Dome). DeNA infielder Shugo Maki (28) hit a solo home run over the left-field fence in the third inning. Maki had been removed from the active roster under the special bereavement leave provision for the Giants game on July 31, and returned to the lineup for this game. He revealed that his grandmother, who lived in Nagano, had passed away at age 86: \"My grandmother on my mother's side passed away. She had taken care of me for so long. I'm glad I got to see her face one last time.\"",
                "literal": "「巨人7－8DeNA」（1日，东京巨蛋）。DeNA的内野手牧秀悟（28岁）在第3局击出了越过左外野的阳春本垒打。牧选手因7月31日对巨人战中的庆吊休假特例被从出场选手注册中抹消，于本日复归比赛。「母亲那边的祖母去世了。因为一直以來受到她很多照顾。最后能见到她的脸真是太好了」，他公开了住在长野的祖母以86岁高龄去世的消息。",
                "grammar": "「〜を放ちました」— 击出…。例：ソロ本塁打を放ちました（击出了阳春本垒打）。\n「〜により」— 由于…。例：特例により（根据特例）。\n「〜て良かった」— 做…真是太好了。例：顔が見られて良かった（能见到面真是太好了）。",
                "vocab": [
                    ["内野手", "ないやしゅ", "内野手"],
                    ["本塁打", "ほんるいだ", "本垒打"],
                    ["慶弔休暇", "けいちょうきゅうか", "庆吊休假（红白事假）"],
                    ["抹消", "まっしょう", "注销、抹去"],
                    ["復帰", "ふっき", "复归、回归"],
                    ["明かす", "あかす", "公开、坦白"]
                ]
            },
            {
                "ja": "本塁打を放った直後、牧選手は天を見上げるような仕草を見せました。「打った感触としては、あんまり入る打球じゃないなと思いましたけど、ばあちゃんに打たせてもらったのかなと思います」と、最愛の祖母に捧げる一打となりました。",
                "en": "Immediately after hitting the home run, Maki made a gesture of looking up at the sky. \"My feeling off the bat was that it wasn't really the kind of ball that would go out, but I think maybe my grandma helped me hit it,\" he said — a blow dedicated to his beloved grandmother.",
                "literal": "击出本垒打后立刻，牧选手做出了仰望天空般的动作。「从击球的手感来说，我觉得那不是会飞出去的球，但我想也许是奶奶让我打出去的」，这成为了献给最爱的祖母的一击。",
                "grammar": "「〜直後」— …之后立刻。例：放った直後（击出之后立刻）。\n「〜のかなと思います」— 我觉得也许…。例：打たせてもらったのかなと思います（我想也许是奶奶让我打出去的）。\n「〜に捧げる」— 献给…。例：祖母に捧げる一打（献给祖母的一击）。",
                "vocab": [
                    ["仕草", "しぐさ", "动作、举止"],
                    ["感触", "かんしょく", "手感、感觉"],
                    ["打球", "だきゅう", "击球"],
                    ["最愛", "さいあい", "最爱"],
                    ["捧げる", "ささげる", "献上、奉献"],
                    ["一打", "いちだ", "一击"]
                ]
            },
            {
                "ja": "思い出を振り返り、「足が悪いんですけど、小学校や中学校の時は、よく試合を見に来てくれました。ばあちゃんが作るけんちん汁がめっちゃ好きだったので、そのために帰ったりもしてました」と話していました。",
                "en": "Looking back on his memories, he said, \"She had bad legs, but in elementary and junior high school, she often came to watch my games. I really loved the kenchin soup my grandma made, so I'd even go home for that.\"",
                "literal": "回顾回忆，「奶奶腿脚不好，但小学和中学的时候，她经常来看比赛。因为超喜欢奶奶做的筑前煮汤，所以也会为了那个回家」，他这样说道。",
                "grammar": "「〜んですけど」— …的（说明理由，语气柔和）。例：足が悪いんですけど（腿脚不好，但是…）。\n「〜てくれました」— （别人）为我做…。例：見に来てくれました（来看我比赛了）。\n「〜たり〜たり」— 又…又…（列举）。例：帰ったりもしてました（也会回家）。",
                "vocab": [
                    ["振り返る", "ふりかえる", "回顾"],
                    ["けんちん汁", "けんちんじる", "筑前煮汤（蔬菜汤）"],
                    ["めっちゃ", "めっちゃ", "非常、超（口语）"],
                    ["小学校", "しょうがっこう", "小学"],
                    ["試合", "しあい", "比赛"],
                    ["思い出", "おもいで", "回忆"]
                ]
            }
        ]
    },
    {
        "slug": "bare-danshi-america-sekihai",
        "title": "バレー男子 決勝ならず…米にフルセット惜敗 スロベニアとの3位決定戦へ",
        "subtitle": "バレーボールネーションズリーグ男子準決勝で日本は米国に2―3で敗れ、決勝進出を逃した。連勝は13でストップ。2日にスロベニアと3位決定戦を戦う。",
        "paras": [
            {
                "ja": "バレーボールネーションズリーグ男子決勝大会の準決勝が8月1日、中国・寧波で行われ、日本は米国に2―3で敗れ、決勝進出を逃しました。1次リーグから13戦全勝だった日本に対し、パリ五輪銅メダルの米国は1次リーグ5位通過。今大会の1次リーグでは、日本がフルセットの末に3―2で逆転勝ちしていました。",
                "en": "The men's semifinal of the Volleyball Nations League Finals was held on August 1 in Ningbo, China, and Japan lost 2-3 to the United States, missing out on a place in the final. Japan had won all 13 matches since the preliminary round, while the United States, bronze medalists at the Paris Olympics, advanced from 5th place in the preliminaries. In this tournament's preliminary round, Japan had come from behind to win 3-2 after five sets.",
                "literal": "排球国家联赛男子决赛阶段的半决赛于8月1日在中国宁波举行，日本以2－3负于美国，错失了晋级决赛的机会。相对于从第一轮开始13战全胜的日本，巴黎奥运会铜牌的美国以第一轮第5名出线。在本届大赛的第一轮中，日本曾在打满五局后以3－2逆转获胜。",
                "grammar": "「〜を逃しました」— 错失…。例：決勝進出を逃しました（错失晋级决赛）。\n「〜に対し」— 相对于…。例：全勝だった日本に対し（相对于全胜的日本）。\n「〜の末に」— 经过…之后。例：フルセットの末に（经过打满五局之后）。",
                "vocab": [
                    ["準決勝", "じゅんけっしょう", "半决赛"],
                    ["決勝進出", "けっしょうしんしゅつ", "晋级决赛"],
                    ["全勝", "ぜんしょう", "全胜"],
                    ["銅メダル", "どうめだる", "铜牌"],
                    ["逆転勝ち", "ぎゃくてんがち", "逆转获胜"],
                    ["フルセット", "ふるせっと", "打满五局"]
                ]
            },
            {
                "ja": "第1セットは中盤から相手の高いブロックに苦戦し、19―25で落としました。第2セットは主将の石川祐希や西田有志が効果的に得点し、25―23で競り勝ちました。第3セットも25―20で取り、セットを連取しましたが、第4セットは19―25で落とし、フルセットにもつれ込みました。",
                "en": "Japan struggled against the opponents' high blocks from the middle of the first set and lost it 19-25. In the second set, captain Yuki Ishikawa and Yuji Nishida scored effectively, and Japan won a close 25-23. They took the third set 25-20 as well, winning two sets in a row, but dropped the fourth 19-25, sending the match to a fifth set.",
                "literal": "第1局从中盘开始苦战于对方的高拦网，以19－25丢掉。第2局主将石川祐希和西田有志有效地得分，以25－23艰难取胜。第3局也以25－20拿下，连续取得两局，但第4局以19－25丢掉，陷入了决胜局。",
                "grammar": "「〜に苦戦し」— 苦战于…。例：高いブロックに苦戦し（苦战于高拦网）。\n「〜で落としました」— 以…丢掉。例：19―25で落としました（以19-25丢掉）。\n「〜にもつれ込みました」— 陷入…。例：フルセットにもつれ込みました（陷入决胜局）。",
                "vocab": [
                    ["中盤", "ちゅうばん", "中盘、中段"],
                    ["ブロック", "ぶろっく", "拦网"],
                    ["主将", "しゅしょう", "主将、队长"],
                    ["得点", "とくてん", "得分"],
                    ["競り勝つ", "せりかつ", "险胜、艰难取胜"],
                    ["連取", "れんしゅ", "连续取得"]
                ]
            },
            {
                "ja": "最終セット、日本は13―15と競り負け、今大会初黒星で連勝は13でストップしました。日本は2日、2大会ぶりのメダルを懸けて、3位決定戦でスロベニアと対戦します。",
                "en": "In the final set, Japan lost a close one 13-15, taking their first loss of the tournament and ending their winning streak at 13. On the 2nd, Japan will face Slovenia in the third-place match, aiming for their first medal in two tournaments.",
                "literal": "最后一局，日本以13－15惜败，本届大赛首次失利，连胜停留在13场。日本将在2日，以时隔两届大赛的奖牌为目标，在季军争夺战中对阵斯洛文尼亚。",
                "grammar": "「〜と競り負け」— 惜败于…。例：13―15と競り負け（以13-15惜败）。\n「〜でストップしました」— 在…停止。例：連勝は13でストップしました（连胜停在13场）。\n「〜を懸けて」— 以…为赌注、为目标。例：メダルを懸けて（以奖牌为目标）。",
                "vocab": [
                    ["最終セット", "さいしゅうせっと", "最后一局"],
                    ["初黒星", "はつくろぼし", "首次失利"],
                    ["連勝", "れんしょう", "连胜"],
                    ["ストップ", "すとっぷ", "停止"],
                    ["3位決定戦", "さんいけっていせん", "季军争夺战"],
                    ["対戦", "たいせん", "对阵、对战"]
                ]
            }
        ]
    },
    {
        "slug": "goto-maki-tif-40sai",
        "title": "後藤真希 TIFで自虐あいさつ「40歳おばさん」 LOVEマシーンなど5曲披露",
        "subtitle": "元モーニング娘。の後藤真希が世界最大のアイドルフェス「TOKYO IDOL FESTIVAL 2026」に出演。「40歳おばさん」と自虐の自己紹介をしながら5曲を披露した。",
        "paras": [
            {
                "ja": "元モーニング娘。で歌手の後藤真希が1日、東京・お台場で開催中の世界最大のアイドルフェス「TOKYO IDOL FESTIVAL 2026」に出演し、モーニング娘。時代の楽曲など計5曲を披露しました。昨年に続き2年連続の出演で、今年はソロでステージに立ちました。",
                "en": "Goto Maki, former Morning Musume. member and singer, appeared on the 1st at \"TOKYO IDOL FESTIVAL 2026,\" the world's largest idol festival currently being held in Odaiba, Tokyo, performing five songs including numbers from her Morning Musume. era. It was her second consecutive appearance following last year, and this year she took the stage solo.",
                "literal": "前早安少女组。成员兼歌手的后藤真希1日出演了在东京·台场举办的全球最大偶像节「TOKYO IDOL FESTIVAL 2026」，表演了早安少女组。时代等共计5首歌曲。继去年之后连续第2年出演，今年以个人身份登上了舞台。",
                "grammar": "「〜で」— 作为…。例：元モーニング娘。で歌手（前早安少女组。成员、歌手）。\n「〜に続き」— 继…之后。例：昨年に続き（继去年之后）。\n「〜連続の」— 连续…的。例：2年連続の出演（连续两年出演）。",
                "vocab": [
                    ["元", "もと", "前、原"],
                    ["歌手", "かしゅ", "歌手"],
                    ["開催中", "かいさいちゅう", "举办中"],
                    ["楽曲", "がっきょく", "歌曲"],
                    ["披露", "ひろう", "表演、展示"],
                    ["ソロ", "そろ", "个人、独唱"]
                ]
            },
            {
                "ja": "アイドルファンの「ごっちん」コールに迎えられると、セクシーな衣装で登場。「40歳おばさん……、違う違う違う、後藤真希です」と自虐的な自己紹介をしつつ、森高千里の『私がおばさんになっても』をカバーしました。",
                "en": "Welcomed by the \"Gocchin\" chants of idol fans, she appeared in a sexy outfit. \"A 40-year-old auntie... no, no, no, I'm Goto Maki,\" she said in a self-deprecating self-introduction, while covering Moritaka Chisato's \"Watashi ga Obasan ni Natte mo\" (Even If I Become an Old Lady).",
                "literal": "被偶像粉丝的「ごっちん」应援声迎接后，她以性感的服装登场。「40岁大妈……不对不对不对，我是后藤真希」，一边做着自嘲的自我介绍，一边翻唱了森高千里的《就算我变成大妈》。",
                "grammar": "「〜に迎えられると」— 一被…迎接就…。例：コールに迎えられると（一被应援声迎接）。\n「〜しつつ」— 一边…一边…。例：自己紹介をしつつ（一边自我介绍）。\n「〜をカバーしました」— 翻唱了…。例：森高千里の曲をカバーしました（翻唱了森高千里的歌）。",
                "vocab": [
                    ["コール", "こーる", "应援声、呼喊"],
                    ["衣装", "いしょう", "服装、戏服"],
                    ["自虐的", "じぎゃくてき", "自嘲的"],
                    ["自己紹介", "じこしょうかい", "自我介绍"],
                    ["カバー", "かばー", "翻唱"],
                    ["登場", "とうじょう", "登场"]
                ]
            },
            {
                "ja": "ラストナンバーの『LOVEマシーン』では会場の盛り上がりが最高潮に。この日一番の大歓声が起こると、後藤は「みんな最高！」と感謝を伝え、「またどこかで会いましょう！」と約束してステージを締めくくりました。",
                "en": "With the final number \"LOVE Machine,\" the venue's excitement reached its peak. As the biggest cheers of the day erupted, Goto expressed her gratitude — \"You're all the best!\" — and closed out the stage with a promise: \"Let's meet again somewhere!\"",
                "literal": "在压轴曲目《LOVE机器》中，会场的热情达到最高潮。当天最大的欢呼声响起后，后藤传达了感谢「大家最棒！」，并约定「让我们在某个地方再会吧！」，为舞台画上了句号。",
                "grammar": "「〜では」— 在…（场面）中。例：ラストナンバーでは（在压轴曲目时）。\n「〜が起こると」— 一发生…就…。例：大歓声が起こると（欢呼声一响起）。\n「〜て締めくくりました」— 以…结束。例：ステージを締めくくりました（为舞台画上句号）。",
                "vocab": [
                    ["ラストナンバー", "らすとなんばー", "压轴曲目"],
                    ["盛り上がり", "もりあがり", "热情高涨"],
                    ["最高潮", "さいこうちょう", "最高潮"],
                    ["大歓声", "だいかんせい", "大声欢呼"],
                    ["感謝", "かんしゃ", "感谢"],
                    ["締めくくる", "しめくくる", "总结、收尾"]
                ]
            }
        ]
    },
    {
        "slug": "roshia-kiu-daikibo-kougeki",
        "title": "ロシアがウクライナ・キーウに大規模攻撃 9人死亡、30人以上けが",
        "subtitle": "ロシア軍がウクライナの首都キーウを夜間に大規模攻撃し、子ども4人を含む30人以上がけが。ゼレンスキー大統領はパトリオットのミサイル供与を改めて求めた。",
        "paras": [
            {
                "ja": "ロシアがウクライナの首都キーウに大規模な攻撃を行い、9人が死亡、30人以上がけがをしました。キーウの市長は1日、夜間にロシア軍の攻撃があり、子ども4人を含む30人以上がけがをしたと明らかにしました。住宅にも被害が出たとしています。",
                "en": "Russia carried out a large-scale attack on Ukraine's capital Kyiv, killing 9 people and injuring more than 30. Kyiv's mayor revealed on the 1st that a nighttime Russian military attack had left more than 30 people injured, including 4 children. He said residential buildings were also damaged.",
                "literal": "俄罗斯对乌克兰首都基辅发动了大规模攻击，造成9人死亡，30人以上受伤。基辅市长1日公布，夜间遭到俄军攻击，包括4名儿童在内的30人以上受伤。据称住宅也受到了损害。",
                "grammar": "「〜を行い」— 进行了…。例：大規模な攻撃を行い（发动大规模攻击）。\n「〜と明らかにしました」— 公布称…。例：けがをしたと明らかにしました（公布称受伤了）。\n「〜としています」— 表示（主张）…。例：被害が出たとしています（表示受到了损害）。",
                "vocab": [
                    ["首都", "しゅと", "首都"],
                    ["大規模", "だいきぼ", "大规模"],
                    ["攻撃", "こうげき", "攻击"],
                    ["市長", "しちょう", "市长"],
                    ["夜間", "やかん", "夜间"],
                    ["被害", "ひがい", "损害、受灾"]
                ]
            },
            {
                "ja": "ゼレンスキー大統領によりますと、ロシア軍は弾道ミサイル27発を含むミサイル35発や、150機以上のドローンを発射し、攻撃はキーウのほか中部ドニプロや北東部ハルキウ州などにも及びました。ゼレンスキー氏は、迎撃ミサイルが不足しているため撃墜できた弾道ミサイルは1発だけだったとし、アメリカ製防空システム「パトリオット」のミサイル供与を改めて求めています。",
                "en": "According to President Zelensky, Russian forces launched 35 missiles including 27 ballistic missiles, and more than 150 drones, with attacks extending beyond Kyiv to central Dnipro, northeastern Kharkiv Oblast and elsewhere. Zelensky said that because interceptor missiles are insufficient, only one ballistic missile could be shot down, and he renewed his request for missile supplies for the American-made air defense system \"Patriot.\"",
                "literal": "据泽连斯基总统称，俄军发射了包括27发弹道导弹在内的35发导弹以及150架以上的无人机，攻击除基辅外还波及中部第聂伯罗和东北部哈尔科夫州等地。泽连斯基表示，由于拦截导弹不足，能够击落的弹道导弹只有1发，并再次要求提供美国制防空系统「爱国者」的导弹。",
                "grammar": "「〜によりますと」— 据…称。例：ゼレンスキー大統領によりますと（据泽连斯基总统称）。\n「〜を含む」— 包含…。例：弾道ミサイル27発を含む（包含27发弹道导弹）。\n「〜とし」— 表示（主张）…。例：1発だけだったとし（表示只有1发）。",
                "vocab": [
                    ["弾道ミサイル", "だんどうみさいる", "弹道导弹"],
                    ["ドローン", "どろーん", "无人机"],
                    ["発射", "はっしゃ", "发射"],
                    ["迎撃", "げいげき", "迎击、拦截"],
                    ["撃墜", "げきつい", "击落"],
                    ["防空システム", "ぼうくうしすてむ", "防空系统"]
                ]
            }
        ]
    },
    {
        "slug": "ishiba-syouhizei-hihan",
        "title": "石破前首相 高市首相の「消費税率1％」方針を批判 「財源示さなければ無責任」",
        "subtitle": "高市首相が2027年4月から2年間、飲食料品の消費税率を1％に引き下げる方針を表明したことを受け、石破前首相が「代わりの財源を示さなければ無責任」と批判した。",
        "paras": [
            {
                "ja": "高市首相が2027年4月から2年間、飲食料品の消費税率を1％に引き下げる方針を正式に表明したことを受け、石破前首相は「財源が示されていない」と批判しました。8月1日、鳥取県倉吉市で開かれた自民党鳥取県連の会合で、「消費税は全額社会保障に充てることになっている。代わりの財源を示さなければこれほど無責任なことはない」と述べました。",
                "en": "In response to Prime Minister Takaichi's formal announcement of a policy to cut the consumption tax rate on food and beverages to 1% for two years from April 2027, former Prime Minister Ishiba criticized that \"no funding source has been shown.\" At a meeting of the LDP Tottori Prefectural Federation held in Kurayoshi City, Tottori Prefecture, on August 1, he stated, \"Consumption tax is supposed to be allocated entirely to social security. There is nothing more irresponsible than not showing an alternative funding source.\"",
                "literal": "针对高市首相正式表明2027年4月起2年间将饮食料品的消费税税率下调至1％的方针，石破前首相批判称「财源未被出示」。8月1日，在鸟取县仓吉市召开的自民党鸟取县联合会议上，他表示「消费税按规定全额用于社会保障。不拿出替代财源的话，没有比这更不负责任的事了」。",
                "grammar": "「〜ことを受け」— 针对…、鉴于…。例：表明したことを受け（针对表明一事）。\n「〜ことになっている」— 按规定…。例：充てることになっています（按规定用于…）。\n「〜なければ〜ない」— 如果不…就不…。例：示さなければ無責任（不拿出就（是）不负责任）。",
                "vocab": [
                    ["消費税", "しょうひぜい", "消费税"],
                    ["引き下げる", "ひきさげる", "下调、降低"],
                    ["正式に", "せいしきに", "正式地"],
                    ["財源", "ざいげん", "财源"],
                    ["社会保障", "しゃかいほしょう", "社会保障"],
                    ["無責任", "むせきにん", "不负责任"]
                ]
            },
            {
                "ja": "さらに石破前首相は「財政が毀損すれば通貨が安くなる。通貨が安くなれば金利が上がる。金利が上がれば物価が上がる。それにより苦しむのは誰だ」と述べ、かねてから訴える給付案は「間違っているとは思わない」と強調しました。一方、消費減税については、政権与党内でも意見が割れています。",
                "en": "Furthermore, Ishiba said, \"If public finances are damaged, the currency weakens. If the currency weakens, interest rates rise. If interest rates rise, prices rise. Who suffers from that?\" and stressed that his long-advocated benefit plan is \"not something I think is wrong.\" Meanwhile, opinions are divided even within the ruling party over the consumption tax cut.",
                "literal": "此外，石破前首相表示「财政一旦受损货币就会贬值。货币一旦贬值利率就会上升。利率一旦上升物价就会上涨。因此受苦的是谁」，并强调自己一直主张的补贴方案「并不认为有错」。另一方面，关于消费减税，即使在执政党内部意见也存在分歧。",
                "grammar": "「〜ば〜」— 如果…就…（条件句）。例：毀損すれば通貨が安くなる（受损就会贬值）。\n「〜かねてから」— 一直、向来。例：かねてから訴える（一直主张的）。\n「〜とは思わない」— 不认为…。例：間違っているとは思わない（不认为有错）。",
                "vocab": [
                    ["財政", "ざいせい", "财政"],
                    ["毀損", "きそん", "损害、损坏"],
                    ["通貨", "つうか", "货币"],
                    ["金利", "きんり", "利率"],
                    ["物価", "ぶっか", "物价"],
                    ["与党", "よとう", "执政党"]
                ]
            },
            {
                "ja": "高市首相は7月30日、全所得階層に負担軽減が及ぶよう、飲食料品の消費税率1％への引き下げを2027年4月から2年間先行させると表明しました。財源については赤字国債に頼らず、税外収入の更なる確保などを行い、2年後に必ず税率8％に戻すと述べています。",
                "en": "On July 30, Prime Minister Takaichi stated that, so that the burden reduction reaches all income brackets, the consumption tax rate on food and beverages would be cut to 1% for two years starting April 2027. Regarding funding, she said they will not rely on deficit bonds, but will secure further non-tax revenue, and will definitely return the rate to 8% after two years.",
                "literal": "高市首相7月30日表明，为了使负担减轻惠及所有收入阶层，将把饮食料品的消费税率下调至1％从2027年4月起先行实施2年。关于财源，她表示不依赖赤字国债，将确保更多的税外收入等，2年后必定恢复到8％的税率。",
                "grammar": "「〜よう」— 为了…。例：負担軽減が及ぶよう（为了减轻负担惠及）。\n「〜と表明しました」— 表明…。例：先行させると表明しました（表明先行实施）。\n「〜に頼らず」— 不依赖…。例：赤字国債に頼らず（不依赖赤字国债）。",
                "vocab": [
                    ["所得階層", "しょとくかいそう", "收入阶层"],
                    ["負担軽減", "ふたんけいげん", "减轻负担"],
                    ["先行", "せんこう", "先行、领先"],
                    ["赤字国債", "あかじこくさい", "赤字国债"],
                    ["税外収入", "ぜいがいしゅうにゅう", "税外收入"],
                    ["戻す", "もどす", "恢复、归还"]
                ]
            }
        ]
    }
]

# ==================================================================
# PROCESSING
# ==================================================================
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
