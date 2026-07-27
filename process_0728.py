#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-07-28 (Tue) Edition"""
import json, os, sys, subprocess, time, re, glob
from sudachipy import tokenizer, dictionary

BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-07-28'
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

articles = [
    {
        "slug": "shokuhin-syouhizei-1p",
        "title": "食料品の消費税1％ 政府・与党が方針固める 首相が30日にも指示へ",
        "subtitle": "政府・与党が食料品の消費税率を1％に引き下げる方針を固めた。高市首相が30日にも指示する見通し。",
        "paras": [
            {
                "ja": "政府・与党は28日、食料品の消費税率を軽減税率（8％）からさらに引き下げ、1％とする方針を固めた。高市早苗首相が30日にも関係閣僚に指示する見通しとなった。与党幹部によると、対象は飲食料品とし、2年間の時限措置とする案が軸となっている。低所得層向けの給付と合わせて検討する。",
                "en": "The government and ruling party on the 28th finalized a policy to further reduce the consumption tax rate on food items from the reduced rate (8%) to 1%. Prime Minister Takaichi is expected to instruct relevant ministers as early as the 30th. According to ruling party officials, the plan centers on a temporary measure targeting food and beverages for a period of two years. It will be considered alongside benefits for low-income groups.",
                "literal": "政府和执政党28日确定了将食品的消费税率从轻减税率（8％）进一步下调至1％的方针。高市早苗首相预计将在30日向相关阁僚下达指示。据执政党干部称，对象为饮食料品，以2年的时限措施方案为核心。将与面向低收入阶层的给付一并検讨。",
                "grammar": "「〜を固めた」— 确定了…。例：方針を固めた（确定了方针）。\n「〜見通し」— 预计…。例：指示する見通し（预计指示）。\n「〜を軸とする」— 以…为核心。例：案が軸となっている（以方案为核心）。",
                "vocab": [
                    ["食料品", "しょくりょうひん", "食品"],
                    ["消費税", "しょうひぜい", "消费税"],
                    ["軽減税率", "けいげんぜいりつ", "轻减税率"],
                    ["時限措置", "じげんそち", "时限措施"],
                    ["低所得層", "ていしょとくそう", "低收入阶层"]
                ]
            },
            {
                "ja": "一方、財源の問題が課題となっている。年7000億円程度の税収減が見込まれ、政府は特例公債や予備費の活用を検討している。野党からは「さらなる減税は財政を悪化させる」との批判が出ている。高市首相は支持率回復を狙い、8月上旬までに最終決断する考えだ。",
                "en": "Meanwhile, the funding issue remains a challenge. An annual tax revenue reduction of approximately 700 billion yen is expected, and the government is considering using special government bonds and reserve funds. Opposition parties have criticized that 'further tax cuts will worsen fiscal conditions.' Prime Minister Takaichi aims to make a final decision by early August, seeking to recover approval ratings.",
                "literal": "另一方面，财源问题成为课题。预计每年约7000亿日元的税收减少，政府正在検讨使用特例公债和预备费。在野党批评称「进一步的减税将使财政恶化」。高市首相以恢复支持率为目标，计划在8月上旬前做出最终决断。",
                "grammar": "「〜が見込まれる」— 预计…。例：税収減が見込まれる（预计税收减少）。\n「〜との批判」— …的批评。例：批判が出ている（出现了批评）。\n「〜考えだ」— 打算…。例：決断する考えだ（打算做出决断）。",
                "vocab": [
                    ["財源", "ざいげん", "财源"],
                    ["税収減", "ぜいしゅうげん", "税收减少"],
                    ["特例公債", "とくれいこうさい", "特例公债"],
                    ["予備費", "よびひ", "预备费"],
                    ["財政", "ざいせい", "财政"]
                ]
            }
        ]
    },
    {
        "slug": "taifuu13-gou-mouretsu",
        "title": "台風13号「ドルフィン」最強ランク「猛烈な」勢力へ 中心気圧915hPa",
        "subtitle": "台風13号がマーシャル諸島付近で発達し、最強ランク「猛烈な」台風へ。31日には中心気圧915hPaに達する見込み。",
        "paras": [
            {
                "ja": "気象庁が28日午前3時50分に発表した情報によると、台風13号（ドルフィン）はマーシャル諸島付近を西へ進みながら発達を続けている。今後の到達勢力は上方修正され、気象庁の基準で最強ランクとなる「猛烈な」台風まで急速に発達する見通しとなっている。中心気圧は992ヘクトパスカル、最大瞬間風速は35メートル。",
                "en": "According to information released by the Japan Meteorological Agency at 3:50 AM on the 28th, Typhoon No. 13 (Dolphin) is continuing to develop as it moves westward near the Marshall Islands. The forecast intensity has been revised upward, with the typhoon expected to rapidly develop into a 'violent' typhoon, the strongest rank on the JMA scale. The central pressure is 992 hPa, with maximum instantaneous wind speeds of 35 m/s.",
                "literal": "据气象厅28日上午3时50分发布的消息，台风第13号（海豚）在 Marshall 群岛附近向西前进的同时持续增强。今后的到达强度被上调，预计将急速发展为气象厅标准中最强等级的「猛烈」台风。中心气压992百帕，最大瞬间风速35米/秒。",
                "grammar": "「〜によると」— 据…。例：発表した情報によると（据发布的信息）。\n「〜見通し」— 预计。例：発達する見通し（预计增强）。\n「〜となっている」— 成为…。例：35メートルとなっている（为35米/秒）。",
                "vocab": [
                    ["台風", "たいふう", "台风"],
                    ["気象庁", "きしょうちょう", "气象厅"],
                    ["中心気圧", "ちゅうしんきあつ", "中心气压"],
                    ["最大瞬間風速", "さいだいしゅんかんふうそく", "最大瞬间风速"],
                    ["猛烈", "もうれつ", "猛烈、凶猛"]
                ]
            },
            {
                "ja": "今後の予報によると、台風13号は太平洋上を進みながら発達速度を強める見込みだ。31日午前3時には中心気圧915ヘクトパスカル、最大瞬間風速75メートルの「猛烈な」台風に達する予想。8月1日から2日にかけても勢力を維持したまま、南鳥島近海を西北西から北西へ進むと予想されている。現時点では日本本土から遠く離れているが、今後の動向に厳重な警戒が必要だ。",
                "en": "According to the latest forecast, Typhoon No. 13 is expected to accelerate its development as it moves across the Pacific Ocean. By 3:00 AM on the 31st, it is predicted to reach 'violent' typhoon status with a central pressure of 915 hPa and maximum instantaneous winds of 75 m/s. From August 1st to 2nd, it is expected to maintain its intensity while moving from west-northwest to northwest near Minamitorishima. Currently far from mainland Japan, but close vigilance of its future path is necessary.",
                "literal": "据今后预报，台风13号将在太平洋上前进的同时加强发展速度。预计31日上午3时将到达中心气压915百帕、最大瞬间风速75米/秒的「猛烈」台风。预计8月1日至2日期间也将维持势力，从西北西向北西方向在 Minamitorishima 近海前进。目前虽远离日本本土，但需要严密警戒今后的动向。",
                "grammar": "「〜ながら」— 一边…一边。例：進みながら（一边前进）。\n「〜にかけて」— 从…到…。例：1日から2日にかけて（从1日到2日）。\n「〜が予想される」— 被预计。例：進むと予想されている（被预计前进）。",
                "vocab": [
                    ["発達速度", "はったつそくど", "发展速度"],
                    ["勢力", "せいりょく", "势力、强度"],
                    ["南鳥島", "みなみとりしま", "南鸟岛"],
                    ["警戒", "けいかい", "警戒"],
                    ["動向", "どうこう", "动向、趋势"]
                ]
            }
        ]
    },
    {
        "slug": "henoko-doushisha-sousaku",
        "title": "辺野古転覆事故 海上保安当局が同志社国際高校を家宅捜索",
        "subtitle": "沖縄・辺野古沖での小型船転覆事故で、死亡した女子高校生の遺族側の告訴を受け、海保が同志社国際高校を家宅捜索した。",
        "paras": [
            {
                "ja": "沖縄県名護市辺野古沖で同志社国際高校の生徒らを乗せた小型船が転覆し、女子高校生と船長が死亡した事故で、海上保安当局が同志社国際高校を家宅捜索したことが分かった。この事故は3月16日、平和学習で訪れていた同校の生徒18人らを乗せた小型船2隻が転覆したもので、高校2年生の武石知華さんと船長の金井創さんが死亡した。",
                "en": "In connection with the capsizing accident of small boats off the coast of Henoko, Nago City, Okinawa, involving students from Doshisha International High School, which left a female high school student and a captain dead, the Japan Coast Guard conducted a search of the school. The accident occurred on March 16 when two small boats carrying 18 students from the school who were visiting for peace studies capsized, killing second-year student Takeishi Chika and captain Kanai So.",
                "literal": "在冲绳县名护市边野古外海，载有同志社国际高中学生的小型船只翻覆，导致女高中生和船长死亡的事故中，海上保安当局对同志社国际高中进行了家宅搜查。该事故于3月16日发生，当时载有正在参加和平学习的该校18名学生等的2艘小型船只翻覆，高二学生武石知华和船长金井创死亡。",
                "grammar": "「〜をめぐる」— 围绕…的。例：事故をめぐり（围绕事故）。\n「〜が分かった」— 判明。例：家宅捜索したことが分かった（判明进行了家宅搜查）。\n「〜もので」— 表示原因/说明。例：転覆したもので（翻覆了）。",
                "vocab": [
                    ["転覆", "てんぷく", "翻覆、倾覆"],
                    ["家宅捜索", "かたくそうさく", "家宅搜查"],
                    ["海上保安庁", "かいじょうほあんちょう", "海上保安厅"],
                    ["小型船", "こがたせん", "小型船只"],
                    ["遺族", "いぞく", "遗属、死者家属"]
                ]
            },
            {
                "ja": "遺族側によると、捜索は業務上過失致死傷容疑などでの告訴を受けたもの。告訴の対象は高校の校長ら4人と、市民団体「ヘリ基地反対協議会」の共同代表ら7人のあわせて11人に上る。学校法人同志社は取材に対し、「取材対応できる者が帰っているので、分からない」とコメントしている。事故をめぐっては、安全対策の不備が指摘されており、今後の捜査の行方が注目される。",
                "en": "According to the bereaved family, the search was based on a criminal complaint for charges including professional negligence resulting in death and injury. The complaint targets a total of 11 people — four including the high school principal, and seven including co-representatives of the civic group 'Heliport Opposition Council.' Doshisha Educational Corporation commented to the press saying, 'The person who can respond to inquiries has gone home, so we don't know.' Inadequate safety measures have been pointed out regarding the accident, and the future direction of the investigation is drawing attention.",
                "literal": "据遗属方面称，搜查是基于业务上过失致死伤等嫌疑的刑事告诉。告诉对象包括高中校长等4人以及市民团体「直升机基地反对协议会」的共同代表等7人，共计11人。学校法人同志社在接受采访时表示「能应对采访的人已经回家了，不清楚」。围绕该事故，安全措施不完善被指出，今后的搜查进展备受关注。",
                "grammar": "「〜によると」— 据…。例：遺族側によると（据遗属方面）。\n「〜に上る」— 达到…（数量）。例：11人に上る（达到11人）。\n「〜行方」— …的动向/走向。例：捜査の行方（搜查的走向）。",
                "vocab": [
                    ["業務上過失致死傷", "ぎょうむじょうかしつちししょう", "业务上过失致死伤"],
                    ["告訴", "こくそ", "控告、起诉"],
                    ["市民団体", "しみんだんたい", "市民团体"],
                    ["安全対策", "あんぜんたいさく", "安全措施"],
                    ["不備", "ふび", "不完备、缺陷"]
                ]
            }
        ]
    },
    {
        "slug": "trump-frb-risage",
        "title": "トランプ氏 FRBに利下げを要求 ウォーシュ議長は「素晴らしい」",
        "subtitle": "トランプ前大統領がFRBに利下げを要求。ウォーシュFRB議長を「素晴らしい」と評価した。",
        "paras": [
            {
                "ja": "トランプ前大統領は27日、連邦準備制度理事会（FRB）に対して利下げを実施するよう求めた。トランプ氏は自身のSNSで、「ウォーシュFRB議長は素晴らしい仕事をしているが、今すぐ利下げが必要だ。アメリカ経済のためにも、もっと積極的に利下げを行うべきだ」と投稿した。市場では年内の利下げ観測が強まっている。",
                "en": "Former President Trump on the 27th called on the Federal Reserve Board (FRB) to implement interest rate cuts. Trump posted on his social media, 'Chairman Walsh is doing a great job at the Fed, but rate cuts are needed immediately. For the sake of the American economy, rate cuts should be implemented more aggressively.' Market expectations for rate cuts within the year are strengthening.",
                "literal": "前总统特朗普27日要求联邦储备制度理事会（FRB）实施降息。特朗普在自身SNS上发文称「沃什FRB主席工作出色，但现在需要立即降息。为了美国经济，应该更积极地实施降息」。市场上年内降息的预期正在增强。",
                "grammar": "「〜よう求める」— 要求…。例：実施するよう求めた（要求实施）。\n「〜べきだ」— 应该…。例：行うべきだ（应该进行）。\n「〜観測が強まる」— …预期增强。例：利下げ観測が強まっている（降息预期在增强）。",
                "vocab": [
                    ["利下げ", "りさげ", "降息"],
                    ["連邦準備制度理事会", "れんぽうじゅんびせいどりじかい", "联邦储备委员会（FRB）"],
                    ["議長", "ぎちょう", "主席、议长"],
                    ["市場", "しじょう", "市场"],
                    ["観測", "かんそく", "观测、预期"]
                ]
            },
            {
                "ja": "トランプ氏は従来から低金利を主張しており、FRBの金融政策にたびたび介入してきた。今回の発言は、ウォーシュ議長が先週の連邦公開市場委員会（FOMC）で政策金利を据え置いたことを受けたものだ。ウォーシュ氏はトランプ政権時代に経済補佐官を務めた経歴があり、トランプ氏との関係は比較的良好とされている。専門家の間では、FRBの独立性を脅かす可能性を懸念する声も上がっている。",
                "en": "Trump has traditionally advocated for low interest rates and has frequently intervened in Fed monetary policy. His latest remarks came after Chairman Walsh held the policy rate steady at last week's FOMC meeting. Walsh previously served as an economic advisor during the Trump administration and his relationship with Trump is considered relatively good. Among experts, concerns have been raised that this could threaten the Fed's independence.",
                "literal": "特朗普一贯主张低利率，经常介入FRB的金融政策。此次发言是针对沃什主席在上周的联邦公开市场委员会（FOMC）会议上将政策利率维持不变。沃什氏在特朗普政权时代曾担任经济辅佐官，与特朗普的关系被认为相对良好。专家之间也出现了担忧可能威胁FRB独立性的声音。",
                "grammar": "「〜たびたび」— 屡次、经常。例：介入してきた（屡次介入）。\n「〜を受けたもの」— 基于…的。例：発言は…を受けたもの（发言是基于…）。\n「〜懸念する声」— 担忧的声音。例：声も上がっている（也出现了声音）。",
                "vocab": [
                    ["低金利", "ていきんり", "低利率"],
                    ["金融政策", "きんゆうせいさく", "金融政策"],
                    ["据え置く", "すえおく", "维持不变"],
                    ["経歴", "けいれき", "经历、履历"],
                    ["独立性", "どくりつせい", "独立性"]
                ]
            }
        ]
    },
    {
        "slug": "rosia-gun-teiin-zou",
        "title": "ロシア軍の定員242万6000人に引き上げ プーチン大統領が署名",
        "subtitle": "プーチン大統領がロシア軍の定員を現在の約240万人から242万6000人に引き上げる大統領令に署名した。",
        "paras": [
            {
                "ja": "ロシアのプーチン大統領は、ロシア軍の定員を現在の約240万人から242万6000人に引き上げる大統領令に署名した。国防省の発表によると、戦闘員を2万人以上増やす方針で、ウクライナへの侵攻を長期化させる意向を示したものとみられる。新たな定員は来年1月1日から適用される。",
                "en": "Russian President Putin signed a decree increasing the size of the Russian military from the current approximately 2.4 million to 2.426 million personnel. According to the Defense Ministry's announcement, the policy is to increase combat personnel by more than 20,000, seen as an indication of intent to prolong the invasion of Ukraine. The new staffing level will take effect from January 1st next year.",
                "literal": "俄罗斯总统普京签署了总统令，将俄罗斯军的定员从目前的约240万人增至242万6000人。据国防省发表，方针是增加2万人以上的战斗人员，被认为是表明了将乌克兰入侵长期化的意向。新定员将从明年1月1日起适用。",
                "grammar": "「〜を引き上げる」— 提高、提升。例：定員を引き上げる（提高定员）。\n「〜とみられる」— 被认为…。例：示したものとみられる（被认为表明了）。\n「〜から適用される」— 从…开始适用。例：1日から適用される（从1日起适用）。",
                "vocab": [
                    ["定員", "ていいん", "定员、编制人数"],
                    ["大統領令", "だいとうりょうれい", "总统令"],
                    ["署名", "しょめい", "署名、签字"],
                    ["戦闘員", "せんとういん", "战斗人员"],
                    ["侵攻", "しんこう", "入侵、进攻"]
                ]
            },
            {
                "ja": "今回の増員は2022年のウクライナ侵攻開始後、3回目の定員拡大となる。ロシアではウクライナ戦線での損失が続いており、兵力不足を補う目的があると分析されている。また、プーチン大統領は演説で「西側諸国との対立が長引く可能性がある」と述べ、軍の増強を継続する姿勢を示している。一方、国内では徴兵回避の動きや経済への負担増加が懸念されている。",
                "en": "This expansion is the third increase in personnel since the start of the Ukraine invasion in 2022. Russia continues to suffer losses on the Ukrainian front, and the move is analyzed as aimed at compensating for manpower shortages. Additionally, President Putin stated in a speech that 'confrontation with Western countries may be prolonged,' showing a posture of continuing military buildup. Meanwhile, concerns are rising domestically about draft evasion and increased economic burden.",
                "literal": "此次增员是2022年乌克兰入侵开始后的第3次定员扩大。俄罗斯在乌克兰战线持续出现损失，被分析为补充兵力不足的目的。此外，普京总统在演讲中表示「与西方各国的对立可能长期化」，显示出继续増強军队的姿态。另一方面，国内对征兵回避动向和经济负担增加的担忧正在扩大。",
                "grammar": "「〜となる」— 成为…、是第…次。例：3回目となる（是第3次）。\n「〜目的がある」— 有…的目的。例：補う目的がある（有补充的目的）。\n「〜一方」— 另一方面。例：一方（另一方面）。",
                "vocab": [
                    ["増員", "ぞういん", "增员、增加人员"],
                    ["兵力", "へいりょく", "兵力"],
                    ["戦線", "せんせん", "战线"],
                    ["徴兵", "ちょうへい", "征兵"],
                    ["負担", "ふたん", "负担"]
                ]
            }
        ]
    },
    {
        "slug": "ukuraina-rosia-douin",
        "title": "ウクライナ大統領「ロシアが30万〜50万人の動員を計画」",
        "subtitle": "ゼレンスキー大統領がロシアによる新たな大規模動員計画を暴露。30万〜50万人規模との見方を示した。",
        "paras": [
            {
                "ja": "ウクライナのゼレンスキー大統領は27日、ロシアが新たに30万人から50万人規模の動員を計画していると明らかにした。ゼレンスキー氏は夜のビデオ演説で「ロシアは秋から冬にかけて大規模な動員を準備している。30万人から50万人規模になる可能性がある」と述べ、西側諸国にさらなる軍事支援を要請した。",
                "en": "Ukrainian President Zelensky revealed on the 27th that Russia is planning a new mobilization of 300,000 to 500,000 personnel. In his evening video address, Zelensky stated, 'Russia is preparing a large-scale mobilization from autumn through winter. It could be on the scale of 300,000 to 500,000 people,' and called for further military support from Western countries.",
                "literal": "乌克兰总统泽连斯基27日明确表示，俄罗斯计划新动员30万至50万人规模。泽连斯基在晚间视频演讲中表示「俄罗斯正在准备从秋季到冬季的大规模动员。可能有30万到50万人规模」，并要求西方各国进一步提供军事支援。",
                "grammar": "「〜と明らかにした」— 明确表示…。例：計画していると明らかにした（明确表示正在计划）。\n「〜可能性がある」— 有…可能性。例：可能性がある（有可能性）。\n「〜を要請した」— 请求了…。例：支援を要請した（请求了支援）。",
                "vocab": [
                    ["動員", "どういん", "动员"],
                    ["ビデオ演説", "びでおえんぜつ", "视频演讲"],
                    ["大規模", "だいきぼ", "大规模"],
                    ["軍事支援", "ぐんじしえん", "军事支援"],
                    ["要請", "ようせい", "请求、要求"]
                ]
            },
            {
                "ja": "これに先立ち、プーチン大統領はロシア軍の定員を242万6000人に引き上げる大統領令に署名しており、動員計画の一環と見られている。ウクライナ軍はここ数ヶ月、東部戦線で劣勢が続いており、ゼレンスキー大統領は欧米に対し、長距離ミサイルや防空システムの供与を加速するよう求めている。ロシアとウクライナの双方で戦力の拡大が進み、戦闘の長期化は避けられない情勢だ。",
                "en": "Prior to this, President Putin signed a decree increasing the Russian military's personnel to 2.426 million, which is seen as part of the mobilization plan. Ukrainian forces have been at a disadvantage on the eastern front for several months, and President Zelensky is urging Western countries to accelerate the supply of long-range missiles and air defense systems. Both Russia and Ukraine are expanding their military capabilities, making a prolonged conflict unavoidable.",
                "literal": "在此之前，普京总统签署了将军队定员提高至242万6000人的总统令，被认为是动员计划的一环。乌克兰军队近几个月来在东部战线持续处于劣势，泽连斯基总统要求欧美加速提供长距离导弹和防空系统。俄罗斯和乌克兰双方都在推进战力扩大，战斗的长期化是不可避免的局势。",
                "grammar": "「〜に先立ち」— 在此之前。例：これに先立ち（在此之前）。\n「〜と見られている」— 被认为…。例：一環と見られている（被认为是一环）。\n「〜を余儀なくされる」— 被迫…（这里用「避けられない」）。例：避けられない（不可避免）。",
                "vocab": [
                    ["一環", "いっかん", "一环、一部分"],
                    ["劣勢", "れっせい", "劣势"],
                    ["長距離", "ちょうきょり", "长距离"],
                    ["防空システム", "ぼうくうしすてむ", "防空系统"],
                    ["戦力", "せんりょく", "战斗力、军事力量"]
                ]
            }
        ]
    },
    {
        "slug": "reomichan-itaiken",  
        "title": "「頑張ったね、おうちに帰ろうね」 行方不明の5歳男児・嶺臣ちゃん 父親が最後の対面語る",
        "subtitle": "鹿児島・霧島市の温泉施設から行方不明となっていた田中嶺臣くん（5歳）の遺体が発見され、父親が約1ヶ月ぶりの対面を語った。",
        "paras": [
            {
                "ja": "鹿児島県霧島市の天降川で先週見つかった遺体は、先月21日から行方不明となっていた田中嶺臣くん（5歳）と確認された。27日昼前、発見現場を訪れた父親は多くの花やお菓子が手向けられているのを見て、「近所の人かもしれない。とても感謝している」と静かに語った。警察からは「見ない方がいい」と止められたが、父親は「どうしても見たくて」と対面を決意した。",
                "en": "The body found last week in the Amorigawa River in Kirishima City, Kagoshima Prefecture, was confirmed to be 5-year-old Tanaka Reomi, who had been missing since the 21st of last month. When his father visited the discovery site around noon on the 27th and saw the many flowers and snacks left there, he quietly said, 'It might be neighbors. I'm very grateful.' The police advised him not to look, but the father decided to see his son, saying 'I absolutely wanted to see him.'",
                "literal": "在鹿儿岛县雾岛市的天降川上周发现的遗体，被确认是自上月21日起失踪的田中岭臣君（5岁）。27日午前，父亲访问发现现场，看到很多花和点心被供奉，静静地表示「可能是附近的人。非常感谢」。虽然警察劝阻说「最好别看」，但父亲决心见面说「无论如何都想见」。",
                "grammar": "「〜と確認された」— 被确认为…。例：嶺臣くんと確認された（确认为岭臣君）。\n「〜て欲しい」— 希望…（这里用感謝している）。例：感謝している（感谢）。\n「〜ても」— 即使…也。例：見たくて（想看）。",
                "vocab": [
                    ["行方不明", "ゆくえふめい", "下落不明"],
                    ["遺体", "いたい", "遗体"],
                    ["発見現場", "はっけんげんば", "发现现场"],
                    ["対面", "たいめん", "见面、会面"],
                    ["手向ける", "たむける", "供奉、献"]
                ]
            },
            {
                "ja": "父親は「嶺臣には変わりない」と顔を見て、「頑張ったね。おうちに帰ろうね」と声をかけたという。嶺臣くんは6月21日、霧島市の温泉施設「かれい川の湯」で、両親が3分ほど目を離した間に浴室からいなくなり、行方が分からなくなっていた。窓から外に出られる構造で、窓の下から川まで約8メートル。警察は嶺臣くんが自分で窓から外に出て川に落ちた可能性があるとみている。",
                "en": "His father saw his face and said 'He's still Reomi,' and spoke to him, saying 'You did great. Let's go home.' Reomi went missing on June 21st at the 'Kareigawa no Yu' hot spring facility in Kirishima City, when his parents looked away for about three minutes and he disappeared from the bathroom. The structure allowed exit through a window, and it was about 8 meters from below the window to the river. Police believe it is possible that Reomi went out through the window on his own and fell into the river.",
                "literal": "父亲看到脸说「还是岭臣没错」，并说「努力了。回家吧」。岭臣君于6月21日在雾岛市的温泉设施「かれい川之汤」中，父母视线离开约3分钟期间从浴室消失，行踪不明。构造可以通过窗户到外面，从窗户下到河边约8米。警察认为岭臣君可能自己从窗户出去掉进了河里。",
                "grammar": "「〜という」— 据说…。例：声をかけたという（据说说了话）。\n「〜間に」— 在…期间。例：目を離した間に（在视线移开期间）。\n「〜可能性がある」— 有…可能性。例：落ちた可能性がある（有掉落的可能性）。",
                "vocab": [
                    ["温泉施設", "おんせんしせつ", "温泉设施"],
                    ["浴室", "よくしつ", "浴室"],
                    ["目を離す", "めをはなす", "视线移开"],
                    ["構造", "こうぞう", "构造"],
                    ["損傷", "そんしょう", "损伤"]
                ]
            }
        ]
    },
    {
        "slug": "kiritani-hiroto-gan",
        "title": "桐谷広人さん 前立腺と大腸に「2つのがん」 闘病と株主優待の日々",
        "subtitle": "「将棋の棋士」「株主優待の達人」として知られる桐谷広人さんが前立腺がんと大腸がんの同時罹患を公表。闘病生活を語った。",
        "paras": [
            {
                "ja": "「将棋の棋士」として知られ、「株主優待の達人」としてもおなじみの桐谷広人さん（75）が、前立腺がんと大腸がんの「2つのがん」を患っていることを公表した。今年1月に前立腺がんが見つかり、術前検査の過程で大腸がんも発覚。6月末には大腸がんの手術を受け、約40〜60センチの腸を切除した。桐谷さんは「不幸中の幸いでした」と笑顔で語った。",
                "en": "Kirita Hiroto (75), known as a 'shogi professional' and familiar as the 'master of shareholder perks,' has revealed that he is suffering from two cancers — prostate cancer and colon cancer. Prostate cancer was discovered in January, and colon cancer was also detected during pre-operative testing. He underwent colon cancer surgery at the end of June, with about 40-60 cm of his intestine removed. Kirita smiled and said, 'It was a blessing in disguise.'",
                "literal": "以「将棋棋士」闻名，也以「股东优惠达人」为人熟知的桐谷广人先生（75岁）公开了患有前列腺癌和直肠癌「两种癌症」的情况。今年1月发现前列腺癌，在术前检查过程中也发现了大肠癌。6月末接受了大肠癌手术，切除了约40〜60厘米的肠道。桐谷先生笑着说「真是不幸中的万幸」。",
                "grammar": "「〜として知られる」— 作为…知名。例：棋士として知られる（作为棋士知名）。\n「〜を患う」— 患病。例：がんを患っている（患有癌症）。\n「〜を公表した」— 公开了…。例：公表した（公开了）。",
                "vocab": [
                    ["将棋", "しょうぎ", "将棋、日本象棋"],
                    ["棋士", "きし", "棋手、棋士"],
                    ["株主優待", "かぶぬしゆうたい", "股东优惠"],
                    ["前立腺がん", "ぜんりつせんがん", "前列腺癌"],
                    ["大腸がん", "だいちょうがん", "大肠癌"]
                ]
            },
            {
                "ja": "桐谷さんは術後の経過について、「手術の翌日からリハビリで歩いた。3日目から自転車のリハビリもさせられた」と明かした。「自転車のリハビリなんて桐谷さんだからですか？」と聞かれると、「誰でもやるみたいです」と笑った。今後は半年間の抗がん剤治療を受ける予定で、「しんどくて仕事に行けない日も出てくるかもしれないが、楽しみにしてくれている方のためにできるだけ行きたい」と前向きに語っている。",
                "en": "Regarding his post-operative recovery, Kirita revealed, 'I started walking for rehabilitation the day after surgery. From day three, they even had me do cycling rehab.' When asked, 'Is the cycling rehab just because you're Kirita-san?' he laughed and said, 'It seems everyone does it.' He plans to undergo six months of chemotherapy going forward, saying positively, 'There may be days when I'm too unwell to work, but for those who look forward to seeing me, I want to go as much as possible.'",
                "literal": "关于术后经过，桐谷先生透露「手术第二天就开始走路康复。第3天开始还做了自行车康复」。当被问到「自行车康复只因为是桐谷先生吗？」，他笑着说「好像谁都会做」。今后预定接受半年的抗癌剂治疗，他积极地说「也许会有难受得无法工作的日子，但为了期待见到我的人，我想尽可能去」。",
                "grammar": "「〜について」— 关于…。例：経過について（关于经过）。\n「〜と聞かれると」— 被问到…时。例：聞かれると（被问到）。\n「〜つもりだ」— 打算…。例：受ける予定（预定接受）。",
                "vocab": [
                    ["術後", "じゅつご", "术后、手术后"],
                    ["リハビリ", "りはびり", "康复训练"],
                    ["抗がん剤", "こうがんざい", "抗癌剂、化疗药物"],
                    ["前向き", "まえむき", "积极、向前看"],
                    ["闘病", "とうびょう", "与疾病斗争"]
                ]
            }
        ]
    },
    {
        "slug": "chugoku-teppomizu",
        "title": "中国のキャンプ場で「鉄砲水」 テントが次々濁流に 10人死亡",
        "subtitle": "中国のキャンプ場で鉄砲水が発生し、テントが濁流に飲み込まれて少なくとも10人が死亡した。",
        "paras": [
            {
                "ja": "中国南部のキャンプ場で27日、鉄砲水が発生し、テントが次々に濁流に飲み込まれる事故があった。地元当局によると、これまでに少なくとも10人の死亡が確認され、数人が行方不明となっている。現場では観光客らが川沿いにテントを設営しており、突然の増水により逃げ遅れたとみられる。映像には「子ども！子ども！」と叫ぶ人々の声が記録されていた。",
                "en": "On the 27th, a flash flood occurred at a campsite in southern China, with tents being swallowed one after another by the muddy torrent. According to local authorities, at least 10 deaths have been confirmed so far, with several people still missing. Tourists had set up tents along the river at the site and are believed to have been unable to escape in time due to the sudden rise in water levels. Footage captured people shouting 'Children! Children!'",
                "literal": "中国南部的露营地27日发生山洪，帐篷相继被浊流吞没。据当地当局称，目前已确认至少10人死亡，数人下落不明。现场有游客沿河搭建帐篷，据认为因突然涨水而未能及时逃生。录像中记录着人们呼喊「孩子！孩子！」的声音。",
                "grammar": "「〜によると」— 据…。例：地元当局によると（据当地当局）。\n「〜とみられる」— 被认为…。例：逃げ遅れたとみられる（被认为未能及时逃生）。\n「〜ていた」— 过去进行时。例：記録されていた（被记录着）。",
                "vocab": [
                    ["キャンプ場", "きゃんぷじょう", "露营地"],
                    ["鉄砲水", "てっぽうみず", "山洪、突发的洪水"],
                    ["濁流", "だくりゅう", "浊流、泥水"],
                    ["行方不明", "ゆくえふめい", "下落不明"],
                    ["設営", "せつえい", "搭建、设置"]
                ]
            },
            {
                "ja": "中国では夏季に局地的な豪雨が増えており、今回の事故も突然の水位上昇が原因とみられる。専門家は気候変動の影響で、こうした異常気象が今後さらに頻発する可能性を指摘している。中国当局は現場周辺での捜索活動を続けるとともに、安全なキャンプ場運営のためのガイドライン強化を検討している。",
                "en": "Localized heavy rainfall increases in China during the summer season, and this accident is also believed to have been caused by a sudden rise in water levels. Experts point out that such extreme weather events could become more frequent in the future due to the effects of climate change. Chinese authorities are continuing search operations around the site and are considering strengthening guidelines for safe campsite operations.",
                "literal": "中国夏季局部暴雨增多，此次事故也被认为是突然水位上升所致。专家指出受气候变化影响，此类异常气象今后可能更加频发。中国当局在继续进行现场周边的搜索活动的同时，也在検讨加強安全露营地运营的指导方针。",
                "grammar": "「〜が原因」— 以…为原因。例：水位上昇が原因（以水位上升为原因）。\n「〜可能性を指摘」— 指出可能性。例：頻発する可能性を指摘（指出频发的可能性）。\n「〜とともに」— 与…一起/同时。例：続けるとともに（在继续的同时）。",
                "vocab": [
                    ["豪雨", "ごうう", "暴雨"],
                    ["気候変動", "きこうへんどう", "气候变化"],
                    ["異常気象", "いじょうきしょう", "异常气象"],
                    ["ガイドライン", "がいどらいん", "指导方针"],
                    ["頻発", "ひんぱつ", "频发"]
                ]
            }
        ]
    }
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

# UPDATE index.json
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

# UPDATE reading-room.js READING_LIST
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

# VERIFY
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
