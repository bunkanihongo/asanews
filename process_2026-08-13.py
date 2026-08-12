#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-10 (Mon) Edition"""
import json, os, subprocess, re, time
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-13'
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
        "slug": "tenki-rakurai-keihou",
        "title": "今日13日も所々で雷雲が発達 東北から近畿を中心に急な激しい雨や落雷に注意",
        "subtitle": "from tenki.jp",
        "paras": [
            {
                "ja": "今日13日も雨雲や雷雲の湧きやすい状況が続きます。東北や関東、東海、近畿を中心に、急に降る激しい雨や、落雷、突風に注意が必要です。昨夜から今日13日の未明にかけて、本州のあちらこちらで雨雲が発達。静岡県御前崎市で1時間33.5ミリの激しい雨を観測するなど、特に東海で雨脚が強まりました。",
                "en": "Today, the 13th, conditions remain favorable for rain clouds and thunderclouds to form. Around Tohoku, Kanto, Tokai, and Kinki in particular, caution is needed against sudden heavy rain, lightning, and gusts. From last night into the early hours of today, rain clouds developed across Honshu. Rain intensified especially in Tokai, where 33.5 mm of heavy rain fell in one hour in Omaezaki City, Shizuoka Prefecture.",
                "literal": "今天13日也持续着容易涌起雨云和雷云的情况。以东北、关东、东海、近畿为中心，需要注意骤降的强降雨、落雷和阵风。从昨夜到今日13日凌晨，本州各地雨云发展。静冈县御前崎市观测到1小时33.5毫米的强降雨等，特别是东海降雨势头增强。",
                "grammar": "「〜やすい」— 容易…。例：雷雲の湧きやすい状況（容易涌起雷云的情况）。\n「〜を中心に」— 以…为中心。例：東北や関東を中心に（以东北和关东为中心）。\n「〜にかけて」— 从…到…（时间/范围）。例：昨夜から未明にかけて（从昨夜到凌晨）。",
                "vocab": [["雷雲", "らいうん", "雷雨云"], ["湧く", "わく", "涌起、冒出"], ["落雷", "らくらい", "落雷"], ["突風", "とっぷう", "阵风、狂风"], ["未明", "みめい", "凌晨、拂晓"], ["雨脚", "あまあし", "雨势"]]
            },
            {
                "ja": "今日13日は、台風15号から変わった熱帯低気圧が山陰沖を西よりに進み、この熱帯低気圧に向かうように湿った空気が流れ込むでしょう。また、日本の東には高気圧があり、この縁をまわる湿った空気も本州付近に流れ込みます。さらに、本州の上空には寒気が居座り、広い範囲で大気の不安定な状態が続くでしょう。",
                "en": "Today, a tropical depression that formed from Typhoon No. 15 will move westward off the San'in coast, and moist air will flow toward this depression. Also, there is a high-pressure system east of Japan, and moist air circulating around its edge will also flow into the vicinity of Honshu. Furthermore, cold air remains aloft over Honshu, so unstable atmospheric conditions will continue over a wide area.",
                "literal": "今天13日，由台风15号转变而来的热带低气压将在山阴近海向西推进，潮湿空气将向这个热带低气压流入。另外，日本以东有高气压，绕其边缘的潮湿空气也将流入本州附近。而且，本州上空寒气流连不去，大范围的大气不稳定状态将持续。",
                "grammar": "「〜から変わった」— 由…转变来的。例：台風15号から変わった熱帯低気圧（由台风15号转变来的热带低气压）。\n「〜ように」— 像…那样/为了…。例：向かうように流れ込む（朝着…那样流入）。\n「〜居座り」— 滞留不走。例：寒気が居座り（寒气流连不去）。",
                "vocab": [["熱帯低気圧", "ねったいていきあつ", "热带低气压"], ["山陰", "さんいん", "山阴地区（日本海侧）"], ["湿った", "しめった", "潮湿的"], ["高気圧", "こうきあつ", "高气压"], ["寒気", "かんき", "寒气、冷空气"], ["不安定", "ふあんてい", "不稳定"]]
            },
            {
                "ja": "急な強雨や雷雨の前兆となる現象は3つ。「真っ黒い雲が近づく」「急に冷たい風が吹く」「ゴロゴロと雷の音が聞こえる」です。このような変化を感じたら、まもなく激しい雨が降ったり、雷が鳴ったりする恐れがありますので、すぐに安全な所へ避難してください。",
                "en": "There are three phenomena that signal sudden heavy rain or thunderstorms: \"a jet-black cloud approaches,\" \"a cold wind suddenly blows,\" and \"you hear thunder rumbling.\" If you notice such changes, heavy rain may soon fall or thunder may strike, so evacuate to a safe place immediately.",
                "literal": "骤降强降雨或雷雨的前兆现象有3个。“漆黑的云靠近”“突然吹来冷风”“听到轰隆隆的雷声”。如果感觉到这样的变化，不久就可能下暴雨或打雷，请立即避难到安全的地方。",
                "grammar": "「〜前兆となる」— 成为…的前兆。例：強雨の前兆となる現象（成为强降雨前兆的现象）。\n「〜たり〜たりする」— 又…又…。例：雨が降ったり、雷が鳴ったり（下雨或打雷）。\n「〜恐れがあります」— 有…的危险/可能。例：雷が鳴ったりする恐れがあります（有可能打雷）。",
                "vocab": [["前兆", "ぜんちょう", "前兆、预兆"], ["真っ黒い", "まっくろい", "漆黑的"], ["ゴロゴロ", "ごろごろ", "轰隆隆（雷声）"], ["避難", "ひなん", "避难"], ["安全", "あんぜん", "安全"], ["激しい", "はげしい", "激烈的、猛烈的"]]
            },
            {
                "ja": "避難する場所は、近くのしっかりした建物や、車の中が良いでしょう。木の下での雨宿りは、木に落ちた雷が人に飛び移ることがあるので、危険です。万が一、周囲に避難する場所がない時は、両足をそろえて、頭を下げてしゃがみ、両手で耳をふさぎましょう。",
                "en": "For shelter, a sturdy building nearby or inside a car is best. Taking shelter under a tree is dangerous, because lightning that strikes the tree can jump to a person. If there is nowhere to take shelter, squat down with your feet together, lower your head, and cover your ears with both hands.",
                "literal": "避难的地方，附近的坚固建筑物或车内为好。在树下避雨很危险，因为落在树上的雷有时会转移到人身上。万一周围没有避难场所时，请双脚并拢、低下头蹲下，用双手捂住耳朵。",
                "grammar": "「〜が良いでしょう」— …为好（建议）。例：車の中が良いでしょう（车内为好）。\n「〜ことがある」— 有时会…。例：飛び移ることがある（有时会转移）。\n「〜ましょう」— 让我们…吧（劝诱）。例：耳をふさぎましょう（捂住耳朵吧）。",
                "vocab": [["しっかりした", "しっかりした", "坚固的、结实的"], ["雨宿り", "あまやどり", "避雨"], ["飛び移る", "とびうつる", "跳移、转移"], ["万が一", "まんがいち", "万一"], ["しゃがむ", "しゃがむ", "蹲下"], ["ふさぐ", "ふさぐ", "堵住、捂住"]]
            },
        ]
    },
    {
        "slug": "kokki-sonkai-tsumi",
        "title": "日本国旗損壊罪法が施行 拘禁刑2年以下か罰金",
        "subtitle": "from 共同通信",
        "paras": [
            {
                "ja": "日本の国旗を傷つける行為を処罰する日本国旗損壊罪法が13日、施行された。「人に著しく不快、嫌悪の情を催させる方法」で公然と国旗を損壊、除去、汚損した場合に2年以下の拘禁刑または20万円以下の罰金を科す。国会審議では、憲法が保障する「表現の自由」の侵害や、拡大解釈による適用への懸念が指摘された。",
                "en": "The Act on the Crime of Damaging the National Flag, which penalizes acts that damage the Japanese flag, took effect on the 13th. Those who openly destroy, remove, or defile the flag \"in a manner that causes people marked discomfort or disgust\" will be subject to up to two years of imprisonment or a fine of up to 200,000 yen. During Diet deliberations, concerns were raised about infringement of the \"freedom of expression\" guaranteed by the Constitution and about application through expansive interpretation.",
                "literal": "处罚损害日本国旗行为的日本国旗损坏罪法于13日施行。以“使人显著产生不快、厌恶情绪的方法”公然损坏、移除、污损国旗的，处2年以下拘禁刑或20万日元以下罚金。国会审议中，有人指出这会侵害宪法保障的“表现自由”，以及因扩大解释而适用的担忧。",
                "grammar": "「〜を処罰する」— 处罚…。例：国旗を傷つける行為を処罰する（处罚损害国旗的行为）。\n「〜場合に」— 在…的情况下。例：損壊した場合に処罰（在损坏的情况下处罚）。\n「〜が指摘された」— 被指出…。例：懸念が指摘された（指出了担忧）。",
                "vocab": [["損壊", "そんかい", "损坏、毁坏"], ["処罰", "しょばつ", "处罚"], ["施行", "しこう", "施行"], ["嫌悪", "けんお", "厌恶、嫌恶"], ["公然", "こうぜん", "公然、公开"], ["拘禁刑", "こうきんけい", "拘禁刑（监禁刑）"]]
            },
            {
                "ja": "国旗損壊罪の創設は高市早苗首相が首相就任前から提唱し、昨年10月の自民党と日本維新の会との連立政権合意書に盛り込まれた。「国旗を大切にする国民感情の保護」を目的に、自民、維新、国民民主、参政4党が先の特別国会に共同提出し、7月17日に成立した。",
                "en": "The creation of the flag-damage crime was advocated by Prime Minister Takaichi Sanae even before she took office, and was incorporated into the coalition agreement between the Liberal Democratic Party and Nippon Ishin last October. Aiming to \"protect the national sentiment of treasuring the flag,\" the four parties — LDP, Ishin, Kokumin Minshu, and Sanseitō — jointly submitted the bill to the previous extraordinary Diet session, and it passed on July 17.",
                "literal": "国旗损坏罪的创设由高市早苗首相就任前就提出，被写入了去年10月自民党与日本维新会之间的联合政权协议书中。以“保护珍视国旗的国民感情”为目的，自民、维新、国民民主、参政4党在之前的特别国会上共同提交，于7月17日成立。",
                "grammar": "「〜前から提唱し」— 从…之前就提倡。例：首相就任前から提唱し（就任前就提倡）。\n「〜に盛り込まれた」— 被写入…。例：合意書に盛り込まれた（被写入协议书中）。\n「〜を目的に」— 以…为目的。例：国民感情の保護を目的に（以保护国民感情为目的）。",
                "vocab": [["創設", "そうせつ", "创设"], ["提唱", "ていしょう", "提倡"], ["連立政権", "れんりつせいけん", "联合政权"], ["合意書", "ごういしょ", "协议书"], ["共同提出", "きょうどうていしゅつ", "共同提交"], ["成立", "せいりつ", "成立、通过"]]
            },
            {
                "ja": "処罰対象は、行為の外形、周囲の状況その他の客観的な事情を総合的に勘案すると規定。適用に当たって表現の自由など憲法の保障する国民の自由と権利を不当に侵害しないよう留意するとされた。付則では、施行後3年をめどに状況を勘案し、必要がある場合は所要の措置を講じるとした。",
                "en": "The law stipulates that the subject of punishment is determined by comprehensively considering the outward form of the act, surrounding circumstances, and other objective facts. It also states that care must be taken not to improperly infringe on the freedoms and rights of the people guaranteed by the Constitution, such as freedom of expression, when applying the law. In supplementary provisions, it says that within about three years after enforcement, the situation will be reviewed and necessary measures will be taken if needed.",
                "literal": "处罚对象规定为综合考量行为的外形、周围状况及其他客观情况。适用之际，要注意不得不当侵害表现自由等宪法保障的国民自由与权利。附则规定，以施行后3年为期审视情况，有必要时采取所需措施。",
                "grammar": "「〜に当たって」— 在…之际。例：適用に当たって（在适用之际）。\n「〜よう留意する」— 注意做到…。例：侵害しないよう留意する（注意不要侵害）。\n「〜をめどに」— 以…为目标/期限。例：3年をめどに（以3年为期）。",
                "vocab": [["処罰対象", "しょばつたいしょう", "处罚对象"], ["外形", "がいけい", "外形"], ["客観的", "きゃっかんてき", "客观的"], ["勘案", "かんあん", "斟酌、考量"], ["付則", "ふそく", "附则"], ["措置", "そち", "措施"]]
            },
        ]
    },
    {
        "slug": "tokkyu-sonic-syoutotsu",
        "title": "事故に気が付かず特急が走行続ける JR日豊本線で車と衝突 上下線運休しお盆の移動に影響",
        "subtitle": "from TOSテレビ大分",
        "paras": [
            {
                "ja": "12日午後、福岡県内の踏切でJR日豊本線の特急列車と車が衝突する事故があり、一時、上下線ともに運休となりました。特急は事故に気がつかず、大分県の宇佐駅まで走行したということです。事故が起きたのは福岡県の三毛門駅と吉富駅の間のJR日豊本線の踏切です。",
                "en": "On the afternoon of the 12th, a limited express train on the JR Nippo Main Line collided with a car at a railroad crossing in Fukuoka Prefecture, and both up and down lines were temporarily suspended. The limited express reportedly continued running without noticing the accident, all the way to Usa Station in Oita Prefecture. The accident occurred at a crossing on the JR Nippo Line between Miketo Station and Yoshitomi Station in Fukuoka Prefecture.",
                "literal": "12日下午，福冈县内的铁路道口发生了JR日丰本线特快列车与汽车相撞的事故，上下行线一度全部停运。据说特快没有察觉事故，一直行驶到了大分县的宇佐站。事故发生地在福冈县三毛门站与吉富站之间的JR日丰本线道口。",
                "grammar": "「〜という事故があり」— 发生了…的事故。例：衝突する事故があり（发生了相撞事故）。\n「〜に気がつかず」— 没有察觉到…。例：事故に気がつかず（没有察觉事故）。\n「〜ということです」— 据说…。例：走行したということです（据说行驶了）。",
                "vocab": [["踏切", "ふみきり", "铁路道口"], ["衝突", "しょうとつ", "相撞、冲突"], ["特急", "とっきゅう", "特快列车"], ["上下線", "じょうげせん", "上下行线"], ["運休", "うんきゅう", "停运"], ["走行", "そうこう", "行驶"]]
            },
            {
                "ja": "JR九州によりますと、12日午後2時すぎ、下りの特急列車ソニックと車が衝突しました。しかし、特急列車はそのまま走行を続けたということです。一方、車は破損し、踏切の非常停止ボタンが押されたことから、JRは宇佐駅でこの特急列車を止めて確認したところ、側面に損傷が確認され、事故が発覚したということです。",
                "en": "According to JR Kyushu, shortly after 2 p.m. on the 12th, the downbound limited express Sonic collided with a car. However, the limited express reportedly continued running as it was. Meanwhile, the car was damaged, and because the emergency stop button at the crossing had been pressed, JR stopped the train at Usa Station to check it, where damage on the side was confirmed, and the accident came to light.",
                "literal": "据JR九州称，12日下午2点多，下行特快列车Sonic与汽车相撞。但据说特快列车就那样继续行驶了。另一方面，汽车破损，由于道口的紧急停车按钮被按下，JR在宇佐站停下这列特快确认后，确认了侧面损伤，事故由此暴露。",
                "grammar": "「〜によりますと」— 据…称。例：JR九州によりますと（据JR九州称）。\n「〜ことから」— 因为…（原因）。例：ボタンが押されたことから（因为按钮被按下）。\n「〜たところ」— 一…结果…。例：確認したところ（一确认结果）。",
                "vocab": [["下り", "くだり", "下行"], ["そのまま", "そのまま", "就那样、原样"], ["破損", "はそん", "破损"], ["非常停止", "ひじょうていし", "紧急停止"], ["側面", "そくめん", "侧面"], ["発覚", "はっかく", "暴露、败露"]]
            },
            {
                "ja": "乗客およそ250人にけがはありませんでした。この影響で日豊本線は一時、上下線とも運休となり、お盆の時期の移動に影響が出ました。運転は午後5時半ごろまでに再開されています。",
                "en": "No injuries were reported among the approximately 250 passengers. Due to this incident, the Nippo Main Line was temporarily suspended in both directions, affecting travel during the Obon holiday period. Operations had resumed by around 5:30 p.m.",
                "literal": "约250名乘客无人受伤。受此影响，日丰本线一度上下行均停运，对盂兰盆节期间的出行造成了影响。运行在下午5点半左右前已恢复。",
                "grammar": "「〜にけがはありませんでした」— 没有受伤。例：乗客にけがはありませんでした（乘客没有受伤）。\n「〜お盆の時期」— 盂兰盆节期间。例：お盆の時期の移動（盂兰盆节期间的出行）。\n「〜までに再開」— 在…之前恢复。例：午後5時半ごろまでに再開（在下午5点半前恢复）。",
                "vocab": [["乗客", "じょうきゃく", "乘客"], ["およそ", "およそ", "大约"], ["お盆", "おぼん", "盂兰盆节"], ["移動", "いどう", "出行、移动"], ["再開", "さいかい", "恢复、重新开始"], ["影響", "えいきょう", "影响"]]
            },
        ]
    },
    {
        "slug": "awaodori-satsuei-manner",
        "title": "「怖い」阿波おどり開幕も踊り手から不安の声 女性踊り手狙う動画拡散",
        "subtitle": "from FNNプライムオンライン",
        "paras": [
            {
                "ja": "徳島の夏の夜を彩る一大行事、屋外会場での阿波おどりが12日スタートした。「踊る阿呆に見る阿呆」のお囃子とともに踊り手たちが勇壮かつ華麗な舞いを披露する「阿波おどり」。15日まで4日間にわたり、徳島市内の複数の屋外会場で行われる。しかし、今年は阿波おどりの開催にあたり、踊り手たちから「不安の声」が聞かれた。「観客による撮影マナー」の問題だ。",
                "en": "Awa Odori, a major event that colors Tokushima's summer nights, began at outdoor venues on the 12th. Dancers perform brave and gorgeous dances to the accompaniment of hayashi music, embodying the saying \"dancing fools and watching fools.\" It will be held at multiple outdoor venues in Tokushima City over four days until the 15th. However, this year, ahead of the festival, voices of concern were heard from the dancers. The problem is \"camera manners of spectators.\"",
                "literal": "点缀德岛夏夜的一大盛事——室外会场的阿波舞于12日开幕。伴着“跳舞的傻瓜、看舞的傻瓜”的伴奏乐，舞者们表演勇壮而华丽的舞蹈“阿波舞”。到15日为止历时4天，在德岛市内多个室外会场举行。但今年阿波舞举办之际，舞者们发出了“不安之声”。这是“观众拍摄礼仪”的问题。",
                "grammar": "「〜を彩る」— 点缀…、为…增添色彩。例：夏の夜を彩る行事（点缀夏夜的活动）。\n「〜にわたり」— 历时…。例：4日間にわたり（历时4天）。\n「〜にあたり」— 在…之际。例：開催にあたり（在举办之际）。",
                "vocab": [["彩る", "いろどる", "点缀、装点"], ["一大行事", "いちだいぎょうじ", "一大盛事"], ["お囃子", "おはやし", "伴奏乐、囃子"], ["勇壮", "ゆうそう", "勇壮"], ["華麗", "かれい", "华丽"], ["撮影マナー", "さつえいまなー", "拍摄礼仪"]]
            },
            {
                "ja": "踊り手の女性は「色々な人に阿波おどりの魅力を知って欲しいということで撮ってくださっている方もいると思うが、『本来の目的ではない撮り方』によって、その動画が世界に発信されるわけで、すごく怖い」と話す。臀部や胸など、踊り手の女性の体の一部を一般のカメラマンが撮り続けるなどする動画が、撮影された本人が知らないうちに、ネットに投稿・拡散しているのだ。",
                "en": "A female dancer said, \"Some people film us because they want many people to know the charm of Awa Odori, but videos shot 'in ways that aren't the original purpose' get broadcast to the world, and that's really scary.\" Videos in which amateur photographers keep filming parts of female dancers' bodies, such as their hips and chests, are being posted and spread online without the filmed dancers knowing.",
                "literal": "女舞者说：“虽然也有人是为了让更多人了解阿波舞的魅力而拍摄，但以‘并非本来的拍摄目的’拍出的视频会向世界传播，非常可怕。”摄影师持续拍摄女舞者臀部、胸部等身体部位的视频，在被拍者本人不知情的情况下被上传到网络并扩散开来。",
                "grammar": "「〜てほしい」— 希望…。例：知って欲しい（希望了解）。\n「〜わけで」— 也就是说…（说明）。例：発信されるわけで（也就是会被传播）。\n「〜ないうちに」— 在…之前/不知不觉中。例：知らないうちに（在不知情时）。",
                "vocab": [["魅力", "みりょく", "魅力"], ["本来", "ほんらい", "本来"], ["臀部", "でんぶ", "臀部"], ["拡散", "かくさん", "扩散"], ["投稿", "とうこう", "投稿"], ["撮影", "さつえい", "拍摄"]]
            },
            {
                "ja": "約160人の踊り手が所属する「阿呆連」の責任者は、少なくとも数年前からこうした動画の存在をいくつも確認していると言う。こうした状況を受け、踊り手たちは普段の練習でも自らを守る対策をせざるを得ないという。「夏なので、あまり長袖長ズボンというわけにはいかないんですが、できるだけ透けない、ボディーラインが出ないような服にしてもらう」と話す。",
                "en": "The leader of \"Aho-ren,\" an organization with about 160 dancers, says they have confirmed the existence of several such videos since at least a few years ago. Faced with this situation, dancers are forced to take measures to protect themselves even during regular practice. He says, \"Since it's summer, we can't exactly have them wear long sleeves and long pants, so we ask them to wear clothes that don't show through and don't reveal body lines as much as possible.\"",
                "literal": "约有160名舞者所属的“阿呆连”负责人称，至少从几年前起就已确认了多段此类视频的存在。面对这种情况，舞者们即使在平时的练习中也不得不采取自我保护的对策。“因为是夏天，不能要求穿长袖长裤，所以尽量让大家穿不透明、不显身材线条的衣服。”他这样说道。",
                "grammar": "「〜せざるを得ない」— 不得不…。例：対策をせざるを得ない（不得不采取对策）。\n「〜わけにはいかない」— 不能…（情理上）。例：長袖長ズボンというわけにはいかない（不能要求长袖长裤）。\n「〜ようにする」— 设法做到…。例：服にしてもらう（让她们穿…的衣服）。",
                "vocab": [["所属", "しょぞく", "所属"], ["責任者", "せきにんしゃ", "负责人"], ["対策", "たいさく", "对策"], ["長袖", "ながそで", "长袖"], ["透ける", "すける", "透明、透光"], ["ボディーライン", "ぼでぃーらいん", "身体线条"]]
            },
            {
                "ja": "阿波おどりの実行委員会は「一般の個人カメラマン・撮影者へのお願い」として公序良俗に反する発信を控えるなど、撮影マナーの徹底を呼びかけている。実行委員会側は、踊り手が「性的で不快な動画」だと訴える動画の投稿者の1人にコンタクトを取り、投稿をやめるよう直接話をしたという。しかし、投稿者は「あれは芸術だと、そういう感覚で撮ったと、だからひとつも恥ずかしいことはない」と言われ、線引きが難しいと感じている。",
                "en": "The Awa Odori executive committee has updated its website to call for thorough camera manners, such as refraining from posts that violate public order and morals, under the heading \"A request to general individual photographers.\" The committee reportedly contacted one of the posters of videos that dancers say are \"sexual and unpleasant\" videos and directly asked them to stop posting. However, the poster said, \"That's art, I filmed it with that feeling, so there's nothing to be ashamed of,\" and the committee finds it difficult to draw the line.",
                "literal": "阿波舞执行委员会以“致普通个人摄影师、拍摄者的请求”为题，呼吁贯彻拍摄礼仪，如克制发布违反公序良俗的内容等。委员会方面联系了舞者控诉的“性暗示且令人不快视频”的其中一名发布者，直接与其交涉要求停止发布。但发布者称“那是艺术，是带着那种感觉拍的，所以一点都不觉得羞耻”，委员会感到很难划定界限。",
                "grammar": "「〜に反する」— 违反…。例：公序良俗に反する（违反公序良俗）。\n「〜を控える」— 克制…。例：発信を控える（克制发布）。\n「〜よう直接話をした」— 直接交涉要求…。例：やめるよう直接話をした（直接要求停止）。",
                "vocab": [["実行委員会", "じっこういいんかい", "执行委员会"], ["公序良俗", "こうじょりょうぞく", "公序良俗"], ["徹底", "てってい", "彻底"], ["呼びかける", "よびかける", "呼吁"], ["コンタクト", "こんたくと", "联系、接触"], ["線引き", "せんびき", "划界、界限"]]
            },
        ]
    },
    {
        "slug": "chuko-sya-hasan",
        "title": "中古車販売会社が破産開始決定 負債総額は2億1000万円",
        "subtitle": "from MBC南日本放送",
        "paras": [
            {
                "ja": "中古車販売やカーメンテナンスなどを手がける鹿児島市の企業が、鹿児島地裁から破産開始決定を受けたことがわかりました。破産開始決定を受けたのは、鹿児島市川上町の「Zeal」です。東京商工リサーチ鹿児島支店によりますと「Zeal」は2020年6月に設立。鹿児島市川上町に店舗を構え、中古車販売や、自動車のボディを守るプロテクションフィルムコーティングなどのサービスなども提供し、個人顧客から一定の受注基盤を構築していました。",
                "en": "A company in Kagoshima City that deals in used car sales and car maintenance has been ordered by the Kagoshima District Court to begin bankruptcy proceedings. The company that received the bankruptcy order is \"Zeal,\" located in Kawakami-cho, Kagoshima City. According to Tokyo Shoko Research's Kagoshima branch, Zeal was established in June 2020. It operated a store in Kawakami-cho, Kagoshima City, offering used car sales and services such as protective film coating that protects car bodies, and had built a certain order base among individual customers.",
                "literal": "经营二手车销售和汽车保养等的鹿儿岛市企业，已获悉被鹿儿岛地方法院作出破产程序开始决定。被作出破产开始决定的是鹿儿岛市川上町的“Zeal”。据东京商工调查鹿儿岛分店称，“Zeal”于2020年6月设立。在鹿儿岛市川上町开设门店，提供二手车销售以及保护汽车车身的保护膜涂层等服务，在个人客户中建立了稳定的接单基础。",
                "grammar": "「〜を手がける」— 经营、从事…。例：中古車販売を手がける（经营二手车销售）。\n「〜を受けた」— 受到…。例：破産開始決定を受けた（被作出破产开始决定）。\n「〜によりますと」— 据…称。例：東京商工リサーチによりますと（据东京商工调查称）。",
                "vocab": [["中古車", "ちゅうこしゃ", "二手车"], ["破産", "はさん", "破产"], ["負債", "ふさい", "负债"], ["地裁", "ちさい", "地方法院"], ["設立", "せつりつ", "设立"], ["受注", "じゅちゅう", "接单"]]
            },
            {
                "ja": "しかし近年は中古車相場の変動が大きく、アメリカの関税政策を背景とした輸出環境の変化もありました。国内市場における需給の緩みや価格下落圧力により販売不振へと陥り、資金繰りが逼迫したとされています。",
                "en": "In recent years, however, used car market prices have fluctuated greatly, and there were also changes in the export environment against the backdrop of US tariff policies. Due to loosening supply-demand conditions in the domestic market and downward pressure on prices, the company fell into poor sales, and its cash flow reportedly became strained.",
                "literal": "但近年来二手车行情波动很大，以美国关税政策为背景的出口环境也发生了变化。由于国内市场供求松动和价格下跌压力，销售陷入不振，资金周转被认为趋于紧张。",
                "grammar": "「〜を背景とした」— 以…为背景的。例：関税政策を背景とした変化（以关税政策为背景的变化）。\n「〜により」— 由于…。例：価格下落圧力により（由于价格下跌压力）。\n「〜とされています」— 被认为…。例：逼迫したとされています（被认为趋于紧张）。",
                "vocab": [["相場", "そうば", "行情、市价"], ["変動", "へんどう", "变动"], ["関税", "かんぜい", "关税"], ["需給", "じゅきゅう", "供求"], ["販売不振", "はんばいふしん", "销售不振"], ["資金繰り", "しきんぐり", "资金周转"]]
            },
            {
                "ja": "鹿児島地方裁判所からの破産開始決定は6月29日で、負債総額は債権者30人に対して2億1000万円とみられています。",
                "en": "The bankruptcy order from the Kagoshima District Court was issued on June 29, and the total liabilities are estimated at 210 million yen owed to 30 creditors.",
                "literal": "鹿儿岛地方法院的破产开始决定为6月29日，负债总额被认为是对30名债权人合计2亿1000万日元。",
                "grammar": "「〜に対して」— 对…（对象）。例：債権者30人に対して（对30名债权人）。\n「〜とみられています」— 被认为…。例：2億1000万円とみられています（被认为2亿1000万日元）。",
                "vocab": [["破産開始決定", "はさんかいしけってい", "破产程序开始决定"], ["債権者", "さいけんしゃ", "债权人"], ["総額", "そうがく", "总额"], ["みられる", "みられる", "被认为"], ["決定", "けってい", "决定"], ["6月29日", "ろくがつにじゅうくにち", "6月29日"]]
            },
        ]
    },
    {
        "slug": "taifu-tamago-kantou",
        "title": "新たな「台風のたまご」発生 17日お盆明けに関東沖接近のおそれ",
        "subtitle": "from NBC長崎放送",
        "paras": [
            {
                "ja": "気象庁によりますと、12日午前3時現在、小笠原近海で新たな「台風のたまご（熱帯低気圧）」が発生しています。今後「台風」へと発達しながら北上し、お盆休み明けとなる8月17日（月）ごろに、再び関東など東日本へ接近するおそれがあります。",
                "en": "According to the Japan Meteorological Agency, as of 3 a.m. on the 12th, a new \"typhoon egg (tropical depression)\" had formed off the Ogasawara Islands. It will develop into a \"typhoon\" and move northward, and there is a risk that it will again approach Kanto and other parts of eastern Japan around Monday, August 17, after the Obon holiday.",
                "literal": "据气象厅称，截至12日凌晨3点，小笠原近海出现了新的“台风的蛋（热带低气压）”。今后它将一边发展成“台风”一边北上，在盂兰盆节假期结束后的8月17日（周一）前后，有可能再次接近关东等东日本地区。",
                "grammar": "「〜現在」— 截至…时点。例：午前3時現在（截至凌晨3点）。\n「〜ながら」— 一边…一边…。例：発達しながら北上し（一边发展一边北上）。\n「〜おそれがあります」— 有…的危险/可能。例：接近するおそれがあります（有可能接近）。",
                "vocab": [["気象庁", "きしょうちょう", "气象厅"], ["小笠原", "おがさわら", "小笠原（群岛）"], ["熱帯低気圧", "ねったいていきあつ", "热带低气压"], ["発達", "はったつ", "发展、增强"], ["北上", "ほくじょう", "北上"], ["接近", "せっきん", "接近"]]
            },
            {
                "ja": "気象庁によりますと、小笠原近海にある熱帯低気圧は12日午前3時現在、1時間に約15キロの速さで東北東へ進んでいます。中心気圧は996ヘクトパスカル、中心付近の最大風速は15メートルです。この熱帯低気圧は今後海上で発達し、13日午前3時までには「台風」に変わる見込みです。",
                "en": "According to the JMA, the tropical depression off the Ogasawara Islands was moving east-northeast at about 15 km per hour as of 3 a.m. on the 12th. Its central pressure is 996 hectopascals, and the maximum wind speed near the center is 15 meters per second. This tropical depression will develop over the sea and is expected to become a \"typhoon\" by 3 a.m. on the 13th.",
                "literal": "据气象厅称，小笠原近海的热带低气压截至12日凌晨3点正以每小时约15公里的速度向东北偏东方向移动。中心气压为996百帕，中心附近最大风速为15米。这个热带低气压今后将在海上发展，预计到13日凌晨3点前将变成“台风”。",
                "grammar": "「〜の速さで」— 以…的速度。例：15キロの速さで進む（以15公里的速度移动）。\n「〜までには」— 到…之前。例：13日までには（到13日之前）。\n「〜見込みです」— 预计…。例：変わる見込みです（预计变成）。",
                "vocab": [["東北東", "とうほくとう", "东北偏东"], ["中心気圧", "ちゅうしんきあつ", "中心气压"], ["ヘクトパスカル", "へくとぱすかる", "百帕（气压单位）"], ["最大風速", "さいだいふうそく", "最大风速"], ["見込み", "みこみ", "预计、预期"], ["進む", "すすむ", "前进、移动"]]
            },
            {
                "ja": "台風へと発達した後は、日本の東海上を北北西へと進路を変え、お盆休み明けの17日（月）ごろに関東沖へ接近する予想となっています。今後の進路や強さの発達具合によっては、お盆のUターンラッシュや連休明けの交通機関、各地の天気に影響を与える可能性があるため、最新の気象情報に十分な注意が必要です。",
                "en": "After developing into a typhoon, it is forecast to change course to the north-northwest over the seas east of Japan and approach off the coast of Kanto around Monday the 17th, after the Obon holiday. Depending on its future track and how much it strengthens, it could affect the Obon return-travel rush, transportation after the holidays, and weather in various regions, so close attention to the latest weather information is necessary.",
                "literal": "发展成台风后，预计它将把路线改为向日本东部海域的西北偏北方向前进，在盂兰盆节假期结束后的17日（周一）前后接近关东近海。根据今后路径和强度发展情况，有可能对盂兰盆节的返程高峰、假期结束后的交通机构以及各地天气造成影响，因此需要充分注意最新气象信息。",
                "grammar": "「〜へと」— 朝着…（方向变化）。例：北北西へと進路を変え（将路线改为向北北西）。\n「〜によっては」— 根据…的不同。例：発達具合によっては（根据发展情况）。\n「〜可能性がある」— 有…的可能性。例：影響を与える可能性がある（有可能造成影响）。",
                "vocab": [["進路", "しんろ", "路径、路线"], ["北北西", "ほくほくせい", "西北偏北"], ["予想", "よそう", "预测"], ["Uターン", "ゆーたーん", "返乡返程（U-turn）"], ["交通機関", "こうつうきかん", "交通机构"], ["気象情報", "きしょうじょうほう", "气象信息"]]
            },
        ]
    },
    {
        "slug": "yatsushiro-sichousya-menjin",
        "title": "免振装置を備え171億円かけ建てた庁舎 震度6強で「免震機能は失われている」",
        "subtitle": "from RKK熊本放送",
        "paras": [
            {
                "ja": "10年前の熊本地震で被災し、建て替えられた八代市役所が今回の地震で被害を受けました。地震の2日後に開かれた八代市の災害対策本部会議で報告されたのが、復旧・復興の拠点である庁舎の被害状況でした。八代市の担当者は「地下の壁と天井の一部崩壊。配管の破損による水漏れ。免震装置のズレ、つぶれが発生している」と説明しました。",
                "en": "Yatsushiro City Hall, which was rebuilt after being damaged in the Kumamoto earthquake 10 years ago, was damaged in this latest earthquake. What was reported at the city's disaster response headquarters meeting held two days after the quake was the damage to the city hall building, which serves as the base for recovery and reconstruction. A city official explained, \"Partial collapse of underground walls and ceilings. Water leakage from damaged piping. Displacement and crushing of the seismic isolation devices have occurred.\"",
                "literal": "10年前在熊本地震中受灾、重建的八代市政府大楼在这次地震中受损。在地震2天后召开的八代市灾害对策本部会议上报告的，是作为恢复复兴据点的政府大楼的受损情况。八代市负责人说明称：“地下墙壁和天花板部分坍塌。配管破损导致漏水。免震装置发生偏移和压溃。”",
                "grammar": "「〜で被災し」— 在…中受灾。例：熊本地震で被災し（在熊本地震中受灾）。\n「〜の拠点である」— 是…据点的。例：復興の拠点である庁舎（作为复兴据点的政府大楼）。\n「〜による」— 由…造成的。例：配管の破損による水漏れ（配管破损造成的漏水）。",
                "vocab": [["被災", "ひさい", "受灾"], ["建て替える", "たてかえる", "重建、翻建"], ["庁舎", "ちょうしゃ", "政府大楼、厅舍"], ["復旧", "ふっきゅう", "恢复"], ["復興", "ふっこう", "复兴"], ["免震装置", "めんしんそうち", "免震装置"]]
            },
            {
                "ja": "4年前に完成したばかりの庁舎は、今回の地震で地下の壁や天井の一部が崩落し、今も立ち入り禁止となっている場所があります。地震があった7月28日は、40人ほどの住民を受け入れていましたが、この状況にそれを停止せざるを得ませんでした。",
                "en": "The city hall, which had been completed only four years ago, suffered partial collapse of underground walls and ceilings in this earthquake, and some areas remain off-limits even now. On July 28, when the earthquake struck, the building was sheltering about 40 residents, but they had no choice but to stop doing so under these circumstances.",
                "literal": "4年前刚刚建成的政府大楼在这次地震中地下墙壁和天花板部分坍塌，至今仍有禁止入内的场所。地震发生的7月28日，大楼接纳了约40名居民，但在这种情况下不得不停止接纳。",
                "grammar": "「〜たばかり」— 刚刚…。例：完成したばかり（刚刚完成）。\n「〜となっています」— 处于…状态。例：立ち入り禁止となっています（处于禁止入内状态）。\n「〜せざるを得ませんでした」— 不得不…。例：停止せざるを得ませんでした（不得不停止）。",
                "vocab": [["崩落", "ほうらく", "坍塌、崩落"], ["立ち入り禁止", "たちいりきんし", "禁止入内"], ["住民", "じゅうみん", "居民"], ["受け入れる", "うけいれる", "接纳、接收"], ["停止", "ていし", "停止"], ["状況", "じょうきょう", "状况"]]
            },
            {
                "ja": "以前の八代市役所の庁舎が10年前の地震で被災したため、約171億円かけた新しい庁舎が4年前に完成しました。揺れを軽減するために地下1階の柱に「ダンパー」と呼ばれる装置が設置されました。このダンパーが今回の熊本地震で大きく変形し、ズレが生じたのです。",
                "en": "Because the previous Yatsushiro City Hall building was damaged in the earthquake 10 years ago, a new building costing about 17.1 billion yen was completed four years ago. To reduce shaking, devices called \"dampers\" were installed on the columns of the basement level. These dampers were greatly deformed in this Kumamoto earthquake, resulting in displacement.",
                "literal": "由于以前的八代市政府大楼在10年前的地震中受灾，耗资约171亿日元的新政府大楼于4年前建成。为减轻摇晃，在地下1层的柱子上安装了被称为“减震器”的装置。这个减震器在这次熊本地震中严重变形，产生了偏移。",
                "grammar": "「〜ため」— 因为…。例：被災したため（因为受灾）。\n「〜ために」— 为了…。例：揺れを軽減するために（为了减轻摇晃）。\n「〜と呼ばれる」— 被称为…的。例：ダンパーと呼ばれる装置（被称为减震器的装置）。",
                "vocab": [["軽減", "けいげん", "减轻"], ["ダンパー", "だんぱー", "减震器、阻尼器"], ["設置", "せっち", "设置"], ["変形", "へんけい", "变形"], ["ズレ", "ずれ", "偏移、错位"], ["生じる", "しょうじる", "产生、发生"]]
            },
            {
                "ja": "2日、免震機能について小野市長は「免震機能は失われている」との見解を示しました。一方、地震後、免震機能の調査をした専門家の1人は「免震装置は見たことがないほど変形したが、機能を発揮したことで上部構造に大きな損傷はない。現状、建物の安全性に問題はない」としているものの、「今後大きな揺れに耐えられるかは調査中」としています。",
                "en": "On the 2nd, Mayor Ono expressed the view regarding the seismic isolation function that \"the seismic isolation function has been lost.\" Meanwhile, one expert who investigated the seismic isolation function after the earthquake said, \"The isolation devices were deformed more than I've ever seen, but because they performed their function, there is no major damage to the upper structure. At present, there is no problem with the building's safety,\" though they added that \"whether it can withstand major shaking in the future is under investigation.\"",
                "literal": "2日，关于免震功能，小野市长表明了“免震功能已经丧失”的见解。另一方面，地震后调查免震功能的其中一位专家表示：“免震装置变形到从未见过的程度，但由于发挥了功能，上部结构没有大的损伤。目前建筑物的安全性没有问题。”不过他也表示“今后能否承受大的摇晃尚在调查中”。",
                "grammar": "「〜との見解を示した」— 表明了…的见解。例：失われているとの見解（已经丧失的见解）。\n「〜たこと」— 因为…了。例：機能を発揮したことで（因为发挥了功能）。\n「〜ものの」— 虽然…但是…。例：問題はないとしているものの（虽然表示没有问题）。",
                "vocab": [["免震機能", "めんしんきのう", "免震功能"], ["見解", "けんかい", "见解"], ["専門家", "せんもんか", "专家"], ["発揮", "はっき", "发挥"], ["上部構造", "じょうぶこうぞう", "上部结构"], ["損傷", "そんしょう", "损伤"]]
            },
        ]
    },
    {
        "slug": "nakakyusyu-oudan-douro",
        "title": "「所要時間1時間以上短縮」全線開通で運送事業者の6割がプラス効果 中九州横断道路アンケート",
        "subtitle": "from OBS大分放送",
        "paras": [
            {
                "ja": "TSMCの進出などを受けて期待されている中九州横断道路について、全線開通した場合、運送事業者の6割がプラスの効果を見込んでいることがわかりました。大銀経済経営研究所は、大分と熊本のトラック運送事業者に中九州横断道路についてアンケートを実施し、279の事業者から得た回答について結果をまとめました。",
                "en": "Regarding the Trans-Kyushu Central Expressway, which is expected to bring benefits following TSMC's entry, it has been found that 60% of transport operators expect positive effects if the entire line opens. The Dai-Gin Economic Research Institute conducted a survey on the expressway among trucking operators in Oita and Kumamoto and compiled results from responses obtained from 279 operators.",
                "literal": "关于因TSMC进驻等而备受期待的中九州横断道路，已获悉若全线开通，6成运输业者预计会有正面效果。大银经济经营研究所对大分和熊本的卡车运输业者实施了关于中九州横断道路的问卷调查，汇总了从279家业者获得的回答结果。",
                "grammar": "「〜を受けて」— 因…、随着…。例：TSMCの進出を受けて（随着TSMC进驻）。\n「〜場合」— 在…的情况下。例：全線開通した場合（全线开通的情况下）。\n「〜を実施し」— 实施…。例：アンケートを実施し（实施问卷调查）。",
                "vocab": [["進出", "しんしゅつ", "进驻、进入"], ["横断", "おうだん", "横断、横穿"], ["全線", "ぜんせん", "全线"], ["運送事業者", "うんそうじぎょうしゃ", "运输业者"], ["アンケート", "あんけーと", "问卷调查"], ["回答", "かいとう", "回答"]]
            },
            {
                "ja": "全線が開通した場合、大分市から熊本市までの所要時間が現在の3時間39分のところ、2時間29分と1時間以上の短縮が見込まれています。アンケートの結果、「プラスの効果がある」と答えた事業所の割合は約6割に上りました。理由としては「運送効率が上がる」が39.4パーセントと最も多くなっています。",
                "en": "If the entire line opens, travel time from Oita City to Kumamoto City is expected to be cut from the current 3 hours 39 minutes to 2 hours 29 minutes — a reduction of more than one hour. In the survey results, the proportion of businesses that answered \"there will be positive effects\" reached about 60%. As for reasons, \"transport efficiency will improve\" was the most common at 39.4 percent.",
                "literal": "若全线开通，从大分市到熊本市的所需时间预计将从目前的3小时39分缩短为2小时29分，缩短1小时以上。问卷调查结果显示，回答“有正面效果”的事业所比例达到约6成。理由中“运输效率提高”占39.4%，为最多。",
                "grammar": "「〜のところ」— 目前是…（对比）。例：3時間39分のところ（目前是3小时39分）。\n「〜が見込まれています」— 预计…。例：短縮が見込まれています（预计缩短）。\n「〜に上りました」— 达到…。例：6割に上りました（达到6成）。",
                "vocab": [["所要時間", "しょようじかん", "所需时间"], ["短縮", "たんしゅく", "缩短"], ["割合", "わりあい", "比例"], ["効率", "こうりつ", "效率"], ["最も", "もっとも", "最"], ["理由", "りゆう", "理由"]]
            },
            {
                "ja": "また、今後の運送ルートの変化については変わらないとした事業者が多いものの、13.3パーセントが「大分港の利用が増える」と回答しています。今年度、最も難所とされた大分と熊本の県境に位置する「滝室坂道路」の6キロの区間が開通します。TSMC進出による波及効果とともに、今回の熊本地震を受けて災害時に対応できる道路としても早期の開通が期待されています。",
                "en": "Also, regarding future changes to transport routes, many operators said there would be no change, but 13.3 percent answered that \"use of Oita Port will increase.\" This fiscal year, the 6-kilometer section of the \"Takimurozaka Road,\" located on the prefectural border between Oita and Kumamoto and considered the most difficult section, will open. Along with the ripple effects of TSMC's entry, early opening is also expected because the road can be used for disaster response following this Kumamoto earthquake.",
                "literal": "另外，关于今后运输路线的变化，虽然多数业者回答不会改变，但有13.3%回答“大分港的使用将增加”。本年度，位于大分与熊本县界、被认为最难路段的“泷室坂道路”6公里区间将开通。与TSMC进驻的波及效应一起，由于这次熊本地震后作为灾害时能应对的道路，早期开通也备受期待。",
                "grammar": "「〜ものの」— 虽然…但是…。例：多いものの（虽然多）。\n「〜とともに」— 与…一起。例：波及効果とともに（与波及效应一起）。\n「〜が期待されています」— …备受期待。例：早期の開通が期待されています（早期开通备受期待）。",
                "vocab": [["ルート", "るーと", "路线"], ["県境", "けんざかい", "县界"], ["難所", "なんしょ", "难行路段、难关"], ["区間", "くかん", "区间"], ["波及効果", "はきゅうこうか", "波及效应"], ["災害時", "さいがいじ", "灾害时"]]
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
