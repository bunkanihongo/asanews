#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-09 (Sun) Edition"""
import json, os, subprocess, re, time
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-09'
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
# TODAY'S ARTICLES — 2026-08-09
# ==================================================================
articles = []
articles += [
    {
        "slug": "taifuu15-tohoku-jouriku",
        "title": "東〜北日本は急な雷雨のおそれ 台風15号はあさって東北に上陸か",
        "subtitle": "from TBS NEWS DIG",
        "paras": [
            {
                "ja": "きょう9日も午後を中心に、東日本や北日本では雷雲が発達する見通しです。局地的には1時間に50ミリ以上の、短時間で道路が冠水するほどの滝のような非常に激しい雨や雷雨となるおそれがあります。本州付近は晴れ間がありますが、午後は東日本や北日本を中心に、天気が急変するおそれがあります。",
                "en": "Today, the 9th, thunderclouds are expected to develop in eastern and northern Japan, mainly in the afternoon. Locally, there is a risk of extremely heavy rain and thunderstorms like waterfalls — more than 50 millimeters per hour, enough to flood roads in a short time. The area around Honshu will have some clear spells, but in the afternoon there is a risk of sudden weather changes, mainly in eastern and northern Japan.",
                "literal": "今天9日也以午后为中心，东日本和北日本预计雷云将发展。局部地区可能出现1小时50毫米以上、短时间内足以使道路积水的瀑布般的极强暴雨和雷雨。本州附近虽有晴间，但午后以东日本和北日本为中心，天气有骤变的可能。",
                "grammar": "「〜見通しです」— 预计…。例：雷雲が発達する見通しです（预计雷云将发展）。\n「〜おそれがあります」— 有…的危险/可能。例：激しい雨となるおそれがあります（有可能下暴雨）。\n「〜ほどの」— 达到…程度的。例：道路が冠水するほどの雨（大到使道路积水的雨）。",
                "vocab": [["雷雲", "らいうん", "雷雨云"], ["発達", "はったつ", "发展、增强"], ["局地的", "きょくちてき", "局部性的"], ["冠水", "かんすい", "积水、淹没"], ["滝", "たき", "瀑布"], ["急変", "きゅうへん", "骤变"]]
            },
            {
                "ja": "最高気温は、西日本や東日本でだいたい前日と同じくらいでしょう。名古屋・大阪・広島は35℃など、35℃以上の猛暑日になる所もありそうです。東京都心は33℃くらいで蒸し暑く感じられるでしょう。青森は25℃で前日より9℃も下がるため、体調管理や服装選びに注意が必要です。",
                "en": "Maximum temperatures will be roughly the same as the previous day in western and eastern Japan. Some places such as Nagoya, Osaka, and Hiroshima will reach 35°C or more, becoming extremely hot days. Central Tokyo will feel humid and hot at around 33°C. Aomori will drop to 25°C — 9°C lower than the previous day — so attention to health management and clothing choices is necessary.",
                "literal": "最高气温，西日本和东日本大致与前一天相同吧。名古屋、大阪、广岛等地有达到35℃以上酷暑日的地方。东京都心约33℃，会感到闷热吧。青森为25℃，比前一天下降9℃，因此需要注意身体管理和服装选择。",
                "grammar": "「〜同じくらいでしょう」— 大概和…一样吧。例：前日と同じくらいでしょう（大概和前一天一样吧）。\n「〜もあるそうです」— 似乎也有…。例：猛暑日になる所もありそうです（似乎也有达到酷暑日的地方）。\n「〜ため、〜が必要です」— 因为…，所以需要…。例：9℃も下がるため、注意が必要です（因为下降9℃，所以需要注意）。",
                "vocab": [["最高気温", "さいこうきおん", "最高气温"], ["猛暑日", "もうしょび", "酷暑日（35度以上）"], ["蒸し暑い", "むしあつい", "闷热"], ["都心", "としん", "市中心"], ["体調管理", "たいちょうかんり", "身体状态管理"], ["服装選び", "ふくそうえらび", "选择服装"]]
            },
            {
                "ja": "日本の東で発生している台風15号は、あさって山の日の11日ごろ、東北に上陸するおそれがあります。あまり発達はしない見込みですが、東北では11日午後から急激に雨や風が強まる可能性があります。台風15号は12日には日本海に抜け、13日には熱帯低気圧に変わる見込みです。",
                "en": "Typhoon No. 15, which formed east of Japan, may make landfall in the Tohoku region around the 11th, the day after tomorrow, which is Mountain Day. It is not expected to develop much, but in Tohoku, rain and wind may rapidly intensify from the afternoon of the 11th. Typhoon No. 15 is expected to move out to the Sea of Japan on the 12th and turn into a tropical depression on the 13th.",
                "literal": "在日本以东生成的台风15号，有可能于后天“山之日”11日前后登陆东北。预计不会怎么发展，但东北地区从11日下午起风雨有可能急剧增强。台风15号预计12日移出日本海，13日变为热带低气压。",
                "grammar": "「〜ごろ、〜おそれがあります」— 在…左右，有…的可能。例：11日ごろ上陸するおそれがあります（有可能在11日前后登陆）。\n「〜見込みです」— 预计将…。例：熱帯低気圧に変わる見込みです（预计将变为热带低气压）。\n「〜可能性があります」— 有…的可能性。例：雨や風が強まる可能性があります（风雨有可能增强）。",
                "vocab": [["上陸", "じょうりく", "登陆"], ["山の日", "やまのひ", "山之日（日本节日）"], ["急激", "きゅうげき", "急剧"], ["強まる", "つよまる", "增强"], ["抜ける", "ぬける", "穿过、移出"], ["熱帯低気圧", "ねったいていきあつ", "热带低气压"]]
            },
            {
                "ja": "西日本や東海付近は台風や熱帯低気圧に向かう南からの湿った空気の通り道となるため、お盆期間は大気の状態が不安定となるおそれがあります。一方、台風が通り過ぎたあと、関東や東北太平洋側には涼しく湿った風が吹き込みます。台風が離れても曇りや雨が続き、東京都心の最高気温は30℃を下回る日が多くなるでしょう。",
                "en": "Western Japan and the Tokai area will become a passage for moist air coming from the south toward the typhoon and tropical depression, so atmospheric conditions may become unstable during the Obon holiday period. On the other hand, after the typhoon passes, cool, moist winds will blow into the Pacific side of Kanto and Tohoku. Even after the typhoon moves away, cloudy and rainy weather will continue, and days when central Tokyo's maximum temperature falls below 30°C will likely increase.",
                "literal": "西日本和东海附近将成为流向台风和热带低气压的南方潮湿空气的通道，因此盂兰盆节期间大气状态有可能变得不稳定。另一方面，台风经过之后，关东和东北太平洋一侧将吹入凉爽潮湿的风。即使台风远离，阴天和降雨仍将持续，东京都心的最高气温低于30℃的日子将会增多吧。",
                "grammar": "「〜通り道となる」— 成为…的通道。例：湿った空気の通り道となる（成为潮湿空气的通道）。\n「〜一方、〜」— 另一方面，…。例：一方、涼しい風が吹き込みます（另一方面，凉爽的风吹入）。\n「〜を下回る」— 低于…。例：30℃を下回る日（低于30℃的日子）。",
                "vocab": [["湿った", "しめった", "潮湿的"], ["通り道", "とおりみち", "通道、经过之路"], ["お盆", "おぼん", "盂兰盆节"], ["大気", "たいき", "大气"], ["不安定", "ふあんてい", "不稳定"], ["下回る", "したまわる", "低于、降到…以下"]]
            },
        ]
    },
    {
        "slug": "koudai-naikaku-sijiritsu",
        "title": "高市内閣の支持率、初の6割切り 消費税1％表明直後も下落",
        "subtitle": "from TBS NEWS DIG",
        "paras": [
            {
                "ja": "8月1日、2日に実施したJNN世論調査で高市内閣の支持率が先月調査から6.7ポイント下落し59.2％となった。政権発足から9か月で初めて6割を切り、下落傾向が続いているが、過去の政権と比較しても依然高い数字だといえる。",
                "en": "In the JNN public opinion poll conducted on August 1 and 2, the approval rating of the Takaichi Cabinet fell 6.7 points from last month's survey to 59.2%. For the first time in the nine months since the government took office, it fell below 60%, and although the downward trend continues, it can still be said to be a high figure compared with past governments.",
                "literal": "在8月1日、2日实施的JNN舆论调查中，高市内阁的支持率比上个月调查下降6.7个百分点，降至59.2%。政权成立9个月以来首次跌破6成，虽然呈持续下降趋势，但与过去的政权相比仍可以说是较高的数字。",
                "grammar": "「〜で初めて」— …以来第一次。例：政権発足から9か月で初めて（政权成立9个月以来第一次）。\n「〜が続いている」— …正在持续。例：下落傾向が続いている（下降趋势仍在持续）。\n「〜といえる」— 可以说…。例：依然高い数字だといえる（可以说是依然较高的数字）。",
                "vocab": [["世論調査", "よろんちょうさ", "舆论调查"], ["支持率", "しじりつ", "支持率"], ["下落", "げらく", "下跌"], ["政権", "せいけん", "政权"], ["発足", "はっそく", "成立、启动"], ["比較", "ひかく", "比较"]]
            },
            {
                "ja": "高市内閣の支持率は5月の調査以降、下落が続いている。特徴としては、女性より男性のほうが支持率がやや高く、年代別に見ると年齢が上がるにつれて支持率が下がる傾向はこれまでと変わらない。最大の特徴は「支持政党なし」と答えた、いわゆる「無党派層」の支持離れが顕著になっていることだ。",
                "en": "The approval rating of the Takaichi Cabinet has continued to decline since the May survey. As a characteristic, men's approval is slightly higher than women's, and by age group, the tendency for approval to fall as age rises is unchanged from before. The biggest characteristic is that the so-called \"unaffiliated voters\" — those who answered \"no supporting party\" — are conspicuously turning away from support.",
                "literal": "高市内阁的支持率自5月调查以来持续下降。特征方面，男性比女性支持率略高，按年龄段看，随着年龄上升支持率下降的倾向与以往相同。最大的特征是回答“无支持政党”的所谓“无党派层”的支持流失变得显著。",
                "grammar": "「〜として」— 作为…。例：特徴としては（作为特征来看）。\n「〜につれて」— 随着…。例：年齢が上がるにつれて（随着年龄的增长）。\n「〜ことだ」— 就是…（说明重点）。例：無党派層の支持離れが顕著になっていることだ（就是无党派层的支持流失变得显著）。",
                "vocab": [["年代別", "ねんだいべつ", "按年龄段"], ["傾向", "けいこう", "倾向"], ["支持政党", "しじせいとう", "支持的政党"], ["無党派層", "むとうはそう", "无党派层"], ["支持離れ", "しじばなれ", "支持流失"], ["顕著", "けんちょ", "显著"]]
            },
            {
                "ja": "高市内閣発足直後の支持率は歴代2位となる82.0％だったが、当時は高齢層を含むすべての年代層で支持が高く、無党派層も「高市内閣を支持できる」と答えた人が80％にものぼった。この無党派層が政権発足から9か月経った今、49％と激減していることがわかった。",
                "en": "Immediately after the Takaichi Cabinet took office, the approval rating was 82.0%, the second highest ever, and at that time support was high across all age groups including the elderly, with even 80% of unaffiliated voters answering that they could support the Takaichi Cabinet. It has been found that support among these unaffiliated voters has now plummeted to 49%, nine months after the government took office.",
                "literal": "高市内阁刚成立时的支持率为历代第二高的82.0%，当时包括高龄层在内的所有年龄段支持率都很高，无党派层中回答“能支持高市内阁”的人也高达80%。如今政权成立已过9个月，这一无党派层的支持率骤减至49%，这一点已经明确。",
                "grammar": "「〜となる」— 达到…（数值）。例：歴代2位となる82.0％（达到历代第二的82.0%）。\n「〜にものぼる」— 高达…。例：80％にものぼった（高达80%）。\n「〜ことがわかった」— 得知、明确了…。例：激減していることがわかった（明确了正在骤减）。",
                "vocab": [["歴代", "れきだい", "历代"], ["高齢層", "こうれいそう", "高龄层"], ["経つ", "たつ", "（时间）经过"], ["激減", "げきげん", "骤减"], ["発足直後", "はっそくちょくご", "刚成立后"], ["含む", "ふくむ", "包括"]]
            },
        ]
    },
    {
        "slug": "todai-syusyuuya",
        "title": "東大卒・年収1100万円の男性を“刺しゅう屋”へ導いた「人間を忘れた夏」",
        "subtitle": "from 東洋経済オンライン",
        "paras": [
            {
                "ja": "東大出身、外資系投資銀行に就職して、年収1100万円——。それだけを聞けば“勝ち組”と思われるような人生を、田中優輝さんは歩んでいました。しかし外銀での仕事は「速く、正確に、間違えず」に処理することが重視され、神経をすり減らす日々でした。",
                "en": "Graduating from the University of Tokyo, getting a job at a foreign investment bank, with an annual income of 11 million yen — Tanaka Yuki was living a life that would seem like a \"winner's life\" just by hearing that. However, at the foreign bank, work that emphasized processing \"quickly, accurately, without mistakes\" wore down his nerves day after day.",
                "literal": "东大毕业，进入外资投资银行工作，年收入1100万日元——仅凭这些就会被认为过着“人生赢家”般生活的田中优辉。但是在外资银行的工作重视“快速、准确、不出错”地处理事务，是耗损神经的日子。",
                "grammar": "「〜と思われる」— 被认为是…。例：勝ち組と思われるような人生（被认为是赢家的那种人生）。\n「〜ことが重視される」— …被重视。例：処理することが重視され（处理事务被重视）。\n「〜日々でした」— 是…的日子。例：神経をすり減らす日々でした（是耗损神经的日子）。",
                "vocab": [["出身", "しゅっしん", "出身"], ["外資系", "がいしけい", "外资系"], ["投資銀行", "とうしぎんこう", "投资银行"], ["勝ち組", "かちぐみ", "人生赢家、胜利组"], ["重視", "じゅうし", "重视"], ["すり減らす", "すりへらす", "损耗、磨耗"]]
            },
            {
                "ja": "2023年の夏が、いつ終わったのか、私はあまり覚えていません。朝起きる。スマホでメールを見る。タクシーに乗る。会社に着く。デスクに座る。画面を見る。昼を急いで食べる。また画面を見る。夜中に帰る。シャワーを浴びる。寝る。また朝になる。外を歩いていない月が、何カ月も続きました。",
                "en": "I don't really remember when the summer of 2023 ended. Wake up in the morning. Check email on my phone. Take a taxi. Arrive at the office. Sit at the desk. Stare at the screen. Eat lunch in a hurry. Stare at the screen again. Go home late at night. Take a shower. Sleep. And morning comes again. Months passed in which I didn't walk outside.",
                "literal": "2023年的夏天何时结束的，我已不太记得。早上起床。用手机看邮件。乘出租车。到公司。坐在桌前。看屏幕。匆忙吃午饭。又看屏幕。深夜回家。洗澡。睡觉。又到早晨。没有在外面行走的月份，持续了好几个月。",
                "grammar": "「〜のか、あまり覚えていません」— 不太记得是否/何时…。例：いつ終わったのか、覚えていません（不记得何时结束的）。\n「〜が続きました」— …持续了。例：何カ月も続きました（持续了好几个月）。\n「また〜」— 又、再次（重复）。例：また朝になる（又到早晨）。",
                "vocab": [["覚えていない", "おぼえていない", "不记得"], ["スマホ", "すまほ", "智能手机"], ["デスク", "ですく", "办公桌"], ["画面", "がめん", "屏幕"], ["急いで", "いそいで", "匆忙地"], ["夜中", "よなか", "深夜"]]
            },
            {
                "ja": "徹夜は、ありました。仮眠も取らず、40時間ぶっ通しに近い集中をする日もありました。夜10時に出社して、次の日の午前11時まで案件を進め、そこから別の案件に移り、またその日の夜中まで続く毎日に色はありませんでした。締切の時間は刻んでも、季節は刻めませんでした。",
                "en": "There were all-nighters. There were days when I concentrated for nearly 40 hours straight without even taking a nap. Going to the office at 10 p.m., working on a case until 11 a.m. the next day, then moving to another case and continuing until midnight again — those days had no color. I could count the deadline hours, but I could not mark the seasons.",
                "literal": "有过通宵。也有不假寐、连续近40小时集中工作的日子。晚上10点上班，推进案件到第二天上午11点，再从那里转向另一个案件，又持续到当天深夜——这样的每一天都没有色彩。截止时间可以计时，但季节却无法记录。",
                "grammar": "「〜ぶっ通し」— 连续不间断。例：40時間ぶっ通しに近い集中（接近40小时不间断的专注）。\n「〜ても、〜ませんでした」— 即使…也未能…。例：締切の時間は刻んでも、季節は刻めませんでした（即使能数着截止时间，也无法记录季节）。\n「〜に移り」— 转移到…。例：別の案件に移り（转移到另一个案件）。",
                "vocab": [["徹夜", "てつや", "通宵、熬夜"], ["仮眠", "かみん", "小睡、打盹"], ["出社", "しゅっしゃ", "上班到公司"], ["案件", "あんけん", "项目、案件"], ["締切", "しめきり", "截止"], ["刻む", "きざむ", "刻、记录"]]
            },
            {
                "ja": "ある日、トイレの鏡で自分の顔を見ました。知らない男がいました。表情がなくて、目に光がなくて、紙みたいな色をした、24歳の男。そのあと、入社直前の同期で集まった写真を見ました。4月の私は、笑っていました。でも、半年後の自分と、見比べる。別人でした。",
                "en": "One day, I looked at my face in the restroom mirror. There was a stranger. A 24-year-old man with no expression, no light in his eyes, and a face the color of paper. After that, I looked at a photo of my peers gathered just before joining the company. In April, I was smiling. But when I compare it with myself six months later — it was a different person.",
                "literal": "有一天，我在厕所的镜子里看到了自己的脸。有一个不认识的男人。没有表情，眼里没有光，像纸一样颜色的24岁男人。之后，我看了入职前同期同事们聚在一起的照片。4月的我在笑着。但是，与半年后的自己相比——是另一个人。",
                "grammar": "「〜みたいな」— 像…一样的。例：紙みたいな色（像纸一样的颜色）。\n「〜がなくて、〜」— 没有…，而且…。例：表情がなくて、目に光がなくて（没有表情，眼里也没有光）。\n「〜と、見比べる」— 与…相比较。例：半年後の自分と見比べる（与半年后的自己相比）。",
                "vocab": [["鏡", "かがみ", "镜子"], ["表情", "ひょうじょう", "表情"], ["光", "ひかり", "光芒、光彩"], ["入社", "にゅうしゃ", "入职"], ["同期", "どうき", "同期入职的同事"], ["別人", "べつじん", "另一个人"]]
            },
        ]
    },
    {
        "slug": "kushiro-hisyochi",
        "title": "「真夏日ゼロ」の釧路が避暑地として急成長 長期滞在者が続々",
        "subtitle": "from UHB 北海道文化放送",
        "paras": [
            {
                "ja": "北海道内で8月6日、7日と2日連続の真夏日となる中、22度ほどだった釧路市。涼しい気候を逆手にとった観光客や長期滞在者の獲得作戦が加速しています。釧路市の7月の最高気温の平均はなんと21.2℃。今シーズン、30度以上の真夏日は一度もなく、25度以上の夏日ですらわずか1日しかありません。釧路の武器は「真夏日ゼロ」です。",
                "en": "While Hokkaido saw two consecutive tropical days on August 6 and 7, Kushiro City was around 22 degrees. Efforts to attract tourists and long-stay visitors by turning the cool climate to advantage are accelerating. The average July maximum temperature in Kushiro is a surprising 21.2°C. This season, there has not been a single tropical day of 30°C or more, and even summer days of 25°C or more have occurred only once. Kushiro's weapon is \"zero tropical days.\"",
                "literal": "在北海道内8月6日、7日连续两天出现盛夏日的情况下，气温约22度的钏路市。利用凉爽气候反其道而行、争取游客和长期逗留者的作战正在加速。钏路市7月最高气温平均竟然为21.2℃。本赛季，30度以上的盛夏日一次也没有，连25度以上的夏日也仅有1天。钏路的武器是“盛夏日为零”。",
                "grammar": "「〜となる中、〜」— 在…的情况下，…。例：2日連続の真夏日となる中（在连续两天盛夏日的情况下）。\n「〜を逆手にとる」— 反过来利用…。例：涼しい気候を逆手にとった（反过来利用凉爽气候）。\n「〜しかありません」— 只有…。例：わずか1日しかありません（仅仅只有1天）。",
                "vocab": [["真夏日", "まなつび", "盛夏日（30度以上）"], ["連続", "れんぞく", "连续"], ["逆手", "さかて", "反手、反过来利用"], ["滞在者", "たいざいしゃ", "逗留者"], ["獲得", "かくとく", "获得"], ["武器", "ぶき", "武器、法宝"]]
            },
            {
                "ja": "“霧のマチ”として知られる港町の釧路。沖合の海流の影響で気温が上がりにくく、7月の最高気温の平均は札幌市よりも5度以上、東京よりも10度以上も低いんです。釧路を訪れた観光客は、地元の人も「別世界」の涼しさを実感しています。「想像を上回る、涼しさというか、寒さ…」（東京からの観光客）",
                "en": "Kushiro, a port town known as the \"city of fog.\" Because of the influence of offshore currents, temperatures are hard to rise, and the average July maximum temperature is more than 5 degrees lower than Sapporo and more than 10 degrees lower than Tokyo. Visitors to Kushiro, and even locals, feel a coolness from \"another world.\" \"It's coolness beyond imagination — or rather, cold...\" (a tourist from Tokyo)",
                "literal": "作为“雾之城”而闻名的港町钏路。由于近海海流的影响气温难以升高，7月最高气温平均比札幌市低5度以上，比东京低10度以上。到访钏路的游客，连当地人也实际感受到“另一个世界”般的凉爽。“超出想象的凉爽，与其说是凉爽不如说是寒冷……”（来自东京的游客）",
                "grammar": "「〜として知られる」— 作为…而闻名。例：霧のマチとして知られる（作为雾之城而闻名）。\n「〜にくい」— 难以…。例：気温が上がりにくく（气温难以升高）。\n「〜というか、〜」— 与其说是…不如说是…。例：涼しさというか、寒さ（与其说是凉爽不如说是寒冷）。",
                "vocab": [["霧", "きり", "雾"], ["港町", "みなとまち", "港口城市"], ["沖合", "おきあい", "近海、离岸"], ["海流", "かいりゅう", "海流"], ["実感", "じっかん", "实际感受"], ["上回る", "うわまわる", "超过"]]
            },
            {
                "ja": "そんな釧路の気候を逆手に取った長期滞在者の獲得作戦が市内で加速しています。こちらのホテルでは2泊から10泊以上専用の連泊プランを10月末まで用意していて、1泊料金より割安になっています。この企画は好評で、2か月以上にわたって宿泊する人も。宿泊者数は8月2日時点の2か月間で、すでに2025年のキャンペーン期間4か月分の宿泊者数を上回っています。",
                "en": "In the city, efforts to attract long-stay visitors by turning Kushiro's climate to advantage are accelerating. This hotel offers a consecutive-night plan for stays of 2 nights to 10 nights or more until the end of October, at rates cheaper than a single-night stay. The plan has been well received, with some people staying for more than two months. In the two months as of August 2, the number of guests has already exceeded the number during the four-month campaign period in 2025.",
                "literal": "将钏路的这种气候反其道而行、争取长期逗留者的作战正在市内加速。这家酒店准备了到10月底为止的2晚至10晚以上专用连住方案，比单晚价格更划算。该企划很受欢迎，也有人连续住宿2个月以上。截至8月2日的两个月住宿人数，已经超过了2025年活动期间4个月的住宿人数。",
                "grammar": "「〜専用」— 专用…。例：2泊から10泊以上専用の連泊プラン（2晚至10晚以上专用的连住方案）。\n「〜にわたって」— 持续…（时间范围）。例：2か月以上にわたって宿泊する（持续住宿两个月以上）。\n「〜時点で」— 截至…时点。例：8月2日時点の2か月間（截至8月2日的两个月）。",
                "vocab": [["連泊", "れんぱく", "连续住宿"], ["プラン", "ぷらん", "方案、套餐"], ["割安", "わりやす", "划算、较便宜"], ["好評", "こうひょう", "好评"], ["キャンペーン", "きゃんぺーん", "促销活动"], ["上回る", "うわまわる", "超过"]]
            },
            {
                "ja": "このホテルで初めて釧路で10日間滞在する東京在住の土田信子さん（85）です。「空港に着いた瞬間に『ああ良かった』と思いました。生きていく上で気温は本当に大事で、今の東京は正常な生活が私の年齢だとできなくなってきている。こんな極楽みたいなところは、ないと思っています」と話しました。",
                "en": "This is Tsuchida Nobuko (85), who lives in Tokyo and is staying in Kushiro for 10 days for the first time at this hotel. \"The moment I arrived at the airport, I thought, 'Ah, I'm so glad.' Temperature is really important for living, and at my age, a normal life in Tokyo today is becoming impossible. I don't think there's any place like this paradise,\" she said.",
                "literal": "她是在这家酒店首次在钏路逗留10天的东京居民土田信子（85岁）。“到达机场的瞬间我就想‘啊，太好了’。气温对生活来说真的很重要，以我这个年龄，现在的东京已经越来越无法过正常的生活了。我觉得没有比这更像极乐世界的地方了。”她这样说道。",
                "grammar": "「〜た瞬間に」— …的瞬间。例：空港に着いた瞬間に（到达机场的瞬间）。\n「〜上で」— 在…方面。例：生きていく上で気温は大事（在生活方面气温很重要）。\n「〜みたいなところ」— 像…一样的地方。例：極楽みたいなところ（像极乐世界一样的地方）。",
                "vocab": [["在住", "ざいじゅう", "居住、住在"], ["滞在", "たいざい", "逗留"], ["瞬間", "しゅんかん", "瞬间"], ["正常", "せいじょう", "正常"], ["極楽", "ごくらく", "极乐世界"], ["羽織る", "はおる", "披上、披着"]]
            },
        ]
    },
    {
        "slug": "syounigan-doraggu-rosu",
        "title": "2歳で小児がんになった息子 薬はあるのに日本では使えない「ドラッグロス」",
        "subtitle": "from MBSニュース",
        "paras": [
            {
                "ja": "京都市で暮らす鈴木幸之助君、5歳。10万人に約2人という確率で発症するといわれる小児がん「神経芽腫」と闘っています。その中で直面したのは、国外の薬が日本では使えない「ドラッグ・ロス」の問題。必死に生きる幸之助君と家族の約2年間の歩みに密着しました。",
                "en": "Suzuki Konosuke, 5 years old, lives in Kyoto City. He is fighting neuroblastoma, a childhood cancer said to occur in about 2 out of every 100,000 people. What he faced along the way was the problem of \"drug loss\" — medicines available abroad that cannot be used in Japan. The program closely followed about two years of the lives of Konosuke and his family, who are living desperately.",
                "literal": "住在京都市的铃木幸之助，5岁。他正在与据说每10万人中约有2人发病的小儿癌症“神经母细胞瘤”作斗争。其中他直面的是国外药物在日本无法使用的“药品缺失”问题。节目紧密跟拍了拼命活下去的幸之助君与家人约两年的历程。",
                "grammar": "「〜といわれる」— 据说…。例：発症するといわれる（据说会发病）。\n「〜と闘っています」— 正在与…斗争。例：小児がんと闘っています（正在与小儿癌症斗争）。\n「〜に密着しました」— 紧密跟拍…。例：家族の歩みに密着しました（紧密跟拍家人的历程）。",
                "vocab": [["小児がん", "しょうにがん", "小儿癌症"], ["発症", "はっしょう", "发病"], ["確率", "かくりつ", "概率"], ["神経芽腫", "しんけいがしゅ", "神经母细胞瘤"], ["直面", "ちょくめん", "直面"], ["必死", "ひっし", "拼命"]]
            },
            {
                "ja": "「日常を過ごしているだけで悲しみが押し寄せてくる。ずっと一緒にいたいし、早く元気になってほしい」母・鈴木瑠衣さんは涙を流しながら3歳（当時）の息子を抱きかかえました。この時、両親は主治医から幸之助君の「5年生存率は50％」だと告げられていたのです。",
                "en": "\"Just living an ordinary day, sadness washes over me. I want to stay with him forever, and I want him to get better soon.\" Mother Suzuki Rui held her 3-year-old son (at the time) in her arms in tears. At this time, the parents had been told by the attending physician that Konosuke's five-year survival rate was 50%.",
                "literal": "“仅仅是过着日常，悲伤就会涌上来。想一直在一起，希望他早日恢复健康。”母亲铃木瑠衣流着泪抱起了3岁（当时）的儿子。这时，父母已经从主治医生那里得知幸之助君的“5年生存率为50%”。",
                "grammar": "「〜だけで」— 仅仅是…。例：日常を過ごしているだけで（仅仅是过着日常）。\n「〜てほしい」— 希望（对方）…。例：早く元気になってほしい（希望你早日康复）。\n「〜と告げられていた」— 被告知…。例：50％だと告げられていた（被告知是50%）。",
                "vocab": [["押し寄せる", "おしよせる", "涌来、袭来"], ["涙を流す", "なみだをながす", "流泪"], ["抱きかかえる", "だきかかえる", "抱在怀里"], ["主治医", "しゅじい", "主治医生"], ["生存率", "せいぞんりつ", "生存率"], ["告げる", "つげる", "告知"]]
            },
            {
                "ja": "病院で検査を受けると、腎臓の上の副腎に約11センチの“腫瘍”が見つかり、神経芽腫と呼ばれる小児がんの一種だと診断されました。すぐに抗がん剤などによる治療が始まりました。薬の副作用で食欲がなくなり、やせ細っていく幸之助君。治療に時間がとられ保育園に通えず、友達と話す機会も少ない。成長に大切な日常は奪われていきました。",
                "en": "When he was examined at the hospital, a tumor of about 11 centimeters was found in the adrenal gland above the kidney, and he was diagnosed with neuroblastoma, a type of childhood cancer. Treatment with anticancer drugs and other measures began immediately. Due to side effects of the medicine, Konosuke lost his appetite and grew thin. Time was taken up by treatment, so he could not attend nursery school, and he had few chances to talk with friends. The everyday life that is important for growth was taken away.",
                "literal": "在医院接受检查后，肾脏上方的肾上腺发现约11厘米的“肿瘤”，被诊断为称为神经母细胞瘤的一种小儿癌症。立即开始了抗癌剂等治疗。由于药物副作用失去食欲、日渐消瘦的幸之助君。治疗占用了时间，无法上保育园，与朋友说话的机会也很少。对成长重要的日常生活被夺走了。",
                "grammar": "「〜と呼ばれる」— 被称为…的。例：神経芽腫と呼ばれる小児がん（被称为神经母细胞瘤的小儿癌症）。\n「〜による治療」— 通过…的治疗。例：抗がん剤などによる治療（通过抗癌剂等的治疗）。\n「〜ていきました」— 逐渐…（变化过程）。例：日常は奪われていきました（日常生活逐渐被夺走）。",
                "vocab": [["副腎", "ふくじん", "肾上腺"], ["腫瘍", "しゅよう", "肿瘤"], ["診断", "しんだん", "诊断"], ["抗がん剤", "こうがんざい", "抗癌药"], ["副作用", "ふくさよう", "副作用"], ["奪う", "うばう", "夺走"]]
            },
            {
                "ja": "幸之助君は標準的な治療を乗り越えました。ただ、首のリンパ節などにもがんの“転移”が確認され、再発の可能性が高い高リスクと診断されていました。高リスクの神経芽腫の再発率は40〜50%。再発すれば5年生存率はわずか10％程度とされています。両親は再発リスクを下げるための治療を模索しました。しかし、国内には幸之助君が受けられる治療が見つかりませんでした。",
                "en": "Konosuke overcame the standard treatment. However, metastasis of the cancer was also confirmed in lymph nodes in his neck and elsewhere, and he was diagnosed as high-risk with a high possibility of recurrence. The recurrence rate for high-risk neuroblastoma is 40-50%. If it recurs, the five-year survival rate is said to be only about 10%. His parents searched for treatment to lower the risk of recurrence. However, they could not find treatment that Konosuke could receive in Japan.",
                "literal": "幸之助君挺过了标准治疗。但是，颈部淋巴结等处也确认了癌症的“转移”，被诊断为复发可能性高的高风险。高风险神经母细胞瘤的复发率为40〜50%。一旦复发，5年生存率据说仅有10%左右。父母为了降低复发风险而摸索治疗。然而，在国内没有找到幸之助君能够接受的治疗。",
                "grammar": "「〜を乗り越えました」— 克服了…。例：標準的な治療を乗り越えました（挺过了标准治疗）。\n「〜とされています」— 被认为是…。例：10％程度とされています（被认为是10%左右）。\n「〜ための治療」— 为了…的治疗。例：再発リスクを下げるための治療（为了降低复发风险的治疗）。",
                "vocab": [["標準的", "ひょうじゅんてき", "标准的"], ["乗り越える", "のりこえる", "克服、挺过"], ["リンパ節", "りんぱせつ", "淋巴结"], ["転移", "てんい", "转移"], ["再発", "さいはつ", "复发"], ["模索", "もさく", "摸索、探寻"]]
            },
        ]
    },
    {
        "slug": "senji-yuketsu-jintai-jikken",
        "title": "戦時中、大学で輸血の人体実験 患者に動物の血使用、死亡例も",
        "subtitle": "from 共同通信",
        "paras": [
            {
                "ja": "国内の複数の大学が戦時中、子どもを含む入院患者らに動物の血液などを使い輸血の人体実験をしていたことが8日、分かった。通常の輸血が困難な戦場での応用を意図した実験が多く、死者も出ていた。戦争と医学の問題に詳しい吉中丈志・京都大医学部臨床教授は「戦争遂行への協力で、非倫理的な人体実験のハードルが下がっていたと考えられる」と指摘する。",
                "en": "It was learned on the 8th that multiple universities in Japan conducted human blood-transfusion experiments during wartime, using animal blood and other substances on hospitalized patients, including children. Many of the experiments were intended for application on battlefields where normal transfusions were difficult, and there were deaths. Yoshinaka Takeshi, a clinical professor at Kyoto University's Faculty of Medicine who is knowledgeable about the issues of war and medicine, points out that \"as cooperation with the war effort, it is thought that the hurdle for unethical human experiments had been lowered.\"",
                "literal": "国内的数所大学在战时，对包括儿童在内的住院患者使用动物血液等进行输血人体实验一事于8日被查明。意图用于普通输血困难的战场应用的实验很多，也出现了死者。熟悉战争与医学问题的京都大学医学部临床教授吉中丈志指出：“可以认为，作为对战争遂行的协助，非伦理人体实验的门槛被降低了。”",
                "grammar": "「〜ことが分かった」— 得知、查明…。例：人体実験をしていたことが分かった（查明曾进行人体实验）。\n「〜を意図した」— 以…为目的的。例：戦場での応用を意図した実験（以战场应用为目的的实验）。\n「〜と考えられる」— 可以认为…。例：ハードルが下がっていたと考えられる（可以认为门槛被降低了）。",
                "vocab": [["戦時中", "せんじちゅう", "战争期间"], ["入院患者", "にゅういんかんじゃ", "住院患者"], ["輸血", "ゆけつ", "输血"], ["人体実験", "じんたいじっけん", "人体实验"], ["戦場", "せんじょう", "战场"], ["非倫理的", "ひりんりてき", "非伦理的"]]
            },
            {
                "ja": "京都府立医大、九州帝国大（現九州大）、熊本医大（現熊本大）が実施。採血から時間を置いた「保存血」、血液型の異なる「異型血」、動物由来の「異種血」を注入していた。1937年の日中戦争開始前から太平洋戦争期までの実験の論文が、当時の医学誌などに掲載されていることを吉中氏と共同通信が確認した。",
                "en": "Kyoto Prefectural University of Medicine, Kyushu Imperial University (now Kyushu University), and Kumamoto Medical College (now Kumamoto University) carried out the experiments. They injected \"preserved blood\" that had been stored after collection, \"incompatible blood\" of different blood types, and \"heterologous blood\" derived from animals. Yoshinaka and Kyodo News confirmed that papers on experiments from before the start of the Sino-Japanese War in 1937 through the Pacific War period had been published in medical journals of the time.",
                "literal": "京都府立医科大学、九州帝国大学（现九州大学）、熊本医科大学（现熊本大学）实施了实验。他们注入了采血后放置一段时间的“保存血”、血型不同的“异型血”、来自动物的“异种血”。吉中氏与共同通信社确认，1937年日中战争开始前至太平洋战争期间的实验论文曾刊登于当时的医学杂志等。",
                "grammar": "「〜から〜まで」— 从…到…。例：日中戦争開始前から太平洋戦争期まで（从日中战争开始前到太平洋战争时期）。\n「〜ことを確認した」— 确认了…。例：掲載されていることを確認した（确认了曾被刊登）。\n「〜に時間を置いた」— 放置了一段时间的…。例：採血から時間を置いた保存血（采血后放置了一段时间的保存血）。",
                "vocab": [["実施", "じっし", "实施"], ["採血", "さいけつ", "采血"], ["保存血", "ほぞんけつ", "保存血液"], ["異型血", "いけいけつ", "异型血液"], ["異種血", "いしゅけつ", "异种血液"], ["掲載", "けいさい", "刊登"]]
            },
            {
                "ja": "熊本医大では、脳の手術を受けウマの保存血を輸血された男性が、その後死亡。骨髄炎で転院してきた9歳男児は、21日間保存した血漿の注入からまもなく死亡した。担当者が中国・南京の病院を訪れてウマの保存血を注入した事例でも1人が亡くなった。",
                "en": "At Kumamoto Medical College, a man who underwent brain surgery and received a transfusion of preserved horse blood later died. A 9-year-old boy transferred to the hospital with osteomyelitis died soon after receiving an injection of blood plasma preserved for 21 days. In one case, an official visited a hospital in Nanjing, China, and injected preserved horse blood, and one person died.",
                "literal": "在熊本医科大学，接受脑部手术并被输入马保存血的男性之后死亡。因骨髓炎转院而来的9岁男童，在注入保存了21天的血浆后不久死亡。负责人到访中国南京的医院注入马保存血的案例中，也有1人死亡。",
                "grammar": "「〜を受け、〜」— 接受…之后，…。例：脳の手術を受け、その後死亡（接受脑部手术后死亡）。\n「〜からまもなく」— …之后不久。例：注入からまもなく死亡した（注入后不久死亡）。\n「〜でも」— 在…中也。例：事例でも1人が亡くなった（在案例中也有1人死亡）。",
                "vocab": [["ウマ", "うま", "马"], ["手術", "しゅじゅつ", "手术"], ["骨髄炎", "こつずいえん", "骨髓炎"], ["転院", "てんいん", "转院"], ["血漿", "けっしょう", "血浆"], ["事例", "じれい", "案例"]]
            },
        ]
    },
    {
        "slug": "budo-tounan-taiho",
        "title": "高級ブドウ約200房を盗んだ疑い 42歳男を逮捕 自宅から約300房発見",
        "subtitle": "from RSK山陽放送",
        "paras": [
            {
                "ja": "先月、岡山県久米南町のビニールハウスで栽培されていたブドウ約200房を盗んだ疑いで倉敷市の男が逮捕されました。窃盗の容疑で逮捕されたのは倉敷市の無職の男（42）です。警察によりますと、男は先月17日午後5時30分ごろから18日午前9時30分ごろまでの間、久米南町の男性（75）の畑にあるビニールハウス内から、栽培されていたシャインマスカット約200房（時価40万円相当）を盗んだ疑いが持たれています。",
                "en": "A man from Kurashiki City was arrested on suspicion of stealing about 200 bunches of grapes grown in a vinyl greenhouse in Kumenan Town, Okayama Prefecture, last month. Arrested on suspicion of theft is a 42-year-old unemployed man from Kurashiki City. According to police, the man is suspected of stealing about 200 bunches of Shine Muscat grapes (worth about 400,000 yen at market value) from a greenhouse on the farm of a 75-year-old man in Kumenan Town, between around 5:30 p.m. on the 17th and 9:30 a.m. on the 18th of last month.",
                "literal": "上个月，因涉嫌盗窃冈山县久米南町塑料大棚中栽培的约200串葡萄，仓敷市的一名男子被逮捕。因盗窃嫌疑被逮捕的是仓敷市的无业男子（42岁）。据警方称，该男子涉嫌在上月17日下午5点30分左右至18日上午9点30分左右期间，从久米南町一位75岁男性的农田塑料大棚内，盗走栽培中的阳光玫瑰葡萄约200串（时价约40万日元）。",
                "grammar": "「〜疑いで逮捕」— 因…嫌疑被逮捕。例：盗んだ疑いで逮捕されました（因盗窃嫌疑被逮捕）。\n「〜によりますと」— 据…称。例：警察によりますと（据警方称）。\n「〜（時価…相当）」— （时价…相当于）。例：時価40万円相当（时价相当于40万日元）。",
                "vocab": [["ビニールハウス", "びにーるはうす", "塑料大棚"], ["房", "ふさ", "（葡萄等的）串"], ["窃盗", "せっとう", "盗窃"], ["容疑", "ようぎ", "嫌疑"], ["無職", "むしょく", "无业"], ["時価", "じか", "时价、市价"]]
            },
            {
                "ja": "美咲署管内では、2024年10月以降ブドウの盗難被害が数件あったほか、今月にも井原署管内でブドウの盗難被害があったため、警察が合同捜査を行っていました。警察では現場付近の防犯カメラの映像などから男の容疑を特定したとして、きょう8日逮捕したもので、男の家からは約300房のブドウが見つかりました。",
                "en": "In the jurisdiction of Misaki Police Station, there had been several grape theft incidents since October 2024, and there was also a grape theft in the jurisdiction of Ibara Police Station this month, so police conducted a joint investigation. Police identified the man's suspicion from security camera footage near the scene and arrested him today, the 8th, and about 300 bunches of grapes were found at the man's home.",
                "literal": "在美咲警署辖区内，2024年10月以后除发生数起葡萄被盗案件外，本月井原警署辖区内也发生了葡萄被盗案件，因此警方进行了联合搜查。警方根据现场附近的防盗摄像头影像等锁定了该男子的嫌疑，于今天8日将其逮捕，并从男子家中发现了约300串葡萄。",
                "grammar": "「〜ほか、〜」— 除…之外，还…。例：数件あったほか、今月にも被害があった（除数起外，本月也有受害）。\n「〜として、〜」— 作为…，…（以此为由）。例：容疑を特定したとして逮捕（以锁定嫌疑为由逮捕）。\n「〜ものだ」— （表示说明、解释）。例：逮捕したもので（是逮捕了他的）。",
                "vocab": [["署管内", "しょかんない", "警署管辖区内"], ["盗難", "とうなん", "被盗"], ["被害", "ひがい", "受害"], ["合同捜査", "ごうどうそうさ", "联合搜查"], ["防犯カメラ", "ぼうはんかめら", "防盗摄像头"], ["特定", "とくてい", "锁定、确定"]]
            },
            {
                "ja": "調べに対し男は、「私がやったことに間違いありません」「盗んだブドウを売って生活費に充てていました」などと容疑を認めていて、男が販売目的でブドウを盗んでいたとみて余罪についても調べています。",
                "en": "In response to the investigation, the man admitted to the suspicion, saying, \"There's no mistake that I did it\" and \"I sold the stolen grapes and used the money for living expenses,\" and police are also investigating additional crimes, believing that the man stole the grapes for the purpose of selling them.",
                "literal": "面对调查，该男子承认了嫌疑，称“是我干的这一点没有错”“我把偷来的葡萄卖掉用作生活费了”，警方认为该男子以销售为目的盗窃葡萄，并正在调查其馀罪。",
                "grammar": "「〜に対し」— 面对…、对于…。例：調べに対し男は（面对调查，男子…）。\n「〜に間違いありません」— 无疑是…。例：私がやったことに間違いありません（是我干的这点没错）。\n「〜とみて」— 认为…。例：販売目的で盗んでいたとみて（认为是以销售为目的盗窃）。",
                "vocab": [["調べ", "しらべ", "调查、审讯"], ["生活費", "せいかつひ", "生活费"], ["充てる", "あてる", "充当、用作"], ["容疑を認める", "ようぎをみとめる", "承认嫌疑"], ["販売目的", "はんばいもくてき", "销售目的"], ["余罪", "よざい", "余罪、其他罪行"]]
            },
        ]
    },
    {
        "slug": "iran-horumuzu-keikai",
        "title": "イラン革命防衛隊が米国をけん制「海峡再開はイランの条件を全面的に受け入れる必要がある」",
        "subtitle": "from FNNプライムオンライン",
        "paras": [
            {
                "ja": "イラン革命防衛隊は8日、ホルムズ海峡の通航再開にはアメリカがイランの条件を全面的に受け入れる必要があるとの考えを改めて示しました。イラン革命防衛隊の報道官は8日、地元メディアに対し、ホルムズ海峡はイランにとって国家戦略上、重要な水路であり、通航する船舶はイランが定めるルールに従わなければならないと強調しました。",
                "en": "Iran's Islamic Revolutionary Guard Corps reiterated on the 8th its position that, for the resumption of navigation through the Strait of Hormuz, the United States must fully accept Iran's conditions. On the 8th, the IRGC spokesman emphasized to local media that the Strait of Hormuz is a strategically important waterway for Iran, and that ships passing through must comply with the rules set by Iran.",
                "literal": "伊朗革命卫队8日再次表明了这样的立场：霍尔木兹海峡恢复通航，美国必须全面接受伊朗的条件。伊朗革命卫队发言人8日对当地媒体强调，霍尔木兹海峡对伊朗而言是国家战略上的重要水路，通航的船舶必须遵守伊朗制定的规则。",
                "grammar": "「〜には〜必要がある」— 要…必须…。例：再開には受け入れる必要がある（要恢复通航必须接受）。\n「〜との考えを示しました」— 表明了…的想法。例：受け入れる必要があるとの考え（必须接受的想法）。\n「〜なければならない」— 必须…。例：ルールに従わなければならない（必须遵守规则）。",
                "vocab": [["革命防衛隊", "かくめいぼうえいたい", "革命卫队"], ["けん制", "けんせい", "牵制、威慑"], ["通航", "つうこう", "通航"], ["全面的", "ぜんめんてき", "全面的"], ["報道官", "ほうどうかん", "发言人"], ["強調", "きょうちょう", "强调"]]
            },
            {
                "ja": "そのうえで、ホルムズ海峡の再開は合意が近いとされるイランとオマーンの交渉とは関係なく、アメリカがイランの条件を全面的に受け入れたうえで交渉への介入をやめる必要があるとけん制しました。こうしたなか、UAE（アラブ首長国連邦）の外務省は8日、国営石油会社のタンカーがホルムズ海峡を航行中にイランによるミサイル攻撃を受けたと発表しました。けが人はいなかったということです。",
                "en": "Furthermore, the IRGC warned that the reopening of the Strait is unrelated to the Iran-Oman negotiations believed to be close to agreement, and that the United States must fully accept Iran's conditions and stop intervening in the negotiations. Amid this situation, the UAE (United Arab Emirates) Foreign Ministry announced on the 8th that a tanker of its state oil company was attacked by an Iranian missile while navigating the Strait of Hormuz. It was reported that there were no injuries.",
                "literal": "在此基础上，革命卫队还进行了牵制：霍尔木兹海峡的重新开放与据称接近达成协议的伊朗和阿曼的谈判无关，美国必须在全面接受伊朗条件的基础上停止对谈判的介入。在此背景下，UAE（阿拉伯联合酋长国）外交部8日宣布，国营石油公司的油轮在霍尔木兹海峡航行期间遭到伊朗的导弹攻击。据称没有人员受伤。",
                "grammar": "「〜とされる」— 被认为…。例：合意が近いとされる交渉（被认为接近达成协议的谈判）。\n「〜たうえで」— 在…的基础上。例：受け入れたうえで（在接受了的基础上）。\n「〜ということです」— 据说…。例：けが人はいなかったということです（据说没有受伤者）。",
                "vocab": [["合意", "ごうい", "达成协议"], ["交渉", "こうしょう", "谈判"], ["介入", "かいにゅう", "介入"], ["外務省", "がいむしょう", "外交部"], ["タンカー", "たんかー", "油轮"], ["ミサイル", "みさいる", "导弹"]]
            },
            {
                "ja": "UAE外務省は、イラン革命防衛隊がホルムズ海峡を経済的な圧力の手段として利用していると批判し、海峡の全面的かつ無条件での早期再開を求めました。",
                "en": "The UAE Foreign Ministry criticized the IRGC for using the Strait of Hormuz as a means of economic pressure, and called for the early reopening of the strait in full and without conditions.",
                "literal": "UAE外交部批判伊朗革命卫队将霍尔木兹海峡用作经济施压的手段，并呼吁海峡全面且无条件地早日恢复通航。",
                "grammar": "「〜として利用している」— 作为…加以利用。例：圧力の手段として利用している（作为施压手段利用）。\n「〜かつ〜」— 并且…（书面语）。例：全面的かつ無条件（全面且无条件）。\n「〜を求めました」— 呼吁、要求…。例：早期再開を求めました（呼吁早日恢复）。",
                "vocab": [["批判", "ひはん", "批评"], ["経済的", "けいざいてき", "经济上的"], ["圧力", "あつりょく", "压力"], ["手段", "しゅだん", "手段"], ["無条件", "むじょうけん", "无条件"], ["早期", "そうき", "早期"]]
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
