#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-07-29 (Wed) Edition — Kumamoto Earthquake Special"""
import json, os, subprocess, time, re, sys
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-07-29'
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
    r = subprocess.run(
        ['edge-tts', '--voice', 'ja-JP-NanamiNeural',
         '--text', text, '--write-media', outpath],
        capture_output=True, timeout=300)
    return os.path.exists(outpath) and os.path.getsize(outpath) > 1000

# ==================================================================
# TODAY'S ARTICLES — 2026-07-29
# Top news: Kumamoto M7.1 earthquake strikes, BYD launches EV in Japan
# ==================================================================
articles = [
    # 1 — MAIN: Kumamoto M7.1 earthquake
    {
        "slug": "kumamoto-m71-shindo7",
        "title": "熊本県で最大震度7 M7.1の地震 広範囲で被害",
        "subtitle": "28日午後、熊本県で最大震度7の強い地震が発生。イオンモール熊本で爆発、日本製紙八代工場で複数が閉じ込められるなど広範囲で被害が出ている。",
        "paras": [
            {
                "ja": "28日午後4時27分ごろ、熊本県で最大震度7を観測する強い地震がありました。気象庁によりますと、震源地は熊本県熊本地方で、震源の深さはおよそ2キロと推定されています。地震の規模を示すマグニチュードは7.1と推定され、気象庁はこの地震を「令和8年熊本地震」と命名しました。",
                "en": "At around 4:27 PM on the 28th, a strong earthquake with a maximum seismic intensity of 7 was observed in Kumamoto Prefecture. According to the Japan Meteorological Agency, the epicenter was in the Kumamoto region of Kumamoto Prefecture, with the depth estimated at approximately 2 km. The magnitude of the earthquake is estimated at 7.1, and the JMA named it the 'Reiwa 8 Kumamoto Earthquake.'",
                "literal": "28日下午4点27分左右，熊本县观测到了最大震度7的强烈地震。据气象厅称，震源位于熊本县熊本地方，震源深度约2公里。地震规模为里氏7.1级，气象厅将此地震命名为「令和8年熊本地震」。",
                "grammar": "「〜ごろ」— 大约…时候。例：4時27分ごろ（大约4点27分）。\n「〜によりますと」— 据…（报道/说明）。例：気象庁によりますと（据气象厅称）。\n「〜と命名しました」— 命名为…。例：「令和8年熊本地震」と命名しました（命名为「令和8年熊本地震」）。",
                "vocab": [
                    ["最大震度7", "さいだいしんどなな", "最大震度7"],
                    ["震源地", "しんげんち", "震源地"],
                    ["推定", "すいてい", "推测、估算"],
                    ["マグニチュード", "まぐにちゅーど", "里氏震级"],
                    ["命名", "めいめい", "命名"]
                ]
            },
            {
                "ja": "この地震で、熊本県嘉島町のイオンモール熊本で駐車場の天井が崩落し、2人が死亡、1人が心肺停止の重体となっています。また日本製紙八代工場では、倒壊した建物に複数の従業員が閉じ込められ、2人が心肺停止、9人が安否不明となっています。宇城市や氷川町では多くの住宅が全壊し、地震の揺れでけがをした人が相次いで病院に運ばれました。",
                "en": "In this earthquake, the ceiling of a parking lot collapsed at Aeon Mall Kumamoto in Kashima Town, Kumamoto Prefecture, killing two people and leaving one in cardiopulmonary arrest. At the Nippon Paper Yatsushiro plant, multiple employees were trapped in a collapsed building, with two in cardiopulmonary arrest and nine unaccounted for. In Uki City and Hikawa Town, many houses were completely destroyed, and people injured by the earthquake tremors were successively transported to hospitals.",
                "literal": "在此次地震中，熊本县嘉岛町的永旺梦乐城熊本店停车场天花板坍塌，造成2人死亡、1人心肺停止重伤。此外，日本制纸八代工厂倒塌的建筑内有数名员工被困，2人心肺停止，9人安危不明。宇城市和冰川町许多住宅全毁，因地震摇晃受伤的人相继被送往医院。",
                "grammar": "「〜で」— 在…（地点）/ 因…。例：この地震で（在此次地震中）。\n「〜となっています」— 处于…状态。例：安否不明となっています（处于安危不明的状态）。\n「〜に運ばれました」— 被送往…。例：病院に運ばれました（被送往医院）。",
                "vocab": [
                    ["崩落", "ほうらく", "坍塌、崩落"],
                    ["天井", "てんじょう", "天花板"],
                    ["閉じ込める", "とじこめる", "关在里面、困住"],
                    ["従業員", "じゅうぎょういん", "员工"],
                    ["全壊", "ぜんかい", "全毁（完全倒塌）"]
                ]
            },
            {
                "ja": "気象庁は今後1週間程度、特に今後2〜3日の間は最大震度7程度の地震に注意するよう呼びかけています。また熊本県内では今後も最高気温35度以上の猛暑日が続き、夜も最低気温が25度を下回らない熱帯夜が続く予報で、避難生活中の熱中症にも十分注意するよう呼びかけています。政府はプッシュ型支援を展開し、自衛隊を派遣して情報収集と救助活動を行っています。",
                "en": "The Japan Meteorological Agency is calling for caution regarding earthquakes of up to seismic intensity 7 for about the next week, particularly the next 2-3 days. Additionally, within Kumamoto Prefecture, extreme heat days with maximum temperatures of 35°C or higher are forecast to continue, and tropical nights where minimum temperatures do not fall below 25°C are also expected, so the agency is urging sufficient caution against heatstroke during evacuation life. The government is deploying push-type support and dispatching Self-Defense Forces for information gathering and rescue operations.",
                "literal": "气象厅呼吁今后一周左右，特别是今后2-3天内注意最大震度7级左右的地震。此外，熊本县内预计今后最高气温35度以上的酷暑日将持续，夜间最低气温不低于25度的热带夜也将持续，呼吁避难生活中也要充分注意中暑。政府正在展开推送式支援，派遣自卫队进行信息收集和救助活动。",
                "grammar": "「〜よう呼びかけています」— 呼吁…。例：注意するよう呼びかけています（呼吁注意）。\n「〜予報で」— 预报显示…。例：続く予報で（预报将持续）。\n「〜ています」— 正在…。例：行っています（正在进行）。",
                "vocab": [
                    ["呼びかける", "よびかける", "呼吁、号召"],
                    ["猛暑日", "もうしょび", "酷暑日（35度以上）"],
                    ["熱帯夜", "ねったいや", "热带夜（夜间25度以上）"],
                    ["熱中症", "ねっちゅうしょう", "中暑"],
                    ["自衛隊", "じえいたい", "自卫队"]
                ]
            }
        ]
    },
    # 2 — Gov't response to earthquake
    {
        "slug": "kumamoto-seihu-zien",
        "title": "高市首相「人命第一で対応」 政府が被災地支援を急ぐ",
        "subtitle": "熊本県での地震を受け、政府は被害状況の把握と被災者の救助・支援を急ぐ。首相はプッシュ型支援を指示した。",
        "paras": [
            {
                "ja": "熊本県を震源とする地震の発生を受け、政府は被害状況の把握と被災者の救助・支援を急ぐ構えだ。高市首相は28日、「人命第一で全力を挙げて対応する」と述べ、関係省庁に対してプッシュ型支援を展開するよう指示した。首相官邸の危機管理センターには情報連絡室が設置され、被害情報の収集が進められている。",
                "en": "Following the earthquake centered in Kumamoto Prefecture, the government is moving quickly to grasp the damage situation and rescue and support victims. Prime Minister Takaichi stated on the 28th, 'We will respond with all our strength, putting human life first,' and instructed relevant ministries to deploy push-type support. An information liaison office was established at the Crisis Management Center of the Prime Minister's Office, and damage information is being collected.",
                "literal": "受熊本县为震源的地震发生，政府正在加紧掌握受灾情况和救助支援受灾者。高市首相28日表示「将把人命放在第一位全力应对」，指示相关省厅展开推送式支援。首相官邸危机管理中心设置了信息联络室，正在推进受灾信息的收集。",
                "grammar": "「〜を受け」— 受…、根据…。例：発生を受け（受发生影响）。\n「〜構えだ」— 姿态、准备做…。例：急ぐ構えだ（准备加紧）。\n「〜よう指示した」— 指示…。例：展開するよう指示した（指示展开）。",
                "vocab": [
                    ["震源", "しんげん", "震源"],
                    ["被災者", "ひさいしゃ", "受灾者"],
                    ["人命", "じんめい", "人命"],
                    ["関係省庁", "かんけいしょうちょう", "相关省厅"],
                    ["危機管理センター", "ききかんりせんたー", "危机管理中心"]
                ]
            },
            {
                "ja": "小泉防衛相は防衛省内で記者団の取材に応じ、自衛隊のF2戦闘機やヘリコプターを出動させて情報収集を行っているほか、熊本、福岡、長崎、佐賀の各県庁に連絡官を派遣したと発表した。政府は今後、被害の拡大状況に応じて、さらなる人員や物資の支援を検討する方針だ。また、東京電力や九州電力など電力各社は、被災地への電力供給の安定化に向けて対応を進めている。",
                "en": "Defense Minister Koizumi told reporters at the Defense Ministry that in addition to dispatching F2 fighter jets and helicopters from the Self-Defense Forces for information gathering, liaison officers have been sent to the prefectural offices of Kumamoto, Fukuoka, Nagasaki, and Saga. The government plans to consider further personnel and material support depending on the extent of the damage. Additionally, power companies including TEPCO and Kyushu Electric Power are working to stabilize electricity supply to the affected areas.",
                "literal": "小泉防卫相在防卫省内接受了记者团的采访，宣布除了出动自卫队F2战斗机和直升机进行信息收集外，还向熊本、福冈、长崎、佐贺各县厅派遣了联络官。政府今后将根据受灾扩大状况，研究进一步的人员和物资支援。此外，东京电力和九州电力等各电力公司正在推进受灾地区电力供应的稳定化。",
                "grammar": "「〜に応じ」— 根据…。例：取材に応じ（接受采访）。\n「〜ほか」— 除了…之外。例：行っているほか（除了正在做…之外）。\n「〜に応じて」— 根据…。例：状況に応じて（根据情况）。",
                "vocab": [
                    ["防衛相", "ぼうえいしょう", "防卫大臣"],
                    ["出動", "しゅつどう", "出动"],
                    ["連絡官", "れんらくかん", "联络官"],
                    ["派遣", "はけん", "派遣"],
                    ["物資", "ぶっし", "物资"]
                ]
            }
        ]
    },
    # 3 — Kumamoto heat + earthquake warning
    {
        "slug": "kumamoto-kisyatu-rikisya",
        "title": "熊本で震度7の地震 熱中症にも警戒を",
        "subtitle": "熊本県で震度7の地震が発生。猛暑日と熱帯夜が続く中、避難生活での熱中症対策も急務に。",
        "paras": [
            {
                "ja": "昨日28日午後、熊本県熊本地方を震源とする地震が発生し、宇城市や氷川町で最大震度7を観測しました。今日29日の宇城市は最高気温が33℃前後まで上がる見込みで、避難生活を送る人々は厳しい暑さとの闘いを強いられています。気象庁は被災地では熱中症のリスクが非常に高まっているとして、こまめな水分補給や休憩を呼びかけています。",
                "en": "Yesterday afternoon, an earthquake centered in the Kumamoto region of Kumamoto Prefecture occurred, with a maximum seismic intensity of 7 observed in Uki City and Hikawa Town. Today, the 29th, Uki City is expected to see temperatures rise to around 33°C, forcing evacuees to battle severe heat. The Japan Meteorological Agency warns that the risk of heatstroke is extremely high in the disaster area and is urging frequent hydration and rest.",
                "literal": "昨天28日下午，熊本县熊本地方为震源的地震发生，宇城市和冰川町观测到了最大震度7。今天29日宇城市最高气温预计将升至33℃左右，过着避难生活的人们被迫与酷暑作斗争。气象厅称受灾地区中暑风险非常高，呼吁及时补充水分和休息。",
                "grammar": "「〜見込み」— 预计…。例：上がる見込み（预计上升）。\n「〜を強いられる」— 被迫…。例：闘いを強いられています（被迫进行斗争）。\n「〜として」— 作为…。例：高まっているとして（作为正在升高…）。",
                "vocab": [
                    ["観測", "かんそく", "观测"],
                    ["避難生活", "ひなんせいかつ", "避难生活"],
                    ["厳しい", "きびしい", "严酷、严峻"],
                    ["リスク", "りすく", "风险"],
                    ["水分補給", "すいぶんほきゅう", "补充水分"]
                ]
            },
            {
                "ja": "気象庁は今後1週間程度は同程度の地震に注意が必要だと警告しています。熊本県内では引き続き猛暑が続くため、避難所での熱中症対策が急務となっています。自治体はエアコンの効いた避難所の確保や、冷却グッズの配布などの対策を進めています。専門家は「地震の揺れによる恐怖と暑さによるストレスが重なり、体調を崩す人が増える恐れがある」と指摘しています。",
                "en": "The JMA warns that caution is needed for similar-level earthquakes for about the next week. As extreme heat continues within Kumamoto Prefecture, heatstroke countermeasures at evacuation centers have become an urgent task. Local governments are advancing measures such as securing air-conditioned evacuation centers and distributing cooling supplies. Experts point out that 'the fear from earthquake tremors combined with the stress from the heat may increase the number of people falling ill.'",
                "literal": "气象厅警告今后一周左右需要注意同等程度的地震。熊本县内酷暑持续，避难所的中暑对策成为紧急任务。地方政府正在推进确保有空调的避难所和发放冷却用品等措施。专家指出「地震摇晃带来的恐惧和暑热导致的压力叠加，可能有更多人身体状况变差」。",
                "grammar": "「〜必要がある」— 有必要…。例：注意が必要だ（有必要注意）。\n「〜となっています」— 成为…。例：急務となっています（成为紧急任务）。\n「〜恐れがある」— 有…的危险。例：増える恐れがある（有增加的危险）。",
                "vocab": [
                    ["警告", "けいこく", "警告"],
                    ["引き続き", "ひきつづき", "继续、持续"],
                    ["急務", "きゅうむ", "紧急任务"],
                    ["自治体", "じちたい", "地方政府、自治体"],
                    ["体調を崩す", "たいちょうをくずす", "身体不适、搞坏身体"]
                ]
            }
        ]
    },
    # 4 — BYD EV in Japan
    {
        "slug": "byd-karukei-ev",
        "title": "中国BYDが日本で軽EV「ラッコ」 実質100万円台",
        "subtitle": "世界最大のEVメーカー中国BYDが日本市場攻略の切り札となる軽EVを投入。軽自動車市場に新たな競争が始まる。",
        "paras": [
            {
                "ja": "世界最大のEVメーカー、中国BYDが日本市場攻略の切り札となる軽EV「RACCO（ラッコ）」を、国の補助金適用後で100万円台の実質価格で投入することがわかりました。ラッコは全長3395mmと軽自動車規格に合わせたコンパクトなボディで、航続距離は200キロ以上を想定。2027年にも発売される見通しです。",
                "en": "China's BYD, the world's largest EV manufacturer, is set to launch a light EV called 'RACCO' in the Japanese market as a trump card, with an effective price in the 1 million yen range after national subsidies. The RACCO has a compact body at 3,395mm in total length, conforming to light vehicle standards, with an expected driving range of over 200 km. It is expected to go on sale in 2027.",
                "literal": "世界最大EV制造商中国BYD将投入攻占日本市场的王牌轻EV「RACCO（海獭）」，在适用国家补助金后实际价格为100万日元左右。RACCO全长3395mm，符合轻汽车规格的紧凑车身，续航距离预计200公里以上。预计2027年发售。",
                "grammar": "「〜となる」— 成为…。例：切り札となる（成为王牌）。\n「〜見通し」— 预计、展望。例：発売される見通しです（预计发售）。\n「〜で」— 以…（价格/状态）。例：100万円台で（以100万日元区间）。",
                "vocab": [
                    ["軽EV", "けいイーヴィー", "轻型电动车"],
                    ["補助金", "ほじょきん", "补助金、补贴"],
                    ["航続距離", "こうぞくきょり", "续航距离"],
                    ["発売", "はつばい", "发售、上市"],
                    ["市場", "しじょう", "市场"]
                ]
            },
            {
                "ja": "BYDは既に日本で中型EV「ATTO3」や「ドルフィン」「シール」などを販売していますが、日本の軽自動車市場は国内メーカーの牙城となっていました。軽自動車は日本の独自規格で、税制面や車庫証明などの優遇措置があり、多くの日本人に親しまれています。BYDがこの分野に本格参入すれば、日本の自動車メーカーにとっては大きな脅威となると専門家はみています。",
                "en": "BYD already sells mid-size EVs such as the 'ATTO3,' 'Dolphin,' and 'Seal' in Japan, but Japan's light vehicle market had been a stronghold of domestic manufacturers. Light vehicles are a unique Japanese standard with tax benefits and garage certificate exemptions, and are popular among many Japanese. Experts believe that if BYD makes a full-scale entry into this segment, it will pose a major threat to Japanese automakers.",
                "literal": "BYD虽已在日本销售中型EV「ATTO3」「海豚」「海豹」等，但日本轻汽车市场一直是国内制造商的堡垒。轻汽车是日本独特规格，享有税制和车库证明等方面的优惠措施，深受许多日本人喜爱。专家认为BYD如果正式进入这个领域，对日本汽车制造商来说将是巨大威胁。",
                "grammar": "「〜となっていました」— 成为了…。例：牙城となっていました（成为了堡垒/地盘）。\n「〜で」— 以…。例：税制面で（在税制方面）。\n「〜とみています」— 认为、预计。例：脅威となるとみています（认为是威胁）。",
                "vocab": [
                    ["中型", "ちゅうがた", "中型"],
                    ["牙城", "がじょう", "堡垒、根据地"],
                    ["独自規格", "どくじきかく", "独特规格"],
                    ["優遇措置", "ゆうぐうそち", "优待措施"],
                    ["脅威", "きょうい", "威胁"]
                ]
            }
        ]
    },
    # 5 — US walks out at UN
    {
        "slug": "kokuren-futsu-hatugen-taiseki",
        "title": "国連安保理で仏発言中に米代表団が退席",
        "subtitle": "国連安全保障理事会でウクライナ問題を議論中、フランスの発言中に米国代表団が退席。人権高等弁務官の任期延長を巡り対立。",
        "paras": [
            {
                "ja": "27日の国連安全保障理事会でウクライナ問題を議論する会合で、フランスが発言する際に米国代表団が退席しました。トゥルク国連人権高等弁務官の任期延長を巡り対立が激化したことが原因です。米国はこれまでも国連人権理事会から脱退するなど、国連関連組織との関係が悪化していました。",
                "en": "At a UN Security Council meeting on the 27th discussing the Ukraine issue, the US delegation walked out as France was speaking. This was due to intensifying conflict over the extension of the term of UN High Commissioner for Human Rights Turk. The US has previously withdrawn from the UN Human Rights Council and other UN-related organizations, deteriorating its relationship with them.",
                "literal": "在27日联合国安理会讨论乌克兰问题的会议上，法国发言时美国代表团退席。原因是围绕联合国人权事务高级专员图尔克的任期延长问题对立激化。美国此前也曾退出联合国人权理事会等，与联合国相关组织的关系已经恶化。",
                "grammar": "「〜際に」— 在…的时候。例：発言する際に（在发言的时候）。\n「〜を巡り」— 围绕…。例：任期延長を巡り（围绕任期延长）。\n「〜ていました」— 已经…了。例：悪化していました（已经恶化了）。",
                "vocab": [
                    ["安全保障理事会", "あんぜんほしょうりじかい", "安全理事会"],
                    ["代表団", "だいひょうだん", "代表团"],
                    ["退席", "たいせき", "退席"],
                    ["人権高等弁務官", "じんけんこうとうべんむかん", "人权事务高级专员"],
                    ["任期延長", "にんきえんちょう", "任期延长"]
                ]
            },
            {
                "ja": "米国の退席について、国連事務総長副報道官はコメントを控えたものの、「国連としては全加盟国が総会を通じて下された決定を尊重することを期待している」と述べました。外交専門家は、米国のこうした行動が国際社会における孤立を深める可能性を指摘しています。一方、フランス政府は「対話を通じた解決が重要だ」との立場を改めて強調しました。",
                "en": "Regarding the US walkout, the UN Deputy Spokesperson refrained from commenting but stated, 'The UN expects all member states to respect decisions made through the General Assembly.' Diplomatic experts point out that such US actions could deepen its isolation in the international community. Meanwhile, the French government reiterated its position that 'resolution through dialogue is important.'",
                "literal": "关于美国退席，联合国副秘书长发言人虽然避免评论，但表示「联合国期待全体成员国尊重通过大会做出的决定」。外交专家指出，美国的此类行为可能会加深在国际社会的孤立。另一方面，法国政府再次强调了「通过对话解决很重要」的立场。",
                "grammar": "「〜ものの」— 虽然…但是…。例：コメントを控えたものの（虽然避免评论）。\n「〜を通じて」— 通过…。例：総会を通じて（通过大会）。\n「〜可能性を指摘する」— 指出…的可能性。例：孤立を深める可能性を指摘しています（指出加深孤立的可能性）。",
                "vocab": [
                    ["退席", "たいせき", "退席"],
                    ["コメントを控える", "こめんとをひかえる", "避免评论"],
                    ["加盟国", "かめいこく", "成员国"],
                    ["孤立", "こりつ", "孤立"],
                    ["対話", "たいわ", "对话"]
                ]
            }
        ]
    },
    # 6 — Higashino Keigo colon cancer
    {
        "slug": "higashino-keigo-daichogan",
        "title": "作家・東野圭吾さん 大腸がんのため死去 68歳",
        "subtitle": "「容疑者Xの献身」などで知られる作家の東野圭吾さんが、大腸がんのため亡くなった。初期症状について医師が解説。",
        "paras": [
            {
                "ja": "「容疑者Xの献身」などで知られる人気作家の東野圭吾さんが、7月23日に大腸がんのため亡くなったことが報じられました。68歳でした。東野さんは1985年に「放課後」で江戸川乱歩賞を受賞してデビュー。その後「白夜行」「流星の絆」「ナミヤ雑貨店の奇蹟」など数々のベストセラーを生み出し、多くの作品が映画やドラマ化されました。",
                "en": "It has been reported that popular author Keigo Higashino, known for 'The Devotion of Suspect X' and other works, passed away on July 23 due to colon cancer. He was 68 years old. Higashino debuted in 1985 by winning the Edogawa Rampo Prize for 'Houkago (After School).' He subsequently produced numerous bestsellers including 'Byakuyako (Journey Under the Midnight Sun),' 'Ryusei no Kizuna (The Bonds of the Shooting Stars),' and 'The Miracles of the Namiya General Store,' with many of his works adapted into films and dramas.",
                "literal": "以「嫌疑人X的献身」等闻名的作家东野圭吾于7月23日因大肠癌去世的消息被报道。享年68岁。东野1985年以「放学后」获得江户川乱步奖出道。之后创作了「白夜行」「流星之绊」「浪矢杂货店的奇迹」等众多畅销书，许多作品被改编成电影和电视剧。",
                "grammar": "「〜ことで知られる」— 以…而闻名。例：献身で知られる（以献身而闻名）。\n「〜たことが報じられた」— 据报道…。例：亡くなったことが報じられました（据报道去世）。\n「〜化される」— 被…化。例：映画化されました（被改编成电影）。",
                "vocab": [
                    ["大腸がん", "だいちょうがん", "大肠癌"],
                    ["作家", "さっか", "作家"],
                    ["デビュー", "でびゅー", "出道"],
                    ["ベストセラー", "べすとせらー", "畅销书"],
                    ["映画化", "えいがか", "改编成电影"]
                ]
            },
            {
                "ja": "医師によると、大腸がんの初期症状としては血便や腹痛、便秘と下痢の繰り返しなどがあるといいます。しかし初期には自覚症状がほとんどないため、早期発見には定期的な検診が重要です。特に50歳以上の人はリスクが高まるため、自治体が行う検診を積極的に受けることが推奨されています。東野さんの死去を受け、多くのファンや関係者から追悼の声が寄せられています。",
                "en": "According to doctors, early symptoms of colon cancer include blood in the stool, abdominal pain, and alternating constipation and diarrhea. However, because there are almost no noticeable symptoms in the early stages, regular checkups are important for early detection. In particular, people aged 50 and over are at higher risk, so it is recommended that they actively participate in screening provided by local governments. Following Higashino's death, many fans and相关人员have offered condolences.",
                "literal": "据医生称，大肠癌的初期症状有便血、腹痛、便秘和腹泻反复等。但由于初期几乎没有自觉症状，定期检查对早期发现非常重要。特别是50岁以上的人风险增高，建议积极接受地方政府实施的检查。东野去世后，许多粉丝和相关人士纷纷表达了哀悼。",
                "grammar": "「〜によると」— 据…。例：医師によると（据医生称）。\n「〜ため」— 因为/为了。例：自覚症状がないため（因为没有自觉症状）。\n「〜ことが推奨されています」— 被推荐做…。例：受けることが推奨されています（被推荐接受）。",
                "vocab": [
                    ["症状", "しょうじょう", "症状"],
                    ["血便", "けつべん/けつべん", "便血"],
                    ["早期発見", "そうきはっけん", "早期发现"],
                    ["検診", "けんしん", "检查、体检"],
                    ["追悼", "ついとう", "追悼、哀悼"]
                ]
            }
        ]
    },
    # 7 — World extreme weather
    {
        "slug": "sekai-ijou-kishou",
        "title": "欧州で史上最悪の山火事 世界で異常気象が続出",
        "subtitle": "欧州の山火事、中国のハイペース台風、各地で深刻な異常気象が発生。気候変動の影響が懸念される。",
        "paras": [
            {
                "ja": "欧州で史上最悪の山火事が発生し、中国ではハイペースで台風が上陸するなど、世界中で異常気象が続出しています。27日も日本各地でゲリラ雷雨が発生し、大分県日田では九州で初めて40℃以上の酷暑日を観測しました。欧州では熱波による山火事がギリシャやフランスなどで猛威を振るい、消防士が足りず住民が消火活動に加わる事態となっています。",
                "en": "The worst wildfires in history are occurring in Europe, and typhoons are making landfall at a record pace in China, with extreme weather events erupting around the world. On the 27th, guerrilla thunderstorms occurred in various parts of Japan, and Hita City in Oita Prefecture observed temperatures exceeding 40°C for the first time in Kyushu. In Europe, wildfires due to heatwaves are raging in Greece and France, with situations where firefighters are insufficient and residents are joining firefighting efforts.",
                "literal": "欧洲发生史上最严重的山火，中国台风以高频率登陆，世界各地异常天气接连出现。27日日本各地也发生了局部雷雨，大分县日田观测到了九州首次40度以上的酷暑日。欧洲因热浪引发的山火在希腊和法国等地肆虐，出现了消防员不足、居民参与灭火活动的事态。",
                "grammar": "「〜で」— 在…（区域）。例：九州で（在九州）。\n「〜初めて」— 首次。例：初めて40℃以上（首次40度以上）。\n「〜事態となっています」— 成为…的状况。例：事態となっています（成为…的状况）。",
                "vocab": [
                    ["異常気象", "いじょうきしょう", "异常天气"],
                    ["山火事", "やまかじ", "山火"],
                    ["熱波", "ねっぱ", "热浪"],
                    ["猛威を振るう", "もういをふるう", "肆虐、猛烈发作"],
                    ["消火活動", "しょうかかつどう", "灭火活动"]
                ]
            },
            {
                "ja": "気候変動の影響で、こうした異常気象が世界的に増加しています。専門家は「地球温暖化により大気中のエネルギーが増え、気象現象が極端化している」と指摘します。台風12号に続き、南シナ海では新たな熱帯低気圧が発生し台風に発達する見込み。各国は気候変動対策の加速を迫られており、今後の国際的な協力が鍵を握るとみられています。",
                "en": "Due to the effects of climate change, such extreme weather events are increasing globally. Experts point out that 'global warming is increasing energy in the atmosphere, making weather phenomena more extreme.' Following Typhoon No. 12, a new tropical depression has formed in the South China Sea and is expected to develop into a typhoon. Countries are being pressed to accelerate climate change countermeasures, and future international cooperation is seen as the key.",
                "literal": "受气候变化影响，此类异常天气在全球范围内增加。专家指出「全球变暖增加了大气中的能量，气象现象趋向极端化」。继台风12号之后，南中国海出现了新的热带低气压，预计将发展成台风。各国被迫加速气候变化对策，今后的国际合作被视为关键。",
                "grammar": "「〜により」— 由于…。例：地球温暖化により（由于全球变暖）。\n「〜ている」— 正在/持续…。例：極端化している（正在极端化）。\n「〜とみられています」— 被认为是…。例：鍵を握るとみられています（被认为是掌握关键）。",
                "vocab": [
                    ["気候変動", "きこうへんどう", "气候变化"],
                    ["地球温暖化", "ちきゅうおんだんか", "全球变暖"],
                    ["大気", "たいき", "大气"],
                    ["極端化", "きょくたんか", "极端化"],
                    ["熱帯低気圧", "ねったいていきあつ", "热带低气压"]
                ]
            }
        ]
    },
    # 8 — Summer sleep tips
    {
        "slug": "natsu-kaisoku-nouhizyou",
        "title": "夏の快眠 専門家がすすめ「脳を冷やす」方法",
        "subtitle": "暑くて寝苦しい夏の夜。専門家がすすめる「脳を冷やす」快眠方法や、冷えすぎ対策グッズを紹介。",
        "paras": [
            {
                "ja": "暑くて寝苦しい夏の夜が続いています。冷えすぎて起きてしまうという悩みを解決するアイテムも続々登場しています。専門家がすすめるのは「脳を冷やす」快眠方法です。脳の温度を下げることで深い眠りに入りやすくなり、睡眠の質が向上するといいます。具体的には、首元を冷やす保冷枕や冷却シートの使用が効果的だとされています。",
                "en": "Hot, sleepless summer nights continue. Items that solve the problem of waking up due to being too cold are also appearing one after another. What experts recommend is a method of 'cooling the brain' for better sleep. By lowering the temperature of the brain, it becomes easier to enter deep sleep, improving sleep quality. Specifically, the use of cooling pillows that cool the neck area and cooling sheets is said to be effective.",
                "literal": "炎热难眠的夏夜持续着。解决因过冷而醒来的烦恼的商品也纷纷登场。专家推荐的是「冷却大脑」的安眠方法。据说通过降低大脑温度更容易进入深度睡眠，提高睡眠质量。具体来说，使用冷却脖颈部位的保冷枕和冷却贴片被认为是有效的。",
                "grammar": "「〜やすい」— 容易…。例：入りやすくなる（变得容易进入）。\n「〜といいます」— 据说…。例：向上するといいます（据说会提高）。\n「〜とされています」— 被认为是…。例：効果的だとされています（被认为是有效的）。",
                "vocab": [
                    ["快眠", "かいみん", "安眠、舒适睡眠"],
                    ["寝苦しい", "ねぐるしい", "难以入睡的"],
                    ["脳", "のう", "大脑"],
                    ["保冷", "ほれい", "保冷、冷却"],
                    ["睡眠の質", "すいみんのしつ", "睡眠质量"]
                ]
            },
            {
                "ja": "また、エアコンのつけっぱなしによる「寝冷え問題」を解決するグッズも注目されています。「ひんやり×あったか」ブランケットは、表と裏で素材が違い、冷房が強いときに寒い面を上にするとひんやり、寒いときはあったかい面で調節できる便利なアイテムです。専門家は「寝室の温度は26〜28度に設定し、足元を冷やさないことが快眠のコツです」とアドバイスしています。",
                "en": "Additionally, items that solve the 'sleep chills problem' caused by leaving the air conditioner on are also attracting attention. The 'cool x warm' blanket has different materials on the front and back, a convenient item that feels cool when you put the cold side up when the AC is strong, or can be adjusted with the warm side when you're cold. Experts advise, 'Setting the bedroom temperature to 26-28°C and not letting your feet get cold is the key to good sleep.'",
                "literal": "此外，解决空调一直开导致的「睡觉过冷问题」的商品也备受关注。「凉爽×温暖」毯子正反面材质不同，空调强时把冷面朝上就凉爽，冷的时候用暖和的一面调节，是方便的用品。专家建议「将卧室温度设定在26-28度，不让脚部受凉是舒适睡眠的秘诀」。",
                "grammar": "「〜による」— 由…引起的。例：つけっぱなしによる（由一直开着引起的）。\n「〜と」— 如果…就…。例：調節できると（如果能调节就）。\n「〜ことです」— 就是做…。例：コツです（诀窍就是…）。",
                "vocab": [
                    ["エアコン", "えあこん", "空调"],
                    ["寝冷え", "ねびえ", "睡觉着凉"],
                    ["ブランケット", "ぶらんけっと", "毯子"],
                    ["素材", "そざい", "材质"],
                    ["寝室", "しんしつ", "卧室"]
                ]
            }
        ]
    },
    # 9 — Kids SNS age restrictions
    {
        "slug": "kodomo-sns-nenrei-seigen",
        "title": "子どものSNS利用に一律年齢制限 政府が検討へ",
        "subtitle": "こども家庭庁がSNSの一律年齢制限を検討。オーストラリアやEUなど海外の動きも加速。",
        "paras": [
            {
                "ja": "こども家庭庁は、SNSなどを利用する子どもの保護策を巡り、利用者の一律の年齢制限について検討する方針を固めました。30日の有識者会議で示される中間報告書案に方針が盛り込まれる見込みです。SNSによるいじめや犯罪被害、依存症などから子どもを守るための対策が急務となっています。",
                "en": "The Children and Families Agency has decided to consider uniform age restrictions for users regarding measures to protect children using SNS and other services. The policy is expected to be included in a draft interim report to be presented at an expert meeting on the 30th. Measures to protect children from bullying, crime victimization, and addiction caused by SNS have become an urgent task.",
                "literal": "儿童家庭厅围绕保护使用SNS等的儿童的措施，计划讨论用户统一年龄限制的方针。预计方针将被纳入30日专家会议将公布的中期报告草案中。保护儿童免受SNS欺凌、犯罪受害和依赖症等问题的对策已成为紧急任务。",
                "grammar": "「〜を巡り」— 围绕…。例：保護策を巡り（围绕保护措施）。\n「〜方針を固めました」— 确定了方针。例：検討する方針を固めました（确定了讨论的方针）。\n「〜見込みです」— 预计…。例：盛り込まれる見込みです（预计将被纳入）。",
                "vocab": [
                    ["年齢制限", "ねんれいせいげん", "年龄限制"],
                    ["こども家庭庁", "こどもかていちょう", "儿童家庭厅"],
                    ["保護策", "ほごさく", "保护措施"],
                    ["いじめ", "いじめ", "欺凌"],
                    ["依存症", "いぞんしょう", "依赖症、成瘾"]
                ]
            },
            {
                "ja": "海外では子どものSNS利用を制限する動きが加速しています。オーストラリアは2024年12月に16歳未満のSNS利用を一律禁止。EUも7月13日に13歳未満の利用を制限する方針を明らかにしています。一方で、表現の自由やプライバシーの観点から、一律規制に慎重な意見もあります。政府は海外の事例も参考にしながら、バランスの取れた規制を目指すとしています。",
                "en": "Overseas, moves to restrict children's SNS use are accelerating. Australia uniformly banned SNS use by those under 16 in December 2024. The EU also announced a policy to restrict use by those under 13 on July 13. On the other hand, there are cautious opinions about uniform regulation from the perspectives of freedom of expression and privacy. The government says it aims for balanced regulation while also referencing overseas cases.",
                "literal": "海外限制儿童使用SNS的动向正在加速。澳大利亚于2024年12月全面禁止未满16岁使用SNS。欧盟也于7月13日明确了限制13岁以下使用的方针。另一方面，从表达自由和隐私角度出发，也有人对统一限制持谨慎态度。政府表示将参考海外案例，寻求平衡的监管。",
                "grammar": "「〜未満」— 未满…。例：16歳未満（未满16岁）。\n「〜一方で」— 另一方面…。例：一方で（另一方面）。\n「〜ながら」— 一边…一边…。例：参考にしながら（一边参考）。",
                "vocab": [
                    ["一律", "いちりつ", "一律、统一"],
                    ["禁止", "きんし", "禁止"],
                    ["表現の自由", "ひょうげんのじゆう", "表达自由"],
                    ["プライバシー", "ぷらいばしー", "隐私"],
                    ["規制", "きせい", "管制、规定"]
                ]
            }
        ]
    },
    # 10 — US president Iran threat
    {
        "slug": "m-kunren-tairan-kougeki",
        "title": "米大統領 イランと友好的協議続けるも決裂なら攻撃も",
        "subtitle": "トランプ米大統領がイランとの協議状況を説明。交渉決裂時には本格的な軍事攻撃を示唆。中東情勢が緊迫化。",
        "paras": [
            {
                "ja": "トランプ米大統領は27日、イランと「非常に友好的な協議」が進められていると主張し、対イラン攻撃を当面控える姿勢を改めて示しました。一方で、交渉が決裂すれば本格的な軍事作戦に踏み切る考えも示唆しています。イランは核開発を続けており、国際社会の懸念が高まっています。",
                "en": "US President Trump on the 27th claimed that 'very friendly talks' were proceeding with Iran, and once again showed a posture of refraining from attacking Iran for the time being. On the other hand, he also suggested that if negotiations break down, he would proceed with full-scale military operations. Iran continues its nuclear development, raising international concern.",
                "literal": "美国总统特朗普27日声称与伊朗正在进行「非常友好的协商」，再次展现出暂时避免对伊攻击的姿态。另一方面，他也暗示如果谈判破裂，将采取全面军事行动。伊朗持续进行核开发，国际社会的担忧在加剧。",
                "grammar": "「〜と主張する」— 主张…。例：進められていると主張（主张正在进行）。\n「〜一方で」— 一方面…另一方面。例：一方で（另一方面）。\n「〜示唆する」— 暗示、表明。例：考えも示唆しています（也暗示了想法）。",
                "vocab": [
                    ["協議", "きょうぎ", "协商、协议"],
                    ["主張", "しゅちょう", "主张"],
                    ["攻撃", "こうげき", "攻击"],
                    ["決裂", "けつれつ", "破裂、决裂"],
                    ["軍事作戦", "ぐんじさくせん", "军事作战"]
                ]
            },
            {
                "ja": "中東では緊張が続いており、サウジアラビア防空軍は27日、首都リヤドや同国東部の石油関連施設を狙った無人機（ドローン）を撃墜したと発表しました。サウジの国防当局者によると、ドローンはイランが支援するイラク国内の勢力が発射したものだということです。米国とイランの対立は中東全体の安定に影響を及ぼす可能性があり、国際社会は双方に自制を求めています。",
                "en": "Tensions continue in the Middle East. On the 27th, the Saudi Arabian Air Defense Force announced that it had shot down drones targeting the capital Riyadh and oil-related facilities in the eastern part of the country. According to Saudi defense officials, the drones were launched by Iran-backed forces within Iraq. The conflict between the US and Iran could affect the stability of the entire Middle East, and the international community is calling for restraint from both sides.",
                "literal": "中东紧张持续。沙特防空部队27日宣布击落了瞄准首都利雅得和该国东部石油相关设施的无人机。据沙特国防官员称，无人机是由伊朗支持的伊拉克境内势力发射的。美国和伊朗的对立可能影响整个中东的稳定，国际社会呼吁双方保持克制。",
                "grammar": "「〜によると」— 据…。例：国防当局者によると（据国防官员称）。\n「〜ということです」— 据说是…。例：発射したものだということです（据说是发射的）。\n「〜可能性がある」— 有…的可能性。例：影響を及ぼす可能性がある（有产生影响的可能性）。",
                "vocab": [
                    ["緊張", "きんちょう", "紧张"],
                    ["無人機", "むじんき", "无人机"],
                    ["撃墜", "げきつい", "击落"],
                    ["石油関連施設", "せきゆかんれんしせつ", "石油相关设施"],
                    ["自制", "じせい", "克制、自制"]
                ]
            }
        ]
    },
    # 11 — Apple market cap
    {
        "slug": "apple-shijyou-syuri",
        "title": "Apple時価総額 世界首位に返り咲き 株価過去最高",
        "subtitle": "Appleの株価が過去最高値を更新し、時価総額で世界首位に返り咲いた。AI戦略への期待が背景に。",
        "paras": [
            {
                "ja": "27日のニューヨーク株式市場で、米Appleの株価が最高値を更新し、時価総額で約4兆9400億ドルとなり世界首位に返り咲きました。Appleは業績が好調で、特にiPhoneの販売が堅調です。また、生成AI分野への積極的な投資も評価され、投資家の信頼を集めています。2位にはマイクロソフト、3位にはエヌビディアが続いています。",
                "en": "On the New York stock market on the 27th, US Apple's stock price hit a record high, returning to the top position worldwide with a market capitalization of approximately $4.94 trillion. Apple's performance is strong, particularly with solid iPhone sales. Additionally, its active investment in the generative AI field is being evaluated positively, gathering investor confidence. Microsoft is in second place, followed by Nvidia in third.",
                "literal": "27日的纽约证券市场上，美国苹果公司股价更新最高值，以约4.94万亿美元的市值重返世界首位。苹果业绩良好，尤其是iPhone销售坚挺。此外，对生成AI领域的积极投资也获得好评，赢得了投资者的信赖。第二位是微软，第三位是英伟达。",
                "grammar": "「〜で」— 以…。例：約4兆9400億ドルで（以约4.94万亿美元）。\n「〜特に」— 特别是。例：特にiPhoneの販売（特别是iPhone的销售）。\n「〜投資家の信頼を集める」— 吸引投资者的信任。例：信頼を集めています（在聚集信任）。",
                "vocab": [
                    ["時価総額", "じかそうがく", "市值总额"],
                    ["株価", "かぶか", "股价"],
                    ["最高値", "さいかね", "最高价"],
                    ["返り咲く", "かえりざく", "重返、东山再起"],
                    ["投資家", "とうしか", "投资者"]
                ]
            },
            {
                "ja": "Appleの好調な業績の背景には、Apple Intelligenceと呼ばれる自社開発のAI機能が搭載された最新iPhoneの需要が拡大していることがあります。また、サービス部門の収益も順調に伸びており、同社の収益源の多様化が進んでいます。市場アナリストはAppleの成長は当面続くと予測しており、時価総額5兆ドル突破も視野に入ってきています。",
                "en": "Behind Apple's strong performance is the expanding demand for the latest iPhone equipped with its self-developed AI features called 'Apple Intelligence.' Additionally, revenue from the services segment is growing steadily, and the company's revenue diversification is progressing. Market analysts predict Apple's growth will continue for the foreseeable future, with a market capitalization exceeding $5 trillion now within sight.",
                "literal": "苹果业绩良好的背景在于搭载了名为Apple Intelligence的自研AI功能的最新iPhone需求扩大。此外，服务部门的收入也在稳步增长，公司收入来源多样化正在推进。市场分析师预测苹果的增长短期内将持续，市值突破5万亿美元也进入了视野。",
                "grammar": "「〜背景にある」— 在…的背景下。例：好調の背景（业绩良好的背景）。\n「〜ている」— 正在…。例：拡大している（正在扩大）。\n「〜と予測する」— 预测…。例：続くと予測（预测会持续）。",
                "vocab": [
                    ["好調", "こうちょう", "良好、势头好"],
                    ["需要", "じゅよう", "需求"],
                    ["サービス部門", "さーびすぶもん", "服务部门"],
                    ["収益", "しゅうえき", "收益"],
                    ["多様化", "たようか", "多样化"]
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
        print(f"   🔊 Generating MP3 P{i+1}...", end=' ', flush=True)
        if gen_mp3(p['ja'], outpath):
            sz = os.path.getsize(outpath)
            print(f"({sz//1024}KB)")
        else:
            print(f"FAILED")

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
    print(f"   ✅ Blog post saved")

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
    escaped_title = item['title'].replace("'", "\\'").replace('"', '\\"')
    js_list.append(f"""    {{
      id: '{item['id']}',
      title: '{escaped_title}',
      kicker: '中級',
      desc: '',
      badge: '{item['length']}段落',
      file: '/asanews/assets/readings/{item['id']}.json'
    }}""")

existing_ids = {a['id'] for a in new_entries}
existing_entries = []
for item in existing_index:
    if item['id'] not in existing_ids:
        escaped = item['title'].replace("'", "\\'").replace('"', '\\"')
        existing_entries.append(f"""    {{
      id: '{item['id']}',
      title: '{escaped}',
      kicker: '中級',
      desc: '',
      badge: '{item['length']}段落',
      file: '/asanews/assets/readings/{item['id']}.json'
    }}""")

all_js_list = js_list + existing_entries
js_replace = "                                                        const READING_LIST = [\n" + ",\n".join(all_js_list) + "\n    ];"

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
