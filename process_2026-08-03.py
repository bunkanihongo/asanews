#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-03 (Mon) Edition"""
import json, os, subprocess, re, time
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-03'
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
# TODAY'S ARTICLES — 2026-08-03
# ==================================================================
articles = [
    {
        "slug": "habita-kanai-modosu-siji",
        "title": "イオン熊本爆発 死亡の従業員2人「館内へ戻るよう指示」と運営会社が認める",
        "subtitle": "「イオンモール熊本」の爆発で女性従業員2人が死亡した雑貨店の運営会社「ハビタ」の幹部が、2人が地震後に一時避難した後、売上金を金庫に移すため館内に戻るよう指示したと明らかにした。",
        "paras": [
            {
                "ja": "「イオンモール熊本」（熊本県嘉島町）で7月28日に起きた爆発で、女性従業員2人が死亡した雑貨店の運営会社「ハビタ」の幹部2人が2日、報道陣の取材に応じました。幹部は、亡くなった2人が地震後に一時避難した後、売上金を金庫に移すため、会社側が館内に戻るよう指示したと明らかにしました。また、1人の通夜に参列した際、遺族に謝罪し、一連の経緯をまとめた書面を渡したということです。",
                "en": "Two executives of Habita, the company that runs the general goods store where two female employees died in the explosion at Aeon Mall Kumamoto (Kashima Town, Kumamoto Prefecture) on July 28, spoke to the press on the 2nd. They revealed that after the two women briefly evacuated following the earthquake, the company instructed them to return inside the mall to move the day's sales into the safe. They also apologized to the bereaved family at one of the wakes and handed over a document summarizing the sequence of events.",
                "literal": "7月28日在「永旺商城熊本」（熊本县嘉岛町）发生的爆炸中，2名女性员工死亡的杂货店运营公司「哈比塔」的2名高管于2日接受了记者采访。高管表示，2名死者在地震后一度避难之后，公司方面为了把营业收入转移到金库，指示她们返回馆内。此外，在出席其中一人的守夜仪式时，向遗属道歉，并递交了汇总事件经过的书面材料。",
                "grammar": "「〜に応じました」— 接受了…（采访等）。例：報道陣の取材に応じました（接受了记者采访）。\n「〜と明らかにしました」— 明确表示…。例：指示したと明らかにしました（明确表示做出了指示）。\n「〜ということです」— 据说…。例：書面を渡したということです（据说递交了书面材料）。",
                "vocab": [
                    ["運営会社", "うんえいがいしゃ", "运营公司"],
                    ["幹部", "かんぶ", "高管、干部"],
                    ["避難", "ひなん", "避难"],
                    ["売上金", "うりあげきん", "营业收入"],
                    ["金庫", "きんこ", "金库"],
                    ["遺族", "いぞく", "遗属"]
                ]
            },
            {
                "ja": "遺族によると、亡くなった1人は熊本市の大竹玖瑠美さん（22）です。7月28日の地震の後、いったん外に出ましたが、館内に戻るのが目撃されていました。会社側から謝罪を受けた大竹さんの母親は「（娘は）帰ってこないんですよ」と泣きながら訴えました。通夜には多くの友人らが訪れ、大竹さんを悼みました。",
                "en": "According to the bereaved family, one of the deceased was Kurumi Otake (22) from Kumamoto City. After the earthquake on July 28, she briefly went outside, but was seen returning inside the mall. Otake's mother, who received the apology from the company, sobbed, \"(My daughter) isn't coming home.\" Many friends visited the wake to mourn her.",
                "literal": "据遗属称，死者之一是熊本市的大竹玖瑠美（22岁）。7月28日地震后，她一度到了外面，但有人目击到她返回馆内。接受公司方面道歉的大竹母亲哭着诉说「（女儿）不会回来了」。守夜仪式上有许多朋友前来悼念大竹。",
                "grammar": "「〜によると」— 据…称。例：遺族によると（据遗属称）。\n「〜のが目撃されていました」— 有人目击到…（被动态）。例：館内に戻るのが目撃されていました（有人目击到她返回馆内）。\n「〜ながら」— 一边…一边…。例：泣きながら訴えました（一边哭一边诉说）。",
                "vocab": [
                    ["目撃", "もくげき", "目击"],
                    ["謝罪", "しゃざい", "道歉"],
                    ["訴える", "うったえる", "诉说、控诉"],
                    ["悼む", "いたむ", "哀悼"],
                    ["帰ってくる", "かえってくる", "回来"],
                    ["訪れる", "おとずれる", "到访、来临"]
                ]
            },
            {
                "ja": "ハビタの営業部長は報道陣の取材に「今から考えると、命に代えるものではない」と述べました。ハビタのホームページによると、同社は1976年創業で、熊本など九州で十数店舗を運営しています。爆発は28日午後5時50分ごろ発生し、2人を含め計7人が死亡しました。イオンは29日に開いた会見で、7人が館内にいた理由は不明としていました。警察や消防は、爆発の詳しい原因を調べています。",
                "en": "Habita's sales department manager told the press, \"Looking back now, it was not something worth trading for lives.\" According to Habita's website, the company was founded in 1976 and operates more than a dozen stores in Kyushu, including Kumamoto. The explosion occurred around 5:50 p.m. on the 28th, killing seven people in total, including the two women. At a press conference held on the 29th, Aeon said the reason the seven people were inside the mall was unknown.",
                "literal": "哈比塔的营业部长对记者表示「现在回想起来，这不是可以用生命来交换的东西」。根据哈比塔官网，该公司1976年创业，在熊本等九州地区运营十几家店铺。爆炸发生在28日下午5点50分左右，包括2名女性在内共7人死亡。永旺在29日召开的记者会上表示，7人在馆内的原因不明。",
                "grammar": "「〜に代えるものではない」— 不是能用…交换的。例：命に代えるものではない（不是能用生命交换的东西）。\n「〜によると」— 根据…。例：ホームページによると（根据官网）。\n「〜ごろ」— 大约…（时间）。例：午後5時50分ごろ発生しました（下午5点50分左右发生）。",
                "vocab": [
                    ["営業部長", "えいぎょうぶちょう", "营业部长"],
                    ["創業", "そうぎょう", "创业"],
                    ["十数店舗", "じゅうすうてんぽ", "十几家店铺"],
                    ["発生", "はっせい", "发生"],
                    ["計", "けい", "共计"],
                    ["会見", "かいけん", "记者会"]
                ]
            }
        ]
    },
    {
        "slug": "jishingumo-gosoku-chuui",
        "title": "地震と雲を関係付ける誤情報に注意 命を守るための「正しい防災」とは",
        "subtitle": "熊本地震の後、SNSに「地震雲」に関する投稿が見られる。気象庁は「雲は大気の現象、地震は大地の現象で、両者は全く別」と説明。珍しい雲の科学的な理由と正しい防災を解説する。",
        "paras": [
            {
                "ja": "7月28日に熊本県で最大震度7を観測した地震のあと、SNSに地震発生と雲を関係付ける投稿が見受けられます。大きな災害が起こって不安なときに、たまたま珍しい雲を見つけてしまうと、驚いてしまうこともあるかもしれません。しかし、気象庁は「雲は大気の現象であり、地震は大地の現象で、両者は全く別の現象です」という見解を示しており、いわゆる「地震雲」について、現時点では科学的な説明はできていないとしています。",
                "en": "After the earthquake that recorded a maximum seismic intensity of 7 in Kumamoto Prefecture on July 28, posts linking the earthquake to clouds have been appearing on social media. When you are anxious after a major disaster, you might be startled if you happen to spot an unusual cloud. However, the Japan Meteorological Agency has long stated its view that \"clouds are an atmospheric phenomenon and earthquakes are a terrestrial phenomenon — the two are completely different,\" and says that so-called \"earthquake clouds\" cannot currently be scientifically explained.",
                "literal": "7月28日在熊本县观测到最大震度7的地震之后，社交网络上可以看到将地震发生与云联系起来的帖子。发生大灾害感到不安的时候，如果碰巧发现了罕见的云，有时也许会被吓到。但是，气象厅一直表示「云是大气现象，地震是大地现象，两者是完全不同的现象」，关于所谓的「地震云」，目前认为无法进行科学的说明。",
                "grammar": "「〜てしまう」— 表示动作的完成或遗憾。例：見つけてしまうと（一旦发现的话）。\n「〜かもしれません」— 也许、可能。例：驚いてしまうこともあるかもしれません（有时也许会被吓到）。\n「〜としています」— 认为…、主张…。例：説明はできていないとしています（认为无法说明）。",
                "vocab": [
                    ["最大震度", "さいだいしんど", "最大震度"],
                    ["観測", "かんそく", "观测"],
                    ["見受けられる", "みうけられる", "能看到、能发现"],
                    ["たまたま", "たまたま", "碰巧"],
                    ["気象庁", "きしょうちょう", "气象厅"],
                    ["見解", "けんかい", "见解、看法"]
                ]
            },
            {
                "ja": "珍しい形や変わった色の雲が発生すると「地震雲では？」と騒がれることがあります。しかし、どんなに珍しくても、雲がその形や色になるには科学的な理由があります。例えば「吊るし雲（レンズ雲）」は、上空の強い風が山を越えるときの風の波によってできる雲の一種で、富士山周辺などでときどき見られます。地震の予知にはなりませんが、天気が下り坂に向かうサインとして知られています。もくもくと上に伸びて、上の方がキノコのように広がる雲は「かなとこ雲」と呼ばれ、発達した積乱雲が空の天井にぶつかって横に広がることでできます。この雲の下は、大抵、激しい雨や雷雨になっています。",
                "en": "When clouds of unusual shapes or colors appear, people sometimes make a fuss asking, \"Could these be earthquake clouds?\" But no matter how unusual they seem, there is a scientific reason why clouds take that shape or color. For example, \"hanging clouds\" (lenticular clouds) are a type of cloud formed by waves in strong winds as they cross mountains, and are occasionally seen around Mount Fuji. They cannot predict earthquakes, but they are known as a sign that the weather is turning for the worse. Clouds that billow upward and spread out like a mushroom at the top are called \"anvil clouds,\" formed when a developed cumulonimbus cloud hits the ceiling of the sky and spreads sideways. Beneath such clouds, there are usually heavy rain or thunderstorms.",
                "literal": "出现形状奇特或颜色异常的云时，有时会被炒作成「是不是地震云？」。但是，无论看起来多么罕见，云变成那种形状或颜色都有科学的理由。例如「吊云（透镜云）」是上空强风翻越山岭时产生的风波形成的一种云，在富士山周边等地偶尔能看到。它不能预测地震，但作为天气将变坏的信号而为人所知。蓬蓬勃勃向上伸展、顶端像蘑菇一样展开的云叫做「铁砧云」，是发展旺盛的积雨云撞到天空的天花板后向横扩展而形成的。这种云的下方，大多是猛烈的降雨或雷雨。",
                "grammar": "「〜では？」— 是不是…呢。例：地震雲では？（是不是地震云？）。\n「〜によってできる」— 由…形成。例：風の波によってできる雲（由风波形成的云）。\n「〜として知られています」— 作为…而为人所知。例：サインとして知られています（作为信号而知名）。",
                "vocab": [
                    ["珍しい", "めずらしい", "罕见的、稀奇的"],
                    ["騒がれる", "さわがれる", "被炒作、引起议论"],
                    ["吊るし雲", "つるしぐも", "吊云、透镜云"],
                    ["予知", "よち", "预知"],
                    ["下り坂", "くだりざか", "下坡、转坏"],
                    ["積乱雲", "せきらんうん", "积雨云"]
                ]
            },
            {
                "ja": "雲の一部が緑やピンク、黄色など色がついて見えるものを「彩雲」といいます。太陽の近くに巻積雲や高積雲がかかっているときに見られることが多く、光が雲粒を回り込んで進む「回折」によってこのような色になります。SNSの情報をうのみにせず、地震が起きたときは、気象庁や自治体の公式情報をもとに、落ち着いて行動することが大切です。",
                "en": "Clouds whose parts appear tinted green, pink, yellow, or other colors are called \"saiun\" (iridescent clouds). They are often seen when cirrocumulus or altocumulus clouds hang near the sun, and the colors result from \"diffraction,\" in which light bends around cloud particles. Rather than swallowing social media information whole, when an earthquake occurs it is important to act calmly based on official information from the Japan Meteorological Agency and local governments.",
                "literal": "云的一部分看起来带上了绿色、粉色、黄色等颜色的叫做「彩云」。在太阳附近有卷积云或高积云笼罩时经常能看到，光绕过云粒前进的「衍射」使它呈现出这样的颜色。不要囫囵吞枣地相信社交网络的信息，地震发生时，以气象厅和地方政府等官方信息为基础，冷静地行动是很重要的。",
                "grammar": "「〜といいます」— 叫做…。例：彩雲といいます（叫做彩云）。\n「〜によって」— 由于…、通过…。例：回折によってこのような色になります（由于衍射呈现出这样的颜色）。\n「〜をうのみにせず」— 不囫囵吞枣地相信…。例：SNSの情報をうのみにせず（不盲信社交网络的信息）。",
                "vocab": [
                    ["彩雲", "さいうん", "彩云"],
                    ["巻積雲", "けんせきうん", "卷积云"],
                    ["回折", "かいせつ", "衍射"],
                    ["うのみにする", "うのみにする", "囫囵吞枣、盲目相信"],
                    ["自治体", "じちたい", "地方政府、自治体"],
                    ["公式情報", "こうしきじょうほう", "官方信息"]
                ]
            }
        ]
    },
    {
        "slug": "kihara-nijuu-saigai-mousho",
        "title": "木原官房長官「今年の猛暑、まさに二重の災害」 災害関連死の抑制へ対策",
        "subtitle": "熊本県は車中泊避難をしていた70代の女性が熱中症の疑いで死亡したとみられることを発表。木原官房長官は猛暑と地震の「二重の災害」と述べ、災害関連死の抑制に力を入れる考えを示した。",
        "paras": [
            {
                "ja": "木原官房長官は2日、令和8年熊本地震について「今年の夏の猛暑、まさに二重の災害というべき状況だと認識している」と強調した上で、災害関連死への対策に力を入れる考えを示しました。熊本県は同日、車中泊避難をしていた70代の女性が、熱中症の疑いで死亡したとみられることを発表しました。",
                "en": "Chief Cabinet Secretary Kihara, speaking on the 2nd about the Reiwa 8 Kumamoto earthquake, emphasized that \"this summer's extreme heat is truly a situation that should be called a double disaster,\" and showed his intention to focus on measures against disaster-related deaths. On the same day, Kumamoto Prefecture announced that a woman in her 70s who had been evacuating by sleeping in her car is believed to have died of suspected heatstroke.",
                "literal": "木原官房长官2日就令和8年熊本地震表示「我认识到今年夏天的酷暑，正是应该称为双重灾害的状况」，并在此基础上表明了着力于灾害相关死亡对策的想法。熊本县同一天公布了，一名在车中过夜避难的70多岁女性疑似因中暑死亡。",
                "grammar": "「〜というべき」— 可以说…、应该称为…。例：二重の災害というべき状況（应该称为双重灾害的状况）。\n「〜た上で」— 在…的基础上。例：強調した上で（在强调的基础上）。\n「〜とみられる」— 被认为…。例：死亡したとみられます（被认为已经死亡）。",
                "vocab": [
                    ["官房長官", "かんぼうちょうかん", "内阁官房长官"],
                    ["猛暑", "もうしょ", "酷暑"],
                    ["二重の災害", "にじゅうのさいがい", "双重灾害"],
                    ["災害関連死", "さいがいかんれんし", "灾害相关死亡"],
                    ["車中泊", "しゃちゅうはく", "在车里过夜"],
                    ["熱中症", "ねっちゅうしょう", "中暑"]
                ]
            },
            {
                "ja": "総理大臣官邸で記者団の取材に応じた木原長官は、「今回、熱中症の疑いで車中で亡くなられた方に心からお悔やみを申し上げる」と述べました。その上で「最終的に災害関連死をいかに抑制していくかに軸足を置いていく」と強調し、「冷房や水の確保をはじめ、避難所の良好な環境をしっかりと整備することが必要だ」と述べました。",
                "en": "Responding to reporters at the Prime Minister's Official Residence, Kihara said, \"I offer my heartfelt condolences to the person who died in a car of suspected heatstroke this time.\" He then stressed that \"we will put our focus on how to ultimately curb disaster-related deaths,\" adding that \"it is necessary to properly prepare a good environment at evacuation centers, including securing air conditioning and water.\"",
                "literal": "在总理大臣官邸接受记者采访的木原长官表示「此次，向疑似中暑在车中去世的人致以衷心的哀悼」。在此基础上他强调「最终将以如何抑制灾害相关死亡为重点」，并表示「有必要切实完善以冷气和饮水保障为首的避难所良好环境」。",
                "grammar": "「〜に応じた」— 接受了…。例：取材に応じた（接受了采访）。\n「〜をはじめ」— 以…为首、包括…。例：冷房や水の確保をはじめ（包括冷气和饮水的保障）。\n「〜が必要だ」— 有必要…。例：整備することが必要だ（有必要进行完善）。",
                "vocab": [
                    ["官邸", "かんてい", "官邸"],
                    ["お悔やみ", "おくやみ", "哀悼、吊唁"],
                    ["抑制", "よくせい", "抑制"],
                    ["軸足を置く", "じくあしをおく", "以…为重点"],
                    ["冷房", "れいぼう", "冷气、空调"],
                    ["避難所", "ひなんじょ", "避难所"]
                ]
            },
            {
                "ja": "また、被災者への保健・医療・福祉支援について、避難所だけでなく、在宅避難や車中泊避難をしている被災者に対しても、行政職員が自ら出向くよう指示したことを明らかにしました。2日には熊本県宇土市でホテルや旅館への避難の取り組みが開始されたほか、宇城市と氷川町では3日から建設型応急住宅の設置工事に着手する見込みです。さらに、3日に高市総理大臣が被災地を視察する予定で、今後の被災支援の充実につなげる考えです。避難生活の長期化も懸念されており、被災者の健康管理が重要な課題となっています。",
                "en": "He also revealed that he had instructed administrative staff to proactively visit affected residents — not only those in evacuation centers, but also those evacuating at home or sleeping in their cars — for health, medical, and welfare support. On the 2nd, efforts to evacuate people to hotels and inns began in Uto City, Kumamoto Prefecture, and construction of prefabricated emergency housing is expected to start in Uki City and Hikawa Town on the 3rd. Furthermore, Prime Minister Takaichi is scheduled to visit the disaster area on the 3rd, with the aim of enhancing future support for victims.",
                "literal": "此外，关于对受灾者的保健・医疗・福祉支援，他明确表示已指示行政职员亲自上门走访，不仅针对避难所，也针对在家避难和车中过夜避难的受灾者。2日，熊本县宇土市开始了转移到酒店和旅馆避难的举措，宇城市和冰川町预计3日开始着手建设型应急住宅的安装工程。另外，高市总理大臣预定3日视察灾区，考虑将其与今后充实受灾支援联系起来。",
                "grammar": "「〜だけでなく〜も」— 不仅…而且…。例：避難所だけでなく、在宅避難の被災者にも（不仅是避难所，也包括在家避难的受灾者）。\n「〜見込みです」— 预计…。例：着手する見込みです（预计将着手）。\n「〜につなげる」— 与…联系起来、用于…。例：支援の充実につなげる（用于充实支援）。",
                "vocab": [
                    ["被災者", "ひさいしゃ", "受灾者"],
                    ["出向く", "でむく", "前往、亲自上门"],
                    ["旅館", "りょかん", "日式旅馆"],
                    ["建設型応急住宅", "けんせつがたおうきゅうじゅうたく", "建设型应急住宅"],
                    ["着手", "ちゃくしゅ", "着手"],
                    ["視察", "しさつ", "视察"]
                ]
            }
        ]
    },
    {
        "slug": "takaichi-shijiritsu-teika",
        "title": "高市内閣の支持率59.2% 先月調査から6.7ポイント下落 JNN世論調査",
        "subtitle": "JNNの世論調査で高市内閣の支持率が59.2%となり、先月から6.7ポイント下落した。「支持しない」は37.6%で6.8ポイント上昇した。",
        "paras": [
            {
                "ja": "最新のJNNの世論調査で、高市内閣の支持率が先月の調査から6.7ポイント下落して59.2%でした。先月の調査では65.9%で、支持率は50%を超える高い水準が続いています。一方、「支持しない」と答えた人は、先月から6.8ポイント上昇して37.6%でした。下落の背景には、熊本地震への対応や物価高などへの評価が影響しているとみられます。",
                "en": "In the latest JNN opinion poll, the approval rating of the Takaichi Cabinet fell 6.7 points from last month's survey to 59.2%. In last month's survey it was 65.9%, and the rating continues to hold a high level above 50%. Meanwhile, those who answered that they \"do not support\" the cabinet rose 6.8 points from last month to 37.6%. The decline appears to be influenced by assessments of the response to the Kumamoto earthquake and high prices.",
                "literal": "在最新的JNN舆论调查中，高市内阁的支持率比上个月的调查下降6.7个百分点，为59.2%。上个月的调查为65.9%，支持率持续保持在超过50%的高水平。另一方面，回答「不支持」的人比上个月上升6.8个百分点，达到37.6%。下滑的背景被认为受到对熊本地震的应对以及物价上涨等的评价的影响。",
                "grammar": "「〜ポイント下落して」— 下降了…个百分点。例：6.7ポイント下落して59.2%でした（下降6.7个百分点，为59.2%）。\n「〜一方」— 另一方面。例：一方、「支持しない」と答えた人は（另一方面，回答「不支持」的人）。\n「〜とみられます」— 被认为…。例：影響しているとみられます（被认为产生了影响）。",
                "vocab": [
                    ["世論調査", "よろんちょうさ", "舆论调查"],
                    ["支持率", "しじりつ", "支持率"],
                    ["ポイント", "ぽいんと", "百分点"],
                    ["下落", "げらく", "下跌、下滑"],
                    ["水準", "すいじゅん", "水平"],
                    ["物価高", "ぶっかだか", "物价上涨"]
                ]
            },
            {
                "ja": "政党の支持率は、自民党が30.9%、国民民主党が3.0%、日本維新の会が2.9%などとなりました。また、「支持する政党はない」と答えた人は46.4%に上りました。各党の支持率は、前回調査と比べて大きな変動は見られませんでした。内閣支持率は、国民が現在の内閣をどの程度支持しているかを示す数字で、政治の安定度を測る目安の一つとされています。",
                "en": "Among party support ratings, the Liberal Democratic Party stood at 30.9%, the Democratic Party for the People at 3.0%, and Nippon Ishin at 2.9%. Moreover, those who said they \"support no party\" rose to 46.4%. The cabinet approval rating is a figure showing how much the public supports the current cabinet, and is regarded as one of the benchmarks for measuring the stability of politics.",
                "literal": "政党的支持率方面，自民党为30.9%，国民民主党为3.0%，日本维新会为2.9%等。另外，回答「没有支持的政党」的人上升到46.4%。内阁支持率是显示国民在多大程度上支持现任内阁的数字，被认为是衡量政治稳定度的标准之一。",
                "grammar": "「〜などとなりました」— 为…等等。例：2.9%などとなりました（为2.9%等等）。\n「〜に上りました」— 达到…（数量）。例：46.4%に上りました（达到46.4%）。\n「〜とされています」— 被认为是…。例：目安の一つとされています（被认为是标准之一）。",
                "vocab": [
                    ["政党", "せいとう", "政党"],
                    ["自民党", "じみんとう", "自民党"],
                    ["上回る", "うわまわる", "超过"],
                    ["目安", "めやす", "标准、大致基准"],
                    ["安定度", "あんていど", "稳定度"],
                    ["測る", "はかる", "测量、衡量"]
                ]
            },
            {
                "ja": "調査は8月1日と2日、全国の18歳以上の男女2851人を対象に行われました。コンピューターで無作為に数字を組み合わせ、固定電話と携帯電話の両方にかけて行う「RDD方式」を採用しています。そのうち36.2%にあたる1033人から有効な回答を得ました。JNNの世論調査は毎月実施されており、内閣や政党への評価の移り変わりを把握する材料となっています。",
                "en": "The survey was conducted on August 1 and 2, targeting 2,851 men and women aged 18 or older nationwide. It employs the \"RDD method,\" in which numbers are randomly generated by computer and calls are made to both landlines and mobile phones. Valid responses were obtained from 1,033 people, or 36.2% of the total.",
                "literal": "调查于8月1日和2日实施，以全国18岁以上的男女2851人为对象。采用计算机随机组合数字、同时拨打固定电话和手机的「RDD方式」。其中获得了相当于36.2%的1033人的有效回答。",
                "grammar": "「〜を対象に」— 以…为对象。例：2851人を対象に行われました（以2851人为对象实施）。\n「〜にあたる」— 相当于…。例：36.2%にあたる1033人（相当于36.2%的1033人）。\n「〜を得ました」— 获得了…。例：有効な回答を得ました（获得了有效回答）。",
                "vocab": [
                    ["無作為", "むさくい", "随机"],
                    ["固定電話", "こていでんわ", "固定电话"],
                    ["携帯電話", "けいたいでんわ", "手机"],
                    ["採用", "さいよう", "采用"],
                    ["有効", "ゆうこう", "有效"],
                    ["回答", "かいとう", "回答"]
                ]
            }
        ]
    },
    {
        "slug": "kuwaki-shiho-zen-ei-v",
        "title": "桑木志帆が涙の日本勢7人目メジャーV 渋野日向子に続く全英制覇",
        "subtitle": "海外女子メジャー「AIG女子オープン」最終日、23歳の桑木志帆がプレーオフの末に初優勝。日本勢3人目の全英Vで、海外メジャー優勝は7人目の快挙となった。",
        "paras": [
            {
                "ja": "海外女子メジャーのAIG女子オープン最終日が2日、イングランドのロイヤルリザム＆セントアンズGCで行われました。23歳の桑木志帆がプレーオフ2ホール目でエスター・ヘンセライト（ドイツ）を下し、海外メジャーという大舞台で初制覇を果たしました。海外メジャー優勝は日本勢にとって長年の目標の一つで、ギャラリーも大いに沸きました。この日は竹田麗央が6位タイに入るなど、日本勢の活躍が目立ちました。",
                "en": "The final round of the AIG Women's Open, a women's major championship, was held on the 2nd at Royal Lytham & St Annes GC in England. Shiho Kuwaki, 23, defeated Esther Henseleit (Germany) on the second playoff hole, achieving her first victory on the big stage of a major championship abroad. Winning a major overseas has long been one of the goals for Japanese players, and the gallery was in high spirits.",
                "literal": "海外女子大满贯赛事AIG女子公开赛的决赛轮于2日在英格兰的皇家莱瑟姆及圣安妮斯高尔夫俱乐部举行。23岁的桑木志帆在加洞赛第2洞击败埃斯特・亨泽莱特（德国），在海外大满贯这一大舞台上实现了首次夺冠。海外大满贯夺冠对日本选手来说是长久以来的目标之一，观众席也大为沸腾。",
                "grammar": "「〜で行われました」— 在…举行。例：ロイヤルリザムで行われました（在皇家莱瑟姆举行）。\n「〜を下し」— 击败…。例：ヘンセライトを下し（击败亨泽莱特）。\n「〜を果たしました」— 实现了…。例：初制覇を果たしました（实现了首次夺冠）。",
                "vocab": [
                    ["メジャー", "めじゃー", "大满贯赛事"],
                    ["最終日", "さいしゅうび", "决赛轮、最后一天"],
                    ["プレーオフ", "ぷれーおふ", "加洞赛、季后赛"],
                    ["制覇", "せいは", "称霸、夺冠"],
                    ["大舞台", "おおぶたい", "大舞台"],
                    ["沸く", "わく", "沸腾、兴奋"]
                ]
            },
            {
                "ja": "プレーオフ1ホール目はともにパー。迎えた2ホール目、桑木は2打目でグリーンを捉えましたが、バーディパットは約80センチショートしました。対するヘンセライトがボギーとし、桑木が2パットのパーで勝負ありとなりました。大ギャラリーの歓声に対して笑顔満開の桑木は、仲間たちからの祝福を受けると、目に涙が浮かびました。",
                "en": "Both players made par on the first playoff hole. On the second hole, Kuwaki reached the green in two, but her birdie putt came up about 80 centimeters short. Henseleit, in contrast, made bogey, and Kuwaki's two-putt par settled the match. Beaming at the roar of the large gallery, Kuwaki's eyes filled with tears as she received congratulations from her teammates.",
                "literal": "加洞赛第1洞双方都打出标准杆。进入第2洞，桑木第2杆攻上果岭，但小鸟推短了约80厘米。相比之下亨泽莱特打出柏忌，桑木以两推标准杆分出胜负。面对大批观众的欢呼声笑容满面的桑木，在收到同伴们的祝福时，眼中泛起了泪花。",
                "grammar": "「〜ともに」— 双方都…。例：ともにパー（双方都是标准杆）。\n「〜に対して」— 对于…。例：歓声に対して（面对欢呼声）。\n「〜勝負あり」— 分出胜负。例：2パットのパーで勝負ありとなりました（以两推标准杆分出胜负）。",
                "vocab": [
                    ["グリーン", "ぐりーん", "果岭"],
                    ["バーディ", "ばーでぃ", "小鸟球"],
                    ["ボギー", "ぼぎー", "柏忌（高于标准杆一杆）"],
                    ["歓声", "かんせい", "欢呼声"],
                    ["祝福", "しゅくふく", "祝福"],
                    ["涙が浮かぶ", "なみだがある", "泪花浮现"]
                ]
            },
            {
                "ja": "2019年の渋野日向子、昨年の山下美夢有に続く日本勢3人目の全英Vです。日本勢による海外メジャー優勝は、樋口久子、渋野、笹生優花、古江彩佳、西郷真央、山下に続く7人目の快挙となりました。賞金総額は大会史上最高の1000万ドル（約16億3000万円）で、優勝した桑木は150万ドル（約2億4000万円）を獲得しました。",
                "en": "It is the third British Open victory by a Japanese player, following Hinako Shibuno in 2019 and Miyu Yamashita last year. For Japanese players, winning a major abroad was a feat achieved by only seven players, following Hisako Higuchi, Shibuno, Yuka Saso, Ayaka Furue, Mao Saigo, and Yamashita. The total prize money was a tournament-record $10 million (about 1.63 billion yen), and champion Kuwaki earned $1.5 million (about 240 million yen).",
                "literal": "这是继2019年的涩野日向子、去年的山下美梦有之后，日本选手第3次夺得全英赛冠军。日本选手在海外大满贯夺冠，是继樋口久子、涩野、笹生优花、古江彩佳、西乡真央、山下之后的第7人的壮举。总奖金为大会史上最高的1000万美元（约16亿3000万日元），夺冠的桑木获得了150万美元（约2亿4000万日元）。",
                "grammar": "「〜に続く」— 继…之后。例：渋野日向子に続く（继涩野日向子之后）。\n「〜快挙となりました」— 成为…的壮举。例：7人目の快挙となりました（成为第7人的壮举）。\n「〜を獲得しました」— 获得了…。例：150万ドルを獲得しました（获得了150万美元）。",
                "vocab": [
                    ["快挙", "かいきょ", "壮举"],
                    ["賞金総額", "しょうきんそうがく", "奖金总额"],
                    ["史上最高", "しじょうさいこう", "史上最高"],
                    ["獲得", "かくとく", "获得"],
                    ["大ギャラリー", "だいぎゃらりー", "大批观众"],
                    ["目に涙が浮かぶ", "めになみだがある", "眼中泛起泪花"]
                ]
            }
        ]
    },
    {
        "slug": "docomo-no-ginkou-sidou",
        "title": "「ドコモの銀行」きょう始動 「d NEOBANK」消滅、最大4.5%還元",
        "subtitle": "8月3日、住信SBIネット銀行が「ドコモSMTBネット銀行」に商号変更し、個人向け銀行サービス「ドコモの銀行」がスタート。dカードのスマホ決済で初年度最大4.5%のポイント還元も始まる。",
        "paras": [
            {
                "ja": "8月3日、住信SBIネット銀行が関係当局の認可を前提として「ドコモSMTBネット銀行」へと商号を変更し、個人向けの銀行サービスブランドを「ドコモの銀行」へ刷新してスタートしました。これに伴い、従来親しまれてきた「d NEOBANK」のサービス名称は消滅し、個人向け銀行サービスは「ドコモの銀行」に一本化されます。スマートフォン向けアプリの名称も変更される予定です。",
                "en": "On August 3, Sumitomo Mitsui Trust SBI Net Bank changed its trade name to \"Docomo SMTB Net Bank\" (subject to approval from the relevant authorities) and launched its retail banking service under the renewed brand \"Docomo no Ginko\" (Docomo Bank). With this change, the familiar \"d NEOBANK\" service name disappears, and retail banking services are consolidated into Docomo Bank. The name of the smartphone app will also be changed.",
                "literal": "8月3日，住信SBI网络银行在获得相关当局批准的前提下将商号变更为「docomo SMTB网络银行」，面向个人的银行服务品牌刷新为「docomo银行」并启动。随之，以往为人熟知的「d NEOBANK」服务名称消失，面向个人的银行服务将统一为「docomo银行」。智能手机应用的名称也预定变更。",
                "grammar": "「〜を前提として」— 以…为前提。例：認可を前提として（以批准为前提）。\n「〜に伴い」— 随着…。例：これに伴い（随之）。\n「〜に一本化されます」— 被统一为…。例：ドコモの銀行に一本化されます（统一为docomo银行）。",
                "vocab": [
                    ["商号", "しょうごう", "商号、公司名称"],
                    ["認可", "にんか", "批准、许可"],
                    ["刷新", "さっしん", "刷新、更新"],
                    ["消滅", "しょうめつ", "消失、消灭"],
                    ["一本化", "いっぽんか", "统一、合并"],
                    ["アプリ", "あぷり", "应用程序"]
                ]
            },
            {
                "ja": "サービスの刷新に合わせて、ドコモグループの決済や証券サービスと連携したポイント還元特典が順次提供されます。8月20日からは「dアカウント」との連携機能が始まり、「dカード」の引き落とし口座を「ドコモの銀行」に設定してスマホ決済を利用すると、基本還元率1.0%に加えて引落特典が上乗せされ、初年度は最大4.5%のdポイント還元を受けることができます。",
                "en": "Along with the service renewal, point-return benefits linked with Docomo Group payment and securities services will be provided sequentially. From August 20, linkage with \"d Account\" begins: if you set the debit account for your \"d Card\" to Docomo Bank and use smartphone payments, on top of the basic 1.0% return rate, a direct-debit bonus is added, allowing you to receive up to 4.5% d-point returns in the first year.",
                "literal": "配合服务的刷新，与docomo集团支付和证券服务联动的积分返利特典将陆续提供。从8月20日起开始「d账户」的联动功能，如果将「d卡」的扣款账户设置为「docomo银行」并使用手机支付，在基本返利率1.0%的基础上再加上扣款特典，第一年最高可以获得4.5%的d积分返利。",
                "grammar": "「〜に合わせて」— 配合…、随着…。例：刷新に合わせて（配合刷新）。\n「〜に加えて」— 在…之上、加上…。例：基本還元率1.0%に加えて（在基本返利率1.0%之上）。\n「〜ことができます」— 能够…。例：還元を受けることができます（能够获得返利）。",
                "vocab": [
                    ["還元", "かんげん", "返利、回馈"],
                    ["特典", "とくてん", "特典、优惠"],
                    ["連携", "れんけい", "联动、合作"],
                    ["引き落とし", "ひきおとし", "扣款、自动转账"],
                    ["口座", "こうざ", "账户"],
                    ["上乗せ", "のせのせ", "追加、加码"]
                ]
            },
            {
                "ja": "刷新の背景には「やさしい金融を、みんなの手に」という企業ビジョンがあります。ドコモの調査によると、自分の金融知識が平均以上だと考えている人は全体のわずか22%にとどまり、投資未経験者の約8割が身近に相談できる場所がないと回答しました。ドコモは「おサイフケータイ」や「d払い」で培ってきたキャッシュレス基盤と、金融各社のノウハウを結集し、支払う、ためる、増やすといった金融行動を一気通貫で支援することを目指しています。",
                "en": "Behind the renewal is the corporate vision of \"kind finance, in everyone's hands.\" According to a Docomo survey, only 22% of people consider their financial knowledge above average, and about 80% of those with no investing experience said they have no one nearby to consult. Docomo aims to combine the cashless infrastructure cultivated through \"Osafu-Keitai\" and \"d Barai\" with the know-how of financial companies, providing seamless support for financial actions such as paying, saving, and growing money.",
                "literal": "刷新的背景是「把温柔的金融，送到每个人手中」这一企业愿景。根据docomo的调查，认为自己的金融知识在平均以上的人仅占整体的22%，投资无经验者中约有8成回答身边没有可以咨询的地方。docomo将通过在「手机钱包」和「d支付」中积累起来的无现金基盘与各金融公司的专业诀窍集结起来，目标是贯穿始终地支援支付、储蓄、增值等金融行为。",
                "grammar": "「〜背景には〜があります」— …的背景是…。例：刷新の背景にはビジョンがあります（刷新的背景是这一愿景）。\n「〜にとどまり」— 仅停留在…。例：わずか22%にとどまり（仅停留在22%）。\n「〜を目指しています」— 以…为目标。例：支援することを目指しています（以支援为目标）。",
                "vocab": [
                    ["ビジョン", "びじょん", "愿景"],
                    ["知識", "ちしき", "知识"],
                    ["未経験者", "みけいけんしゃ", "无经验者"],
                    ["培う", "つちかう", "培养、积累"],
                    ["結集", "けっしゅう", "集结、汇聚"],
                    ["一気通貫", "いっきつうかん", "贯穿始终、一站式"]
                ]
            }
        ]
    },
    {
        "slug": "iphone-shin-seihin-hinusu",
        "title": "今年のiPhone新製品、発売直後から品薄になる可能性 クックCEOが警告",
        "subtitle": "Appleのティム・クックCEOが次の四半期に「供給制約の影響が大幅に拡大する」と警告。折りたたみ型の「iPhone Ultra」などが発売直後から入手困難になる可能性がある。",
        "paras": [
            {
                "ja": "Appleのティム・クックCEOは、2026年第3四半期の決算説明会で、次の四半期に「供給制約の影響が大幅に拡大する」と警告しました。わかりやすくいえば、もうすぐ発表されるiPhoneの新製品群、特に期待が高まっている折りたたみ型の「iPhone Ultra」などが、発売直後から入手困難な状況になる可能性があるということです。",
                "en": "Apple CEO Tim Cook warned in the Q3 2026 earnings call that \"the impact of supply constraints will expand significantly\" in the next quarter. In plain terms, the new iPhone lineup to be announced soon — especially the highly anticipated foldable \"iPhone Ultra\" — could become hard to obtain immediately after release.",
                "literal": "苹果的蒂姆・库克CEO在2026年第三季度财报说明会上警告称，下一季度「供应制约的影响将大幅扩大」。简单来说，就是即将发布的iPhone新产品群，尤其是备受期待的折叠型「iPhone Ultra」等，有可能在发售后立即陷入难以入手的状况。",
                "grammar": "「〜で/に警告しました」— 在…上警告。例：決算説明会で警告しました（在财报说明会上发出警告）。\n「〜わかりやすくいえば」— 简单来说。例：わかりやすくいえば（简单来说）。\n「〜可能性がある」— 有可能…。例：入手困難になる可能性がある（有可能难以入手）。",
                "vocab": [
                    ["決算説明会", "けっさんせつめいかい", "财报说明会"],
                    ["供給制約", "きょうきゅうせいやく", "供应制约"],
                    ["拡大", "かくだい", "扩大"],
                    ["折りたたみ型", "おりたたみがた", "折叠型"],
                    ["入手困難", "にゅうしゅこんなん", "难以入手"],
                    ["発表", "はっぴょう", "发布、发表"]
                ]
            },
            {
                "ja": "Appleによれば、今回の供給不足はサプライヤーや製造パートナーの問題ではなく、iPhoneとMacの製品サイクルへの需要が「予想をはるかに超えた」ことが主因だといいます。一方で、RAM（メモリー）の市場価格が上昇を続けており、クックCEOは「メモリーの市場価格が上昇し続けており、事業への影響が増大している」と述べました。Appleは先月、メモリーチップのコスト上昇に対応するため製品の価格を大幅に引き上げています。",
                "en": "According to Apple, this shortage is not a problem with suppliers or manufacturing partners; the main cause is that demand for the iPhone and Mac product cycles \"far exceeded expectations.\" Meanwhile, market prices for RAM (memory) continue to rise, and Cook said, \"Memory market prices continue to rise, and the impact on our business is increasing.\" Last month, Apple significantly raised product prices to cope with rising memory chip costs.",
                "literal": "据苹果称，此次供应不足不是供应商或制造合作伙伴的问题，主要原因是iPhone和Mac产品周期的需求「远远超出了预期」。另一方面，RAM（内存）的市场价格持续上涨，库克CEO表示「内存市场价格持续上涨，对业务的影响正在增大」。苹果上个月为了应对内存芯片成本上升，大幅提高了产品价格。",
                "grammar": "「〜によれば」— 根据…。例：Appleによれば（据苹果称）。\n「〜はるかに超えた」— 远远超过。例：予想をはるかに超えた（远远超出预期）。\n「〜に対応するため」— 为了应对…。例：コスト上昇に対応するため（为了应对成本上升）。",
                "vocab": [
                    ["供給不足", "きょうきゅうぶそく", "供应不足"],
                    ["需要", "じゅよう", "需求"],
                    ["主因", "しゅいん", "主要原因"],
                    ["市場価格", "しじょうかかく", "市场价格"],
                    ["増大", "ぞうだい", "增大"],
                    ["大幅に", "おおはばに", "大幅地"]
                ]
            },
            {
                "ja": "2026年秋に発売予定のiPhone 18シリーズは、iPhone 18 Pro、iPhone 18 Pro Max、そして初の折りたたみ型となるiPhone Ultraの3モデルになると予想されています。新型iPhoneが発売とともに争奪戦になるのはもはや恒例行事とも言えますが、今年は例年以上に入手が難しい状況になりそうです。もし新型iPhoneの購入を計画している場合は、早めに情報収集と購入計画を立てておくことが重要になりそうです。",
                "en": "The iPhone 18 series scheduled for release in fall 2026 is expected to consist of three models: the iPhone 18 Pro, iPhone 18 Pro Max, and the iPhone Ultra, which would be the first foldable iPhone. New iPhones turning into a scramble at launch is almost a yearly tradition, but this year it looks like they will be even harder to get than usual. If you are planning to buy a new iPhone, it will likely be important to gather information and make a purchase plan early.",
                "literal": "预定2026年秋季发售的iPhone 18系列，预计将由iPhone 18 Pro、iPhone 18 Pro Max以及首款折叠型iPhone Ultra共3款机型组成。新款iPhone一发售就陷入争夺战几乎可以说是例行活动，但今年看起来会比往年更加难以入手。如果计划购买新款iPhone，尽早进行信息收集和制定购买计划似乎很重要。",
                "grammar": "「〜と予想されています」— 预计…。例：3モデルになると予想されています（预计为3款机型）。\n「〜と言えます」— 可以说…。例：恒例行事とも言えます（可以说是例行活动）。\n「〜ておく」— 事先做…。例：計画を立てておく（事先制定计划）。",
                "vocab": [
                    ["シリーズ", "しりーず", "系列"],
                    ["モデル", "もでる", "机型、型号"],
                    ["争奪戦", "そうだつせん", "争夺战"],
                    ["恒例行事", "こうれいぎょうじ", "例行活动"],
                    ["例年", "れいねん", "往年"],
                    ["情報収集", "じょうほうしゅうしゅう", "信息收集"]
                ]
            }
        ]
    },
    {
        "slug": "perseus-ryuuseigun-mikoro",
        "title": "1時間に最大100個の流星 2026年最大の天体ショー「ペルセウス座流星群」",
        "subtitle": "毎年8月中旬に見ごろを迎えるペルセウス座流星群。今年は極大と新月が重なるため観測条件はほぼ完璧。暗い夜空なら1時間に最大100個の流れ星が見られる可能性がある。",
        "paras": [
            {
                "ja": "毎年8月中旬に極大を迎えるペルセウス座流星群は、年間で最も人気の高い流星群のひとつです。今年はたくさんの流星が見られる「当たり年」と期待されています。流星群の活動期は7月17日から8月24日までで、最も活発になる極大は8月13日の午前11時ごろと予想されています。注目すべきは12日夜から13日明け方にかけてで、今年は13日が新月のため、観測条件はほぼ完璧といっていいでしょう。",
                "en": "The Perseid meteor shower, which peaks every year in mid-August, is one of the most popular meteor showers of the year. This year it is expected to be a \"bumper year\" with many meteors visible. The shower is active from July 17 to August 24, and its peak, when it is most active, is predicted around 11 a.m. on August 13. The time to watch is from the night of the 12th into the early morning of the 13th; since the 13th is a new moon this year, the observing conditions can be called nearly perfect.",
                "literal": "每年8月中旬迎来极大的英仙座流星雨，是一年中最受欢迎的流星雨之一。今年被期待为能看到大量流星的「丰收年」。流星雨的活动期是7月17日到8月24日，最活跃的极大预计在8月13日上午11点左右。值得关注的是12日夜间到13日凌晨，今年13日是新月，因此观测条件可以说是几乎完美。",
                "grammar": "「〜を迎える」— 迎来…。例：極大を迎える（迎来极大）。\n「〜にかけて」— 到…为止（时间范围）。例：12日夜から13日明け方にかけて（从12日夜间到13日凌晨）。\n「〜といっていいでしょう」— 可以说…吧。例：ほぼ完璧といっていいでしょう（可以说是几乎完美吧）。",
                "vocab": [
                    ["流星群", "りゅうせいぐん", "流星雨、流星群"],
                    ["極大", "きょくだい", "极大、高峰"],
                    ["当たり年", "あたりどし", "丰收年、好运之年"],
                    ["新月", "しんげつ", "新月"],
                    ["観測条件", "かんそくじょうけん", "观测条件"],
                    ["明け方", "あけがた", "黎明、拂晓"]
                ]
            },
            {
                "ja": "ペルセウス座流星群は、「スイフト・タットル彗星」が内太陽系に残していった塵の帯を地球の軌道が横切る際に生じます。流星物質が地球の大気圏に秒速59kmという高速で突入し、大気と衝突して発光します。高速で夜空を駆ける明るい流星が特徴で、「火球」と呼ばれる非常に明るい流星が出現することでも知られています。",
                "en": "The Perseids occur when Earth's orbit crosses the band of dust left in the inner solar system by Comet Swift-Tuttle. Meteoroids plunge into Earth's atmosphere at high speed — 59 km per second — and glow as they collide with the air. The shower is characterized by bright meteors racing across the night sky, and is also known for producing extremely bright meteors called \"fireballs.\"",
                "literal": "英仙座流星雨是地球的轨道横穿「斯威夫特・塔特尔彗星」遗留在内太阳系的尘埃带时产生的。流星物质以每秒59公里的高速突入地球大气层，与大气碰撞而发光。其特征是高速划过夜空的明亮流星，也以出现被称为「火球」的极亮流星而闻名。",
                "grammar": "「〜際に」— 在…的时候。例：軌道が横切る際に（在轨道横穿的时候）。\n「〜という高速で」— 以…的高速。例：秒速59kmという高速で（以每秒59公里的高速）。\n「〜ことで知られています」— 以…而闻名。例：出現することでも知られています（也以出现…而闻名）。",
                "vocab": [
                    ["彗星", "すいせい", "彗星"],
                    ["塵", "ちり", "尘埃、灰尘"],
                    ["軌道", "きどう", "轨道"],
                    ["大気圏", "たいきけん", "大气层"],
                    ["突入", "とつにゅう", "突入、冲入"],
                    ["火球", "かきゅう", "火球"]
                ]
            },
            {
                "ja": "2026年はペルセウス座流星群の極大と新月が重なるため、数年ぶりにすばらしい「星降る夜」となるのではないかと天文関係者は期待しています。街明かりのない暗い夜空の下なら、1時間に最大100個の流れ星が見られる可能性があります。観測に最適な場所を探すには、光害マップで暗い夜空が残されている場所を探すといいでしょう。観察する際は、目を暗闇に慣らしてから空を見上げると、より多くの流星を見つけやすくなります。",
                "en": "Because the Perseid peak and the new moon coincide in 2026, astronomers expect this could be a wonderful \"starfall night\" for the first time in several years. Under a dark sky free of city lights, up to 100 shooting stars per hour may be visible. To find the best place for observing, it is a good idea to use a light-pollution map to locate areas where dark skies remain.",
                "literal": "2026年由于英仙座流星雨的极大与新月重叠，天文学家们期待这可能成为数年来首次的美妙「星落之夜」。在没有街灯的黑暗夜空下，1小时最多可能看到100颗流星。要寻找最适合观测的地点，用光害地图寻找仍保留着黑暗夜空的地方比较好。",
                "grammar": "「〜のではないか」— 是不是…呢（委婉推测）。例：星降る夜となるのではないか（会不会成为星落之夜呢）。\n「〜可能性があります」— 有…的可能性。例：見られる可能性があります（有能看到的可能性）。\n「〜といいでしょう」— …比较好。例：探すといいでしょう（找一下比较好）。",
                "vocab": [
                    ["重なる", "かさなる", "重叠、重合"],
                    ["天文関係者", "てんもんかんけいしゃ", "天文相关人士"],
                    ["流れ星", "ながれぼし", "流星"],
                    ["最適", "さいてき", "最合适、最佳"],
                    ["光害", "ひかりがい", "光污染"],
                    ["残される", "のこされる", "被留下"]
                ]
            }
        ]
    },
    {
        "slug": "windows-hotel-wifi-keikoku",
        "title": "Windowsユーザーは「ホテルのWi-Fiは使うな」 マイクロソフトが緊急警告",
        "subtitle": "マイクロソフトが、ロシアのサイバー攻撃者による旅行者を標的にしたハッキングキャンペーン「CaptiveCrunch」を発見。ホテルなどのWi-Fiを介して認証情報を窃取される脅威を警告した。",
        "paras": [
            {
                "ja": "マイクロソフトは米国時間7月31日、「組織は、公共や宿泊施設のネットワークインフラが信頼できない可能性があると想定すべきだ」と警告しました。これは、出張者に対する同社のセキュリティアドバイスが著しく厳格化したことを示しています。ロシアのサイバー攻撃者による新たなハッキングの脅威は、世界中の旅行者を標的にしてマルウェアを送り込み、認証情報を窃取するといいます。",
                "en": "On July 31 U.S. time, Microsoft warned that \"organizations should assume that the network infrastructure of public and lodging facilities may not be trustworthy.\" This shows that the company's security advice for business travelers has become significantly stricter. The new hacking threat from Russian cyber attackers reportedly targets travelers worldwide, sending in malware and stealing credentials.",
                "literal": "微软于美国时间7月31日警告称「组织应该设想公共和住宿设施的网络基础设施可能不可信」。这表明该公司面向出差人士的安全建议已明显严格化。据称，俄罗斯网络攻击者的新型黑客威胁以全世界的旅行者为目标，植入恶意软件并窃取认证信息。",
                "grammar": "「〜と想定すべきだ」— 应该设想…。例：信頼できないと想定すべきだ（应该设想为不可信）。\n「〜を示しています」— 显示出…。例：厳格化したことを示しています（显示出已严格化）。\n「〜を標的にして」— 以…为目标。例：旅行者を標的にして（以旅行者为目标）。",
                "vocab": [
                    ["宿泊施設", "しゅくはくしせつ", "住宿设施"],
                    ["インフラ", "いんふら", "基础设施"],
                    ["想定", "そうてい", "设想、假定"],
                    ["出張者", "しゅっちょうしゃ", "出差者"],
                    ["標的", "ひょうてき", "目标、靶子"],
                    ["窃取", "せっしゅ", "窃取"]
                ]
            },
            {
                "ja": "この警告は、マイクロソフトがロシアの「Midnight Blizzard」のサブクラスターである「Storm-2945」によるものと特定した、世界的なキャンペーン「CaptiveCrunch」の発見を受けたものです。このキャンペーンは、侵害されたゲストネットワークを通じて、認証情報の窃取やマルウェアの配信を行い、出張者を標的にしています。マイクロソフトによると、この活動は5月初旬から続いており、世界中の宿泊施設やその他のゲストネットワークが関与しているということです。",
                "en": "The warning follows the discovery of the global campaign \"CaptiveCrunch,\" which Microsoft attributed to \"Storm-2945,\" a subcluster of Russia's \"Midnight Blizzard.\" The campaign steals credentials and distributes malware through compromised guest networks, targeting business travelers. According to Microsoft, the activity has continued since early May, involving lodging facilities and other guest networks around the world.",
                "literal": "这一警告是在发现全球性活动「CaptiveCrunch」之后发出的，微软将该活动认定为俄罗斯「Midnight Blizzard」的子集群「Storm-2945」所为。该活动通过被入侵的访客网络窃取认证信息、分发恶意软件，以出差者为目标。据微软称，该活动从5月上旬持续至今，全世界的住宿设施及其他访客网络都被卷入其中。",
                "grammar": "「〜を受けたものです」— 是在…之后发出的。例：発見を受けたものです（是在发现之后发出的）。\n「〜を通じて」— 通过…。例：ゲストネットワークを通じて（通过访客网络）。\n「〜に関与している」— 与…有关、被卷入。例：ネットワークが関与している（网络被卷入其中）。",
                "vocab": [
                    ["キャンペーン", "きゃんぺーん", "行动、活动"],
                    ["侵害", "しんがい", "入侵、侵害"],
                    ["配信", "はいしん", "分发、推送"],
                    ["初旬", "しょじゅん", "上旬"],
                    ["関与", "かんよ", "参与、关联"],
                    ["特定", "とくてい", "认定、锁定"]
                ]
            },
            {
                "ja": "攻撃者はネットワークトラフィックを操作することで、宿泊客をマイクロソフトを模したサインインページにリダイレクトさせます。ホテルのWi-Fiに接続するときは、不審なログインページが出ても個人情報を入力せず、公式サイトを直接確認するなどの注意が必要です。マイクロソフトは、脅威アクターがAndroidデバイスを標的にしている可能性を示す兆候も把握しているとしています。",
                "en": "By manipulating network traffic, attackers redirect hotel guests to sign-in pages that imitate Microsoft. When connecting to hotel Wi-Fi, even if a suspicious login page appears, you should not enter personal information; instead, check the official website directly — such caution is necessary. Microsoft also says it has detected signs that the threat actors may be targeting Android devices as well.",
                "literal": "攻击者通过操纵网络流量，将住宿客人重定向到模仿微软的登录页面。连接酒店Wi-Fi时，即使出现可疑的登录页面也不要输入个人信息，直接确认官方网站等注意是必要的。微软表示，也掌握到威胁行为者可能以Android设备为目标的迹象。",
                "grammar": "「〜ことで」— 通过…（手段）。例：操作することで（通过操作）。\n「〜を模した」— 模仿…的。例：マイクロソフトを模したページ（模仿微软的页面）。\n「〜としています」— 表示…。例：把握しているとしています（表示已掌握）。",
                "vocab": [
                    ["トラフィック", "とらふぃっく", "流量、通信量"],
                    ["操作", "そうさ", "操作、操纵"],
                    ["模する", "もする", "模仿"],
                    ["不審", "ふしん", "可疑"],
                    ["個人情報", "こじんじょうほう", "个人信息"],
                    ["兆候", "ちょうこう", "征兆、迹象"]
                ]
            }
        ]
    },
    {
        "slug": "windows11-8gb-memory",
        "title": "Windows 11は8GBメモリでも快適に使えるようになる？ 品質向上への中間報告",
        "subtitle": "マイクロソフトがWindows 11の品質向上への取り組みの中間報告を発表。メモリ効率化の改善により、8GBメモリのPCでも快適に使えるようになる可能性が示された。",
        "paras": [
            {
                "ja": "マイクロソフトは2026年3月、「年内はWindows 11の新機能追加の方針を改め、機能性の改善に努めていく」と宣言しました。タスクバーの配置やファイルエクスプローラーの挙動問題、Windows Updateに関する煩わしさなど、不満の多かった項目を順に解決していくことが開発チームのミッションです。",
                "en": "In March 2026, Microsoft declared that it would change its policy of adding new Windows 11 features for the rest of the year and focus on improving functionality. Resolving one by one the items that drew the most complaints — such as taskbar layout, File Explorer behavior problems, and the annoyance of Windows Update — is the development team's mission.",
                "literal": "微软于2026年3月宣布「年内将改变Windows 11新增功能的方向，致力于功能性的改善」。按顺序解决任务栏的布局、文件资源管理器的行为问题、Windows Update的烦人之处等不满较多的项目，是开发团队的使命。",
                "grammar": "「〜に努めていく」— 致力于…。例：改善に努めていく（致力于改善）。\n「〜に関する」— 与…相关的。例：Windows Updateに関する煩わしさ（与Windows Update相关的烦扰）。\n「〜ていく」— 表示动作的持续。例：解決していく（逐步解决）。",
                "vocab": [
                    ["方針を改める", "ほうしんをあらためる", "改变方针"],
                    ["機能性", "きのうせい", "功能性"],
                    ["タスクバー", "たすくばー", "任务栏"],
                    ["挙動", "きょどう", "行为、动作"],
                    ["煩わしさ", "わずらわしさ", "烦扰、麻烦"],
                    ["ミッション", "みっしょん", "使命"]
                ]
            },
            {
                "ja": "そして7月30日、その中間報告がブログに投稿されました。報告では、Windows Updateによる中断を減らす変更のプレビュー開始や、ドライバーの品質・信頼性・セキュリティの基準を引き上げる「Driver Quality Initiative」の導入、ファイルエクスプローラーの改善などが挙げられています。これらの改善は、2026年後半に登場する大型アップデート「26H2」で展開されるとみられます。",
                "en": "Then, on July 30, the interim report was posted to the blog. The report lists changes such as starting previews of changes that reduce interruptions caused by Windows Update, the introduction of the \"Driver Quality Initiative\" to raise quality, reliability, and security standards for drivers, and improvements to File Explorer. These improvements are expected to be rolled out with the major update \"26H2\" arriving in the latter half of 2026.",
                "literal": "然后于7月30日，中期报告被发布到博客上。报告中列举了开始预览减少Windows Update造成的中断的变更、引入将驱动程序的质量・可靠性・安全标准提升的「Driver Quality Initiative」、文件资源管理器的改善等。这些改善预计将在2026年下半年登场的大型更新「26H2」中展开。",
                "grammar": "「〜が挙げられています」— 列举了…。例：改善などが挙げられています（列举了改善等）。\n「〜とみられます」— 预计…。例：展開されるとみられます（预计将展开）。\n「〜に登場する」— 在…登场。例：26H2で展開される（在26H2中展开）。",
                "vocab": [
                    ["中間報告", "ちゅうかんほうこく", "中期报告"],
                    ["中断", "ちゅうだん", "中断"],
                    ["プレビュー", "ぷれびゅー", "预览"],
                    ["信頼性", "しんらいせい", "可靠性"],
                    ["基準", "きじゅん", "标准"],
                    ["導入", "どうにゅう", "引入、导入"]
                ]
            },
            {
                "ja": "特に注目されるのがメモリ効率化への取り組みです。アプリやコンポーネント全体のオーバーヘッドを削除するためのより効率的なメモリアロケーターや、WinUI 3のチューニングなどが含まれます。今まではマシンパワーに頼って運用されていた部分をより効率的に使いつつ、パフォーマンス向上につなげるという取り組みで、8GBメモリのPCでも快適に使えるようになる可能性があります。",
                "en": "Particularly noteworthy is the effort toward memory efficiency. It includes a more efficient memory allocator to remove overhead across apps and components, as well as tuning of WinUI 3. It is an initiative to use more efficiently the parts that previously relied on machine power, while linking this to performance gains — raising the possibility that even PCs with 8GB of RAM will become comfortable to use.",
                "literal": "特别受到关注的是面向内存效率化的举措。其中包括为了消除应用程序和组件整体的开销而采用更高效的内存分配器、WinUI 3的调优等。这是一项在更高效地使用以往依赖机器性能运行的部分的同时，与性能提升相连接的举措，8GB内存的PC也有可能变得可以舒适使用。",
                "grammar": "「〜が含まれます」— 包含…。例：チューニングなどが含まれます（包含调优等）。\n「〜につなげる」— 与…相连、用于…。例：向上につなげる（用于提升）。\n「〜可能性があります」— 有…的可能性。例：快適に使えるようになる可能性があります（有可能变得可以舒适使用）。",
                "vocab": [
                    ["効率化", "こうりつか", "效率化"],
                    ["オーバーヘッド", "おーばーへっど", "开销、额外负担"],
                    ["アロケーター", "あろけーたー", "分配器"],
                    ["チューニング", "ちゅーにんぐ", "调优、调校"],
                    ["パフォーマンス", "ぱふぉーまんす", "性能"],
                    ["快適", "かいてき", "舒适"]
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
