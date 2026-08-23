#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-24 (Mon) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-24'
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
        "slug": "futatsu-kaikyou-antei",
        "title": "「二つの海峡」安定に注力　日本政府、原油輸送確保狙う　首脳外交求める声",
        "subtitle": "from 時事通信",
        "paras": [
            {
                "ja": "茂木敏充外相は22日、サウジアラビアとオマーンの中東2カ国歴訪を終え、帰国した。6日間の訪問で狙ったのは、原油輸送の要衝、ホルムズ海峡とバベルマンデブ海峡の「自由で安全な航行」の確保だ。米国とイランの戦闘終結に向けた協議の行方が見通せない中、高市早苗首相の対面による首脳外交に期待する声も出ている。",
                "en": "Foreign Minister Toshimitsu Motegi returned home on the 22nd after concluding visits to two Middle Eastern countries, Saudi Arabia and Oman. What he aimed for during the six-day visit was securing \"free and safe navigation\" through the Strait of Hormuz and the Bab el-Mandeb Strait, key points for crude oil transport. With the outcome of talks toward ending the U.S.-Iran conflict uncertain, voices are emerging that expect summit diplomacy through face-to-face meetings by Prime Minister Sanae Takaichi.",
                "literal": "外相茂木敏充22日结束了沙特阿拉伯和阿曼两个中东国家的历访，回国。6天访问所瞄准的，是原油运输要冲霍尔木兹海峡和曼德海峡的「自由且安全的航行」的确保。在美国和伊朗战斗终结的协议走向难以预料的背景下，也出现了期待首相高市早苗通过面对面进行首脑外交的声音。",
                "grammar": "「〜を終え」— 结束…（书面语）。例：歴訪を終え、帰国した（结束历访后回国）。\n「〜に向けた」— 面向…的。例：戦闘終結に向けた協議（面向终结战斗的协议）。\n「〜の行方が見通せない」— …的走向难以预料。例：協議の行方が見通せない中（在协议走向难以预料的情况下）。",
                "vocab": [["外相", "がいしょう", "外长"], ["歴訪", "れきほう", "历访、巡访"], ["要衝", "ようしょう", "要冲"], ["原油", "げんゆ", "原油"], ["航行", "こうこう", "航行"], ["確保", "かくほ", "确保"]]
            },
            {
                "ja": "「オマーンでは海水淡水化事業が進められており、積極的な役割を果たしたい」。茂木氏は20日、同国の首都マスカットでバドル外相と会談し、こう約束した。オマーンはホルムズ海峡の南側の沿岸国だ。イランは協議の中で民間船舶などからの通航料の徴収を主張しているとされるが、日本は国際法違反だとして反対の立場だ。",
                "en": "\"Desalination projects are advancing in Oman, and we want to play an active role,\" Motegi promised on the 20th, meeting with Foreign Minister Badr in Muscat, the country's capital. Oman is a coastal nation on the southern side of the Strait of Hormuz. Iran is said to be asserting the collection of transit fees from civilian vessels and others in the talks, but Japan takes a position of opposition, calling it a violation of international law.",
                "literal": "「阿曼正在进行海水淡化事业，希望发挥积极作用」。茂木氏20日在同国首都马斯喀特与巴德尔外相会谈，如此承诺。阿曼是霍尔木兹海峡南侧的沿岸国。伊朗据称在协议中主张征收民间船舶等的通航费，但日本以违反国际法为由持反对立场。",
                "grammar": "「〜ており」— …着（正式书面语）。例：進められており（正在推进着）。\n「〜とされる」— 据称…。例：主張しているとされる（据称正在主张）。\n「〜として」— 以…为由、作为…。例：国際法違反だとして（以违反国际法为由）。",
                "vocab": [["海水淡水化", "かいすいたんすいか", "海水淡化"], ["首都", "しゅと", "首都"], ["沿岸国", "えんがんこく", "沿岸国"], ["船舶", "せんぱく", "船舶"], ["通航料", "つうこうりょう", "通航费"], ["徴収", "ちょうしゅう", "征收"]]
            },
            {
                "ja": "茂木氏はオマーンに先立ってサウジも訪れた。サウジは「アラブの盟主」とされ、アラブ諸国に影響力を持つ。日本は原油の9割を中東に依存してきた。ホルムズ海峡封鎖を受け、バベルマンデブ海峡の重要性が増しているが、沿岸国のイエメンの親イラン武装組織フーシ派が、同海峡を通航するサウジの船舶を攻撃しており、情勢が不安定化している。",
                "en": "Motegi also visited Saudi Arabia before Oman. Saudi Arabia is regarded as the \"leader of the Arab world\" and holds influence over Arab countries. Japan has depended on the Middle East for 90 percent of its crude oil. With the Strait of Hormuz sealed off, the importance of the Bab el-Mandeb Strait is increasing, but the Iran-backed Houthi armed group in Yemen, a coastal nation, has been attacking Saudi vessels transiting the strait, destabilizing the situation.",
                "literal": "茂木氏在访问阿曼之前也访问了沙特。沙特被视为「阿拉伯盟主」，对阿拉伯各国拥有影响力。日本原油的九成一直依赖中东。受霍尔木兹海峡封锁影响，曼德海峡的重要性在增加，但沿岸国也门的亲伊朗武装组织胡塞派正在攻击通过该海峡的沙特船舶，局势正变得不稳定。",
                "grammar": "「〜に先立って」— 在…之前。例：オマーンに先立って（在访问阿曼之前）。\n「〜とされ」— 被视为…。例：盟主とされ（被视为盟主）。\n「〜ており、」— …着，且…。例：攻撃しており（正在攻击，…）。",
                "vocab": [["盟主", "めいしゅ", "盟主"], ["影響力", "えいきょうりょく", "影响力"], ["依存", "いぞん", "依赖"], ["封鎖", "ふうさ", "封锁"], ["武装組織", "ぶそうそしき", "武装组织"], ["情勢", "じょうせい", "局势"], ["不安定", "ふあんてい", "不稳定"]]
            },
            {
                "ja": "「二つの海峡」の安定に向けて注力するのは外相だけではない。首相は今月に入り、オマーン、イラン、トルコの首脳と電話会談し、協力を求めた。ただ、夏の外国訪問を見送った首相に対しては、政府内から「イラン訪問が実現すれば日本の存在感を示す絶好の機会になる」（関係者）と一段の対応を期待する声も漏れる。",
                "en": "The foreign minister is not the only one focusing on stabilizing the \"two straits.\" This month, the prime minister has held telephone talks with the leaders of Oman, Iran, and Turkey, seeking cooperation. However, regarding the prime minister, who gave up foreign visits this summer, voices within the government are also leaking out that expect further steps, such as \"If a visit to Iran is realized, it would be a perfect opportunity to show Japan's presence\" (a source).",
                "literal": "致力于「两个海峡」稳定的不只是外相。首相进入本月以来，与阿曼、伊朗、土耳其的首脑进行了电话会谈，寻求合作。但是，对于放弃夏季出国访问的首相，政府内部也漏出了期待进一步应对的声音，如「如果实现对伊朗的访问，将成为展示日本存在感的绝好机会」（相关人士）。",
                "grammar": "「〜に向けて」— 面向…。例：安定に向けて（面向稳定）。\n「〜に入り」— 进入…以来。例：今月に入り（进入本月以来）。\n「〜ば…になる」— 如果…就会成为…。例：実現すれば…機会になる（如果实现就会成为机会）。",
                "vocab": [["注力", "ちゅうりょく", "着力、倾注力量"], ["首脳", "しゅのう", "首脑"], ["電話会談", "でんわかいだん", "电话会谈"], ["見送る", "みおくる", "放弃、不实行"], ["存在感", "そんざいかん", "存在感"], ["絶好", "ぜっこう", "绝好"], ["漏れる", "もれる", "泄露、透出"]]
            },
        ]
    },
    {
        "slug": "syouhizei-genzei-sijiritsu",
        "title": "消費減税、71％が財政に不安　内閣支持率は最低更新50％",
        "subtitle": "from 共同通信",
        "paras": [
            {
                "ja": "共同通信社は22、23両日、全国電話世論調査を実施した。政府が決定した消費税減税に関し、財政への不安を「感じる」「ある程度感じる」が計71.7％となった。高市内閣の支持率は50.2％で、前回7月調査から3.5ポイント減少し、発足以来最低を更新した。内閣不支持率は33.9％で、内閣支持率は3月調査から6回連続で下落している。",
                "en": "Kyodo News conducted a nationwide telephone opinion poll on the 22nd and 23rd. Regarding the consumption tax cut decided by the government, those who \"feel\" or \"somewhat feel\" anxiety about public finances totaled 71.7 percent. The approval rating for the Takaichi Cabinet was 50.2 percent, down 3.5 points from the previous July survey, marking the lowest since its inauguration. The disapproval rating was 33.9 percent, and the approval rating has fallen for six consecutive surveys since March.",
                "literal": "共同通讯社22、23两天实施了全国电话舆论调查。关于政府决定的消费税减税，对财政感到不安「有感觉」「有一定感觉」共计71.7%。高市内阁的支持率为50.2%，比上次7月调查减少3.5个百分点，刷新了成立以来的最低纪录。内阁不支持率为33.9%，内阁支持率自3月调查以来连续6次下降。",
                "grammar": "「〜に関し」— 关于…。例：消費税減税に関し（关于消费税减税）。\n「〜となりました」— 达到了…。例：計71.7％となりました（共计达到了71.7%）。\n「〜以来」— 自…以来。例：発足以来最低（成立以来最低）。",
                "vocab": [["世論調査", "よろんちょうさ", "舆论调查"], ["実施", "じっし", "实施"], ["減税", "げんぜい", "减税"], ["財政", "ざいせい", "财政"], ["支持率", "しじりつ", "支持率"], ["発足", "ほっそく", "成立、发起"], ["下落", "げらく", "下降"]]
            },
            {
                "ja": "高市早苗首相が検討する内閣改造・自民党役員人事を巡り、派閥裏金事件で処分を受けた議員を重要ポストに起用することに「反対」が73.8％となった。中道改革連合、立憲民主、公明3党の合流協議を巡り、「合流は全て取りやめ、元の立民、公明に戻すべきだ」が51.0％に上った。",
                "en": "Regarding the cabinet reshuffle and Liberal Democratic Party executive appointments that Prime Minister Sanae Takaichi is considering, 73.8 percent were \"opposed\" to appointing lawmakers disciplined in the faction slush fund scandal to important posts. On questions about the merger talks among the three parties — the Chudo Kaikaku Rengo (centrist reform alliance), the Constitutional Democratic Party, and Komeito — 51.0 percent said \"the merger should be scrapped entirely and we should return to the original CDP and Komeito.\"",
                "literal": "围绕首相高市早苗正在探讨的内阁改造和自民党干部人事，对起用因派系秘密资金事件受处分的议员担任重要职位「反对」达到73.8%。围绕中道改革联合、立宪民主、公明3党的合并协议，回答「合并应全部取消，回到原来的立民、公明」上升到51.0%。",
                "grammar": "「〜を巡り」— 围绕…。例：人事を巡り（围绕人事）。\n「〜に上った」— 达到、上升到…。例：51.0％に上った（上升到51.0%）。\n「〜べきだ」— 应该…。例：戻すべきだ（应该回到）。",
                "vocab": [["検討", "けんとう", "探讨、研究"], ["内閣改造", "ないかくかいぞう", "内阁改组"], ["役員", "やくいん", "干部、高管"], ["派閥", "はばつ", "派系"], ["裏金", "うらがね", "秘密资金"], ["処分", "しょぶん", "处分"], ["起用", "きよう", "起用"]]
            },
            {
                "ja": "飲食料品の消費税率を来年4月から2年間、1％に引き下げる政府方針については「賛成」52.7％、「反対」43.1％となった。回答は固定電話425人、携帯電話627人。",
                "en": "Regarding the government's policy of lowering the consumption tax rate on food and beverages to 1 percent for two years from next April, 52.7 percent were \"in favor\" and 43.1 percent \"opposed.\" Respondents were 425 landline phone users and 627 mobile phone users.",
                "literal": "关于从明年4月起两年内将食品饮料消费税率下调至1%的政府方针，「赞成」为52.7%、「反对」为43.1%。回答者为固定电话425人、手机627人。",
                "grammar": "「〜については」— 关于…。例：政府方針については（关于政府方针）。\n「〜に引き下げる」— 下调到…。例：1％に引き下げる（下调到1%）。\n「〜となりました」— 成为了…。例：「反対」43.1％となりました（「反对」为43.1%）。",
                "vocab": [["飲食料品", "いんしょくりょうひん", "食品饮料"], ["税率", "ぜいりつ", "税率"], ["引き下げる", "ひきさげる", "下调"], ["方針", "ほうしん", "方针"], ["賛成", "さんせい", "赞成"], ["固定電話", "こていでんわ", "固定电话"]]
            },
        ]
    },
    {
        "slug": "chiba-gouu-suiryou-syaryou",
        "title": "千葉豪雨、水没車両は1万台規模か　一変した日常「まだ10年乗りたかった」愛車との別れに悲痛な声",
        "subtitle": "from 日テレNEWS NNN",
        "paras": [
            {
                "ja": "先週、記録的な豪雨に見舞われた千葉県内では多くの車が水没し、熊谷知事は被災車両が1万台に及ぶ可能性があるとの見方を示しています。22日、千葉市の住宅街には、全国から集められたJAFの特別支援隊の姿がありました。",
                "en": "In Chiba Prefecture, hit by record heavy rain last week, many cars were submerged, and Governor Kumagai has expressed the view that affected vehicles may reach 10,000. On the 22nd, in a residential area of Chiba City, special support teams from JAF assembled from across the country were on the scene.",
                "literal": "上周遭受创纪录暴雨的千叶县内许多车辆被水淹没，熊谷知事表示看法认为受灾车辆可能达到1万辆。22日，在千叶市的住宅区，有从全国各地汇集来的JAF特别支援队的身影。",
                "grammar": "「〜に見舞われた」— 遭受了…。例：豪雨に見舞われた（遭受了暴雨）。\n「〜に及ぶ」— 达到…。例：1万台に及ぶ（达到1万辆）。\n「〜との見方を示しています」— 表示…的看法。例：可能性があるとの見方を示しています（表示有可能的看法）。",
                "vocab": [["記録的", "きろくてき", "创纪录的"], ["豪雨", "ごうう", "暴雨"], ["水没", "すいぼつ", "水淹、淹没"], ["被災", "ひさい", "受灾"], ["知事", "ちじ", "知事（县最高行政长官）"], ["支援隊", "しえんたい", "支援队"]]
            },
            {
                "ja": "取材したのは、レッカーを依頼していた中村さんです。中村さんは、自宅前にとめていた3台が水につかってしまったといいます。中でも、特にお気に入りだという黒い車がありました。「本当にすごい気に入っていた車なので、ダメになっちゃったらショックは大きいんですけど」と話します。思い入れがあるのには理由がありました。「母を連れて旅行に行きたいってことで、大きめな車を買っていたので。主人と、もうこの車は乗り潰すつもりで乗ろうねって言っていて、そういう矢先だったので、手放すのはつらい部分があるんですけど」",
                "en": "The person we interviewed was Mr. Nakamura, who had requested a tow truck. He said that three cars parked in front of his home had been flooded. Among them was a black car he was especially fond of. \"I really loved this car, so if it's ruined, the shock will be great,\" he said. There was a reason for his attachment. \"I bought a larger car because I wanted to take my mother on trips. My husband and I had said we'd drive this one until it died, and it was right at that point, so letting it go is painful.\"",
                "literal": "接受采访的是委托了拖车的中村先生。中村先生说，停在自家门前的3辆车被水淹了。其中有一辆特别中意的黑色车。「因为是非常喜欢的车，如果报废了打击会很大」。对它有感情是有理由的。「因为想带母亲去旅行，所以买了大一点的车。和丈夫说过这辆车要一直开到报废，正说到这个节骨眼上，所以放手有难过的地方」。",
                "grammar": "「〜てしまった」— …了（表示遗憾）。例：水につかってしまった（被水淹了）。\n「〜といいます」— 据说/他说…。例：3台が水につかったといいます（他说3辆被水淹了）。\n「〜矢先だった」— 正是…的节骨眼上。例：そういう矢先だった（正是在那个时候）。",
                "vocab": [["取材", "しゅざい", "采访"], ["レッカー", "れっかー", "拖车"], ["依頼", "いらい", "委托"], ["お気に入り", "おきにいり", "中意、心爱"], ["思い入れ", "おもいいれ", "感情投入、眷恋"], ["乗り潰す", "のりつぶす", "开到报废"], ["手放す", "てばなす", "放手、舍弃"]]
            },
            {
                "ja": "もう一度乗る望みを残していましたが、レッカーで移動される車からは水が流れ出てきました。そして、被災した車との別れの時が訪れました。「やっぱり、ああやって行っちゃうと寂しいものが…」と中村さんは話しました。",
                "en": "He had kept hope of driving it once more, but water flowed out of the car as it was moved by the tow truck. Then the time came to say goodbye to the damaged car. \"After all, when it goes off like that, there's something lonely about it...\" Mr. Nakamura said.",
                "literal": "虽然还留有再开一次的希望，但从被拖车移动的车里流出了水。然后，与被灾车辆告别的时刻到来了。「果然，那样离去的话，有寂寞的感觉…」中村先生这样说道。",
                "grammar": "「〜ましたが、」— 虽然…但是…。例：望みを残していましたが（虽然留有希望）。\n「〜てきました」— …出来了。例：流れ出てきました（流了出来）。\n「〜と…は話しました」— …说（引用）。例：寂しいものが…と話しました（说感到寂寞）。",
                "vocab": [["望み", "のぞみ", "希望"], ["別れ", "わかれ", "离别"], ["訪れる", "おとずれる", "来临、到访"], ["寂しい", "さびしい", "寂寞的"], ["やっぱり", "やっぱり", "果然"], ["流れ出る", "ながれでる", "流出"]]
            },
            {
                "ja": "22日、取材班が向かった千葉市役所の駐車場には、端から端までずらっと車が並んでいました。豪雨の影響で市内の道路などに放置されていた車両が集められていました。持ち主への引き渡しを早く進めるため、土日も対応していました。取材で出会ったのは、神奈川県から2時間半かけて来たという40代の女性です。水没した場所には車が見当たらず、市役所などに連絡して、ようやくこの場所にあることが分かったといいます。1週間ぶりの再会を果たしましたが、車は“廃車”になってしまうことになりました。",
                "en": "On the 22nd, at the Chiba City Hall parking lot the reporting team visited, cars were lined up from end to end. Vehicles that had been left on city roads and elsewhere due to the heavy rain had been gathered there. Staff were working even on weekends to speed up returning them to their owners. The person the team met was a woman in her 40s who had come from Kanagawa Prefecture, a two-and-a-half-hour drive away. She said she couldn't find her car where it had been submerged, and after contacting the city hall and others, she finally learned it was at this location. She was reunited with it for the first time in a week, but the car ended up being written off as \"scrapped.\"",
                "literal": "22日，采访组前往的千叶市政府停车场里，从这头到那头整齐排满了车。因暴雨影响而被遗弃在市区道路等的车辆被集中到这里。为了尽快推进向车主的移交，周末也在对应。采访中遇到的是一位从神奈川县花了2个半小时赶来的40多岁女性。被淹没的地点没有找到车，联系市政府等处后，终于得知车在这个地方。虽然时隔一周重逢了，但车最终变成了「报废」。",
                "grammar": "「〜に向かった」— 前往了…。例：市役所の駐車場に向かった（前往了市政府停车场）。\n「〜ため、」— 为了…/因为…。例：進めるため（为了推进）。\n「〜ぶりの再会」— 时隔…的重逢。例：1週間ぶりの再会（时隔一周的重逢）。",
                "vocab": [["取材班", "しゅざいばん", "采访组"], ["駐車場", "ちゅうしゃじょう", "停车场"], ["放置", "ほうち", "放置、遗弃"], ["引き渡し", "ひきわたし", "移交、交付"], ["見当たらない", "みあたらない", "找不到"], ["ようやく", "ようやく", "终于"], ["廃車", "はいしゃ", "报废车"]]
            },
        ]
    },
    {
        "slug": "danchi-kurashi-nikoichi",
        "title": "戸建てを売って家族5人で越してきた人も　入居率V字回復「団地」の魅力　令和の「団地暮らし」",
        "subtitle": "from 関西テレビ",
        "paras": [
            {
                "ja": "近年、都心部の賃貸マンションの家賃が上がり続けています。大阪市内の物件も大幅に上昇し、特にファミリー向けマンションでは平均家賃がおよそ17万円と、関西で最も高い水準に達しています。そんな中、見直されているのが、かつて時代遅れのイメージを持たれていた団地です。入居率がV字回復した団地を取材し、手頃な家賃だけではない、令和の団地暮らしの実態に迫りました。",
                "en": "In recent years, rents for condominium apartments in central urban areas have continued to rise. Properties in Osaka City have also risen sharply, and for family-oriented apartments in particular, the average rent has reached about 170,000 yen, the highest level in Kansai. Amid this, attention is turning again to public housing complexes (danchi), which once had an outdated image. We visited a danchi whose occupancy rate has recovered in a V-shape and got close to the reality of Reiwa-era danchi living, which is about more than just affordable rent.",
                "literal": "近年来，市中心区域的租赁公寓房租持续上涨。大阪市内的房源也大幅上涨，尤其是面向家庭的公寓平均房租约17万日元，达到了关西最高水平。在这样的情况下，被重新审视的，是曾经被认为过时印象的团地（公营住宅区）。我们采访了入住率呈V字恢复的团地，逼近了不只是房租实惠的令和团地生活的实态。",
                "grammar": "「〜続けています」— 持续…。例：上がり続けています（持续上涨）。\n「〜と」— 达到…（表示数量）。例：17万円と（达到17万日元）。\n「〜だけではない」— 不只是…。例：手頃な家賃だけではない（不只是实惠的房租）。",
                "vocab": [["都心部", "としんぶ", "市中心区域"], ["賃貸", "ちんたい", "租赁"], ["家賃", "やちん", "房租"], ["上昇", "じょうしょう", "上涨"], ["水準", "すいじゅん", "水平"], ["団地", "だんち", "团地（公营住宅区）"], ["入居率", "にゅうきょりつ", "入住率"]]
            },
            {
                "ja": "大阪府堺市の南部、泉北ニュータウンの一角にある茶山台団地は1971年に誕生した大規模賃貸団地です。高度経済成長期には、当たり前のお風呂や水洗トイレなどの最新設備が整い、入居倍率が50倍を超える“夢の住まい”でした。しかし2000年代以降は高齢化などにより入居率が低下し、2016年にはおよそ20%が空室という状況に追い込まれました。住民と行政が一体となった取り組みが始まり、2021年以降は入居率が9割以上にまで回復しています。",
                "en": "Chayamadai Danchi, located in a corner of Senboku New Town in the southern part of Sakai City, Osaka Prefecture, is a large-scale rental housing complex born in 1971. During the high economic growth period, it was a \"dream home\" equipped with the latest facilities such as what are now ordinary baths and flush toilets, with an application ratio exceeding 50 times. However, from the 2000s onward, occupancy fell due to aging and other factors, and by 2016 about 20 percent of units had been driven into vacancy. With efforts in which residents and the local government worked as one, occupancy has recovered to over 90 percent since 2021.",
                "literal": "位于大阪府堺市南部、泉北新城一角的茶山台团地是1971年诞生的大规模租赁团地。在经济高速增长期，配备了如今理所当然的浴室和抽水马桶等最新设备，是申请倍率超过50倍的「梦想住宅」。但是2000年代以后，由于老龄化等原因入住率下降，2016年约20%被逼入空置的状况。居民与行政一体的举措开始后，2021年以后入住率恢复到了9成以上。",
                "grammar": "「〜に整い」— 配备齐全。例：最新設備が整い（最新设备齐全）。\n「〜を超える」— 超过…。例：50倍を超える（超过50倍）。\n「〜に追い込まれました」— 被逼到…。例：状況に追い込まれました（被逼到…状况）。",
                "vocab": [["一角", "いっかく", "一角"], ["誕生", "たんじょう", "诞生"], ["高度経済成長期", "こうどけいざいせいちょうき", "经济高速增长期"], ["水洗トイレ", "すいせいといれ", "抽水马桶"], ["空室", "くうしつ", "空房"], ["行政", "ぎょうせい", "行政"], ["回復", "かいふく", "恢复"]]
            },
            {
                "ja": "茶山台団地で注目を集めているのが「ニコイチ」と呼ばれる物件です。2つの部屋をセットで貸し出し、玄関やベランダを通じて行き来できる間取りになっています。2部屋でおよそ90平方メートルで家賃は月8万7000円。大阪市内中心部で同サイズのマンションを借りれば平均20万円以上かかるため、10万円以上の差が生まれる計算です。",
                "en": "What is drawing attention at Chayamadai Danchi is a housing type called \"nikoichi\" (two-in-one). Two units are rented out as a set, laid out so residents can move between them through the entrance or balcony. The two units total about 90 square meters, with rent of 87,000 yen per month. Since renting a same-size apartment in central Osaka would cost an average of over 200,000 yen, it works out to a difference of more than 100,000 yen.",
                "literal": "在茶山台团地备受瞩目的是被称为「ニコイチ」（两间合一）的房源。两间屋子成套出租，是可以通过玄关和阳台来往的户型。两间约90平方米，房租每月8万7000日元。如果在大阪市中心区域租同尺寸的公寓平均要花20万日元以上，因此算下来会产生10万日元以上的差距。",
                "grammar": "「〜と呼ばれる」— 被称为…。例：ニコイチと呼ばれる（被称为ニコイチ）。\n「〜を通じて」— 通过…。例：ベランダを通じて（通过阳台）。\n「〜ため、」— 因为…。例：20万円以上かかるため（因为要花20万日元以上）。",
                "vocab": [["注目", "ちゅうもく", "瞩目"], ["物件", "ぶっけん", "房源、物业"], ["間取り", "まどり", "户型、格局"], ["玄関", "げんかん", "玄关、大门"], ["ベランダ", "べらんだ", "阳台"], ["平方メートル", "へいほうめーとる", "平方米"], ["差", "さ", "差距"]]
            },
            {
                "ja": "男の子3人を育てる前野さんも、「ニコイチ」の物件を借りています。前野さんは戸建てを売って家族5人で茶山台に越してきたといいます。「茶山台にほれ込んでしまって。どうしても茶山台に来たくて」と話します。地域の小学校の評判に加え、「年齢を超えたつながりも、新興住宅ではなかなか味わえない」というご近所付き合いの温かさも、移住の決め手だったといいます。",
                "en": "Mr. Maeno, who is raising three boys, also rents a \"nikoichi\" unit. He says he sold his detached house and moved to Chayamadai with his family of five. \"I fell in love with Chayamadai. I really wanted to come to Chayamadai,\" he says. Along with the reputation of the local elementary school, the warmth of neighborly relations — \"connections across generations are hard to experience in a new residential development\" — was reportedly the deciding factor in the move.",
                "literal": "养育3个男孩的前野先生也租了「ニコイチ」的房源。据说前野先生卖掉独栋住宅，一家5口搬到了茶山台。「对茶山台着了迷。无论如何都想来茶山台」。除了地区小学的声誉之外，「超越年龄的交往，在新兴住宅区很难体会到」的这种近邻交往的温暖，据说也是移居的决定性因素。",
                "grammar": "「〜てしまって」— …了（表程度深）。例：ほれ込んでしまって（着了迷）。\n「〜に加え」— 除…之外还…。例：評判に加え（除了声誉之外）。\n「〜という」— 这种…的。例：味わえないという…温かさ（难以体会…的这种温暖）。",
                "vocab": [["育てる", "そだてる", "养育"], ["戸建て", "こだて", "独栋住宅"], ["ほれ込む", "ほれこむ", "着迷、倾心"], ["評判", "ひょうばん", "声誉、评价"], ["新興住宅", "しんこうじゅうたく", "新兴住宅区"], ["味わう", "あじわう", "体会、品味"], ["移住", "いじゅう", "移居"], ["決め手", "きめて", "决定性因素"]]
            },
        ]
    },
    {
        "slug": "ohtani-tousyu-fukki",
        "title": "大谷翔平、最短で来週にも投手復帰　監督説明「タイミング合えば」…次回ブルペン後に状態判断",
        "subtitle": "from Full-Count",
        "paras": [
            {
                "ja": "ドジャース・大谷翔平投手が最短で来週（日本時間9月1日～7日）にも投手復帰する可能性があると、23日（同24日）の試合前にデーブ・ロバーツ監督が説明した。大谷は22日（同23日）の試合前にライブBPに登板した。ロバーツ監督によると、25日（同26日）からアトランタで行われる3連戦中にブルペン投球を行い、その次の投球は状態次第では試合になる可能性があるという。",
                "en": "Dodgers pitcher Shohei Ohtani could return to the mound as early as next week (September 1–7, Japan time), manager Dave Roberts explained before the game on the 23rd (the 24th, Japan time). Ohtani pitched in a live batting practice session before the game on the 22nd (the 23rd, Japan time). According to Roberts, he will throw a bullpen session during the three-game series in Atlanta starting on the 25th (the 26th, Japan time), and depending on his condition, his next throwing session could be in a game.",
                "literal": "道奇队的大谷翔平投手最快下周（日本时间9月1日～7日）也有可能重返投手位置，23日（同24日）赛前主教练戴夫·罗伯茨作了说明。大谷22日（同23日）赛前站上了Live BP（实战击球练习）的投手丘。据罗伯茨教练称，25日（同26日）起在亚特兰大举行的3连战期间将进行牛棚投球，下一次投球根据状态有可能就是比赛。",
                "grammar": "「〜によると」— 根据…。例：ロバーツ監督によると（据罗伯茨教练称）。\n「〜次第では」— 根据…情况、视…而定。例：状態次第では（视状态而定）。\n「〜可能性がある」— 有…的可能性。例：試合になる可能性がある（有成为比赛的可能性）。",
                "vocab": [["投手", "とうしゅ", "投手"], ["復帰", "ふっき", "复出、回归"], ["登板", "とうばん", "登板（投手上场比赛）"], ["ブルペン", "ぶるぺん", "牛棚（投手练习区）"], ["投球", "とうきゅう", "投球"], ["状態", "じょうたい", "状态"], ["監督", "かんとく", "主教练"]]
            },
            {
                "ja": "監督は試合復帰について、「次回のブルペンでの投球内容次第」だとし、「ショウヘイ自身の感覚が大事だ。タイミングが合えば素晴らしいことだし、逆に『もう少し打者と対戦する必要がある』と感じるかもしれない」と話した。早ければ来週にも試合で登板するのかと問われた監督は、「おそらく来週になるだろう」と話した。ドジャースは9月1日（同2日）から本拠地で9連戦が行われる日程となっている。試合に登板すれば7月3日（同4日）のパドレス戦以来となる。昨年投手復帰を果たした際と同じく、ショートイニングからになる見込みだ。",
                "en": "On his return to games, the manager said it \"depends on the contents of his next bullpen session,\" adding, \"Shohei's own feeling is what matters. If the timing is right, that would be great, and conversely, he might feel he 'needs to face a few more batters.'\" Asked whether he could pitch in a game as early as next week, the manager said, \"Probably it will be next week.\" The Dodgers' schedule has a nine-game home stand starting September 1 (the 2nd, Japan time). If he pitches in a game, it will be his first since the Padres game on July 3 (the 4th, Japan time). As with last year when he returned to pitching, he is expected to start with short innings.",
                "literal": "教练关于回归比赛表示「取决于下次牛棚的投球内容」，「翔平自身的感受很重要。时机合适的话是很好的事，反过来也可能觉得『还需要再和打者交手一些』」。被问到最快下周是否也会在比赛中登板，教练说「大概会是下周吧」。道奇队从9月1日（同2日）起将在主场进行9连战的日程。如果比赛中登板，将是7月3日（同4日）对教士队比赛以来的首次。与去年实现投手复出时一样，预计将从短局数开始。",
                "grammar": "「〜次第」— 取决于…。例：投球内容次第（取决于投球内容）。\n「〜ば…し、」— 如果…就…，又…。例：合えば素晴らしいことだし（如果合适就很好）。\n「〜以来となる」— 成为…以来的首次。例：パドレス戦以来となる（成为对教士战以来的首次）。",
                "vocab": [["感覚", "かんかく", "感觉、感受"], ["タイミング", "たいみんぐ", "时机"], ["対戦", "たいせん", "对阵、交手"], ["本拠地", "ほんきょち", "主场、根据地"], ["連戦", "れんせん", "连续比赛"], ["見込み", "みこみ", "预计"], ["イニング", "いにんぐ", "局（棒球用语）"]]
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