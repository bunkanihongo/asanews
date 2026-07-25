#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-07-26 (Sun) Edition"""
import json, os, sys, subprocess, time, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-07-26'
tok = dictionary.Dictionary().create()
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
    for t in tok.tokenize(text):
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
    try:
        subprocess.run(
            ['edge-tts', '--voice', 'ja-JP-NanamiNeural',
             '--text', text, '--write-media', outpath],
            capture_output=True, timeout=180)
    except Exception as e:
        print(f"   ⚠️ edge-tts error: {e}")
        return False
    return os.path.exists(outpath) and os.path.getsize(outpath) > 1000

# ==================================================================
# TODAY'S ARTICLES — 2026-07-26
# ==================================================================
articles = [
    {
        "slug": "fukutokyo-kakuchi-meigori",
        "title": "副首都に大阪・福岡・愛知が名乗り 北海道・宮城も意欲",
        "subtitle": "副首都構想関連法が成立したことを受け、各地の知事が名乗りを上げている。大阪・福岡・愛知に加え、北海道と宮城も意欲を示した。",
        "paras": [
            {
                "ja": "副首都構想関連法が24日に成立したことを受け、複数の道府県が名乗りを上げている。大阪府の吉村知事は「副首都は複数あるべきだ」と述べ、来春にも住民投票を実施したい考えだ。福岡県の服部知事は「オール福岡で取り組む」と表明し、北海道の鈴木知事も札幌市と協議を進める方針を示した。",
                "en": "Following the enactment of the sub-capital related legislation on the 24th, multiple prefectures have thrown their hats into the ring. Osaka Governor Yoshimura stated that 'there should be multiple sub-capitals' and expressed his intention to hold a referendum as early as next spring. Fukuoka Governor Hattori declared they would tackle it 'as a united Fukuoka,' and Hokkaido Governor Suzuki indicated a policy of moving forward with discussions in Sapporo.",
                "literal": "随着副首都相关法律于24日成立，多个道府县纷纷表态参与。大阪府知事吉村表示「副首都应该有多个」，有意最快明年春季实施居民投票。福冈县知事服部表明「举全福冈之力推进」，北海道知事铃木也表示将与札幌市推进协商。",
                "grammar": "「〜を受け」— 基于…、随着…。例：成立したことを受け（随着法律成立）。\n「〜考えだ」— 表示打算/想法。例：実施したい考えだ（打算实施）。\n「〜方針を示した」— 显示了…方针。例：進める方針を示した（显示了推进的方针）。",
                "vocab": [
                    ["副首都", "ふくしゅと", "副首都"],
                    ["名乗りを上げる", "なのりをあげる", "表态参加、报名"],
                    ["知事", "ちじ", "知事（都道府县首长）"],
                    ["住民投票", "じゅうみんとうひょう", "居民投票"],
                    ["協議", "きょうぎ", "协商、协议"]
                ]
            },
            {
                "ja": "一方、東京都の小池知事は「東京一極集中の是正」という言葉に警戒感を示した。地方交付税制度などの構造的な問題の責任を東京に転嫁するものだとの認識を示し、「そういう言葉を聞くたびに危機感を覚えてしまう」と批判した。副首都に指定されれば規制緩和や税制優遇措置などが受けられる見込みで、今後の動きが注目される。",
                "en": "Meanwhile, Tokyo Governor Koike expressed wariness about the phrase 'correcting the excessive concentration in Tokyo,' indicating her view that it shifts responsibility for structural issues such as the local allocation tax system onto Tokyo, and criticized that 'every time I hear those words, I feel a sense of crisis.' Being designated as a sub-capital is expected to bring deregulation and tax incentives, so future developments are drawing attention.",
                "literal": "另一方面，东京都知事小池对「纠正东京一极集中」这一说法表现出警惕。她指出这似乎是将地方交付税制度等结构性问题的责任转嫁给东京，批评说「每次听到这种话都会感到危机感」。若被指定为副首都，有望获得放宽管制和税制优惠等政策，今后的动向备受关注。",
                "grammar": "「〜たびに」— 每次…。例：聞くたびに（每次听到）。\n「〜ものだ」— 表示性质/理应。例：転嫁するものだ（是转嫁给…的）。\n「〜見込みで」— 预计…。例：受けられる見込みで（预计可以享受）。",
                "vocab": [
                    ["警戒感", "けいかいかん", "警惕感"],
                    ["一極集中", "いっきょくしゅうちゅう", "一极集中"],
                    ["地方交付税", "ちほうこうふぜい", "地方交付税"],
                    ["規制緩和", "きせいかんわ", "放松管制"],
                    ["税制優遇", "ぜいせいゆうぐう", "税收优惠"]
                ]
            }
        ]
    },
    {
        "slug": "shinagawa-mansion-kaji",
        "title": "品川区のマンションで火事 ソーラーパネル充電中に出火か",
        "subtitle": "東京・品川区の11階建てマンションで火事があり、5階バルコニーが焼けた。住人がソーラーパネルを使って充電中だった。",
        "paras": [
            {
                "ja": "25日午後、東京・品川区の東急目黒線「不動前駅」近くにある11階建てマンションで火事があった。「燃えている」と目撃者から通報があり、消防車22台が出動した。火は約2時間半後に消し止められ、5階のバルコニー外壁15平方メートルが焼けた。住人は避難したが、けが人はいない。",
                "en": "On the afternoon of the 25th, a fire broke out in an 11-story apartment building near Fudomae Station on the Tokyu Meguro Line in Shinagawa, Tokyo. A witness reported 'it's burning,' and 22 fire trucks were dispatched. The fire was extinguished about two and a half hours later, with 15 square meters of the 5th-floor balcony exterior wall burned. Residents evacuated but no injuries were reported.",
                "literal": "25日下午，东京品川区东急目黑线「不动前站」附近的11层公寓发生火灾。有目击者通报「着火了」，22辆消防车出动。大火约两个半小时后被扑灭，5楼阳台外壁15平方米被烧毁。住户进行了避难，但无人员受伤。",
                "grammar": "「〜近くにある」— 在…附近。例：駅近くにある（在车站附近）。\n「〜ことから」— 因为…。例：通報があった（因为有通报）。\n「〜が、〜」— 虽然…但是…。例：避難したが、けが人はいない（虽然避难了，但无受伤者）。",
                "vocab": [
                    ["マンション", "まんしょん", "公寓楼"],
                    ["火事", "かじ", "火灾"],
                    ["バルコニー", "ばるこにー", "阳台"],
                    ["出動", "しゅつどう", "出动"],
                    ["消し止める", "けしとめる", "扑灭"]
                ]
            },
            {
                "ja": "警視庁によると、当時5階の住人がバルコニーでソーラーパネルを使って充電しており、そこから出火した可能性があるという。ソーラーパネルをバルコニーに設置して家庭用電源として使用するケースが増えているが、専門家は「正しい知識と設置方法が必要だ」と注意を呼びかけている。警視庁と東京消防庁が詳しい出火原因を調べている。",
                "en": "According to the Metropolitan Police Department, a resident on the 5th floor was charging using a solar panel on the balcony at the time, and that may have been the source of the fire. Cases of installing solar panels on balconies for household power are increasing, but experts are urging caution, saying 'proper knowledge and installation methods are necessary.' The police and fire department are investigating the exact cause.",
                "literal": "据警视厅称，当时5楼住户在阳台上使用太阳能板充电，有可能因此引发火灾。在阳台安装太阳能板作为家用电源的案例正在增加，但专家呼吁注意「需要正确的知识和安装方法」。警视厅和东京消防厅正在调查详细起火原因。",
                "grammar": "「〜可能性がある」— 有…可能性。例：出火した可能性がある（有可能起火）。\n「〜ケースが増えている」— …情况在增加。例：使用するケースが増えている（使用的情况在增加）。\n「〜よう呼びかけている」— 呼吁…。例：注意を呼びかけている（呼吁注意）。",
                "vocab": [
                    ["ソーラーパネル", "そーらーぱねる", "太阳能板"],
                    ["充電", "じゅうでん", "充电"],
                    ["出火", "しゅっか", "起火"],
                    ["設置", "せっち", "设置、安装"],
                    ["呼びかける", "よびかける", "呼吁"]
                ]
            }
        ]
    },
    {
        "slug": "okayadokari-4163-taiho",
        "title": "天然記念物オカヤドカリ4163匹を発送 中国籍の男3人逮捕",
        "subtitle": "国指定天然記念物のオカヤドカリ約4000匹を許可なく捕獲し、段ボールに詰めて発送しようとした中国人3人が逮捕された。",
        "paras": [
            {
                "ja": "国指定の天然記念物オカヤドカリ4163匹を許可なく捕獲し、段ボール箱に詰めて発送しようとした中国籍の男3人が、文化財保護法違反の疑いで逮捕された。配送業者が段ボールの中から「ガサゴソ」という音に気付き、警察に通報した。3人は沖縄県内で捕獲し、コンビニから発送しようとしていた。",
                "en": "Three Chinese men were arrested on suspicion of violating the Cultural Properties Protection Law for capturing 4,163 Okinawan hermit crabs—a nationally designated natural monument—without permission and attempting to ship them packed in cardboard boxes. A delivery company noticed rustling sounds from the boxes and alerted police. The three had captured them within Okinawa Prefecture and were attempting to ship them from a convenience store.",
                "literal": "涉嫌未经许可捕获国家指定天然纪念物——陆寄居蟹4163只并将其装入纸箱试图发货的3名中国籍男子，因涉嫌违反文化财保护法被逮捕。快递公司注意到纸箱中传出「嘎沙嘎沙」的声音并报警。三人在冲绳县内捕获，并试图从便利店发货。",
                "grammar": "「〜疑いで逮捕」— 以…嫌疑逮捕。例：違反の疑いで逮捕（以违反嫌疑逮捕）。\n「〜中から」— 从…里面。例：段ボールの中から（从纸箱里面）。\n「〜ようとしていた」— 正想要…。例：発送しようとしていた（正想要发货）。",
                "vocab": [
                    ["天然記念物", "てんねんきねんぶつ", "天然纪念物"],
                    ["オカヤドカリ", "おかやどかり", "陆寄居蟹"],
                    ["捕獲", "ほかく", "捕获"],
                    ["文化財保護法", "ぶんかざいほごほう", "文化财保护法"],
                    ["段ボール", "だんぼーる", "纸箱"]
                ]
            },
            {
                "ja": "県内では2023年以降、外国人がオカヤドカリを無断で移動させようとする事件が相次いでいる。専門家は「生息環境が悪化している中で、ペットブームによる大量採取が個体群を減少させる恐れがある」と警鐘を鳴らす。オカヤドカリは国内に7種の生息が確認されており、すべてが国の天然記念物に指定されている。許可なく捕獲や移動をすることは原則禁止されている。",
                "en": "Since 2023, there have been a series of incidents in the prefecture involving foreigners attempting to illegally transport hermit crabs. Experts warn that 'amid deteriorating habitats, mass collection driven by the pet boom risks reducing the population.' Seven species of hermit crabs are confirmed to inhabit Japan, all designated as national natural monuments. In principle, capturing or transporting them without permission is prohibited.",
                "literal": "在该县，自2023年以来，外国人试图擅自移动陆寄居蟹的事件接连发生。专家警告称「在栖息环境不断恶化的情况下，宠物热潮导致的大量采集有可能使种群减少」。日本国内确认栖息着7种陆寄居蟹，全部被指定为国家天然纪念物。未经许可的捕获和移动原则上被禁止。",
                "grammar": "「〜以降」— …以后。例：2023年以降（2023年以后）。\n「〜相次ぐ」— 接连发生。例：事件が相次いでいる（事件接连发生）。\n「〜恐れがある」— 有…危险。例：減少させる恐れがある（有可能减少）。",
                "vocab": [
                    ["相次ぐ", "あいつぐ", "接连发生"],
                    ["生息環境", "せいそくかんきょう", "栖息环境"],
                    ["ペットブーム", "ぺっとぶーむ", "宠物热潮"],
                    ["個体群", "こたいぐん", "种群"],
                    ["警鐘", "けいしょう", "警钟、警示"]
                ]
            }
        ]
    },
    {
        "slug": "chugokujin-kankoku-hanchuu",
        "title": "習近平「日本は危険」で中国人が韓国へ 反中感情が爆発",
        "subtitle": "中国政府が日本への渡航自粛を呼びかけた結果、中国人観光客が韓国に殺到。韓国では反中デモが拡大している。",
        "paras": [
            {
                "ja": "中国政府が台湾問題をめぐり「日本は危険」と自国民に日本への渡航自粛を呼びかけた結果、多くの中国人観光客が韓国に向かった。韓国では中国人観光客の消費額が月間記録を更新する一方、激増する観光客に対し現地では反中感情が高まっている。観光地ではトラブルも相次ぎ、政府と国民の間で認識のズレが生じている。",
                "en": "As a result of the Chinese government calling on its citizens to refrain from traveling to Japan over the Taiwan issue, telling them 'Japan is dangerous,' many Chinese tourists have headed to Korea instead. While Chinese tourist spending in Korea has set monthly records, anti-China sentiment is rising locally amid the surge. Troubles at tourist spots are occurring one after another, creating a gap in perception between the government and its citizens.",
                "literal": "中国政府围绕台湾问题呼吁本国公民「日本危险」并要求避免赴日的结果，大量中国游客涌向韩国。在韩国，中国游客消费额刷新月度记录的同时，面对激增的游客，当地反中情绪正在高涨。旅游地纠纷接连不断，政府与国民之间产生了认识分歧。",
                "grammar": "「〜をめぐり」— 围绕…。例：台湾問題をめぐり（围绕台湾问题）。\n「〜一方」— 一方面…另一方面…。例：記録を更新する一方（一方面刷新记录）。\n「〜ズレが生じる」— 产生偏差。例：認識のズレが生じている（产生了认识偏差）。",
                "vocab": [
                    ["渡航自粛", "とこうじしゅく", "避免出境旅行"],
                    ["殺到", "さっとう", "蜂拥而至"],
                    ["消費額", "しょうひがく", "消费额"],
                    ["反中感情", "はんちゅうかんじょう", "反中情绪"],
                    ["トラブル", "とらぶる", "纠纷、麻烦"]
                ]
            },
            {
                "ja": "5月のインバウンド旅行者によるクレジットカード消費額は2兆1200億ウォン（約2330億円）に達し、月間初の2兆ウォン突破となった。前年同月比で67.1％増で、中国人旅行者の消費額は前年比3倍超に膨らんでいる。韓国政府は中国人団体客向けビザなし入国制度を年末まで延長したが、SNS上では中国人観光客のマナーを巡る批判が広がっている。",
                "en": "Credit card spending by inbound travelers in May reached 2.12 trillion won (approx. 233 billion yen), breaking the 2 trillion won monthly mark for the first time. This represents a 67.1% increase year-on-year, with Chinese tourist spending swelling to more than triple the previous year. The Korean government extended the visa-free entry system for Chinese group tourists until the end of the year, but criticism over Chinese tourist manners is spreading on social media.",
                "literal": "5月份入境游客的信用卡消费额达到2.12万亿韩元（约2330亿日元），首次突破月均2万亿韩元大关。同比增长67.1%，中国游客的消费额膨胀至前一年的3倍以上。韩国政府将针对中国团体游客的免签入境制度延长至年底，但社交媒体上针对中国游客礼仪的批评正在蔓延。",
                "grammar": "「〜に達する」— 达到…。例：2兆ウォンに達した（达到2万亿韩元）。\n「〜比」— 与…相比。例：前年比3倍超（比前一年超过3倍）。\n「〜を巡る」— 围绕…。例：マナーを巡る批判（围绕礼仪的批评）。",
                "vocab": [
                    ["インバウンド", "いんばうんど", "入境（游客）"],
                    ["クレジットカード", "くれじっとかーど", "信用卡"],
                    ["ビザなし", "びざなし", "免签证"],
                    ["マナー", "まなー", "礼仪、礼貌"],
                    ["延長", "えんちょう", "延长"]
                ]
            }
        ]
    },
    {
        "slug": "ukuraina-dorone-taikoku",
        "title": "ウクライナが「ドローン大国」に変貌 生産量は年間300万〜600万機",
        "subtitle": "開戦から4年、ウクライナは欧米から武器をもらう立場から、自国でドローンを開発・輸出する「ドローン大国」へと変貌した。",
        "paras": [
            {
                "ja": "ロシアの侵攻開始から4年以上が経過したウクライナは、今や「ドローン大国」へと変貌を遂げている。年間のドローン生産量は300万〜600万機に達し、ロシア軍の標的への破壊・損傷の約8割をドローンが占める。かつて欧米から武器の供与を受けていたウクライナだが、今では米国からドローンの輸出を求められる立場になった。",
                "en": "More than four years after the start of Russia's invasion, Ukraine has transformed into a 'drone superpower.' Annual drone production has reached 3 to 6 million units, with drones accounting for about 80% of destruction and damage to Russian military targets. Once a recipient of weapons from the West, Ukraine has now reached a position where the US is asking it to export drones.",
                "literal": "俄罗斯入侵开始已过去4年多的乌克兰，如今已转变为「无人机大国」。年无人机产量达到300万至600万架，对俄军目标的破坏和损伤中约8成由无人机完成。曾经从欧美接受武器供应的乌克兰，如今却处于被美国要求出口无人机的立场。",
                "grammar": "「〜を遂げる」— 实现…、完成…。例：変貌を遂げている（实现了转变）。\n「〜に達する」— 达到…。例：600万機に達する（达到600万架）。\n「〜立場になった」— 变成了…立场。例：求められる立場になった（变成了被要求的立场）。",
                "vocab": [
                    ["ドローン", "どろーん", "无人机"],
                    ["変貌", "へんぼう", "改变面貌"],
                    ["生産量", "せいさんりょう", "生产量"],
                    ["標的", "ひょうてき", "目标、标的"],
                    ["損傷", "そんしょう", "损伤"]
                ]
            },
            {
                "ja": "ウクライナ政府は2026年末までに欧州各国に10カ所の輸出センターを設立する計画だ。すでに英国とドイツではウクライナ製ドローンの現地生産が始まっている。国内には450社以上のドローン関連企業が活動し、2026年中には700万機の生産を目指している。もはや中国の技術を必要とせず、独自の改良で世界市场に挑む姿勢を見せている。",
                "en": "The Ukrainian government plans to establish 10 export centers in European countries by the end of 2026. Local production of Ukrainian-made drones has already begun in the UK and Germany. More than 450 drone-related companies are operating domestically, aiming to produce 7 million units during 2026. No longer dependent on Chinese technology, Ukraine is showing a stance of challenging the global market with its own innovations.",
                "literal": "乌克兰政府计划到2026年底在欧洲各国设立10处出口中心。英国和德国已经开始本地生产乌克兰制无人机。国内有450家以上的无人机相关企业在活跃，目标在2026年内生产700万架。已无需依赖中国技术，展现出以独自改良挑战世界市场的姿态。",
                "grammar": "「〜までに」— 到…为止。例：2026年末までに（到2026年底）。\n「〜で始まる」— 在…开始。例：英国で始まっている（在英国已经开始）。\n「〜目指す」— 以…为目标。例：生産を目指している（以生产为目标）。",
                "vocab": [
                    ["輸出", "ゆしゅつ", "出口"],
                    ["現地生産", "げんちせいさん", "本地生产"],
                    ["関連企業", "かんれんきぎょう", "相关企业"],
                    ["独自", "どくじ", "独自"],
                    ["挑む", "いどむ", "挑战"]
                ]
            }
        ]
    },
    {
        "slug": "ozumo-atsumifuji-360man",
        "title": "横綱撃破で360万円 大相撲・熱海富士が懸賞60本を獲得",
        "subtitle": "大相撲名古屋場所13日目、関脇・熱海富士が横綱・豊昇龍を破り、懸賞金360万円を獲得した。",
        "paras": [
            {
                "ja": "大相撲名古屋場所13日目、関脇・熱海富士（伊勢ヶ濱）が横綱・豊昇龍（立浪）を寄り倒しで破った。この一番には規定上限の60本の懸賞旗が掲げられ、熱海富士は懸賞金360万円を獲得した。懸賞は1本7万円で、協会手数料などを差し引いた6万円が勝った力士に支払われる。60本すべてがかけられるのは異例のことだ。",
                "en": "On Day 13 of the Nagoya Grand Sumo Tournament, komusubi Atamifuji defeated yokozuna Hoshoryu by yoritaoshi. A record maximum of 60 prize flags were displayed for this bout, and Atamifuji won 3.6 million yen in prize money. Each prize is 70,000 yen, with 60,000 yen after association fees going to the winning wrestler. Having all 60 prizes offered is extremely unusual.",
                "literal": "大相扑名古屋场所第13天，关胁热海富士（伊势滨部屋）以寄倒击败了横纲丰升龙（立浪部屋）。这一场比赛悬挂了规定上限的60面悬赏旗，热海富士获得了悬赏金360万日元。悬赏每根7万日元，扣除协会手续费等后的6万日元支付给获胜力士。全部60根悬赏都被挂出是极为罕见的。",
                "grammar": "「〜で破った」— 以…方式击败。例：寄り倒しで破った（以寄倒方式击败）。\n「〜に掲げられる」— 被悬挂在…。例：懸賞旗が掲げられた（悬赏旗被挂出）。\n「〜が支払われる」— …被支付。例：力士に支払われる（被支付给力士）。",
                "vocab": [
                    ["横綱", "よこづな", "横纲（相扑最高位）"],
                    ["関脇", "せきわけ", "关胁（相扑第三位）"],
                    ["懸賞", "けんしょう", "悬赏金"],
                    ["寄り倒し", "よりたおし", "寄倒（相扑招数）"],
                    ["力士", "りきし", "相扑选手"]
                ]
            },
            {
                "ja": "ABEMAで実況を担当した清野アナウンサーも「この取組、なんと60本の懸賞がかけられています。ついに60まで来ましたよ」と驚きを見せた。SNSでは「懸賞60！！」「上限だ」「夢がある」と熱狂的な反響が相次いだ。あまりの札束の厚みに「ワイの30カ月の収入がー」などの声も寄せられた。熱海富士は14日目も勝ち、千秋楽に関脇・安青錦との対戦を迎える。",
                "en": "The ABEMA commentator Kiyono expressed surprise, saying 'This bout has 60 prizes! Finally we've reached 60!' Social media erupted with excited reactions like '60 prizes!!' and 'That's the limit!' and 'There's a dream!' The thickness of the cash bundle drew comments like 'That's 30 months of my salary!' Atamifuji also won on Day 14 and faces sekiwake Aonishiki on the final day.",
                "literal": "在ABEMA担任解说的清野播音员也惊讶地表示「这场比赛竟然挂了60根悬赏旗。终于到60了啊」。社交网络上相继出现了「悬赏60！！」「上限了」「有梦想啊」等狂热反响。因为钞票捆太厚，也有人发出「这是我30个月的收入啊」等感叹。热海富士在第14天也获胜了，将在千秋乐迎战关胁安青锦。",
                "grammar": "「〜なんと」— 竟然…（表示惊讶）。例：なんと60本（竟然60根）。\n「〜があいつぐ」— …接连不断。例：反響が相次いだ（反响接连不断）。\n「〜に迎える」— 迎接…。例：対戦を迎える（迎来对战）。",
                "vocab": [
                    ["実況", "じっきょう", "实况解说"],
                    ["取組", "とりくみ", "比赛、一场相扑"],
                    ["上限", "じょうげん", "上限"],
                    ["札束", "さつたば", "钞票捆"],
                    ["千秋楽", "せんしゅうらく", "千秋乐（最后一天）"]
                ]
            }
        ]
    },
    {
        "slug": "maeda-daizen-premier",
        "title": "前田大然がプレミアリーグへ イプスウィッチが獲得発表",
        "subtitle": "スコットランドのセルティックから日本代表FW前田大然がイングランド・プレミアリーグに昇格したイプスウィッチに移籍した。",
        "paras": [
            {
                "ja": "プレミアリーグに昇格したイプスウィッチ・タウンは25日、日本代表FWの前田大然をセルティックから獲得したと発表した。契約期間は2029年夏までの3年間。前日には守田英正のハル加入も決定しており、今季プレミアリーグのクラブに所属する日本人選手は8人となった。SNSでは「マジか！」「すごい時代だ」と歓喜の声が上がっている。",
                "en": "Ipswich Town, promoted to the Premier League, announced on the 25th that they have acquired Japan national team forward Daizen Maeda from Celtic. The contract is for 3 years until the summer of 2029. The previous day, Hidenari Morita's move to Hull was also confirmed, bringing the number of Japanese players belonging to Premier League clubs this season to 8. Social media erupted with joy, with comments like 'No way!' and 'What an amazing era!'",
                "literal": "升入英超联赛的伊普斯维奇镇25日宣布从凯尔特人引进日本代表前锋前田大然。合同期至2029年夏季，为期3年。前一天，守田英正加盟赫尔城也已确定，本赛季英超俱乐部所属的日本球员达到8人。社交网络上响起「真的吗！」「真是个了不起的时代」等欢呼声。",
                "grammar": "「〜と発表した」— 发表…。例：獲得したと発表した（发表了获得的消息）。\n「〜まで」— 到…为止。例：2029年夏まで（到2029年夏季为止）。\n「〜に所属する」— 属于…。例：クラブに所属する（属于俱乐部）。",
                "vocab": [
                    ["プレミアリーグ", "ぷれみありーぐ", "英超联赛"],
                    ["昇格", "しょうかく", "升级、升格"],
                    ["獲得", "かくとく", "获得、签下"],
                    ["契約期間", "けいやくきかん", "合同期"],
                    ["移籍", "いせき", "转会"]
                ]
            },
            {
                "ja": "前田は「鬼プレス」と呼ばれる圧倒的な運動量とスピードが持ち味で、セルティックでは公式戦通算95試合で41ゴールを記録した。SNSでは「あのスピードと運動量がプレミアでどうハマるか楽しみ」「相手DFにとって悪夢の90分になるだろう」と期待の声が多く寄せられている。前田は「プレミアリーグの舞台に立てることをとてもうれしく思います。チームの力になれるよう頑張ります」とコメントした。",
                "en": "Maeda is known for his overwhelming work rate and speed, nicknamed 'demon press.' At Celtic, he recorded 41 goals in 95 official matches. Social media was flooded with hopeful comments like 'I can't wait to see how his speed and work rate work in the Premier League' and 'It'll be a nightmare 90 minutes for opposing defenders.' Maeda commented, 'I'm very happy to be able to play on the Premier League stage. I'll do my best to contribute to the team.'",
                "literal": "前田以其被称为「鬼逼抢」的压倒性运动量和速度为特点，在凯尔特人正式比赛共95场中打进41球。社交媒体上充满期待的声音：「他的速度和运动量在英超会如何发挥作用令人期待」「对于对方后卫来说将成为噩梦般的90分钟吧」。前田表示：「非常高兴能够站在英超的舞台上。我会努力为球队贡献力量。」",
                "grammar": "「〜が持ち味」— …是特点/长处。例：運動量が持ち味（运动量是特点）。\n「〜で〜を記録」— 以…记录了…。例：95試合で41ゴール（95场比赛41个进球）。\n「〜よう頑張る」— 努力…。例：力になれるよう頑張る（努力做贡献）。",
                "vocab": [
                    ["鬼プレス", "おにぷれす", "疯狂的逼抢"],
                    ["運動量", "うんどうりょう", "运动量"],
                    ["持ち味", "もちあじ", "特点、长处"],
                    ["通算", "つうさん", "总计"],
                    ["公式戦", "こうしきせん", "正式比赛"]
                ]
            }
        ]
    },
    {
        "slug": "takaichi-shijiritsu-kokkarinen",
        "title": "混迷国会で「高市離れ」の兆候 期待と違う市民の声",
        "subtitle": "会期末を迎えた国会。内閣支持率の下落が続き、市民からは「期待と違う」との声が聞かれるようになった。",
        "paras": [
            {
                "ja": "国会は25日に会期末を迎えたが、高市政権の支持率下落が目立っている。副首都構想関連法は2票差で成立したものの、野党からは「大阪ありき」との批判が噴出した。公明党も「暮らしが先だ」と強調し、連立与党内からも不満の声が漏れる。ANNの世論調査では内閣支持率が50％を切り、政権運営に黄信号がともり始めている。",
                "en": "The Diet session ended on the 25th, but the decline in approval ratings for the Takaichi administration is becoming prominent. Although the sub-capital legislation was passed by a margin of just two votes, opposition parties erupted with criticism that it was 'Osaka-first.' Komeito also emphasized that 'people's livelihoods come first,' with dissatisfaction leaking even from within the ruling coalition. ANN's opinion poll showed the cabinet approval rating falling below 50%, signaling trouble for the administration's management.",
                "literal": "国会于25日迎来了会期末，但高市政权支持率的下降引人注目。副首都相关法案虽然以2票之差成立，但在野党却爆发出「大阪优先」的批评。公明党也强调「民生优先」，联合执政党内也传出不满声音。ANN的舆论调查显示内阁支持率跌破50%，政权运营开始亮起黄灯。",
                "grammar": "「〜ものの」— 虽然…但是…。例：成立したものの（虽然成立了）。\n「〜が噴出する」— …爆发出来。例：批判が噴出した（批评爆发了）。\n「〜を切る」— 跌破…。例：50％を切った（跌破50%）。",
                "vocab": [
                    ["会期末", "かいきまつ", "会期末"],
                    ["支持率", "しじりつ", "支持率"],
                    ["下落", "げらく", "下降"],
                    ["連立与党", "れんりつよとう", "联合执政党"],
                    ["黄信号", "きしんごう", "黄灯、警告信号"]
                ]
            },
            {
                "ja": "国会では与党議員へのアンケートでも厳しい声が目立った。日本維新の会の原山議員は「改革を先送りするような国会運営には満足できず、よりスピード感をもった決断と行動が必要だ」と指摘。一方、自民議員からも「与野党ともに拙速な審議だった」と反省の声が出ている。物価高対策や消費税減税をめぐる議論も山積しており、今後の政権運営が試されることになる。",
                "en": "In a survey of ruling party lawmakers, critical voices were prominent. Harayama, a lawmaker from Nippon Ishin, pointed out that 'I'm not satisfied with Diet management that postpones reforms; faster decisions and action are needed.' Meanwhile, even LDP lawmakers expressed regret, saying 'Both ruling and opposition parties engaged in hasty deliberations.' With discussions on price measures and consumption tax cuts piling up, the administration's future management faces a serious test.",
                "literal": "在国会对执政党议员的问卷调查中，严厉的意见也很突出。日本维新会的原山议员指出「对推迟改革的国会运营无法满意，需要更有速度感的决断和行动」。另一方面，自民党议员也发出了「朝野双方都进行了草率审议」的反省声音。围绕物价上涨对策和消费税减税的讨论堆积如山，今后的政权运营将面临考验。",
                "grammar": "「〜を先送りする」— 推迟…。例：改革を先送りする（推迟改革）。\n「〜が必要だ」— 需要…。例：決断が必要だ（需要决断）。\n「〜ことになる」— 就会…（表示结果）。例：試されることになる（就会受到考验）。",
                "vocab": [
                    ["アンケート", "あんけーと", "问卷调查"],
                    ["改革", "かいかく", "改革"],
                    ["先送り", "さきおくり", "推迟"],
                    ["拙速", "せっそく", "草率、仓促"],
                    ["山積する", "やまづみする", "堆积如山"]
                ]
            }
        ]
    },
    {
        "slug": "okamoto-kouzou-soushiki",
        "title": "レバノンで岡本公三元被告の葬儀 英雄視する声も",
        "subtitle": "日本赤軍のメンバーとして有名な岡本公三容疑者がレバノンで死亡。葬儀が執り行われ、パレスチナ人らから英雄視された。",
        "paras": [
            {
                "ja": "1972年にイスラエルの空港で銃乱射事件を起こした「日本赤軍」のメンバー、岡本公三容疑者（78）の葬儀がレバノンの首都ベイルートで執り行われた。岡本容疑者はPFLP（パレスチナ解放人民戦線）と共闘し、100人以上を死傷させた事件を起こした。長年レバノンに潜伏していたが、肺の合併症で死亡したという。",
                "en": "A funeral was held in Beirut, the capital of Lebanon, for Kozo Okamoto (78), a member of the Japanese Red Army who carried out a shooting attack at an Israeli airport in 1972. Okamoto fought alongside the PFLP (Popular Front for the Liberation of Palestine) and was involved in an incident that killed or injured over 100 people. He had been hiding in Lebanon for many years and reportedly died from lung complications.",
                "literal": "1972年在以色列机场制造枪击事件的「日本赤军」成员冈本公三嫌疑人（78岁）的葬礼在黎巴嫩首都贝鲁特举行。冈本嫌疑人与PFLP（巴勒斯坦解放人民阵线）共同战斗，制造了造成100多人死伤的事件。据称长年潜伏在黎巴嫩，因肺部并发症死亡。",
                "grammar": "「〜を起こした」— 引发了…。例：事件を起こした（引发了事件）。\n「〜と共闘する」— 与…共同战斗。例：PFLPと共闘した（与PFLP共同战斗）。\n「〜という」— 据说…。例：死亡したという（据称死亡了）。",
                "vocab": [
                    ["日本赤軍", "にほんせきぐん", "日本赤军"],
                    ["銃乱射事件", "じゅうらんしゃじけん", "枪击事件"],
                    ["葬儀", "そうぎ", "葬礼"],
                    ["潜伏", "せんぷく", "潜伏"],
                    ["合併症", "がっぺいしょう", "并发症"]
                ]
            },
            {
                "ja": "岡本容疑者はパレスチナ人の間では、イスラエルに敵対する英雄として見られてきた。葬儀には多くの関係者が集まり、PFLPの担当者は「最後まで彼は『パレスチナ』と繰り返していた。彼の意志を受け継いでいく」と述べた。一方で、日本政府はこれまで岡本容疑者の身柄引き渡しを求めてきたが、レバノン側は応じていなかった。国際テロの記憶と中東の複雑な政治情勢を改めて浮き彫りにした。",
                "en": "Okamoto was seen as a hero among Palestinians who oppose Israel. Many associates gathered at the funeral, and a PFLP representative said, 'Until the very end, he kept repeating 'Palestine.' We will carry on his will.' Meanwhile, the Japanese government had been seeking Okamoto's extradition but Lebanon had not complied. The case has once again highlighted the legacy of international terrorism and the complex political situation in the Middle East.",
                "literal": "冈本嫌疑人在巴勒斯坦人中被视为对抗以色列的英雄。许多相关人士聚集在葬礼上，PFLP负责人表示「直到最后一刻他都在重复『巴勒斯坦』。我们将继承他的意志」。另一方面，日本政府此前一直要求引渡冈本嫌疑人，但黎方未予回应。此事再次凸显了国际恐怖主义的记忆与中东复杂的政治局势。",
                "grammar": "「〜として見られる」— 被视为…。例：英雄として見られてきた（一直被视作英雄）。\n「〜を受け継ぐ」— 继承…。例：意志を受け継いでいく（继承意志）。\n「〜を求める」— 要求…。例：引き渡しを求めてきた（一直要求引渡）。",
                "vocab": [
                    ["英雄", "えいゆう", "英雄"],
                    ["敵対する", "てきたいする", "敌对"],
                    ["意志", "いし", "意志"],
                    ["身柄引き渡し", "みがらひきわたし", "引渡（嫌犯）"],
                    ["浮き彫り", "うきぼり", "凸显、突出"]
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
        print(f"   🔤 Tokenizing P{i+1}...", end=" ")
        words = tokenize_text(p['ja'])
        print(f"({len(words)} tokens)")
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
        time.sleep(0.5)

    # 4. Blog post
    ja_text = '\n\n'.join([p['ja'] for p in art['paras'][:3]])
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

# Build new JS list entries
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
        print(f"  {status} {slug:40s} | {pc} paras | {d[0]['title'][:30]}...")
        ok += 1
    else:
        print(f"  ❌ {slug} MISSING!")

print(f"\n🎉 {ok}/{len(processed)} articles processed successfully!")
print(f"{'='*60}")
