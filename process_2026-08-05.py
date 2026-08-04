#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-05 (Wed) Edition"""
import json, os, subprocess, re, time
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-05'
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
# TODAY'S ARTICLES — 2026-08-05
# ==================================================================
articles = []
articles += [
    {
        "slug": "takeda-shinichi-tenkin",
        "title": "武田真一アナ、NHK時代の5度の転勤を回想 「会社が一方的に働く場所を決める時代」に転機",
        "subtitle": "from 読売新聞オンライン",
        "paras": [
            {
                "ja": "武田は2023年にNHKを退局し、フリーに転身した。NHK時代は、熊本放送局を振り出しに、東京、沖縄、大阪など5度の転勤を経験した。様々な出会いを得る一方で、単身赴任生活は計3年間になった。「転勤は人生を豊かにしてくれたが、組織の一員として悲哀も感じた」と明かす。",
                "en": "Takeda left NHK in 2023 and became a freelancer. During his NHK years, he experienced five transfers, starting at the Kumamoto Broadcasting Station, then Tokyo, Okinawa, Osaka, and elsewhere. While he gained various encounters, his solo postings away from family totaled three years. He revealed, \"Transfers enriched my life, but I also felt sorrow as a member of an organization.\"",
                "literal": "武田于2023年从NHK退职，转为了自由职业者。在NHK时代，以熊本广播局为起点，经历了东京、冲绳、大阪等5次调动。一方面获得了各种相遇，另一方面单身赴任生活共计达到3年。「调动虽然丰富了我的人生，但作为组织的一员也感受到了悲哀」他这样透露。",
                "grammar": "「〜を振り出しに」— 以…为起点、开端。例：熊本放送局を振り出しに5度の転勤を経験した（以熊本广播局为起点经历了5次调动）。\n「〜一方で」— 一方面…另一方面…。例：様々な出会いを得る一方で（一方面获得各种相遇）。\n「〜と明かす」— 透露、表明…。例：悲哀も感じたと明かす（透露也感受到了悲哀）。",
                "vocab": [
                    ["退局", "たいきょく", "离开电视台（退职）"],
                    ["転身", "てんしん", "转行、改行"],
                    ["振り出し", "ふりだし", "起点、开端"],
                    ["単身赴任", "たんしんふにん", "单身赴任"],
                    ["悲哀", "ひあい", "悲哀"],
                    ["明かす", "あかす", "透露、坦白"]
                ]
            },
            {
                "ja": "一方で、子どもが転校を迫られるなど「家族が築いてきた学校や地域とのつながりが断たれることは心の重荷になった」。大阪放送局時代は2年間の単身赴任生活を送った。その際、大阪市内でふとみかけた看板が忘れられない。「Why are you here？（なぜここにいるのか）」と書かれていた。「『なぜ』と言われても、会社の命令だよ」。そうつぶやいた後、涙が出そうになったという。",
                "en": "On the other hand, he said, \"Having my children forced to change schools and having the ties to schools and communities that my family had built severed became a heavy burden on my heart.\" During his Osaka posting, he lived alone for two years. A sign he happened to see in Osaka City at that time is unforgettable. It read, \"Why are you here?\" \"Even if you ask 'why,' it's the company's order,\" he muttered — and he says he nearly burst into tears.",
                "literal": "另一方面，孩子被迫转学等，「与家人建立起来的学校和地区的联系被切断，成了心中的重担」。在大阪广播局时代度过了2年的单身赴任生活。那时，在大阪市内偶然看到的招牌令人难忘。上面写着「Why are you here？（为什么你在这里）」。他嘟囔说「就算被问『为什么』，那也是公司的命令」。据说嘟囔完之后，差点流出眼泪。",
                "grammar": "「〜を迫られる」— 被迫…。例：転校を迫られる（被迫转学）。\n「〜と書かれていた」— 上面写着…（被动）。例：看板に書かれていた（招牌上写着）。\n「〜そうになった」— 差点就…。例：涙が出そうになった（差点哭出来）。",
                "vocab": [
                    ["転校", "てんこう", "转学"],
                    ["築いてきた", "きずいてきた", "建立起来的"],
                    ["断たれる", "たたれる", "被切断、被断绝"],
                    ["重荷", "おもに", "重担、负担"],
                    ["ふと", "ふと", "偶然、无意中"],
                    ["つぶやく", "つぶやく", "嘟囔、自言自语"]
                ]
            },
            {
                "ja": "初任地の熊本放送局時代に、高校の同級生だった妻と結婚した。最初の松山放送局への転勤時、妻は地元紙を退職して同行してくれた。5度の転勤では、社宅で同僚家族とバーベキューを楽しみ、地域の人から「テレビ見たよ」と声をかけられた。「地方勤務を嫌だと感じたことはなく、人生の財産だと思っている」と振り返る。",
                "en": "During his first posting at the Kumamoto Broadcasting Station, he married his wife, who had been his high school classmate. When he was first transferred to the Matsuyama station, his wife quit her job at a local newspaper to accompany him. Through his five transfers, he enjoyed barbecues with colleagues' families in company housing and was greeted by locals saying, \"I saw you on TV.\" He looks back, saying, \"I never disliked working in regional areas; I consider it a treasure of my life.\"",
                "literal": "在最初任职地的熊本广播局时代，与高中同学时代的妻子结了婚。第一次调往松山广播局时，妻子辞去地方报纸的工作陪同前往。在5次调动中，在公司住宅里与同事家人享受烧烤，被当地人说「在电视上看到你了」。「从未觉得地方勤务讨厌，我认为那是人生的财产」他这样回顾。",
                "grammar": "「〜時」— …的时候。例：転勤時、妻は同行してくれた（调动时，妻子陪同前往）。\n「〜てくれた」— （别人）为我做…。例：同行してくれた（陪我一起去了）。\n「〜と振り返る」— 回顾说…。例：財産だと思っていると振り返る（回顾说认为是财产）。",
                "vocab": [
                    ["初任地", "しょにんち", "最初的任职地"],
                    ["同級生", "どうきゅうせい", "同班同学"],
                    ["地元紙", "じもとし", "地方报纸"],
                    ["同行", "どうこう", "同行、陪同"],
                    ["社宅", "しゃたく", "公司住宅"],
                    ["振り返る", "ふりかえる", "回顾、回首"]
                ]
            },
            {
                "ja": "共働き世帯が当たり前となり、リモートワークの普及も進む。会社が一方的に「働く場所」を決める時代は転機を迎えつつある。実際、転勤を拒否する若手社員が増え、企業の中には転勤手当を最大100万円に拡充するなど、制度の見直しに動くところも出てきている。",
                "en": "Dual-income households have become the norm, and remote work has spread. The era in which companies unilaterally decide \"where you work\" is now at a turning point. In fact, young employees who refuse transfers are increasing, and some companies are moving to revise their systems, such as expanding transfer allowances up to 1 million yen.",
                "literal": "双职工家庭变得理所当然，远程办公的普及也在推进。公司单方面决定「工作地点」的时代正在迎来转折点。实际上，拒绝调动的年轻员工在增加，企业中也出现了将调动补贴最多扩大到100万日元等、着手修订制度的公司。",
                "grammar": "「〜が当たり前となり」— …变得理所当然。例：共働き世帯が当たり前となり（双职工家庭变得理所当然）。\n「〜つつある」— 正在…（进行中）。例：転機を迎えつつある（正迎来转折点）。\n「〜に出てきている」— 开始出现…。例：動くところも出てきている（开始出现行动的地方）。",
                "vocab": [
                    ["共働き", "ともばたらき", "双职工"],
                    ["当たり前", "あたりまえ", "理所当然"],
                    ["リモートワーク", "りもーとわーく", "远程办公"],
                    ["一方的に", "いっぽうてきに", "单方面地"],
                    ["転機", "てんき", "转折点"],
                    ["拡充", "かくじゅう", "扩充、扩大"]
                ]
            }
        ]
    },
    {
        "slug": "aeon-kumamoto-sainyuukan",
        "title": "イオンモール熊本、避難後になぜ再入館？ 生存した従業員らの証言が浮かび上がらせる実態",
        "subtitle": "from 熊本日日新聞",
        "paras": [
            {
                "ja": "2026年熊本地震後に大規模な爆発が起きた大型商業施設「イオンモール熊本」（嘉島町）では、専門店の従業員7人が犠牲になった。7人はいずれも外に避難した後に館内に戻り、爆発に巻き込まれたとみられる。地震で無事だった命がなぜ失われたのか。イオンは「社員もテナント従業員も避難したら館内には戻らないことになっている」と説明する。しかし、無事だった従業員らの証言からは、ルールが徹底されていなかった実態が浮かび上がる。",
                "en": "At the large commercial facility \"Aeon Mall Kumamoto\" (Kashima Town), where a massive explosion occurred after the 2026 Kumamoto earthquake, seven specialty-store employees lost their lives. All seven are believed to have returned inside the mall after evacuating outside, and were caught up in the explosion. Why were lives that had survived the earthquake lost? Aeon explains, \"The rule is that neither employees nor tenant staff return inside after evacuating.\" However, testimonies from surviving employees reveal that the rule had not been thoroughly enforced.",
                "literal": "在2026年熊本地震后发生大规模爆炸的大型商业设施「永旺商城熊本」（嘉岛町），7名专卖店员工遇难。7人据说都是在外出避难后返回馆内，被卷入爆炸的。在地震中平安无事的生命为什么被夺走了呢？永旺解释说「员工和租户员工都规定避难后不得返回馆内」。但是，从平安无事员工的证言中，浮现出规则没有被彻底贯彻的实际情况。",
                "grammar": "「〜とみられる」— 被认为…。例：爆発に巻き込まれたとみられる（被认为被卷入爆炸）。\n「〜ことになっている」— 规定是…。例：館内には戻らないことになっている（规定不得返回馆内）。\n「〜実態が浮かび上がる」— 浮现出实际情况。例：徹底されていなかった実態が浮かび上がる（浮现出未被彻底贯彻的实情）。",
                "vocab": [
                    ["犠牲", "ぎせい", "牺牲、遇难"],
                    ["いずれも", "いずれも", "全都"],
                    ["巻き込まれる", "まきこまれる", "被卷入"],
                    ["テナント", "てなんと", "租户、入驻商户"],
                    ["徹底", "てってい", "彻底"],
                    ["実態", "じったい", "实际情况"]
                ]
            },
            {
                "ja": "地震は7月28日午後4時27分ごろ発生。2階フードコート近くで働いていた女性（22）はとっさに客を避難誘導した後、自身も北側駐車場に避難した。約45分後、女性は1階北側の出入り口から店舗に戻った。誘導していた男性スタッフから「貴重品がないと帰れない従業員は一緒にまとまって取りに行くように」と言われたからだという。館内は天井が落ちた箇所があり、停電し、スプリンクラーで水浸しになった店舗もあった。「ドーン」。施設の南側中央付近で爆発が起きたのは、避難して数分たった午後5時50分ごろだった。",
                "en": "The earthquake struck around 4:27 p.m. on July 28. A woman (22) working near the second-floor food court guided customers to evacuate on the spot, then evacuated herself to the north parking lot. About 45 minutes later, she returned to her store through a first-floor north entrance. This was because a male staff member who had been guiding people said, \"Employees who can't go home without their valuables should go together as a group to retrieve them.\" Inside, some ceiling sections had fallen, power was out, and some stores were flooded by sprinklers. \"BOOM.\" The explosion occurred near the center of the south side of the facility at around 5:50 p.m., a few minutes after she had evacuated.",
                "literal": "地震于7月28日下午4点27分左右发生。在2楼美食广场附近工作的女性（22岁）当场引导顾客避难后，自己也避到了北侧停车场。约45分钟后，女性从1楼北侧的出入口返回了店铺。据说是因为正在引导的男性工作人员说「没有贵重物品就无法回家的员工，大家一起结伴去取」。馆内有天花板掉落的部位，停电了，也有被喷淋装置泡水的店铺。「咚——」。爆炸发生在避难几分钟后的下午5点50分左右，地点是设施南侧中央附近。",
                "grammar": "「〜とっさに」— 当即、立刻。例：とっさに客を避難誘導した（当即引导顾客避难）。\n「〜ように言われた」— 被要求…。例：貴重品を取りに行くように言われた（被要求去取）。\n「〜があり、〜もあった」— 有…也有…。例：水浸しになった店舗もあった（也有被水淹的店铺）。\n「〜ごろだった」— 是…左右（时间）。例：午後5時50分ごろだった（是下午5点50分左右）。",
                "vocab": [
                    ["とっさに", "とっさに", "当即、立刻"],
                    ["避難誘導", "ひなんゆうどう", "引导避难"],
                    ["貴重品", "きちょうひん", "贵重物品"],
                    ["停電", "ていでん", "停电"],
                    ["水浸し", "みずびたし", "泡水、水淹"],
                    ["巻き込む", "まきこむ", "卷入"]
                ]
            },
            {
                "ja": "「館内に戻っていいとアナウンスしたのか」。地震の翌29日、記者会見したイオンの吉田昭夫社長は報道陣の問いに「一切ございません。明確に否定しておきます」と強調した。しかし、イオン側の見解とは異なる証言が相次ぐ。2階の雑貨店で働いていた大竹玖瑠美さん（22）は、売上金を金庫に戻すため館内に戻り、爆発に巻き込まれて亡くなった。店の運営会社「ハビタ」は、大竹さんらに館内に戻るよう指示を出したとして遺族に謝罪した。",
                "en": "\"Did you announce that it was okay to return inside?\" At a press conference the next day, the 29th, Aeon President Akio Yoshida stressed to reporters, \"We made no such announcement at all. I clearly deny it.\" However, testimonies contradicting Aeon's account are coming one after another. Kurumi Otake (22), who worked at a general goods store on the second floor, returned inside to put the day's sales in the safe and died in the explosion. The store's operating company, Habita, apologized to the bereaved family, admitting that it instructed Otake and others to return inside.",
                "literal": "「有没有广播说可以返回馆内？」。地震翌日的29日，召开记者会的永旺社长吉田昭夫面对记者的提问强调说「完全没有。我明确予以否认」。但是，与永旺方面的说法不同的证言接连出现。在2楼杂货店工作的大竹玖瑠美（22岁）为了把营业收入放回金库而返回馆内，被卷入爆炸身亡。店铺运营公司「哈比塔」因向大竹等人下达了返回馆内的指示而向遗属道歉。",
                "grammar": "「〜とアナウンスしたのか」— 是广播了…吗。例：館内に戻っていいとアナウンスしたのか（广播了可以回馆内吗）。\n「〜として」— 作为…、以…的身份。例：指示を出したとして謝罪した（以发出了指示为由道歉）。\n「〜ように指示を出した」— 下达了…的指示。例：館内に戻るよう指示を出した（下达了返回馆内的指示）。",
                "vocab": [
                    ["アナウンス", "あなうんす", "广播、通告"],
                    ["明確に", "めいかくに", "明确地"],
                    ["否定", "ひてい", "否定、否认"],
                    ["見解", "けんかい", "见解、看法"],
                    ["相次ぐ", "あいつぐ", "接连不断"],
                    ["遺族", "いぞく", "遗属"]
                ]
            }
        ]
    },
    {
        "slug": "keikan-happa-kawachinagano",
        "title": "警察官が刃物持った男に発砲、男は搬送先で死亡 大阪・河内長野市",
        "subtitle": "from 読売テレビ",
        "paras": [
            {
                "ja": "4日午後、大阪府河内長野市で警察官が刃物を持った男に拳銃を発砲しました。銃弾は男に当たり、病院に搬送されましたが、死亡が確認されました。警察によりますと、現場は河内長野市木戸西町で、4日午後7時ごろ「包丁を持った血だらけの男がスーパーの出入り口付近で暴れている」と110番通報がありました。",
                "en": "On the afternoon of the 4th, a police officer fired a handgun at a man holding a blade in Kawachinagano City, Osaka Prefecture. The bullet struck the man, who was taken to a hospital, where his death was confirmed. According to police, the scene was in Kidonishimachi, Kawachinagano City; around 7 p.m. on the 4th, a call to 110 reported, \"A man covered in blood holding a kitchen knife is causing a disturbance near the supermarket entrance.\"",
                "literal": "4日下午，在大阪府河内长野市，警察向手持刀具的男子开枪。子弹击中男子，被送往医院，但确认死亡。据警方称，现场是河内长野市木户西町，4日下午7点左右接到了110报警，称「持刀浑身是血的男子在超市出入口附近闹事」。",
                "grammar": "「〜によりますと」— 据…称。例：警察によりますと（据警方称）。\n「〜ごろ」— …左右（时间）。例：午後7時ごろ（下午7点左右）。\n「〜と110番通報がありました」— 接到了…的110报警。例：暴れていると110番通報がありました（接到闹事的110报警）。",
                "vocab": [
                    ["刃物", "はもの", "刀具、利器"],
                    ["拳銃", "けんじゅう", "手枪"],
                    ["発砲", "はっぽう", "开枪、射击"],
                    ["搬送", "はんそう", "运送（伤员）"],
                    ["血だらけ", "ちだらけ", "浑身是血"],
                    ["通報", "つうほう", "报警、通报"]
                ]
            },
            {
                "ja": "複数の警察官が駆けつけたところ、男が刃物を向けてきたことから、男性巡査部長（32）が「刃物を捨てろ」と警告した上で、上空に拳銃で1発、威嚇射撃したということです。その後も男は向かってきたため、巡査部長はもう1発発砲して、男の左胸に弾が命中したということです。",
                "en": "When multiple police officers rushed to the scene, the man turned his blade toward them, so a male sergeant (32) warned, \"Drop the knife,\" and then fired one warning shot into the air with his handgun. The man kept coming at them, so the sergeant fired another shot, which struck the man in the left chest.",
                "literal": "多名警察赶到后，因为男子举刀相向，男性警长（32岁）警告「把刀放下」之后，朝空中用手枪开了一枪进行鸣枪警告。据说之后男子仍然扑过来，警长又开了一枪，子弹命中了男子的左胸。",
                "grammar": "「〜たところ」— 一…就…、当…时。例：駆けつけたところ、男が刃物を向けてきた（赶到时，男子举刀相向）。\n「〜た上で」— 在…之后。例：警告した上で、威嚇射撃した（警告之后鸣枪）。\n「〜ため」— 因为…。例：向かってきたため、もう1発発砲した（因为扑了过来，又开了一枪）。",
                "vocab": [
                    ["駆けつける", "かけつける", "赶到、急忙前往"],
                    ["巡査部長", "じゅんさぶちょう", "警长"],
                    ["警告", "けいこく", "警告"],
                    ["威嚇射撃", "いかくしゃげき", "鸣枪警告、威慑射击"],
                    ["命中", "めいちゅう", "命中"],
                    ["左胸", "ひだりむね", "左胸"]
                ]
            },
            {
                "ja": "警察は男を公務執行妨害と銃刀法違反の疑いで現行犯逮捕しました。男は病院に搬送されましたが、死亡が確認されました。警察官にけがはなく、ほかに巻き込まれた人もいませんでした。警察は男の身元や当時の詳しい状況を調べています。また、拳銃の使用については「発砲の要件は満たしていると思うが、詳しくは調査中」としています。",
                "en": "Police arrested the man on the spot on suspicion of obstructing official duties and violating the Swords and Firearms Control Law. The man was transported to the hospital, but his death was confirmed. No officers were injured, and no one else was caught up in the incident. Police are investigating the man's identity and the detailed circumstances at the time. Regarding the use of the handgun, they stated, \"We believe the requirements for firing were met, but the details are under investigation.\"",
                "literal": "警方以妨害公务和违反刀枪法的嫌疑现行逮捕了男子。男子被送往医院，但确认死亡。警察没有受伤，也没有其他被卷入的人。警方正在调查男子的身份和当时的详细情况。另外，关于手枪的使用，「认为满足开枪的要件，但详情正在调查中」。",
                "grammar": "「〜の疑いで」— 以…的嫌疑。例：銃刀法違反の疑いで逮捕（以违反刀枪法的嫌疑逮捕）。\n「〜現行犯逮捕」— 现行犯逮捕（当场逮捕）。例：現行犯逮捕しました（当场逮捕了）。\n「〜としています」— 表示…、主张…。例：調査中としています（表示正在调查）。",
                "vocab": [
                    ["公務執行妨害", "こうむしっこうぼうがい", "妨害公务"],
                    ["銃刀法", "じゅうとうほう", "刀枪法（枪支刀具管制法）"],
                    ["現行犯", "げんこうはん", "现行犯"],
                    ["身元", "みもと", "身份、来历"],
                    ["要件", "ようけん", "要件、必要条件"],
                    ["調査中", "ちょうさちゅう", "调查中"]
                ]
            }
        ]
    },
    {
        "slug": "ichou-54pon-kareru",
        "title": "名物イチョウ54本が一斉に枯れる 原因は伐採時の除草剤、根がつながっていた 東京・町田",
        "subtitle": "from FNNプライムオンライン",
        "paras": [
            {
                "ja": "東京・町田市の住宅街を走る「団地いちょう通り」で思わぬ事態が起きました。通りの名前にもなっている名物のイチョウの木が、一斉に枯れてしまったのです。発覚は近隣住民からの通報でした。市が調査したところ、約870メートルにわたり、イチョウの木54本が枯れているのが確認されました。毎年秋にはきれいな黄色に染まり、街ゆく人に季節のうつろいをつげていたイチョウ。一体、何が起きたのでしょうか。",
                "en": "An unexpected situation occurred on \"Danchi Icho-dori\" street running through a residential area in Machida City, Tokyo. The famous ginkgo trees that gave the street its name have all withered at once. The discovery came from a report by nearby residents. When the city investigated, it confirmed that 54 ginkgo trees had died over a stretch of about 870 meters. Every autumn they turned a beautiful yellow, telling passersby of the changing seasons. What on earth happened?",
                "literal": "在穿过东京・町田市住宅区的「团地银杏大道」，发生了意想不到的事态。成为街道名字由来的名物银杏树，一下子全都枯萎了。发现源于附近居民的通报。市政府调查后发现，约870米范围内确认有54棵银杏树枯萎。每年秋天染成漂亮的黄色、向路人传达季节变迁的银杏。到底发生了什么呢？",
                "grammar": "「〜てしまう」— 表示完了或遗憾。例：枯れてしまったのです（全都枯萎了）。\n「〜たところ」— 一调查发现…。例：市が調査したところ、54本が枯れているのが確認されました（市政府一调查，确认了54棵枯萎）。\n「〜のでしょうか」— 到底…呢。例：何が起きたのでしょうか（到底发生了什么呢）。",
                "vocab": [
                    ["一斉に", "いっせいに", "同时、一齐"],
                    ["枯れる", "かれる", "枯萎、枯死"],
                    ["発覚", "はっかく", "被发现、败露"],
                    ["通報", "つうほう", "通报、举报"],
                    ["うつろい", "うつろい", "变迁、更替"],
                    ["一体", "いったい", "到底、究竟"]
                ]
            },
            {
                "ja": "市によりますと、原因は過去に伐採したイチョウに塗った除草剤でした。2026年2月、道路計画に沿う形で一部のイチョウを伐採。その際、新たな芽が出るのを防ぐための除草剤を切り株の表面に塗っていました。しかし、この切り株の根が、実は周辺のイチョウの根と土の中でつながっていて、除草剤が他の木にも広がり、枯れてしまったとみられています。",
                "en": "According to the city, the cause was herbicide applied to ginkgo trees that had been cut down in the past. In February 2026, some ginkgo trees were felled in line with a road plan. At that time, herbicide was applied to the surface of the stumps to prevent new shoots from sprouting. However, the roots of these stumps were actually connected underground to the roots of surrounding ginkgo trees, and the herbicide is believed to have spread to the other trees, killing them.",
                "literal": "据市政府称，原因是涂在以往采伐的银杏上的除草剂。2026年2月，按照道路规划采伐了一部分银杏。当时，为了防止长出新芽，在树桩表面涂抹了除草剂。但是，这些树桩的根实际上在土壤中与周围的银杏根相连，除草剂被认为扩散到了其他树上，导致枯萎。",
                "grammar": "「〜によりますと」— 据…称。例：市によりますと（据市政府称）。\n「〜に沿う形で」— 按照…的形式。例：道路計画に沿う形で伐採（按照道路规划进行采伐）。\n「〜とみられています」— 被认为…。例：枯れてしまったとみられています（被认为枯萎了）。",
                "vocab": [
                    ["伐採", "ばっさい", "采伐、砍伐"],
                    ["除草剤", "じょそうざい", "除草剂"],
                    ["切り株", "きりかぶ", "树桩、伐根"],
                    ["芽", "め", "芽"],
                    ["広がる", "ひろがる", "扩散、蔓延"],
                    ["つながる", "つながる", "相连、连接"]
                ]
            },
            {
                "ja": "街の人は「木が（下で）つながってるんだってね。だからしょうがないと思った」と話しました。市は今後、イチョウを植え直す方針です。木と木が土の中でつながっていることは専門家の間ではよく知られていますが、今回のように除草剤が広範囲の木に影響した事例は珍しいとみられています。",
                "en": "A local resident said, \"I heard the trees are connected (underground), so I thought there was nothing we could do.\" The city plans to replant ginkgo trees in the future. That trees are connected underground is well known among experts, but cases like this one, where herbicide affected trees over a wide area, are considered rare.",
                "literal": "街上的人说「听说树（在地下）是连着的。所以觉得没办法」。市政府今后计划重新种植银杏。树木在地下相连这一点在专家之间广为人知，但像这次除草剂影响了大范围树木的事例被认为是罕见的。",
                "grammar": "「〜ってね」— 听说…（口语）。例：つながってるんだってね（听说连着呢）。\n「〜しょうがない」— 没办法。例：だからしょうがないと思った（所以觉得没办法）。\n「〜方針です」— 方针是…。例：植え直す方針です（方针是重新种植）。",
                "vocab": [
                    ["植え直す", "うえなおす", "重新种植"],
                    ["方針", "ほうしん", "方针"],
                    ["専門家", "せんもんか", "专家"],
                    ["広範囲", "こうはんい", "大范围"],
                    ["影響", "えいきょう", "影响"],
                    ["事例", "じれい", "事例"]
                ]
            }
        ]
    },
]
articles += [
    {
        "slug": "kome-nouka-akaji",
        "title": "「とんでもない赤字」コメ作りやめる農家も JA福井県が概算金示せない中、ハナエチゼンの収穫始まる",
        "subtitle": "from 福井テレビ",
        "paras": [
            {
                "ja": "この秋、新米がいくらになるのかを気にしているのは、コメを買う消費者だけではありません。福井県内のJAは、コメ農家に前払いする「概算金」をまだ示しておらず、農家も自分のコメがいくらになるのか分かっていません。そんな中、福井市内では4日、早くもハナエチゼンの収穫が始まりました。",
                "en": "This autumn, it's not only consumers buying rice who are worried about how much new rice will cost. Agricultural cooperatives (JA) in Fukui Prefecture have not yet announced the \"provisional payment\" made in advance to rice farmers, so farmers don't know how much their rice will fetch either. Amid this situation, harvesting of Hanaechizen rice began early on the 4th in Fukui City.",
                "literal": "这个秋天，关心新米能卖多少钱的不只是买米的消费者。福井县内的JA还没有公布预先支付给稻农的「概算金」，农民也不知道自己的米能卖多少钱。在这样的情况下，福井市内4日早早地开始了「花越前」大米的收割。",
                "grammar": "「〜を気にしている」— 在意、担心…。例：新米がいくらになるのかを気にしている（担心新米能卖多少钱）。\n「〜ず」— 不…（否定）。例：概算金をまだ示しておらず（还没有公布概算金）。\n「〜そんな中」— 在这样的情况下。例：そんな中、収穫が始まりました（在这种情况下，收割开始了）。",
                "vocab": [
                    ["新米", "しんまい", "新米"],
                    ["前払い", "まえばらい", "预付"],
                    ["概算金", "がいさんきん", "概算金（预付款）"],
                    ["農家", "のうか", "农户、农民"],
                    ["収穫", "しゅうかく", "收割、收获"],
                    ["早くも", "はやくも", "早早地、竟然这么快"]
                ]
            },
            {
                "ja": "福井市のコメ農家・白井清志さんは、約50ヘクタールの田んぼで5つの品種を作っています。ところが今年は、収穫初日の風景が違いました。「去年は6社ぐらいトラックが並んだ。今年は1社も来ない。コメを売ってくれと1社も言うてこない」。「令和の米騒動」とも呼ばれたコメ不足の影響で、多くの集荷業者が農家に殺到した去年から一転、今年は静かな収穫初日を迎えています。",
                "en": "Kiyoshi Shirai, a rice farmer in Fukui City, grows five varieties across about 50 hectares of paddies. But this year, the scene on the first day of harvest was different. \"Last year, trucks from about six companies lined up. This year, not a single one has come. No company has come asking to buy our rice.\" Last year, many grain collectors swarmed farmers due to the rice shortage dubbed the \"Reiwa rice riots\" — but this year has turned around completely, with a quiet first day of harvest.",
                "literal": "福井市的稻农白井清志在约50公顷的田里种植5个品种。但是今年，收割第一天的景象不同了。「去年大约有6家公司的卡车排队。今年一家都不来。没有一家公司来说要买米」。受被称为「令和米骚动」的缺米影响，许多收购商涌向农户的去年截然不同，今年迎来了安静的收割第一天。",
                "grammar": "「〜ところが」— 但是、然而。例：ところが今年は風景が違いました（然而今年景象不同）。\n「〜から一転」— 与…截然转变。例：殺到した去年から一転（与涌来的去年截然不同）。\n「〜を迎えています」— 迎来…。例：静かな収穫初日を迎えています（迎来了安静的收割首日）。",
                "vocab": [
                    ["品種", "ひんしゅ", "品种"],
                    ["集荷業者", "しゅうかぎょうしゃ", "收购商、集货商"],
                    ["殺到", "さっとう", "蜂拥而至"],
                    ["一転", "いってん", "截然转变"],
                    ["米騒動", "こめそうどう", "米骚动、抢米风潮"],
                    ["並ぶ", "ならぶ", "排队、排列"]
                ]
            },
            {
                "ja": "5月の田植えから数カ月、白井さんの支出はすでに決まっています。白井さんが今年仕入れた肥料は総額900万円で去年の2倍です。農機具を動かす燃料代も上がっています。コメの買い取り価格について白井さんは「今年は1万6000円ぐらいと予想しているが、生産原価が2万2000円から3000円。とんでもない赤字なんで、今年で農家をやめるという人は出てきたね」と話します。",
                "en": "Months after planting in May, Shirai's expenses are already fixed. The fertilizer he purchased this year totaled 9 million yen, twice as much as last year. Fuel costs for farm machinery have also risen. Regarding the purchase price for rice, Shirai says, \"I expect around 16,000 yen this year, but the production cost is 22,000 to 23,000 yen. It's an absurd loss, so people are already deciding to quit farming after this year.\"",
                "literal": "从5月插秧开始的几个月，白井的支出已经确定了。白井今年购入的肥料总额900万日元，是去年的2倍。驱动农机具的燃料费也上涨了。关于大米的收购价格，白井说「今年预计1万6000日元左右，但生产成本是2万2000到3000日元。因为是非常离谱的赤字，已经出现了今年就放弃务农的人」。",
                "grammar": "「〜と予想している」— 预计…。例：1万6000円ぐらいと予想している（预计1万6000日元左右）。\n「〜なんで」— 因为…（口语）。例：とんでもない赤字なんで（因为是非常离谱的赤字）。\n「〜という人は出てきた」— 出现了…的人。例：農家をやめるという人は出てきた（出现了放弃务农的人）。",
                "vocab": [
                    ["田植え", "たうえ", "插秧"],
                    ["支出", "ししゅつ", "支出"],
                    ["肥料", "ひりょう", "肥料"],
                    ["燃料代", "ねんりょうだい", "燃料费"],
                    ["買い取り価格", "かいとりかかく", "收购价格"],
                    ["赤字", "あかじ", "赤字、亏损"]
                ]
            },
            {
                "ja": "黄金色に実った稲が一面に広がる秋の見慣れた光景は、当たり前ではなくなるかもしれません。コメの価格が下がれば、農家はみんなやめてしまう。白井さんは以前からそう警告してきましたが、その不安はいま、現実のものとなっています。",
                "en": "The familiar autumn scene of golden rice spreading across the fields may no longer be taken for granted. If rice prices fall, all farmers will quit. Shirai has long warned of this, and that anxiety is now becoming a reality.",
                "literal": "金黄色稻穗铺满一望无际的田地的秋天熟悉景象，也许将不再理所当然。如果大米价格下跌，农民们都会放弃。白井以前就一直这样警告，而那份不安现在正变成现实。",
                "grammar": "「〜かもしれません」— 也许…。例：当たり前ではなくなるかもしれません（也许不再理所当然）。\n「〜ば」— 如果…就…。例：価格が下がれば、農家はやめてしまう（价格一跌，农民就会放弃）。\n「〜現実のものとなっています」— 正在变成现实。例：不安はいま、現実のものとなっています（不安现在正变成现实）。",
                "vocab": [
                    ["黄金色", "こがねいろ", "金黄色"],
                    ["実る", "みのる", "结果实、成熟"],
                    ["一面", "いちめん", "一片、满眼"],
                    ["見慣れた", "みなれた", "看惯了的"],
                    ["警告", "けいこく", "警告"],
                    ["現実", "げんじつ", "现实"]
                ]
            }
        ]
    },
    {
        "slug": "joshi-kousei-kyouhaku",
        "title": "「会わんかったら親や学校に言うぞ」女子高校生を脅迫しホテルへ…44歳男を逮捕 大阪府警",
        "subtitle": "from MBSニュース",
        "paras": [
            {
                "ja": "SNSで知り合った女子高校生を脅し、性的暴行を加え撮影したとして44歳の男が逮捕されました。警察によりますと、東大阪市の無職・橋本久典容疑者（44）は去年8月、大阪府内でSNSで知り合った女子高校生（10代）を脅迫し、性的暴行を加え撮影するなどした疑いがもたれています。",
                "en": "A 44-year-old man has been arrested for threatening a female high school student he met on social media, sexually assaulting her, and filming it. According to police, Hisanori Hashimoto (44), unemployed, of Higashiosaka City, is suspected of threatening a female high school student (a teenager) he met on SNS in Osaka Prefecture in August last year, assaulting her sexually, and filming the act.",
                "literal": "因威胁在SNS上认识的女子高中生、施加强奸并拍摄，44岁的男子被逮捕。据警方称，东大阪市的无业人员・桥本久典嫌疑人（44岁）去年8月，在大阪府内涉嫌威胁在SNS上认识的女子高中生（10多岁），施加强奸并拍摄等。",
                "grammar": "「〜として」— 以…为由、因…。例：脅し、撮影したとして逮捕（因威胁并拍摄而被逮捕）。\n「〜によりますと」— 据…称。例：警察によりますと（据警方称）。\n「〜疑いがもたれています」— 被怀疑…。例：疑いがもたれています（涉嫌）。",
                "vocab": [
                    ["脅す", "おどす", "威胁、恐吓"],
                    ["性的暴行", "せいてきぼうこう", "性暴力、强奸"],
                    ["逮捕", "たいほ", "逮捕"],
                    ["容疑者", "ようぎしゃ", "嫌疑人"],
                    ["無職", "むしょく", "无业"],
                    ["疑い", "うたがい", "嫌疑"]
                ]
            },
            {
                "ja": "事件の前に女子高校生と会った際、個人情報が分かる物を撮影し、その後「会わんかったら親や学校に言うぞ」などと脅し、ホテルに連れて来ていたということです。橋本容疑者はすでに別の女子高校生に性的暴行を加えたなどとして逮捕・起訴されていて、その捜査の過程で今回の事件が浮上。押収されたスマートフォンには十数人の女性の動画などが残されていたということです。",
                "en": "When he met the student before the incident, he photographed items that revealed her personal information, and afterward threatened her with remarks like \"If you don't meet me, I'll tell your parents and school,\" bringing her to a hotel. Hashimoto had already been arrested and indicted for sexually assaulting another female high school student, and this case surfaced during that investigation. Videos of more than a dozen women were found on his confiscated smartphone.",
                "literal": "事件发生前与女子高中生见面时，拍摄了能知道个人信息的物品，之后用「不见面的话就告诉你父母和学校」等威胁，把她带到了酒店。桥本嫌疑人已经因对另一名女子高中生施加强奸等而被逮捕起诉，在这次事件的搜查过程中，本次事件浮出水面。被扣押的智能手机中留有十几名女性的视频等。",
                "grammar": "「〜際」— …的时候。例：女子高校生と会った際（与女高中生见面时）。\n「〜ぞ」— 语气助词，表示强调警告。例：親や学校に言うぞ（就告诉你父母和学校哦）。\n「〜として浮上」— 作为…浮现出来。例：捜査の過程で今回の事件が浮上（在搜查过程中本案浮出水面）。",
                "vocab": [
                    ["個人情報", "こじんじょうほう", "个人信息"],
                    ["脅す", "おどす", "威胁"],
                    ["連れて来る", "つれてくる", "带来、领来"],
                    ["起訴", "きそ", "起诉"],
                    ["捜査", "そうさ", "搜查、侦查"],
                    ["押収", "おうしゅう", "扣押、没收"]
                ]
            },
            {
                "ja": "警察は橋本容疑者の認否を明らかにしていません。SNSを通じて知り合った相手とのトラブルは後を絶ちません。警察は「知らない人からの誘いには慎重に対応してほしい」と呼びかけています。",
                "en": "Police have not disclosed whether Hashimoto admits to the charges. Trouble involving people who meet through social media shows no end. Police are urging, \"Please respond carefully to invitations from people you don't know.\"",
                "literal": "警方没有公布桥本嫌疑人是否认罪。通过SNS认识的对象之间的纠纷层出不穷。警方呼吁「对陌生人的邀约请慎重应对」。",
                "grammar": "「〜を明らかにしていません」— 没有公布…。例：認否を明らかにしていません（没有公布认罪与否）。\n「〜後を絶ちません」— 层出不穷、不断。例：トラブルは後を絶ちません（纠纷层出不穷）。\n「〜てほしい」— 希望（对方）…。例：慎重に対応してほしい（希望慎重应对）。",
                "vocab": [
                    ["認否", "にんぴ", "是否认罪"],
                    ["トラブル", "とらぶる", "纠纷、麻烦"],
                    ["後を絶たない", "あとをたたない", "层出不穷"],
                    ["誘い", "さそい", "邀请、邀约"],
                    ["慎重に", "しんちょうに", "慎重地"],
                    ["呼びかける", "よびかける", "呼吁、号召"]
                ]
            }
        ]
    },
    {
        "slug": "ny-dow-54000-dai",
        "title": "NYダウ900ドル超高、連日の最高値 中東情勢の緊張緩和に期待",
        "subtitle": "from 朝日新聞",
        "paras": [
            {
                "ja": "4日のニューヨーク株式市場で、主要企業でつくるダウ工業株平均が、前日の終値から900ドル超上昇し、初めて5万4000ドル台をつけて取引を終えた。中東情勢の緊張緩和への期待や、好調な企業決算などが買いにつながった。ダウ平均の終値は前日より907.47ドル（1.71%）高い、5万4085.88ドルだった。4日は取引開始直後から買いが広がり、上げ幅は一時1000ドルを超え、取引時間中の最高値も更新した。",
                "en": "On the New York stock market on the 4th, the Dow Jones Industrial Average, composed of major companies, rose more than 900 dollars from the previous day's close, finishing trading above the 54,000 level for the first time. Expectations of easing tensions in the Middle East and strong corporate earnings drove buying. The Dow closed at 54,085.88 dollars, up 907.47 dollars (1.71%) from the previous day. On the 4th, buying spread from the very start of trading, with the gain temporarily exceeding 1,000 dollars, also updating the intraday record high.",
                "literal": "在4日的纽约股票市场，由主要企业构成的道琼斯工业平均指数比前一日收盘价上涨超过900美元，首次站上5万4000点区间收盘。对中东局势紧张缓和的期待以及强劲的企业财报等带动了买入。道琼斯平均收盘价为5万4085.88美元，比前一日高907.47美元（1.71%）。4日从交易开始后不久买盘就扩大，涨幅一度超过1000美元，也刷新了盘中最高价。",
                "grammar": "「〜台をつけて」— 达到…的区间。例：5万4000ドル台をつけて取引を終えた（站上5万4000点区间收盘）。\n「〜が買いにつながった」— 带动了买盘。例：期待や決算が買いにつながった（期待和财报带动了买盘）。\n「〜一時」— 一度、暂时。例：上げ幅は一時1000ドルを超えた（涨幅一度超过1000美元）。",
                "vocab": [
                    ["株式市場", "かぶしきしじょう", "股票市场"],
                    ["終値", "おわりね", "收盘价"],
                    ["上昇", "じょうしょう", "上涨"],
                    ["緊張緩和", "きんちょうかんわ", "紧张缓和"],
                    ["決算", "けっさん", "财报、决算"],
                    ["上げ幅", "あげはば", "涨幅"]
                ]
            },
            {
                "ja": "米国のベッセント財務長官は4日、米CNBCのインタビューで、イランとの協議を巡り、エネルギー輸送の要衝であるホルムズ海峡の開放について、「今日か明日にも、合意する可能性がある」と述べた。原油価格の指標となる「米国産WTI原油」の先物価格は、一時6%超下落し、1バレル=75ドル台をつけた。",
                "en": "U.S. Treasury Secretary Bessent said in an interview with CNBC on the 4th that, regarding talks with Iran, there is a possibility of an agreement \"today or tomorrow\" on reopening the Strait of Hormuz, a key chokepoint for energy transport. The futures price of \"U.S. WTI crude,\" the benchmark for oil prices, fell more than 6% at one point, reaching the mid-$70s per barrel.",
                "literal": "美国财政部长贝森特4日在接受美国CNBC采访时，围绕与伊朗的磋商，就能源运输要冲霍尔木兹海峡的开放表示「今天或明天也有可能达成协议」。作为原油价格指标的「美国产WTI原油」期货价格一度下跌超过6%，跌至1桶75美元区间。",
                "grammar": "「〜を巡り」— 围绕…。例：イランとの協議を巡り（围绕与伊朗的磋商）。\n「〜である」— 是…（书面语）。例：要衝であるホルムズ海峡（作为要冲的霍尔木兹海峡）。\n「〜可能性がある」— 有可能…。例：合意する可能性がある（有可能达成协议）。",
                "vocab": [
                    ["財務長官", "ざいむちょうかん", "财政部长"],
                    ["協議", "きょうぎ", "磋商、协商"],
                    ["要衝", "ようしょう", "要冲、咽喉要地"],
                    ["原油", "げんゆ", "原油"],
                    ["先物価格", "さきものかかく", "期货价格"],
                    ["下落", "げらく", "下跌"]
                ]
            },
            {
                "ja": "中東情勢の緊張緩和への期待や、原油価格の下落を受けて株が買われ、テクノロジー関連などで上昇が目立った。また、建設機械大手のキャタピラーは、4日に発表した決算の内容が好感され、終値は前日から5%超上昇した。データセンター投資の増加などを受けて需要が増え、売上高や純利益が前年同期から伸びた。",
                "en": "Stocks were bought on expectations of easing Middle East tensions and falling oil prices, with notable gains in technology-related shares. Also, Caterpillar, a major construction machinery maker, saw its earnings released on the 4th received favorably, with its closing price rising more than 5% from the previous day. Demand increased on the back of growing data center investment, and sales and net profit grew from the same period last year.",
                "literal": "受对中东局势紧张缓和的期待以及原油价格下跌的影响，股票被买入，科技相关板块的上涨引人注目。另外，建设机械巨头卡特彼勒4日公布的财报内容受到好评，收盘价比前一日上涨超过5%。受数据中心投资增加等影响需求增长，销售额和净利润比去年同期增长。",
                "grammar": "「〜を受けて」— 受…影响、基于…。例：原油価格の下落を受けて（受原油价格下跌影响）。\n「〜が好感され」— 受到好评。例：決算の内容が好感され（财报内容受到好评）。\n「〜から伸びた」— 比…增长。例：前年同期から伸びた（比去年同期增长）。",
                "vocab": [
                    ["テクノロジー", "てくのろじー", "科技"],
                    ["目立つ", "めだつ", "显眼、引人注目"],
                    ["建設機械", "けんせつきかい", "工程机械"],
                    ["好感", "こうかん", "好感、好评"],
                    ["売上高", "うりあげだか", "销售额"],
                    ["純利益", "じゅんりえき", "净利润"]
                ]
            }
        ]
    },
    {
        "slug": "kumamoto-jishin-isshuukan",
        "title": "熊本地震1週間、避難所に7538人・断水4万4380戸 連日の猛暑で被災者の心身の不調懸念",
        "subtitle": "from 読売新聞オンライン",
        "paras": [
            {
                "ja": "熊本県で最大震度7を観測した地震は4日、発生から1週間となった。死者は、車中泊による熱中症の疑いで亡くなった1人を含む38人、住宅被害は1万3690棟に上る。一部自治体で断水は解消せず、避難所には7538人が身を寄せている。連日の猛暑が続き、被災者の疲労や心身の不調が心配される。",
                "en": "On the 4th, one week had passed since the earthquake that recorded a maximum seismic intensity of 7 in Kumamoto Prefecture. The death toll has reached 38, including one person believed to have died of heatstroke while evacuating in a car, and 13,690 homes have been damaged. Water outages remain unresolved in some municipalities, and 7,538 people are taking shelter in evacuation centers. With extreme heat continuing day after day, there are concerns about victims' exhaustion and physical and mental health.",
                "literal": "在熊本县观测到最大震度7的地震，到4日已过去1周。死者包括1名疑似因车中过夜避难中暑死亡的人在内共38人，住宅受损达1万3690栋。部分地方政府断水尚未解除，7538人正在避难所栖身。连日酷暑持续，受灾者的疲劳和身心不适令人担忧。",
                "grammar": "「〜から1週間となった」— 距…已过去1周。例：発生から1週間となった（距发生已过1周）。\n「〜に上る」— 达到…（数量大）。例：住宅被害は1万3690棟に上る（住宅受损达1万3690栋）。\n「〜が心配される」— 令人担忧…。例：心身の不調が心配される（身心不适令人担忧）。",
                "vocab": [
                    ["震度", "しんど", "震度"],
                    ["死者", "ししゃ", "死者"],
                    ["車中泊", "しゃちゅうはく", "在车里过夜"],
                    ["断水", "だんすい", "断水"],
                    ["身を寄せる", "みをよせる", "栖身、投靠"],
                    ["猛暑", "もうしょ", "酷暑"]
                ]
            },
            {
                "ja": "気象庁によると、4日の最高気温は熊本市で36.8度を観測した。県によると、震度6強以上を観測した自治体を管轄する4消防では、地震発生の7月28日から7日間で熱中症の搬送は1日平均約30件に及んだ。震度7を観測した宇城市や氷川町など、4市町の約4万4380戸で断水が続く。全域での復旧は8月末の見通しだ。",
                "en": "According to the Japan Meteorological Agency, the highest temperature on the 4th was 36.8 degrees in Kumamoto City. According to the prefecture, at four fire departments covering municipalities that recorded intensity 6-lower or higher, heatstroke transports averaged about 30 per day over the seven days since the earthquake on July 28. Water outages continue in about 44,380 households across four municipalities, including Uki City and Hikawa Town, where intensity 7 was recorded. Full restoration is expected by the end of August.",
                "literal": "据气象厅称，4日熊本市观测到最高气温36.8度。据县方称，管辖观测到震度6强以上地方政府的4个消防署，从地震发生的7月28日起7天内，中暑运送平均每天达到约30件。观测到震度7的宇城市和冰川町等4个市町约4万4380户持续断水。全域恢复预计在8月底。",
                "grammar": "「〜によると」— 据…称。例：気象庁によると（据气象厅称）。\n「〜に及んだ」— 达到…。例：1日平均約30件に及んだ（平均每天达到约30件）。\n「〜の見通しだ」— 预计…。例：8月末の見通しだ（预计8月底）。",
                "vocab": [
                    ["気象庁", "きしょうちょう", "气象厅"],
                    ["最高気温", "さいこうきおん", "最高气温"],
                    ["管轄", "かんかつ", "管辖"],
                    ["熱中症", "ねっちゅうしょう", "中暑"],
                    ["搬送", "はんそう", "运送（伤员）"],
                    ["復旧", "ふっきゅう", "恢复"]
                ]
            },
            {
                "ja": "西日本高速道路は4日、九州自動車道について、8月後半に全線開通する見通しと発表した。九州新幹線は熊本―鹿児島中央駅間で運休中で、JR九州は全線での再開について「8月中は困難」としている。気象庁は4日、記者会見し、今後1週間程度は最大震度5強以上の地震に注意するよう呼びかけた。発生回数は緩やかに減少しているものの、地震活動は依然として活発で、最大震度5強程度以上の発生確率は平常時の80倍程度という。",
                "en": "NEXCO West Japan announced on the 4th that the Kyushu Expressway is expected to fully reopen in the second half of August. The Kyushu Shinkansen remains suspended between Kumamoto and Kagoshima-Chuo stations, with JR Kyushu saying full resumption \"will be difficult within August.\" The Japan Meteorological Agency held a press conference on the 4th, calling on people to be alert for earthquakes of maximum intensity 5-lower or stronger for about the next week. Although the number of quakes is gradually decreasing, seismic activity remains active, with the probability of an earthquake of intensity 5-lower or stronger said to be about 80 times higher than normal.",
                "literal": "西日本高速道路4日宣布，九州机动车道预计8月下旬全线开通。九州新干线熊本—鹿儿岛中央站区间停运中，JR九州表示全线恢复「8月内困难」。气象厅4日召开记者会，呼吁今后1周左右注意最大震度5强以上的地震。发生次数虽然正在缓慢减少，但地震活动依然活跃，最大震度5强程度以上的发生概率据称是平时的80倍左右。",
                "grammar": "「〜と発表した」— 宣布…。例：全線開通する見通しと発表した（宣布预计全线开通）。\n「〜としている」— 表示…、认为…。例：8月中は困難としている（表示8月内困难）。\n「〜ものの」— 虽然…但是…。例：減少しているものの、依然として活発だ（虽然减少，但仍然活跃）。",
                "vocab": [
                    ["全線開通", "ぜんせんかいつう", "全线开通"],
                    ["運休", "うんきゅう", "停运"],
                    ["再開", "さいかい", "恢复、重启"],
                    ["呼びかける", "よびかける", "呼吁"],
                    ["緩やか", "ゆるやか", "缓慢"],
                    ["確率", "かくりつ", "概率"]
                ]
            }
        ]
    },
]
articles += [
    {
        "slug": "ion-bakuhatsu-wedding-dress",
        "title": "イオンモール爆発で犠牲となった妻、告別式にウェディングドレス飾った夫「生前に着させてあげたかった」",
        "subtitle": "from 読売新聞オンライン",
        "paras": [
            {
                "ja": "「イオンモール熊本」で発生した爆発事故で、犠牲となったアパレル従業員の女性（39）の告別式が4日、熊本市で営まれた。夫で喪主を務めた男性（39）は、着せられなかったウェディングドレスを会場に飾り、「生前に着させてあげたかった。遅くなったが、喜んでくれるといいな」と涙まじりにほほ笑んだ。",
                "en": "A funeral was held in Kumamoto City on the 4th for a female apparel store employee (39) who lost her life in the explosion at Aeon Mall Kumamoto. Her husband (39), who served as chief mourner, displayed in the venue a wedding dress she never got to wear, and smiled through tears, saying, \"I wanted to let her wear it while she was alive. It's late now, but I hope she'll be pleased.\"",
                "literal": "在「永旺商城熊本」发生的爆炸事故中遇难的女装店女员工（39岁）的告别仪式4日在熊本市举行。担任丧主的丈夫（39岁）把没能让她穿上的婚纱装饰在会场，含着泪微笑着说「生前真想让她穿上。虽然晚了，但希望她会高兴」。",
                "grammar": "「〜で営まれた」— 在…举行（仪式）。例：告別式が熊本市で営まれた（告别仪式在熊本市举行）。\n「〜てあげたかった」— 本想为（对方）做…。例：着させてあげたかった（本想让她穿上）。\n「〜といいな」— 要是…就好了。例：喜んでくれるといいな（要是她会高兴就好了）。",
                "vocab": [
                    ["犠牲", "ぎせい", "牺牲、遇难"],
                    ["告別式", "こくべつしき", "告别仪式"],
                    ["喪主", "もしゅ", "丧主"],
                    ["ウェディングドレス", "うぇでぃんぐどれす", "婚纱"],
                    ["涙まじり", "なみだまじり", "含泪、带着泪"],
                    ["ほほ笑む", "ほほえむ", "微笑"]
                ]
            },
            {
                "ja": "男性によると、女性はモール2階のアパレル店に勤務し、地震後に一度は屋外へ避難したが、施設に戻って爆発に巻き込まれたとみられる。夫婦は約15年前に結婚したが、式を挙げておらず、「いつかウェディングドレスを着て写真を撮ろうね」と約束を交わしていたという。",
                "en": "According to the husband, the woman worked at an apparel store on the second floor of the mall and evacuated outside after the earthquake, but is believed to have returned to the facility and been caught in the explosion. The couple married about 15 years ago but never held a ceremony, and had promised each other, \"Someday let's wear a wedding dress and take photos.\"",
                "literal": "据丈夫称，女性在商场2楼的女装店工作，地震后曾一度避难到室外，但被认为返回设施后被卷入爆炸。夫妇约15年前结婚，但没有举行仪式，据说曾互相约定「哪天穿上婚纱拍照片吧」。",
                "grammar": "「〜によると」— 据…称。例：男性によると（据丈夫称）。\n「〜とみられる」— 被认为…。例：巻き込まれたとみられる（被认为被卷入）。\n「〜を交わしていた」— 互相交换（约定）。例：約束を交わしていた（互相约定过）。",
                "vocab": [
                    ["勤務", "きんむ", "工作、任职"],
                    ["屋外", "おくがい", "室外"],
                    ["夫婦", "ふうふ", "夫妇"],
                    ["式を挙げる", "しきをあげる", "举行婚礼"],
                    ["約束", "やくそく", "约定"],
                    ["交わす", "かわす", "交换、互致"]
                ]
            },
            {
                "ja": "この日は親族を通じて譲り受けたドレスを式場に飾り、女性が好きだったピンク色のバラなどで祭壇を彩った。中学の同級生だった2人の友人らを含め数多くの人たちが参列し、花を手向けた。式の最後、ドレスとともに、夫婦で名付けた中学1年の長男（13）と同じ名前の花をひつぎに入れ、「なんで施設に戻ったんだ……。今までありがとう。子どものことを見守っていてね」と送り出した。",
                "en": "On this day, the dress received through relatives was displayed in the venue, and the altar was decorated with pink roses, the woman's favorite flowers. Many people attended, including two friends who had been their junior high school classmates, and offered flowers. At the end of the ceremony, along with the dress, they placed in the coffin flowers bearing the same name as their eldest son (13), a first-year junior high student whom the couple had named together, and sent her off with the words, \"Why did you go back into the building...? Thank you for everything until now. Please watch over our child.\"",
                "literal": "这一天，把通过亲属转赠的婚纱装饰在仪式会场，用女性喜欢的粉色玫瑰等装点了祭坛。包括曾是初中同学的2位友人在内，许多人出席并献花。仪式的最后，把与夫妇共同命名的初中一年级长子（13岁）同名的花和婚纱一起放入棺中，送别道「为什么要返回设施呢……。至今为止谢谢你。请守护孩子」。",
                "grammar": "「〜を通じて」— 通过…。例：親族を通じて譲り受けた（通过亲属受赠）。\n「〜を含め」— 包括…在内。例：友人らを含め数多くの人たちが参列した（包括友人在内许多人出席）。\n「〜んだ」— 口语疑问・感叹。例：なんで施設に戻ったんだ（为什么要返回设施呢）。",
                "vocab": [
                    ["譲り受ける", "ゆずりうける", "受赠、继承"],
                    ["祭壇", "さいだん", "祭坛"],
                    ["彩る", "いろどる", "装点、点缀"],
                    ["参列", "さんれつ", "出席（仪式）"],
                    ["手向ける", "たむける", "献（花）"],
                    ["見守る", "みまもる", "守护、注视"]
                ]
            },
            {
                "ja": "男性は式後、「本当に本当に長い1週間だった。まだ実感はわかないが、息子と一緒に妻の分も生きていく」と静かに語った。地震のあとに起きた爆発で命を落とした7人。遺された家族たちの悲しみは深い。",
                "en": "After the ceremony, the husband said quietly, \"It was truly, truly a long week. I still can't quite feel it's real, but I'll live on with our son, living my wife's share too.\" Seven people lost their lives in the explosion that followed the earthquake. The grief of the families left behind runs deep.",
                "literal": "丈夫在仪式后平静地说「真的是非常漫长的一周。还没有真实感，但我要和儿子一起，把妻子的份也活出来」。在地震后发生的爆炸中失去生命的7人。被留下的家人们的悲伤很深。",
                "grammar": "「〜た」＋「〜が」— 过去＋转折。例：まだ実感はわかないが（虽然还没有真实感）。\n「〜の分も」— 连…的份也。例：妻の分も生きていく（把妻子的份也活出来）。\n「〜と静かに語った」— 平静地说…。例：静かに語った（平静地说道）。",
                "vocab": [
                    ["実感", "じっかん", "真实感"],
                    ["わく", "わく", "涌出、产生"],
                    ["命を落とす", "いのちをおとす", "丧命"],
                    ["遺される", "のこされる", "被留下"],
                    ["悲しみ", "かなしみ", "悲伤"],
                    ["深い", "ふかい", "深的、深沉的"]
                ]
            }
        ]
    },
    {
        "slug": "fukuoka-kengikai-daisansha",
        "title": "福岡県議会が第三者委設置へ 正副議長ポスト巡る金銭授受疑惑、批判高まり方針転換",
        "subtitle": "from 西日本新聞me",
        "paras": [
            {
                "ja": "福岡県議会が、正副議長ポストを巡る金銭授受疑惑について、日弁連のガイドラインに基づく第三者委員会を設置する見通しであることが4日分かった。蔵内勇夫議長は調査に時間がかかるとして否定していたが、議会内外から設置を求める声が強まり、方針転換を余儀なくされた格好だ。",
                "en": "It became known on the 4th that the Fukuoka Prefectural Assembly is expected to establish a third-party committee, based on the Japan Federation of Bar Associations' guidelines, regarding suspicions of money exchanges involving the posts of assembly speaker and vice speaker. Assembly Speaker Isao Kurauchi had rejected the idea, saying an investigation would take time, but voices demanding its establishment grew both inside and outside the assembly, forcing a policy reversal.",
                "literal": "福冈县议会围绕正副议长职位相关的金钱授受嫌疑，4日获悉将依据日辩联的指导方针设立第三方委员会的预定。藏内勇夫议长此前以调查耗时为由予以否定，但议会内外要求设立的声音增强，被迫转变了方针。",
                "grammar": "「〜を巡る」— 围绕…的。例：正副議長ポストを巡る疑惑（围绕正副议长职位的嫌疑）。\n「〜に基づく」— 基于…的。例：ガイドラインに基づく第三者委員会（基于指导方针的第三方委员会）。\n「〜を余儀なくされた」— 被迫…。例：方針転換を余儀なくされた（被迫转变方针）。",
                "vocab": [
                    ["議長", "ぎちょう", "议长"],
                    ["金銭授受", "きんせんじゅじゅ", "金钱授受"],
                    ["疑惑", "ぎわく", "嫌疑、疑云"],
                    ["ガイドライン", "がいどらいん", "指导方针、准则"],
                    ["第三者委員会", "だいさんしゃいいんかい", "第三方委员会"],
                    ["余儀なくされる", "よぎなくされる", "被迫、不得已"]
                ]
            },
            {
                "ja": "関係者によると、県弁護士会とも既に調整しており、県議会と利害関係がない弁護士や学識者で構成する見込み。調査の詳細は議会側に事前に伝えず、議会側に不利な結果でも公表し、問題を確認した場合は是正措置を提示するという。",
                "en": "According to people involved, coordination with the prefectural bar association has already begun, and the committee is expected to be composed of lawyers and academics with no conflicts of interest with the assembly. The details of the investigation will not be shared with the assembly side in advance; even results unfavorable to the assembly will be made public, and corrective measures will be proposed if problems are confirmed.",
                "literal": "据相关人士称，已与县律师会进行协调，预计由与县议会没有利害关系的律师和学者组成。调查的详细内容不事先告知议会方面，即使是对议会方面不利的结果也会公布，确认有问题时将提示纠正措施。",
                "grammar": "「〜見込み」— 预计、预定。例：構成する見込み（预计由…组成）。\n「〜ず」— 不…。例：事前に伝えず（不事先告知）。\n「〜場合は」— …的情况下。例：問題を確認した場合は（确认有问题的情况下）。",
                "vocab": [
                    ["調整", "ちょうせい", "协调、调整"],
                    ["利害関係", "りがいかんけい", "利害关系"],
                    ["学識者", "がくしきしゃ", "学者、有学识的人"],
                    ["構成", "こうせい", "构成、组成"],
                    ["公表", "こうひょう", "公布"],
                    ["是正措置", "ぜせいそち", "纠正措施"]
                ]
            },
            {
                "ja": "蔵内氏は報道により疑惑が発覚した直後の7月上旬、外部の弁護士らによる聞き取り調査で対応する方針を示していた。しかしその後、服部誠太郎知事が知事部局の問題について第三者委を設置して検証する方針を発表し、議会側も同様の対応が望ましいとの考えを表明。自民党の若手議員の間で「客観性の高い調査でないと県民は納得しない」との声が高まり、他会派からも第三者委設置を要望する動きが出ていた。蔵内氏は4日夜、「検討を進めた結果、ベストな形が見いだせる道が見えてきた」とするコメントを発表した。",
                "en": "Kurauchi had indicated a policy of responding through hearings conducted by outside lawyers in early July, right after the suspicion came to light through media reports. However, Governor Seitaro Hattori subsequently announced a policy of establishing a third-party committee to verify problems in the governor's office, and the assembly side also expressed the view that a similar response was desirable. Among young LDP lawmakers, calls grew that \"unless the investigation is highly objective, the public won't accept it,\" and other factions also moved to request a third-party committee. On the night of the 4th, Kurauchi released a comment saying, \"As a result of our deliberations, we can now see a path to finding the best form.\"",
                "literal": "藏内氏在嫌疑经报道曝光的7月上旬，曾表示以外部律师等进行问询调查的方针。但此后，服部诚太郎知事公布了就知事部局问题设立第三方委员会进行验证的方针，议会方面也表示认为同样的应对是可取的。自民党年轻议员之间「没有高客观性的调查县民不会信服」的呼声高涨，其他党派也出现了要求设立第三方委员会的动作。藏内氏4日晚发表了「推进探讨的结果，看到了能找出最佳形式的道路」的评论。",
                "grammar": "「〜発覚した直後」— 刚被曝光的…之后。例：疑惑が発覚した直後の7月上旬（嫌疑刚曝光的7月上旬）。\n「〜との声が高まる」— …的呼声高涨。例：納得しないとの声が高まり（不会信服的呼声高涨）。\n「〜とするコメント」— 表示…的评论。例：見えてきたとするコメント（表示看到了道路的评论）。",
                "vocab": [
                    ["発覚", "はっかく", "曝光、败露"],
                    ["聞き取り調査", "ききとりちょうさ", "问询调查"],
                    ["知事", "ちじ", "知事（县长）"],
                    ["検証", "けんしょう", "验证"],
                    ["客観性", "きゃっかんせい", "客观性"],
                    ["要望", "ようぼう", "要求、期望"]
                ]
            }
        ]
    },
    {
        "slug": "higashino-keigo-eien-no-kioku",
        "title": "東野圭吾さん最新作「永遠の記憶」発売 涙を流しながら本を受け取るファンの姿も",
        "subtitle": "from サンケイスポーツ",
        "paras": [
            {
                "ja": "7月23日に大腸がんのため68歳で亡くなった作家、東野圭吾さんの代表作「ガリレオ」シリーズ最新作で遺作「永遠の記憶」（文藝春秋刊、税込み2310円）の発売カウントダウンイベントが4日夜、東京・紀伊國屋書店新宿本店で行われた。",
                "en": "On the night of the 4th, a countdown event for the release of \"Eien no Kioku\" (Bungeishunju, 2,310 yen including tax) — the latest and final work in the \"Galileo\" series, the masterpiece series by author Keigo Higashino, who died of colorectal cancer on July 23 at age 68 — was held at Kinokuniya Bookstore's main Shinjuku store in Tokyo.",
                "literal": "因大肠癌于7月23日以68岁去世的作家东野圭吾的代表作「伽利略」系列最新作兼遗作「永远的記憶」（文艺春秋出版，含税2310日元）的发售倒计时活动，4日晚在东京・纪伊国屋书店新宿本店举行。",
                "grammar": "「〜のため」— 因为…（原因）。例：大腸がんのため亡くなった（因大肠癌去世）。\n「〜で」— 以…的状态（年龄）。例：68歳で亡くなった（以68岁去世）。\n「〜が行われた」— 举行了…。例：イベントが行われた（举行了活动）。",
                "vocab": [
                    ["大腸がん", "だいちょうがん", "大肠癌"],
                    ["代表作", "だいひょうさく", "代表作"],
                    ["シリーズ", "しりーず", "系列"],
                    ["遺作", "いさく", "遗作"],
                    ["税込み", "ぜいこみ", "含税"],
                    ["カウントダウン", "かうんとだうん", "倒计时"]
                ]
            },
            {
                "ja": "シリーズ11作目の同作は、前作の「透明な螺旋」以来、約5年ぶりとなる長編。「ガリレオ、最後の謎」と銘打ち、8月5日に発売される。シリーズの主人公である天才物理学者、湯川学が、月刊小説誌「オール讀物」1996年11月号掲載の短編「燃える」に登場してから30周年という節目でもあった。",
                "en": "The work, the 11th in the series, is the first full-length novel in about five years since the previous \"Tomeina Rasen\" (Transparent Spiral). Billed as \"Galileo's Final Mystery,\" it goes on sale August 5. It also marks the 30th anniversary of the series' protagonist, genius physicist Manabu Yukawa, first appearing in the short story \"Moeru\" (Burning), published in the November 1996 issue of the monthly fiction magazine \"All Yomimono.\"",
                "literal": "系列第11作的该作品，是自前作「透明的螺旋」以来约5年来的长篇。以「伽利略、最后的谜题」为宣传语，将于8月5日发售。系列主人公天才物理学家汤川学，自出现在月刊小说杂志「All读物」1996年11月号刊载的短篇「燃烧」中以来，也恰逢30周年的节点。",
                "grammar": "「〜ぶり」— 时隔…。例：約5年ぶりとなる長編（时隔约5年的长篇）。\n「〜と銘打ち」— 以…为宣传语。例：「最後の謎」と銘打ち（以「最后的谜题」为宣传）。\n「〜という節目」— …的节点。例：30周年という節目でもあった（也是30周年的节点）。",
                "vocab": [
                    ["長編", "ちょうへん", "长篇"],
                    ["銘打つ", "めいうつ", "以…为名、宣传"],
                    ["主人公", "しゅじんこう", "主人公"],
                    ["天才物理学者", "てんさいぶつりがくしゃ", "天才物理学家"],
                    ["掲載", "けいさい", "刊载"],
                    ["節目", "ふしめ", "节点、阶段"]
                ]
            },
            {
                "ja": "発売日前日となる4日午後11時59分50秒からは発売日に向けてカウントダウン。日付が変わると、ファンたちは「ありがとう！！」と胸いっぱいに絶叫。中には、涙ぐみながら最新作を受け取る来場者の姿も見られた。この日は50人のファンが集結した。募集は26日正午から始まり、わずか2分で即完したという。",
                "en": "From 11:59:50 p.m. on the 4th, the day before release, a countdown to the release date began. When the date changed, fans shouted \"Thank you!!\" with full hearts. Some attendees were seen receiving the new work with tears in their eyes. Fifty fans gathered that day; applications opened at noon on the 26th and sold out in just two minutes.",
                "literal": "从发售日前一天的4日晚上11点59分50秒起，开始了面向发售日的倒计时。日期一变，粉丝们满怀激动地高喊「谢谢！！」。其中也能看到边流泪边接过最新作的到场者身影。这一天聚集了50名粉丝。招募从26日中午开始，据说仅仅2分钟就立即满员。",
                "grammar": "「〜となる」— 成为…。例：発売日前日となる4日（成为发售日前一天的4日）。\n「〜胸いっぱいに」— 满怀激动地。例：胸いっぱいに絶叫（满怀激动地高喊）。\n「〜ながら」— 一边…一边…。例：涙ぐみながら受け取る（边流泪边接过）。",
                "vocab": [
                    ["日付", "ひづけ", "日期"],
                    ["胸いっぱい", "むねいっぱい", "满怀、满心"],
                    ["絶叫", "ぜっきょう", "大声喊叫"],
                    ["涙ぐむ", "なみだぐむ", "含泪、眼含热泪"],
                    ["集結", "しゅうけつ", "聚集"],
                    ["即完", "そくかん", "立即售罄"]
                ]
            },
            {
                "ja": "東京都在住の30代男性は、「子供の頃、『容疑者Xの献身』で初めて長い本というものを読んだ」と回想。「これから読めなくなるのはすごく寂しい。もっと読みたかった」と唇をかんだ。神奈川県から訪れた20代の女性は、高校時代に東野作品に出会い、「片想い」がお気に入り。「今まで残してくれた100冊以上の本を大切に読みたいです」と話した。",
                "en": "A man in his 30s living in Tokyo recalled, \"When I was a kid, 'The Devotion of Suspect X' was the first long book I ever read.\" Biting his lip, he said, \"It's so sad that we won't be able to read new works anymore. I wanted to read more.\" A woman in her 20s who came from Kanagawa Prefecture discovered Higashino's works in high school, and \"Kataomoi\" (Unrequited Love) is her favorite. \"I want to read the 100-plus books he left us with care,\" she said.",
                "literal": "居住在东京都的30多岁男性回忆说「小时候，通过『嫌疑人X的献身』第一次读了长篇小说这样的东西」。「今后再也读不到新作，非常寂寞。还想多读一些」他咬着嘴唇说。从神奈川县来访的20多岁女性高中时代接触了东野作品，「单恋」是她的最爱。「我想珍惜地阅读他至今留下的100多本书」她说道。",
                "grammar": "「〜というもの」— 叫做…的东西。例：長い本というものを読んだ（读了长篇书这样的东西）。\n「〜唇をかんだ」— 咬住嘴唇（忍住感情）。例：唇をかんだ（咬住了嘴唇）。\n「〜を大切に読みたい」— 想珍惜地读…。例：本を大切に読みたいです（想珍惜地读书）。",
                "vocab": [
                    ["回想", "かいそう", "回忆、回想"],
                    ["寂しい", "さびしい", "寂寞、冷清"],
                    ["唇をかむ", "くちびるをかむ", "咬嘴唇（忍住感情）"],
                    ["お気に入り", "おきにいり", "最爱、中意"],
                    ["残す", "のこす", "留下"],
                    ["大切に", "たいせつに", "珍惜地"]
                ]
            }
        ]
    },
]
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
