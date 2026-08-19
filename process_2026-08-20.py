#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-20 (Thu) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-20'
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
        "slug": "moushobi-zenkoku-20260820",
        "title": "今日20日も九州や東海で猛暑日続出 熊本は37℃の危険な暑さ 熱中症警戒アラート15府県",
        "subtitle": "from tenki.jp",
        "paras": [
            {
                "ja": "今日20日(木)も広く厳しい残暑となるでしょう。九州から東海では猛暑日(最高気温35℃以上)が続出しそうです。熊本市では気温が37℃まで上がり、危険な暑さとなるでしょう。東京都心は33℃と真夏並みの暑さとなりそうです。熱中症警戒アラートが鹿児島など15府県に発表されています。熱中症に警戒してください。",
                "en": "Thursday the 20th will also bring severe lingering summer heat nationwide. From Kyushu to Tokai, \"mōshobi\" days (maximum 35°C or higher) are expected to appear one after another. In Kumamoto City the temperature will rise to 37°C, bringing dangerous heat. Central Tokyo is likely to see midsummer-like heat of 33°C. Heatstroke alerts have been issued for 15 prefectures including Kagoshima. Please be wary of heatstroke.",
                "literal": "今天20日（周四）全国也将出现严峻的残暑。从九州到东海，猛暑日（最高气温35度以上）似乎将接连出现。熊本市气温将上升到37度，将是危险的炎热。东京中心预计33度，将是盛夏般的炎热。热中暑警戒警报已向鹿儿岛等15个都府县发布。请注意防中暑。",
                "grammar": "「〜となるでしょう」— 将会变成…吧（推测）。例：危険な暑さとなるでしょう（将会是危险的炎热）。\n「〜となりそうです」— 看起来会变成…。例：真夏並みの暑さとなりそうです（看起来会变成盛夏般的炎热）。\n「〜てください」— 请…（请求）。例：熱中症に警戒してください（请注意防中暑）。",
                "vocab": [["残暑", "ざんしょ", "残暑、初秋的炎热"], ["猛暑日", "もうしょび", "猛暑日（最高气温35度以上）"], ["続出", "ぞくしゅつ", "接连出现"], ["危険", "きけん", "危险"], ["熱中症", "ねっちゅうしょう", "中暑、热射病"], ["警戒", "けいかい", "警戒"]]
            },
            {
                "ja": "熱中症警戒アラートが鹿児島、熊本、佐賀、長崎、大分、福岡、高知、愛媛、香川、鳥取、島根、広島、和歌山、兵庫、京都の15府県に発表されています。発表されていない地域でも沖縄から近畿、北陸、関東、東北で、暑さ指数(WBGT)が31以上となり、熱中症のリスクが高くなります。こまめな水分補給を心がけるなど、熱中症対策を万全にしてください。",
                "en": "Heatstroke alerts have been issued for 15 prefectures: Kagoshima, Kumamoto, Saga, Nagasaki, Oita, Fukuoka, Kochi, Ehime, Kagawa, Tottori, Shimane, Hiroshima, Wakayama, Hyogo, and Kyoto. Even in areas without alerts, the heat index (WBGT) will reach 31 or higher from Okinawa to Kinki, Hokuriku, Kanto, and Tohoku, raising the risk of heatstroke. Please take complete heatstroke measures, such as hydrating frequently.",
                "literal": "热中暑警戒警报已向鹿儿岛、熊本、佐贺、长崎、大分、福冈、高知、爱媛、香川、鸟取、岛根、广岛、和歌山、兵库、京都等15个都府县发布。即使未发布的地区，从冲绳到近畿、北陆、关东、东北，暑热指数（WBGT）也将达到31以上，中暑风险升高。请留意勤补水等，做好周全的中暑对策。",
                "grammar": "「〜に発表されています」— 已被发布到…（被动・状态）。例：15府県に発表されています（已向15个都府县发布）。\n「〜以上となり」— 达到…以上。例：暑さ指数が31以上となり（暑热指数达到31以上）。\n「〜ましょう／てください」— 让我们…吧／请…。例：対策を万全にしてください（请做好周全对策）。",
                "vocab": [["府県", "ふけん", "都府县"], ["地域", "ちいき", "地区"], ["暑さ指数", "あつさしすう", "暑热指数（WBGT）"], ["リスク", "りすく", "风险"], ["こまめに", "こまめに", "勤快地、经常"], ["水分補給", "すいぶんほきゅう", "补充水分"], ["万全", "ばんぜん", "周全、万全"]]
            },
            {
                "ja": "熱中症対策の1つに「プレクーリング」があります。これは屋外の作業などを始める前にあらかじめ体を冷やしておくことで、作業中に体温が上がるペースを緩やかにする方法です。1つ目は体の内側から冷やす方法で、凍らせたスポーツ飲料などで作る「アイススラリー」を飲むのがおすすめです。微細な氷と液体が混ざっているため、冷たさがゆっくり体の内部に伝わりやすくなります。",
                "en": "One heatstroke measure is \"pre-cooling.\" This is a method of cooling the body beforehand before starting outdoor work, so that the pace at which body temperature rises during work is slowed. The first method cools from inside the body; drinking \"ice slurry\" made from frozen sports drinks and the like is recommended. Because fine ice and liquid are mixed, the cold is easily transferred slowly to the body's interior.",
                "literal": "中暑对策之一有「预冷（pre-cooling）」。这是在开始户外作业等之前事先冷却身体，使作业中体温上升的速度变缓的方法。第一种是从身体内部冷却的方法，推荐饮用用冷冻运动饮料等制作的「冰浆（ice slurry）」。由于细小的冰和液体混合在一起，寒意更容易慢慢传到身体内部。",
                "grammar": "「〜ておく」— 事先…（准备）。例：体を冷やしておく（事先冷却身体）。\n" "「〜ため」— 因为…。例：微細な氷と液体が混ざっているため（因为细小的冰和液体混合着）。\n「〜やすくなる」— 变得容易…。例：伝わりやすくなります（变得容易传导）。",
                "vocab": [["屋外", "おくがい", "室外、户外"], ["あらかじめ", "あらかじめ", "事先、预先"], ["体温", "たいおん", "体温"], ["緩やか", "ゆるやか", "缓慢"], ["アイススラリー", "あいすすらりー", "冰浆（碎冰饮料）"], ["微細", "びさい", "微小、细微"], ["液体", "えきたい", "液体"]]
            },
            {
                "ja": "もう1つは、体の外側から冷やす方法です。保冷剤などが体に接触するように作られたクールベストや、ファンのついた上着を着るのもおすすめです。また、水温10～15℃の水の入った器に手や足を入れ、10分ほど冷やすだけでも効果があります。水温が低すぎると血管が収縮してしまい、逆効果になります。プレクーリングは方法を組み合わせて行うと、より効果的です。",
                "en": "The other method cools from outside the body. It is also recommended to wear a cooling vest made so that cool packs contact the body, or a jacket with a fan attached. Also, just putting hands or feet in a container of water at 10–15°C and cooling for about 10 minutes is effective. If the water is too cold, blood vessels constrict, which is counterproductive. Combining methods makes pre-cooling more effective.",
                "literal": "另一种是从身体外部冷却的方法。推荐穿为了让保冷剂等接触身体而制作的冷却背心、或带风扇的上衣。另外，将手脚放入装有10～15度水的容器中，冷却10分钟左右也很有效。如果水温过低，血管会收缩，反而适得其反。预冷结合多种方法进行会更有效。",
                "grammar": "「〜すぎると」— 如果过度…的话。例：水温が低すぎると（如果水温过低的话）。\n「〜てしまい」— 结果…了（遗憾）。例：血管が収縮してしまい（血管结果收缩了）。\n「〜と、〜」— 如果…就会…（条件）。例：組み合わせて行うと、より効果的です（如果组合进行，会更有效）。",
                "vocab": [["クールベスト", "くーるべすと", "冷却背心"], ["保冷剤", "ほれいざい", "保冷剂、冰袋"], ["接触", "せっしょく", "接触"], ["血管", "けっかん", "血管"], ["収縮", "しゅうしゅく", "收缩"], ["逆効果", "ぎゃくこうか", "适得其反、反效果"], ["効果的", "こうかてき", "有效果的"]]
            },
        ]
    },
    {
        "slug": "chiba-gouu-syaryou-tekkai",
        "title": "千葉豪雨 千葉市内の幹線道路上の放置車両をすべて撤去 生活道路は今後順次",
        "subtitle": "from TBS NEWS DIG",
        "paras": [
            {
                "ja": "千葉市は、豪雨で市内の幹線道路で動けなくなっていたすべての車両の撤去が完了したと発表しました。千葉県内では、豪雨の影響で水没などで動けなくなった車が一時、2700台にのぼり、このうち千葉市が管理する道路には2500台ほどが残されていました。2500台のうち、幹線道路にはおよそ1700台が残され、撤去作業が行われていました。",
                "en": "Chiba City announced that it has completed removing all vehicles that had become immobilized on the city's trunk roads due to the heavy rain. In Chiba Prefecture, the number of cars immobilized by flooding and other causes at one point reached 2,700; of these, about 2,500 remained on roads managed by Chiba City. Of the 2,500, roughly 1,700 remained on trunk roads, and removal work was underway.",
                "literal": "千叶市宣布，暴雨中在市内干线道路上动弹不得的全部车辆的撤除已完成。在千叶县内，受暴雨影响因水淹等而动弹不得的汽车一度达到2700辆，其中约2500辆留在了千叶市管理的道路上。2500辆中，干线道路上残留了约1700辆，撤除作业一直在进行。",
                "grammar": "「〜たと発表しました」— 宣布了…。例：撤去が完了したと発表しました（宣布撤除已完了）。\n「〜にのぼり」— 达到…（数量）。例：2700台にのぼり（达到2700辆）。\n「〜てしまっていた」— 结果一直…（状态）。例：動けなくなっていた車（一直动弹不得的车）。",
                "vocab": [["幹線道路", "かんせんどうろ", "干线道路"], ["撤去", "てっきょ", "撤除、拆除"], ["完了", "かんりょう", "完成"], ["水没", "すいぼつ", "被水淹没"], ["残される", "のこされる", "被留下"], ["およそ", "およそ", "大约"]]
            },
            {
                "ja": "千葉市によりますと、きのうまでに254台を回収し、きょうは67台を回収したということで、これで市の幹線道路に残っていた321台の車がすべて撤去されたということです。一方、およそ1400台の車については、所有者が自ら撤去したほか、ロードサービス業者に依頼するなどして撤去されたということです。",
                "en": "According to Chiba City, 254 vehicles were collected by yesterday and 67 were collected today, so the 321 cars remaining on the city's trunk roads have now all been removed. On the other hand, about 1,400 cars were removed by their owners themselves or by requests to roadside-assistance operators, among other means.",
                "literal": "据千叶市称，到昨天为止回收了254辆，今天回收了67辆，这样一来，残留在市干线道路上的321辆汽车已全部撤除。另一方面，约1400辆汽车，除所有者自行撤除外，也有通过委托道路救援业者等方式撤除的。",
                "grammar": "「〜ということです」— 据说…、据…称。例：すべて撤去されたということです（据说已全部撤除）。\n「〜によりますと」— 据…说。例：千葉市によりますと（据千叶市称）。\n「〜ほか」— 除…之外。例：自ら撤去したほか（除自行撤除之外）。",
                "vocab": [["回収", "かいしゅう", "回收"], ["所有者", "しょゆうしゃ", "所有者"], ["自ら", "みずから", "亲自、自己"], ["依頼", "いらい", "委托、请求"], ["業者", "ぎょうしゃ", "业者、从业者"], ["一方", "いっぽう", "另一方面"]]
            },
            {
                "ja": "撤去された車は、市役所が所有している土地などに保管されていて、あす以降、所有者への引き取り作業などを順次行っていくということです。さらに道幅の狭い生活道路には車が残されていて、市はあす以降、生活道路上の車についても順次、撤去作業を行うとしています。",
                "en": "The removed cars are being stored on land owned by the city hall and other sites, and from tomorrow onward the city will sequentially undertake work such as handing the vehicles back to their owners. Furthermore, cars still remain on narrow residential roads, and the city says it will sequentially carry out removal work on those residential roads as well from tomorrow onward.",
                "literal": "被撤除的汽车被保管在市役所所有的土地等处，从明天起将依次进行向所有者的领取移交等工作。此外，狭窄的生活道路上还残留着汽车，市里表示从明天起也将依次对生活道路上的汽车进行撤除作业。",
                "grammar": "「〜ていて」— 正处于…状态。例：保管されていて（正被保管着）。\n「〜ていく」— 接下来将…（进行）。例：順次行っていく（将依次进行）。\n「〜としています」— 表示…（打算）。例：撤去作業を行うとしています（表示将进行撤除作业）。",
                "vocab": [["保管", "ほかん", "保管、存储"], ["引き取り", "ひきとり", "领取、取回"], ["順次", "じゅんじ", "依次、顺次"], ["道幅", "みちはば", "路宽"], ["生活道路", "せいかつどうろ", "生活道路（住宅区道路）"], ["狭い", "せまい", "狭窄、窄"]]
            },
        ]
    },
    {
        "slug": "byouin-chuusya-jiko-kobayashi",
        "title": "小林市の病院駐車場で診察待つ列に車突っ込む 74歳女性が死亡 運転の女性を過失運転致死疑いで捜査",
        "subtitle": "from MRT宮崎放送",
        "paras": [
            {
                "ja": "19日朝、宮崎県小林市の病院の駐車場で、診察に訪れた人の列に普通乗用車が突っ込む事故があり、70代の女性が死亡しました。事故があったのは小林市細野にある病院の駐車場で、19日午前7時ごろ、「車が人の列に突っ込んだ」と警察に通報がありました。",
                "en": "On the morning of the 19th, an accident occurred at a hospital parking lot in Kobayashi City, Miyazaki Prefecture, in which a passenger car plowed into a line of people who had come for outpatient care, and a woman in her 70s died. The accident happened at the parking lot of a hospital in Hosono, Kobayashi City; around 7 a.m. on the 19th, police received a report that a car had plowed into a line of people.",
                "literal": "19日早晨，在宫崎县小林市的医院停车场，发生了普通轿车冲入前来就诊的队列的事故，一名70多岁的女性死亡。事故发生地在位于小林市细野的医院停车场，19日上午7点左右，有「汽车冲入了人群队列」的通报报警。",
                "grammar": "「〜で、〜」— 在…（场所）发生…。例：駐車場で…事故があり（在停车场发生了…事故）。\n「〜ごろ」— 大约…（时间）。例：午前7時ごろ（上午7点左右）。\n「〜と通報がありました」— 有…的通报。例：車が列に突っ込んだと通報がありました（有汽车冲入队列的通报）。",
                "vocab": [["駐車場", "ちゅうしゃじょう", "停车场"], ["診察", "しんさつ", "就诊、诊疗"], ["突っ込む", "つっこむ", "冲入、撞入"], ["事故", "じこ", "事故"], ["通報", "つうほう", "通报、报警"], ["死亡", "しぼう", "死亡"]]
            },
            {
                "ja": "この事故で、鹿児島県湧水町の看護師、宇都尚子さん(74歳)が意識不明の重体で市内の病院に運ばれましたが、およそ2時間後に死亡しました。警察によりますと、宇都さんは通院のため病院を訪れ、複数の人と診療が始まる時間まで待機していて、その列に停車していた普通乗用車が突っ込んだということです。",
                "en": "In this accident, nurse Uto Hisako (74) of Yusui Town, Kagoshima Prefecture, was taken unconscious and in critical condition to a hospital in the city, but died about two hours later. According to police, Uto had visited the hospital for treatment and was waiting with several others until the time treatment began, when a stationary passenger car plowed into that line.",
                "literal": "在此事故中，鹿儿岛县涌水町的护士宇都尚子（74岁）以意识不清的重伤状态被送往市内医院，约2小时后死亡。据警方称，宇都女士为就诊而来到医院，与其他多人一起等候到诊疗开始的时间，停在那队列旁的普通轿车冲入了队列。",
                "grammar": "「〜が、〜」— 虽然…但是…。例：運ばれましたが、死亡しました（虽然被送往医院，但死亡了）。\n「〜ため」— 为了…／因为…。例：通院のため（为了就诊）。\n「〜ていた」— 当时正…。例：待機していて（当时正等候着）。",
                "vocab": [["看護師", "かんごし", "护士"], ["意識不明", "いしきふめい", "意识不明"], ["重体", "じゅうたい", "重伤、病危"], ["通院", "つういん", "去医院就诊"], ["待機", "たいき", "等候、待命"], ["停車", "ていしゃ", "停车"]]
            },
            {
                "ja": "警察は、車を運転していた74歳の女性を過失運転傷害の疑いで現行犯逮捕しましたが、その後、釈放しました。そして、容疑を過失運転致死に切り替え、任意で捜査を進めています。診療開始を待つ列ができる時間帯で、駐車場では運転操作を誤った可能性もあるとみて調べています。",
                "en": "Police arrested the 74-year-old woman who had been driving the car on suspicion of negligent driving causing injury, but released her afterward. They then switched the suspicion to negligent driving causing death and are continuing an investigation on a voluntary basis. Because it was a time when a line forms while waiting for treatment to begin, they are investigating the possibility that the driver misoperated the vehicle in the parking lot.",
                "literal": "警方以过失驾驶致伤的嫌疑当场逮捕了驾驶汽车的74岁女性，但之后将其释放。然后将嫌疑改为过失驾驶致死，正在进行任意调查。在等候诊疗开始的队列出现的时段，他们认为停车场内可能发生了驾驶操作失误，正在展开调查。",
                "grammar": "「〜が、〜」— 虽然…但…。例：逮捕しましたが、その後、釈放しました（虽然逮捕了，但之后释放了）。\n「〜可能性もあるとみて」— 认为有可能…。例：運転操作を誤った可能性もあるとみて（认为有可能操作失误）。\n「〜ています」— 正在…。例：捜査を進めています（正在推进调查）。",
                "vocab": [["現行犯", "げんこうはん", "现行犯"], ["逮捕", "たいほ", "逮捕"], ["釈放", "しゃくほう", "释放"], ["容疑", "ようぎ", "嫌疑"], ["過失", "かしつ", "过失"], ["任意", "にんい", "任意"], ["捜査", "そうさ", "调查"]]
            },
        ]
    },
    {
        "slug": "icc-syokai-bei-seisai",
        "title": "ICC所長への米制裁に非難拡大 仏・EU・国連が相次ぎ表明 赤根智子所長を制裁対象に",
        "subtitle": "from ロイター",
        "paras": [
            {
                "ja": "フランスや欧州連合(EU)、国連は19日、国際刑事裁判所(ICC)の赤根智子所長と同裁判所の上級法廷弁護士に米国が科した制裁を巡り、相次いで非難や懸念を表明しました。ルビオ米国務長官は18日、赤根所長と上級法廷弁護士アブドゥライ・セイ氏を制裁対象に加えたと発表しました。",
                "en": "France, the European Union (EU), and the United Nations on the 19th expressed criticism and concern one after another over the sanctions the United States imposed on International Criminal Court (ICC) President Akane Tomoko and the court's senior defense lawyer. U.S. Secretary of State Rubio announced on the 18th that he had added President Akane and senior lawyer Abdoulaye Seye to the sanctions list.",
                "literal": "法国、欧盟（EU）、联合国于19日，就美国对国际刑事法院（ICC）的赤根智子院长及该法院高级辩护律师施加的制裁，接连表达了谴责和担忧。美国国务卿卢比奥18日宣布已将赤根院长和高级辩护律师阿卜杜拉耶·塞伊列入制裁对象。",
                "grammar": "「〜を巡り」— 围绕…。例：米国が科した制裁を巡り（围绕美国施加的制裁）。\n「〜相次いで」— 接连地。例：相次いで非難や懸念を表明しました（接连表达了谴责和担忧）。\n「〜と発表しました」— 宣布了…。例：制裁対象に加えたと発表しました（宣布已列入制裁对象）。",
                "vocab": [["制裁", "せいさい", "制裁"], ["非難", "ひなん", "谴责、批评"], ["懸念", "けねん", "担忧、顾虑"], ["所長", "しょちょう", "院长、所长"], ["法廷", "ほうてい", "法庭"], ["対象", "たいしょう", "对象"]]
            },
            {
                "ja": "フランス外務省報道官は「フランスは、ICCとその職員、そして裁判所を支える市民社会組織に対して取られるあらゆる形態の脅迫と強制手段を糾弾する」と表明しました。EUのフォンデアライエン委員長とコスタ議長も「ICCと赤根所長、そしてその使命を守る当局者らと固く連帯する」と述べました。",
                "en": "A French Foreign Ministry spokesperson stated, \"France condemns any form of intimidation and coercion taken against the ICC, its staff, and the civil-society organizations that support the court.\" EU Commission President von der Leyen and Council President Costa also said they \"firmly stand in solidarity with the ICC, President Akane, and the authorities who defend its mission.\"",
                "literal": "法国外交部发言人表示「法国谴责对ICC及其职员、以及支持法院的市民社会组织所采取的一切形式的胁迫与强制手段」。欧盟委员会主席冯德莱恩和欧洲理事会主席科斯塔也表示「与ICC、赤根院长、以及守护其使命的当局者坚定团结一致」。",
                "grammar": "「〜に対して」— 对…、针对…。例：ICCとその職員に対して（对ICC及其职员）。\n" "「〜と表明しました」— 表明了…。例：糾弾すると表明しました（表明将予以谴责）。\n「〜と述べました」— 陈述了…。例：連帯すると述べました（表示将团结一致）。",
                "vocab": [["報道官", "ほうどうかん", "发言人"], ["職員", "しょくいん", "职员"], ["市民社会", "しみんしゃかい", "市民社会"], ["脅迫", "きょうはく", "胁迫、威胁"], ["糾弾", "きゅうだん", "声讨、谴责"], ["連帯", "れんたい", "团结、声援"]]
            },
            {
                "ja": "国連のグテレス事務総長も、今回の制裁決定を深く懸念しています。国連報道官は定例記者会見で「事務総長は今回の指定、および他のICC職員に対する継続中の指定について深い懸念を表明する」と語りました。国連は同裁判所を「国際刑事司法の重要な柱」と見なしていると述べました。",
                "en": "UN Secretary-General Guterres also deeply concerns over this sanctions decision. A UN spokesperson said at a regular press briefing that \"the Secretary-General expresses deep concern over the current designation and the continuing designations of other ICC officials.\" He stated that the UN regards the court as \"an essential pillar of international criminal justice.\"",
                "literal": "联合国秘书长古特雷斯也对此制裁决定深表担忧。联合国发言人在例行记者会上表示「秘书长就此次指定、以及针对其他ICC职员的持续指定深表担忧」。并称联合国将该法院视为「国际刑事司法的关键支柱」。",
                "grammar": "「〜ております／ています」— 正…（郑重）。例：深く懸念しています（深表担忧）。\n「〜について」— 关于…。例：継続中の指定について（关于持续中的指定）。\n「〜と見なしています」— 视为…。例：重要な柱と見なしています（视为重要支柱）。",
                "vocab": [["事務総長", "じむそうちょう", "秘书长"], ["決定", "けってい", "决定"], ["指定", "してい", "指定"], ["継続中", "けいぞくちゅう", "持续中"], ["柱", "はしら", "支柱、核心"], ["司法", "しほう", "司法"]]
            },
        ]
    },
    {
        "slug": "toranpu-kinjonei-kaidan",
        "title": "トランプ氏 金正恩氏と年内会談の意向 北朝鮮は核兵器「57発保有」と発言",
        "subtitle": "from ロイター",
        "paras": [
            {
                "ja": "トランプ米大統領は19日、北朝鮮の金正恩朝鮮労働党総書記と年内に会談する意向を表明しました。また、北朝鮮は「非常に強力な」核兵器を57発保有しているとも述べました。トランプ氏は、今年後半に金正恩氏と会談する予定があるかという記者団からの質問に対し「会談する予定だ」と応じました。",
                "en": "U.S. President Trump stated on the 19th his intention to hold talks with North Korean Workers' Party General Secretary Kim Jong-un within the year. He also said North Korea possesses 57 \"very powerful\" nuclear weapons. In response to reporters' questions about whether he planned to meet with Kim in the latter half of the year, Trump replied, \"I plan to meet.\"",
                "literal": "美国总统特朗普19日表明与朝鲜劳动党总书记金正恩在年内会面的意向。另外还称北朝鲜拥有57枚「非常强大」的核武器。针对记者团提出的今年下半年是否计划与金正恩会面的提问，特朗普回应称「计划会面」。",
                "grammar": "「〜意向を表明しました」— 表明了…意向。例：会談する意向を表明しました（表明了进行会谈的意向）。\n「〜と述べました」— 述说了…。例：57発保有していると述べました（说拥有57枚）。\n「〜予定があるかという質問に対し」— 针对是否有…计划的提问。例：会談する予定があるかという質問に対し（针对是否会面的提问）。",
                "vocab": [["意向", "いこう", "意向"], ["表明", "ひょうめい", "表明、声明"], ["核兵器", "かくへいき", "核武器"], ["保有", "ほゆう", "拥有、持有"], ["総書記", "そうしょき", "总书记"], ["会談", "かいだん", "会谈"]]
            },
            {
                "ja": "トランプ氏はさらに「私は金正恩氏をよく知っている。賢明な大統領がいる限り、彼は問題を起こさないだろう」と語りました。その上で「彼は非常に強力な核兵器を57発持っている。（保有を）決して許すべきではなかった。私が大統領だったら許さなかっただろう」と続けました。",
                "en": "Trump further said, \"I know Kim Jong-un very well. As long as there's a wise president, he won't cause problems.\" He added, \"He has 57 very powerful nuclear weapons. We should never have allowed it. If I'd been president, I wouldn't have allowed it.\"",
                "literal": "特朗普还称「我非常了解金正恩。只要有明智的总统在，他就不会惹麻烦」。接着又说「他拥有57枚非常强大的核武器。本绝不应容许（其拥有）。如果我是总统，就不会容许吧」。",
                "grammar": "「〜てよく知っている」— 非常了解…。例：金正恩氏をよく知っている（非常了解金正恩）。\n「〜ている限り」— 只要…。例：賢明な大統領がいる限り（只要有明智的总统在）。\n「〜べきではなかった」— 本不应该…（后悔）。例：決して許すべきではなかった（本绝不应容许）。",
                "vocab": [["賢明", "けんめい", "明智、贤明"], ["限り", "かぎり", "只要…的范围内"], ["問題を起こす", "もんだいをおこす", "惹麻烦、制造问题"], ["決して", "けっして", "决（不）、绝对（不）"], ["許す", "ゆるす", "容许、宽恕"], ["続ける", "つづける", "继续"]]
            },
            {
                "ja": "北朝鮮が保有する核兵器の数については、長年にわたり専門家の間で推計に幅があります。ストックホルム国際平和研究所(SIPRI)は6月、北朝鮮が「およそ60発の核弾頭を組み立てた可能性があり、少なくともさらに30発を製造できるだけの核分裂性物質を保有している」との推計を示しました。",
                "en": "Regarding the number of nuclear weapons North Korea possesses, estimates have varied among experts for many years. In June, the Stockholm International Peace Research Institute (SIPRI) estimated that North Korea \"may have assembled roughly 60 nuclear warheads and possesses enough fissile material to build at least 30 more.\"",
                "literal": "关于北朝鲜拥有的核武器数量，多年来专家之间的推算存在差异。斯德哥尔摩国际和平研究所（SIPRI）6月提出了「朝鲜可能组装了约60枚核弹头，并拥有至少能再制造30枚的核裂变物质」的推算。",
                "grammar": "「〜については」— 关于…。例：核兵器の数については（关于核武器的数量）。\n「〜にわたり」— 长达…（期间）。例：長年にわたり（长达多年）。\n「〜との推計を示しました」— 给出了…的推算。例：製造できるだけの…との推計を示しました（给出了可制造…的推算）。",
                "vocab": [["推計", "すいけい", "推算、估算"], ["核弾頭", "かくだんとう", "核弹头"], ["組み立てる", "くみたてる", "组装"], ["少なくとも", "すくなくとも", "至少"], ["物質", "ぶっしつ", "物质"], ["核分裂性", "かくぶんれつせい", "核裂变性"]]
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
        if audio_ok:
            ok += 1
            print(f"   ✅ {slug}: {pc} paragraphs, audio OK")
        else:
            print(f"   ⚠️ {slug}: audio missing")
print(f"\n{ok}/{len(processed)} articles verified")
