#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-07-31 (Fri) Edition"""
import json, os, subprocess, re, time
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-07-31'
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
# TODAY'S ARTICLES — 2026-07-31
# ==================================================================
articles = [
    {
        "slug": "syouhizei-1p-hyoumei",
        "title": "高市首相 食料品の消費税率「1％」を正式表明 実質ゼロへ",
        "subtitle": "高市首相が2027年4月から2年間、食料品の消費税率を8％から1％に引き下げる方針を正式表明。「実質ゼロ」を目指す。",
        "paras": [
            {
                "ja": "高市早苗首相は30日、食料品の消費税率を2027年4月から2年間、8%から1%に引き下げる方針を正式に表明した。さらに1%分を所得に連動して給付することで「実質ゼロ」とする。政府は来週にも消費減税の方針を閣議決定し、今秋の臨時国会に関連法案を提出する意向だ。",
                "en": "Prime Minister Takaichi formally announced a policy on the 30th to reduce the consumption tax rate on food items from 8% to 1% for two years starting April 2027. Furthermore, by providing benefits linked to income equivalent to 1%, the effective rate would become 'practically zero.' The government intends to make a cabinet decision on the consumption tax cut as early as next week and submit relevant bills to the extraordinary Diet session this autumn.",
                "literal": "高市早苗首相30日，正式表明了将食品消费税从2027年4月起两年内从8%降至1%的方针。更通过联动所得给付1%部分实现「实质零」。政府预计下周将消费减税方针进行阁议决定，今秋向临时国会提交相关法案。",
                "grammar": "「〜方針を正式に表明した」— 正式表明了…的方针。例：引き下げる方針を表明した（表明了降低的方针）。\n「〜ことで」— 通过…的方式。例：給付することで（通过给付的方式）。\n「〜意向だ」— 有意…、打算…。例：提出する意向だ（打算提交）。",
                "vocab": [["消費税", "しょうひぜい", "消费税"], ["食料品", "しょくりょうひん", "食品"], ["引き下げる", "ひきさげる", "降低、下调"], ["表明する", "ひょうめいする", "表明"], ["給付", "きゅうふ", "给付、补贴"], ["臨時国会", "りんじこっかい", "临时国会"]]
            },
            {
                "ja": "首相は「物価高や税、社会保険料の負担に苦しんできた中所得・低所得の方の負担軽減が最重要課題」と述べた。2年後に税率を戻すことについて「私が責任を持ち、確実に税率を戻す」と明言した。1989年の消費税導入後、初めての税率引き下げとなる見通しだ。",
                "en": "The Prime Minister stated that 'reducing the burden on middle- and low-income people who have been suffering from high prices, taxes, and social insurance premiums is the most important issue.' Regarding returning the tax rate after two years, she clearly stated, 'I will take responsibility and ensure the rate is restored.' This would be the first tax rate reduction since the introduction of the consumption tax in 1989.",
                "literal": "首相表示「减轻苦于物价高涨、税和社会保险费负担的中低收入者的负担是最重要课题」。关于2年后恢复税率，明确表示「我负有责任，确实恢复税率」。这将是1989年消费税导入以来首次降低税率。",
                "grammar": "「〜に苦しんできた」— 一直苦于…。例：負担に苦しんできた（一直苦于负担）。\n「〜について」— 关于…。例：税率を戻すことについて（关于恢复税率）。\n「〜見通しだ」— 预计是…。例：引き下げとなる見通しだ（预计为降低）。",
                "vocab": [["物価高", "ぶっかだか", "物价高涨"], ["社会保険料", "しゃかいほけんりょう", "社会保险费"], ["負担軽減", "ふたんけいげん", "减轻负担"], ["最重要課題", "さいじゅうようかだい", "最重要课题"], ["責任", "せきにん", "责任"], ["導入", "どうにゅう", "导入、引入"]]
            }
        ]
    },
    {
        "slug": "taifuu13-dolphin-mouretsu",
        "title": "台風13号「ドルフィン」猛烈な勢力で北上 九州・沖縄に接近か",
        "subtitle": "猛烈な台風13号（ドルフィン）が中心気圧910hPa、最大瞬間風速80mで発達。来週後半に九州・沖縄に接近の可能性。",
        "paras": [
            {
                "ja": "気象庁によると、猛烈な勢力の台風13号（ドルフィン）は31日6時時点で、1時間におよそ20キロの速さで西北西へ進んでいる。中心の気圧は910ヘクトパスカル、中心付近の最大風速は55メートル、最大瞬間風速は80メートルとなっている。台風13号は今後西寄りに進み、来月2日ごろにかけて猛烈な勢力を維持する見込みだ。",
                "en": "According to the Japan Meteorological Agency, the violent typhoon No. 13 (Dolphin) was moving northwestward at about 20 km/h as of 6:00 AM on the 31st. Its central pressure is 910 hPa, with maximum sustained winds of 55 m/s near the center and maximum instantaneous wind speeds of 80 m/s. Typhoon No. 13 is expected to continue moving westward and maintain its violent intensity until around the 2nd of next month.",
                "literal": "据气象厅称，猛烈的台风13号（多尔芬）31日6点时以每小时约20公里的速度向西北西前进。中心气压910百帕，中心附近最大风速55米/秒，最大瞬间风速80米/秒。台风13号今后向西前进，预计到8月2日左右维持猛烈势力。",
                "grammar": "「〜によると」— 据…所述。例：気象庁によると（据气象厅称）。\n「〜見込みだ」— 预计…。例：維持する見込みだ（预计维持）。\n「〜にかけて」— 到…为止。例：2日ごろにかけて（到2号左右为止）。",
                "vocab": [["台風", "たいふう", "台风"], ["猛烈", "もうれつ", "猛烈"], ["中心気圧", "ちゅうしんきあつ", "中心气压"], ["最大瞬間風速", "さいだいしゅんかんふうそく", "最大瞬间风速"], ["勢力", "せいりょく", "势力、强度"], ["維持する", "いじする", "维持"]]
            },
            {
                "ja": "その後、台風は進路を北西方向に変えて、来週末には九州の西を北上する予想となっている。小笠原諸島では台風の影響で大しけとなり、伊豆諸島でも波が高くなる見通しだ。今後の太平洋高気圧の位置や勢力によっては、西日本に接近する予測も出ており、来月6日ごろから九州や沖縄に影響を及ぼす可能性がある。",
                "en": "Afterward, the typhoon is forecast to change course to the northwest and move northward past western Kyushu around the weekend of next week. The Ogasawara Islands are expected to experience rough seas due to the typhoon, and waves are also forecast to build in the Izu Islands. Depending on the position and strength of the Pacific high-pressure system, there are predictions of the typhoon approaching western Japan, with possible impacts on Kyushu and Okinawa from around the 6th of next month.",
                "literal": "之后，台风预计将路径转向西北方向，下周末前后沿九州西侧北上。小笠原诸岛将受台风影响出现大浪，伊豆诸岛也预计浪高。根据今后太平洋高气压的位置和势力，也出现接近西日本的预测，从下月6日左右起可能对九州和冲绳产生影响。",
                "grammar": "「〜予想となっている」— 预计为…。例：北上する予想となっている（预计北上）。\n「〜見通しだ」— 预计是…。例：波が高くなる見通しだ（预计浪高）。\n「〜可能性がある」— 有可能…。例：影響を及ぼす可能性がある（有可能造成影响）。",
                "vocab": [["進路", "しんろ", "路径"], ["北上する", "ほくじょうする", "北上"], ["太平洋高気圧", "たいへいようこうきあつ", "太平洋高气压"], ["接近する", "せっきんする", "接近"], ["影響を及ぼす", "えいきょうをおよぼす", "造成影响"], ["大しけ", "おおしけ", "大浪"]]
            }
        ]
    },
    {
        "slug": "saichou-katsudansou-m8",
        "title": "「南海トラフだけではない」1000年以上沈黙する日本最長の活断層",
        "subtitle": "熊本地震を受け、四国を横断する日本最長の活断層「中央構造線断層帯」に注目。M8クラスの地震の恐れも。",
        "paras": [
            {
                "ja": "2026年7月28日に熊本地震を引き起こした活断層と、四国の活断層の関係について検証が進んでいる。四国には日本最長の活断層である「中央構造線断層帯」が走っており、和歌山から徳島・愛媛を横断し、海を渡って大分までつながっている。今回の熊本地震の原因とみられる「日奈久断層帯」は中央構造線の延長線上にあり、両者がつながっていると考える学者もいる。",
                "en": "Investigations are underway into the relationship between the active fault that caused the Kumamoto earthquake on July 28, 2026, and active faults in Shikoku. Shikoku has Japan's longest active fault — the 'Median Tectonic Line Fault Zone' — which runs from Wakayama across Tokushima and Ehime, crossing the sea to reach Oita. The 'Hinagu Fault Zone,' believed to have caused the Kumamoto earthquake, lies on the extension of the Median Tectonic Line, and some scholars believe the two are connected.",
                "literal": "关于2026年7月28日引发熊本地震的活断层与四国活断层的关系的验证正在进行中。四国分布着日本最长的活断层「中央构造线断层带」，从和歌山横断德岛、爱媛，跨海连接到大分。被认为是今回熊本地震原因的「日奈久断层带」位于中央构造线的延长线上，也有学者认为两者相连。",
                "grammar": "「〜を引き起こした」— 引发了…。例：地震を引き起こした（引发了地震）。\n「〜とみられる」— 被认为是…。例：原因とみられる（被认为是原因）。\n「〜ており」— 正在…（连接形式）。例：走っており（分布着）。",
                "vocab": [["活断層", "かつだんそう", "活断层"], ["中央構造線", "ちゅうおうこうぞうせん", "中央构造线"], ["断層帯", "だんそうたい", "断层带"], ["熊本地震", "くまもとじしん", "熊本地震"], ["延長線", "えんちょうせん", "延长线"], ["学者", "がくしゃ", "学者"]]
            },
            {
                "ja": "専門家は「中央構造線断層帯」について、1000年以上大きな地震を起こしていないと指摘する。中央構造線が動けばM8クラスの地震となる可能性があり、四国や近畿、中部地方にまで大きな被害が及ぶ恐れがある。熊本地震がこの断層帯にどのような影響を与えるか、引き続き監視が必要だとされている。",
                "en": "Experts point out that the Median Tectonic Line Fault Zone has not produced a major earthquake in over 1,000 years. If the Median Tectonic Line moves, it could generate a magnitude 8-class earthquake, which could cause extensive damage across Shikoku, the Kinki region, and even the Chubu region. Continued monitoring is said to be necessary to determine what kind of impact the Kumamoto earthquake may have on this fault zone.",
                "literal": "专家指出「中央构造线断层带」已1000年以上没有发生大地震。中央构造线一旦活动，有可能发生M8级地震，四国、近畿乃至中部地区都可能遭受巨大损害。熊本地震对该断层带带来何种影响，需要持续监控。",
                "grammar": "「〜と指摘する」— 指出…。例：指摘する（指出）。\n「〜可能性があり」— 有…的可能性。例：M8クラスとなる可能性があり（有成为M8级的可能性）。\n「〜恐れがある」— 有…的危险。例：被害が及ぶ恐れがある（有波及损害的危险）。",
                "vocab": [["専門家", "せんもんか", "专家"], ["指摘する", "してきする", "指出"], ["M8クラス", "えむはちくらす", "M8级"], ["近畿", "きんき", "近畿地区"], ["監視", "かんし", "监控"], ["被害が及ぶ", "ひがいがおよぶ", "波及损害"]]
            }
        ]
    },
    {
        "slug": "kumamoto-jishin-hisaisha-koe",
        "title": "「シャワーが泥水」熊本地震 被災者の生の声と求める支援",
        "subtitle": "熊本地震発生から2日。イオンモール熊本の爆発や停電・断水の中、被災者が直面する厳しい現実。",
        "paras": [
            {
                "ja": "子どもたちが夏休みに入り、家族で買い物に出かけていた人も多かったであろう7月28日16時過ぎ、突如として熊本県を襲った大地震。30日昼過ぎの時点では34人の死亡が確認されており、人的被害は120人に上っている。熊本県嘉島町に位置するイオンモール熊本では地震発生から約1時間後に爆発が発生。2階部分は崩落し、屋根が吹き飛ぶなど大きな被害が出た。",
                "en": "Just after 4 PM on July 28th, when many families with children on summer vacation were out shopping, a major earthquake suddenly struck Kumamoto Prefecture. As of the afternoon of the 30th, 34 deaths had been confirmed, with human casualties reaching 120. At Aeon Mall Kumamoto in Kashima Town, Kumamoto Prefecture, an explosion occurred about an hour after the earthquake. The second floor collapsed and the roof was blown off, causing extensive damage.",
                "literal": "孩子们进入暑假、许多家庭外出购物的7月28日下午4点过后，熊本县突然遭受大地震袭击。30日中午时分已确认34人死亡，人员伤亡达120人。位于熊本县嘉岛町的AEON MALL熊本在地震发生后约1小时发生爆炸。2楼部分崩塌，屋顶被吹飞等出现巨大损害。",
                "grammar": "「〜であろう」— 大概是…吧。例：多かったであろう（大概很多吧）。\n「〜として」— 突然…。例：突如として（突然）。\n「〜に上っている」— 达到…。例：120人に上っている（达到120人）。",
                "vocab": [["襲う", "おそう", "袭击"], ["死亡", "しぼう", "死亡"], ["確認", "かくにん", "确认"], ["人的被害", "じんてきひがい", "人员伤亡"], ["崩落", "ほうらく", "崩塌、垮塌"], ["吹き飛ぶ", "ふきとぶ", "被吹飞"]]
            },
            {
                "ja": "近所に住む60代の女性は爆発の衝撃音について「家の中にいたら、『ボーン』とかなり大きな音とともに地響きがした。大きな地震のあとで、さらに爆発が起きたので本当に怖かった」と語った。被災地では停電や断水が続き、猛暑の中での車中泊を強いられる被災者も少なくない。水や食料、簡易トイレなどの支援物資の不足が深刻化している。",
                "en": "A woman in her 60s living nearby described the explosion: 'I was at home when I heard a loud 'BOOM' along with ground shaking. After the big earthquake, another explosion occurred, and it was truly terrifying.' Power outages and water shortages continue in the affected areas, and not a few survivors are forced to sleep in their cars in the intense heat. Shortages of support supplies such as water, food, and portable toilets are becoming severe.",
                "literal": "住在附近的60多岁女性谈及爆炸的冲击音：「在家时听到『嘣』的巨大声响同时地面震动。大地震后又发生爆炸，真的很可怕」。灾区持续停电断水，不少灾民被迫在酷暑中车中过夜。水、食物、简易厕所等支援物资的不足正在严重化。",
                "grammar": "「〜について」— 关于…。例：衝撃音について（关于冲击音）。\n「〜とともに」— 与…同时。例：音とともに（与声音同时）。\n「〜を強いられる」— 被迫…。例：車中泊を強いられる（被迫在车中过夜）。",
                "vocab": [["衝撃音", "しょうげきおん", "冲击音"], ["地響き", "じひびき", "地鸣、地面震动"], ["停電", "ていでん", "停电"], ["断水", "だんすい", "断水"], ["車中泊", "しゃちゅうはく", "车内过夜"], ["支援物資", "しえんぶっし", "支援物资"]]
            }
        ]
    },
    {
        "slug": "matsunoya-mama-ouen-natsu",
        "title": "松のや「ママ応援企画」に批判 謝罪し「夏休み企画」に変更",
        "subtitle": "とんかつ専門店「松のや」が「ママ応援企画」を発表するも批判受け謝罪。「夏休み企画」に変更し、どなたでも利用可能に。",
        "paras": [
            {
                "ja": "松屋フーズが展開するとんかつ専門店「松のや」の公式Xが30日、「ママ応援企画」に批判が寄せられたことから「夏休み企画」に変更し、キャンペーンを実施すると告知した。「15歳以下のお子さんとママさんが使えます」という内容に、SNS上で「独身女性はダメで子持ちのママはいいの？」といった批判の声が相次いでいた。",
                "en": "The official X (formerly Twitter) account of Matsuya Foods' tonkatsu specialty restaurant 'Matsu no Ya' announced on the 30th that it would change its promotion from a 'Mom Support Campaign' to a 'Summer Vacation Campaign' following criticism. The original offer stated it could be used 'by children 15 and under and their moms,' which drew criticism on social media such as, 'So unmarried women can't use it but mothers can?'",
                "literal": "松屋食品运营的炸猪排专门店「松之屋」的官方X于30日公告，因「妈妈应援企划」遭到批评，变更为「暑假企划」并实施活动。「15岁以下孩子和妈妈可使用」的内容在SNS上相继招来「单身女性不行，有孩子的妈妈就行？」等批评。",
                "grammar": "「〜ことから」— 因为…。例：批判が寄せられたことから（因为收到了批评）。\n「〜という内容に」— 对于…的内容。例：使えますという内容に（对于「可以使用」的内容）。\n「〜相次いでいた」— 接连发生。例：批判が相次いでいた（批评接连不断）。",
                "vocab": [["展開する", "てんかいする", "开展、运营"], ["とんかつ", "とんかつ", "炸猪排"], ["キャンペーン", "きゃんぺーん", "宣传活动"], ["批判", "ひはん", "批评"], ["謝罪する", "しゃざいする", "道歉"], ["独身", "どくしん", "单身"]]
            },
            {
                "ja": "同日、公式Xは「皆さまのコメントを読んで、『たしかにその通りだな』と感じました。配慮が足りず、申し訳ありません」と謝罪した。その後「15歳以下のお子さんとその保護者の方が使えます」と修正し、キャンペーンを「夏休み企画」として再スタートさせることを発表した。SNS上では対応を評価する声も多く見られた。",
                "en": "On the same day, the official X account apologized, saying, 'After reading everyone's comments, we felt, 'You're absolutely right.' Our consideration was insufficient, and we apologize.' They then revised the offer to 'usable by children 15 and under and their guardians' and announced the campaign would restart as a 'Summer Vacation Campaign.' Many voices on social media also praised the response.",
                "literal": "同日，官方X道歉说「阅读了大家的评论，确实觉得『说得对』。考虑不周，非常抱歉」。之后修正为「15岁以下孩子及其监护人可使用」，并宣布活动作为「暑假企划」重新启动。在SNS上也能看到很多评价对应措施的声音。",
                "grammar": "「〜て」— 表示原因或并列。例：読んで（读了之后）。\n「〜と感じました」— 感觉到…。例：その通りだなと感じました（感觉到说得对）。\n「〜として」— 作为…。例：夏休み企画として（作为暑假企划）。",
                "vocab": [["配慮", "はいりょ", "关怀、考虑"], ["修正する", "しゅうせいする", "修正"], ["保護者", "ほごしゃ", "监护人"], ["再スタート", "さいすたーと", "重新启动"], ["評価する", "ひょうかする", "评价"], ["対応", "たいおう", "应对、对应"]]
            }
        ]
    },
    {
        "slug": "fukuoka-kengikai-kingin",
        "title": "福岡県議会「カツアゲ問題」 告発議員を支える重鎮とフジ人気アナ",
        "subtitle": "カネを要求されたと告発する吉松県議に対し、背後には全国的に知られる重鎮議員が存在。その姪はフジの人気女子アナだった。",
        "paras": [
            {
                "ja": "カネを要求された、カツアゲ同然だ——。福岡県議会の「金銭授受騒動」で揺れる中、告発者の吉松源昭県議（58）は自民党会派幹部から多額の現金を要求されたと主張。幹部との会話を録音したとする音源も公開し、孤立しながらも奮戦している。この吉松氏には、じつは後ろ盾がいることが分かった。その人物とは全国に名を知られる人気アナウンサーと意外な関係があった。",
                "en": "'I was asked for money — it's basically extortion.' Amid the turmoil over 'money exchange' at the Fukuoka Prefectural Assembly, whistleblower assemblyman Motoaki Yoshimatsu (58) claims he was demanded a large sum of cash by ruling party executives. He has also released audio recordings of conversations with the executives and is fighting on despite being isolated. It turns out Yoshimatsu actually has a backer — someone with a surprising connection to a nationally known popular announcer.",
                "literal": "被要求给钱，简直像敲诈——。福冈县议会的「金钱授受骚动」中，告发者吉松源昭县议（58岁）主张被自党派系干部要求了巨额现金。还公开了与干部对话的录音，孤军奋战。吉松氏实际上有后台。该人物与全国知名的人气女播音员有着意外关系。",
                "grammar": "「〜同然だ」— 简直是…。例：カツアゲ同然だ（简直是敲诈）。\n「〜とする」— 作为…的。例：録音したとする音源（作为进行了录音的音源）。\n「〜ことが分かった」— 判明…。例：後ろ盾がいることが分かった（判明有后台）。",
                "vocab": [["カツアゲ", "かつあげ", "敲诈、勒索"], ["金銭授受", "きんせんじゅじゅ", "金钱授受"], ["騒動", "そうどう", "骚动"], ["告発する", "こくはつする", "告发"], ["録音", "ろくおん", "录音"], ["後ろ盾", "うしろだて", "后台、后盾"]]
            },
            {
                "ja": "吉松氏の後ろ盾は、自民党の重鎮・中村明彦議員。中村議員の姪はフジテレビの人気女子アナウンサー・井上清華アナだ。中村議員はかつて井上アナが大学ミスコンの時に「姪に入れてくれんね」と応援していたという。告発者を支える重鎮議員と全国区の人気アナの意外な関係に、ネット上でも話題を集めている。一方、藏内議長側は「事実無根」と否定しており、今後の調査が注目される。",
                "en": "Yoshimatsu's backer is LDP heavyweight Assemblyman Akihiko Nakamura. Nakamura's niece is popular Fuji TV announcer Sayaka Inoue. Nakamura reportedly supported his niece when she was in a university pageant, saying 'Please vote for my niece.' The unexpected relationship between the heavyweight assemblyman supporting the whistleblower and the nationally popular announcer is gathering attention online. Meanwhile, Chairman Kurauchi's side denies the allegations as 'groundless,' and future investigations are being watched closely.",
                "literal": "吉松氏的后盾是自民党重镇中村明彦议员。中村议员的侄女是富士电视台的人气女播音员井上清華。据说中村议员曾在井上主播参加大学选美时为她应援。支持告发者的重镇议员与全国人气播音员的意外关系在网上也引发话题。另一方面，藏内议长方面否认说「毫无事实根据」，今后的调查备受关注。",
                "grammar": "「〜という」— 据说…。例：応援していたという（据说曾应援）。\n「〜ており」— 正在…。例：否定しており（正在否定）。\n「〜が注目される」— …受到关注。例：調査が注目される（调查受到关注）。",
                "vocab": [["重鎮", "じゅうちん", "重镇、重要人物"], ["姪", "めい", "侄女"], ["人気アナウンサー", "にんきあなうんさー", "人气播音员"], ["ミスコン", "みすこん", "选美比赛"], ["話題を集める", "わだいをあつめる", "引发话题"], ["事実無根", "じじつむこん", "毫无事实根据"]]
            }
        ]
    },
    {
        "slug": "juuminzei-hikaze-hikaku",
        "title": "住民税非課税の目安は年収110万円に 国の一律給付なし",
        "subtitle": "2026年度の住民税非課税世帯向け給付の現状。年収110万円が非課税の目安に。国の一律現金給付は実施されず。",
        "paras": [
            {
                "ja": "物価が上がり続けるなか、低所得世帯向けの給付金に関心が集まっている。しかし2026年度は国による一律の現金給付が実施されていない。過去に実施されていた住民税非課税世帯向けの3万円給付も、2025年度分で受付は終了している。住民税非課税の年収目安は約110万円となっている。",
                "en": "Amid continued price increases, attention is focused on benefits for low-income households. However, no uniform cash benefits from the national government have been implemented in fiscal 2026. The 30,000-yen benefit previously provided to households exempt from residence tax also ended with fiscal 2025. The income threshold for residence tax exemption is approximately 1.1 million yen.",
                "literal": "在物价持续上涨中，对低收入家庭的给付金受到关注。但2026年度国家没有实施统一的现金给付。过去实施的面向居民税非課税家庭的3万日元给付也在2025年度结束受理。居民税非课税的年收入标准约为110万日元。",
                "grammar": "「〜なか」— 在…之中。例：上がり続けるなか（在持续上涨之中）。\n「〜向けの」— 面向…的。例：低所得世帯向け（面向低收入家庭）。\n「〜で受付は終了」— 受理在…结束。例：2025年度分で受付は終了（2025年度部分受理结束）。",
                "vocab": [["住民税", "じゅうみんぜい", "居民税"], ["非課税", "ひかぜい", "非课税"], ["低所得", "ていしょとく", "低收入"], ["給付金", "きゅうふきん", "给付金"], ["一律", "いちりつ", "统一、一律"], ["年収", "ねんしゅう", "年收入"]]
            },
            {
                "ja": "2026年6月に成立した令和8年度補正予算では、個人向けの一律現金給付は盛り込まれていない。過去の住民税非課税世帯向け給付の多くは臨時的な措置だった。今後は各自治体が独自に子育て世帯や低所得世帯への支援を実施するケースが増えている。6月に届いた住民税決定通知書を確認し、自身の課税状況を把握しておくことが重要だと専門家はアドバイスしている。",
                "en": "The fiscal 2026 supplementary budget passed in June 2026 did not include any uniform cash benefits for individuals. Most of the past benefits for residence-tax-exempt households were temporary measures. Going forward, there is an increasing number of cases where individual municipalities are implementing their own support for child-rearing households and low-income households. Experts advise that it's important to check the residence tax assessment notice that arrived in June and understand your own tax status.",
                "literal": "2026年6月成立的令和8年度补正预算中未包含面向个人的统一现金给付。过去的面向居民税非课税家庭的给付多为临时性措施。今后，各地方政府自行实施对育儿家庭和低收入家庭支援的案例正在增加。专家建议确认6月送达的居民税决定通知书，掌握自身的课税状况。",
                "grammar": "「〜では」— 在…方面。例：補正予算では（在补正预算方面）。\n「〜たものの」— 虽然是…但是…（此处未使用）。\n「〜ておく」— 事先做好…。例：把握しておく（事先掌握）。\n「〜とアドバイスしている」— 建议说…。",
                "vocab": [["補正予算", "ほせいよさん", "补正预算"], ["盛り込む", "もりこむ", "纳入、包含"], ["臨時的", "りんじてき", "临时性"], ["措置", "そち", "措施"], ["自治体", "じちたい", "地方政府"], ["課税状況", "かぜいじょうきょう", "课税状况"]]
            }
        ]
    },
    {
        "slug": "doru157en-kawase-kainyu",
        "title": "ドル円 一時157円台に急騰 政府・日銀が為替介入か",
        "subtitle": "外国為替市場で円相場が一時1ドル157円台まで急騰。政府・日銀の円買い介入との見方が強まる。",
        "paras": [
            {
                "ja": "外国為替市場でドル円相場が急速に5円近く円高方向に傾いた。政府・日銀による為替介入の可能性がある。円相場は30日夜、1ドル＝162円台後半で推移していたが、午後10時半すぎから円が一気に買われ、1ドル＝157円台後半まで5円近く円高に振れる場面があった。157円台をつけるのは今年5月以来のことだ。",
                "en": "In the foreign exchange market, the dollar-yen rate rapidly moved nearly 5 yen in the yen's favor. There is a possibility of currency intervention by the government and the Bank of Japan. The yen was trading in the upper 162 yen range against the dollar on the evening of the 30th, but after 10:30 PM, the yen was suddenly bought up, swinging nearly 5 yen stronger to the upper 157 yen range. The 157 yen level was last seen in May of this year.",
                "literal": "在外汇市场上，美元日元汇率急速向日元升值方向倾斜了约5日元。存在政府·日银进行汇率干预的可能性。日元汇率30日晚间在1美元=162日元后半段推移，但晚上10点半过后日元被一口气买入，出现一度升至1美元=157日元后半段、升值近5日元的情况。触及157日元区间是今年5月以来首次。",
                "grammar": "「〜方向に傾いた」— 向…方向倾斜。例：円高方向に傾いた（向日元升值方向倾斜）。\n「〜可能性がある」— 有…的可能性。例：為替介入の可能性がある（有汇率干预的可能性）。\n「〜以来」— 以来。例：5月以来（5月以来）。",
                "vocab": [["外国為替市場", "がいこくかわせしじょう", "外汇市场"], ["円高", "えんだか", "日元升值"], ["為替介入", "かわせかいにゅう", "汇率干预"], ["推移する", "すいいする", "推移"], ["急騰する", "きゅうとうする", "急剧上涨"], ["円買い", "えんがい", "买入日元"]]
            },
            {
                "ja": "市場関係者からは政府・日銀が円買い・ドル売りの為替介入に踏み切ったとの見方が出ている。政府・日銀は4月末から5月にかけて11.7兆円規模の為替介入を実施したものの、2か月足らずで元の円安水準まで戻っている。今回の介入でも円安を根本的に食い止められるかは未知数だ。今後の為替動向に引き続き注目が必要だ。",
                "en": "Market participants believe the government and BOJ have stepped into yen-buying, dollar-selling intervention. Although the government and BOJ implemented approximately 11.7 trillion yen in currency intervention from late April to May, the yen returned to its original weak levels in less than two months. Whether this intervention can fundamentally stem the yen's weakness remains uncertain. Continued attention to future exchange rate movements is necessary.",
                "literal": "市场相关人士认为政府·日银已采取买入日元、卖出美元的汇率干预措施。政府·日银虽然从4月末到5月实施了约11.7万亿日元的汇率干预，但不到2个月就回到了原来的日元贬值水平。即使此次干预能否从根本上阻止日元贬值仍是未知数。需要继续关注今后的汇率动向。",
                "grammar": "「〜との見方」— …的看法。例：踏み切ったとの見方（认为已采取行动的看法）。\n「〜ものの」— 虽然…但是…。例：実施したものの（虽然实施了但…）。\n「〜かは未知数だ」— 是否…尚不可知。",
                "vocab": [["市場関係者", "しじょうかんけいしゃ", "市场相关人士"], ["踏み切る", "ふみきる", "下决心、采取行动"], ["円安", "えんやす", "日元贬值"], ["食い止める", "くいとめる", "阻止、遏制"], ["未知数", "みちすう", "未知数"], ["動向", "どうこう", "动向"]]
            }
        ]
    },
    {
        "slug": "souri-kumamoto-nyuuri",
        "title": "首相 8月3日にも熊本入り 被災状況を把握へ",
        "subtitle": "高市首相が熊本地震の被災状況把握のため8月3日にも熊本県入りする調整。停電や断水、車中泊の被災者も少なくない。",
        "paras": [
            {
                "ja": "高市早苗首相は熊本地震の被災状況を把握するため、8月3日にも熊本県入りする調整に入った。現地の受け入れ態勢や天候を見極めて最終判断する。複数の政府関係者が30日、明らかにした。現地では停電や断水が続き、猛暑の中で車中泊をする被災者も少なくない。首相は自治体関係者らと意見交換し、今後の復旧・復興対策に生かしたい考えだ。",
                "en": "Prime Minister Takaichi has begun coordination to visit Kumamoto Prefecture as early as August 3rd to assess the damage from the Kumamoto earthquake. The final decision will be made based on the local reception situation and weather conditions, as multiple government sources revealed on the 30th. Power outages and water shortages continue in the affected areas, and not a few evacuees are sleeping in their cars in the intense heat. The Prime Minister plans to exchange opinions with local government officials and utilize the information for future recovery and reconstruction measures.",
                "literal": "高市早苗首相为了把握熊本地震的受灾状况，已进入协调8月3日访问熊本县的阶段。将根据当地接收态势和天气做出最终判断。多位政府相关人士于30日公布。当地持续停电断水，酷暑中不得不在车内过夜的灾民也不在少数。首相将与地方政府相关人员交换意见，希望活用于今后的修复·复兴对策。",
                "grammar": "「〜にも」— 最早在…（时间）。例：8月3日にも（最早在8月3日）。\n「〜調整に入った」— 进入协调阶段。例：入りする調整に入った（进入访问的协调阶段）。\n「〜考えだ」— 打算…。例：生かしたい考えだ（打算活用于）。",
                "vocab": [["被災状況", "ひさいじょうきょう", "受灾状况"], ["調整に入る", "ちょうせいにはいる", "进入协调"], ["受け入れ態勢", "うけいれたいせい", "接收态势"], ["見極める", "みきわめる", "看清、判断"], ["復旧", "ふっきゅう", "修复"], ["復興", "ふっこう", "复兴"]]
            },
            {
                "ja": "首相は30日の非常災害対策本部会議で「自治体のニーズを踏まえ、政府一丸となって取り組む」と述べ、必要な物資の確保やインフラ復旧に全力を挙げるよう関係閣僚に指示した。熊本県では28日の地震以降、余震が続いており、被災者の不安は続いている。政府は被災地への支援体制を強化している。",
                "en": "At the Emergency Disaster Response Headquarters meeting on the 30th, the Prime Minister stated, 'We will work together as one government based on the needs of local governments,' and instructed relevant ministers to make every effort to secure necessary supplies and restore infrastructure. Aftershocks have continued in Kumamoto Prefecture since the earthquake on the 28th, and the anxiety of affected residents persists. The government is strengthening its support system for the disaster area.",
                "literal": "首相在30日的非常灾害对策本部会议上表示「基于地方政府的需要，政府团结一致应对」，指示相关阁僚全力确保必要物资和基础设施修复。熊本县自28日地震以来余震持续，受灾者的不安仍在持续。政府正在强化对灾区的支援体制。",
                "grammar": "「〜を踏まえ」— 基于…。例：ニーズを踏まえ（基于需求）。\n「〜一丸となって」— 团结一致。例：政府一丸となって（政府团结一致）。\n「〜よう指示した」— 指示…。例：挙げるよう指示した（指示全力…）。",
                "vocab": [["非常災害", "ひじょうさいがい", "非常灾害"], ["対策本部", "たいさくほんぶ", "对策总部"], ["物資", "ぶっし", "物资"], ["インフラ", "いんふら", "基础设施"], ["余震", "よしん", "余震"], ["支援体制", "しえんたいせい", "支援体制"]]
            }
        ]
    },
    {
        "slug": "senbotsusha-izoku-50nen-gosiharu",
        "title": "戦没者遺族への特別弔慰金 50年間誤って支給 総額180万円",
        "subtitle": "ある戦没者遺族に対し、県が50年間にわたり要件を満たさない特別弔慰金を支給し続けていたことが判明。総額180万円。",
        "paras": [
            {
                "ja": "太平洋戦争の戦没者遺族に支給する特別弔慰金について、県が支給要件を満たさない遺族に対し、50年間にわたり誤って支給していたことが分かった。県によると、県内に本籍地がある戦没者の遺族1人に対してで、1976年から50年間にわたり総額は180万円にのぼるという。今年2月の審査で要件を満たしていないことが判明し、県はこの遺族に説明と謝罪をした上で、返還請求権が消滅していない過去5年分の25万円の返還手続きを進めている。",
                "en": "Regarding special condolence payments to families of war dead from the Pacific War, it has been revealed that a prefectural government had been mistakenly making payments for 50 years to a family that did not meet the eligibility requirements. According to the prefecture, for one bereaved family of a war dead whose registered domicile is in the prefecture, the total amount reached 1.8 million yen over 50 years starting from 1976. In February of this year, a review revealed that the requirements were not met. After explaining and apologizing to the family, the prefecture is proceeding with procedures to recover 250,000 yen for the past five years, for which the right to claim restitution has not yet expired.",
                "literal": "关于向太平洋战争阵亡者遗属支付的特别吊慰金，县被发现对不满足支付要件的遗属，持续50年错误支付。据县称，对县内户籍地的1名阵亡者遗属，从1976年起50年间总额达180万日元。今年2月的审查中发现不满足条件，县在向该遗属说明和道歉后，正在推进对请求权尚未消灭的过去5年部分25万日元的返还手续。",
                "grammar": "「〜について」— 关于…。例：特別弔慰金について（关于特别吊慰金）。\n「〜にわたり」— 长达…（时间）。例：50年間にわたり（长达50年）。\n「〜た上で」— 在…之后。例：謝罪した上で（在道歉之后）。",
                "vocab": [["戦没者", "せんぼつしゃ", "阵亡者"], ["遺族", "いぞく", "遗属"], ["特別弔慰金", "とくべつちょういきん", "特别吊慰金"], ["本籍地", "ほんせきち", "户籍地"], ["返還", "へんかん", "返还、归还"], ["審査", "しんさ", "审查"]]
            },
            {
                "ja": "なお個人の特定につながる恐れがあるとして、遺族の年代や性別、満たしていなかった要件などは明らかにしていない。県は「誠に申し訳ございません」と陳謝し、審査に不十分な点があったとして再発防止に努めるとしている。長年にわたる行政のミスに、専門家はチェック体制の強化が必要だと指摘している。",
                "en": "To avoid identifying the individual, the prefecture has not disclosed the bereaved family member's age, gender, or the specific requirements that were not met. The prefecture apologized, saying 'We are truly sorry,' acknowledging that there were deficiencies in the screening process, and stated it would work to prevent recurrence. Regarding this long-standing administrative error, experts point out the need to strengthen the checking system.",
                "literal": "鉴于有可能导致个人被特定，遗属的年龄、性别以及未满足的要件等不予公开。县表示「非常抱歉」并道歉，承认审查有不充分之处，将致力于防止再次发生。对于长期持续的行政失误，专家指出需要加强检查体制。",
                "grammar": "「〜として」— 作为理由。例：恐れがあるとして（因为有可能…）。\n「〜努めるとしている」— 表示致力于…。例：再発防止に努めるとしている（致力于防止再发）。\n「〜と指摘している」— 指出…。例：強化が必要だと指摘（指出需要加强）。",
                "vocab": [["特定", "とくてい", "特定"], ["陳謝する", "ちんしゃする", "道歉、致歉"], ["不十分", "ふじゅうぶん", "不充分"], ["再発防止", "さいはつぼうし", "防止再次发生"], ["行政", "ぎょうせい", "行政"], ["チェック体制", "ちぇっくたいせい", "检查体制"]]
            }
        ]
    },
    {
        "slug": "onward-aeon-kumamoto-shain",
        "title": "オンワードが従業員の死亡を発表 イオンモール熊本",
        "subtitle": "アパレル大手オンワードHDがイオンモール熊本の爆発事故で従業員1人の死亡を発表。他に2人の安否確認を進める。",
        "paras": [
            {
                "ja": "アパレル大手のオンワードホールディングスは爆発事故があったイオンモール熊本で従業員1人が亡くなったと発表した。他に従業員2人の安否確認を進めている。オンワードグループはイオンモール熊本に「エニィスィス」「ウィゴー」の2店舗を出店している。同社は「ご冥福を心からお祈り申し上げるとともに、ご遺族の皆様に衷心よりお悔み申し上げます」とコメントしている。",
                "en": "Major apparel company Onward Holdings announced that one employee died in the explosion accident at Aeon Mall Kumamoto. The company is also working to confirm the safety of two other employees. The Onward Group operates two stores at Aeon Mall Kumamoto — 'Any Sis' and 'Wego.' The company commented, 'We sincerely pray for their soul and extend our deepest condolences to the bereaved family.'",
                "literal": "服装大手Onward Holdings宣布，在发生爆炸事故的AEON MALL熊本有1名员工死亡。另外正在确认其他2名员工的安全。Onward集团在AEON MALL熊本开设了「Any Sis」「Wego」2家店铺。该公司表示「衷心祈愿冥福的同时，向遗属致以诚挚哀悼」。",
                "grammar": "「〜と発表した」— 发表了…。例：亡くなったと発表した（发表了死亡的消息）。\n「〜を進めている」— 正在推进…。例：安否確認を進めている（正在确认安危）。\n「〜とともに」— 与…同时。例：お祈りするとともに（在祈祷的同时）。",
                "vocab": [["アパレル", "あぱれる", "服装"], ["大手", "おおて", "大企业"], ["従業員", "じゅうぎょういん", "员工"], ["発表する", "はっぴょうする", "发表"], ["安否確認", "あんぴかくにん", "安危确认"], ["ご冥福", "ごめいふく", "冥福"]]
            },
            {
                "ja": "イオンによると、イオンモール熊本では専門店の従業員7人の死亡が確認されている。従業員約2700人の安否確認は完了しているという。今回の地震と爆発により、イオンモール熊本の建物は大きく損傷し、周辺地域の経済活動にも深刻な影響が出ている。政府は被災企業への支援策を検討している。",
                "en": "According to Aeon, seven deaths of specialty store employees have been confirmed at Aeon Mall Kumamoto. Safety confirmation for approximately 2,700 employees has been completed. Due to the earthquake and explosion, the Aeon Mall Kumamoto building was severely damaged, also having a serious impact on economic activity in the surrounding area. The government is considering support measures for affected businesses.",
                "literal": "据AEON称，AEON MALL熊本已确认7名专卖店员工死亡。约2700名员工的安危确认已完成。受此次地震和爆炸影响，AEON MALL熊本的建筑严重损坏，周边地区的经济活动也受到严重影响。政府正在讨论对受灾企业的支援措施。",
                "grammar": "「〜によると」— 据…称。例：イオンによると（据AEON称）。\n「〜により」— 由于…。例：地震と爆発により（由于地震和爆炸）。\n「〜に出ている」— 正在出现…。例：影響が出ている（正在出现影响）。",
                "vocab": [["死亡", "しぼう", "死亡"], ["確認", "かくにん", "确认"], ["損傷", "そんしょう", "损坏、损伤"], ["経済活動", "けいざいかつどう", "经济活动"], ["深刻", "しんこく", "深刻"], ["支援策", "しえんさく", "支援措施"]]
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
