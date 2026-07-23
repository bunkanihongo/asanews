#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-07-24 (Fri) Edition"""
import json, os, sys, subprocess, time, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-07-24'
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
# TODAY'S ARTICLES
# ==================================================================
articles = [
    {
        "slug": "kousho-ondo-40-do-ichigatsu",
        "title": "8月初旬 関東甲信など40℃以上「酷暑日」の可能性 1か月予報",
        "subtitle": "気象庁の1か月予報で関東甲信・東海など8月上旬に40℃以上の酷暑日となる可能性。熱中症に厳重警戒が必要。",
        "paras": [
            {
                "ja": "気象庁は23日、最新の1か月予報を発表した。この先1か月、全国的に気温が高い見込みで、特に東日本や西日本では8月上旬にかけて気温がかなり高い予想となっている。関東甲信や東海では最高気温40℃以上の「酷暑日」となる可能性もあるという。",
                "en": "The Japan Meteorological Agency released its latest one-month forecast on the 23rd. Temperatures are expected to remain high nationwide for the next month, with particularly high temperatures forecast for eastern and western Japan through early August. Regions including Kanto-Koshin and Tokai may see 'extreme heat days' with maximum temperatures exceeding 40°C.",
                "literal": "气象厅23日发表了最新的1个月预报。今后1个月，全国范围内气温预计偏高，特别是东日本和西日本到8月上旬气温相当高的预测。关东甲信和东海可能出现最高气温40℃以上的「酷暑日」。",
                "grammar": "「〜見込み」— 预计…。例：高い見込み（预计偏高）。\n「〜にかけて」— 到…为止（时间范围）。例：8月上旬にかけて（到8月上旬）。\n「〜という」— 据说…。例：可能性もあるという（据说也有可能）。",
                "vocab": [
                    ["気象庁", "きしょうちょう", "气象厅"],
                    ["1か月予報", "いっかげつよほう", "一个月预报"],
                    ["見込み", "みこみ", "预计、可能性"],
                    ["酷暑日", "こくしょび", "酷暑日、极热天"],
                    ["最高気温", "さいこうきおん", "最高气温"]
                ]
            },
            {
                "ja": "気象庁は北海道から九州、奄美地方に「高温に関する早期天候情報」も発表した。この地域では29日ごろから10年に一度レベルの高温が予想されている。北日本も8月上旬は気温がかなり高くなる可能性があるという。",
                "en": "The JMA also issued 'Early Weather Information on High Temperatures' for areas from Hokkaido to Kyushu and the Amami region. These areas are expected to see once-in-a-decade level high temperatures from around the 29th. Northern Japan may also see quite high temperatures in early August.",
                "literal": "气象厅也从北海道到九州、奄美地区发表了「高温相关的早期天气信息」。这些地区预计从29日左右开始出现十年一遇水平的高温。北日本8月上旬气温也有可能相当高。",
                "grammar": "「〜に関する」— 关于…的。例：高温に関する早期天候情報（有关高温的早期天气信息）。\n「〜ごろから」— 从…左右开始。例：29日ごろから（从29日左右开始）。\n「〜レベル」— …水平、程度。例：10年に一度レベル（十年一遇水平）。",
                "vocab": [
                    ["高温", "こうおん", "高温"],
                    ["早期天候情報", "そうきてんこうじょうほう", "早期天气信息"],
                    ["奄美", "あまみ", "奄美"],
                    ["地域", "ちいき", "地区"],
                    ["北日本", "きたにほん", "北日本"]
                ]
            },
            {
                "ja": "一方、東北と北陸は7月末まで梅雨前線の影響を受けやすく、梅雨空が続く見込みだ。30日ごろに北海道付近を低気圧が通過した後は東北や北陸も晴れる日が多くなり、31日ごろに梅雨明けとなりそうだ。",
                "en": "Meanwhile, the Tohoku and Hokuriku regions are likely to remain under the influence of the seasonal rain front until the end of July, with continued rainy season conditions. After a low-pressure system passes near Hokkaido around the 30th, the Tohoku and Hokuriku regions should see more sunny days, with the rainy season likely ending around the 31st.",
                "literal": "另一方面，东北和北陆到7月底容易受梅雨锋面影响，预计持续梅雨天气。30日左右低气压通过北海道附近后，东北和北陆晴天的日子也会增多，预计31日左右出梅。",
                "grammar": "「〜影響を受けやすい」— 容易受…影响。例：前線の影響を受けやすい（容易受锋面影响）。\n「〜そうだ」— 好像…（样态）。例：梅雨明けとなりそうだ（好像要出梅了）。",
                "vocab": [
                    ["梅雨前線", "ばいうぜんせん", "梅雨锋面"],
                    ["北陸", "ほくりく", "北陆地区"],
                    ["低気圧", "ていきあつ", "低气压"],
                    ["梅雨明け", "つゆあけ", "出梅、梅雨结束"],
                    ["晴れる", "はれる", "放晴"]
                ]
            }
        ]
    },
    {
        "slug": "seven-eleven-tenpai-fusei-tenbai",
        "title": "セブンイレブン 店舗関係者が人気キャラ商品を不正転売 法的には？",
        "subtitle": "セブンイレブン加盟店で店員やオーナーによる人気キャラ商品の買い占め・転売が発覚。弁護士が法的見解を解説。",
        "paras": [
            {
                "ja": "コンビニ大手のセブン-イレブン・ジャパンが、加盟店の一部で発売前の人気キャラクター商品について、店員やオーナーによる買い占めや転売が行われたとして、全国の加盟店に警告していたことが23日に報じられた。",
                "en": "It was reported on the 23rd that Seven-Eleven Japan, a major convenience store chain, had issued warnings to its franchise stores nationwide after some stores were found to have employees and owners engaging in hoarding and reselling popular character merchandise before its official release.",
                "literal": "便利店巨头Seven-Eleven Japan，关于部分加盟店在人气角色商品发售前店员或店主进行囤积和转卖一事，23日报道称已向全国加盟店发出警告。",
                "grammar": "「〜について」— 关于…。例：商品について（关于商品）。\n「〜による」— 由…造成的/进行的。例：店員による買い占め（由店员进行的囤积）。\n「〜として」— 作为…。例：警告していたとして（作为警告）。",
                "vocab": [
                    ["コンビニ", "こんびに", "便利店"],
                    ["加盟店", "かめいてん", "加盟店"],
                    ["買い占め", "かいしめ", "囤积、扫货"],
                    ["転売", "てんばい", "转卖"],
                    ["警告", "けいこく", "警告"]
                ]
            },
            {
                "ja": "弁護士によると、店員やオーナーが商品を定価で買い取った後に転売する行為は、刑事罰の対象にはなりにくいという。店内の商品は仕入れの段階で加盟店オーナーに所有権が移るため、自分の商品を転売しても横領や背任には当たらない可能性が高いとされる。",
                "en": "According to lawyers, the act of employees or owners purchasing merchandise at list price and then reselling it is unlikely to be subject to criminal penalties. Since ownership of in-store merchandise typically transfers to the franchise owner at the procurement stage, reselling one's own merchandise is unlikely to constitute embezzlement or breach of trust.",
                "literal": "据律师称，店员或店主以定价购买商品后转卖的行为，很难成为刑事处罚的对象。因为店内商品在采购阶段所有权就转移到了加盟店店主手中，所以即使转卖自己的商品，也不太可能构成侵占或背信。",
                "grammar": "「〜によると」— 据…说。例：弁護士によると（据律师说）。\n「〜にくい」— 难以…。例：なりにくい（难以成为）。\n「〜ため」— 因为…。例：移るため（因为转移）。",
                "vocab": [
                    ["弁護士", "べんごし", "律师"],
                    ["定価", "ていか", "定价"],
                    ["刑事罰", "けいじばつ", "刑事处罚"],
                    ["所有権", "しょゆうけん", "所有权"],
                    ["横領", "おうりょう", "侵占"]
                ]
            },
            {
                "ja": "ただし、セブン-イレブン・ジャパンのフランチャイズ契約に違反する可能性はあり、実際に契約を中途解約されたケースもある。企業倫理や消費者の信頼という観点からも、こうした行為は問題視されている。",
                "en": "However, such actions may violate the Seven-Eleven Japan franchise agreement, and there have actually been cases where contracts were terminated mid-term. From the perspective of corporate ethics and consumer trust, such behavior is being viewed as problematic.",
                "literal": "但是，有可能违反Seven-Eleven Japan的特许经营合同，实际上也有中途解约的案例。从企业伦理和消费者的信赖的观点来看，这种行为也受到质疑。",
                "grammar": "「〜可能性がある」— 有…可能性。例：違反する可能性がある（有违反的可能性）。\n「〜ケースもある」— 也有…的情况。例：解約されたケース（被解约的情况）。\n「〜という観点から」— 从…的观点来看。",
                "vocab": [
                    ["フランチャイズ", "ふらんちゃいず", "特许经营"],
                    ["契約", "けいやく", "合同"],
                    ["中途解約", "ちゅうとかいやく", "中途解约"],
                    ["企業倫理", "きぎょうりんり", "企业伦理"],
                    ["消費者", "しょうひしゃ", "消费者"],
                    ["信頼", "しんらい", "信赖"]
                ]
            }
        ]
    },
    {
        "slug": "tsubame-suzume-otonari",
        "title": "ツバメとスズメ 隣同士で子育て 長野で珍しい光景",
        "subtitle": "長野県松本市でツバメとスズメが隣り合わせの巣で子育て。珍しい共棲に住民も驚き。",
        "paras": [
            {
                "ja": "長野県松本市の民家の敷地内で、ツバメとスズメが隣り合わせの巣で子育てに励んでいる。住宅に隣接する建物のひさしに巣があり、6月ごろにツバメが最初の巣を構えた。巣立ち後、スズメが使われなくなった巣にごみなどを運んで「リフォーム」し、子育てを始めたという。",
                "en": "Swallows and sparrows are raising their chicks side by side in adjacent nests on the property of a private home in Matsumoto City, Nagano Prefecture. The nests are located on the eaves of a building adjacent to the house. The swallows first built a nest around June. After the chicks left, sparrows carried debris and other materials to 'renovate' the abandoned nest and began raising their own young.",
                "literal": "在长野县松本市的一处民宅院内，燕子和麻雀在相邻的巢穴中养育雏鸟。巢穴在紧邻住宅的建筑的屋檐上，6月左右燕子先筑了第一个巢。雏鸟离巢后，麻雀搬运垃圾等将不再使用的巢「改造」后开始了育儿。",
                "grammar": "「〜合う」— 互相…。例：隣り合わせ（互相紧挨着）。\n「〜に励む」— 致力于…。例：子育てに励む（致力于育儿）。\n「〜という」— 据说…。例：始めたという（据说开始了）。",
                "vocab": [
                    ["ツバメ", "つばめ", "燕子"],
                    ["スズメ", "すずめ", "麻雀"],
                    ["隣り合わせ", "となりあわせ", "相邻、紧挨着"],
                    ["巣", "す", "巢、窝"],
                    ["子育て", "こそだて", "育儿、养育幼鸟"],
                    ["リフォーム", "りふぉーむ", "改造、翻新"]
                ]
            },
            {
                "ja": "21日には、スズメの親がひなに餌を運んでくると、ツバメの親が警戒するように周りを飛び交っていたが、互いのひなに危害を加えることはなかった。坪田さん（83）は「昔は屋根瓦の隙間にスズメは巣を作っていたが今は隙間がない。ツバメの巣をスズメが好んでいるのかな」と話している。",
                "en": "On the 21st, when a parent sparrow came to feed its chicks, a parent swallow flew around as if keeping watch, but neither harmed the other's young. Mr. Tsubota (83) commented, 'Sparrows used to build nests in gaps between roof tiles, but there are no gaps anymore. Maybe sparrows have come to prefer swallows' nests.'",
                "literal": "21日，当麻雀亲鸟来给雏鸟喂食时，燕子亲鸟像警戒一样在周围飞来飞去，但没有对对方的雏鸟造成伤害。坪田先生（83岁）说「以前麻雀在屋顶瓦片的缝隙中筑巢，但现在没有缝隙了。麻雀可能喜欢上燕子的巢了吧」。",
                "grammar": "「〜ように」— 像…一样地。例：警戒するように（像警戒一样地）。\n「〜が」— 然而（转折）。例：危害を加えることはなかったが（但没有伤害）。\n「〜かな」— 表疑问或推测。例：好んでいるのかな（可能喜欢吧）。",
                "vocab": [
                    ["餌", "えさ", "饵、食物"],
                    ["ひな", "ひな", "雏鸟"],
                    ["飛び交う", "とびかう", "纷飞、飞来飞去"],
                    ["危害", "きがい", "危害"],
                    ["屋根瓦", "やねがわら", "屋顶瓦片"],
                    ["隙間", "すきま", "缝隙"]
                ]
            }
        ]
    },
    {
        "slug": "disney-owakonka-neage",
        "title": "値上げディズニーの「オワコン化」 子ども200万人減の裏で増える大人客",
        "subtitle": "東京ディズニーリゾートがまた値上げ。家族で1日10万円も。売上最高も株価低迷のパラドックス。",
        "paras": [
            {
                "ja": "東京ディズニーリゾートがまた値上げに踏み切る。2026年10月から大人1デーパスポートの上限価格が1万900円から1万2400円に引き上げられる。ネット上では「もう家族で行けない」「さすがに高すぎる」と悲鳴が上がっている。",
                "en": "Tokyo Disney Resort is raising its prices once again. From October 2026, the maximum price for an adult 1-Day Passport will increase from 10,900 yen to 12,400 yen. Online, people are lamenting, 'We can no longer go as a family' and 'This is just too expensive.'",
                "literal": "东京迪士尼度假村再次实施涨价。从2026年10月起，成人1日护照的上限价格将从1万900日元提高到1万2400日元。网上出现了「已经不能全家去了」「果然太贵了」等哀叹声。",
                "grammar": "「〜に踏み切る」— 下决心做…。例：値上げに踏み切る（下决心涨价）。\n「〜から…に引き上げる」— 从…提高到…。例：1万900円から1万2400円に（从1万900日元提高到1万2400日元）。",
                "vocab": [
                    ["値上げ", "ねあげ", "涨价"],
                    ["パスポート", "ぱすぽーと", "护照、通行证"],
                    ["上限価格", "じょうげんかかく", "上限价格"],
                    ["引き上げる", "ひきあげる", "提高、提升"],
                    ["悲鳴", "ひめい", "哀鸣声、抱怨声"]
                ]
            },
            {
                "ja": "大人2人、中学生1人、小学生1人の家族なら、繁忙日は入園だけで4万円前後になり、食事やお土産、交通費を含めれば日帰りでも総額10万円近くになる。以前は中高生が友達同士で気軽に遊びに行ける場所だったが、今では一大イベントになりつつある。",
                "en": "For a family of two adults, one middle school student, and one elementary school student, admission alone on peak days comes to around 40,000 yen. Including meals, souvenirs, and transportation, even a day trip could total nearly 100,000 yen. It used to be a place where high school students could casually go with friends, but it's now becoming a major event.",
                "literal": "如果是大人2人、中学生1人、小学生1人的家庭，繁忙日仅入园就需要4万日元左右，包括餐饮、纪念品、交通费的话即使当天往返总金额也可能接近10万日元。以前是初高中生之间可以轻松去玩的地方，现在正在变成一大活动。",
                "grammar": "「〜前後」— …左右。例：4万円前後（4万日元左右）。\n「〜つつある」— 正在逐渐…。例：なりつつある（正在逐渐变成）。",
                "vocab": [
                    ["繁忙日", "はんぼうび", "繁忙日"],
                    ["入園", "にゅうえん", "入园"],
                    ["お土産", "おみやげ", "纪念品、特产"],
                    ["日帰り", "ひがえり", "当天往返"],
                    ["一大イベント", "いちだい", "一大活动"]
                ]
            },
            {
                "ja": "運営会社のオリエンタルランドの売上高は過去最高を記録したが、株価は約半値に下落している。子どもや若者の来園者が減り、代わりに40代以上の大人客が増えていることが将来性への不安につながっているという。投資家たちは高価格路線の持続可能性に疑問を抱いている。",
                "en": "While the operating company Oriental Land recorded its highest-ever revenue, its stock price has fallen to about half its peak. The decline in child and young visitors, replaced by an increase in adult visitors aged 40 and above, is said to be fueling concerns about future growth. Investors are questioning the sustainability of the high-price strategy.",
                "literal": "运营公司Oriental Land的销售额创下历史最高纪录，但股价下跌至约一半。儿童和年轻人的入园人数减少，取而代之的是40岁以上成年客人的增加，这被指与对未来性的不安有关。投资者对高价路线的可持续性抱有疑问。",
                "grammar": "「〜に」— 关于（表示结果）。例：半値に下落（跌至一半）。\n「〜につながる」— 导致…、与…相关。例：不安につながる（导致不安）。",
                "vocab": [
                    ["売上高", "うりあげだか", "销售额"],
                    ["過去最高", "かこさいこう", "历史最高"],
                    ["株価", "かぶか", "股价"],
                    ["来園者", "らいえんしゃ", "来园游客"],
                    ["将来性", "しょうらいせい", "未来性、前景"],
                    ["投資家", "とうしか", "投资者"]
                ]
            }
        ]
    },
    {
        "slug": "hannmono-otoko-keisatsu-happou",
        "title": "コンビニ駐車場で刃物男に警察官が発砲 住宅街に銃声 熊本",
        "subtitle": "熊本県合志市のコンビニ駐車場で刃物を持った21歳の男に警察官が発砲。強盗の疑いも視野に捜査。",
        "paras": [
            {
                "ja": "22日午後6時ごろ、熊本県合志市のコンビニ「ファミリーマート」の駐車場で、刃物を持った男に警察官が発砲する事件があった。警察が事件を認知したのは午後6時1分。コンビニの店員から「刃物を持った男が入ってきた」と通報があり、約5分後に警察官が現場に到着した。",
                "en": "Around 6 PM on the 22nd, an incident occurred at a FamilyMart convenience store parking lot in Koshi City, Kumamoto Prefecture, where police officers fired at a man wielding a knife. Police received a report at 6:01 PM from a store employee saying 'a man with a knife came in,' and officers arrived at the scene about five minutes later.",
                "literal": "22日下午6点左右，在熊本县合志市的便利店「FamilyMart」的停车场，发生了持刀男子被警察开枪的事件。警察在下午6点1分认知到事件。便利店店员报警称「持刀男子进来了」，约5分钟后警察到达现场。",
                "grammar": "「〜ごろ」— …左右（时间）。例：午後6時ごろ（下午6点左右）。\n「〜て」— 表示原因。例：通報があり（因为有报警）。\n「〜た」— 过去式。例：到着した（到达了）。",
                "vocab": [
                    ["コンビニ", "こんびに", "便利店"],
                    ["駐車場", "ちゅうしゃじょう", "停车场"],
                    ["刃物", "はもの", "刀具、利器"],
                    ["警察官", "けいさつかん", "警察官"],
                    ["発砲", "はっぽう", "开枪、发射"],
                    ["通報", "つうほう", "报警、通报"]
                ]
            },
            {
                "ja": "警察官が刃物を捨てるよう説得した上で発砲し、男に命中。現行犯逮捕されたのは近くに住む職業不詳の前田詩音容疑者（21）で、右肩と右足に軽傷を負った。男は確保された後、「強盗だ」と自分で言っていたという。",
                "en": "After attempting to persuade the man to drop his weapon, the officers fired, hitting him. The suspect arrested at the scene was Shion Maeda (21), an unemployed local resident. He sustained minor injuries to his right shoulder and right leg. After being subdued, the man reportedly said 'I'm a robber' himself.",
                "literal": "警察劝男子丢弃刀具后开枪，命中男子。被现行逮捕的是住在附近的职业不详的前田詩音嫌疑人（21岁），右肩和右足受了轻伤。该男子被控制后，自己说了「我是强盗」。",
                "grammar": "「〜よう」— 表示方式/目的。例：捨てるよう説得（劝其丢弃）。\n「〜上で」— 在…之后。例：説得した上で（在劝告之后）。\n「〜という」— 据说。例：言っていたという（据说说了）。",
                "vocab": [
                    ["説得する", "せっとくする", "说服、劝导"],
                    ["命中する", "めいちゅうする", "命中"],
                    ["現行犯逮捕", "げんこうはんたいほ", "现行犯逮捕"],
                    ["容疑者", "ようぎしゃ", "嫌疑人"],
                    ["軽傷", "けいしょう", "轻伤"],
                    ["強盗", "ごうとう", "强盗"]
                ]
            },
            {
                "ja": "警察は強盗の疑いもあるとみて捜査を進めている。現場周辺は住宅街で子どもの通う塾などもあり人通りが多い。警察は拳銃の使用が適正だったか調査中だとしている。7月20日にも神奈川県相模原市で同様の事案があり、警察の威嚇発砲の是非が注目されている。",
                "en": "Police are also investigating on suspicion of robbery. The area around the scene is a residential neighborhood with many passersby, including children attending cram schools. Police say they are investigating whether the use of firearms was appropriate. A similar incident occurred in Sagamihara City, Kanagawa Prefecture on July 20th, drawing attention to the appropriateness of police warning shots.",
                "literal": "警方也认为有抢劫嫌疑并展开调查。现场周围是住宅区，有孩子上补习班等，人流量大。警方表示正在调查枪支的使用是否适当。7月20日在神奈川县相模原市也发生了类似事件，警察的威吓射击的是非受到关注。",
                "grammar": "「〜とみて」— 认为是…、判断为…。例：疑いもあるとみて（认为也有嫌疑）。\n「〜ている」— 正在…。例：調査中だとしている（表示正在调查）。",
                "vocab": [
                    ["捜査", "そうさ", "搜查、调查"],
                    ["住宅街", "じゅうたくがい", "住宅区"],
                    ["人通り", "ひとどおり", "人来人往"],
                    ["拳銃", "けんじゅう", "手枪"],
                    ["適正", "てきせい", "适当、合理"],
                    ["威嚇", "いかく", "威胁、威吓"]
                ]
            }
        ]
    },
    {
        "slug": "gundam-shinsaku-2027",
        "title": "『ガンダム』新作アニメ発表 2027年展開 神山健治監督が挑む新世界線",
        "subtitle": "ガンダム新作『機動戦士ガンダムRG アレックスゼロ』が2027年に展開。ゲームと世界観を共有する新プロジェクト。",
        "paras": [
            {
                "ja": "『ガンダム』シリーズの新作アニメ『機動戦士ガンダムRG XARX-ZERO』（アレックスゼロ）が制作されることが決定した。2027年に展開され、映像と場面カットが公開された。監督・シリーズ構成は神山健治氏、主人公のアズミ・レイ役は大塚剛央が担当する。",
                "en": "A new Gundam series anime titled 'Mobile Suit Gundam RG XARX-ZERO' has been greenlit for production. It is set to launch in 2027, with visuals and scene cuts already released. The director and series composer is Kenji Kamiyama, with Takeo Otsuka voicing the protagonist Azumi Ray.",
                "literal": "《高达》系列的新作动画《机动战士高达RG XARX-ZERO》（阿列克斯零）确定制作。将于2027年展开，映像和场景截图已公开。导演·系列构成为神山健治氏，主人公阿兹米·雷由大塚刚央饰演。",
                "grammar": "「〜が決定した」— 决定…。例：制作されることが決定した（决定制作）。\n「〜役」— …角色。例：主人公のアズミ・レイ役（主人公阿兹米·雷的角色）。\n「〜が担当する」— 由…担任。例：大塚剛央が担当する（由大塚刚央担任）。",
                "vocab": [
                    ["ガンダム", "がんだむ", "高达"],
                    ["新作", "しんさく", "新作品"],
                    ["アニメ", "あにめ", "动画"],
                    ["制作", "せいさく", "制作"],
                    ["監督", "かんとく", "导演"],
                    ["主人公", "しゅじんこう", "主人公"]
                ]
            },
            {
                "ja": "同作はゲーム「GUNDAM ROGUE ORBIT」と世界観を共有するメディアミックス企画「RGプロジェクト」の一環だ。アニメではゲームから約100年前の世界を舞台に物語が描かれ、ゲームではその後の世界をプレイヤー自身が体験する構成になっている。",
                "en": "The work is part of the 'RG Project,' a media mix initiative sharing the same world setting as the game 'GUNDAM ROGUE ORBIT.' The anime will tell a story set about 100 years before the game, while the game allows players to personally experience the world that follows.",
                "literal": "该作品是与游戏《GUNDAM ROGUE ORBIT》共享世界观的媒体混合企划「RG项目」的一环。动画将以游戏约100年前的世界为舞台描绘故事，而游戏则让玩家自身体验之后的世界。",
                "grammar": "「〜を共有する」— 共享…。例：世界観を共有する（共享世界观）。\n「〜を舞台に」— 以…为舞台。例：世界を舞台に（以世界为舞台）。\n「〜一環だ」— 是…的一环。例：企画の一環だ（是企划的一环）。",
                "vocab": [
                    ["世界観", "せかいかん", "世界观"],
                    ["メディアミックス", "めでぃあみっくす", "媒体混合（跨媒体）"],
                    ["企画", "きかく", "企划、计划"],
                    ["舞台", "ぶたい", "舞台"],
                    ["体験する", "たいけんする", "体验"]
                ]
            },
            {
                "ja": "物語は太陽系外からもたらされた三つの福音により人類が空前の繁栄を迎えた世界が舞台。しかし発見から10年後にそれらが暴走し、攻撃的な自己増殖系が出現。人類は地球を放棄し、それから45年後、月面で一人の少年が目を覚ますところから物語が始まる。",
                "en": "The story is set in a world where humanity has achieved unprecedented prosperity thanks to three 'gospels' brought from outside the solar system. However, 10 years after their discovery, they go rogue, spawning an aggressive self-replicating system. Humanity is forced to abandon Earth, and 45 years later, a boy awakens on the lunar surface — where the story begins.",
                "literal": "故事以来自太阳系外的三个福音使人类迎来空前繁荣的世界为舞台。然而发现10年后它们暴走，出现攻击性的自我增殖系统。人类放弃地球，45年后一个月球表面的少年醒来——故事由此开始。",
                "grammar": "「〜により」— 由于…。例：繁栄を迎えた（迎来了繁荣）。\n「〜から…後」— 从…之后。例：それから45年後（从那以后的45年后）。\n「〜ところから」— 从…之处。例：目を覚ますところから始まる（从醒来的地方开始）。",
                "vocab": [
                    ["太陽系", "たいようけい", "太阳系"],
                    ["福音", "ふくいん", "福音"],
                    ["空前", "くうぜん", "空前"],
                    ["繁栄", "はんえい", "繁荣"],
                    ["暴走する", "ぼうそうする", "失控、暴走"],
                    ["月面", "げつめん", "月球表面"]
                ]
            }
        ]
    },
    {
        "slug": "naikaku-shijiritsu-teika-kikikan",
        "title": "内閣支持率減 与党に危機感 皇室典範改正・国会運営が影響",
        "subtitle": "高市内閣の支持率が下落。典範改正と強引な国会運営が要因か。食料品減税の判断迫られる。",
        "paras": [
            {
                "ja": "報道各社の世論調査で高市内閣の支持率が下落している。皇室典範の改正や与党の国会運営が影響したとの見方が広がる。時事通信の7月の調査では支持率は49.0％で政権発足後の最低を記録。毎日新聞の調査でも支持率は10ポイント減の41％に落ち込んだ。",
                "en": "Approval ratings for the Takaichi Cabinet are declining across media polls. A widespread view attributes this to the revision of the Imperial House Law and the ruling party's Diet management. In Jiji Press's July survey, the approval rate dropped to 49.0%, the lowest since the administration took office. Mainichi Shimbun's survey also showed a 10-point drop to 41%.",
                "literal": "各媒体报道的舆论调查显示高市内阁的支持率正在下降。广泛的看法是皇室典范的修改和执政党的国会运营产生了影响。时事通信的7月调查中支持率为49.0%，是政权成立后的最低纪录。每日新闻的调查中支持率也下降了10个百分点至41%。",
                "grammar": "「〜で下落する」— 在…方面下降。例：支持率が下落（支持率下降）。\n「〜との見方」— …的看法。例：影響したとの見方（认为产生了影响的看法）。\n「〜に落ち込む」— 跌至…。例：41％に落ち込んだ（跌至41%）。",
                "vocab": [
                    ["世論調査", "よろんちょうさ", "舆论调查"],
                    ["支持率", "しじりつ", "支持率"],
                    ["下落する", "げらくする", "下降、下跌"],
                    ["政権", "せいけん", "政权"],
                    ["発足", "ほっそく", "成立、启动"],
                    ["最低", "さいてい", "最低"]
                ]
            },
            {
                "ja": "与党からは深刻な受け止めが出ている。閣僚の一人は支持下落の理由について「皇室典範と強引な国会運営だ」と指摘した。典範改正を巡っては旧宮家の男系男子を養子として迎えることに国民の理解が得られていないとの声が根強い。首相の国会対応にも批判が集まっている。",
                "en": "Serious concerns have emerged from within the ruling party. One cabinet minister pointed to 'the Imperial House Law and forceful Diet management' as reasons for the declining support. Regarding the law revision, there is persistent criticism that public understanding has not been gained for the plan to bring male descendants of former imperial families into the imperial household as adoptees. The Prime Minister's Diet handling has also drawn criticism.",
                "literal": "执政党内部出现了严重的反应。一位阁僚指出支持率下降的原因「是皇室典范和强行国会运营」。围绕典范修改，关于将旧宫家男系男子作为养子迎入皇室一事根深蒂固地存在着国民理解不足的声音。首相的国会应对也受到批评。",
                "grammar": "「〜について」— 关于…。例：理由について（关于理由）。\n「〜を巡って」— 围绕…。例：典範改正を巡って（围绕典范修改）。\n「〜との声」— …的声音。例：得られていないとの声（没有得到理解的声音）。",
                "vocab": [
                    ["深刻", "しんこく", "深刻"],
                    ["受け止め", "うけとめ", "接受、反应"],
                    ["閣僚", "かくりょう", "阁僚、部长"],
                    ["強引", "ごういん", "强行、强硬"],
                    ["旧宮家", "きゅうみやけ", "旧宫家（皇室分支）"],
                    ["養子", "ようし", "养子"]
                ]
            },
            {
                "ja": "物価高対策の遅れも支持離れを招いたとの見方がある。首相は近く食料品の消費税減税の判断を迫られる。与党は衆院選公約で2年間の税率ゼロを掲げていたが、自民関係者は「消費税を1％に下げる中途半端な対応では支持率がさらに落ち込む」と懸念している。",
                "en": "There is also a view that delays in addressing rising prices have led to declining support. The Prime Minister will soon face a decision on reducing the consumption tax on food items. The ruling party had promised a zero tax rate for two years in their Lower House election manifesto, but LDP insiders are concerned that 'a half-baked measure reducing the consumption tax to just 1% would cause approval ratings to fall even further.'",
                "literal": "物价高涨对策的滞后也被认为导致了支持率下降。首相近期被迫就食品消费税减税做出判断。执政党在众议院选举公约中提出了两年税率为零的承诺，但自民党相关人士担心「将消费税降至1%的半吊子应对会导致支持率进一步下降」。",
                "grammar": "「〜を招く」— 招致…。例：支持離れを招いた（招致了支持率下降）。\n「〜を迫られる」— 被迫…。例：判断を迫られる（被迫做出判断）。\n「〜では」— 如果是…的话（负面条件）。例：中途半端な対応では（如果是半吊子的应对的话）。",
                "vocab": [
                    ["物価高", "ぶっかだか", "物价高涨"],
                    ["対策", "たいさく", "对策"],
                    ["消費税", "しょうひぜい", "消费税"],
                    ["減税", "げんぜい", "减税"],
                    ["公約", "こうやく", "公约、承诺"],
                    ["中途半端", "ちゅうとはんぱ", "半吊子、不彻底"]
                ]
            }
        ]
    },
    {
        "slug": "trump-ohtani-sansan-dodgers",
        "title": "トランプ大統領が大谷翔平を絶賛 25分スピーチ ドジャース表敬訪問",
        "subtitle": "ワールドシリーズ連覇のドジャースがホワイトハウス訪問。トランプ大統領が大谷と山本を絶賛。",
        "paras": [
            {
                "ja": "昨季ワールドシリーズ連覇を果たしたドジャースが23日、米ワシントンDCのホワイトハウスを表敬訪問し、大谷翔平投手（32）、山本由伸投手（27）、佐々木朗希投手（24）らがトランプ大統領（80）と対面した。トランプ大統領は約25分間のスピーチを行った。",
                "en": "The Dodgers, who won consecutive World Series titles last season, made a courtesy visit to the White House in Washington D.C. on the 23rd. Pitchers Shohei Ohtani (32), Yoshinobu Yamamoto (27), and Roki Sasaki (24) met with President Donald Trump (80). President Trump delivered a speech lasting approximately 25 minutes.",
                "literal": "上赛季达成世界大赛连冠的道奇队23日访问了美国华盛顿特区的白宫，大谷翔平投手（32岁）、山本由伸投手（27岁）、佐佐木朗希投手（24岁）等与特朗普总统（80岁）会面。特朗普总统发表了约25分钟的演讲。",
                "grammar": "「〜を果たす」— 实现…、完成…。例：連覇を果たした（实现了连冠）。\n「〜と対面した」— 与…会面。例：大統領と対面した（与总统会面）。",
                "vocab": [
                    ["ワールドシリーズ", "わーるどしりーず", "世界大赛（MLB总决赛）"],
                    ["連覇", "れんぱ", "连冠"],
                    ["表敬訪問", "ひょうけいほうもん", "礼节性拜访"],
                    ["対面する", "たいめんする", "会面、见面"],
                    ["スピーチ", "すぴーち", "演讲"]
                ]
            },
            {
                "ja": "トランプ大統領は壇上で大谷について「これまで満票でリーグMVPを2度以上受賞した選手はいない。ただ一人、日本が生んだ伝説、ショウヘイ・オオタニを除いて。誰もが彼を愛しています」と絶賛。昨季55本塁打を放ち満票でMVPを獲得したことに触れ、「史上最高の投手でありながら同時に史上最高の打者にもなれる」と称えた。",
                "en": "On stage, President Trump praised Ohtani, saying, 'No player has ever won the league MVP unanimously more than twice, except for one — the legend born in Japan, Shohei Ohtani. Everyone loves him.' Referring to Ohtani's 55 home runs last season and unanimous MVP win, Trump lauded him as 'the greatest pitcher in history who can also be the greatest hitter at the same time.'",
                "literal": "特朗普总统在台上关于大谷赞不绝口：「至今没有选手以满票获得联盟MVP两次以上。只有一个人例外——日本诞生的传说、大谷翔平。所有人都爱他」。提及上赛季55支本垒打以满票获得MVP的事迹，称赞他「既是有史以来最好的投手，同时也能成为有史以来最好的击球手」。",
                "grammar": "「〜を除いて」— 除了…之外。例：オオタニを除いて（除了大谷之外）。\n「〜ながら」— 一边…一边…/虽然…但是…。例：投手でありながら（既是投手）。\n「〜に触れる」— 提及…。例：ことに触れ（提及了…的事）。",
                "vocab": [
                    ["満票", "まんぴょう", "全票、满票"],
                    ["MVP", "えむぶいぴー", "MVP（最有价值球员）"],
                    ["受賞する", "じゅしょうする", "获奖"],
                    ["伝説", "でんせつ", "传说"],
                    ["本塁打", "ほんるいだ", "本垒打"],
                    ["称える", "たたえる", "称赞、赞扬"]
                ]
            },
            {
                "ja": "山本由伸にも言及し、名前を呼んだ後は近寄ってガッチリ握手を交わした。トランプ氏は「ワールドシリーズMVPのヨシ・ヤマモト。本当に素晴らしい投球でした」と話した。今回は佐々木朗希投手が初参加。引退したカーショーの姿もあり、チームメートたちとの再会の場にもなった。",
                "en": "Trump also mentioned Yoshinobu Yamamoto, approaching him after calling his name and giving a firm handshake. He said, 'World Series MVP Yoshi Yamamoto. Truly magnificent pitching.' This was Roki Sasaki's first participation. Retired pitcher Clayton Kershaw was also present, making it a reunion among teammates.",
                "literal": "也提到了山本由伸，叫了名字后走近并紧紧地握了手。特朗普说「世界大赛MVP的山本由伸。真是精彩的投球」。这次佐佐木朗希投手首次参加。退役的克肖也在场，成为了队友们再会的场合。",
                "grammar": "「〜に言及する」— 提及…。例：山本にも言及した（也提到了山本）。\n「〜を交わす」— 互相…。例：握手を交わした（互相握手）。",
                "vocab": [
                    ["言及する", "げんきゅうする", "提及、提到"],
                    ["握手", "あくしゅ", "握手"],
                    ["投球", "とうきゅう", "投球"],
                    ["初参加", "はつさんか", "首次参加"],
                    ["引退する", "いんたいする", "退役、退休"],
                    ["再会", "さいかい", "再会、重逢"]
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
