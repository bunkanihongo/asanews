#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-31 (Mon) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-31'
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
        "slug": "france-aircon-100man-en",
        "title": "フランスではエアコン2台で約100万円 日本の価格に「泣きたいわ」",
        "subtitle": "from Hint-Pot",
        "paras": [
            {
                "ja": "近年、フランスでは厳しい暑さに見舞われることも増え、夏を快適に過ごすための備えが欠かせなくなっています。YouTubeチャンネルで現地の暮らしを発信しているMamiさん一家は、猛暑のフランスを離れ、日本へ一時帰国。滞在中に家電量販店を訪れたところ、フランス人の夫は、ある商品の価格を見て「パパ……泣きたいわ」と衝撃を受けました。",
                "en": "In recent years France has been hit by severe heat more and more often, making preparations for a comfortable summer essential. The Mami family, who share their local life on a YouTube channel, left sweltering France and temporarily returned to Japan. While there, they visited a home electronics store, and the French husband was shocked at the price of a certain product, saying, 'Papa... I could cry.'",
                "literal": "近年来，法国遭受严酷酷暑的情况增多，为了舒适度过夏天而做的准备变得不可或缺。在YouTube频道上发布当地生活的Mami一家离开了酷暑的法国，暂时回到日本。滞留期间去了家电量贩店，法国的丈夫看到某个商品的价格，受到了冲击并说出「爸爸……想哭」。",
                "grammar": "「〜に見舞われる」— 遭遇到、受到…（不好的事）。例：厳しい暑さに見舞われる（遭遇到严酷酷暑）。\n「〜ところ」— 就在（那时）…（时间节点）。例：家電量販店を訪れたところ（去家电量贩店时）。\n「〜わ」— 句尾女性用语，表感叹/感动。例：泣きたいわ（好想哭啊）。",
                "vocab": [["猛暑", "もうしょ", "酷暑、猛暑"], ["見舞われる", "みまわれる", "遭受、遭遇"], ["家電量販店", "かでんりょうはんてん", "家电量贩店"], ["一時帰国", "いちじきこく", "临时回国、短期回国"], ["衝撃", "しょうげき", "冲击、震惊"], ["絶句", "ぜっく", "无言、一时说不出话"]]
            },
            {
                "ja": "目についた製品は、本体に加えて標準工事費込みで16万円ほど。実は、近年のフランスで続く猛暑に耐えかね、一家は現地でエアコンを2台購入したばかり。しかし、夏に購入したにもかかわらず取り付け工事はなんと11月まで待たされ、費用は工事費などすべて込みで約100万円もかかるそうです。",
                "en": "The product that caught his eye cost about 160,000 yen including the standard installation fee in addition to the main unit. In fact, unable to endure the heat that has continued in France in recent years, the family had just purchased two air conditioners locally. However, even though they bought them in summer, they were reportedly made to wait until November for the installation work, and the cost, including all installation fees, comes to about 1 million yen.",
                "literal": "入眼的商品，除主机外含标准安装费约16万日元。其实，因为难以忍受近年来法国持续的酷暑，一家人在当地刚买了2台空调。然而，尽管夏天购买，安装工程竟然被拖到11月，费用含安装费等所有在内约需100万日元。",
                "grammar": "「〜に耐えかね」— 难以忍受…。例：猛暑に耐えかねて（难以忍受酷暑）。\n「〜にもかかわらず」— 尽管…却…。例：夏に購入したにもかかわらず（尽管夏天购买）。\n「〜そうです」— 听说…（传闻）。例：約100万円もかかるそうです（听说要花约100万日元）。",
                "vocab": [["標準工事費", "ひょうじゅんこうじひ", "标准安装费"], ["耐えかねる", "たえかねる", "难以忍受"], ["取り付け工事", "とりつけこうじ", "安装工程"], ["人件費", "じんけんひ", "人工费"], ["普及率", "ふきゅうりつ", "普及率"], ["ハードルが高い", "ハードルがたかい", "门槛高、难度大"]]
            }
        ]
    },
    {
        "slug": "matsumoto-family-jiko-kouhan",
        "title": "「涙一つ出ないのか」5人亡くした遺族 被告の淡々とした表情に憤り",
        "subtitle": "from 毎日新聞",
        "paras": [
            {
                "ja": "三重県亀山市の新名神高速道路下り線のトンネル内で3月20日未明、渋滞中の車列に大型トラックが突っ込み計6人が死亡した。車列の最後尾にいたのが、静岡県袋井市の会社員、松本幸司さん（当時45歳）の一家5人だった。幸司さんが運転し、妻恵梨子さんと長女、長男、次女を乗せて大阪のテーマパークに向かっていた。誕生日祝いを兼ねた家族旅行だった。",
                "en": "In the early hours of March 20, a large truck plowed into a line of cars stuck in traffic inside a tunnel on the down line of the Shin-Meishin Expressway in Kameyama City, Mie Prefecture, killing a total of six people. At the very back of the line was the five-member family of Koji Matsumoto (45 at the time), a company employee from Fukuroi City, Shizuoka Prefecture. Koji was driving, carrying his wife Eriko and his eldest daughter, eldest son, and second daughter toward a theme park in Osaka. It was a family trip that also doubled as a birthday celebration.",
                "literal": "在3月20日凌晨，三重县龟山市的新名神高速公路下行线的隧道内，大型卡车撞入拥堵的车列，共造成6人死亡。位于车列最后的是静冈县袋井市的公司职员松本幸司（当时45岁）一家5人。幸司驾车，载着妻子惠梨子、长女、长子和次女前往大阪的主题公园。这是一场兼作生日庆祝的家族旅行。",
                "grammar": "「〜未明」— …凌晨。例：3月20日未明（3月20日凌晨）。\n「〜を兼ねた」— 兼有…、兼作…。例：誕生日祝いを兼ねた旅行（兼作生日庆祝的旅行）。\n「〜に乗せて」— 载着…。例：妻を乗せて（载着妻子）。",
                "vocab": [["突っ込む", "つっこむ", "撞入、冲入"], ["車列", "しゃれつ", "车列、车辆队列"], ["下り線", "くだりせん", "下行线"], ["テーマパーク", "てーまぱーく", "主题公园"], ["渋滞", "じゅうたい", "堵车、拥堵"], ["未明", "みめい", "凌晨"]]
            },
            {
                "ja": "事故は午前2時20分ごろ発生。追突の衝撃で幸司さんは車外に投げ出され、4人を乗せた車も炎上した。恵梨子さんの兄に連絡が入ったのは午前8時半過ぎ。あまりに衝撃的な内容に、兄は当初は「警察をかたった詐欺だろう」と疑った。一方で、恵梨子さんらとは一向に連絡が取れず、繰り返し流れてくる事故のニュースを目にし、現実を受け入れざるを得なかった。",
                "en": "The accident occurred around 2:20 a.m. Koji was thrown from the vehicle by the impact of the rear-end collision, and the car carrying the four others caught fire. Eriko's older brother received the call shortly after 8:30 a.m. Because the content was too shocking, at first he suspected it was 'a scam pretending to be the police.' Meanwhile, he could not get in touch with Eriko and the others at all, and as he saw the accident news repeat over and over, he had no choice but to accept the reality.",
                "literal": "事故发生于凌晨约2点20分。因追尾冲击，幸司被抛出车外，载着4人的车辆也起火燃烧。惠梨子的哥哥接到通知是在上午8点半过后。因内容过于冲击，哥哥起初怀疑是「冒充警察的诈骗吧」。另一方面，完全联系不上惠梨子等人，看到反复播出的事故新闻，不得不接受现实。",
                "grammar": "「〜ざるを得ない」— 不得不…。例：現実を受け入れざるを得なかった（不得不接受现实）。\n「〜一方で」— 另一方面…。例：疑った。一方で（先怀疑，另一方面…）。\n「一向に〜ない」— 完全没有…。例：一向に連絡が取れず（完全联系不上）。",
                "vocab": [["追突", "ついとつ", "追尾、追撞"], ["炎上", "えんじょう", "起火燃烧"], ["かたる", "かたる", "冒充、假冒"], ["受け入れる", "うけいれる", "接受"], ["遺族", "いぞく", "遗属、家属"], ["公判", "こうはん", "公审、开庭审理"]]
            },
            {
                "ja": "大型トラックを運転していた被告は事故直前、スマートフォンで動画投稿アプリの料理動画を約13秒間見ていたとされる。初公判で被告は起訴内容を認めた。検察官が遺族の悲痛な思いを読み上げた時、遺族の目には、被告の表情が淡々とした様子に見えたという。2人は「涙一つ出ないのか。反省や謝罪のかけらも感じなかった」と憤る。",
                "en": "The defendant driving the large truck is said to have watched a cooking video on a video-sharing app on his smartphone for about 13 seconds right before the accident. At his first trial he admitted to the charges. It is said that when the prosecutor read out the bereaved family's painful feelings, the defendant's expression appeared calm and detached in the family's eyes. The two said angrily, 'Could he not shed a single tear? We felt not a shred of remorse or apology.'",
                "literal": "驾驶大型卡车的被告，在事故发生前，据说用智能手机观看视频投稿应用的料理视频约13秒。首次公审上被告承认了起诉内容。当检察官宣读遗属悲痛的心情时，在遗属眼中，被告的表情看起来平淡冷静。两人气愤地说「一滴眼泪都不流吗。感受不到一丝反省和谢罪」。",
                "grammar": "「〜とされる」— 据说…。例：見ていたとされる（据说看了）。\n「〜たという」— 据说…（传闻+引用）。例：淡々とした様子に見えたという（据说看起来平静）。\n「〜かけらもない」— 一丝…也没有。例：反省のかけらも感じなかった（没感到一丝反省）。",
                "vocab": [["淡々と", "たんたんと", "平淡、冷淡"], ["悲痛", "ひつう", "悲痛"], ["起訴内容", "きそないよう", "起诉内容"], ["読み上げる", "よみあげる", "宣读、念出来"], ["謝罪", "しゃざい", "谢罪、道歉"], ["憤る", "いきどおる", "气愤、愤慨"]]
            }
        ]
    },
    {
        "slug": "kouno-tarou-zeigen-hantai",
        "title": "河野太郎氏「消費税減税は『高市政権』のナローパス」 財源10兆円の捻出に警鐘",
        "subtitle": "from 週プレNEWS",
        "paras": [
            {
                "ja": "高市早苗首相は来年4月から2年限定で飲食料品の消費税を1％に引き下げることを表明し、閣議決定に至った。しかし、河野太郎議員は今も自民党内でこの減税に反対し続けている。「高市政権が飲食料品にかかる消費税を8％から1％に下げることを決めましたが、私は反対です。減税をするとさまざまなデメリットが生じる一方で、メリットは国民が期待したほどのものにならない可能性が高いからです」。",
                "en": "Prime Minister Sanae Takaichi announced she would cut the consumption tax on food and beverages to 1% for a limited period of two years from next April, leading to a Cabinet decision. However, lawmaker Taro Kono continues to oppose this tax cut within the Liberal Democratic Party. 'The Takaichi administration has decided to lower the consumption tax on food and beverages from 8% to 1%, but I am opposed. This is because while a tax cut produces various demerits, it is highly likely that the merits will not be as much as the public expects.'",
                "literal": "高市早苗首相表明自明年4月起，限时2年将饮食料品的消费税降至1%，并达到阁议决定。然而，河野太郎议员至今仍在自民党内持续反对这一减税。「高市政权决定将饮食料品的消费税从8%降至1%，但我反对。因为减税会带来各种弊端，而好处很可能达不到国民期待的程度」。",
                "grammar": "「〜に至った」— 达到…、最终…。例：閣議決定に至った（达到阁议决定）。\n" 
                "「〜一方で」— 一方面…另一方面…。例：デメリットが生じる一方で（一方面产生弊端，另一方面…）。\n「〜ほどのものにならない」— 达不到…的程度。例：期待したほどのものにならない（达不到期待的程度）。",
                "vocab": [["表明", "ひょうめい", "表明、声明"], ["閣議決定", "かくぎけってい", "内阁会议决定"], ["減税", "げんぜい", "减税"], ["デメリット", "でめりっと", "弊端、缺点"], ["メリット", "めりっと", "好处、优点"], ["反対", "はんたい", "反对"]]
            },
            {
                "ja": "河野氏は、この2年間の減税で必要となる財源は約10兆円だが、その捻出方法がまだ決まっていないと指摘する。「もし公債発行で賄った場合は、日本の財政に対するマーケットの信認が損なわれ、円安、金利高を加速させるリスクがあります。その先に待つのはさらなるインフレです。物価高対策としての減税なのに、さらなる物価高を招く。これではなんのための減税かわかりません」。",
                "en": "Kono points out that the funds needed for this two-year tax cut amount to about 10 trillion yen, but how to secure them has not yet been decided. 'If it is covered by issuing government bonds, market confidence in Japan's fiscal situation would be damaged, creating a risk of accelerating a weak yen and higher interest rates. What awaits beyond that is further inflation. Even though this is a tax cut meant as a measure against rising prices, it would invite even higher prices. At that point, I don't know what the tax cut is for.'",
                "literal": "河野指出，这2年减税所需的财源约10万亿日元，但其筹措方法尚未确定。「如果用发行公债来填补，会损害市场对日本财政的信赖，存在加速日元贬值、利率上升的风险。之后等待的是进一步的通货膨胀。明明是作为物价高涨对策的减税，却招致进一步的物价高涨。这样一来就不知道减税是为了什么」。",
                "grammar": "「〜を損なう」— 损害…。例：信認が損なわれ（损害信赖）。\n「〜リスクがあります」— 有…的风险。例：加速させるリスクがあります（有加速的风险）。\n「〜を招く」— 招致…。例：さらなる物価高を招く（招致进一步的物价高涨）。",
                "vocab": [["財源", "ざいげん", "财源、资金来源"], ["捻出", "ねんしゅつ", "筹措、腾挪"], ["公債発行", "こうさいはっこう", "发行公债"], ["信認", "しんにん", "信赖、信任"], ["円安", "えんやす", "日元贬值"], ["金利高", "きんりだか", "利率上升、高息"]]
            },
            {
                "ja": "与野党が消費税減税の是非を協議する社会保障国民会議の議論は混迷を極めた。河野氏は、今回の減税によってダメージを受ける業界として外食産業や農業を挙げ、「高市政権はナローパス（選択肢が限られ、困難な状況）の中で減税をやろうとしているように見えてなりません」と警鐘を鳴らす。",
                "en": "The deliberations of the Social Security National Conference, where ruling and opposition parties discuss the merits of the consumption tax cut, reached a state of great confusion. Kono cited the restaurant industry and agriculture as industries that would be damaged by this tax cut, and raised a warning, saying, 'The Takaichi administration appears to be trying to carry out the tax cut within a narrow pass (a difficult situation with limited options).'",
                "literal": "执政党与在野党就消费减税是非进行协商的社会保障国民会议讨论陷入极度混乱。河野举出此次减税会受损的行业为外食产业和农业，发出警示称「高市政权看起来像是在狭窄通道（选择受限、困难的状况）中试图进行减税」。",
                "grammar": "「〜を極める」— 达到极点、…至极。例：混迷を極めた（陷入极度混乱）。\n「〜してなりません」— 不禁感到…。例：見えてなりません（不禁觉得…）。\n「〜を挙げる」— 举出…。例：外食産業や農業を挙げ（举出外食产业和农业）。",
                "vocab": [["混迷", "こんめい", "混乱、迷乱"], ["外食産業", "がいしょくさんぎょう", "餐饮业、外食产业"], ["警鐘", "けいしょう", "警钟、警示"], ["ナローパス", "なろーぱす", "狭窄通道、艰难处境"], ["選択肢", "せんたくし", "选择项"], ["ダメージ", "だめーじ", "损害、伤害"]]
            }
        ]
    },
    {
        "slug": "konji-otto-nanbyou-chichi",
        "title": "難病の息子「病気を理由に我慢する必要はない」 父が語る子育ての願い",
        "subtitle": "from CHANTO Web",
        "paras": [
            {
                "ja": "難病「レックリングハウゼン病」によって顔に腫瘍ができ、歩行には装具を必要とする村上泰大さんの三男・魂児さん。幼い頃から周囲の心ない視線に傷つきながらも、小学6年生にして自身の病気についてSNSで発信を行うなど、積極的に社会との関わりを持ってきました。そこには「病気を理由に我慢する必要はない」という、父・泰大さんの願いがありました。",
                "en": "Konji, the third son of Mr. Yasuhiro Murakami, has tumors on his face due to the intractable disease 'neurofibromatosis,' and needs a brace for walking. Even as he was hurt by the thoughtless looks of those around him from an early age, he actively engaged with society, such as sharing information about his illness on social media even as an elementary school sixth-grader. Behind this was his father Yasuhiro's wish that 'there is no need to endure because of illness.'",
                "literal": "因难病「雷克林豪森病」，脸上长出肿瘤、步行需要装具的村上泰大的三男・魂儿。从小虽被周围无心目光所伤，却从小学六年级起就在SNS上发布关于自己疾病的信息，积极与社会建立联系。其背后有父亲泰大「不必以疾病为理由忍耐」的愿望。",
                "grammar": "「〜ながらも」— 虽然…却…。例：傷つきながらも（虽然受伤却…）。\n「〜にして」— 即便在（年纪）…。例：小学6年生にして（即便只是小学六年级）。\n「〜を理由に」— 以…为理由。例：病気を理由に我慢する（以疾病为理由忍耐）。",
                "vocab": [["難病", "なんびょう", "难病、疑难杂症"], ["腫瘍", "しゅよう", "肿瘤"], ["装具", "そうぐ", "装具、护具"], ["心ない", "こころない", "无心的、没分寸的"], ["発信", "はっしん", "发布、发信"], ["我慢", "がまん", "忍耐、忍受"]]
            },
            {
                "ja": "病院から子どもが生まれたと連絡が来て職場からすぐに駆けつけると、魂児は別室にいると言われました。別室で対面を果たしたのですが、なんだか顔に違和感がある。その後、妻の病室に戻ると先生が来て、「ちょっと気になることがある」と言われ、すぐに大学病院に救急搬送されたんです。何がなんだかよくわからないまま、生まれて4、5時間後に病理検査のための摘出手術をすることになりました。",
                "en": "When he received word from the hospital that his child had been born and rushed over from work, he was told that Konji was in a separate room. He met him in that separate room, but somehow felt something was off about his face. Later, when he returned to his wife's hospital room, a doctor came and said, 'There's something a bit concerning,' and Konji was immediately taken by ambulance to a university hospital. Not understanding what was happening, about four or five hours after birth, he underwent surgery to remove the tumor for a pathology exam.",
                "literal": "接到医院通知孩子出生、从单位立刻赶去后，被告知魂儿在别的房间。在那个房间见了面，但总觉得脸上有异样感。之后回到妻子病房时医生来了，说「有点在意的事」，随即被紧急送往大学医院。在完全搞不清状况的情况下，出生仅4、5小时后，就进行了用于病理检查的摘除手术。",
                "grammar": "「〜駆けつける」— 匆忙赶到。例：職場からすぐに駆けつけると（从单位立刻赶到）。\n「〜違和感がある」— 有异样感。例：顔に違和感がある（脸上有异样感）。\n「〜ことになりました」— 结果变成…（客观决定）。例：摘出手術をすることに（结果要做摘除手术）。",
                "vocab": [["駆けつける", "かけつける", "匆忙赶到"], ["違和感", "いわかん", "异样感、违和感"], ["救急搬送", "きゅうきゅうはんそう", "紧急送医"], ["病理検査", "びょうりけんさ", "病理检查"], ["摘出", "てきしゅつ", "摘除、切除"], ["対面", "たいめん", "见面、对面"]]
            },
            {
                "ja": "病理検査の結果、難病と言われましたが、初めて聞く名前だし、難病と言われても実感がすぐにはわかなかったですね。医師からは、顔の腫瘍は成長とともに少しずつ増えて、腫瘍自体も大きくなり、腫瘍の重みで顔が垂れ下がる。外見にも変化が現れると説明を受けました。また視神経にも腫瘍がある影響で緑内障もあり、左目はかすかな光程度しか見えていないと言われました。",
                "en": "As a result of the pathology exam, he was told it was an intractable disease, but it was a name he had never heard before, and even being told it was an intractable disease, he could not immediately grasp the reality of it. The doctors explained that the tumors on his face would gradually increase as he grew, the tumors themselves would enlarge, and his face would sag under their weight, with changes also appearing in his appearance. He was also told that due to tumors affecting the optic nerve he had glaucoma, and his left eye could only perceive faint light at best.",
                "literal": "病理检查的结果被告知是难病，但因为是第一次听到的名字，即使说是难病也没有立刻产生实感。医生说明道，脸上的肿瘤会随成长逐渐增多，肿瘤本身也会变大，因肿瘤重量脸部会下垂，外观也会出现变化。另外据说因视神经也有肿瘤而患青光眼，左眼几乎只能看到微弱的亮光。",
                "grammar": "「〜だし」— 因为…又…（列举理由）。例：初めて聞く名前だし（因为是第一次听到的名字）。\n「〜とともに」— 随着…。例：成長とともに増えて（随着成长而增多）。\n「〜程度しか〜ない」— 只有…（程度的）而已。例：かすかな光程度しか見えていない（只能看到微弱的光）。",
                "vocab": [["実感", "じっかん", "实感、切身体会"], ["視神経", "ししんけい", "视神经"], ["緑内障", "りょくないしょう", "青光眼"], ["かすか", "かすか", "微弱、模糊"], ["病変", "びょうへん", "病变"], ["垂れ下がる", "たれさがる", "下垂、向下挂"]]
            }
        ]
    }
]


processed = []
for art in articles:
    slug = art['slug']
    title = art['title']
    print(f"\n{'='*60}\n📰 {title}")

    paragraphs_out = []
    for i, p in enumerate(art['paras']):
        paragraphs_out.append({
            "id": f"p{i+1}",
            "ja": p['ja'],
            "en": p['en'],
            "literal": p['literal'],
            "grammar": p['grammar'],
            "vocab": p['vocab'],
            "words": tokenize_text(p['ja']),
            "audio": f"assets/audio/{slug}/p{i+1}.mp3"
        })

    reading = [{
        "id": slug,
        "title": title,
        "subtitle": art['subtitle'],
        "level": "中級",
        "length": len(art['paras']),
        "date": TODAY,
        "paragraphs": paragraphs_out
    }]

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
        p0 = d[0]['paragraphs'][0]
        gt = type(p0['grammar']).__name__
        vt = type(p0['vocab']).__name__
        v0t = type(p0['vocab'][0]).__name__
        pc = len(d[0]['paragraphs'])
        audio_ok = True
        for i in range(pc):
            ap = f'{BASE}/assets/audio/{slug}/p{i+1}.mp3'
            if not os.path.exists(ap):
                audio_ok = False
        if audio_ok and gt == 'str' and vt == 'list' and v0t == 'list':
            ok += 1
            print(f"   ✅ {slug}: {pc} paragraphs, grammar={gt}, vocab={vt}/{v0t}, audio OK")
        else:
            print(f"   ⚠️ {slug}: type={gt}/{vt}/{v0t} audio_ok={audio_ok}")
print(f"\n{ok}/{len(processed)} articles verified")
