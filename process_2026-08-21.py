#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-21 (Fri) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-21'
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
        "slug": "shinmai-kakaku-daikyuu",
        "title": "26年産新米 大幅値下がりの見通し 概算金 前年比2〜4割下落",
        "subtitle": "from 共同通信",
        "paras": [
            {
                "ja": "2026年産の新米価格が、高騰した前年に比べて大幅に値下がりする見通しとなったことが分かりました。各地のJAグループが新米を集荷する際にコメ農家に前払いする「概算金」が決まり始め、北海道や北信越の3県では前年比2〜4割程度下落しました。コメ余りを背景に、値下がりは他地域にも広がっていきそうです。",
                "en": "It has become clear that 2026-crop new rice prices are expected to fall significantly compared with the soaring previous year. The \"estimated payments\" that regional JA groups pay rice farmers in advance when collecting new rice have begun to be set, falling about 20–40% year-on-year in Hokkaido and three prefectures in Hokushin'etsu. Against a backdrop of a rice surplus, the price decline is likely to spread to other regions as well.",
                "literal": "2026年产的新米价格，与暴涨的前一年相比出现了大幅下跌的预想，此事已得知。各地JA集团在收购新米时向稻农预付的「概算金」已开始决定，北海道和北信越3县相比前一年下降了约2～4成。以大米过剩为背景，下跌似乎还将扩展到其他地区。",
                "grammar": "「〜ことになった」— 变成了…（结果）。例：値下がりする見通しとなった（变成下跌的预想）。\n「〜始め」— 开始…。例：概算金が決まり始め（概算金开始决定）。\n「〜そうです」— 看起来会…（样态）。例：広がっていきそうです（看起来会不断扩大）。",
                "vocab": [["新米", "しんまい", "新米、当年产大米"], ["高騰", "こうとう", "暴涨、价格飞涨"], ["値下がり", "ねさがり", "降价、跌价"], ["集荷", "しゅうか", "收货、收购"], ["概算金", "がいさんきん", "概算金（预付款）"], ["前払い", "まえばらい", "预付"], ["下落", "げらく", "下跌、下落"]]
            },
            {
                "ja": "夏に九州などでいち早く収穫された早場米は、スーパーの店頭価格が既に5キロ3千円前後まで下がっています。物価高が続く中で家計には朗報ですが、離農が増える恐れもあります。農家の間では、生産費用を賄えず経営を圧迫するのではないかとの危機感が高まっています。",
                "en": "Early-harvest rice, gathered quickly in Kyushu and elsewhere in summer, has already dropped to around 3,000 yen per 5 kg at supermarket shelves. Amid continuing high prices this is good news for household budgets, but there is also a risk that the number of farmers quitting will increase. Among farmers, anxiety is growing that production costs will not be covered and that this will squeeze their management.",
                "literal": "夏季在九州等地抢先收获的早场米，超市柜台价格已经降到5公斤3千日元前后。在物价高企持续之中对家计虽是喜讯，但也有离农增加的担忧。农户之间，无法承担生产费用、将压迫经营的危机感正在高涨。",
                "grammar": "「〜前後」— …前后（约数）。例：5キロ3千円前後（5公斤3千日元前后）。\n「〜恐れもあります」— 也有…的担忧。例：離農が増える恐れもあります（也有离农增加的担忧）。\n「〜ではないかと」— 会不会…（疑虑）。例：経営を圧迫するのではないかと（是不是会压迫经营）。",
                "vocab": [["早場米", "はやばまい", "早稻米"], ["店頭", "てんとう", "柜台、店面"], ["物価", "ぶっか", "物价"], ["朗報", "ろうほう", "好消息、喜讯"], ["離農", "りのう", "弃农、离开农业"], ["賄える", "まかなえる", "能负担、能筹措"], ["圧迫", "あっぱく", "压迫、挤压"]]
            },
            {
                "ja": "JA全農にいがたは、26年産の「一般コシヒカリ」の概算金を、玄米60キロ当たりで前年比38%減の1万8500円に決めたと発表しました。新潟県は最大のコメ産地で、他地域への影響が大きいとみられています。各JAは集荷したコメを今後、少しでも高く取引し、農家にコストに見合った額を還元できないか検討しています。",
                "en": "JA Zen-Noh Niigata announced that it has set the estimated payment for 2026-crop \"standard Koshihikari\" at 18,500 yen per 60 kg of brown rice, a decrease of 38% from the previous year. Niigata Prefecture is the largest rice-producing area, and the impact on other regions is seen as large. Each JA is considering whether it can trade the collected rice as high as possible going forward and return to farmers an amount commensurate with their costs.",
                "literal": "JA全农新潟宣布，将26年产的「一般越光米」的概算金定为玄米每60公斤前一年比减少38%的18500日元。新潟县是最大的大米产地，对其他地区的影响被认为很大。各JA正在探讨今后能否将收购的大米尽量高额交易，以追加支付的形式向农户返还与成本相当的金额。",
                "grammar": "「〜と発表しました」— 宣布了…。例：決めたと発表しました（宣布已决定）。\n" "「〜とみられています」— 被认为…。例：影響が大きいとみられています（被认为影响很大）。\n「〜できないか検討しています」— 正在探讨能否…。例：還元できないか検討しています（正在探讨能否返还）。",
                "vocab": [["玄米", "げんまい", "糙米、玄米"], ["当たり", "あたり", "每…"], ["産地", "さんち", "产地"], ["影響", "えいきょう", "影响"], ["取引", "とりひき", "交易"], ["還元", "かんげん", "返还、还原"], ["検討", "けんとう", "探讨、研究"]]
            },
        ]
    },
    {
        "slug": "daiichi-pan-touki-39kg",
        "title": "大山県道に連日のパン投棄 合計39kg確認 鶏のレバーも 鳥取",
        "subtitle": "from BSS山陰放送",
        "paras": [
            {
                "ja": "鳥取県にある国立公園大山の県道で、連日、大量の食パンが捨てられています。20日の朝も被害が確認され、これで5日目となりました。発見された食パンは、これまでに合計で40キロ近くになります。ガードレールの柱の間に、市販サイズより大きい食パンが100メートルほどの間隔で点在していました。",
                "en": "Along the prefectural road in Daisen National Park in Tottori Prefecture, large amounts of bread are being dumped day after day. Damage was also confirmed on the morning of the 20th, making this the fifth day. The bread discovered so far totals nearly 40 kilograms in all. Loaves larger than commercial size were scattered at intervals of about 100 meters between the posts of the guardrail.",
                "literal": "在鸟取县国立公园大山的县道上，连日被丢弃大量面包。20日早晨也确认了受害，至此已是第5天。被发现的面包，至此合计接近40公斤。在护栏柱之间，比市售尺寸更大的面包以约100米间隔逐个分布着。",
                "grammar": "「〜ています」— 正在…（持续状态）。例：捨てられています（正被丢弃着）。\n「〜となりました」— 到了…。例：5日目となりました（到了第5天）。\n「〜ほど」— …左右（程度）。例：100メートルほどの間隔（约100米的间隔）。",
                "vocab": [["国立公園", "こくりつこうえん", "国立公园"], ["大量", "たいりょう", "大量"], ["投棄", "とうき", "丢弃、乱扔"], ["被害", "ひがい", "受害、损害"], ["合計", "ごうけい", "合计"], ["ガードレール", "がーどれーる", "护栏"], ["点在", "てんざい", "散落、分布于"]]
            },
            {
                "ja": "事の発端は今月14日、自然公園財団の職員が巡回中に道路わきのパン投棄を発見したことです。14日だけで重さ16.7キロありました。その後も19日には鶏の内臓、レバーのようなものが1.3キロ見つかり、20日朝にはまた大量の食パン10.5キロが確認されました。職員らは、普通の不法投棄とは違う何らかの目的があるとみています。",
                "en": "The incident began on the 14th of this month, when staff of the National Park Foundation discovered dumped bread at the roadside during a patrol. On the 14th alone it weighed 16.7 kilograms. Afterward, on the 19th, about 1.3 kg of chicken offal resembling liver was found, and on the morning of the 20th another 10.5 kg of bread was confirmed. The staff believe there is some purpose different from ordinary illegal dumping.",
                "literal": "事情的开端是本月14日，自然公园财团职员巡逻时发现路边被丢弃的面包。仅14日就重达16.7公斤。之后19日又发现类似鸡内脏、肝脏的东西1.3公斤，20日早晨又确认了大量面包10.5公斤。职员们认为这与普通非法丢弃不同，带有某种目的。",
                "grammar": "「〜ことです」— 就是…（说明原因）。例：発見したことです（就是发现了…）。\n「〜だけで」— 仅…就。例：14日だけで16.7キロ（仅14日就16.7公斤）。\n「〜とみています」— 认为…。例：何らかの目的があるとみています（认为有某种目的）。",
                "vocab": [["発端", "ほったん", "开端、起因"], ["巡回", "じゅんかい", "巡逻、巡回"], ["内臓", "ないぞう", "内脏"], ["レバー", "ればー", "肝脏"], ["不法投棄", "ふほうとうき", "非法丢弃、乱倒"], ["目的", "もくてき", "目的"], ["何らか", "なんらか", "某种、某"]]
            },
            {
                "ja": "この周辺では、これまでにクマの目撃情報も出ていて、職員らは餌付けにつながる危険性を指摘しています。自然公園財団は「普通の不法投棄とは完全に違う目的で行われている。生き物に影響が出る恐れもある」と話しています。警察もパン投棄の経緯を調べています。",
                "en": "In this area, bear sightings have also been reported so far, and staff point out the danger that this could lead to feeding wild animals. The National Park Foundation says, \"This is being done with a purpose completely different from ordinary illegal dumping. There is also a risk of an impact on wildlife.\" Police are also investigating the circumstances of the bread dumping.",
                "literal": "这一带此前也已出现熊的目击信息，职员们指出这可能导致喂食野生动物。自然公园财团表示「这是以与普通非法丢弃完全不同的目的进行的。也存在对生物产生影响的风险」。警方也在调查面包被丢弃的经过。",
                "grammar": "「〜につながる」— 导致…、通向…。例：餌付けにつながる（导致喂食）。\n「〜恐れもある」— 也有…的风险。例：影響が出る恐れもある（也有产生影响的风险）。\n「〜ています」— 正在…。例：調べています（正在调查）。",
                "vocab": [["周辺", "しゅうへん", "周边、一带"], ["目撃", "もくげき", "目击"], ["餌付け", "えづけ", "喂食、投喂"], ["危険性", "きけんせい", "危险性"], ["指摘", "してき", "指出、指出"], ["生き物", "いきもの", "生物、活物"], ["経緯", "いきさつ", "经过、来龙去脉"]]
            },
        ]
    },
    {
        "slug": "tokkyu-sesshoku-4nin-shibou",
        "title": "東武日光線 作業員4人が特急と接触し死亡 退避完了の合図中に事故",
        "subtitle": "from 産経新聞",
        "paras": [
            {
                "ja": "東武日光線の新鹿沼駅で20日、作業員4人が特急列車に接触して死亡した事故は、見張りの作業員が列車に退避完了の合図を出す中で起きました。作業員が退避する過程で何らかのトラブルがあったとみられています。線路への立ち入り作業は人為ミスを防ぐため複数の確認が取られるのが一般的ですが、事故は防げませんでした。",
                "en": "The accident at Tobu Nikkō Line's Shin-Kanuma Station on the 20th, in which four workers died after being struck by an express train, occurred while a lookout worker was signaling the train that evacuation was complete. A problem of some kind is believed to have occurred during the workers' evacuation. Line-entry work usually involves multiple checks to prevent human error, but the accident could not be prevented.",
                "literal": "在東武日光线的北鹿沼站20日，发生作业员4人与特急列车接触死亡的交通事故，事故发生在了望作业员向列车发出退避完成信号的过程中。作业员在退避过程中被认为发生了某种麻烦。为防止人为失误，进入线路作业一般会进行多重确认，但事故未能防住。",
                "grammar": "「〜中で起きました」— 在…过程中发生。例：合図を出す中で起きました（在发出信号过程中发生）。\n「〜とみられています」— 被认为…。例：トラブルがあったとみられています（被认为有麻烦）。\n「〜ため」— 为了…。例：人為ミスを防ぐため（为了防止人为失误）。",
                "vocab": [["接触", "せっしょく", "接触、相撞"], ["見張り", "みはり", "了望、看守"], ["退避", "たいひ", "退避、躲避"], ["合図", "あいず", "信号、暗号"], ["過程", "かてい", "过程"], ["人為ミス", "じんいみす", "人为失误"], ["防ぐ", "ふせぐ", "防止、防范"]]
            },
            {
                "ja": "東武鉄道は記者会見を開き、ホーム下の線路上で作業員が除草剤を散布していたことを明らかにしました。上り線の見張りは2人で行うことになっていましたが、当時は1人が意思疎通できず、もう1人が現場から80メートル付近の位置から、退避完了を意味する黄色の旗で合図し、列車側は警笛で反応しました。",
                "en": "Tobu Railway held a press conference and revealed that workers were spraying herbicide on the track beneath the platform. The watch on the inbound line was supposed to be conducted by two people, but at the time one could not communicate, and the other signaled from a position about 80 meters from the site with a yellow flag meaning evacuation complete; the train side responded with its horn.",
                "literal": "東武铁路召开记者会，澄清了作业员正在站台下方的线路上喷洒除草剂的事实。上行线的了望本应由2人进行，但当时有1人无法沟通意志，另一人从距现场约80米的位置，以表示退避完成的黄旗发出信号，列车方以汽笛作出反应。",
                "grammar": "「〜ことになっていました」— 本应…（规定）。例：2人で行うことになっていました（本应由2人进行）。\n「〜で」— 以…（手段）。例：黄色の旗で合図し（以黄旗发出信号）。\n「〜付近」— …附近。例：80メートル付近（80米附近）。",
                "vocab": [["除草剤", "じょそうざい", "除草剂"], ["散布", "さんぷ", "喷洒、散布"], ["上り線", "のぼりせん", "上行线"], ["意思疎通", "いしそつう", "沟通、意思交流"], ["警笛", "けいてき", "汽笛、警笛"], ["反応", "はんのう", "反应"], ["明らかにする", "あきらかにする", "查明、澄清"]]
            },
            {
                "ja": "近年は安全管理が徹底され、JR東日本は列車接近を無線で受信する警告機を作業員全員が身に着けています。赤外線センサーやAIカメラを活用する例もあります。ただ、運行本数が少ない路線を中心に、マンパワー頼みになりがちです。保線作業に詳しい大手鉄道関係者は「最近は運行時間中の線路立ち入りを避ける意識が高まっている。今時では考えられない事故だ」と話しました。",
                "en": "In recent years safety management has been thorough, and every worker at JR East wears a warning device that receives train approach signals wirelessly. There are also examples using infrared sensors and AI cameras. However, especially on lines with few trains, it tends to rely on manpower. A major railway official familiar with track maintenance said, \"Recently there's a growing awareness of avoiding entry onto the track during operating hours. This is an accident unthinkable in this day and age.\"",
                "literal": "近年安全管理得以贯彻，JR东日本让全体作业员佩戴无线接收列车接近的警报机。也有活用红外线传感器和AI摄像头的例子。只是，以运行车次少的线路为中心，容易依赖人力。熟悉养路作业的大型铁路相关人士表示「最近避开运行时间进入线路的意识正在提高。这是如今时代难以想象的事故」。",
                "grammar": "「〜ています」— 正在…（资格持续）。例：全員が身に着けています（全体佩戴着）。\n「〜がちです」— 容易…、往往…。例：マンパワー頼みになりがちです（容易依赖人力）。\n「〜では考えられない」— 在…无法想象。例：今時では考えられない（当今无法想象）。",
                "vocab": [["徹底", "てってい", "贯彻、彻底"], ["警告機", "けいこくき", "警报装置"], ["身に着ける", "みにつける", "佩戴、穿戴"], ["赤外線", "せきがいせん", "红外线"], ["マンパワー", "まんぱわー", "人力"], ["保線", "ほせん", "养路（铁路）"], ["意識", "いしき", "意识"]]
            },
        ]
    },
    {
        "slug": "tobikomi-spot-20sai-ishikifumei",
        "title": "川に飛び込み20歳大学生が意識不明 高知・汗見川の飛び込みスポット",
        "subtitle": "from テレビ高知",
        "paras": [
            {
                "ja": "20日午後、高知県の山あいを流れる川で、遊泳中だった20歳の男子大学生が意識不明となる水難事故がありました。男子大学生は、岩場から川へ飛び込んで川岸に上がった後、おう吐して気を失ったということです。消防が駆けつけると、大学生は川岸の岩場で横たわっていて、すでに意識不明の状態でした。",
                "en": "On the afternoon of the 20th, a water accident occurred on a river flowing through the mountains of Kōchi Prefecture, in which a 20-year-old male university student who was swimming became unconscious. According to reports, after diving into the river from a rocky area and climbing onto the bank, the student vomited and lost consciousness. When firefighters arrived, the student was lying on the rocky bank, already unconscious.",
                "literal": "20日下午，在流经高知县山间的河中，发生了正在游泳的20岁男大学生失去意识的水难事故。据称，该大学生从岩石处跳入河中、上岸之后，呕吐并晕了过去。消防赶到时，大学生正横躺在河岸岩石上，已处于意识不明的状态。",
                "grammar": "「〜ことになっています」— 据说…（传闻）。例：おう吐して気を失ったということです（据说呕吐并晕过去了）。\n「〜と」— 一旦…就。例：川岸に上がった後（上岸之后）。\n「〜ていました」— 处于…状态。例：横たわっていて（正横躺着）。",
                "vocab": [["山あい", "やまあい", "山间、山谷"], ["遊泳", "ゆうえい", "游泳"], ["水難事故", "すいなんじこ", "水难事故、溺水事故"], ["岩場", "いわば", "岩石地带"], ["おう吐", "おうと", "呕吐"], ["気を失う", "きをうしなう", "失去意识、昏过去"], ["横たわる", "よこたわる", "横躺、横卧"]]
            },
            {
                "ja": "事故があったのは、本山町坂本を流れる汗見川です。男子大学生は当時、友人ら数人と川で泳いでいて、飛び込みスポットとして知られる「亀岩」から川に飛び込んでいました。数回飛び込んだ後、岸から5メートルほど離れた岩の上で四つん這いになって休み始め、おう吐して、そのまま気を失ったということです。",
                "en": "The accident occurred on the Asemi River flowing through Sakamoto, Motoyama Town. At the time, the student was swimming in the river with several friends and had been diving into the river from \"Kameiwa,\" a spot known for diving. After diving several times, he began resting on all fours on a rock about 5 meters from the bank, vomited, and lost consciousness as he was.",
                "literal": "事故发生地是流经本山町坂本的汗见川。当时，该大学生正与几位友人等在河中游泳，从以飞身跳水地点闻名的「龟岩」跳入河中。在跳了几次之后，在距河岸约5米的岩石上四肢着地开始休息，随即呕吐，就那么失去了意识。",
                "grammar": "「〜として知られる」— 作为…而闻名。例：飛び込みスポットとして知られる（以跳水地点闻名）。\n「〜ことになっています」— 据说…。例：そのまま気を失ったということです（据说就那么晕过去了）。\n「〜ほど」— 大约…。例：5メートルほど離れた（相距大约5米）。",
                "vocab": [["四つん這い", "よつんばい", "四肢着地、爬行"], ["友人", "ゆうじん", "朋友"], ["飛び込む", "とびこむ", "跳入、跳进"], ["亀岩", "かめいわ", "龟岩（形似龟的岩石）"], ["離れる", "はなれる", "离开、远离"], ["そのまま", "そのまま", "就那样、照原样"]]
            },
            {
                "ja": "男子大学生は頭に出血を伴う傷を負っていますが、この傷が飛び込んだことによるものかはわかっていません。また、ライフジャケットは着用しておらず、水面から高さ4メートルほどの場所から飛び込んでいたということです。飛び込んだ場所の水深はおよそ3メートルでした。警察は、当時の詳しい状況を調べています。",
                "en": "The student has wounds accompanied by bleeding on his head, but it is unknown whether these wounds were caused by diving. Also, he had not worn a life jacket and had been diving from a spot about 4 meters above the water surface. The water at the diving point was about 3 meters deep. Police are investigating the detailed circumstances at the time.",
                "literal": "该大学生头部带有伴随出血的伤，但尚不知这伤是否因跳水所致。另外，他没有穿救生衣，是从距水面约4米高的地方跳下的。跳入处的水深大约3米。警方正在调查当时的具体情况。",
                "grammar": "「〜かをし」— 是否…。例：この傷が飛び込んだことによるものかを（这伤是否因跳水所致）。\n「〜ておらず」— 未…（书面否定）。例：ライフジャケットを着用しておらず（未穿救生衣）。\n「〜ほど」— 大约…。例：高さ4メートルほど（高度大约4米）。",
                "vocab": [["出血", "しゅっけつ", "出血"], ["伴う", "ともなう", "伴随、带有"], ["ライフジャケット", "らいふじゃけっと", "救生衣"], ["着用", "ちゃくよう", "穿着、佩戴"], ["水面", "すいめん", "水面"], ["水深", "すいしん", "水深"], ["状況", "じょうきょう", "状况、情况"]]
            },
        ]
    },
    {
        "slug": "chugoku-okinawa-kizoku-gigi",
        "title": "中国 沖縄の帰属に「疑義」 バタン諸島にも類似主張",
        "subtitle": "from 共同通信",
        "paras": [
            {
                "ja": "中国が共産党機関紙などを通じ、日本の沖縄県やフィリピン最北に位置するバタン諸島の帰属に疑義を呈する見解を打ち出しています。高市早苗首相の台湾有事を巡る国会答弁や、日比が5月に合意した海洋境界画定交渉開始へのけん制とみられます。専門家は、政治や社会の不安定化を狙う「認知戦」の一種だと指摘しています。",
                "en": "Through Communist Party organs and other outlets, China is putting forward views that cast doubt on the territorial status of Japan's Okinawa Prefecture and the Batan Islands, located at the northern tip of the Philippines. This is seen as a warning against Prime Minister Takaichi Sanae's Diet answers over a Taiwan contingency and against the start of maritime boundary delimitation negotiations that the Philippines and Japan agreed on in May. Experts point out that this is a kind of \"cognitive warfare\" aimed at destabilizing politics and society.",
                "literal": "中国通过共产党机关报等，正在提出对日本冲绳县及其位于菲律宾最北端的巴丹群岛的归属持疑义的观点。这被认为是针对高市早苗首相围绕台湾有事的国会答辩、以及日菲5月就海洋边界划定谈判开始达成合意的牵制。专家指出，这是瞄准政治和社会不稳定化的「认知战」的一种。",
                "grammar": "「〜を通じ」— 通过…。例：党機関紙などを通じ（通过党机关报等）。\n「〜とみられます」— 被认为是…。例：けん制とみられます（被认为是牵制）。\n「〜だと指摘しています」— 指出是…。例：認知戦の一種だと指摘しています（指出是一种认知战）。",
                "vocab": [["帰属", "きぞく", "归属"], ["疑義", "ぎぎ", "疑义、疑问"], ["呈する", "ていする", "提出、呈示"], ["けん制", "けんせい", "牵制、掣肘"], ["国会答弁", "こっかいとうべん", "国会答辩"], ["境界", "きょうかい", "边界、疆界"], ["認知戦", "にんちせん", "认知战"]]
            },
            {
                "ja": "日比の排他的経済水域（EEZ）の境界画定交渉は、沖縄県の石垣島の南西約400キロにあるバタン諸島と先島諸島の間の海域が対象です。台湾の東側が含まれ、台湾を自国領土と主張する中国は交渉開始に反発しています。人民日報は、明治政府が1879年に琉球王国を廃した琉球処分に関し「19世紀の国際法の規定違反だ」と主張する学者の論文を載せました。",
                "en": "The maritime boundary delimitation negotiations between the Philippines and Japan cover the sea area between the Batan Islands, about 400 km southwest of Ishigaki Island in Okinawa Prefecture, and the Sakishima Islands. The area east of Taiwan is included, and China, which claims Taiwan as its own territory, opposes the start of negotiations. The People's Daily carried a scholar's paper claiming that the Ryukyu Disposition, by which the Meiji government abolished the Ryukyu Kingdom in 1879, \"violated the rules of 19th-century international law.\"",
                "literal": "日菲的专属经济区（EEZ）边界划定谈判，以位于冲绳县石垣岛西南约400公里的巴丹群岛与先岛群岛之间的海域为对象。包含台湾东侧，主张台湾为其本国领土的中国对谈判开始表示反对。人民日报刊登了一篇学者论文，主张明治政府1879年废除琉球王国的琉球处分「违反19世纪国际法规定」。",
                "grammar": "「〜が対象です」— 以…为对象。例：間の海域が対象です（以之间的海域为对象）。\n「〜を主張する」— 主张…。例：自国領土と主張する中国（主张其本国领土的中国）。\n「〜に関し」— 关于…。例：琉球処分に関し（关于琉球处分）。",
                "vocab": [["排他的経済水域", "はいたてきけいざいすいいき", "专属经济区（EEZ）"], ["画定", "かくてい", "划定"], ["先島諸島", "さきしましょとう", "先岛群岛"], ["領土", "りょうど", "领土"], ["反発", "はんぱつ", "反抗、反对"], ["廃する", "はいする", "废除"], ["論文", "ろんぶん", "论文"]]
            },
            {
                "ja": "中国は2000年代から、沖縄の日本帰属を揺さぶる発信を繰り返しています。専門家は、こうした言説は領土の現状を直接脅かすものではないが、国民や地域社会に不確実性を生み、長期的に安定を損なう危険性があると指摘します。日本政府は中国側に事実関係を伝え、冷静な対応を求めています。",
                "en": "Since the 2000s, China has repeatedly put out messages that shake Japan's claim over Okinawa. Experts point out that while such discourse does not directly threaten the territorial status quo, it creates uncertainty for citizens and local communities and carries the danger of undermining stability in the long term. The Japanese government is conveying the facts to the Chinese side and calling for a calm response.",
                "literal": "中国自2000年代起，反复进行动摇日本对冲绳归属的发信。专家指出，此类言论虽不会直接威胁领土现状，但会在国民和地区社会制造不确定性，长期有损害稳定的危险性。日本政府正向中方传达事实关系，并要求冷静应对。",
                "grammar": "「〜から、〜」— 从…起。例：2000年代から（从2000年代起）。\n「〜ものではない」— 并非…。例：直接脅かすものではない（并非直接威胁）。\n「〜危険性がある」— 有…的危险。例：安定を損なう危険性がある（有损害稳定的危险）。",
                "vocab": [["揺さぶる", "ゆさぶる", "动摇、撼动"], ["発信", "はっしん", "发信、发送"], ["言説", "げんせつ", "言论、话语"], ["現状", "げんじょう", "现状"], ["脅かす", "おびやかす", "威胁、胁迫"], ["不確実性", "ふかくじつせい", "不确定性"], ["損なう", "そこなう", "损害、损伤"]]
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
