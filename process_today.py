#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-07-25 (Sat) Edition"""
import json, os, sys, subprocess, time, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-07-25'
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
# TODAY'S ARTICLES — 2026-07-25
# ==================================================================
articles = [
    {
        "slug": "fukushuto-houritsu-seiritsu",
        "title": "「副首都構想」具体化に向けた法律が可決・成立",
        "subtitle": "災害時の首都機能バックアップと東京一極集中是正を目的とした「副首都」関連法が参議院本会議で可決・成立した。",
        "paras": [
            {
                "ja": "副首都構想を具体化するための法律が24日、参議院本会議で自民、維新、チームみらいなどの賛成多数で可決・成立した。この法律は、災害時に首都機能を維持するためのバックアップとして「副首都」を整備し、東京一極集中の是正を目指すことを柱としている。",
                "en": "The bill to realize the sub-capital concept was passed and enacted on the 24th at the House of Councillors plenary session with majority approval from the LDP, Ishin, Team Mirai, and others. The law aims to develop a 'sub-capital' as a backup to maintain capital functions during disasters and to correct the excessive concentration in Tokyo.",
                "literal": "为实现副首都构想的具体化法律，24日在参议院全体会议上以自民、维新、Team Mirai等多数赞成通过并成立。该法律以整备「副首都」作为灾害时维持首都功能的备份，以及纠正东京一极集中为核心目标。",
                "grammar": "「〜に向けた」— 面向…的、为…的。例：具体化に向けた法律（为实现具体化的法律）。\n「〜を柱とする」— 以…为核心。例：是正を目指すことを柱としている（以矫正为目标作为核心）。\n「〜で可決・成立」— 以…通过并成立。例：賛成多数で可決・成立（以多数赞成通过并成立）。",
                "vocab": [
                    ["副首都", "ふくしゅと", "副首都、备份首都"],
                    ["可決", "かけつ", "通过（法案）"],
                    ["成立", "せいりつ", "成立"],
                    ["参議院", "さんぎいん", "参议院"],
                    ["一極集中", "いっきょくしゅうちゅう", "一极集中、过度集中"]
                ]
            },
            {
                "ja": "野党側は、採決の条件として特別区設置の住民投票と関係する自治体選挙の同日実施を禁止する内容を付帯決議に盛り込むよう求めていた。与野党は最終的に住民投票と自治体選挙が「重複しないように最大限調整する」との文言を明記することで調整が付き、採決することで合意した。",
                "en": "The opposition parties had demanded that the supplementary resolution include a provision prohibiting simultaneous implementation of a special ward residents' referendum and related local elections as a condition for the vote. The ruling and opposition parties ultimately reached an agreement by specifying language that they would 'coordinate to the maximum extent to avoid overlap' between the referendum and local elections, allowing the vote to proceed.",
                "literal": "在野党方面要求作为表决条件，在附带决议中加入禁止特别区设置的居民投票和相关地方自治体选举同日实施的内容。执政党与在野党最终通过明确记载「最大限度调整以避免」居民投票和地方选举「重复」的措辞达成了协调，并同意进行表决。",
                "grammar": "「〜として」— 作为…。例：条件として（作为条件）。\n「〜よう求める」— 要求…。例：盛り込むよう求めていた（要求加入）。\n「〜ことで合意した」— 就…达成一致。例：調整が付き、採決することで合意した（协调一致，同意进行表决）。",
                "vocab": [
                    ["野党", "やとう", "在野党"],
                    ["採決", "さいけつ", "表决"],
                    ["住民投票", "じゅうみんとうひょう", "居民投票"],
                    ["付帯決議", "ふたいけつぎ", "附带决议"],
                    ["与党", "よとう", "执政党"]
                ]
            }
        ]
    },
    {
        "slug": "taifuu12-gou-hattatsu",
        "title": "台風12号「ノウル」南シナ海で発達 強い勢力で中国華南に上陸へ",
        "subtitle": "台風12号が南シナ海で発達し、強い勢力で中国華南に上陸の恐れ。日本への直接影響は低いが、航路や航空便に注意が必要。",
        "paras": [
            {
                "ja": "台風12号（ノウル）は25日午前6時現在、南シナ海を時速30キロの速さで西北西へ進んでいる。台風は今後さらに発達し、25日夜には「強い」勢力に成長する見込み。26日にかけて中心気圧965ヘクトパスカルまで達した状態で中国南部の華南に接近・上陸する恐れがある。",
                "en": "As of 6:00 AM on the 25th, Typhoon No. 12 (Noul) is moving northwestward across the South China Sea at 30 km/h. The typhoon is expected to develop further and reach 'strong' intensity by the night of the 25th. By the 26th, it is likely to approach and make landfall in southern China's Huanan region with a central pressure of 965 hPa.",
                "literal": "台风第12号（诺尔）25日上午6点现在，以时速30公里向南中国海的西北西方向前进。台风今后将进一步加强，预计25日晚达到「强」势力。到26日为止，中心气压可能降至965百帕，并以该状态接近并登陆中国南部的华南地区。",
                "grammar": "「〜現在」— 截止…时点。例：午前6時現在（上午6点截止）。\n「〜見込み」— 预计…。例：勢力に成長する見込み（预计成长为…势力）。\n「〜恐れがある」— 有…的危险/可能。例：上陸する恐れがある（有登陆的可能）。",
                "vocab": [
                    ["台風", "たいふう", "台风"],
                    ["発達する", "はったつする", "发展、增强"],
                    ["勢力", "せいりょく", "势力、强度"],
                    ["上陸", "じょうりく", "登陆"],
                    ["中心気圧", "ちゅうしんきあつ", "中心气压"]
                ]
            },
            {
                "ja": "日本本土への直接的な影響は低いと見られるが、周辺海域を通る航路や航空便、現地の交通・物流等に影響が出る可能性があるため、最新の運行情報等に注意が必要だ。台風12号は海面水温が高い南シナ海を進みながら勢力を強めており、26日午前6時には最大瞬間風速50メートルまで発達して華南沿岸に達する予想。その後は陸上を進んで急速に衰え、27日午前までに熱帯低気圧に変わる見込みだ。",
                "en": "While direct impact on mainland Japan is expected to be low, there may be effects on shipping routes, flights, and local transportation and logistics in the region, so attention to the latest operational information is necessary. Typhoon No. 12 is intensifying as it moves across the warm waters of the South China Sea. It is forecast to develop to maximum instantaneous wind speeds of 50 m/s by 6:00 AM on the 26th as it reaches the South China coast. Thereafter, it will move inland and rapidly weaken, expected to become a tropical depression by the morning of the 27th.",
                "literal": "对日本本土的直接影响被认为较低，但经由周边海域的航路、航空便以及当地的交通、物流等可能受到影响，因此需要关注最新运行信息。台风12号在海水温度高的南中国海前进的同时增强势力，预计26日上午6点将增强至最大瞬间风速50米/秒并到达华南沿岸。之后将进入陆地急速减弱，预计27日上午前转变为热带低气压。",
                "grammar": "「〜と見られる」— 被认为…。例：低いと見られる（被认为较低）。\n「〜ながら」— 一边…一边…。例：進みながら（一边前进一边…）。\n「〜までに」— 到…之前。例：27日午前までに（到27日上午之前）。",
                "vocab": [
                    ["本土", "ほんど", "本土"],
                    ["航路", "こうろ", "航线、航路"],
                    ["最大瞬間風速", "さいだいしゅんかんふうそく", "最大瞬间风速"],
                    ["華南", "かなん", "华南（中国南部）"],
                    ["熱帯低気圧", "ねったいていきあつ", "热带低气压"]
                ]
            }
        ]
    },
    {
        "slug": "shijiritsu-kyuuraku-takaichi",
        "title": "支持率急落を招く高市首相の「人間不信」 その原点となった地元との確執",
        "subtitle": "毎日新聞調査で支持率41％に急落。高市首相の強引な政治手法の背景にある人間不信と過去のトラウマを分析。",
        "paras": [
            {
                "ja": "毎日新聞の調査で高市内閣の支持率が前月から10ポイント減の41％となった。支持率下落の理由として指摘されているのが、高市早苗首相の強引な政治手法だ。何でも一人で決め、誰にも相談しない「孤高の総理」と言われる高市首相だが、その背後には人とのコミュニケーションが不得手という「人間不信」的な一面が見え隠れする。",
                "en": "In the Mainichi Shimbun survey, the approval rating for the Takaichi Cabinet fell 10 points from the previous month to 41%. The reason cited for the decline is Prime Minister Takaichi's forceful political style. Known as a 'solitary premier' who decides everything alone and consults no one, behind this approach lies a facet of 'mistrust of people' — a difficulty with interpersonal communication.",
                "literal": "每日新闻的调查中，高市内阁的支持率比上个月下降10个百分点至41%。作为支持率下降的原因被指出的是高市早苗首相的强行政治手法。虽然被称为万事一人决定、不与任何人商量的「孤高总理」，但其背后可见不擅长与人沟通的「对人缺乏信任」的一面。",
                "grammar": "「〜として指摘されている」— 作为…被指出。例：理由として指摘されている（作为理由被指出）。\n「〜と言われる」— 被称为…。例：「孤高の総理」と言われる（被称为「孤高的总理」）。\n「〜が見え隠れする」— 隐约可见…。例：一面が見え隠れする（隐约可见一面）。",
                "vocab": [
                    ["支持率", "しじりつ", "支持率"],
                    ["急落", "きゅうらく", "急剧下降"],
                    ["強引", "ごういん", "强行、强硬"],
                    ["孤高", "ここう", "孤高"],
                    ["人間不信", "にんげんふしん", "对人的不信任"]
                ]
            },
            {
                "ja": "高市首相は1992年参院選で自民党からの出馬を申請するが、世襲候補との公認争いに敗れると、県連の反対を押し切って無所属で出馬して落選した。翌年衆院選でトップ当選を果たしたものの、地元県連とのしこりは大きく、その後も誹謗中傷や怪文書に悩まされ続けた。こうした経験から「若い頃に懲りて、誰から誘われても行かない」と議員との付き合いを避けるようになったという。",
                "en": "Prime Minister Takaichi applied to run in the 1992 House of Councillors election as an LDP candidate, but after losing the endorsement race to a hereditary candidate, she ran as an independent against the prefectural association's opposition and lost. Although she achieved the top vote in the following year's general election, the rift with the local party association remained large, and she continued to suffer from slander and anonymous documents. These experiences reportedly taught her a lesson: 'I learned my lesson when I was young, so I don't go anywhere no matter who invites me,' leading her to avoid socializing with fellow lawmakers.",
                "literal": "高市首相在1992年参院选举中申请从自民党出马，但在与世袭候选人的公认竞争中落败后，不顾县联的反对以无党派身份出马并落选。虽在次年的众院选举中以最高票当选，但与当地县联的芥蒂很大，之后也持续遭受诽谤中伤和匿名传单的困扰。据说从这些经验中「年轻时吃了教训，不管谁邀请都不去」，变得回避与议员的交往。",
                "grammar": "〜を押し切る — 不顾…、强行…。例：反対を押し切って（不顾反对）。\n「〜ものの」— 虽然…但是…。例：果たしたものの（虽然实现了…但是…）。\n「〜という」— 据说…。例：避けるようになったという（据说变得回避了）。",
                "vocab": [
                    ["出馬", "しゅつば", "出马、参选"],
                    ["世襲", "せしゅう", "世袭"],
                    ["公認", "こうにん", "公认、正式认可"],
                    ["無所属", "むしょぞく", "无党派"],
                    ["誹謗中傷", "ひぼうちゅうしょう", "诽谤中伤"]
                ]
            }
        ]
    },
    {
        "slug": "nihonka-suru-chugoku",
        "title": "「日本化」する中国 2050年の1人当たりGDPは米国の4分の1に",
        "subtitle": "英シンクタンクが中国経済の「日本化」リスクを指摘。不動産バブル崩壊で約2900兆円が消失。長期停滞の懸念。",
        "paras": [
            {
                "ja": "2026年の中国は、日本が停滞に陥っていく有様を目の当たりにしてきた人なら誰にとっても見覚えのある様相を呈している。不動産バブルの崩壊が家計資産を蒸発させ、資産価格は低迷から抜け出せず、消費者は慎重姿勢に転じ、労働力は縮小しつつあり、統計データにはデフレが忍び寄る。これらは30年前に日本を低成長均衡の状態に閉じ込めたのと同じ要因の組み合わせだ。",
                "en": "China in 2026 presents a picture familiar to anyone who has witnessed Japan's descent into stagnation. The collapse of the real estate bubble has evaporated household assets, asset prices remain mired in a slump, consumers have turned cautious, the labor force is shrinking, and deflation is creeping into the statistics. These are the same combination of factors that trapped Japan in a low-growth equilibrium 30 years ago.",
                "literal": "2026年的中国，呈现出任何目睹过日本陷入停滞状态的人都熟悉的景象。房地产泡沫的崩溃使家庭资产蒸发，资产价格无法摆脱低迷，消费者转向谨慎态度，劳动力正在缩小，统计数据显示通缩正在逼近。这些都是30年前将日本封锁在低增长均衡状态中的相同因素的组合。",
                "grammar": "「〜を目の当たりにする」— 亲眼目睹…。例：有様を目の当たりにしてきた（亲眼目睹了…的状态）。\n「〜つつある」— 正在…。例：縮小しつつあり（正在缩小）。\n「〜と同じ」— 与…相同。例：要因の組み合わせだ（是…因素的组合）。",
                "vocab": [
                    ["停滞", "ていたい", "停滞"],
                    ["不動産", "ふどうさん", "不动产、房地产"],
                    ["バブル", "ばぶる", "泡沫"],
                    ["家計資産", "かけいしさん", "家庭资产"],
                    ["デフレ", "でふれ", "通缩、通货紧缩"]
                ]
            },
            {
                "ja": "英経済シンクタンクのオックスフォード・エコノミクスによると、中国では不動産バブル崩壊により2025年末までに約18兆ドル（約2900兆円）の家計資産が失われた。損失額は2008年のリーマン・ショックを上回っている。同社の長期予測によれば、2050年になっても中国の1人当たりGDPは米国のわずか4分の1にとどまると予想される。生産性向上の度合いが今後の鍵を握るとしている。",
                "en": "According to Oxford Economics, a British economic think tank, about $18 trillion (approx. 2,900 trillion yen) in household assets were lost in China by the end of 2025 due to the collapse of the real estate bubble. The losses exceed those of the 2008 Lehman Shock. According to their long-term forecast, China's per capita GDP will remain at only one-quarter of the US level even by 2050. The degree of productivity improvement will be the key going forward.",
                "literal": "据英国经济智库Oxford Economics称，中国因房地产泡沫崩溃到2025年底损失了约18万亿美元（约2900万亿日元）的家庭资产。损失额超过了2008年的雷曼冲击。根据该公司的长期预测，即使到2050年，中国的人均GDP预计也仅停留在美国的四分之一。生产性提高的程度被认为是今后的关键。",
                "grammar": "「〜によると」— 据…说。例：オックスフォード・エコノミクスによると（据Oxford Economics称）。\n「〜を上回る」— 超过…。例：損失額は…を上回っている（损失额超过…）。\n「〜にとどまる」— 停留在…。例：4分の1にとどまる（停留在四分之一）。",
                "vocab": [
                    ["シンクタンク", "しんくたんく", "智库"],
                    ["損失額", "そんしつがく", "损失额"],
                    ["リーマン・ショック", "りーまん・しょっく", "雷曼冲击"],
                    ["長期予測", "ちょうきよそく", "长期预测"],
                    ["生産性", "せいさんせい", "生产性"]
                ]
            }
        ]
    },
    {
        "slug": "syouhizei-genzei-seiken-owaru",
        "title": "消費減税見送りなら「政権終わる」 支持率下落で官邸に危機感",
        "subtitle": "食料品の消費税減税をめぐり高市首相が決断迫られる。実現しなければ政権存続も危ういとの見方。",
        "paras": [
            {
                "ja": "飲食料品の消費税減税や低所得層向け給付を検討してきた「社会保障国民会議」は、与野党の間で空中分解してしまった。2年間だけの「消費税1％＋給付」の導入を高市首相は決断できるのか。専門家からは物価対策としての有効性や財源に疑問の声が上がり、自民党内にも反対は少なくなく、官邸は危機感いっぱいだという。",
                "en": "The 'National Council on Social Security,' which had been considering consumption tax reductions on food and beverages as well as benefits for low-income groups, has fallen apart between the ruling and opposition parties. Can Prime Minister Takaichi decide to introduce a '1% consumption tax plus benefits' plan for only two years? Experts have raised questions about its effectiveness as a price measure and its funding, and there is considerable opposition even within the LDP, with the Prime Minister's Office reportedly full of a sense of crisis.",
                "literal": "一直在讨论食品饮料消费税减税和向低收入阶层给付的「社会保障国民会议」在朝野政党之间空中解体了。高市首相应能否决断导入仅2年的「消费税1％+给付」？专家对其作为物价对策的有效性和财源提出了质疑，自民党内反对也不少，据称官邸充满危机感。",
                "grammar": "「〜をめぐり」— 围绕…。例：減税をめぐり（围绕减税）。\n「〜か」— 表示疑问。例：決断できるのか（能够决断吗）。\n「〜という」— 据说…。例：危機感いっぱいだという（据说充满危机感）。",
                "vocab": [
                    ["消費税", "しょうひぜい", "消费税"],
                    ["減税", "げんぜい", "减税"],
                    ["低所得層", "ていしょとくそう", "低收入阶层"],
                    ["給付", "きゅうふ", "给付、补贴"],
                    ["財源", "ざいげん", "财源"]
                ]
            },
            {
                "ja": "「報道ステーション」は22日の放送で、官邸キャップが「間違いなく、高市総理は決断すると思う」「官邸を取材しているが『消費減税をやめよう』という雰囲気は一切ない」と伝えた。ANNの世論調査で内閣支持率は50％を切り、総選挙で公約した減税への疑念が一因とみられる。官邸内では「消費税をやらなければ政権が終わる」との危機感が広がっているという。高市首相は8月上旬までに決断するとしている。",
                "en": "On the July 22 broadcast of 'News Station,' the chief government press officer reported, 'Prime Minister Takaichi will undoubtedly decide,' and 'In covering the Prime Minister's Office, there is absolutely no atmosphere of 'let's abandon the consumption tax cut.'' The ANN opinion poll showed the cabinet approval rating falling below 50%, with doubts about the tax cut promised in the general election seen as one factor. Within the Prime Minister's Office, a sense of crisis is spreading that 'if we don't implement the consumption tax cut, the administration will end.' Prime Minister Takaichi is expected to make a decision by early August.",
                "literal": "「报道Station」在22日的节目中，官邸负责人传达了「毫无疑问，高市总理会做出决断」「在采访官邸时完全没有『放弃消费税减税』的氛围」。ANN的舆论调查中内阁支持率跌破50%，对总选举中承诺的减税的怀疑被认为是一个原因。官邸内据称蔓延着「如果不实行消费税减税，政权就会终结」的危机感。高市首相预计在8月上旬前做出决断。",
                "grammar": "「〜と思う」— 认为…。例：決断すると思う（认为会决断）。\n「〜を切る」— 跌破…。例：50％を切った（跌破50%）。\n「〜としている」— 表示预定/声称。例：決断するとしている（预定做出决断）。",
                "vocab": [
                    ["官邸", "かんてい", "官邸、首相官邸"],
                    ["キャップ", "きゃっぷ", "负责人、主任"],
                    ["雰囲気", "ふんいき", "氛围、气氛"],
                    ["公約", "こうやく", "公约、承诺"],
                    ["疑念", "ぎねん", "疑虑、怀疑"]
                ]
            }
        ]
    },
    {
        "slug": "ukuraina-dorone-kougeki",
        "title": "ウクライナ軍がロシアの通販倉庫にドローン攻撃 物流網への攻撃強める",
        "subtitle": "ロシアのネット通販大手ワイルドベリーズの倉庫にドローン攻撃。ウクライナは軍事物流拠点と主張。",
        "paras": [
            {
                "ja": "ロシアのネット通販大手「ワイルドベリーズ」は24日、北西部・サンクトペテルブルクの郊外とレニングラード州にある倉庫がウクライナ軍によるドローン攻撃を受けたと発表した。レニングラード州の知事は、攻撃によって3人がけがをしたとしている。ウクライナ側はこうした施設がドローン用部品などの物流拠点になっていると主張し、攻撃を強めている。",
                "en": "Russia's major online retailer Wildberries announced on the 24th that warehouses in the suburbs of northwestern St. Petersburg and in Leningrad Oblast were hit by a Ukrainian drone attack. The governor of Leningrad Oblast stated that three people were injured in the attack. Ukraine claims that such facilities serve as logistics hubs for drone components and is intensifying its attacks.",
                "literal": "俄罗斯的网络购物巨头「Wildberries」24日发表声明称，位于西北部圣彼得堡郊外和列宁格勒州的仓库遭到乌克兰军队的无人机攻击。列宁格勒州州长表示攻击造成3人受伤。乌方主张此类设施是无人机用零部件等的物流据点，并加强了攻击。",
                "grammar": "「〜による」— 由…引起的。例：ドローン攻撃による（由无人机攻击造成的）。\n「〜としている」— 表示主张/声称。例：3人がけがをしたとしている（声称有3人受伤）。\n「〜を強める」— 加强…。例：攻撃を強めている（正在加强攻击）。",
                "vocab": [
                    ["ドローン", "どろーん", "无人机"],
                    ["倉庫", "そうこ", "仓库"],
                    ["ネット通販", "ねっとつうはん", "网络购物"],
                    ["物流拠点", "ぶつりゅうきょてん", "物流据点"],
                    ["負傷", "ふしょう", "受伤"]
                ]
            },
            {
                "ja": "一方、ウクライナのゼレンスキー大統領は、ロシア中部キーロフにある軍事企業を攻撃したと明らかにした。この企業がミサイル用部品などを供給していたと主張している。また、この日、首都キーウ近郊へのロシア軍のミサイル攻撃で10人が死亡した。ウクライナとロシア双方が攻撃を激化させており、戦闘の長期化が懸念されている。",
                "en": "Meanwhile, Ukrainian President Zelensky revealed that they had attacked a military enterprise in Kirov, central Russia, claiming that the enterprise was supplying missile components. Also on this day, 10 people were killed in a Russian missile attack on the outskirts of the capital Kyiv. Both Ukraine and Russia are intensifying their attacks, raising concerns about the prolonged conflict.",
                "literal": "另一方面，乌克兰总统泽连斯基明确表示攻击了位于俄罗斯中部基洛夫的一家军事企业，并主张该企业供应导弹用零部件等。同一天，首都基辅近郊遭俄军导弹攻击，造成10人死亡。乌克兰和俄罗斯双方都在激化攻击，战争长期化令人担忧。",
                "grammar": "「〜を明らかにした」— 明确表示…。例：攻撃したと明らかにした（明确表示进行了攻击）。\n「〜が懸念されている」— …令人担忧。例：長期化が懸念されている（长期化令人担忧）。",
                "vocab": [
                    ["大統領", "だいとうりょう", "总统"],
                    ["軍事企業", "ぐんじきぎょう", "军工企业"],
                    ["ミサイル", "みさいる", "导弹"],
                    ["激化する", "げきかする", "激化"],
                    ["長期化", "ちょうきか", "长期化"]
                ]
            }
        ]
    },
    {
        "slug": "ro-gun-kitahouryou-ryoukuu",
        "title": "露軍の航空機 北方領土を領空侵犯 日本が厳重抗議",
        "subtitle": "ロシア軍機が北海道・根室半島沖の北方領土上空で領空侵犯。航空自衛隊戦闘機が緊急発進した。",
        "paras": [
            {
                "ja": "ロシア軍の航空機が24日、北海道・根室半島沖の北方領土上空で日本の領空を侵犯した。防衛省によると、ロシア軍機は国後島付近の領空に進入したという。航空自衛隊の戦闘機が緊急発進し、警告を行った。日本政府は外交ルートを通じてロシア側に厳重抗議し、再発防止を求めた。",
                "en": "A Russian military aircraft violated Japan's airspace over the Northern Territories off the Nemuro Peninsula in Hokkaido on the 24th. According to the Defense Ministry, a Russian military aircraft entered Japan's airspace near Kunashiri Island. Air Self-Defense Force fighters scrambled and issued warnings. The Japanese government lodged a strong protest with Russia through diplomatic channels and demanded prevention of recurrence.",
                "literal": "俄罗斯军机24日在北海道根室半岛外海的北方领土上空侵犯了日本领空。据防卫省称，俄罗斯军机进入了国后岛附近的领空。航空自卫队的战斗机紧急起飞并进行了警告。日本政府通过外交渠道向俄方提出严正抗议，并要求防止再次发生。",
                "grammar": "「〜によると」— 据…说。例：防衛省によると（据防卫省称）。\n「〜という」— 据说…。例：進入したという（据说进入了）。\n「〜を通じて」— 通过…。例：外交ルートを通じて（通过外交渠道）。",
                "vocab": [
                    ["領空侵犯", "りょうくうしんぱん", "领空侵犯"],
                    ["北方領土", "ほっぽうりょうど", "北方领土"],
                    ["国後島", "くなしりとう", "国后岛"],
                    ["航空自衛隊", "こうくうじえいたい", "航空自卫队"],
                    ["緊急発進", "きんきゅうはっしん", "紧急起飞"]
                ]
            },
            {
                "ja": "ロシア軍機による領空侵犯は近年増加傾向にあり、2024年度には過去最多を記録している。今回の侵犯を受け、首相官邸は情報収集を強化するよう関係省庁に指示した。外務省は「極めて遺憾であり、強く非難する」とのコメントを発表。ロシア側の意図をめぐっては、最近のウクライナ情勢との関連を指摘する声も出ている。",
                "en": "Airspace violations by Russian military aircraft have been on the rise in recent years, reaching a record high in fiscal 2024. In response to this latest violation, the Prime Minister's Office instructed relevant ministries to strengthen intelligence gathering. The Foreign Ministry issued a statement saying, 'This is extremely regrettable and we strongly condemn it.' Regarding Russia's intentions, some voices point to a connection with the recent situation in Ukraine.",
                "literal": "俄罗斯军机造成的领空侵犯近年来呈增加趋势，2024年度创下了历史最多记录。针对此次侵犯，首相官邸指示相关省厅加强情报收集。外务省发表了「极为遗憾，强烈谴责」的评论。围绕俄方的意图，也有指摘其与最近的乌克兰局势相关的意见。",
                "grammar": "「〜傾向にある」— 有…趋势。例：増加傾向にある（有增加趋势）。\n「〜よう指示した」— 指示…。例：強化するよう指示した（指示加强）。\n「〜をめぐって」— 围绕…。例：意図をめぐって（围绕意图）。",
                "vocab": [
                    ["増加傾向", "ぞうかけいこう", "增加趋势"],
                    ["過去最多", "かこさいとう", "历史最多"],
                    ["情報収集", "じょうほうしゅうしゅう", "情报收集"],
                    ["遺憾", "いかん", "遗憾"],
                    ["非難する", "ひなんする", "谴责、批评"]
                ]
            }
        ]
    },
    {
        "slug": "gaikokujin-eijyu-genkaku",
        "title": "政府が外国人の永住許可要件を厳格化へ 納税義務違反で取消も",
        "subtitle": "政府が外国人の永住許可要件の厳格化案を提示。納税や社会保険料の未納があれば許可取り消しも可能に。",
        "paras": [
            {
                "ja": "政府が外国人の永住許可要件を厳格化する方針を固めたことが明らかになった。新しい制度では、納税や社会保険料の未納があった場合に永住許可を取り消せるようにするほか、許可の申請には安定的な収入や一定以上の日本語能力を求める方向で調整が進められている。",
                "en": "It has been revealed that the government has solidified a policy to tighten the requirements for permanent residency permits for foreigners. Under the new system, the government would be able to revoke permanent residency permits in cases of tax or social insurance premium non-payment, and adjustments are being made toward requiring stable income and a certain level of Japanese language ability for applications.",
                "literal": "政府已明确将强化外国人永住许可条件的方针。在新制度下，除了能够在有纳税或社会保险费未缴纳的情况下取消永住许可外，还在朝着在许可申请时要求稳定的收入和一定以上日语能力的方向进行调整。",
                "grammar": "「〜ことが明らかになった」— …变得明确。例：方針を固めたことが明らかになった（明确了…方针）。\n「〜ほか」— 除了…之外。例：取り消せるようにするほか（除了能够取消之外）。\n「〜方向で調整」— 朝着…方向调整。例：求められる方向で調整（朝着要求…的方向调整）。",
                "vocab": [
                    ["永住許可", "えいじゅうきょか", "永住许可"],
                    ["厳格化", "げんかくか", "严格化"],
                    ["納税", "のうぜい", "纳税"],
                    ["社会保険料", "しゃかいほけんりょう", "社会保险费"],
                    ["取り消す", "とりけす", "取消、撤销"]
                ]
            },
            {
                "ja": "現在、日本では約88万人の外国人が永住許可を持っている。政府は増加する外国人労働者の受け入れ拡大に伴い、制度の適正化が必要と判断した。一方、入管難民法の改正案には慎重な意見もあり、与党内でも調整が続いている。今後、国会で審議される見通しだ。",
                "en": "Currently, approximately 880,000 foreigners hold permanent residency permits in Japan. The government has determined that the system needs to be streamlined as it expands the acceptance of foreign workers. On the other hand, there are cautious opinions about the proposed revisions to the Immigration Control and Refugee Recognition Act, and adjustments continue even within the ruling party. The bill is expected to be deliberated in the Diet going forward.",
                "literal": "目前，日本约有88万外国人持有永住许可。政府判断随着扩大接收不断增加的外国劳动者，需要优化制度。另一方面，对于出入国管理难民法的修正案也存在慎重意见，执政党内也在继续调整。今后预计将在国会上进行审议。",
                "grammar": "「〜に伴い」— 随着…。例：受け入れ拡大に伴い（随着接收扩大）。\n「〜と判断した」— 判断为…。例：必要と判断した（判断为有必要）。\n「〜見通しだ」— 预计是…。例：審議される見通しだ（预计将进行审议）。",
                "vocab": [
                    ["外国人", "がいこくじん", "外国人"],
                    ["労働者", "ろうどうしゃ", "劳动者"],
                    ["入管難民法", "にゅうかんなんみんほう", "出入境管理及难民认定法"],
                    ["改正案", "かいせいあん", "修正案"],
                    ["審議", "しんぎ", "审议"]
                ]
            }
        ]
    },
    {
        "slug": "isha-haikibutsu-iho-taiho",
        "title": "医師の男を廃棄物処理法違反疑いで逮捕 麻酔薬を自身に注射か",
        "subtitle": "医師の男が使用済み注射針などを駅トイレに不法投棄した疑い。麻酔薬を自身に注射し高揚感を得ていた。",
        "paras": [
            {
                "ja": "注射針と麻酔薬入りの瓶を地下鉄の駅の男子トイレなどに捨てたとして、医師の木村光希容疑者（39）が警視庁に逮捕された。廃棄物処理法違反の疑いで、今年3月、注射針8本と麻酔薬入りの瓶を都営新宿線・浜町駅の男子トイレや多目的トイレに捨てたとされている。",
                "en": "Doctor Kimura Koki (39) was arrested by the Tokyo Metropolitan Police on suspicion of illegally disposing of used needles and anesthetic vials in a men's restroom at a subway station. He is suspected of violating the Waste Disposal Act by discarding 8 used needles and anesthetic vials in the men's and multi-purpose restrooms at Hamacho Station on the Toei Shinjuku Line in March this year.",
                "literal": "因将注射针和装有麻醉药的瓶子丢弃在地铁站的男厕等处，医生木村光希嫌疑人（39岁）被警视厅逮捕。涉嫌违反废弃物处理法，今年3月将8根注射针和装麻醉药的瓶子丢弃在都营新宿线滨町站的男厕和多用途厕所。",
                "grammar": "「〜として」— 因为…（理由）。例：捨てたとして（因为丢弃了）。\n「〜疑いで」— 以…嫌疑。例：違反の疑いで（以违反的嫌疑）。\n「〜とされている」— 被认为/被认定为。例：捨てたとされている（被认定为丢弃了）。",
                "vocab": [
                    ["医師", "いし", "医生"],
                    ["注射針", "ちゅうしゃばり", "注射针头"],
                    ["麻酔薬", "ますいやく", "麻醉药"],
                    ["廃棄物", "はいきぶつ", "废弃物"],
                    ["逮捕", "たいほ", "逮捕"]
                ]
            },
            {
                "ja": "当時、木村容疑者はトイレで麻酔薬を自身に注射した後、駅の構内で叫んでいたことから駅員に通報されたという。調べに対し、木村容疑者は「高揚感を得るため麻酔薬を使用していた」と供述する一方、「薬の影響で判断力が低下しており、故意ではない」と述べている。また「認可がおりていない薬を学術研究で使用した」という趣旨の供述もしており、警視庁は余罪についても調べている。",
                "en": "At the time, Kimura allegedly injected himself with anesthetic in the restroom and then shouted inside the station, which led station staff to report him. During questioning, Kimura stated that 'I used anesthetics to get a feeling of euphoria,' while also claiming that 'my judgment was impaired due to the drugs, so it was not intentional.' He also reportedly stated that he 'used unapproved drugs for academic research,' and police are investigating possible additional offenses.",
                "literal": "当时，木村嫌疑人据称在厕所给自己注射了麻醉药后，在车站内大声喊叫，因此被站员通报。面对调查，木村嫌疑人供述「为了获得兴奋感使用了麻醉药」，但同时称「受药物影响判断力下降，并非故意」。此外还供述了「在学术研究中使用了未经批准的药物」，警视厅也在调查其他罪行。",
                "grammar": "「〜ことから」— 因为…。例：叫んでいたことから（因为在大叫）。\n「〜一方」— 一方面…另一方面…。例：供述する一方（一方面供述…）。\n「〜という趣旨」— …内容/大意。例：供述もしている（也做了…内容的供述）。",
                "vocab": [
                    ["容疑者", "ようぎしゃ", "嫌疑人"],
                    ["構内", "こうない", "站内、院内"],
                    ["通報", "つうほう", "通报、报警"],
                    ["高揚感", "こうようかん", "兴奋感、高涨感"],
                    ["故意", "こい", "故意"],
                    ["余罪", "よざい", "其他罪行"]
                ]
            }
        ]
    },
    {
        "slug": "kirishima-nanji-itaibu",
        "title": "霧島市の遺体は行方不明の5歳男児と判明 父親が胸中を語る",
        "subtitle": "鹿児島・霧島市の温泉施設から行方不明となっていた田中嶺臣くんの遺体が700m下流で発見された。",
        "paras": [
            {
                "ja": "鹿児島県霧島市の天降川で先週見つかった遺体の身元について、霧島警察署は先月21日から行方不明となっていた熊本県八代市の保育園児・田中嶺臣くん（5歳）であることが分かったと発表した。警察が司法解剖しDNA型鑑定などを行った結果、遺体が嶺臣くんであることが確認された。死因などについては引き続き捜査中だ。",
                "en": "Regarding the identity of a body found last week in the Amorigawa River in Kirishima City, Kagoshima Prefecture, the Kirishima Police Station announced that it was 5-year-old Tanaka Reomi, a kindergarten child from Yatsushiro City, Kumamoto Prefecture, who had been missing since the 21st of last month. Following a judicial autopsy and DNA analysis, the body was confirmed to be Reomi. The cause of death and other details remain under investigation.",
                "literal": "关于上周在鹿儿岛县雾岛市的天降川发现的遗体身份，雾岛警察署公布，查明是自上月21日起失踪的熊本县八代市保育园儿童田中岭臣君（5岁）。警察进行司法解剖和DNA型鉴定等的结果，确认遗体为岭臣君。死因等正在继续调查中。",
                "grammar": "「〜について」— 关于…。例：身元について（关于身份）。\n「〜ことが分かった」— 判明…。例：男児であることが分かった（判明是男童）。\n「〜結果」— …的结果。例：鑑定などを行った結果（进行鉴定等的结果）。",
                "vocab": [
                    ["遺体", "いたい", "遗体"],
                    ["行方不明", "ゆくえふめい", "下落不明"],
                    ["保育園児", "ほいくえんじ", "保育园儿童"],
                    ["司法解剖", "しほうかいぼう", "司法解剖"],
                    ["死因", "しん", "死因"]
                ]
            },
            {
                "ja": "嶺臣くんは先月21日、家族で訪れた霧島市の温泉施設で入浴中に、両親が目を離した間に浴室からいなくなり行方が分からなくなっていた。施設の浴室からは窓を通じて外に出られる構造で、窓から地面までは約180センチの高さがあり、その後ろには約3メートルの土手と川がある。父親は取材に対し「帰ってきてくれてよかった、生きていてほしかった」と胸中を語った。",
                "en": "Reomi went missing on the 21st of last month while bathing at a hot spring facility in Kirishima City with his family, when his parents looked away and he disappeared from the bathroom. The facility's bathroom had a structure allowing exit through a window, with a height of about 180 cm from the window to the ground, behind which there is a roughly 3-meter embankment and a river. His father told reporters, 'I'm glad you came back, I wish you could have lived,' expressing his heartache.",
                "literal": "岭臣君上个月21日与家人一起到访的雾岛市温泉设施入浴时，在父母视线离开期间从浴室消失，行踪不明。设施浴室的构造可以通过窗户到外面，从窗户到地面约180厘米高，其后有约3米的堤坝和河流。父亲在接受采访时表达了心声：「能回来真是太好了，真希望你还活着」。",
                "grammar": "「〜間に」— 在…期间。例：目を離した間に（在视线移开的期间）。\n「〜構造で」— …的构造。例：出られる構造で（是可以出去的构造）。\n「〜に対し」— 对…、面对…。例：取材に対し（面对采访）。",
                "vocab": [
                    ["温泉施設", "おんせんしせつ", "温泉设施"],
                    ["入浴", "にゅうよく", "入浴"],
                    ["目を離す", "めをはなす", "视线移开"],
                    ["窓", "まど", "窗户"],
                    ["土手", "どて", "堤坝、河岸"],
                    ["胸中", "きょうちゅう", "心中、内心"]
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
# Load existing
index_path = f'{BASE}/assets/readings/index.json'
existing_index = []
if os.path.exists(index_path):
    with open(index_path, 'r') as f:
        existing_index = json.load(f)

# New entries
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

# Prepend new articles to existing
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

# Build new JS list entries (new articles at the top)
js_list = []
for item in new_entries:
    escaped_title = item['title'].replace("'", "\\'")
    js_list.append(f"    {{\n      id: '{item['id']}',\n      title: '{escaped_title}',\n      kicker: '中級',\n      desc: '',\n      badge: '{item['length']}段落',\n      file: '/asanews/assets/readings/{item['id']}.json'\n    }}")

# Also read the existing non-new entries from the current file
# Find the existing entries that aren't the new ones
existing_ids = {a['id'] for a in new_entries}
# Read existing READING_LIST entries that aren't new
existing_entries = []
for item in existing_index:
    if item['id'] not in existing_ids:
        escaped = item['title'].replace("'", "\\'")
        existing_entries.append(f"    {{\n      id: '{item['id']}',\n      title: '{escaped}',\n      kicker: '中級',\n      desc: '',\n      badge: '{item['length']}段落',\n      file: '/asanews/assets/readings/{item['id']}.json'\n    }}")

# Combine
all_js_list = js_list + existing_entries

js_replace = "        const READING_LIST = [\n" + ",\n".join(all_js_list) + "\n    ];"

# Replace in the JS file
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
