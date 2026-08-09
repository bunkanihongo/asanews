#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-10 (Mon) Edition"""
import json, os, subprocess, re, time
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-10'
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
# TODAY'S ARTICLES — 2026-08-10
# ==================================================================
articles = []
articles += [
    {
        "slug": "tenki-zenkoku-moushobi",
        "title": "全国的に日差しあり 東海から西では猛暑日予想 台風15号はあす関東から東北に接近、上陸へ",
        "subtitle": "from TBS NEWS DIG",
        "paras": [
            {
                "ja": "【全国的に日差しあり 東海から西では猛暑日予想】高気圧に覆われて、西日本から北日本にかけて晴れるところが多くなるでしょう。東海から西の地域では、35℃以上の猛暑日となるところもあり、危険な暑さに警戒が必要です。沖縄や九州は、中国大陸を進む台風13号に向かって流れ込む湿った空気の影響で雲が広がりやすく、雨の降る時間もあるでしょう。",
                "en": "[Sunshine nationwide; tropical days forecast from Tokai westward] Covered by a high-pressure system, many places from western Japan to northern Japan will be sunny. In areas from Tokai westward, some places will see tropical days of 35°C or higher, so caution against dangerous heat is needed. In Okinawa and Kyushu, clouds will spread easily due to moist air flowing toward Typhoon No. 13, which is moving across mainland China, and there will be periods of rain.",
                "literal": "【全国有日照，东海以西预计有酷暑日】受高气压覆盖，从西日本到北日本放晴的地方将会增多。东海以西的地区也有达到35℃以上酷暑日的地方，需要警惕危险的高温。冲绳和九州受流向在中国大陆推进的台风13号的潮湿空气的影响，云层容易扩散，也会有降雨的时段。",
                "grammar": "「〜にかけて」— 从…到…（表示范围）。例：西日本から北日本にかけて晴れる（从西日本到北日本放晴）。\n「〜となることもあり」— 也有变成…的情况。例：猛暑日となるところもあり（也有达到酷暑日的地方）。\n「〜やすい」— 容易…。例：雲が広がりやすく（云层容易扩散）。",
                "vocab": [["高気圧", "こうきあつ", "高气压"], ["覆う", "おおう", "覆盖"], ["猛暑日", "もうしょび", "酷暑日（35度以上）"], ["警戒", "けいかい", "警戒、警惕"], ["湿った", "しめった", "潮湿的"], ["流れ込む", "ながれこむ", "流入"]]
            },
            {
                "ja": "【きょうの各地の予想最高気温】札幌:26℃ 釧路:25℃ 青森:27℃ 盛岡:28℃ 仙台:27℃ 新潟:30℃ 長野:32℃ 金沢:32℃ 名古屋:35℃ 東京:31℃ 大阪:35℃ 岡山:35℃ 広島:34℃ 松江:31℃ 高知:33℃ 福岡:34℃ 鹿児島:34℃ 那覇:31℃",
                "en": "[Today's forecast maximum temperatures by region] Sapporo 26°C, Kushiro 25°C, Aomori 27°C, Morioka 28°C, Sendai 27°C, Niigata 30°C, Nagano 32°C, Kanazawa 32°C, Nagoya 35°C, Tokyo 31°C, Osaka 35°C, Okayama 35°C, Hiroshima 34°C, Matsue 31°C, Kochi 33°C, Fukuoka 34°C, Kagoshima 34°C, Naha 31°C.",
                "literal": "【今天各地预计最高气温】札幌26℃、钏路25℃、青森27℃、盛冈28℃、仙台27℃、新潟30℃、长野32℃、金泽32℃、名古屋35℃、东京31℃、大阪35℃、冈山35℃、广岛34℃、松江31℃、高知33℃、福冈34℃、鹿儿岛34℃、那霸31℃。",
                "grammar": "「〜予想最高気温」— 预计最高气温。例：各地の予想最高気温（各地预计最高气温）。\n「〜:〜℃」— 〜：〜℃（数值对应）。例：名古屋:35℃（名古屋35℃）。\n「〜に覆われて」— 被…覆盖。例：高気圧に覆われて（被高气压覆盖）。",
                "vocab": [["各地", "かくち", "各地"], ["予想", "よそう", "预计"], ["最高気温", "さいこうきおん", "最高气温"], ["札幌", "さっぽろ", "札幌"], ["那覇", "なは", "那霸"], ["鹿児島", "かごしま", "鹿儿岛"]]
            },
            {
                "ja": "【東海や関東は午後天気急変のおそれ】気温が上がる午後は大気の状態が不安定となり、東海や関東で突然の雨や雷雨に注意が必要です。午前中晴れていても油断せず、急に冷たい風が吹いてきたり、黒い雲が見えたりしたときは、建物の中に移動するようにしましょう。",
                "en": "[Risk of sudden weather changes in the afternoon in Tokai and Kanto] In the afternoon, when temperatures rise, atmospheric conditions become unstable, so attention is needed for sudden rain and thunderstorms in Tokai and Kanto. Even if it is sunny in the morning, do not let your guard down — when a cold wind suddenly blows or dark clouds appear, move inside a building.",
                "literal": "【东海和关东午后有天气骤变之虞】气温上升的午后大气状态将变得不稳定，东海和关东需要注意突然的降雨和雷雨。即使上午晴朗也不要大意，当突然吹来冷风、或看到黑云时，请转移到建筑物内。",
                "grammar": "「〜おそれ」— 有…的虞/可能。例：天気急変のおそれ（天气骤变的可能）。\n「〜たり〜たり」— 又…又…（举例）。例：冷たい風が吹いてきたり、黒い雲が見えたり（冷风吹来或黑云出现）。\n「〜ようにしましょう」— 请…吧（建议）。例：建物の中に移動するようにしましょう（请转移到建筑物内）。",
                "vocab": [["急変", "きゅうへん", "骤变"], ["大気", "たいき", "大气"], ["不安定", "ふあんてい", "不稳定"], ["雷雨", "らいう", "雷雨"], ["油断", "ゆだん", "疏忽、大意"], ["移動", "いどう", "移动、转移"]]
            },
            {
                "ja": "【台風15号はあす関東から東北に接近、上陸へ】台風15号はあすの午後関東から東北に接近、上陸する見込みです。きょうのうちに側溝の掃除をしたり、飛ばされやすいものを家の中にしまっておいたり、台風への備えをしてください。また、きょうもうねりを伴った高波に注意が必要です。",
                "en": "[Typhoon No. 15 to approach and make landfall from Kanto to Tohoku tomorrow] Typhoon No. 15 is expected to approach and make landfall from Kanto to Tohoku tomorrow afternoon. Before the day is over, clean out the gutters, put things that are easily blown away inside the house, and make preparations for the typhoon. Also, caution is needed today for high waves accompanied by swells.",
                "literal": "【台风15号明天将从关东到东北接近、登陆】台风15号预计明天下午从关东接近东北并登陆。请在今天之内清扫排水沟、把容易被吹飞的东西收进家中，做好台风的防备。另外，今天也需要注意伴随涌浪的大浪。",
                "grammar": "「〜見込みです」— 预计…。例：上陸する見込みです（预计登陆）。\n「〜のうちに」— 在…之内。例：きょうのうちに（在今天之内）。\n「〜を伴った」— 伴随…的。例：うねりを伴った高波（伴随涌浪的大浪）。",
                "vocab": [["接近", "せっきん", "接近"], ["上陸", "じょうりく", "登陆"], ["側溝", "そっこう", "排水沟"], ["備え", "そなえ", "防备"], ["うねり", "うねり", "涌浪"], ["高波", "たかなみ", "大浪"]]
            },
        ]
    },
    {
        "slug": "nanao-ooame",
        "title": "七尾大雨、レベル３警報 列車運休、穴水でも冠水",
        "subtitle": "from 北國新聞社",
        "paras": [
            {
                "ja": "9日の石川県内は曇り、局所的に雨が激しく降った。七尾は明け方にバケツをひっくり返したような雨となり、列車が運休したり、道路が冠水したりした。金沢地方気象台は七尾市に一時、レベル3の大雨警報を出し、注意を求めた。七尾では午前5時37分までの1時間に37・0ミリの雨を観測。13日の大潮を控えて潮位も高く、七尾市、穴水町の沿岸部では道路や農地が冠水した。",
                "en": "On the 9th, Ishikawa Prefecture was cloudy, with heavy rain falling locally. In Nanao, rain like a tipped-over bucket fell around dawn, causing train suspensions and flooded roads. The Kanazawa Local Meteorological Observatory temporarily issued a Level 3 heavy rain warning for Nanao City and called for caution. In Nanao, 37.0 mm of rain was observed in one hour up to 5:37 a.m. With the spring tide on the 13th approaching, the tide level was also high, and roads and farmland were flooded in coastal areas of Nanao City and Nakanoto Town.",
                "literal": "9日的石川县内为阴天，局部降雨猛烈。七尾在黎明时分降下像打翻水桶般的大雨，列车停运、道路积水。金泽地方气象台一度向七尾市发布3级大雨警报，呼吁注意。七尾在截至上午5点37分的1小时内观测到37.0毫米的降雨。由于13日大潮临近，潮位也很高，七尾市、穴水町的沿海地区道路和农田被淹。",
                "grammar": "「〜をひっくり返したような」— 像打翻…一样的。例：バケツをひっくり返したような雨（像打翻水桶一样的雨）。\n「〜たり〜たりした」— 又…又…。例：運休したり、冠水したりした（既停运又积水）。\n「〜を控えて」— 临近…、即将…。例：大潮を控えて潮位も高く（临近大潮，潮位也高）。",
                "vocab": [["局所的", "きょくしょてき", "局部性的"], ["明け方", "あけがた", "黎明、拂晓"], ["運休", "うんきゅう", "停运"], ["冠水", "かんすい", "积水、淹没"], ["大潮", "おおしお", "大潮"], ["潮位", "ちょうい", "潮位"]]
            },
            {
                "ja": "能登半島地震による地盤の低下が指摘される地域も含まれ、住民からは台風の接近が予想されることから不安の声が上がった。穴水町中居の仮設住宅住吉団地の周辺では、高潮の影響で道路の冠水が深さ40センチほどに達した。住民によると、午前4時ごろに町や石川県が設置したポンプ計6台を稼働させたという。",
                "en": "The flooded areas included regions where ground subsidence due to the Noto Peninsula earthquake has been pointed out, and residents voiced anxiety because the approach of a typhoon is expected. Around Sumiyoshi temporary housing complex in Nakai, Nakanoto Town, roads flooded to a depth of about 40 centimeters due to the storm surge. According to residents, a total of six pumps installed by the town and Ishikawa Prefecture were operated from around 4 a.m.",
                "literal": "其中也包括被指出因能登半岛地震而地面下沉的地区，由于预计台风将接近，居民中响起了不安的声音。在穴水町中居的临时住宅住吉团地周边，受风暴潮影响道路积水深达约40厘米。据居民称，凌晨4点左右町和石川县设置的共6台水泵开始运转。",
                "grammar": "「〜による」— 由…造成的。例：地震による地盤の低下（地震造成的地面下沉）。\n「〜ことから」— 因为…（原因）。例：台風の接近が予想されることから（因为预计台风接近）。\n「〜によると」— 据…说。例：住民によると（据居民说）。",
                "vocab": [["地盤", "じばん", "地基、地面"], ["仮設住宅", "かせつじゅうたく", "临时住宅"], ["高潮", "たかしお", "风暴潮"], ["ポンプ", "ぽんぷ", "水泵"], ["稼働", "かどう", "运转、启动"], ["不安", "ふあん", "不安"]]
            },
            {
                "ja": "JR七尾線は午前5時39分ごろから羽咋―和倉温泉駅間で運転を見合わせ、9時50分に再開した。特急2本、普通列車10本が運休し、最大50分の遅れが生じた。のと鉄道は上下線6本を運休し、七尾―田鶴浜駅間ではバスで代替輸送した。最高気温は金沢30・1度、輪島27・8度など。各消防によると、9日午後6時までに金沢、小松など4市町で20〜90代の男女計8人が熱中症の疑いで搬送された。",
                "en": "JR Nanao Line suspended operations between Hakui and Wakuraonsen stations from around 5:39 a.m., resuming at 9:50 a.m. Two limited express trains and 10 local trains were cancelled, causing delays of up to 50 minutes. The Noto Railway cancelled six trains in both directions and provided substitute bus service between Nanao and Tadaotsu stations. Maximum temperatures reached 30.1°C in Kanazawa and 27.8°C in Wajima, among others. According to fire departments, by 6 p.m. on the 9th, a total of 8 men and women in their 20s to 90s in four cities and towns including Kanazawa and Komatsu were transported to hospitals on suspicion of heatstroke.",
                "literal": "JR七尾线从凌晨5点39分左右起在羽咋—和仓温泉站之间暂停运行，9点50分恢复。特快2列、普通列车10列停运，出现最大50分钟的延误。能登铁道上下行共6列停运，七尾—田鹤滨站之间用巴士代替运输。最高气温金泽30.1度、轮岛27.8度等。据各消防部门称，截至9日下午6点，金泽、小松等4个市町有20至90多岁的男女共8人因疑似中暑被送医。",
                "grammar": "「〜を見合わせる」— 暂停…。例：運転を見合わせ（暂停运行）。\n「〜の遅れが生じた」— 发生了…的延误。例：最大50分の遅れが生じた（发生了最大50分钟的延误）。\n「〜の疑いで搬送された」— 因疑似…被送医。例：熱中症の疑いで搬送された（因疑似中暑被送医）。",
                "vocab": [["運転", "うんてん", "运行、驾驶"], ["再開", "さいかい", "恢复、重新开始"], ["特急", "とっきゅう", "特快列车"], ["代替輸送", "だいたいゆそう", "替代运输"], ["熱中症", "ねっちゅうしょう", "中暑"], ["搬送", "はんそう", "运送、送医"]]
            },
        ]
    },
    {
        "slug": "suinan-sujiko",
        "title": "各地で水難事故相次ぐ 千葉・いすみ市の海岸で男性が波にさらわれ死亡 茨城・鉾田市では女性3人が流され1人死亡",
        "subtitle": "from TBS NEWS DIG",
        "paras": [
            {
                "ja": "きのう（9日）、千葉県と茨城県で水難事故が相次ぎ、2人が死亡、1人が重体です。きのう正午ごろ、千葉県いすみ市の海岸で、「男性が波にさらわれ、姿が見えない」と119番通報がありました。警察や消防などによりますと、男性は千葉県八街市に住む玄間晃裕さん（38）で、交際相手と海岸の岩場を散歩中に波にさらわれて行方が分からなくなったということです。玄間さんは300～400メートルほど離れた沖合で発見され、海上保安庁によって救助されましたが、その後、死亡が確認されました。当時、いすみ市には波浪注意報が発表されていたということです。",
                "en": "Yesterday (the 9th), water accidents occurred one after another in Chiba and Ibaraki prefectures, leaving two people dead and one in critical condition. Around noon yesterday, a 119 call was made at a beach in Isumi City, Chiba, saying \"a man was swept away by waves and can no longer be seen.\" According to police and firefighters, the man was Genma Akihiro (38), a resident of Yachimata City, Chiba, who disappeared after being swept away by waves while walking on a rocky beach with his partner. Genma was found offshore about 300 to 400 meters away and rescued by the Japan Coast Guard, but his death was later confirmed. At the time, a high wave advisory had been issued for Isumi City.",
                "literal": "昨天（9日），千叶县和茨城县接连发生水难事故，2人死亡、1人重伤。昨天中午前后，千叶县夷隅市的海岸接到119报警称“男子被浪卷走，看不到身影”。据警察和消防称，该男子是住在千叶县八街市的玄间晃裕（38岁），与交往对象在海边岩石区散步时被浪卷走、去向不明。玄间在约300〜400米外的海面上被发现，被海上保安厅救起，但之后确认死亡。当时，夷隅市发布了海浪注意报。",
                "grammar": "「〜が相次ぎ」— …接连发生。例：水難事故が相次ぎ（水难事故接连发生）。\n「〜によりますと」— 据…称。例：警察や消防などによりますと（据警察和消防等称）。\n「〜ということです」— 据说…。例：発表されていたということです（据说当时已发布）。",
                "vocab": [["水難事故", "すいなんじこ", "水难事故"], ["さらわれる", "さらわれる", "被卷走、被冲走"], ["交際相手", "こうさいあいて", "交往对象"], ["沖合", "おきあい", "海面、近海"], ["海上保安庁", "かいじょうほあんちょう", "海上保安厅"], ["波浪注意報", "はろうちゅういほう", "海浪注意报"]]
            },
            {
                "ja": "また、きのう午後0時すぎ、茨城県鉾田市の海岸でも、海水浴に来ていた女性3人が水中の深みにはまり、流されたということです。1人は自力で岸に辿り着いて通報し、ほかの2人は、現場に駆けつけた救急隊員に救助されましたが、石岡市の会社員・山口莉子さん（23）が意識不明の状態で病院に運ばれ、その後、死亡が確認されました。もう1人の24歳の女性も病院に運ばれましたが、重体です。",
                "en": "Also, shortly after noon yesterday, at a beach in Hokota City, Ibaraki, three women who had come swimming were caught in deep water and swept away, according to reports. One reached the shore on her own and called for help, and the other two were rescued by emergency crews who rushed to the scene, but Yamaguchi Riko (23), a company employee from Ishioka City, was taken to the hospital unconscious and her death was later confirmed. The other woman, 24, was also taken to the hospital and is in critical condition.",
                "literal": "另外，昨天中午12点多，茨城县鉾田市的海岸，来海水浴的3名女性陷入水中深处被卷走。1人靠自己游回岸边报警，另外2人被赶到现场的急救队员救起，但石冈市的公司职员山口莉子（23岁）处于意识不清状态被送往医院，之后确认死亡。另一名24岁女性也被送往医院，目前重伤。",
                "grammar": "「〜にはまり」— 陷入…。例：深みにはまり（陷入深处）。\n「〜に駆けつけた」— 赶到…的。例：現場に駆けつけた救急隊員（赶到现场的急救队员）。\n「〜が確認されました」— 确认了…。例：死亡が確認されました（确认死亡）。",
                "vocab": [["海水浴", "かいすいよく", "海水浴"], ["深み", "ふかみ", "深处"], ["辿り着く", "たどりつく", "好不容易到达"], ["救急隊員", "きゅうきゅうたいいん", "急救队员"], ["意識不明", "いしきふめい", "意识不明"], ["重体", "じゅうたい", "重伤、病危"]]
            },
            {
                "ja": "現場は、離岸流が起こりやすい人工岬「ヘッドランド」の近くの遊泳禁止エリアだったということで、警察は「ヘッドランド」近くに立ち入らないよう呼びかけています。",
                "en": "The scene was a no-swimming area near an artificial cape called a \"headland,\" where rip currents are likely to occur, and police are calling on people not to enter the area near the headland.",
                "literal": "现场是容易发生离岸流的人工岬“防波堤（headland）”附近的禁止游泳区域，警方呼吁不要进入“headland”附近。",
                "grammar": "「〜やすい」— 容易…。例：離岸流が起こりやすい（容易发生离岸流）。\n「〜ということで」— 因为据说…（理由）。例：遊泳禁止エリアだったということで（因为是禁止游泳区域）。\n「〜よう呼びかけています」— 呼吁…。例：立ち入らないよう呼びかけています（呼吁不要进入）。",
                "vocab": [["離岸流", "りがんりゅう", "离岸流"], ["人工岬", "じんこうみさき", "人工岬角"], ["遊泳禁止", "ゆうえいきんし", "禁止游泳"], ["エリア", "えりあ", "区域"], ["立ち入る", "たちいる", "进入"], ["呼びかける", "よびかける", "呼吁"]]
            },
        ]
    },
    {
        "slug": "taiwan-nagasaki-sikiten",
        "title": "台湾、長崎式典の参加者格下げ 席が「使節団区域外」と抗議",
        "subtitle": "from 時事通信",
        "paras": [
            {
                "ja": "台湾の駐日大使に当たる台北経済文化代表処の李逸洋代表は9日、長崎市が同日開いた原爆犠牲者慰霊平和祈念式典を欠席し、駐福岡弁事処（領事館に相当）の処長が代理出席したとSNSで発表した。",
                "en": "Lee Yi-yang, head of the Taipei Economic and Cultural Representative Office, who serves as Taiwan's de facto ambassador to Japan, announced on SNS on the 9th that he would skip the Peace Memorial Ceremony for the Atomic Bomb Victims held by Nagasaki City that day, and that the head of the Fukuoka branch office (equivalent to a consulate) would attend in his place.",
                "literal": "相当于台湾驻日大使的台北经济文化代表处代表李逸洋9日宣布，缺席长崎市当天举行的原子弹牺牲者慰灵和平祈念仪式，由驻福冈办事处（相当于领事馆）处长代理出席。",
                "grammar": "「〜に当たる」— 相当于…。例：駐日大使に当たる（相当于驻日大使）。\n「〜とSNSで発表した」— 通过SNS宣布…。例：代理出席したと発表した（宣布由代理出席）。",
                "vocab": [["駐日大使", "ちゅうにちたいし", "驻日大使"], ["代表処", "だいひょうしょ", "代表处"], ["式典", "しきてん", "仪式、典礼"], ["欠席", "けっせき", "缺席"], ["代理", "だいり", "代理"], ["相当", "そうとう", "相当于"]]
            },
            {
                "ja": "台湾代表の席が「使節団の区域外」だったと記し、抗議のため参加者を格下げしたと説明した。台湾は昨年から同式典に参加している。李氏は「長崎市が中国に追従し、日本に友好的な台湾をおとしめた」として「厳正な抗議と非難」を表明した。",
                "en": "He stated that Taiwan's seats were \"outside the delegation area,\" explaining that he downgraded the participants in protest. Taiwan has participated in the ceremony since last year. Lee expressed \"solemn protest and condemnation,\" saying that \"Nagasaki City has followed China and disparaged Taiwan, which is friendly to Japan.\"",
                "literal": "他在SNS上写道台湾代表的座位位于“使节团区域之外”，并说明为抗议而降低了参加者级别。台湾从去年起参加该仪式。李氏以“长崎市追随中国、贬低了亲日的台湾”为由，表明了“严正抗议和谴责”。",
                "grammar": "「〜と記し」— 写道…。例：区域外だったと記し（写道在区域之外）。\n「〜ため」— 为了…。例：抗議のため（为了抗议）。\n「〜として」— 以…为由。例：おとしめたとして（以贬低…为由）。",
                "vocab": [["使節団", "しせつだん", "使节团"], ["区域", "くいき", "区域"], ["格下げ", "かくさげ", "降低级别"], ["追従", "ついじゅう", "追随、迎合"], ["おとしめる", "おとしめる", "贬低、诋毁"], ["非難", "ひなん", "谴责、指责"]]
            },
            {
                "ja": "対日関係を極めて重視する頼清徳政権の高官が、日本の自治体を強く批判するのは異例。",
                "en": "It is unusual for a senior official of the Lai Ching-te administration, which places great importance on relations with Japan, to strongly criticize a Japanese local government.",
                "literal": "极为重视对日关系的赖清德政权的高官强烈批评日本地方政府，这实属罕见。",
                "grammar": "「〜を重視する」— 重视…。例：対日関係を重視する（重视对日关系）。\n「〜のは異例」— …是罕见的。例：強く批判するのは異例（强烈批评实属罕见）。",
                "vocab": [["対日関係", "たいにちかんけい", "对日关系"], ["極めて", "きわめて", "极其"], ["政権", "せいけん", "政权"], ["高官", "こうかん", "高官"], ["自治体", "じちたい", "地方政府、自治体"], ["異例", "いれい", "罕见、破例"]]
            },
        ]
    },
    {
        "slug": "jieitai-kokusan-ai",
        "title": "自衛隊の指揮統制に国産AI導入へ 政府が検討 「サカナAI」が有力、中国製は排除",
        "subtitle": "from 読売新聞オンライン",
        "paras": [
            {
                "ja": "政府は、自衛隊の部隊運用における中枢の指揮統制に、国産の人工知能（ＡＩ）を導入する方向で検討に入った。国産ＡＩを中核に据えつつ、世界最先端の外国製ＡＩなどと連携させ、迅速な意思決定の体制づくりを目指す。先端技術で戦争の形態が変化する中、ＡＩの導入によって「新しい戦い方」への対応を急ぐ。",
                "en": "The government has begun considering introducing domestically produced artificial intelligence (AI) into the core command and control of Self-Defense Forces operations. While placing domestic AI at the core, it aims to build a system for rapid decision-making by linking it with the world's most advanced foreign AI. As the nature of warfare changes with cutting-edge technology, the government is rushing to respond to \"new ways of fighting\" through the introduction of AI.",
                "literal": "政府已开始探讨在自卫队部队运用的中枢指挥统制中引入国产人工智能（AI）。在将国产AI作为核心的同时，与世界最尖端的外国制AI等联动，目标是建立迅速决策的体制。在尖端技术使战争形态发生变化的背景下，政府正通过引入AI加紧应对“新的作战方式”。",
                "grammar": "「〜方向で検討に入った」— 开始按…方向探讨。例：導入する方向で検討に入った（开始探讨引入）。\n「〜つつ」— 一边…一边…。例：中核に据えつつ（一边作为核心）。\n「〜を目指す」— 以…为目标。例：体制づくりを目指す（以建立体制为目标）。",
                "vocab": [["指揮統制", "しきとうせい", "指挥统制"], ["国産", "こくさん", "国产"], ["人工知能", "じんこうちのう", "人工智能"], ["中核", "ちゅうかく", "核心"], ["連携", "れんけい", "联动、合作"], ["意思決定", "いしけってい", "决策"]]
            },
            {
                "ja": "複数の政府関係者が明らかにした。自衛隊の指揮統制にＡＩが組み込まれるのは初めて。年末に改定する国家安全保障戦略など安保関連３文書に、指揮統制でのＡＩの活用方針を盛り込む。指揮統制は、脅威の状況把握を踏まえ、自衛隊部隊の対処計画の策定から命令を下すまでのプロセスを指す。無人機や衛星、センサーなど先端技術の進展を受け、膨大なデータを短時間に処理してミサイル防衛などの意思決定を行う能力の向上が課題となっていた。",
                "en": "Multiple government officials revealed this. It will be the first time AI is incorporated into SDF command and control. The policy for utilizing AI in command and control will be included in three security-related documents, including the National Security Strategy, to be revised at the end of the year. Command and control refers to the process from formulating response plans for SDF units to issuing orders, based on understanding the threat situation. With advances in cutting-edge technology such as drones, satellites, and sensors, improving the ability to process vast amounts of data in a short time and make decisions such as missile defense had become a challenge.",
                "literal": "多名政府相关人士透露了这一消息。这是AI首次被编入自卫队的指挥统制。将在年底修订的国家安全保障战略等安保相关3份文件中写入指挥统制中活用AI的方针。指挥统制是指基于对威胁状况的把握，从制定自卫队部队应对计划到下命令为止的过程。随着无人机、卫星、传感器等尖端技术的进步，在短时间内处理庞大数据并作出导弹防御等决策的能力提升成为课题。",
                "grammar": "「〜が明らかにした」— …透露/明确了。例：複数の政府関係者が明らかにした（多名政府相关人士透露）。\n「〜を踏まえ」— 基于…。例：状況把握を踏まえ（基于状况把握）。\n「〜が課題となっていた」— …成为课题。例：能力の向上が課題となっていた（能力提升成为课题）。",
                "vocab": [["関係者", "かんけいしゃ", "相关人士"], ["改定", "かいてい", "修订"], ["安全保障", "あんぜんほしょう", "安全保障"], ["脅威", "きょうい", "威胁"], ["膨大", "ぼうだい", "庞大"], ["課題", "かだい", "课题"]]
            },
            {
                "ja": "政府は、自衛隊指揮官の迅速な判断を後押しするため、情報の収集、分析、評価などをＡＩに担わせることを想定する。機密保持など経済安全保障の観点から、国産ＡＩを中心に据える方向だ。国産ＡＩとして最有力視されるのは新興企業「サカナＡＩ」（東京）が開発する「ＳａｋａｎａＦｕｇｕ（サカナ・フグ）」だ。サカナ・フグは、司令塔となるＡＩが複数のＡＩに処理を割り振り、低コストで高性能を出せる「オーケストレーション」機能が特徴だ。",
                "en": "The government envisions having AI handle information gathering, analysis, and evaluation to support quick judgment by SDF commanders. From the perspective of economic security, including confidentiality, it is leaning toward placing domestic AI at the center. The leading candidate for domestic AI is \"Sakana Fugu,\" developed by the startup \"Sakana AI\" (Tokyo). Sakana Fugu features an \"orchestration\" function in which a command-center AI allocates processing to multiple AIs, achieving high performance at low cost.",
                "literal": "政府设想让AI承担信息的收集、分析和评估等，以支持自卫队指挥官迅速作出判断。从机密保持等经济安全保障的观点出发，政府倾向于以国产AI为中心。国产AI中最有希望的是新兴企业“Sakana AI”（东京）开发的“Sakana Fugu”。Sakana Fugu的特点是“编排（orchestration）”功能，即作为司令塔的AI将处理分配给多个AI，能以低成本实现高性能。",
                "grammar": "「〜ため」— 为了…。例：判断を後押しするため（为了支持判断）。\n「〜に担わせる」— 让…承担。例：ＡＩに担わせる（让AI承担）。\n「〜として最有力視される」— 作为…被最看好。例：国産ＡＩとして最有力視される（作为国产AI最被看好）。",
                "vocab": [["後押し", "あとおし", "支持、推动"], ["収集", "しゅうしゅう", "收集"], ["機密保持", "きみつほじ", "机密保持"], ["経済安全保障", "けいざいあんぜんほしょう", "经济安全保障"], ["新興企業", "しんこうきぎょう", "新兴企业"], ["割り振る", "わりふる", "分配"]]
            },
            {
                "ja": "同社はサカナ・フグの開発段階で中国のＡＩモデルも利用していたが、防衛分野への提供では中国モデルを排除する。開発チームも日本国籍者に限る。政府関係者は、「データやシステムを外国に頼らず、自国で自律的に管理する『ＡＩ主権』を重視する政府の方針にも合致する」と説明する。防衛省は７日、安保関連３文書のうち国家防衛戦略など２文書に関して骨格を公表し、この中でＡＩの支援により意思決定の速度・精度を向上させる方針を明記した。",
                "en": "The company also used Chinese AI models during the development stage of Sakana Fugu, but it will exclude Chinese models when providing for the defense field. The development team is also limited to Japanese nationals. A government official explained that this \"also aligns with the government's policy of emphasizing 'AI sovereignty' — autonomously managing data and systems domestically without relying on foreign countries.\" On the 7th, the Defense Ministry released the framework for two of the three security-related documents, including the National Defense Strategy, and clearly stated the policy of improving the speed and accuracy of decision-making with AI support.",
                "literal": "该公司在Sakana Fugu的开发阶段也曾使用中国的AI模型，但在面向防卫领域的提供中将排除中国模型。开发团队也仅限于日本国籍者。政府相关人士说明称，这“也符合政府重视‘AI主权’的方针——不依赖外国、在本国自主管理数据和系统”。防卫省7日公布了安保相关3份文件中包括国家防卫战略在内的2份文件的框架，其中明确写入了借助AI支援提高决策速度与精度的方针。",
                "grammar": "「〜に限る」— 仅限于…。例：日本国籍者に限る（仅限于日本国籍者）。\n「〜に合致する」— 符合…。例：政府の方針にも合致する（也符合政府的方针）。\n「〜に関して」— 关于…。例：２文書に関して骨格を公表し（公布了关于2份文件的框架）。",
                "vocab": [["排除", "はいじょ", "排除"], ["国籍", "こくせき", "国籍"], ["自律的", "じりつてき", "自主的、自律的"], ["合致", "がっち", "符合、一致"], ["骨格", "こっかく", "框架、骨架"], ["明記", "めいき", "明确记载"]]
            },
        ]
    },
    {
        "slug": "gaza-heiwa-koukeihyou",
        "title": "ガザ和平の工程表「拒否」 イスラエル、武器放棄要求",
        "subtitle": "from 共同通信",
        "paras": [
            {
                "ja": "イスラエルのネタニヤフ首相は9日の治安閣議で、パレスチナ自治区ガザ地区の和平実現に向けてトランプ米政権が主導する暫定統治機関「平和評議会」が示した工程表を「拒否する」と述べた。イスラム組織ハマスの武装解除は重火器に限らず「あらゆる武器の放棄」が必要だとし、武装解除までイスラエル軍は撤収しないと強調した。",
                "en": "At a security cabinet meeting on the 9th, Israeli Prime Minister Netanyahu said he \"rejects\" the roadmap presented by the \"Peace Council,\" a provisional governing body led by the Trump administration, toward achieving peace in the Gaza Strip of the Palestinian territories. He stressed that the disarmament of the Islamic organization Hamas requires \"the abandonment of all weapons,\" not just heavy weapons, and that the Israeli military will not withdraw until disarmament is complete.",
                "literal": "以色列总理内塔尼亚胡在9日的安全内阁会议上表示“拒绝”由特朗普美国政权主导的临时统治机构“和平评议会”为实现巴勒斯坦自治区加沙地区和平而提出的路线图。他表示哈马斯伊斯兰组织的解除武装不仅限于重武器，必须“放弃一切武器”，并强调在解除武装之前以色列军队不会撤出。",
                "grammar": "「〜に向けて」— 面向…、为了…。例：和平実現に向けて（为了实现和平）。\n「〜に限らず」— 不仅限于…。例：重火器に限らず（不仅限于重武器）。\n「〜まで〜ない」— 在…之前不…。例：武装解除まで撤収しない（在解除武装前不撤军）。",
                "vocab": [["治安閣議", "ちあんかくぎ", "安全内阁会议"], ["暫定", "ざんてい", "暂定、临时"], ["統治機関", "とうちきかん", "统治机构"], ["工程表", "こうていひょう", "路线图、进度表"], ["武装解除", "ぶそうかいじょ", "解除武装"], ["撤収", "てっしゅう", "撤出"]]
            },
            {
                "ja": "トランプ米大統領は7月30日、ハマスの武装解除とイスラエル軍の撤収に関する「歴史的合意」に達したと表明していた。ネタニヤフ氏は反対の立場を明確にし、武装解除に関し米国と協議しているとも語った。イスラエルでは10月27日に総選挙を控えており、国民や連立を組む極右政党に強硬姿勢をアピールしたとみられる。",
                "en": "On July 30, US President Trump had declared that a \"historic agreement\" had been reached regarding Hamas's disarmament and the withdrawal of Israeli forces. Netanyahu clearly took a position of opposition and also said he was consulting with the United States on disarmament. With a general election scheduled for October 27 in Israel, he appears to have appealed his hard-line stance to the public and the far-right parties in his coalition.",
                "literal": "美国总统特朗普7月30日曾表示，就哈马斯解除武装和以色列军队撤军达成了“历史性协议”。内塔尼亚胡明确表示反对立场，并表示正在就解除武装与美国进行磋商。以色列将于10月27日迎来大选，此举被认为是在向国民和联合执政的极右政党展示强硬姿态。",
                "grammar": "「〜に関する」— 关于…的。例：撤収に関する合意（关于撤军的协议）。\n「〜に達した」— 达成…。例：合意に達した（达成协议）。\n「〜を控えており」— 即将迎来…。例：総選挙を控えており（即将迎来大选）。",
                "vocab": [["歴史的", "れきしてき", "历史性的"], ["合意", "ごうい", "协议、共识"], ["明確", "めいかく", "明确"], ["協議", "きょうぎ", "磋商、协商"], ["総選挙", "そうせんきょ", "大选"], ["強硬", "きょうこう", "强硬"]]
            },
            {
                "ja": "ハマスは声明を出し「工程表に同意し、順守する」と改めて訴えた。ハマスはイスラエル軍のガザ撤収が武装解除の条件と主張している。双方の立場は平行線をたどったままで、和平計画は停滞状態が続きそうだ。平和評議会は7月31日、和平計画を完了させる工程表を発表していた。",
                "en": "Hamas issued a statement and again appealed that it \"agrees with and will abide by the roadmap.\" Hamas insists that the withdrawal of Israeli forces from Gaza is a condition for disarmament. The two sides' positions remain on parallel lines, and the peace plan is likely to remain stalled. The Peace Council had announced on July 31 a roadmap for completing the peace plan.",
                "literal": "哈马斯发表声明，再次呼吁“同意并遵守路线图”。哈马斯主张以色列军队撤出加沙是解除武装的条件。双方立场仍处于平行线状态，和平计划恐怕将持续停滞。和平评议会7月31日公布了完成和平计划的路线图。",
                "grammar": "「〜と改めて訴えた」— 再次呼吁…。例：順守すると訴えた（呼吁将遵守）。\n「〜と主張している」— 主张…。例：条件と主張している（主张是条件）。\n「〜そうだ」— 看起来要…。例：停滞状態が続きそうだ（停滞状态恐怕会持续）。",
                "vocab": [["声明", "せいめい", "声明"], ["順守", "じゅんしゅ", "遵守"], ["訴える", "うったえる", "呼吁、诉求"], ["主張", "しゅちょう", "主张"], ["平行線", "へいこうせん", "平行线（无交集）"], ["停滞", "ていたい", "停滞"]]
            },
        ]
    },
    {
        "slug": "aeon-kumamoto-hinan",
        "title": "イオンモール爆発事故「避難後は戻らない」マニュアル機能せず 現場で混乱",
        "subtitle": "from 日テレNEWS NNN",
        "paras": [
            {
                "ja": "イオンモールの爆発事故で、避難後に従業員らが館内に戻らざるを得なかった様々な事情が取材で明らかになりました。イオン側は「マニュアルの周知を含む運用が徹底できていなかった可能性がある」と取材に答えています。従業員7人が犠牲となったイオンモール熊本の爆発事故。イオンのマニュアルには、「一旦避難した者は館内に入らない」と記載されているといいますが、実際はどうだったのでしょうか。当時、館内にいた客や従業員に取材すると、自らの判断で店内に戻った人や、イオンモール側のスタッフと思われる人が許可を出していたという証言など、マニュアル通りにはいかなかった実態が見えてきました。",
                "en": "In the Aeon Mall explosion accident, interviews have revealed various circumstances that forced employees and others to return inside the building after evacuating. Aeon responded to interviews saying, \"There is a possibility that operations, including dissemination of the manual, were not thoroughly implemented.\" In the explosion accident at Aeon Mall Kumamoto, in which seven employees died, Aeon's manual reportedly states that \"those who have once evacuated must not re-enter the building,\" but what actually happened? Interviews with customers and employees who were inside at the time revealed the reality that things did not go according to the manual — people who returned to the store on their own judgment, and testimony that someone believed to be Aeon Mall staff gave permission.",
                "literal": "在永旺购物中心爆炸事故中，采访显示避难后员工们不得不返回馆内的各种情况。永旺方面在采访中回答称“包括手册周知在内的运用可能未能彻底执行”。造成7名员工遇难的永旺购物中心熊本爆炸事故。永旺的手册上写着“一旦避难者不得进入馆内”，但实际如何呢？采访当时在馆内的顾客和员工后发现，有人自行判断返回店内，也有人证言称疑似永旺购物中心方面的员工许可了进入，与手册不符的实际情况逐渐浮现。",
                "grammar": "「〜ざるを得なかった」— 不得不…。例：戻らざるを得なかった（不得不返回）。\n「〜といいますが」— 据说…，但…。例：記載されているといいますが（据说写着…，但）。\n「〜通りにはいかなかった」— 没有按照…进行。例：マニュアル通りにはいかなかった（没有按手册进行）。",
                "vocab": [["爆発", "ばくはつ", "爆炸"], ["避難", "ひなん", "避难"], ["従業員", "じゅうぎょういん", "员工"], ["マニュアル", "まにゅある", "手册"], ["周知", "しゅうち", "周知、广泛告知"], ["証言", "しょうげん", "证言"]]
            },
            {
                "ja": "イオンモールに入る専門店の従業員によると、地震発生からおよそ45分後、イオン側から「地震の影響につき以降の営業を中止いたします。従業員さまはお帰りいただいて結構でございます」という帰宅を促すメッセージが送られてきました。しかし、受け取った人の中には館内に戻った人もいたといいます。店舗従業員（30代）「メッセージを見てそのまま帰る人もいれば、実際に中に戻った方も数人、結構な数いた。10数名、入っていった」この男性も自分の判断で館内に戻ったといいます。",
                "en": "According to an employee of a specialty store inside Aeon Mall, about 45 minutes after the earthquake occurred, Aeon sent a message urging people to go home: \"Due to the effects of the earthquake, we will suspend operations from now on. Employees, you are welcome to leave.\" However, some of those who received it reportedly returned inside the building. A store employee (in his 30s): \"Some people went home after seeing the message, but quite a few — over a dozen — actually went back inside.\" This man also returned inside on his own judgment.",
                "literal": "据进入永旺购物中心的专卖店员工称，地震发生约45分钟后，永旺方面发来了催促回家的消息：“受地震影响，此后停止营业。员工可以回去了。”但是，收到消息的人中也有返回馆内的。店铺员工（30多岁）说：“看到消息直接回家的人有，实际返回店内的人也有好几个，数量相当多，有十几个人进去了。”这位男性也表示是自己判断返回馆内的。",
                "grammar": "「〜につき」— 由于…（书面语）。例：地震の影響につき（由于地震影响）。\n「〜いただいて結構でございます」— 可以…（敬语）。例：お帰りいただいて結構でございます（您可以回去了）。\n「〜もいれば、〜もいた」— 既有…也有…。例：帰る人もいれば、戻った方もいた（既有回家的也有返回的）。",
                "vocab": [["専門店", "せんもんてん", "专卖店"], ["営業", "えいぎょう", "营业"], ["促す", "うながす", "催促、促进"], ["メッセージ", "めっせーじ", "消息"], ["数人", "すうにん", "数人"], ["判断", "はんだん", "判断"]]
            },
            {
                "ja": "――戻らなければいけない理由はあったのですか。館内に戻った店舗従業員（30代）「私の車のカギを（取りに）。歩いて帰る選択肢はそもそもない」イオンモール熊本の近くには駅がなく、男性は車で40分近くかけて通勤していました。自宅に帰るためには、店に戻り車のカギを取りに行く必要があったのです。館内に戻った店舗従業員（30代）「事務所の中も結構、水浸しになっていて、コンセントとか扇風機をつけたりしてたので、感電するんじゃないかっていう怖さがありました。電源全部切って、抜けるコンセント(プラグ)は抜いて」男性は店の安全確認を行い、10分程で外へ出たといいます。",
                "en": "— Was there a reason you had to go back? Store employee (in his 30s) who returned inside: \"To get my car keys. Walking home wasn't an option in the first place.\" There is no station near Aeon Mall Kumamoto, and the man commuted by car, taking nearly 40 minutes. To get home, he had to go back to the store and retrieve his car keys. The store employee who returned inside (in his 30s): \"The office was quite flooded, and outlets and fans were left on, so I was afraid of electric shock. I turned off all the power and unplugged the plugs I could.\" The man checked the store's safety and went outside about 10 minutes later.",
                "literal": "――当时有必须返回的理由吗？返回馆内的店铺员工（30多岁）：“去拿我的车钥匙。步行回家这个选项从一开始就不存在。”永旺购物中心熊本附近没有车站，这名男性开车通勤，单程近40分钟。为了回家，必须回到店里取车钥匙。返回馆内的店铺员工（30多岁）：“办公室里也淹了不少水，插座和电风扇还开着，所以有会不会触电的恐惧。我把电源全部关掉，能拔的插头都拔了。”据说这名男性确认了店内安全后，约10分钟就出来了。",
                "grammar": "「〜なければいけない」— 必须…。例：戻らなければいけない（必须返回）。\n「〜そもそもない」— 根本不存在…。例：選択肢はそもそもない（选项根本不存在）。\n「〜じゃないかっていう」— 会不会…的那种（口语）。例：感電するんじゃないかっていう怖さ（会不会触电的那种恐惧）。",
                "vocab": [["カギ", "かぎ", "钥匙"], ["選択肢", "せんたくし", "选项、选择"], ["通勤", "つうきん", "通勤"], ["水浸し", "みずびたし", "泡水、水淹"], ["感電", "かんでん", "触电"], ["安全確認", "あんぜんかくにん", "安全确认"]]
            },
        ]
    },
    {
        "slug": "matahachi-intai",
        "title": "又吉克樹投手が今季限りで現役引退 NPB通算503登板",
        "subtitle": "from THE ANSWER",
        "paras": [
            {
                "ja": "プロ野球の中日とソフトバンクでプレーした又吉克樹投手が10日、今季限りでの現役引退を発表した。今季はメキシコでのプレーを目指し春季キャンプに参加したものの契約に至らず、その後は2軍ファーム・リーグに参加するオイシックスに入団していた。",
                "en": "Pitcher Matayachi Katsuki, who played for the Chunichi Dragons and SoftBank Hawks in professional baseball, announced on the 10th that he will retire at the end of this season. This season he aimed to play in Mexico and participated in spring camp, but no contract materialized, and he subsequently joined Oisix, a team in the second-division farm league.",
                "literal": "曾在职业棒球中日和软银效力的又吉克树投手10日宣布本赛季结束后退役。本赛季他曾以在墨西哥打球为目标参加春季集训，但未能签约，之后加入了参加二军农场联赛的Oisix队。",
                "grammar": "「〜限りでの引退」— 到…为止的退役。例：今季限りでの現役引退（本赛季结束后退役）。\n「〜ものの」— 虽然…但是…。例：参加したものの契約に至らず（虽然参加了但未签约）。\n「〜に至らず」— 未能达到…。例：契約に至らず（未能签约）。",
                "vocab": [["プロ野球", "ぷろやきゅう", "职业棒球"], ["現役引退", "げんえきいんたい", "现役退役"], ["春季キャンプ", "しゅんききゃんぷ", "春季集训"], ["契約", "けいやく", "签约、合同"], ["入団", "にゅうだん", "入队"], ["ファーム・リーグ", "ふぁーむ・りーぐ", "二军农场联赛"]]
            },
            {
                "ja": "35歳の又吉は沖縄・西原高から岡山の環太平洋大へ進み、卒業後は四国アイランドリーグの香川に入団。ここで頭角を現し、2013年秋のドラフトで中日の2位指名を受けて入団した。サイドハンドからの速球とクセ球を武器に主にリリーフとして活躍。2021年のオフには独立リーグ出身者として初めてFA権を行使し、ソフトバンクに移籍した。",
                "en": "Matayachi, 35, went from Okinawa's Nishihara High School to Okayama's International Pacific University, and after graduation joined Kagawa of the Shikoku Island League. There he distinguished himself, and in the autumn 2013 draft he was selected by Chunichi in the second round and joined the team. Armed with a sidearm fastball and tricky pitches, he mainly flourished as a reliever. In the 2021 offseason, he became the first independent-league alumnus to exercise free agency rights, transferring to SoftBank.",
                "literal": "35岁的又吉从冲绳西原高中升入冈山的环太平洋大学，毕业后加入四国岛联盟的香川队。在那里崭露头角，2013年秋的选秀中被中日第2轮指名入队。以侧投的快速球和怪癖球为武器，主要作为救援投手活跃。2021年休赛期，他作为独立联盟出身者首次行使FA权，转会到软银。",
                "grammar": "「〜へ進み」— 升入…。例：環太平洋大へ進み（升入环太平洋大学）。\n「〜を武器に」— 以…为武器。例：速球とクセ球を武器に（以快速球和怪癖球为武器）。\n「〜として初めて」— 作为…第一次。例：独立リーグ出身者として初めて（作为独立联盟出身者首次）。",
                "vocab": [["頭角を現す", "とうかくをあらわす", "崭露头角"], ["ドラフト", "どらふと", "选秀"], ["指名", "しめい", "指名选中"], ["サイドハンド", "さいどはんど", "侧投"], ["リリーフ", "りりーふ", "救援投手"], ["移籍", "いせき", "转会"]]
            },
            {
                "ja": "4年契約を結んだソフトバンクでもリリーフとして投げたものの、2025年は1軍登板がなくオフに戦力外通告を受けた。NPB1軍通算503試合に登板し47勝32敗11セーブ、173ホールド、防御率2.84の成績を残した。2017年のアジアプロ野球チャンピオンシップでは日本代表にも選ばれている。",
                "en": "He also pitched as a reliever for SoftBank under a four-year contract, but in 2025 he had no appearances in the first team and received notice that his services were no longer needed in the offseason. He appeared in 503 career NPB first-team games, posting a record of 47 wins, 32 losses, 11 saves, 173 holds, and a 2.84 ERA. He was also selected for the Japanese national team at the 2017 Asia Professional Baseball Championship.",
                "literal": "在签订4年合同的软银他也作为救援投手出场，但2025年没有一军登场记录，休赛期收到战力外通告。NPB一军累计出场503场，留下47胜32败11救援、173次中继成功、防御率2.84的成绩。2017年的亚洲职业棒球冠军赛上他还入选了日本代表队。",
                "grammar": "「〜ものの」— 虽然…但是…。例：投げたものの（虽然投了但）。\n「〜を受けた」— 收到…。例：戦力外通告を受けた（收到战力外通告）。\n「〜の成績を残した」— 留下…的成绩。例：防御率2.84の成績を残した（留下防御率2.84的成绩）。",
                "vocab": [["登板", "とうばん", "上场投球"], ["戦力外通告", "せんりょくがいつうこく", "战力外通知（解约通知）"], ["通算", "つうさん", "累计"], ["セーブ", "せーぶ", "救援成功"], ["ホールド", "ほーるど", "中继成功"], ["防御率", "ぼうぎょりつ", "防御率"]]
            },
            {
                "ja": "ソフトバンク退団後はオフの12球団合同トライアウトに参加し、その後はメキシカンリーグのユカタン・ライオンズの春季キャンプに参加。チーム方針で開幕前にリリースされると、4月にはオイシックスに加わっていた。今季ファーム・リーグでは29試合に投げ2勝2敗、防御率4.05。",
                "en": "After leaving SoftBank, he took part in the offseason 12-team joint tryout, then joined the spring camp of the Yucatan Lions of the Mexican League. Released before the season opened due to team policy, he joined Oisix in April. This season in the farm league he pitched in 29 games with 2 wins and 2 losses and a 4.05 ERA.",
                "literal": "离开软银后，他参加了休赛期12支球队的联合试训，之后参加了墨西哥联赛尤卡坦雄狮队的春季集训。因球队方针在开幕前被解约，4月加入了Oisix。本赛季农场联赛出场29场，2胜2败，防御率4.05。",
                "grammar": "「〜に参加し」— 参加…。例：トライアウトに参加し（参加试训）。\n「〜に加わっていた」— 加入了…。例：オイシックスに加わっていた（加入了Oisix）。\n「〜に投げ」— 出场投了…。例：29試合に投げ（出场29场投球）。",
                "vocab": [["トライアウト", "とらいあうと", "试训、选拔"], ["メキシカンリーグ", "めきしかんりーぐ", "墨西哥联赛"], ["リリース", "りりーす", "解约、释放"], ["試合", "しあい", "比赛"], ["勝利", "しょうり", "胜利"], ["敗戦", "はいせん", "败战"]]
            },
        ]
    },
    {
        "slug": "yuzu-kumamoto-sien",
        "title": "ゆず「幾重」ライブ音源を緊急配信 収益全額を熊本地震の復興支援に",
        "subtitle": "from スポーツ報知",
        "paras": [
            {
                "ja": "人気デュオのゆずが、１４日に「幾重（ライブバージョン）」を緊急配信リリースすることが９日、決まった。この配信で得た収益は、令和８年熊本地震の被災地への復興支援として全額寄付される。",
                "en": "Popular duo Yuzu decided on the 9th to urgently release \"Ikue (Live Version)\" on the 14th. All proceeds from this release will be donated to support reconstruction in areas affected by the Reiwa 8 Kumamoto Earthquake.",
                "literal": "人气双人组合柚子于9日决定14日紧急发布《几重（现场版）》。这次发布所得收益将作为对令和8年熊本地震灾区重建的支援全额捐出。",
                "grammar": "「〜ことが決まった」— 决定…。例：緊急配信リリースすることが決まった（决定紧急发布）。\n「〜として」— 作为…。例：復興支援として（作为重建支援）。\n「〜される」— 被…（被动）。例：全額寄付される（全额捐出）。",
                "vocab": [["デュオ", "でゅお", "双人组合"], ["緊急", "きんきゅう", "紧急"], ["配信", "はいしん", "发布、推送"], ["収益", "しゅうえき", "收益"], ["寄付", "きふ", "捐款"], ["復興支援", "ふっこうしえん", "重建支援"]]
            },
            {
                "ja": "「幾重」は、ＮＨＫ東日本大震災１５年の震災伝承ソングとして書き下ろした曲。震災から１５年の日々と想（おも）い、それぞれの歩みで未来を切り開いていく姿を優しく慈しむようにつづったもので、３月１１日発売の最新アルバム「心音」に収録された。今回のライブバージョンは、７月の全国弾き語りツアー神奈川公演（横浜アリーナ）でのパフォーマンスを音源化したもの。北川悠仁、岩沢厚治がアコースティックギターによる弾き語りで歌声を届けた。",
                "en": "\"Ikue\" is a song written as NHK's disaster-remembrance song marking 15 years since the Great East Japan Earthquake. It gently cherishes the 15 years since the disaster, the feelings, and the figures of people carving out the future with their own steps, and was included in the latest album \"Shin'on,\" released on March 11. The live version released this time is a recording of the performance at the Kanagawa show (Yokohama Arena) of the July nationwide acoustic tour. Kitagawa Yujin and Iwasawa Koji delivered their singing voice through acoustic guitar accompaniment.",
                "literal": "《几重》是为NHK东日本大地震15周年而创作的震灾传承歌曲。它以温柔珍视的方式抒写了震灾后15年的岁月与思念、以及人们各自迈步开拓未来的身姿，收录于3月11日发售的最新专辑《心音》。这次的现场版是把7月全国弹唱巡演神奈川公演（横滨体育馆）的表演音源化的作品。北川悠仁、岩泽厚治用原声吉他弹唱献上了歌声。",
                "grammar": "「〜として書き下ろした」— 为…而新创作的。例：震災伝承ソングとして書き下ろした（作为震灾传承歌曲新创作的）。\n「〜ようにつづった」— 以…方式抒写。例：慈しむようにつづった（以珍视之情抒写）。\n「〜による弾き語り」— 用…弹唱。例：アコースティックギターによる弾き語り（用原声吉他弹唱）。",
                "vocab": [["震災伝承", "しんさいでんしょう", "震灾传承"], ["書き下ろす", "かきおろす", "新创作"], ["慈しむ", "いつくしむ", "珍爱、怜爱"], ["収録", "しゅうろく", "收录"], ["弾き語り", "ひきがたり", "弹唱"], ["パフォーマンス", "ぱふぉーまんす", "表演"]]
            },
            {
                "ja": "２人は「今、ゆずにできることは何か―。原点である『歌』を通じて支援の輪を広げ、届けていきたいと思いました」と説明。「僕たちの音楽が皆様の心に寄り添い、明日の希望となることを心から願っています」とコメントした。ゆずとしても別の形で義援金の寄付を行う予定という。これまで東日本大震災を始め、様々なシーンで復興支援を行ってきた。２０１６年の熊本地震の際には、その年の１２月に熊本城前でフリーライブ「冬至の日ライブ」を実施。１８年の西日本豪雨の際には、「うたエール」の弾き語りバージョンを配信し、その収益を全額、義援金として寄付している。",
                "en": "The two explained, \"We thought, what can Yuzu do now? — We wanted to expand and deliver the circle of support through 'song,' which is our origin.\" They commented, \"We sincerely hope our music will stay close to everyone's hearts and become hope for tomorrow.\" The duo also plans to make donations of relief money in other forms. They have supported reconstruction in various scenes, starting with the Great East Japan Earthquake. During the 2016 Kumamoto Earthquake, they held a free live \"Winter Solstice Live\" in front of Kumamoto Castle in December of that year. During the 2018 western Japan heavy rain, they released the acoustic version of \"Uta Yell,\" donating all proceeds as relief money.",
                "literal": "两人说明道：“现在柚子能做什么呢——。我们想通过作为原点的‘歌’扩大并传递支援的圈子。”并评论说：“衷心希望我们的音乐能贴近大家的心，成为明天的希望。”据说柚子还计划以其他形式进行赈灾捐款。迄今为止，以东北大地震为首，他们在各种场合开展了重建支援。2016年熊本地震时，他们于当年12月在熊本城前举办了免费演唱会“冬至日演唱会”。2018年西日本暴雨时，发布了《歌援》的弹唱版，将全部收益作为赈灾款捐出。",
                "grammar": "「〜を通じて」— 通过…。例：『歌』を通じて（通过“歌”）。\n「〜ことを願っています」— 祝愿…。例：希望となることを願っています（祝愿成为希望）。\n「〜を始め」— 以…为首。例：東日本大震災を始め（以东北大地震为首）。",
                "vocab": [["原点", "げんてん", "原点"], ["支援の輪", "しえんのわ", "支援的圈子"], ["義援金", "ぎえんきん", "赈灾捐款"], ["フリーライブ", "ふりーらいぶ", "免费演唱会"], ["実施", "じっし", "实施"], ["豪雨", "ごうう", "暴雨"]]
            },
            {
                "ja": "コメント全文では「はじめに、この度発生した令和８年熊本地震により被災された皆様に心よりお見舞い申し上げますとともに、お亡くなりになられた方々のご冥福を心よりお祈り申し上げます。余震や厳しい暑さが続く中、ご不安な日々を過ごされていることと思います。２０１６年１２月。僕たちは熊本城前の二の丸広場でフリーライブを開催しました。あの日、熊本や九州の皆様と歌い、同じ時間を過ごしたことは、今も僕たちの心に深く残っています」としている。",
                "en": "In the full comment, they stated: \"First, we offer our heartfelt sympathies to all those affected by the Reiwa 8 Kumamoto Earthquake, and sincerely pray for the souls of those who have passed away. With aftershocks and severe heat continuing, we imagine you are spending anxious days. December 2016. We held a free live at Ninomaru Plaza in front of Kumamoto Castle. Singing with the people of Kumamoto and Kyushu and sharing that time that day still remains deep in our hearts.\"",
                "literal": "在评论全文中他们写道：“首先，谨向因本次令和8年熊本地震受灾的各位致以诚挚慰问，并向遇难者表示衷心哀悼。在余震和酷暑持续之中，想必大家正度过不安的日子。2016年12月。我们在熊本城前的二之丸广场举办了免费演唱会。那一天与熊本和九州的大家一同歌唱、共度时光，至今仍深深留在我们心中。”",
                "grammar": "「〜お見舞い申し上げます」— 谨致慰问（敬语）。例：心よりお見舞い申し上げます（致以衷心慰问）。\n「〜とともに」— 同时…。例：お見舞い申し上げますとともに（致以慰问的同时）。\n「〜ことと思います」— 想必…。例：過ごされていることと思います（想必正在度过）。",
                "vocab": [["被災", "ひさい", "受灾"], ["お見舞い", "おみまい", "慰问"], ["ご冥福", "ごめいふく", "冥福祈愿"], ["余震", "よしん", "余震"], ["開催", "かいさい", "举办"], ["深く残る", "ふかくのこる", "深深留存"]]
            },
        ]
    },
    {
        "slug": "nashi-tounan-saigai",
        "title": "梨5000個を盗まれた農家の男性、熊本の被災地支援へ 「助け合いの輪」に密着",
        "subtitle": "from ABEMA TIMES",
        "paras": [
            {
                "ja": "困っている人がいるなら力になりたい。たとえ自分も困っていたとしても──。気温40度近い酷暑を顧みず汗だくで助ける人たちがいた。震度7の揺れに見舞われ、8月に入っても余震が続く宇城市では、およそ3000人が避難し、断水は8450戸（8日時点）。不便な生活を余儀なくされている。8月3日、宇城市内の焼肉店の駐車場を利用してラーメンの炊き出しが行われていた。福岡県朝倉市のラーメン店、福鶏が朝一番でキッチンカーで駆けつけ、絶品の冷やし鶏スープラーメンを提供。少しでも空腹を満たしてほしいと、炊き出し用に特別スープを用意した。",
                "en": "If someone is in trouble, they want to lend a hand — even if they themselves are struggling. There were people helping out in a sweat, heedless of the scorching heat of nearly 40 degrees. In Uki City, struck by shaking of intensity 7 with aftershocks continuing even into August, about 3,000 people have evacuated and 8,450 households are without water (as of the 8th), forced into an inconvenient life. On August 3, ramen was being served in a parking lot of a yakiniku restaurant in Uki City. Fukukei, a ramen shop in Asakura City, Fukuoka, rushed over first thing in the morning with a kitchen car, offering exquisite chilled chicken soup ramen. They prepared a special soup for the relief cooking so that people could fill their empty stomachs even a little.",
                "literal": "只要有人遇到困难就想伸出援手——即使自己也身处困境。有这样不顾近40度酷暑、大汗淋漓地帮助他人的人们。在遭遇震度7摇晃、进入8月后余震仍在持续的宇城市，约3000人避难，8450户断水（截至8日）。人们被迫过着不便的生活。8月3日，宇城市内一家烤肉店的停车场举行了拉面的赈济供餐。福冈县朝仓市的拉面店福鸡一大清早开着餐车赶到，提供绝品冷鸡汤拉面。为了让人们哪怕稍微填饱肚子，他们准备了供餐专用的特别汤底。",
                "grammar": "「〜なら」— 如果是…的话。例：困っている人がいるなら（如果有人遇到困难）。\n「〜たとえ〜としても」— 即使…也…。例：たとえ自分も困っていたとしても（即使自己也身处困境）。\n「〜を顧みず」— 不顾…。例：酷暑を顧みず（不顾酷暑）。",
                "vocab": [["酷暑", "こくしょ", "酷暑"], ["顧みる", "かえりみる", "顾及、回顾"], ["震度", "しんど", "震度"], ["避難", "ひなん", "避难"], ["断水", "だんすい", "断水"], ["炊き出し", "たきだし", "赈济供餐"]]
            },
            {
                "ja": "子どもたちにラーメンを食べさせていた被災者に話を聞くと、「10年前（の地震の時）は私、子どもがいなかったので全然違いますね。重みというか大変さが。自分は別に食べなくても寝るところはどこでも。寝るところも確保しないといけないし、トイレもそうだけど。やっぱり食べ物かな。着替えも結局汗をかくから、大人は我慢できても、子どもはかゆいと言い始めました」と話した。",
                "en": "When asked, an evacuee who was feeding ramen to children said, \"Ten years ago (during the earthquake), I didn't have children, so it's completely different — the weight of it, or rather the hardship. For myself, I don't have to eat, and I can sleep anywhere. I have to secure a place to sleep, and the toilet too, but in the end it's food. And clothes — in the end you sweat, so adults can endure, but the children started saying they itch.\"",
                "literal": "向正在给孩子们喂拉面的受灾者询问时，对方说：“10年前（地震时）我没有孩子，所以完全不同呢——那种分量，或者说艰难程度。我自己不吃也没关系，睡觉哪里都行。睡觉的地方也必须确保，厕所也是。但果然还是食物吧。换洗衣服也是，因为终究会出汗，大人能忍，但孩子们开始说痒了。”",
                "grammar": "「〜に話を聞くと」— 向…询问时。例：被災者に話を聞くと（向受灾者询问时）。\n「〜というか」— 与其说是…不如说。例：重みというか大変さが（那种分量，或者说艰难）。\n「〜ないといけない」— 必须…。例：確保しないといけない（必须确保）。",
                "vocab": [["被災者", "ひさいしゃ", "受灾者"], ["重み", "おもみ", "分量、重量感"], ["確保", "かくほ", "确保"], ["着替え", "きがえ", "换洗衣物"], ["我慢", "がまん", "忍耐"], ["かゆい", "かゆい", "痒"]]
            },
            {
                "ja": "支援活動を行う石原千聖さんは宇城市内の自宅アパートで被災した。自宅トイレのタンクが壊れ、水も使えず現在は車中泊を送っているという。「今日は支援の方の熱気でいい意味で温かいです。うちはアパートなんですけれども、足の踏み場がない。トイレのタンクのふたが飛んで水が溜まらない状態。冷蔵庫が倒れたことで、買い出ししたばかりだったので、生卵、ヨーグルト、キムチ、そういうのが1日2日くらい入れられていなかったので床にウワァーってなっちゃって…」。そんな状態にもかかわらず被災者支援に汗を流すのは、ある人の行動を知ったからだという。「梨の盗難にあった佐々木さんということを聞いて。何で自分たちが今すごくきつい思いをされているのに。こんな私たちがきつい時に来てくれていると思ったら動かないわけにはいかなくて。その気持ちが嬉しいから、私たちも大変だけど、みんな大変、でも大変な人が県外から来てくださって、全国からの物資がこんなにあったらもう嬉しくてやるしかないなと。私たちがやらないといつまで経っても熊本は立ち上がれない。頑張らないといけない」。",
                "en": "Ishihara Chisato, who carries out support activities, was affected at her apartment in Uki City. The tank of her home toilet broke, and without usable water she is currently living in her car. \"Today is warm, in a good sense, from the passion of the support people. Ours is an apartment, but there's no place to step. The toilet tank lid flew off and water won't collect. The refrigerator fell over — I had just gone shopping, so raw eggs, yogurt, kimchi, things like that hadn't been kept cool for a day or two, and it all went splat on the floor...\" Despite such a situation, she works up a sweat helping victims because she learned of one person's actions. \"I heard about Mr. Sasaki, whose pears were stolen. Why would he come to help while we're going through something so hard right now? When I thought that someone is coming to help us at a time like this, I couldn't just stand by. That feeling makes me happy — we're struggling too, everyone is struggling, but someone in trouble came from outside the prefecture, and with this much aid from all over the country, I felt I had no choice but to do it too. If we don't act, Kumamoto will never stand up again no matter how long we wait. We have to do our best.\"",
                "literal": "进行支援活动的石原千圣在宇城市内的自家公寓受灾。家中厕所水箱坏了，无法用水，目前过着车中过夜的生活。“今天因支援者们的热情，在好的意义上很温暖。我家是公寓，但连下脚的地方都没有。马桶水箱盖飞了，水存不住。冰箱倒了——因为刚采购过，生鸡蛋、酸奶、泡菜那些东西一两天没放进去，就这样哗啦一声全洒在地板上了……”。尽管身处这种状况，她仍挥汗支援受灾者，据说是因为得知了一个人的行动。“听说了梨被盗的佐佐木先生的事。为什么我们自己正这么艰难的时候，他会来帮我们呢。想到在我们这么艰难的时候有人来帮助我们，就不能袖手旁观。那份心意让人高兴，所以我们也很艰难，大家都很艰难，但艰难的人从县外赶来，全国的物资有这么多，那我也只能高兴地去做。如果我们不做，熊本无论等到什么时候都站不起来。必须努力。”",
                "grammar": "「〜にもかかわらず」— 尽管…。例：そんな状態にもかかわらず（尽管是那种状态）。\n「〜わけにはいかなくて」— 不能…。例：動かないわけにはいかなくて（不能袖手旁观）。\n「〜ないといつまで経っても〜ない」— 不…就永远不…。例：やらないといつまで経っても立ち上がれない（不做就永远站不起来）。",
                "vocab": [["車中泊", "しゃちゅうはく", "车中过夜"], ["足の踏み場", "あしのふみば", "下脚之处"], ["買い出し", "かいだし", "采购"], ["物資", "ぶっし", "物资"], ["きつい", "きつい", "艰难、辛苦"], ["立ち上がる", "たちあがる", "站起来、振作"]]
            },
            {
                "ja": "石原さんが言う「梨農家の男性」とは佐々木浩喜さん（54）だ。福岡県うきは市から駆けつけた佐々木さんは自宅を朝5時に出発し、ありったけの支援物資5トンをトラックに乗せて被災者に届けていた。「少しでも恩返しできれば。僕も助けてもらえたので。広がったらいいと思います」。佐々木さんは7月、自身の梨農園で何者かによって梨5000個、200万円相当を盗まれる被害にあっていた。「またかって感じかな、今回は。俺何かしたかなと思いますよね。恨まれているのかなと思いますよね。同じところだけをとられて」。梨の窃盗被害は去年に続き2年連続。その梨農園は市街地から離れた山林の中にある。被害に気づいたのは7月17日、カラスよけの模型を確認するため奥まで入った時、梨が忽然と消えていた。",
                "en": "The \"pear farmer\" Ishihara mentioned is Sasaki Koki (54). Sasaki, who rushed from Ukiha City, Fukuoka, left home at 5 a.m., loading 5 tons of as much relief supplies as he could gather onto a truck and delivering them to the victims. \"If I can repay even a little. I was helped too, so I hope this spreads.\" In July, Sasaki suffered damage when someone stole 5,000 pears worth about 2 million yen from his pear orchard. \"I felt like 'here we go again' this time. I wonder if I did something, you know. I wonder if someone bears a grudge. Only the same spot was taken.\" The pear theft damage continued for the second year in a row. The orchard is in a mountain forest away from the city. He noticed the damage on July 17, when he went deep into the orchard to check the crow-scaring decoys — the pears had vanished all at once.",
                "literal": "石原所说的“梨农男性”是佐佐木浩喜（54岁）。从福冈县浮羽市赶来的佐佐木清晨5点从家出发，把倾其所有的5吨支援物资装上卡车送到受灾者手中。“哪怕能回报一点点也好。因为我也曾受过帮助。希望这份心意能扩散开来”。佐佐木7月在自己的梨园遭到不明人士盗走约200万日元等值的5000个梨。“这次的感觉是‘又来了啊’。我会想是不是自己做了什么。是不是被谁怨恨了。只有同一处被偷了”。梨被盗已是继去年之后连续第2年。那座梨园位于远离市区的山林之中。发现受害是在7月17日，为了确认防乌鸦模型走进果园深处时，梨已经忽然消失了。",
                "grammar": "「〜に駆けつけた」— 赶到…的。例：福岡県から駆けつけた（从福冈赶来的）。\n「〜恩返しできれば」— 若能报恩的话。例：少しでも恩返しできれば（哪怕能回报一点）。\n「〜続き2年連続」— 继…之后连续2年。例：去年に続き2年連続（继去年之后连续第2年）。",
                "vocab": [["駆けつける", "かけつける", "赶到"], ["ありったけ", "ありったけ", "倾其所有"], ["恩返し", "おんがえし", "报恩"], ["相当", "そうとう", "相当于、等值"], ["恨む", "うらむ", "怨恨"], ["忽然", "こつぜん", "忽然、突然"]]
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
