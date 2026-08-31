#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-09-01 (Tue) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-09-01'
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
        "slug": "ise-meirin-shotengai-taika",
        "title": "伊勢神宮近くで火事 戦後まもなく誕生した『明倫商店街』ほぼ全焼か",
        "subtitle": "from テレビ朝日系（ANN）",
        "paras": [
            {
                "ja": "三重県の伊勢神宮のほど近く、宇治山田駅前の商店街で31日午後、大規模な火事がありました。戦後間もないころから続く地域密着の商店街は、ほぼ全てが焼け落ちてしまいました。何台もの消防車両が駆け付け、はしご車が高く伸びる中、商店街のメインゲートの入口の方にまで炎が広がっていました。",
                "en": "A large fire broke out on the afternoon of the 31st in a shopping street near the Ujiyamada Station, not far from Ise Jingu in Mie Prefecture. The community-rooted shopping street, which had continued since soon after the war, was almost completely burned down. As many fire engines rushed in and a ladder truck extended high, the flames had spread as far as the entrance of the shopping street's main gate.",
                "literal": "在三重县伊势神宫附近、宇治山田车站前的商店街，31日下午发生了大规模火灾。从战后不久就延续下来的扎根社区的商店街，几乎全部烧毁。多辆消防车辆赶到、云梯车高高升起的同时，火势已蔓延到商店街主入口附近。",
                "grammar": "「〜のほど近く」— 离…不远的地方。例：伊勢神宮のほど近く（离伊势神宫不远）。\n「〜駆け付ける」— 匆忙赶到。例：消防車両が駆け付け（消防车辆赶到）。\n「〜中」— 在…过程中。例：はしご車が高く伸びる中（云梯车高高升起之时）。",
                "vocab": [["大規模", "だいきぼ", "大规模"], ["焼け落ちる", "やけおちる", "烧毁、烧塌"], ["地域密着", "ちいきみっちゃく", "扎根社区、贴近地区"], ["消防車両", "しょうぼうしゃりょう", "消防车辆"], ["はしご車", "はしごしゃ", "云梯车"], ["駆け付ける", "かけつける", "匆忙赶到"]]
            },
            {
                "ja": "現場は、伊勢神宮の外宮にも近い、近鉄宇治山田駅の目の前にある『明倫商店街』。かつて商店街のすぐ側にはプロ野球黎明期を支えた沢村栄治さんの生家がありました。巨人のエースとして活躍し、史上初のノーヒットノーランを達成。沢村賞にその名を残す伝説の名投手です。",
                "en": "The site is the 'Meirin Shopping Street,' right in front of the Kintetsu Ujiyamada Station, also near the outer shrine of Ise Jingu. Once, right beside the shopping street stood the birthplace of Eiji Sawamura, who supported the early days of professional baseball. He was a legendary ace pitcher who starred for the Giants, achieved the first no-hitter no-run game in history, and left his name on the Sawamura Award.",
                "literal": "现场是靠近伊势神宫外宫、位于近铁宇治山田站正前方的『明伦商店街』。以前商店街旁边就是支撑职棒黎明期、泽村荣治的故居。他作为巨人队的王牌活跃，达成史上首次无安打无失分比赛。是留名泽村奖的传奇王牌投手。",
                "grammar": "「〜も近い」— 也靠近…。例：外宮にも近い（也靠近外宫）。\n「〜目の前」— …眼前、正前方。例：駅の目の前（车站正前方）。\n「〜として活躍」— 作为…而活跃。例：巨人のエースとして活躍（作为巨人队王牌活跃）。",
                "vocab": [["外宮", "げくう", "外宫（伊势神宫）"], ["黎明期", "れいめいき", "黎明期、草创期"], ["生家", "せいか", "故居、出生之家"], ["エース", "えーす", "王牌"], ["ノーヒットノーラン", "のーひっとのーらん", "无安打无失分"], ["伝説", "でんせつ", "传说"]]
            },
            {
                "ja": "どこか懐かしい雰囲気が漂う明倫商店街は、戦後間もない昭和22年に発足。地域密着を掲げる商店街でしたが、来年は80年の節目でした。しかし、わずか数時間で跡形もなく焼け落ちてしまいました。伊勢市では雨の少ない状況が続いていて、30日までの10日間の雨量はわずか0.5ミリでした。午後7時半過ぎ、火はほぼ消し止められましたが、この火事の影響で180戸で停電が起きているといいます。",
                "en": "The Meirin Shopping Street, which exuded somehow a nostalgic atmosphere, was established in Showa 22, soon after the war. It was a shopping street that upheld community ties, and next year would have been its 80th anniversary. However, it burned down without a trace in just a few hours. In Ise City, dry conditions continued, with rainfall over the 10 days through the 30th being only 0.5 millimeters. Shortly after 7:30 p.m. the fire was mostly brought under control, but it is said that the fire caused power outages in 180 households.",
                "literal": "透着几分怀旧氛围的明伦商店街，成立于战后不久的昭和22年。是标榜扎根当地的商店街，明年本应是创立80周年。然而仅短短数小时就被烧得荡然无存。伊势市持续少雨，截至30日的10天雨量仅0.5毫米。傍晚7点半过后火势基本被扑灭，但据报道此次火灾导致180户停电。",
                "grammar": "「〜が漂う」— 飘散着…、透着…。例：懐かしい雰囲気が漂う（透着怀旧氛围）。\n「〜を掲げる」— 高举…、标榜…。例：地域密着を掲げる（标榜扎根地区）。\n「〜跡形もなく」— 毫无痕迹地。例：跡形もなく焼け落ちた（烧得荡然无存）。",
                "vocab": [["漂う", "ただよう", "飘荡、弥漫"], ["発足", "ほっそく", "成立、创办"], ["節目", "ふしめ", "节点、里程碑"], ["跡形もなく", "あとかたちもなく", "毫无痕迹地"], ["雨量", "うりょう", "降雨量"], ["停電", "ていでん", "停电"]]
            }
        ]
    },
    {
        "slug": "mikon-wakamono-kekkon-koete",
        "title": "未婚若者の約3人に1人「結婚するつもりはない」 こども家庭庁 若者10万人調査",
        "subtitle": "from TBS NEWS DIG",
        "paras": [
            {
                "ja": "こども家庭庁は若者を対象にした初めての大規模調査を行い、未婚の若者のおよそ3人に1人が「結婚するつもりはない」と考えていることが調査で明らかになりました。こども家庭庁は今年5月から8月にかけ、15歳から39歳までのおよそ10万人を対象にしたインターネットによる意識調査を行い、7月時点での集計結果を公表しました。",
                "en": "The Children and Families Agency conducted its first large-scale survey of young people, and it was revealed that roughly one in three unmarried young people think 'I have no intention of getting married.' From May through August this year, the agency conducted an internet-based attitude survey of about 100,000 people aged 15 to 39, and published the aggregate results as of July.",
                "literal": "儿童家庭厅实施了以年轻人为对象的首次大规模调查，结果查明约有3分之一的未婚年轻人认为「不打算结婚」。儿童家庭厅从今年5月到8月，以15岁至39岁约10万人为对象进行网络意识调查，并公布了截至7月的汇总结果。",
                "grammar": "「〜こと」— …这一点（名词化）。例：考えていることが明らかになった（查明考虑…这一点）。\n「〜にかけ」— 从…到…（期间）。例：5月から8月にかけ（从5月到8月）。\n「〜を対象にした」— 以…为对象。例：約10万人を対象にした調査（以约10万人为对象的调查）。",
                "vocab": [["対象", "たいしょう", "对象"], ["大規模", "だいきぼ", "大规模"], ["未婚", "みこん", "未婚"], ["意識調査", "いしきちょうさ", "意识调查、民意调查"], ["集計", "しゅうけい", "汇总、统计"], ["公表", "こうひょう", "公布"]]
            },
            {
                "ja": "調査によりますと、未婚の若者の35.1％が「結婚するつもりはない」と回答しました。一方、「いずれは結婚したい」と答えた人は37.5％でした。結婚のハードルを聞いたところ、「安定した結婚生活を送れる収入への不安」が40％と最も多く、次いで「自由な時間がなくなる・趣味時間の短縮」が34.4％、「結婚したいと思える人がいない」が32.6％となっています。",
                "en": "According to the survey, 35.1% of unmarried young people answered that they have no intention of getting married. On the other hand, 37.5% said they want to get married eventually. When asked about the hurdles to marriage, 'anxiety about income to sustain a stable married life' was the highest at 40%, followed by 'losing free time / shorter hobby time' at 34.4%, and 'no one I feel I want to marry' at 32.6%.",
                "literal": "据调查显示，未婚年轻人中有35.1%回答「不打算结婚」。另一方面，回答「早晚想结婚」的人为37.5%。问及结婚的门槛时，「对能否过上稳定婚后生活的不安」占40%为最多，其次是「自由时间减少・爱好时间缩短」占34.4%，「没有想结婚的人」占32.6%。",
                "grammar": "「〜によりますと」— 据…（来源）。例：調査によりますと（据调查）。\n「一方」— 另一方面。例：一方、いずれは結婚したい（另一方面，早晚想结婚）。\n「〜ところ」— 问（之后结果）…。例：ハードルを聞いたところ（问门槛后…）。",
                "vocab": [["回答", "かいとう", "回答"], ["いずれ", "いずれ", "早晚、迟早"], ["ハードル", "はーどる", "障碍、门槛"], ["安定", "あんてい", "稳定"], ["収入", "しゅうにゅう", "收入"], ["短縮", "たんしゅく", "缩短"]]
            },
            {
                "ja": "また、政府は年齢によるSNSの利用制限について議論を続けていますが、「一定年齢以下のこどもは、SNSの利用を制限する必要がある」と答えた人は、年代・性別にかかわらず、5割を超えたということです。こども家庭庁は今年度末までに最終報告書をまとめる予定で、「若者の実態や支援ニーズを捉え、少子化対策などの施策に活かしたい」としています。",
                "en": "Also, the government continues to discuss age-based restrictions on SNS use, but more than half of respondents, regardless of age or gender, said that 'there is a need to restrict SNS use for children under a certain age.' The Children and Families Agency plans to compile a final report by the end of this fiscal year, stating that it wants to 'capture the actual situation and support needs of young people and use them in measures such as countermeasures against the declining birthrate.'",
                "literal": "另外，政府就基于年龄的SNS使用限制持续讨论，但无论年代・性别，答「有必要限制一定年龄以下儿童使用SNS」的人超过5成。儿童家庭厅计划在本年度末前汇总最终报告书，并表示「希望掌握年轻人的实际情况和支持需求，运用到少子化对策等施策中」。",
                "grammar": "「〜にかかわらず」— 无论…、不管…。例：年代・性別にかかわらず（无论年代性别）。\n「〜ということです」— 据说…（传闻）。例：5割を超えたということです（据说超过5成）。\n「〜に活かす」— 运用…于…。例：施策に活かしたい（希望用于施策）。",
                "vocab": [["利用制限", "りようせいげん", "使用限制"], ["一定", "いってい", "一定、固定"], ["かかわらず", "かかわらず", "无论、不管"], ["最終報告書", "さいしゅうほうこくしょ", "最终报告书"], ["実態", "じったい", "实际情况"], ["少子化対策", "しょうしかたいさく", "少子化对策"]]
            }
        ]
    },
    {
        "slug": "kankoku-mizu-kutsujoku-kenen",
        "title": "日本の地震被害に支援したのに…「韓国産の水は水洗トイレに」 侮辱コメントに物議",
        "subtitle": "from 中央日報日本語版",
        "paras": [
            {
                "ja": "地震被害で困難な状況にある熊本に韓国企業が飲料水や生活必需品を支援する中、一部の日本人がソーシャルメディア（SNS）で韓国産の水はトイレの水にでも使うべきだという趣旨の侮辱的なコメントをして物議を醸しています。最近、大韓航空はマグニチュード（M）7.1の地震で被害を受けた熊本に対し、1.5リットル入りの飲料水1000箱、計1万2000本を支援しました。",
                "en": "While Korean companies are supporting Kumamoto, which is in a difficult situation due to earthquake damage, with drinking water and daily necessities, some Japanese people have made insulting comments on social media (SNS) suggesting that Korean-made water should be used even for toilet water, causing controversy. Recently, Korean Air supported Kumamoto, which suffered damage in a magnitude 7.1 earthquake, with 1,000 boxes of 1.5-liter drinking water, totaling 12,000 bottles.",
                "literal": "在地震灾害中处境困难的熊本，韩国企业正支援饮用水和生活必需品之际，一部分日本人在社交媒体（SNS）上发表了「韩国产的水该用于马桶水」这类侮辱性言论，引发争议。最近，大韩航空向遭受M7.1地震灾害的熊本支援了1.5升装饮用水1000箱、共计1万2000瓶。",
                "grammar": "「〜中」— 在…之际、正当…。例：支援する中（在支援之际）。\n「〜という趣旨の」— 大意是…的。例：水にでも使うべきだという趣旨（大意是「该用于水（马桶）」）。\n「〜でも」— 即便…也（举例）。例：トイレの水にでも（即便用于马桶水）。",
                "vocab": [["支援", "しえん", "支援、援助"], ["生活必需品", "せいかつひつじゅひん", "生活必需品"], ["侮辱", "ぶじょく", "侮辱"], ["物議を醸す", "ぶつぎをかもす", "引发争议"], ["マグニチュード", "まぐにちゅーど", "震级"], ["飲料水", "いんりょうすい", "饮用水"]]
            },
            {
                "ja": "ところが4日、ある日本人ネットユーザーは大韓航空による飲料水支援の投稿を共有し、「被災者じゃ無いけど、正直 韓国産の水なんて飲みたく無い。使用用途は、水洗トイレの水しか思いつかない」と投稿し、議論を呼んでいます。これを見た韓国のインターネット上は、「支援してくれた国に対してどうしてそんなことが言えるのか」と、そのコメントを投稿したネットユーザーを批判しています。",
                "en": "However, on the 4th, a certain Japanese internet user shared the post about Korean Air's drinking-water support and posted, 'I'm not a victim, but honestly I don't want to drink Korean-made water. The only use I can think of is water for the flush toilet,' stirring up debate. On the Korean internet, people who saw this criticized the user who posted the comment, saying, 'How can you say such things toward a country that offered support?'",
                "literal": "然而4日，一名日本网民转发了大韩航空饮用水支援的帖子，并上传「虽然不是受灾者，但说实话不想喝韩国产的水。用途只能想到是抽水马桶的水」，引发议论。看到此事的韩国网络上，「对支援过的国家怎能说出这种话」，纷纷谴责发布此评论的网民。",
                "grammar": "「〜ところが」— 然而、可是。例：ところが4日、…（然而4日…）。\n「〜しか〜ない」— 只有…、只能…。例：水しか思いつかない（只能想到水）。\n「〜に対して」— 对…、针对…。例：支援してくれた国に対して（对提供支援的国家）。",
                "vocab": [["ネットユーザー", "ねっとゆーざー", "网民"], ["共有", "きょうゆう", "转发、分享"], ["被災者", "ひさいしゃ", "受灾者"], ["使用用途", "しようようと", "使用用途"], ["水洗トイレ", "すいせんといれ", "抽水马桶"], ["批判", "ひはん", "批评、谴责"]]
            },
            {
                "ja": "別の日本人ネットユーザーは、「支援を受けるのが嫌なら、何も言わず黙っていればいい。プライドが傷ついてあんなことを言っているのか。いまだに帝国主義的な優越意識にとらわれている情けない日本人だ」とした上で、「私が韓国の皆さんに代わって頭を下げたい」と投稿しました。一方、先月28日に熊本で発生したM7.1の地震により、これまでに38人の死亡が確認されています。",
                "en": "Another Japanese internet user posted, 'If you don't want to receive support, you should just stay quiet without saying anything. Are you saying that because your pride is hurt? You are a pitiful Japanese person still trapped in an imperialistic sense of superiority,' adding, 'I want to bow my head on behalf of the people of Korea.' Meanwhile, 38 deaths have so far been confirmed from the M7.1 earthquake that occurred in Kumamoto on the 28th of last month.",
                "literal": "另一位日本网民表示「如果不想接受支援，什么也不说保持沉默就好。是因为自尊受损才说那种话吗。是至今仍被帝国主义式优越感所束缚的可悲日本人」，接着投稿「我想代替韩国各位低头道歉」。另一方面，上个月28日熊本发生的M7.1地震，至今已确认38人死亡。",
                "grammar": "「〜黙っていればいい」— 保持沉默就好了。例：黙っていればいい（沉默就好）。\n「〜とした上で」— 先…之后（再）。例：投稿した上で（说明之后）。\n「〜に代わって」— 代替…。例：韓国の皆さんに代わって（代替韩国的各位）。",
                "vocab": [["黙る", "だまる", "沉默、不作声"], ["プライド", "ぷらいど", "自尊心"], ["優越意識", "ゆうえついしき", "优越感"], ["とらわれる", "とらわれる", "被束缚、受困于"], ["情けない", "なさけない", "可悲的、丢人的"], ["頭を下げる", "あたまをさげる", "低头道歉"]]
            }
        ]
    },
    {
        "slug": "messi-daibyou-intai-sengen",
        "title": "メッシ、アルゼンチン代表引退を発表「今こそが“その時”だ」",
        "subtitle": "from GOAL",
        "paras": [
            {
                "ja": "FWリオネル・メッシ（39）が31日、アルゼンチン代表を引退することを発表しました。先の北中米ワールドカップ（W杯）では、決勝でスペインに敗れて大会連覇を逃したメッシ。その後、父親の逝去という出来事にも直面した同選手は、SNSを通じてメッセージを記しています。「辛い決断だった。魂まで痛む決断だけど、今こそが“その時”なんだと思っている」。",
                "en": "Forward Lionel Messi (39) announced on the 31st that he is retiring from the Argentina national team. In the recent CONCACAF World Cup, Messi lost in the final to Spain and missed out on a consecutive tournament title. Afterward, facing also the passing of his father, the player wrote a message through SNS. 'It was a painful decision. It is a decision that hurts to the very soul, but I believe that now is the time.'",
                "literal": "前锋里奥内尔·梅西（39岁）31日宣布退出阿根廷国家队。在此前的中北美世界杯中，梅西在决赛负于西班牙，错失夺冠连霸。此后，同样面临父亲去世这一事件的梅西，通过SNS写下留言。「这是痛苦的决断。虽然痛彻心扉，但我认为如今正是『那个时刻』」。",
                "grammar": "「〜を引退する」— 退出…、退役…。例：代表を引退する（退出国家队）。\n「〜を逃す」— 错过…。例：大会連覇を逃した（错过连霸）。\n「〜に直面する」— 面临…。例：逝去に直面した（面临去世）。",
                "vocab": [["引退", "いんたい", "引退、退役"], ["決勝", "けっしょう", "决赛"], ["連覇", "れんぱ", "连冠、蝉联"], ["逝去", "せいきょ", "去世、逝世"], ["直面", "ちょくめん", "直面、面临"], ["痛む", "いたむ", "疼痛"]]
            },
            {
                "ja": "「僕はずっとこのユニフォームのために戦い、すべてを出し尽くしてきたんだ。みんなに喜びを届けるために、サッカーを通じて、自分たちがアルゼンチン人であることを誇りに感じてもらうために、ね」「残された時間はわずかだ。僕は自分のすべてを注ぎ込み、これ以上与えられるものはもう何も残っていないんだ」。メッシは2005年8月にアルゼンチンのフル代表でデビューし、2021年のコパ・アメリカ、2022年のカタールW杯、2024年のコパ・アメリカで優勝を果たしました。",
                "en": "'I have always fought for this uniform and given everything I had. To bring everyone joy, and so that through soccer people feel proud to be Argentines.' 'The time left for me is short. I poured everything of myself in, and there is nothing more I can give.' Messi debuted for Argentina's senior national team in August 2005, and won the Copa América in 2021, the Qatar World Cup in 2022, and the Copa América again in 2024.",
                "literal": "「我一直为这件球衣而战，倾尽了一切。为了把喜悦带给每个人，为了通过足球让大家以身为阿根廷人为傲」「剩余的时间不多了。我已倾注了自己的一切，再也没有更多可以给予的了」。梅西于2005年8月在阿根廷成年国家队出道，2021年美洲杯、2022年卡塔尔世界杯、2024年美洲杯均夺得冠军。",
                "grammar": "「〜出し尽くす」— 用尽、倾尽。例：すべてを出し尽くしてきた（倾尽了一切）。\n「〜を誇りに感じる」— 以…为荣。例：誇りに感じてもらう（让人感到自豪）。\n「〜注ぎ込む」— 倾注、投入。例：すべてを注ぎ込み（倾注一切）。",
                "vocab": [["ユニフォーム", "ゆにふぉーむ", "球衣、队服"], ["誇り", "ほこり", "自豪、骄傲"], ["注ぎ込む", "そそぎこむ", "倾注、注入"], ["デビュー", "でびゅー", "出道、首次亮相"], ["優勝", "ゆうしょう", "夺冠、优胜"], ["わずか", "わずか", "仅有、少许"]]
            },
            {
                "ja": "クラブレベルで多くのタイトルに恵まれた同選手は、代表チームでは長く優勝と縁のない日々を送りましたが、2021年以降にタイトルを重ね、アルゼンチン代表としての通算記録は207試合125ゴール68アシスト。歴代最多得点、最多出場記録を保持しています。現役生活最後とも言われる大会での敗退後、深い悲しみとともに、この決断への確信をさらに深めた様子です。",
                "en": "Blessed with many titles at the club level, the player spent a long time without a title for the national team, but from 2021 onward he piled up titles, and his overall record for the Argentina national team is 207 matches, 125 goals, and 68 assists, holding records for the most goals and most appearances in history. After being eliminated in a tournament that was said to be possibly the last of his active career, he appears to have deepened his conviction in this decision along with deep sadness.",
                "literal": "在俱乐部层面获得众多冠军的梅西，在国家队却长期与冠军无缘，但2021年以后接连夺冠，作为阿根廷国家队的总成绩为207场125球68助攻，保持着历史最多进球、最多出场纪录。在被称为可能是职业生涯最后的赛事中被淘汰后，他似乎在深深的悲伤中，进一步加深了对这个决断的确信。",
                "grammar": "「〜に恵まれた」— 深受…眷顾、拥有很多…。例：多くのタイトルに恵まれた（拥有众多冠军）。\n「〜と縁のない」— 与…无缘的。例：優勝と縁のない日々（与冠军无缘的日子）。\n「〜と言われる」— 被称为…。例：最後とも言われる大会（被称为最后的赛事）。",
                "vocab": [["タイトル", "たいとる", "冠军、头衔"], ["功績", "こうせき", "功绩"], ["アシスト", "あしすと", "助攻"], ["歴代", "れきだい", "历代、历来"], ["敗退", "はいたい", "落败、淘汰"], ["確信", "かくしん", "确信、坚定信念"]]
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
