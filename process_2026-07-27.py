#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-07-27 (Mon) Edition"""
import json, os, subprocess, time, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-07-27'
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
    with open('/tmp/tts_input.txt', 'w') as f:
        f.write(text)
    r = subprocess.run(['edge-tts', '--voice', 'ja-JP-NanamiNeural',
                        '--text', text, '--write-media', outpath],
                       capture_output=True, timeout=180)
    return os.path.exists(outpath) and os.path.getsize(outpath) > 1000

# ==================================================================
# TODAY'S ARTICLES — 2026-07-27
# ==================================================================
articles = [
    # 1
    {
        "slug": "takaichi-shijiritsu-57",
        "title": "高市内閣支持が急落57％ 首相の説明「不十分」62％",
        "subtitle": "読売新聞の全国世論調査で高市内閣の支持率が57％に急落。物価高への不満と説明不足が影響。",
        "paras": [
            {
                "ja": "読売新聞社が24日から26日にかけて実施した全国世論調査で、高市内閣の支持率は57％と前回調査の69％から急落し、昨年10月の内閣発足以降最低となった。不支持率は21％から34％に上昇した。皇室典範改正など重要な法案や政策についての高市首相の説明不足や、長引く物価高への不満が影響したとみられる。",
                "en": "In a nationwide opinion poll conducted by the Yomiuri Shimbun from the 24th to the 26th, the approval rating for the Takaichi Cabinet plummeted to 57% from 69% in the previous survey, the lowest since the cabinet was formed in October last year. The disapproval rate rose from 21% to 34%. The drop appears to be due to Prime Minister Takaichi's insufficient explanations regarding important bills and policies such as the Imperial House Law revision, and prolonged dissatisfaction with high prices.",
                "literal": "读卖新闻社从24日到26日实施的全国舆论调查显示，高市内阁支持率从前次调查的69%急降至57%，创下去年10月内阁成立以来的最低水平。不支持率从21%上升至34%。据分析，这是由于高市首相对皇室典范修改等重要法案和政策说明不足，以及长期物价高涨的不满所致。",
                "grammar": "「〜にかけて」— 从…到…（时间范围）。例：24日から26日にかけて（从24日到26日）。\n「〜とみられる」— 被认为是…。例：影響したとみられる（被认为受到影响）。\n「〜発足以降」— 成立以来。例：内閣発足以降（内阁成立以来）。",
                "vocab": [
                    ["支持率", "しじりつ", "支持率"],
                    ["急落", "きゅうらく", "急剧下降"],
                    ["世論調査", "よろんちょうさ", "舆论调查"],
                    ["物価高", "ぶっかだか", "物价高涨"],
                    ["皇室典範", "こうしつてんぱん", "皇室典范"]
                ]
            },
            {
                "ja": "調査によると、物価高に対する政府の対応を「評価しない」は71％で前回の56％から15ポイント上昇した。自民党の支持率も31％に下落。無党派層は39％で前回から6ポイント上昇した。皇室典範改正などの重要法案について、首相が国民に十分に説明していると思うかについては「思わない」が62％で、「思う」の29％を大きく上回った。高市首相は国会最終盤で強引な采配を振るい、内閣支持率の下落に歯止めがかからない状況だ。",
                "en": "According to the survey, those who 'do not evaluate' the government's response to high prices reached 71%, up 15 points from 56% in the previous survey. The LDP's approval rating also fell to 31%. Undecided voters rose to 39%, up 6 points. Regarding whether the Prime Minister has sufficiently explained important bills such as the Imperial House Law revision, 62% said 'no,' far exceeding the 29% who said 'yes.' Prime Minister Takaichi wielded forceful tactics at the end of the Diet session, and the decline in the cabinet approval rating shows no signs of stopping.",
                "literal": "调查显示，对政府应对物价高涨「不予评价」的比例为71%，比上次的56%上升了15个百分点。自民党支持率也降至31%。无党派阶层为39%，比上次上升6个百分点。关于首相是否向国民充分说明了皇室典范修改等重要法案，回答「不认为」的占62%，大幅超过「认为」的29%。高市首相在国会最后阶段采取了强行策略，内阁支持率的下滑势头未能遏制。",
                "grammar": "「〜に対する」— 对…的。例：物価高に対する政府の対応（政府对物价高涨的应对）。\n「〜を上回る」— 超过…。例：「思う」の29％を大きく上回った（大幅超过认为的29%）。\n「〜に歯止めがかからない」— 无法控制…。例：下落に歯止めがかからない（下跌无法阻止）。",
                "vocab": [
                    ["評価する", "ひょうかする", "评价"],
                    ["無党派層", "むとうはそう", "无党派阶层"],
                    ["国会", "こっかい", "国会"],
                    ["最終盤", "さいしゅうばん", "最后阶段"],
                    ["采配", "さいはい", "指挥、策略"]
                ]
            }
        ]
    },
    # 2
    {
        "slug": "josei-tennou-younin-81",
        "title": "女性天皇容認に賛成81％ 共同通信世論調査",
        "subtitle": "共同通信の全国電話世論調査で女性天皇を認めることに賛成が81.0％に達した。政府の説明不足が浮き彫りに。",
        "paras": [
            {
                "ja": "共同通信社が25、26両日に行った全国電話世論調査によると、皇族数確保に向けた改正皇室典範に関連し、女性天皇を認めることに賛成が81.0％だった。反対は16.1％だった。政府・与党が今国会で成立させた改正皇室典範は男系男子による皇位継承を維持する内容だが、国民の大多数が女性天皇を容認している実態が改めて明らかになった。",
                "en": "According to a nationwide telephone opinion poll conducted by Kyodo News on the 25th and 26th, 81.0% of respondents approved of allowing a female emperor in connection with the revision of the Imperial House Law to secure the number of imperial family members. Opposition stood at 16.1%. While the revision enacted by the government and ruling party in the current Diet session maintains male-line male succession to the throne, the poll once again revealed that the vast majority of the public accepts a female emperor.",
                "literal": "据共同通信社25、26两日实施的全国电话舆论调查，与为确保皇族人数而修改的皇室典范修正案相关，赞成承认女性天皇的占81.0%。反对占16.1%。政府和执政党在本次国会上通过的皇室典范修正案虽维持男系男子皇位继承的内容，但再次明确了国民大多数认可女性天皇的实际情况。",
                "grammar": "〜両日 — 两天（25日和26日）。例：25、26両日（25日和26日）。\n「〜に関連し」— 与…相关。例：改正皇室典範に関連し（与修改皇室典范相关）。\n「〜が改めて明らかになった」— 再次明确了…。例：実態が改めて明らかになった（再次明确了实际情况）。",
                "vocab": [
                    ["女性天皇", "じょせいてんのう", "女性天皇"],
                    ["容認", "ようにん", "容许、认可"],
                    ["賛成", "さんせい", "赞成"],
                    ["皇族", "こうぞく", "皇族"],
                    ["皇位継承", "こういけいしょう", "皇位继承"]
                ]
            },
            {
                "ja": "政府は今回の国会で、皇族数確保のため、戦後初となる皇族出身男性による養子縁組を認める制度を導入した。しかし、世論の多くは女性天皇や女性宮家の創設を求めているのが実情だ。調査では「皇室に関心がある」と答えた人は72.6％に上った。皇室の将来像をめぐっては、国民的な議論が引き続き必要だと専門家は指摘している。",
                "en": "In the current Diet session, the government introduced a system—the first of its kind in the postwar period—to allow adoption by male descendants of former imperial families to secure the number of imperial family members. However, the reality is that much of public opinion is calling for a female emperor or the creation of female-led imperial branch families. The survey showed that 72.6% of respondents said they are 'interested in the imperial family.' Experts point out that continued national debate is necessary regarding the future shape of the imperial family.",
                "literal": "政府在此次国会中，为确保皇族人数，导入了战后首次的允许出自皇族的男性进行收养的制度。但实际情况是，舆论多数要求女性天皇或创立女性宫家。调查中回答「对皇室感兴趣」的人占72.6%。专家指出，围绕皇室的未来形象，仍需继续进行国民性的讨论。",
                "grammar": "「〜による」— 由…进行的。例：皇族出身男性による養子縁組（由皇族出身的男性进行的收养）。\n「〜をめぐって」— 围绕…。例：将来像をめぐって（围绕未来形象）。\n「〜引き続き必要だ」— 需要继续…。例：議論が引き続き必要だ（讨论需要继续）。",
                "vocab": [
                    ["養子縁組", "ようしえんぐみ", "收养（关系）"],
                    ["宮家", "みやけ", "宫家（皇室分支）"],
                    ["創設", "そうせつ", "创设"],
                    ["世論", "よろん", "舆论"],
                    ["専門家", "せんもんか", "专家"]
                ]
            }
        ]
    },
    # 3
    {
        "slug": "iran-houfuku-kyuushi",
        "title": "イランが報復休止 米軍の攻撃停止受け",
        "subtitle": "イラン軍報道官が国営テレビで、米軍の攻撃停止を受け報復作戦を休止したと発表。中東情勢に一時的な落ち着き。",
        "paras": [
            {
                "ja": "イランは米軍による攻撃停止を受け、報復作戦を休止した。アクラミニア陸軍報道官が26日、国営テレビに明らかにした。報道官は「米国の攻撃は二晩前まで続いていたが、過去二晩は停止した。我々の戦略は基本的に報復的なものであり、我々も報復作戦を休止した」と語った。イランと米国の間ではここ数週間、緊張が急速に高まっていた。",
                "en": "Iran has paused its retaliatory operations following a halt in US military attacks. Army spokesman Aklaminia told state television on the 26th. The spokesman said, 'The US attacks continued until two nights ago, but have stopped for the past two nights. Our strategy is fundamentally retaliatory, so we have also paused our retaliatory operations.' Tensions between Iran and the US had been rapidly escalating over the past several weeks.",
                "literal": "伊朗在接受美军停止攻击后，暂停了报复作战。陆军发言人Aklaminia于26日向国营电视台明确说明了这一点。发言人表示：「美军的攻击持续到两天前为止，但过去两晚已经停止。我们的战略基本是报复性的，因此我们也暂停了报复作战。」伊朗与美国之间在最近数周内紧张局势急速升级。",
                "grammar": "「〜による」— 由…的。例：米軍による攻撃停止（由美军造成的攻击停止）。\n「〜まで続いていた」— 一直持续到…。例：二晩前まで続いていた（持续到两天前）。\n「〜と語った」— 表达了…。例：と語った（如此表述）。",
                "vocab": [
                    ["報復", "ほうふく", "报复"],
                    ["攻撃", "こうげき", "攻击"],
                    ["戦略", "せんりゃく", "战略"],
                    ["緊張", "きんちょう", "紧张"],
                    ["中東情勢", "ちゅうとうじょうせい", "中东局势"]
                ]
            },
            {
                "ja": "アクラミニア報道官はさらに「米国は今後のために他のシナリオを練っているのかもしれないが、今の状況は彼らが望むものではない。地上作戦を実行すれば、脆弱性は確実に増すだろう。我々はあらゆるシナリオに備えている」と警告した。米国が戦争と空爆の継続に固執すれば、戦域は拡大することになろうと述べた。専門家は停戦が長続きするかどうかは不透明だと分析している。",
                "en": "Spokesman Aklaminia further warned, 'The US may be working on other scenarios for the future, but the current situation is not what they want. If they conduct a ground operation, their vulnerabilities will certainly increase. We are prepared for all scenarios.' He stated that if the US insists on continuing war and airstrikes, the theater of conflict would expand. Experts analyze that it remains unclear whether the ceasefire will be sustained.",
                "literal": "Aklaminia发言人进一步警告称：「美国可能在为今后构思其他剧本，但现状并非他们所期望的。如果实施地面作战，脆弱性必将增加。我们已为所有剧本做好准备。」他表明如果美国固执于继续战争和空袭，战域将扩大。专家分析称停战能否持久尚不透明。",
                "grammar": "「〜かもしれない」— 也许…。例：練っているのかもしれない（也许在构思）。\n「〜よう」— 表示意志或推量。例：拡大することになろう（将会扩大吧）。\n「〜かどうか」— 是否…。例：長続きするかどうか（是否持久）。",
                "vocab": [
                    ["シナリオ", "しなりお", "剧本、情景"],
                    ["地上作戦", "ちじょうさくせん", "地面作战"],
                    ["脆弱性", "ぜいじゃくせい", "脆弱性"],
                    ["空爆", "くうばく", "空袭"],
                    ["戦域", "せんいき", "战域、战场区域"]
                ]
            }
        ]
    },
    # 4
    {
        "slug": "toyota-6nen-sekaiichi",
        "title": "豊田章男の5年前の警告は正しかった トヨタが6年連続世界一",
        "subtitle": "EVに出遅れたと批判されたトヨタが世界販売で6年連続首位。内燃機関を手放さなかった戦略が今、評価されている。",
        "paras": [
            {
                "ja": "なぜトヨタは世界販売台数で6年連続首位になれたのか。中国EVは値下げ競争で利益を削り、EVへ急旋回した欧州勢も巨額の費用計上を迫られている。一方、トヨタはかつて「EVに出遅れた」と批判を浴びながら、内燃機関を手放さなかった。豊田章男氏が5年前に語った「敵は炭素であり、内燃機関ではない」という警告は、いまの自動車市場の現実を正確に言い当てている。",
                "en": "Why has Toyota been able to maintain the top spot in global vehicle sales for six consecutive years? Chinese EVs are squeezing profits through price competition, while European manufacturers that made a sharp pivot to EVs are also being forced to book huge costs. Meanwhile, Toyota, once criticized as 'lagging behind in EVs,' never let go of internal combustion engines. The warning that Akio Toyoda made five years ago—'The enemy is carbon, not the internal combustion engine'—has accurately predicted the current reality of the automotive market.",
                "literal": "为什么丰田能在全球销售台数上连续6年位居首位？中国EV通过降价竞争削减了利润，急速转向EV的欧洲厂商也被迫计提巨额费用。另一方面，丰田虽曾遭受「EV落后」的批评，但未放弃内燃机。丰田章男5年前所说的「敌人是碳，不是内燃机」的警告，准确言中了当前汽车市场的现实。",
                "grammar": "「〜ながら」— 虽然…但是…。例：批判を浴びながら（虽受到批评）。\n「〜言い当てている」— 言中、说对了。例：現実を正確に言い当てている（准确言中了现实）。\n「〜迫られている」— 被迫…。例：計上を迫られている（被迫计入）。",
                "vocab": [
                    ["販売台数", "はんばいだいすう", "销售台数"],
                    ["首位", "しゅい", "首位、第一"],
                    ["値下げ競争", "ねさげきょうそう", "降价竞争"],
                    ["内燃機関", "ないねんきかん", "内燃机"],
                    ["電気自動車", "でんきじどうしゃ", "电动汽车（EV）"]
                ]
            },
            {
                "ja": "2026年の世界EV市場では、「何台売れたか」だけでなく「売って儲かるのか」が重視されるようになった。国際エネルギー機関（IEA）の報告によると、世界のEV販売は2025年に2000万台を超え、新車の4台に1台に達した。しかし欧州ではハイブリッド車（HEV）が34.5％と、最も選ばれた動力源となった。価格、航続距離、充電時間、寒冷地性能といった実用的な要素が、環境意識よりも重くなっている。トヨタのハイブリッド戦略は、こうした現実に適合していたと言える。",
                "en": "In the 2026 global EV market, not only 'how many were sold' but also 'whether selling is profitable' has become important. According to a report by the International Energy Agency (IEA), global EV sales exceeded 20 million units in 2025, reaching one in four new cars. However, in Europe, hybrid vehicles (HEVs) became the most chosen powertrain at 34.5%. Practical factors such as price, range, charging time, and cold-weather performance have become more important than environmental awareness. Toyota's hybrid strategy can be said to have fit this reality well.",
                "literal": "在2026年的全球EV市场，「卖了多少台」之外，「卖了能否赚钱」也变得被重视。据国际能源机构（IEA）报告，全球EV销量在2025年超过2000万辆，达到每4辆新车中就有1辆。但在欧洲，混合动力车（HEV）以34.5%成为最受欢迎的动力源。价格、续航距离、充电时间、寒冷地性能等实用因素比环境意识更为重要。可以说丰田的混合动力战略符合了这样的现实。",
                "grammar": "「〜だけでなく」— 不仅…而且…。例：何台売れたかだけでなく（不仅卖了多少钱）。\n「〜によると」— 据…说。例：報告によると（据报告称）。\n「〜と言える」— 可以说…。例：適合していたと言える（可以说是适合的）。",
                "vocab": [
                    ["市場", "しじょう", "市场"],
                    ["重視する", "じゅうしする", "重视"],
                    ["航続距離", "こうぞくきょり", "续航距离"],
                    ["ハイブリッド車", "はいぶりっどしゃ", "混合动力车"],
                    ["実用的", "じつようてき", "实用的"]
                ]
            }
        ]
    },
    # 5
    {
        "slug": "funai-denki-hasan",
        "title": "船井電機が破産 社員が見た「いちばん長い日」",
        "subtitle": "創業73年の名門・船井電機が突然破産。給料日前日に失職を告げられた約2000人の従業員。",
        "paras": [
            {
                "ja": "2024年10月24日、創業73年の名門・船井電機は突如として破産した。グループ全体で約2000人を超える従業員は給料日前日に失職を告げられ、そのニュースは日本中を駆け巡った。社内放送で「社員の方々は本社5階多目的ホールに集まってください」と流れたのは、昼休みが終わって少し経った午後1時過ぎだった。社員たちは新しい経営陣からの説明があるのだろうと考えていた。",
                "en": "On October 24, 2024, Funai Electric, a prestigious company with 73 years of history, suddenly went bankrupt. More than 2,000 employees across the group were told they had lost their jobs the day before payday, and the news spread throughout Japan. The internal announcement saying 'All employees please gather at the 5th floor multipurpose hall at headquarters' came a little after 1:00 PM, shortly after the lunch break ended. Employees thought they would receive an explanation from the new management team.",
                "literal": "2024年10月24日，创业73年的老字号船井电机突然破产。集团全体约2000多名员工在发薪日前一天被告知失业，该新闻传遍全日本。社内广播播放「请员工们到总公司5楼多功能厅集合」时，是午休结束后不久的下午1点过后。员工们本以为新经营层会进行说明。",
                "grammar": "「〜を告げられる」— 被通知…。例：失職を告げられた（被告知失业）。\n「〜だろうと考えていた」— 原以为会…。例：説明があるのだろうと考えていた（原以为会有说明）。\n「〜を駆け巡る」— 传遍…。例：日本中を駆け巡った（传遍全日本）。",
                "vocab": [
                    ["破産", "はさん", "破产"],
                    ["創業", "そうぎょう", "创业"],
                    ["従業員", "じゅうぎょういん", "员工"],
                    ["失職", "しっしょく", "失业"],
                    ["社内放送", "しゃないほうそう", "公司内部广播"]
                ]
            },
            {
                "ja": "多目的ホールに集まった従業員たちの前で、弁護士が「船井電機は本日、破産が申請され、即日裁判所から破産開始決定が下された。明日の給料は支払えない」と告げた。ホールは不思議なほど静かだった。生活基盤の消失を宣告されても、取り乱す者はいなかった。従業員らには一枚の書類が配られ、署名するように言われた。拒否する者は誰もいなかったという。その後、社員証を返却し、私物を整理して帰宅するよう命じられた。",
                "en": "In front of the employees gathered in the multipurpose hall, a lawyer announced: 'Funai Electric has filed for bankruptcy today, and the court has issued an immediate order to commence bankruptcy proceedings. Tomorrow's salary cannot be paid.' The hall was eerily silent. Even though they had been told their livelihoods were gone, no one panicked. Employees were handed a document and told to sign it. It is said that no one refused. Afterwards, they were instructed to return their employee ID cards, pack their belongings, and go home.",
                "literal": "在聚集在多功能厅的员工面前，律师宣告：「船井电机本日已申请破产，法院即日下达了破产开始决定。明天的工资无法支付。」大厅异常安静。即使被告知生活基础消失，也没有人慌乱。员工每人领到一份文件并被要求签名。据说没有人拒绝。之后被命令归还员工证，整理私物后回家。",
                "grammar": "「〜が下される」— 被下达…。例：決定が下された（下达了决定）。\n「〜ように言われた」— 被要求…。例：署名するように言われた（被要求签名）。\n「〜という」— 据说…。例：誰もいなかったという（据说没有一个人）。",
                "vocab": [
                    ["弁護士", "べんごし", "律师"],
                    ["申請", "しんせい", "申请"],
                    ["給料", "きゅうりょう", "工资"],
                    ["支払う", "しはらう", "支付"],
                    ["署名", "しょめい", "签名"]
                ]
            },
            {
                "ja": "元社員の山崎さん（仮名）は「歩きながら胸に去来したのは、妻と子どもとの生活のこと、そして、こんな状況を招いた上田社長に対する恨みだった」と振り返る。船井電機は経営危機の中で新しい経営陣に委ねられたが、上田社長の経営手腕がむしろ破産を早めたとされている。この破産は「令和のイトマン事件」とも呼ばれ、日本社会に大きな衝撃を与えた。多くの従業員が突如として職を失い、その後の再就職先探しにも苦労したという。",
                "en": "Former employee Yamazaki (a pseudonym) recalls, 'As I walked, what came to mind was my wife and children's livelihood, and resentment toward President Ueda for bringing about this situation.' Funai Electric had been entrusted to new management amid a management crisis, but President Ueda's management skills are said to have actually hastened the bankruptcy. This bankruptcy has been called the 'Reiwa-era Itoman Incident' and sent shockwaves through Japanese society. Many employees suddenly lost their jobs and reportedly struggled to find new employment afterward.",
                "literal": "原员工山崎（化名）回顾说：「边走边在脑海中浮现的是妻子和孩子的生活，以及对招致这种局面的上田社长的怨恨。」船井电机在经营危机中委托给了新的经营层，但据说上田社长的经营手腕反而加速了破产。这起破产被称为「令和的伊藤万事件」，给日本社会带来了巨大冲击。许多员工突然失去工作，据说之后的再就业也很困难。",
                "grammar": "「〜と振り返る」— 回顾说…。例：と振り返る（回顾道）。\n「〜とされている」— 被认为是…。例：早めたとされている（被认为加速了）。\n「〜と呼ばれる」— 被称为…。例：「令和のイトマン事件」とも呼ばれる（也被称为「令和的伊藤万事件」）。",
                "vocab": [
                    ["仮名", "かめい", "化名、假名"],
                    ["経営危機", "けいえいきき", "经营危机"],
                    ["経営手腕", "けいえいしゅわん", "经营手腕"],
                    ["衝撃", "しょうげき", "冲击"],
                    ["再就職", "さいしゅうしょく", "再就业"]
                ]
            }
        ]
    },
    # 6
    {
        "slug": "squeeze-ryuukou",
        "title": "「スクイーズ」なぜ流行？ 専門家が明かす4つの理由",
        "subtitle": "子どもたちを虜にするスクイーズ。ストレス研究の専門家が人気の秘密を分析。",
        "paras": [
            {
                "ja": "ウレタンやシリコンなどの柔らかい素材でできた「スクイーズ」が子どもたちの間で大きなブームとなっている。握ったり押したりするとゆっくりと元の形に戻るのが特徴で、その独特の感触と見た目がSNSでも話題を呼んでいる。富山市の小学2年生の女の子は「スクイーズがないと生きていけない」と話し、机の上には約70個ものスクイーズが並べられていた。",
                "en": "'Squeeze' toys made of soft materials like urethane and silicone have become a huge boom among children. Characterized by slowly returning to their original shape when squeezed or pressed, their unique texture and appearance have become a hot topic on social media. A second-grade girl in Toyama City says, 'I can't live without squeeze toys,' and had about 70 of them lined up on her desk.",
                "literal": "由聚氨酯和硅胶等柔软材料制成的「挤压玩具」在孩子们之间掀起了巨大热潮。其特征是握紧或按下后会慢慢恢复原形，其独特的触感和外观也在SNS上引发话题。富山市的一名小学二年级女生说「没有挤压玩具就活不下去」，她的桌子上摆放着约70个挤压玩具。",
                "grammar": "「〜でできた」— 由…制成的。例：素材でできた（由材料制成的）。\n「〜という」— 表示内容。例：「生きていけない」と話す（说「活不下去」）。\n「〜約〜もの」— 大约…之多。例：約70個もの（约70个之多）。",
                "vocab": [
                    ["スクイーズ", "すくいーず", "挤压玩具、慢回弹玩具"],
                    ["ブーム", "ぶーむ", "热潮、流行"],
                    ["握る", "にぎる", "握"],
                    ["感触", "かんしょく", "触感"],
                    ["SNS", "えすえぬえす", "社交网络"]
                ]
            },
            {
                "ja": "明治大学の堀田秀吾教授はストレスや行動習慣の専門家で、今年上半期のベストセラー本の著者でもある。堀田教授はスクイーズ人気の理由として4つの要素を挙げている。1つ目は「安心感」。モチモチした感触が人間の肌の感触に近く、幼い頃の母親などを無意識に連想させる。2つ目は「癒やし」。ゆっくりと元に戻る動きそのものが心を落ち着かせる。3つ目は「刺激」。デジタルが優勢の現代では、手で直接触れるアナログ体験が新鮮に映る。4つ目は「ストレス解消」。実際に「嫌なことが安心に変わる」と話す子どももいるという。",
                "en": "Professor Shugo Hotta of Meiji University is an expert on stress and behavioral habits, and the author of a best-selling book from the first half of this year. Professor Hotta cites four factors behind the popularity of squeeze toys. First is 'comfort' — the squishy texture is similar to human skin, unconsciously evoking memories of one's mother from childhood. Second is 'healing' — the slow return to shape itself calms the mind. Third is 'stimulation' — in a digital-dominated era, the analog experience of direct touch feels novel. Fourth is 'stress relief' — some children say that 'worry turns into peace of mind.'",
                "literal": "明治大学的堀田秀吾教授是压力和行动习惯的专家，也是今年上半年畅销书的作者。堀田教授列举了挤压玩具人气的4个理由。第一是「安心感」，松软有弹性的触感接近人类皮肤的触感，会让人无意识地联想到幼时的母亲等。第二是「治愈」，慢慢恢复原状的动作本身能让人心情平静。第三是「刺激」，在数字化占优势的现代，手直接触摸的模拟体验反而显得新鲜。第四是「解压」，实际上也有孩子说「讨厌的事会变成安心」。",
                "grammar": "「〜として」— 作为…。例：理由として（作为理由）。\n「〜に近い」— 接近于…。例：感触に近い（接近于…的触感）。\n「〜という」— 据说…。例：子どももいるという（据说也有孩子）。",
                "vocab": [
                    ["専門家", "せんもんか", "专家"],
                    ["安心感", "あんしんかん", "安心感"],
                    ["癒やし", "いやし", "治愈"],
                    ["アナログ", "あなろぐ", "模拟（非数字）"],
                    ["ストレス", "すとれす", "压力"]
                ]
            }
        ]
    },
    # 7
    {
        "slug": "fujisan-taiwan-josei",
        "title": "富士登山中の台湾女性 山頂で突然意識失う",
        "subtitle": "台湾籍の57歳女性が富士山頂で休憩中に意識を失い、山岳遭難救助隊が救助にあたった。",
        "paras": [
            {
                "ja": "富士登山をして山頂で休憩していた台湾の57歳の女性が突然意識を失いました。警察によりますと、26日午後6時前、姉妹3人でツアーに参加し富士登山をしていた台湾籍の女性が山頂で休憩していたところ、突然意識を失いました。このため山小屋の従業員が110番通報し、警察の山岳遭難救助隊が救助活動にあたりました。午後10時半現在、女性はブルドーザーでふもとへ搬送中だということです。",
                "en": "A 57-year-old Taiwanese woman who was resting at the summit of Mount Fuji after climbing suddenly lost consciousness. According to police, just before 6:00 PM on the 26th, the woman—who was climbing Fuji with her two sisters as part of a tour—suddenly collapsed while resting at the summit. A mountain hut employee called 110 (emergency), and the police mountain rescue team responded. As of 10:30 PM, the woman was being transported down the mountain by bulldozer.",
                "literal": "登富士山并在山顶休息的一名台湾57岁女性突然失去了意识。据警方称，26日下午6点前，该台湾籍女性与姐妹3人参加旅行团登富士山，在山顶休息时突然失去意识。为此，山间小屋的员工拨打110报警，警方的山岳遇难救助队进行了救助活动。截至晚上10点半，该女性正在用推土机被运送到山脚下。",
                "grammar": "「〜によりますと」— 据…说（礼貌）。例：警察によりますと（据警方称）。\n「〜ていたところ」— 正在…的时候。例：休憩していたところ（正在休息的时候）。\n「〜ということです」— 据说/听说。例：搬送中だということです（据说正在运送中）。",
                "vocab": [
                    ["富士登山", "ふじとざん", "登富士山"],
                    ["山頂", "さんちょう", "山顶"],
                    ["意識を失う", "いしきをうしなう", "失去意识"],
                    ["山岳遭難", "さんがくそうなん", "山难、山岳遇难"],
                    ["救助隊", "きゅうじょたい", "救助队"]
                ]
            },
            {
                "ja": "警察は登山の際には装備や体調を万全に準備し、少しでも体調や天候等に不安を感じた場合は登山を中止するよう呼びかけています。富士山は夏山シーズンを迎えており、多くの登山客でにぎわっています。しかし高山病や転倒などの事故も相次いでおり、安全な登山のための注意喚起が行われています。専門家は特に十分な休憩と水分補給の重要性を指摘しています。",
                "en": "Police are calling on climbers to thoroughly prepare their equipment and physical condition before climbing, and to cancel their climb if they feel even slightly unwell or concerned about the weather. Mount Fuji has entered its summer climbing season and is crowded with many climbers. However, accidents such as altitude sickness and falls are occurring one after another, and warnings for safe climbing are being issued. Experts particularly emphasize the importance of adequate rest and hydration.",
                "literal": "警方呼吁登山时充分准备装备和身体状况，稍感身体不适或对天气等感到不安时中止登山。富士山已进入夏季登山季节，众多登山客熙熙攘攘。但高山病和跌倒等事故也相继发生，正在进行安全登山的提醒呼吁。专家尤其指出了充分休息和补充水分的重要性。",
                "grammar": "「〜よう呼びかけています」— 呼吁…。例：中止するよう呼びかけています（呼吁中止）。\n「〜を迎えている」— 迎来…。例：夏山シーズンを迎えている（迎来夏季登山季节）。\n「〜が相次ぐ」— 相继发生…。例：事故も相次いでいる（事故也相继发生）。",
                "vocab": [
                    ["装備", "そうび", "装备"],
                    ["体調", "たいちょう", "身体状态"],
                    ["高山病", "こうざんびょう", "高山病"],
                    ["注意喚起", "ちゅういかんき", "提醒呼吁"],
                    ["水分補給", "すいぶんほきゅう", "补充水分"]
                ]
            }
        ]
    },
    # 8
    {
        "slug": "taifuu-nettaiteikiatsu",
        "title": "新たな熱帯低気圧が台風に発達か 今後の進路に注意",
        "subtitle": "台風12号に続き、新たな熱帯低気圧が発生し台風に発達する見込み。日本への影響が懸念される。",
        "paras": [
            {
                "ja": "気象庁の発表によると、新たな熱帯低気圧が発生し、28日までに台風に発達する見込みであることが分かった。台風12号「ノウル」が南シナ海で強い勢力を保ちながら中国華南に接近しているのに続き、新たな渦が日本の南の海上で発生している。気象予報士によると、この熱帯低気圧は今後発達しながら西寄りに進み、日本の南の海上で台風になる可能性が高いという。",
                "en": "According to the Japan Meteorological Agency, a new tropical depression has formed and is expected to develop into a typhoon by the 28th. Following Typhoon No. 12 'Noul,' which is approaching southern China while maintaining strong intensity in the South China Sea, a new vortex has formed over the seas south of Japan. According to weather forecasters, this tropical depression is likely to develop while moving westward and become a typhoon over the seas south of Japan.",
                "literal": "据气象厅发布，已发现新的热带低气压发生，预计到28日前将发展成台风。继台风第12号「诺尔」在南中国海保持强劲势力接近中国华南之后，日本南方的海上出现了新的涡旋。据气象预报员称，这个热带低气压今后将一边发展一边向西移动，在日本南方的海上变成台风的可能性很高。",
                "grammar": "「〜による」— 据…。例：気象庁の発表によると（据气象厅发布）。\n「〜ことが分かった」— 得知…。例：発達する見込みであることが分かった（得知预计会发展）。\n「〜可能性が高い」— …的可能性很高。例：台風になる可能性が高い（变成台风的可能性很高）。",
                "vocab": [
                    ["熱帯低気圧", "ねったいていきあつ", "热带低气压"],
                    ["台風", "たいふう", "台风"],
                    ["発達する", "はったつする", "发展、增强"],
                    ["進路", "しんろ", "路径"],
                    ["気象庁", "きしょうちょう", "气象厅"]
                ]
            },
            {
                "ja": "台風12号は26日午前6時現在、南シナ海を時速30キロで西北西へ進んでいる。最大瞬間風速50メートルまで発達して華南沿岸に達する予想だ。一方、日本の南で発生した熱帯低気圧は今後、日本の南の海上で台風に変わった場合、今後の進路によっては日本列島への接近も考えられる。気象庁は今後の台風情報に注意するよう呼びかけている。8月6日にかけての雨・風シミュレーションでは、週末にかけて全国的に天候が不安定になる可能性が示唆されている。",
                "en": "As of 6:00 AM on the 26th, Typhoon No. 12 is moving west-northwest across the South China Sea at 30 km/h. It is forecast to develop to maximum instantaneous wind speeds of 50 m/s as it reaches the South China coast. Meanwhile, if the tropical depression that formed south of Japan develops into a typhoon over the seas south of Japan, it could approach the Japanese archipelago depending on its future path. The JMA is calling for attention to future typhoon information. Rainfall and wind simulations through August 6 suggest that weather nationwide could become unstable toward the weekend.",
                "literal": "台风第12号26日上午6点现在，以时速30公里向西北西方向在南中国海前进。预计将发展至最大瞬间风速50米/秒，到达华南沿岸。另一方面，日本南方发生的热带低气压今后如果在日本南方的海上变成台风的化，根据今后路径也可能接近日本列岛。气象厅呼吁注意今后台风信息。截至8月6日的雨・风模拟显示，到周末前后全国天气可能变得不稳定。",
                "grammar": "「〜現在」— 截止…时点。例：午前6時現在（截止上午6点）。\n「〜によっては」— 根据…不同。例：進路によっては（根据路径的不同）。\n「〜にかけて」— 到…为止（时间）。例：8月6日にかけて（到8月6日为止）。",
                "vocab": [
                    ["時速", "じそく", "时速"],
                    ["最大瞬間風速", "さいだいしゅんかんふうそく", "最大瞬间风速"],
                    ["華南", "かなん", "华南"],
                    ["日本列島", "にほんれっとう", "日本列岛"],
                    ["天候", "てんこう", "天气"]
                ]
            }
        ]
    },
    # 9
    {
        "slug": "takaichi-tsuyoki-kokkai",
        "title": "高市首相 強気貫く国会運営 自民重鎮「いつかしっぺ返し」",
        "subtitle": "副首都法案を成立させた高市首相の強引な国会運営。身内からも異論が出る中、内閣支持率は下落傾向。",
        "paras": [
            {
                "ja": "事実上の国会会期末を迎えた24日、膠着状態の「副首都」構想関連法案を成立させるべく、高市早苗首相は策を仕込んでいた。複数の関係者によると、首相は憲法59条が定める「60日ルール」を使うことを真剣に検討した。これは衆院で可決した法案を参院が60日以内に議決しないときは否決とみなし、衆院の3分の2以上の賛成で再可決を可能とするものだ。首相は「野党が採決に応じないなら、会期を65日でも70日でも再延長すればいい」と周囲に語っていたという。",
                "en": "On the 24th, effectively the end of the Diet session, Prime Minister Takaichi had prepared strategies to push through the stalled 'sub-capital' related bills. According to multiple sources, the Prime Minister seriously considered using the '60-day rule' stipulated in Article 59 of the Constitution. This rule allows a bill passed by the House of Representatives to be considered rejected if the House of Councillors does not vote on it within 60 days, and then enables it to be re-passed by a two-thirds majority in the lower house. The Prime Minister reportedly told those around her, 'If the opposition doesn't agree to vote, we can just extend the session to 65 or even 70 days.'",
                "literal": "在事实上的国会会期末的24日，为了通过陷入僵局的「副首都」构想相关法案，高市早苗首相准备了策略。据多名相关人士称，首相认真探讨了运用宪法第59条规定的「60天规则」。这是指在众议院通过的法案如果参议院在60天内未表决则视为否决，可通过众议院三分之二以上赞成再次通过。据说首相曾向周围表示：「如果野党不答应表决，将会期再延长到65天甚至70天就可以了。」",
                "grammar": "「〜べく」— 为了…。例：成立させるべく（为了使其成立）。\n「〜ものだ」— 表示性质/规则。例：再可決を可能とするものだ（是使再次表决成为可能的规则）。\n「〜という」— 据说…。例：語っていたという（据说曾说过）。",
                "vocab": [
                    ["国会会期末", "こっかいかいきまつ", "国会会期结束"],
                    ["膠着状態", "こうちゃくじょうたい", "胶着状态、僵局"],
                    ["副首都", "ふくしゅと", "副首都"],
                    ["採決", "さいけつ", "表决"],
                    ["再可決", "さいかけつ", "再次通过"]
                ]
            },
            {
                "ja": "しかし、維新の意向を優先して再可決に踏み切れば、首相の強引さが露骨になる。自民内でも「あまりにも禍根を残す」などと異論が出ていた。こうした声にも首相は「憲法が認めた権利なのに、なんで駄目なん？」と反論。腹心の政府高官から「野党だけでなく参院自民も敵に回す」と説得され、矛を収めたものの、国会最終盤まで続く野党の反対に対しては「堪忍袋の緒が切れた」という。結局、与党側が野党に譲歩する形で決着した。独善的な国会運営が目立った首相に対し、自民重鎮は強気を貫く手法にくぎを刺した。「こんな乱暴なやり方が何度も通じるわけがない。いつかしっぺ返しがくる」と警告している。",
                "en": "However, if she had pushed through with re-passage by prioritizing Ishin's wishes, the Prime Minister's heavy-handedness would have been blatant. Even within the LDP, there were dissenting voices saying it would 'leave too much resentment.' To these voices, the Prime Minister retorted, 'It's a right recognized by the Constitution, so why is it no good?' She was persuaded by a close government official that she would 'make enemies not only of the opposition but also of LDP members in the House of Councillors,' and she temporarily backed down. But as opposition continued into the final stage of the Diet, 'her patience finally ran out.' The matter was ultimately resolved through concessions from the ruling party to the opposition. Regarding the Prime Minister's conspicuously self-righteous Diet management, a senior LDP figure issued a warning against her persistently tough approach: 'There's no way such rough methods will work every time. Someday the backlash will come.'",
                "literal": "但若优先维新会的意向强行再次表决，首相的强行作风将暴露无遗。自民党内也出现了「留下太多祸根」等异议。对于这些声音，首相反驳道：「这是宪法承认的权利，为什么不行？」被心腹的政府高官说服「不仅树敌在野党，连参院自民也会对立」，暂时收敛了锋芒，但对于持续到国会最后阶段的在野党的反对，「忍耐的绳子断了」。结果以执政党向在野党让步的形式收场。对于独善的国会运营引人注目的首相，自民党元老给强硬的作风敲了警钟：「这种粗暴的做法不可能每次都行得通。总有一天会遭到报应。」",
                "grammar": "「〜に踏み切れば」— 如果毅然实行…。例：再可決に踏み切れば（如果强行再次表决）。\n「〜ものの」— 虽然…但是…。例：矛を収めたものの（虽然收敛了锋芒）。\n「〜わけがない」— 不可能…。例：通じるわけがない（不可能行得通）。",
                "vocab": [
                    ["異論", "いろん", "异议"],
                    ["禍根", "かこん", "祸根"],
                    ["腹心", "ふくしん", "心腹"],
                    ["説得する", "せっとくする", "说服"],
                    ["堪忍袋の緒が切れる", "かんにんぶくろのおがきれる", "忍无可忍"]
                ]
            }
        ]
    },
    # 10
    {
        "slug": "topnews-pickup-0727",
        "title": "今日の注目ニュースピックアップ（7月27日）",
        "subtitle": "JR広島駅で新幹線接触事故、千葉で正面衝突死亡事故。今日のニュースをコンパクトにまとめました。",
        "paras": [
            {
                "ja": "JR広島駅で26日夜、山陽新幹線がホームの柵を乗り越えたとみられる30代の男性と接触する事故があった。この事故で男性は重傷を負い、岡山駅と博多駅の間で一時運転が見合わせられた。駅員の通報で駆け付けた警察が詳しい状況を調べている。新幹線の安全運行に影響が出たことから、JR西日本は安全対策の徹底を呼びかけている。",
                "en": "On the night of the 26th, a Shinkansen train at JR Hiroshima Station struck a man in his 30s who apparently climbed over the platform fence. The man was seriously injured, and operations were temporarily suspended between Okayama and Hakata stations. Police who arrived following a station employee's report are investigating the details. As the incident affected the safe operation of the Shinkansen, JR West is calling for thorough safety measures.",
                "literal": "26日晚在JR广岛站，山阳新干线发生了与疑似越过月台栅栏的30多岁男性接触的事故。该事故导致该男性受重伤，冈山站与博多站之间一度暂停运行。接到站员通报后赶到的警方正在调查详细情况。由于对新型干线的安全运行产生了影响，JR西日本呼吁彻底落实安全对策。",
                "grammar": "「〜とみられる」— 被认为…。例：乗り越えたとみられる（被认为是越过了）。\n「〜ことから」— 因为…。例：影響が出たことから（因为产生了影响）。\n「〜ている」— 正在…。例：調べている（正在调查）。",
                "vocab": [
                    ["新幹線", "しんかんせん", "新干线"],
                    ["接触", "せっしょく", "接触、碰撞"],
                    ["柵", "さく", "栅栏"],
                    ["運転見合わせ", "うんてんみあわせ", "暂停运行"],
                    ["安全対策", "あんぜんたいさく", "安全对策"]
                ]
            },
            {
                "ja": "また、千葉県内の国道で26日夜、乗用車同士が正面衝突する事故が発生した。この事故で千葉県の男性1人が死亡、埼玉県の4人家族が重軽傷を負った。警察は事故の原因を詳しく調べている。連日の暑さによる体調変化や路面状況の悪化も影響した可能性があるとして、ドライバーに注意を呼びかけている。",
                "en": "Also on the night of the 26th, a head-on collision between two passenger cars occurred on a national highway in Chiba Prefecture. One man from Chiba died, and a family of four from Saitama Prefecture suffered serious and minor injuries. Police are investigating the cause of the accident. The authorities are calling on drivers to be careful, noting that changes in physical condition due to the continued heat and deteriorating road conditions may have been contributing factors.",
                "literal": "此外，26日晚在千叶县内的国道上，发生了轿车正面相撞的事故事故。该事故导致千叶县1名男性死亡，埼玉县的4人家庭受轻重伤。警方正在详细调查事故原因。由于连日暑热导致的身体状态变化和路面状况恶化也可能是影响因素，警方呼吁驾驶者注意。",
                "grammar": "「〜同士」— 相互之间。例：乗用車同士（轿车之间）。\n「〜として」— 作为…。例：可能性があるとして（作为有可能）。\n「〜ている」— 正在…。例：調べている（正在调查）。",
                "vocab": [
                    ["正面衝突", "しょうめんしょうとつ", "正面相撞"],
                    ["乗用車", "じょうようしゃ", "轿车"],
                    ["死亡", "しぼう", "死亡"],
                    ["重軽傷", "じゅうけいしょう", "轻重伤"],
                    ["路面状況", "ろめんじょうきょう", "路面状况"]
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
        print(f"  {status} {slug:40s} | {pc} paras")
        ok += 1
    else:
        print(f"  ❌ {slug} MISSING!")

print(f"\n🎉 {ok}/{len(processed)} articles processed successfully!")
print(f"{'='*60}")
