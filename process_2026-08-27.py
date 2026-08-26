#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-27 (Thu) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-27'
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
        "slug": "guguru-enjinia-kaiko",
        "title": "年収1470万のGoogleエンジニアが突然クビに…高評価の翌月に一転「著しく不良」とされたワケ",
        "subtitle": "from 弁護士JPニュース",
        "paras": [
            {
                "ja": "10年以上にわたって昇格を重ね、職位を駆け上がってきた——。そんなGoogle日本法人のソフトウェアエンジニアが、ある日突然、勤務状態が“著しく不良”だとして職を追われた。解雇の決め手とされたのは、「職位L5レベルのリーダーシップを発揮すべき」という抽象的な表現により設定された「目標」の“未達”である。年収は1470万円で、解雇直前の評価では「重大な影響」と高く評価されていた。外国籍の30代元社員は解雇の無効などを求め、グーグル合同会社を東京地裁に提訴した。",
                "en": "An engineer at Google Japan who had been repeatedly promoted and climbed the ranks over more than 10 years was suddenly dismissed one day on the grounds that his work condition was \"markedly poor.\" The decisive factor for the dismissal was the \"failure to achieve\" a \"goal\" set through the abstract expression \"should demonstrate leadership at L5 level.\" His annual income was 14.7 million yen, and in his evaluation just before the dismissal he was highly rated as having had a \"major impact.\" A former employee in his 30s of foreign nationality sued Google LLC in the Tokyo District Court seeking to invalidate the dismissal.",
                "literal": "经历了10年以上不断晋升、在职位上步步高升——。这样的谷歌日本法人的软件工程师，某一天突然因工作状态“显著不良”而被解雇。成为解雇决定依据的，是根据「应发挥L5级别职位的领导力」这种抽象表述所设定的「目标」的“未达成”。年收入1470万日元，解雇前不久的评估中还因「重大影响」而获得高度评价。外籍30多岁的前员工为争取解雇无效等，向东京地方法院起诉了谷歌合同会社。",
                "grammar": "「〜にわたって」— 持续…、历经…。例：10年以上にわたって昇格を重ね（历经10年以上不断晋升）。\n「〜として〜された」— 被当作…。例：決め手とされた（被当作决定因素）。\n「〜をめぐって」— 围绕…（此处指诉诸法院）。例：無効などを求め、提訴した（要求无效等，提起诉讼）。",
                "vocab": [["昇格", "しょうかく", "晋升"], ["職位", "しょくい", "职位"], ["十分に", "じゅうぶんに", "充分地"], ["著しく", "いちじるしく", "显著地"], ["解雇", "かいこ", "解雇"], ["提訴", "ていそ", "提起诉讼"], ["無効", "むこう", "无效"]]
            },
            {
                "ja": "元社員のAさんは2014年、L3と呼ばれる職位で入社した。フロントエンドのエンジニアとして誠実に業務をこなし、2023年までにL5へと昇格。入社時に750万円だった年収は、解雇時点で1470万円に達していた。一方でAさんは病気により2度の休業を余儀なくされたが、復帰後も指示された業務をこなし、2025年9月の評価面談では「堅実で信頼できるチームメイト」「成長軌道に乗っている」と高い評価を得ていた。",
                "en": "Mr. A, the former employee, joined the company in 2014 at a rank called L3. Working diligently as a front-end engineer, he was promoted to L5 by 2023. His annual income, which was 7.5 million yen when he joined, had reached 14.7 million yen at the time of the dismissal. Meanwhile, Mr. A was forced to take leave twice due to illness, but after returning he continued to carry out assigned work, and in a September 2025 evaluation interview received high marks such as \"a steady, reliable teammate\" and \"on a growth trajectory.\"",
                "literal": "前员工A先生2014年以被称为L3的职位入职。作为前端工程师认真处理业务，到2023年升为L5。入职时750万日元的年收入，到解雇时已达到1470万日元。另一方面，A先生因病被迫两次停业，但复职后仍完成被指派的工作，在2025年9月的评估面谈中获得了「扎实可靠、值得信赖的队友」「处于成长轨道」的高度评价。",
                "grammar": "「〜と呼ばれる」— 被称为…。例：L3と呼ばれる職位（被称为L3的职位）。\n「〜を余儀なくされた」— 被迫…、不得不…。例：休業を余儀なくされた（被迫停业）。\n「〜に乗っている」— 处于…（轨道）上。例：成長軌道に乗っている（处于成长轨道）。",
                "vocab": [["誠実に", "せいじつに", "诚实地、认真"], ["業務", "ぎょうむ", "业务"], ["休業", "きゅうぎょう", "停业、休息"], ["評価面談", "ひょうかめんだん", "评估面谈"], ["堅実", "けんじつ", "扎实、稳健"], ["成長軌道", "せいちょうきどう", "成长轨道"]]
            },
            {
                "ja": "ところが評価の約1か月後、Aさんは突如PIP（業務改善プログラム）の対象に指定される。PIPとは、成績や勤務状態が不十分とされた社員に一定期間で改善を求める制度だ。同様の日、人事担当者からはMSA（相互退職合意）と呼ばれる退職パッケージが提示され、断ると、これまで経験のないサーバーサイドの業務など4つのタスクが課されたという。Aさんは3回にわたり退職勧奨を受けた。その後、PIP「不達成」を理由に解雇を通告され、社内システムへのアクセス権も一方的に奪われた。Aさんは労働組合に加入し、解雇の撤回と団体交渉を求めたが、会社側は応じないまま解雇を強行したとしている。",
                "en": "However, about a month after the evaluation, Mr. A was suddenly designated as a subject of a PIP (performance improvement plan). A PIP is a system that requires employees deemed to have insufficient performance or work condition to improve within a set period. On the same day, HR offered him a severance package called an MSA (mutual separation agreement), and when he refused, he was reportedly assigned four tasks, including server-side work he had never done before. Mr. A received workplace separation recommendations three times. He was subsequently notified of dismissal on the grounds of \"failure to complete the PIP,\" and his access rights to the company's internal systems were unilaterally taken away. Mr. A joined a labor union and sought revocation of the dismissal and collective bargaining, but the company carried out the dismissal without acceding.",
                "literal": "然而，在评估约1个月后，A先生突然被指定为PIP（业务改善项目）的对象。PIP是指要求被认定成绩或工作状态不充分的员工在固定期限内改善的制度。同一天，人事负责人提出了被称为MSA（双方协商离职）的离职套餐，拒绝后，据说被安排了此前没有经验的服务器端业务等4项任务。A先生3次受到劝退。之后，以PIP「未达成」为由被通知解雇，公司内部系统的访问权限也被单方面剥夺。A先生加入工会，要求撤回解雇并进行团体交涉，但公司在不应答的情况下强行解雇。",
                "grammar": "「〜とされる」— 被认定…。例：不十分とされた社員（被认定不充分的员工）。\n「〜にわたり」— 达…次、历经…。例：3回にわたり退職勧奨を受けた（3次受到劝退）。\n「〜まま」— 保持…状态、未…就。例：応じないまま解雇を強行した（在不应答的情况下强行解雇）。",
                "vocab": [["突如", "とつじょ", "突然"], ["業務改善", "ぎょうむかいぜん", "业务改善"], ["人事担当者", "じんじたんとうしゃ", "人事负责人"], ["退職勧奨", "たいしょくかんしょう", "劝退、劝导离职"], ["撤回", "てっかい", "撤回"], ["団体交渉", "だんたいこうしょう", "团体交涉"]]
            },
        ]
    },
    {
        "slug": "seikatsudouro-30kiro",
        "title": "一発免停も…9月1日から生活道路の法定速度60キロから30キロへ",
        "subtitle": "from テレビ朝日系（ANN）",
        "paras": [
            {
                "ja": "来月1日から、生活道路での法定速度が時速60キロから30キロに引き下げられます。一発免停もあり得るという今回の引き下げ。なぜ速度を半分に規制するのでしょうか。住宅街の生活道路では、子どもが飛び出したり、車同士が接触したりする危険な場面が相次いでいます。",
                "en": "From the 1st of next month, the legal speed limit on residential roads will be lowered from 60 km/h to 30 km/h. This is a reduction that could even result in immediate license suspension. Why regulate the speed down to half? On residential roads in housing areas, dangerous situations are occurring one after another, such as children darting out and cars colliding with each other.",
                "literal": "从下月1日起，生活道路上的法定时速将从60公里下调至30公里。这是可能直接导致吊销驾照的下调。为什么要将速度规制为一半呢？在住宅区的生活道路上，孩子冲出、车辆相互碰撞等危险场面接连发生。",
                "grammar": "「〜から〜に引き下げられる」— 从…下调至…。例：60キロから30キロに引き下げられます（从60公里下调至30公里）。\n「〜もあり得る」— 也可能…。例：一発免停もあり得る（也可能直接吊销驾照）。\n「〜を半分に」— 将…减半。例：速度を半分に規制する（将速度规制为一半）。",
                "vocab": [["生活道路", "せいかつどうろ", "生活道路、居民区道路"], ["法定速度", "ほうていそくど", "法定速度"], ["引き下げる", "ひきさげる", "下调"], ["一発免停", "いっぱつめんてい", "直接吊销驾照"], ["規制", "きせい", "规制、限制"], ["住宅街", "じゅうたくがい", "住宅区"]]
            },
            {
                "ja": "生活道路とは、中央線や中央分離帯がない道路で、国内の国道・都道府県道・市町村道のうち約7割が該当します。東京・江戸川区のある道路は、住宅街の中にある速度制限のない生活道路です。車道と歩道を隔てるガードレールや縁石はなく、歩行者のすぐ横を車両が走っていきます。番組で計測してみると、35キロ、37キロ、40キロで走行していました。今は違反にあたらないものの、来月からはスピード違反となる車もありました。",
                "en": "A residential road is a road without a center line or central median, and about 70 percent of national, prefectural, and municipal roads in Japan fall into this category. A certain road in Tokyo's Edogawa Ward is a residential road in a housing area with no speed limit. There are no guardrails or curbs separating the roadway from the sidewalk, and vehicles pass right alongside pedestrians. When the program measured actual speeds, vehicles were traveling at 35, 37, and 40 km/h. These are not violations now, but from next month some cars would become speeding violations.",
                "literal": "生活道路是指没有中央线和中央分离带、国内国道・都道府县道・市町村道中约7成符合的道路。东京・江户川区的某条道路，是位于住宅区中没有速度限制的生活道路。没有隔离车道和人行道的护栏或路缘石，车辆就从行人紧旁驶过。节目中实测后，车辆以35、37、40公里行驶。现在不算违规，但从下月起也有车辆将构成超速。",
                "grammar": "「〜のうち」— …之中。例：国道などのうち約7割（国道等之中约7成）。\n「〜にあたらない」— 不构成…、不算…。例：違反にあたらない（不构成违规）。\n「〜ものの」— 虽然…但是…。例：今は違反にあたらないものの（虽然现在不构成违规）。",
                "vocab": [["中央線", "ちゅうおうせん", "中央线、车道分界"], ["中央分離帯", "ちゅうおうぶんりたい", "中央分隔带"], ["該当", "がいとう", "符合、适用"], ["歩道", "ほどう", "人行道"], ["縁石", "えんせき", "路缘石"], ["計測", "けいそく", "测量"], ["スピード違反", "すぴーどいはん", "超速违章"]]
            },
            {
                "ja": "超過した速度ごとに反則金や違反点数が決まり、現時点の法定速度60キロのまま来月同じ場所を走ると、一発免停になる可能性もあります。生活道路の近くに住む住民からは「学童があって子どもたちが通る通りなので、慣れていない人が結構スピードを出している」という声が聞かれました。家の前に柵を設置した男性は、これまでに自宅が10回も事故被害に遭ったといいます。「まともに飛び込んだ車は何回かありましたね」と話していました。",
                "en": "Fines and violation points are determined according to the amount of the speed excess, and if one drives in the same place next month at the current legal limit of 60 km/h, there is even a possibility of immediate license suspension. Residents living near residential roads offered voices such as, \"This is a street where schoolchildren pass, so people who aren't used to it drive quite fast.\" A man who installed a fence in front of his house says his home has been damaged in accidents as many as 10 times. He said, \"There have been several times when cars drove straight into it.\"",
                "literal": "根据超速幅度决定罚款和违章点数，若仍以当前法定时速60公里在下月行驶同一地点，也有可能直接吊销驾照。居住生活道路附近的居民中听到了「因为是有学童、孩子们通行的街道，不熟悉的人相当多超速驾驶」的声音。在家门前设置栅栏的男性称，到目前为止自家已遭遇10次事故损害。「有好几次车径直撞进来了」他这样说道。",
                "grammar": "「〜ごとに」— 每…、按照…。例：超過した速度ごとに（根据超速幅度）。\n「〜こと」— 事情、情况（作为引用）。例：自宅が10回も事故被害に遭ったといいます（据说自家遭遇10次事故损害）。\n「〜によると/の声が聞かれた」— 听到…的声音。例：住民からは…声が聞かれました（从居民那里听到…的声音）。",
                "vocab": [["反則金", "はんそくきん", "违章罚款"], ["違反点数", "いはんてんすう", "违章点数"], ["住民", "じゅうみん", "居民"], ["学童", "がくどう", "学童、上学儿童"], ["飛び込む", "とびこむ", "冲入、驶入"], ["柵", "さく", "栅栏、围栏"]]
            },
        ]
    },
    {
        "slug": "gouu-tokubetsu-keihou",
        "title": "石川県・富山県に「レベル5大雨特別警報」　命を守る行動を",
        "subtitle": "from tenki.jp",
        "paras": [
            {
                "ja": "27日朝、石川県と富山県の一部に「レベル5大雨特別警報」が発表されました。対象となったのは、石川県の羽咋市、志賀町、宝達志水町、中能登町と、富山県の氷見市です。大雨により、何らかの災害がすでに発生している可能性が高く、気象台は「ただちに命を守る最善の行動をとってください」と呼びかけています。",
                "en": "On the morning of the 27th, a \"Level 5 heavy rain special warning\" was issued for parts of Ishikawa and Toyama Prefectures. The areas covered are Hakui City, Shiga Town, Hodatsushimizu Town, and Nakanoto Town in Ishikawa Prefecture, and Himi City in Toyama Prefecture. There is a high possibility that some kind of disaster has already occurred due to the heavy rain, and the meteorological observatory is urging people to \"immediately take the best action to protect your life.\"",
                "literal": "27日早晨，石川县和富山县部分地区发布了「5级大雨特别警报」。对象是石川县的羽咋市、志贺町、宝达志水町、中能登町和富山县的冰见市。由于大雨，某种灾害已经发生的可能性很高，气象台呼吁「请立即采取保护生命的最好行动」。",
                "grammar": "「〜に発表された」— 对…发布。例：一部にレベル5大雨特別警報が発表されました（对部分地区发布了5级大雨特别警报）。\n「〜可能性が高い」— …的可能性很高。例：災害がすでに発生している可能性が高く（灾害已经发生的可能性很高）。\n「〜と呼びかけています」— 呼吁…。例：行動をとってくださいと呼びかけています（呼吁请采取行动）。",
                "vocab": [["発表", "はっぴょう", "发布、发表"], ["特別警報", "とくべつけいほう", "特别警报"], ["大雨", "おおあめ", "大雨"], ["災害", "さいがい", "灾害"], ["気象台", "きしょうだい", "气象台"], ["ただちに", "ただちに", "立即、马上"]]
            },
            {
                "ja": "あわてて避難することは危険な場合もあります。身の危険を感じるような雨の降り方だったり、道路が冠水したりしている場合は、どうしても屋外に避難することが難しいこともあります。そのようなときは、少しでも崖や沢から離れた建物や、少しでも浸水しにくい高い場所に移動するなどして、身の安全を確保してください。",
                "en": "Rushing to evacuate can also be dangerous in some cases. When the rain is falling in a way that makes you feel in danger, or when roads are flooded, it may be difficult to evacuate outdoors no matter what. In such cases, secure your own safety by moving to a building somewhat away from cliffs or streams, or to a higher place that is somewhat less prone to flooding.",
                "literal": "匆忙避难有时也很危险。当雨势让人感到生命危险、或道路积水时，有时无论如何也很难在室外避难。这种情况下，请移动到尽量远离崖壁或溪流的建筑物、或尽量不易进水的较高的地方等，确保自身安全。",
                "grammar": "「〜たり〜たり」— …或…（列举）。例：雨の降り方だったり、道路が冠水したり（雨势危险，或道路积水）。\n「〜にくい」— 难以…。例：浸水しにくい高い場所（不易进水的较高处）。\n「〜てください」— 请…（请求）。例：身の安全を確保してください（请确保自身安全）。",
                "vocab": [["避難", "ひなん", "避难"], ["危険", "きけん", "危险"], ["冠水", "かんすい", "积水、淹水"], ["崖", "がけ", "崖、陡坡"], ["沢", "さわ", "溪流、山涧"], ["浸水", "しんすい", "浸水、进水"], ["確保", "かくほ", "确保"]]
            },
            {
                "ja": "特別警報とは、予想される現象が特に異常であるため、重大な災害の起こるおそれが著しく大きい場合に発表される警報です。大雨のほか、氾濫、土砂災害、高潮などにもあり、そのうち氾濫、大雨、土砂災害、高潮の特別警報には「レベル5」という名称がつきます。レベル5大雨特別警報が発表されたときには、避難が困難となっているおそれもあります。命を守ることを第一に、行動してください。",
                "en": "A special warning is an alert issued when the anticipated phenomenon is especially abnormal and the risk of a major disaster occurring is extremely large. In addition to heavy rain, it also applies to flooding, sediment disasters, storm surges, and so on; among these, the special warnings for flooding, heavy rain, sediment disasters, and storm surges carry the name \"Level 5.\" When a Level 5 heavy rain special warning is issued, there is also a risk that evacuation may be difficult. Put protecting your life first and take action.",
                "literal": "特别警报是指，在预料的现象特别异常、重大灾害发生的危险性显著较大时发布的警报。除了大雨之外，还有泛滥、泥沙灾害、风暴潮等，其中泛滥、大雨、泥沙灾害、风暴潮的特别警报带有「5级」的名称。当5级大雨特别警报发布时，也可能存在避难困难的情况。请以保护生命为第一要务采取行动。",
                "grammar": "「〜とは」— 所谓…是…（下定义）。例：特別警報とは…警報です（所谓特别警报是…警报）。\n「〜おそれがある」— 有…的危险、可能…。例：起こるおそれが著しく大きい（发生的危险性显著较大）。\n「〜を第一に」— 以…为第一。例：命を守ることを第一に（以保护生命为第一）。",
                "vocab": [["現象", "げんしょう", "现象"], ["異常", "いじょう", "异常"], ["土砂災害", "どしゃさいがい", "泥沙灾害、土石灾害"], ["高潮", "たかしお", "风暴潮、高潮"], ["氾濫", "はんらん", "泛滥、涨溢"], ["困難", "こんなん", "困难"]]
            },
        ]
    },
    {
        "slug": "burusu-wirisu-ninchishou",
        "title": "ブルース・ウィリス、認知症により「俳優だったことも忘れる」…妻が語る前頭側頭型認知症の怖さ",
        "subtitle": "from Harper's BAZAAR",
        "paras": [
            {
                "ja": "『ダイ・ハード』『シックス・センス』などの名作に携わり、ハリウッドを代表する俳優であるブルース・ウィリスは、失語症の診断を受けたことをきっかけに、2022年3月に俳優業を引退した。その妻エマ・ヘミング・ウィリスは、夫が「前頭側頭型認知症」と診断されるに至った初期の小さな変化について、インタビューで明かしている。",
                "en": "Bruce Willis, an actor representing Hollywood who worked on masterpieces such as \"Die Hard\" and \"The Sixth Sense,\" retired from acting in March 2022 after being diagnosed with aphasia. His wife Emma Heming Willis has revealed in interviews the small early changes that led to her husband being diagnosed with frontotemporal dementia (FTD).",
                "literal": "参与《虎胆龙威》《第六感》等名作、代表好莱坞的演员布鲁斯・威利斯，以被诊断为「失语症」为契机，于2022年3月退出了演员工作。其妻子艾玛・赫明・威利斯在采访中透露了丈夫被诊断为「额颞叶痴呆」前初期的小变化。",
                "grammar": "「〜をきっかけに」— 以…为契机。例：失語症の診断を受けたことをきっかけに（以被诊断为失语症为契机）。\n「〜を代表する」— 代表…。例：ハリウッドを代表する俳優（代表好莱坞的演员）。\n「〜に至った」— 达到…、演变为…。例：診断されるに至った（演变为被诊断）。",
                "vocab": [["名作", "めいさく", "名作"], ["失語症", "しつごしょう", "失语症"], ["引退", "いんたい", "引退、退休"], ["認知症", "にんちしょう", "痴呆症、认知症"], ["診断", "しんだん", "诊断"], ["明かす", "あかす", "透露、揭示"]]
            },
            {
                "ja": "エマによると、ブルースは子どもの頃、ひどい吃音だったという。大学で演劇に出会い、台本を暗記すれば言葉が詰まらずに話せることに気づき、それが俳優の道へと後押しした。また、ブルースは常に言葉に詰まっていたが隠すことが上手だったため、話し方が変わり始めたときも、それが吃音の一部だと思い込み、深刻な病気の初期症状だとは考えなかったという。前頭側頭型認知症は正しく診断されるまでに数年を要し、誤診されたり見逃されたりすることが多いとエマは指摘している。",
                "en": "According to Emma, Bruce had a severe stutter as a child. In college he encountered theater and realized that if he memorized scripts he could speak without stumbling, and that pushed him toward acting. Also, because Bruce had always stumbled over words but was good at hiding it, even when his way of speaking began to change, she assumed it was just part of his stutter and did not think it was an early symptom of a serious illness. Emma points out that frontotemporal dementia takes years to be correctly diagnosed and is often misdiagnosed or overlooked.",
                "literal": "据艾玛称，布鲁斯小时候有严重的口吃。在大学接触了戏剧，发现只要背诵台词就能不结结巴巴地说话，这推动他走上了演员之路。另外，布鲁斯虽然说话总是结巴但很擅长掩饰，因此当他说话方式开始改变时，也一味认为那是口吃的一部分，没想过是严重疾病的初期症状。艾玛指出，额颞叶痴呆需要数年才能被正确诊断，很多时候会被误诊或漏诊。",
                "grammar": "「〜によると」— 根据…。例：エマによると（据艾玛称）。\n「〜をきっかけに／〜へと後押しした」— 推动…走向。例：俳優の道へと後押しした（推动走向演员之路）。\n" 
                "「〜がちだ／〜ことが多い」— 往往…、很多时候…。例：誤診されたり見逃されたりすることが多い（很多时候会被误诊或漏诊）。",
                "vocab": [["吃音", "きつおん", "口吃"], ["暗記", "あんき", "背诵、记住"], ["後押し", "あとおし", "推动、幕后支持"], ["詰まる", "つまる", "堵塞、卡住"], ["初期症状", "しょきしょうじょう", "初期症状"], ["誤診", "ごしん", "误诊"], ["見逃す", "みのがす", "漏掉、忽略"]]
            },
            {
                "ja": "ブルースは現在、妻や娘たちと離れて暮らし、専門施設で生活しているという。報道によると、娘たちの顔を見ても認識できないこともあり、自分が俳優だったという事実も理解できていないとされる。妻のエマは「この旅路は、あまりに多くの家族が直面している現実を私に気づかせた」と述べ、「FTDへの認知度を高め、研究を支援し、介護者たちの傍らに立つために基金を設立した」と、誕生日のメッセージでその思いを伝えている。",
                "en": "Bruce currently lives apart from his wife and daughters, reportedly in a specialized facility. According to reports, he sometimes does not recognize his daughters' faces, and it is said he does not understand even the fact that he was an actor. His wife Emma said in a birthday message, \"This journey has made me aware of the reality that far too many families face,\" and conveyed her feelings that she \"established a foundation to raise awareness of FTD, support research, and stand by the caregivers who carry an immeasurable burden every day.\"",
                "literal": "布鲁斯目前与妻子和女儿分开生活，据说在专业设施中生活。据报道称，有时看到女儿们也不会认出，据说连自己曾是演员这一事实也无法理解。妻子艾玛在生日贺词中表示「这条路让我意识到太多家庭正面临的现实」，并表达了「为了提高对FTD的认知度、支持研究、站在每天背负着不可估量重担的护理者身旁，设立了基金」的想法。",
                "grammar": "「〜という」— 据说…（传闻）。例：専門施設で生活しているという（据说在专业设施中生活）。\n「〜とされる」— 被认为…、据说…。例：理解できていないとされる（据说无法理解）。\n「〜ために」— 为了…。例：研究を支援し…ために（为了支持研究…）。",
                "vocab": [["専門施設", "せんもんしせつ", "专业设施"], ["認識", "にんしき", "认识、识别"], ["介護者", "かいごしゃ", "护理者、看护人"], ["基金", "ききん", "基金"], ["認知度", "にんちど", "认知度、知名度"], ["重荷", "おもに", "重担、负担"], ["傍ら", "かたわら", "身旁、旁边"]]
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
