#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-26 (Wed) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-26'
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
        "slug": "syouhizei-nouka-kyuufukin",
        "title": "消費減税、中小零細農家へ給付金　売上高に応じ減収穴埋め",
        "subtitle": "from 共同通信",
        "paras": [
            {
                "ja": "政府は25日、飲食料品の消費税率を1％に引き下げることで減収となる中小零細農家を支援するため、一定額の給付金を支払う方向で調整に入った。売り上げ規模に応じて減収を穴埋めする仕組みを想定しており、経営への打撃を和らげる狙いがある。制度の詳細や給付額は2027年度当初予算案の編成過程で具体化し、26年末までに決定する方針だ。",
                "en": "On the 25th, the government began coordinating toward paying a fixed amount of grants to support small and micro-scale farmers who would lose revenue from lowering the consumption tax rate on food and beverages to 1 percent. It envisions a system that fills the revenue shortfall according to sales scale, with the aim of softening the blow to management. Details of the system and grant amounts will be fleshed out during the drafting of the initial FY2027 budget and are to be decided by the end of 2026.",
                "literal": "政府25日为支援因将食品饮料消费税税率下调至1%而收入减少的中小零细农户，进入了支付一定金额补助金的方向性调整。设想根据销售额规模填补收入减少的机制，有缓和经营打击的意图。制度详情和补助金额将在2027年度当初预算案的编制过程中具体化，方针是在26年底前决定。",
                "grammar": "「〜ため、」— 为了…/因为…。例：農家を支援するため（为了支援农户）。\n「〜に応じて」— 根据…、按照…。例：売り上げ規模に応じて（根据销售额规模）。\n「〜方針だ」— 方针是…。例：26年末までに決定する方針だ（方针是在26年底前决定）。",
                "vocab": [["消費税", "しょうひぜい", "消费税"], ["給付金", "きゅうふきん", "补助金"], ["減収", "げんしゅう", "收入减少"], ["穴埋め", "あなうめ", "填补"], ["打撃", "だげき", "打击"], ["当初予算案", "とうしょよさんあん", "当初预算案"]]
            },
            {
                "ja": "農水産業は小規模な事業者が大半を占める。現在、売上高が年間1千万円以下の事業者は、消費税の納税義務が全額免除される「免税事業者」となる。5千万円以下は一部が免除される「簡易課税事業者」だ。減税後は消費税相当分の収入が減る一方、肥料や資材の仕入れには10％の消費税を払い続ける必要があり、手取りが少なくなる。",
                "en": "In agriculture and fisheries, small-scale operators account for the majority. Currently, businesses with annual sales of 10 million yen or less become \"tax-exempt operators\" whose obligation to pay consumption tax is fully waived. Those with sales of 50 million yen or less are \"simplified taxation operators\" with a partial waiver. After the tax cut, income equivalent to consumption tax decreases, while they must continue paying 10 percent consumption tax on purchases of fertilizer and materials, reducing their take-home earnings.",
                "literal": "农林水产业中，小规模经营者占大半。目前，年销售额在1千万日元以下的事业者成为消费税纳税义务被全额免除的「免税事业者」。5千万日元以下的是部分被免除的「简易课税事业者」。减税后，相当于消费税部分的收入减少，另一方面，肥料和资材的进货仍需持续支付10%的消费税，到手收入变少。",
                "grammar": "「〜を占める」— 占据…。例：大半を占める（占据大半）。\n「〜一方、」— 一方面…另一方面…。例：収入が減る一方、仕入れには払い続ける（收入减少，另一方面进货却要继续支付）。\n" 
                "「〜〜」",
                "vocab": [["農水産業", "のうすいさんぎょう", "农林水产业"], ["事業者", "じぎょうしゃ", "经营者"], ["納税義務", "のうぜいぎむ", "纳税义务"], ["免税事業者", "めんぜいじぎょうしゃ", "免税经营者"], ["簡易課税", "かんいかぜい", "简易课税"], ["仕入れ", "しいれ", "进货"], ["手取り", "てどり", "到手收入"]]
            },
            {
                "ja": "政府は、この仕入れにかかる税負担を補填する名目で、事業者の区分に応じて給付金を支払う方針だ。政府は支援の概要を自民党に提示し、減税で影響を受ける事業者の不安を解消し、27年4月から円滑な減税開始につなげる狙いだ。",
                "en": "The government plans to pay grants according to the operator category, under the rationale of covering the tax burden on these purchases. The government has presented an outline of the support to the Liberal Democratic Party, aiming to dispel anxiety among affected operators and lead to a smooth start of the tax cut from April 2027.",
                "literal": "政府方针是以填补这一进货相关的税负的名义，根据经营者的区分支付补助金。政府已向自民党出示了支援概要，目标是消除受减税影响的经营者的不安，并衔接27年4月起顺利开始减税。",
                "grammar": "「〜にかかる」— 与…相关、花费于…。例：仕入れにかかる税負担（进货相关的税负）。\n「〜名目で」— 以…名义。例：補填する名目で（以填补的名义）。\n「〜につなげる」— 与…相连、导向…。例：円滑な減税開始につなげる（导向顺利的减税开始）。",
                "vocab": [["補填", "ほてん", "填补、弥补"], ["概要", "がいよう", "概要"], ["提示", "ていじ", "出示、提示"], ["解消", "かいしょう", "消除"], ["円滑", "えんかつ", "顺利"], ["狙い", "ねらい", "目标、意图"]]
            },
        ]
    },
    {
        "slug": "tokuryuu-yakubutsu-taiho",
        "title": "俳優とトクリュウのトップが薬物所持疑い　ホテルのベッドに使用済みコカインの袋",
        "subtitle": "from 日テレNEWS NNN",
        "paras": [
            {
                "ja": "トクリュウのトップの男と俳優として活動する女が、東京・豊島区のホテルの一室でコカインを所持したなどとして逮捕された。逮捕されたのは、六代目山口組系暴力団幹部の菅原翔太容疑者（32）と、「新セリナ」の名前で俳優として活動する阿部星架容疑者（27）だ。2人は先月14日の午前2時すぎ、ホテルの一室でコカインおよそ0.7グラムを所持し、都内でコカインを使用した疑いがもたれている。",
                "en": "A man at the top of a \"tokuryu\" (anonymous fluid criminal group) and a woman active as an actress were arrested on suspicion of possessing cocaine in a hotel room in Toshima Ward, Tokyo. Those arrested are Shota Sugawara (32), an executive of a Sixth Yamaguchi-gumi-affiliated organized crime group, and Seirina Abe (27), who works as an actress under the name \"Shin Serena.\" The two are suspected of possessing about 0.7 grams of cocaine in a hotel room shortly after 2 a.m. on the 14th of last month and using cocaine within Tokyo.",
                "literal": "匿名流动型犯罪团伙（トクリュウ）的头目男性和作为演员活动的女性，因在东京・丰岛区的酒店房间里持有可卡因等嫌疑被逮捕。被逮捕的是六代目山口组系暴力团干部菅原翔太嫌疑人（32岁），以及以「新セリナ」名字作为演员活动的阿部星架嫌疑人（27岁）。2人涉嫌在上月14日凌晨2点多，在酒店房间里持有约0.7克可卡因，并在东京都内使用可卡因。",
                "grammar": "「〜として」— 作为…。例：俳優として活動する（作为演员活动）。\n「〜などとして逮捕された」— 因…等嫌疑被逮捕。例：所持したなどとして逮捕された（因持有等嫌疑被逮捕）。\n「〜疑いがもたれている」— 被怀疑…。例：使用した疑いがもたれている（被怀疑使用）。",
                "vocab": [["所持", "しょじ", "持有、携带"], ["逮捕", "たいほ", "逮捕"], ["暴力団", "ぼうりょくだん", "暴力团、黑社会"], ["幹部", "かんぶ", "干部"], ["容疑者", "ようぎしゃ", "嫌疑人"], ["疑い", "うたがい", "嫌疑"]]
            },
            {
                "ja": "菅原容疑者は匿名・流動型犯罪グループ＝トクリュウのトップとみられ、詐欺や強盗予備の疑いですでに逮捕されていた。捜査の過程で、菅原容疑者がホテルに頻繁に出入りしていることが判明し、警察が詐欺容疑で身柄を確保しようと部屋に入ったところ、ベッドの上に2人がいた。その際、シーツの中やベッドの棚からコカインが入った袋が見つかった。",
                "en": "Sugawara is believed to be the top of the anonymous fluid criminal group, \"tokuryu,\" and had already been arrested on suspicion of fraud and preparation for robbery. During the investigation, it was discovered that Sugawara frequently visited the hotel, and when police entered the room to take him into custody on fraud charges, the two were on the bed. At that time, bags containing cocaine were found inside the sheets and on the bed's shelf.",
                "literal": "菅原嫌疑人被认为是匿名・流动型犯罪团伙＝トクリュウ的头目，已因诈骗和抢劫预备的嫌疑被逮捕。在搜查过程中，查明菅原嫌疑人频繁出入酒店，警察为以诈骗嫌疑控制其人身而进入房间时，2人正在床上。当时，从床单里和床的搁板上发现了装有毒品的袋子。",
                "grammar": "「〜とみられる」— 被认为是…。例：トップとみられ（被认为是头目）。\n「〜ところ、」— 一…就…（接续助词）。例：部屋に入ったところ、2人がいた（一进房间，2人就在）。\n「〜ようと」— 想要…。例：身柄を確保しようと（想要控制其人身）。",
                "vocab": [["流動型", "りゅうどうがた", "流动型"], ["詐欺", "さぎ", "诈骗"], ["強盗予備", "ごうとうよび", "抢劫预备"], ["頻繁に", "ひんぱんに", "频繁地"], ["判明", "はんめい", "查明"], ["身柄", "みがら", "人身、本人"], ["シーツ", "しーつ", "床单"]]
            },
            {
                "ja": "調べに対し、菅原容疑者は「間違いありません」と容疑を認め、阿部容疑者は「使っていません」と容疑を否認している。警察は、菅原容疑者が特殊詐欺などで得たカネを違法薬物の購入にあて、豊島区のホテルで使用を繰り返していたとみて調べている。",
                "en": "In response to questioning, Sugawara admitted to the suspicion, saying, \"There's no mistake,\" while Abe denies it, saying, \"I didn't use it.\" Police believe Sugawara was using money obtained through special fraud and other crimes to buy illegal drugs, and repeatedly using them at the hotel in Toshima Ward, and are investigating.",
                "literal": "面对调查，菅原嫌疑人承认嫌疑说「没有错」，阿部嫌疑人否认嫌疑说「没有使用」。警察认为菅原嫌疑人把通过特殊诈骗等获得的钱用于购买违法药物，并在丰岛区的酒店反复使用，正在展开调查。",
                "grammar": "「〜に対し、」— 对…。例：調べに対し（面对调查）。\n" 
                "「〜にあてる」— 用于…、充作…。例：購入にあて（用于购买）。\n「〜とみて調べている」— 认为…正在调查。例：繰り返していたとみて調べている（认为在反复使用，正在调查）。",
                "vocab": [["否認", "ひにん", "否认"], ["特殊詐欺", "とくしゅさぎ", "特殊诈骗"], ["違法薬物", "いほうやくぶつ", "违法药物"], ["購入", "こうにゅう", "购买"], ["繰り返す", "くりかえす", "反复"], ["カネ", "かね", "金钱"]]
            },
        ]
    },
    {
        "slug": "takubo-sotsugyousyo-gisaku",
        "title": "田久保真紀前市長のPCから偽造された卒業証書のデータ　田久保氏側は裁判で無罪主張する方針",
        "subtitle": "from 静岡朝日テレビ",
        "paras": [
            {
                "ja": "大学の卒業証書を偽造した罪などで在宅起訴されている静岡県伊東市の田久保真紀前市長のパソコンから、偽造された卒業証書のデータが見つかっていたことが、関係者への取材で新たに分かった。近く始まるとされる裁判の重要証拠になるとみられる。",
                "en": "Through interviews with people involved, it has newly come to light that data for a forged diploma was found on the computer of former Ito City, Shizuoka Prefecture Mayor Maki Takubo, who has been indicted without arrest on charges including forgery of a university diploma. It is believed to become important evidence in the trial, which is said to begin soon.",
                "literal": "因伪造大学毕业证书等罪名被在宅起诉的静冈县伊东市前市长田久保真纪的电脑中，发现了被伪造的毕业证书数据，通过采访相关人士得知了这一新情况。这被认为将成为即将开始的审判的重要证据。",
                "grammar": "「〜ことが分かった」— 得知…、发现…。例：データが見つかっていたことが分かった（得知数据曾被找到）。\n「〜とされる」— 据称…、被认为是…。例：近く始まるとされる裁判（据称即将开始的审判）。\n「〜とみられる」— 被认为…。例：重要証拠になるとみられる（被认为将成为重要证据）。",
                "vocab": [["偽造", "ぎぞう", "伪造"], ["在宅起訴", "ざいたくきそ", "在宅起诉（不起诉羁押）"], ["前市長", "ぜんしちょう", "前市长"], ["関係者", "かんけいしゃ", "相关人士"], ["証拠", "しょうこ", "证据"], ["裁判", "さいばん", "审判"]]
            },
            {
                "ja": "田久保前市長は去年、インターネットで注文した東洋大学学長ら印鑑を使って卒業証書を偽造し、議長らに見せた有印私文書偽造などの罪で在宅起訴されている。捜査関係者によると、自宅から押収したパソコンをサイバー捜査により解析したところ、偽造した卒業証書のデータが見つかったという。",
                "en": "Last year, the former mayor was indicted without arrest on charges including forging a document with a seal, for using stamps of the Toyo University president and others ordered online to forge a diploma and showing it to the assembly chair and others. According to investigative sources, when the computer seized from her home was analyzed through cyber investigation, data for the forged diploma was found.",
                "literal": "田久保前市长去年使用在网上订购的东洋大学校长等人的印章伪造毕业证书，并向议长等人出示，因伪造有印私文书等罪名被在宅起诉。据搜查相关人士称，通过网络搜查对从家中扣押的电脑进行解析后，发现了伪造的毕业证书数据。",
                "grammar": "「〜によると」— 根据…。例：捜査関係者によると（据搜查相关人士）。\n「〜ところ、」— 一…就…。例：解析したところ、見つかった（一解析就发现了）。\n「〜という」— 据说…（传闻）。例：見つかったという（据说被发现了）。",
                "vocab": [["印鑑", "いんかん", "印章"], ["議長", "ぎちょう", "议长、主席"], ["有印私文書偽造", "ゆういんしぶんしょぎぞう", "伪造有印私文書"], ["押収", "おうしゅう", "扣押、没收"], ["解析", "かいせき", "解析"], ["サイバー捜査", "さいばーそうさ", "网络搜查"]]
            },
            {
                "ja": "この事件に関する裁判を巡り、田久保前市長側は無罪を主張する方針を固めた。「本人は卒業証書を作成していない」「印鑑を自ら注文した事実はなく、偽造する動機がない」として、「偽物だとすれば第三者が作成したものである」と主張している。また、百条委員会で虚偽陳述した地方自治法違反罪に関しても無罪を主張する方針だ。",
                "en": "Regarding the trial for this case, the former mayor's side has solidified a policy of pleading not guilty. Claiming that \"she did not create the diploma herself,\" \"there is no fact that she ordered the stamps herself, and she had no motive to forge,\" they argue that \"if the diploma is fake, it was created by a third party.\" She also plans to plead not guilty regarding the charge of violating the Local Autonomy Act for making false statements before the 100-member committee.",
                "literal": "围绕这一事件的审判，田久保前市长一方固化了主张无罪方针。「本人没有制作毕业证书」「没有自己订购印章的事实，没有伪造动机」，并主张「如果证书是赝品，那就是第三者制作的」。另外，关于在百条委员会虚假陈述的地方自治法违反罪，方针也是主张无罪。",
                "grammar": "「〜を巡り」— 围绕…。例：裁判を巡り（围绕审判）。\n「〜として、」— 以…为由、主张…。例：動機がないとして（以没有动机为由）。\n「〜だとすれば」— 如果…的话。例：偽物だとすれば（如果是赝品的话）。",
                "vocab": [["無罪", "むざい", "无罪"], ["動機", "どうき", "动机"], ["第三者", "だいさんしゃ", "第三者"], ["虚偽陳述", "きょぎちんじゅつ", "虚假陈述"], ["百条委員会", "ひゃくじょういいんかい", "百条委员会"], ["地方自治法", "ちほうじちほう", "地方自治法"]]
            },
        ]
    },
    {
        "slug": "suwarippanashi-kenkou",
        "title": "「座りっぱなし」はタバコと同じくらい体に悪い　30分に一度立ち上がろう",
        "subtitle": "from プレジデントオンライン",
        "paras": [
            {
                "ja": "1日8時間以上、座っている人は要注意だ。「タバコと同じくらい体に悪い」と警鐘を鳴らす声が上がるくらい、1日の座位時間が長いほど、健康・早期死亡リスクが高くなると指摘されている。しかも、体勢をあまり変えずに同じところにずっと座ったままでいる「座りっぱなし」は、より深刻だという。",
                "en": "People who sit for more than 8 hours a day should be careful. Voices are raising the alarm that it is \"as bad for the body as tobacco,\" and it is pointed out that the longer one's daily sitting time, the higher the risk to health and early death. Moreover, \"sitting still\" — staying in the same spot without changing posture much — is said to be even more serious.",
                "literal": "每天坐8小时以上的人需要特别注意。「和香烟一样对身体有害」的警钟声高涨，据指出，一天中坐着的时间越长，健康和早逝风险就越高。而且，不怎么改变姿势、一直坐在同一个地方的「久坐不动」据说更为严重。",
                "grammar": "「〜ほど〜」— 越…越…。例：座位時間が長いほどリスクが高くなる（坐着的时间越长风险越高）。\n「〜と指摘されている」— 被指出…。例：高くなると指摘されている（被指出会变高）。\n「〜という」— 据说…。例：より深刻だという（据说更严重）。",
                "vocab": [["要注意", "ようちゅうい", "需要特别注意"], ["警鐘", "けいしょう", "警钟"], ["座位時間", "ざいじかん", "坐着的时间"], ["早期死亡", "そうきしぼう", "早逝"], ["体勢", "たいせい", "姿势"], ["座りっぱなし", "すわりっぱなし", "久坐不动"]]
            },
            {
                "ja": "高齢になると、筋肉量が減って自分の体を支えるのもつらくなり、どうしても座っている時間が長くなりがちだ。座りっぱなし対策のポイントは、主に足全体の血流を滞らせないことだ。定期的に姿勢を変え、30分に一度は立ち上がるようにしよう。テレビのリモコンは手元に置かないなど、こまめに動く工夫も効果的だ。",
                "en": "As people get older, muscle mass decreases, making it harder to support one's own body, and sitting time inevitably tends to become longer. The key to countering sitting still is mainly not letting blood flow in the legs stagnate. Change your posture regularly and stand up once every 30 minutes. Tricks to move frequently, such as not keeping the TV remote at hand, are also effective.",
                "literal": "人上了年纪后，肌肉量减少，支撑自己的身体也变得吃力，坐着的时间难免容易变长。久坐对策的要点，主要是不要让整个腿部的血流停滞。定期改变姿势，每30分钟站起来一次吧。不要把电视遥控器放在手边等，勤活动的小窍门也很有效。",
                "grammar": "「〜がちだ」— 容易…、往往…。例：長くなりがちだ（容易变长）。\n" 
                "「〜ようにしよう」— 尽量做到…。例：立ち上がるようにしよう（尽量做到站起来）。\n「〜など」— …之类、…等。例：リモコンは手元に置かないなど（例如不把遥控器放手边等）。",
                "vocab": [["筋肉量", "きんにくりょう", "肌肉量"], ["支える", "ささえる", "支撑"], ["対策", "たいさく", "对策"], ["血流", "けつりゅう", "血流"], ["滞る", "とどこおる", "停滞、不畅"], ["姿勢", "しせい", "姿势"], ["こまめに", "こまめに", "勤快地"]]
            },
            {
                "ja": "脳の老化を防ぐには、ラジオが大いに役立つ。ラジオを聴く時は、耳で聴いた言葉を想像力でカバーしているので、能動的に脳を使っているからだ。脳科学者の実験では、1カ月間毎日2時間以上ラジオを聴いた結果、イメージを記憶として定着させる力と聴く力が強化されたという。ラジオは脳と心の「元気の源」といえるだろう。",
                "en": "Radio is very useful for preventing brain aging. This is because when listening to radio, one covers the words heard with the ears using imagination, actively using the brain. In an experiment by a brain scientist, listening to radio for more than 2 hours every day for one month strengthened the ability to fix images in memory and the ability to listen. Radio could be called the \"source of energy\" for the brain and heart.",
                "literal": "要防止大脑老化，收音机非常有用。因为听收音机时，是用想象力弥补耳朵听到的语言，所以在主动使用大脑。在大脑科学家的实验中，连续1个月每天听2小时以上收音机的结果是，将形象固定为记忆的能力和聆听能力得到了强化。可以说收音机是大脑和心灵的「活力之源」吧。",
                "grammar": "「〜には」— 要…的话、对于…。例：脳の老化を防ぐには（要防止大脑老化）。\n「〜ので」— 因为…。例：脳を使っているからだ（因为在使用大脑）。\n「〜といえるだろう」— 可以说…吧。例：元気の源といえるだろう（可以说是活力之源吧）。",
                "vocab": [["老化", "ろうか", "老化"], ["大いに", "おおいに", "大大地、非常"], ["想像力", "そうぞうりょく", "想象力"], ["能動的", "のうどうてき", "主动的"], ["記憶", "きおく", "记忆"], ["定着", "ていちゃく", "固定、扎根"], ["強化", "きょうか", "强化"]]
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