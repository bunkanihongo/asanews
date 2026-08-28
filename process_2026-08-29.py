#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-29 (Sat) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-29'
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
        "slug": "neparu-dosekiryu-nihonjin",
        "title": "ネパール土石流 行方不明の日本人5人は大阪の一家か 小学生の子も",
        "subtitle": "from 朝日新聞",
        "paras": [
            {
                "ja": "ネパールと中国の国境沿いで26日に起きた土石流で、行方不明の日本人5人は、大阪市内に住む一家とみられることが28日、関係者らへの取材でわかった。一家は40代の両親と10歳の女児、6歳と3歳の男児。28日夕、子どもの通う小学校の校長らが一家の自宅を訪れ、親族とみられる人が対応していた。",
                "en": "It was learned from interviews with related parties on the 28th that the five missing Japanese people in the landslide that occurred on the 26th along the border between Nepal and China are believed to be a family living in Osaka City. The family consists of parents in their 40s, a 10-year-old girl, and boys aged 6 and 3. On the evening of the 28th, the principal of the school the children attend and others visited the family's home, where a person believed to be a relative responded.",
                "literal": "在26日发生于尼泊尔与中国边境附近的土石流中，失踪的5名日本人，据28日对相关人士的采访得知，被怀疑是住在大阪市内的一家人。这一家是40多岁的父母、10岁女孩、6岁和3岁的男孩。28日傍晚，孩子们就读的小学的校长等人来到他们家，貌似亲属的人在应对。",
                "grammar": "「〜とみられる」— 被认为…、推测为…。例：大阪市内に住む一家とみられる（被推测为住在大阪市内的一家人）。\n「〜らが」— …等人。例：校長らが一家の自宅を訪れ（校长等人到访他们家）。\n「〜こと」— 表示内容/情况的名词化。例：ことが28日、取材でわかった（这一情况于28日通过采访得知）。",
                "vocab": [["土石流", "どせきりゅう", "泥石流"], ["行方不明", "ゆくえふめい", "下落不明、失踪"], ["一家", "いっか", "一家人"], ["国境", "こっきょう", "国境"], ["親族", "しんぞく", "亲属"], ["対応", "たいおう", "应对、接待"]]
            },
            {
                "ja": "子ども同士が小学校の同じクラスという女性によると、子どもたちは毎日一緒に登校していたが、夏休みが明けても登校していなかったという。学校では28日、児童に「ネパールで行方不明になった」との説明があったという。知人らによると、一家の母親は大学で学んだ美術や、介護職の経験を生かし、福祉の分野に絵画や工作のイベントを提供するNPO法人を設立していた。",
                "en": "According to a woman whose child is in the same elementary school class as the children, the children used to walk to school together every day, but had not attended school even after summer vacation ended. At the school on the 28th, students were reportedly told that the children \"went missing in Nepal.\" According to acquaintances, the mother of the family, using the art she studied at university and her experience in caregiving, had established an NPO that provides painting and craft events in the welfare field.",
                "literal": "据孩子与小学生们同班的一位女性说，孩子们每天一起上学，但暑假结束后也没有来上学。学校28日向儿童说明称他们「在尼泊尔下落不明」。据熟人等称，这家母亲运用在大学学到的美术和介护职经验，设立了在福祉领域提供绘画和手工活动的NPO法人。",
                "grammar": "「〜によると」— 据…。例：女性によると（据女性说）。\n「〜が、〜という」— 虽然…但是据说…。例：登校していたが…登校していなかったという（虽然…但据说没有来上学）。\n「〜を生かし」— 运用…、发挥…。例：経験を生かし（发挥经验）。",
                "vocab": [["登校", "とうこう", "上学"], ["児童", "じどう", "儿童、小学生"], ["知人", "ちじん", "熟人"], ["介護", "かいご", "护理、照护"], ["福祉", "ふくし", "福利、福祉"], ["NPO法人", "えぬぴーおーほうじん", "非营利组织法人"]]
            },
            {
                "ja": "行方不明になっている5人の旅行の一部を請け負った旅行会社によると、5人は中国チベット自治区を旅行した後、26日に国境からネパールに入り、車でカトマンズのホテルに向かう予定だった。だが、国境を越えた5人を出迎えた運転手から「旅行者を迎えた」と報告があったのを最後に連絡が途絶え、運転手の行方もわかっていない。",
                "en": "According to a travel agency that handled part of the trip for the five missing people, after traveling through China's Tibet Autonomous Region, the five entered Nepal from the border on the 26th and were scheduled to head by car to a hotel in Kathmandu. However, contact ceased after a report from the driver who greeted the five after they crossed the border saying \"I have picked up the travelers,\" and the driver's whereabouts are also unknown.",
                "literal": "据承接了失踪5人部分旅行安排的旅行社称，5人在中国西藏自治区旅行后，26日从边境进入尼泊尔，预定乘车前往加德满都的酒店。但是，以迎接越境5人的司机报告称「已接到旅行者」为最后联系中断，司机也下落不明。",
                "grammar": "「〜を請け負った」— 承揽、承接了…。例：旅行の一部を請け負った（承接了部分旅行）。\n「〜予定だった」— 预定…、打算…。例：ホテルに向かう予定だった（预定前往酒店）。\n「〜のを最後に」— 以…为最后（界限）。例：報告があったのを最後に（以报告为最后）。",
                "vocab": [["請け負う", "うけおう", "承揽、包办"], ["自治区", "じちく", "自治区"], ["予定", "よてい", "预定、计划"], ["国境を越える", "こっきょうをこえる", "越过国境"], ["出迎え", "でむかえ", "迎接"], ["途絶える", "とだえる", "中断、断绝"]],
            },
        ]
    },
    {
        "slug": "iran-saikou-shidousha-ginen",
        "title": "開戦半年後も姿見せないイラン最高指導者 健康と実権に疑念",
        "subtitle": "from ロイター",
        "paras": [
            {
                "ja": "イランの最高指導者モジタバ・ハメネイ師はイラン戦争の開戦から半年が経過した今も国民の前に一度も姿を見せず、肉声も伝わっていないことから、健康状態や実権を巡る疑念が一段と深まっている。ハメネイ師から国民へのメッセージは、ニュースキャスターが読み上げた数件の声明に限られる。",
                "en": "Even half a year after the start of the Iran war, Iran's supreme leader Mojtaba Khamenei has not once appeared before the people, and his voice has not been heard, deepening suspicions over his health and actual power. Messages from Khamenei to the people have been limited to a few statements read aloud by news anchors.",
                "literal": "伊朗最高领袖莫吉塔巴・哈梅内伊即使伊朗战争开战已过半年，至今也一次都没有在国民面前露面，声音也没有传出，因此围绕其健康状况和实权的疑虑进一步加深。从哈梅内伊给国民的信息，仅限由新闻主播宣读的几份声明。",
                "grammar": "「〜から」— 因为…（表示原因）。例：伝わっていないことから（因为没有传出声音）。\n" 
                "「〜を巡る」— 围绕…。例：実権を巡る疑念（围绕实权的疑虑）。\n「〜に限られる」— 仅限于…。例：声明に限られる（仅限于声明）。",
                "vocab": [["最高指導者", "さいこうしどうしゃ", "最高领袖"], ["開戦", "かいせん", "开战"], ["経過", "けいか", "经过、流逝"], ["肉声", "にくせい", "真人声音"], ["実権", "じっけん", "实权"], ["声明", "せいめい", "声明"]]
            },
            {
                "ja": "政府高官や内部事情に詳しい関係者は、暗殺への懸念が不在の理由だと説明する。ハメネイ師は空爆で受けた顔の傷の治療を続ける間、日常的な権限の多くを少数の最高幹部に委ねているという。側近筋は、ハメネイ師の健康状態は大幅に改善しており、思考は明晰で、意思決定にも関与していると説明した。",
                "en": "Senior government officials and sources familiar with internal affairs explain that concern about assassination is the reason for his absence. It is said that while Khamenei continues treatment for facial injuries suffered in an airstrike, he has delegated much of his daily authority to a small number of top officials. Sources close to him say his health has improved considerably, his thinking is clear, and he remains involved in decision-making.",
                "literal": "政府高官和熟悉内情的相关人士说明，对暗杀的担忧是不露面（缺席）的理由。据说在哈梅内伊继续治疗空袭所受的脸部伤期间，把日常权限中的大部分委托给少数最高干部。身边人士说明，哈梅内伊的健康状态大幅改善，思路清晰，也参与决策。",
                "grammar": "「〜と説明する」— 说明…。例：不在の理由だと説明する（说明是不露面的理由）。\n「〜を委ねている」— 委托给…。例：権限の多くを最高幹部に委ねている（把大部分权限委托给最高干部）。\n「〜筋」— …方面（的人）。例：側近筋（身边人士）。",
                "vocab": [["政府高官", "せいふこうかん", "政府高官"], ["暗殺", "あんさつ", "暗杀"], ["懸念", "けねん", "担忧"], ["空爆", "くうばく", "空袭轰炸"], ["権限", "けんげん", "权限"], ["側近", "そっきん", "亲信、身边人"]]
            },
            {
                "ja": "ただ、イランの最強硬派の支持者の間にも疑念が広がりつつある。民兵組織「バシジ」の隊員は「国民がもっと安心できるよう、最高指導者の声を聞くか、最高指導者が指揮を執っていることを示す何らかの証拠を見る必要がある」と語った。写真１枚すら公表されていないことが、士気を損ない、イランの国益にもならないと述べた。",
                "en": "However, doubts are also spreading among supporters of Iran's hardest-line faction. A member of the volunteer militia \"Basij\" said, \"To make the people feel more at ease, we need to hear the supreme leader's voice or see some evidence showing that the supreme leader is in command.\" He stated that not even a single photo being released harms morale and does not serve Iran's national interest.",
                "literal": "但是，在伊朗最强硬派的支持者之间，疑虑也在扩散中。民兵组织「巴斯基」的队员说「为了让国民更加安心，需要听取最高领袖的声音，或者看到显示最高领袖在掌权的某种证据」。他陈述说，连一张照片都没有公布，会损害士气，也不利于伊朗的国家利益。",
                "grammar": "「〜つつある」— 正在…（表示进行）。例：疑念が広がりつつある（疑虑正在扩散）。\n「〜よう」— 为了…（目的）。例：安心できるよう（为了让其安心）。\n「〜すら」— 连…都…。例：写真１枚すら公表されていない（连一张照片都没公布）。",
                "vocab": [["強硬派", "きょうこうは", "强硬派"], ["民兵", "みんぺい", "民兵"], ["士気", "しき", "士气"], ["証拠", "しょうこ", "证据"], ["国益", "こくえき", "国家利益"], ["指揮を執る", "しきをとる", "掌权、指挥"]]
            },
        ]
    },
    {
        "slug": "sandwich-itate-noukousoku",
        "title": "サンドウィッチマン伊達みきお 脳梗塞で活動休止 相方・富澤が現状報告",
        "subtitle": "from 日刊スポーツ",
        "paras": [
            {
                "ja": "お笑いコンビ「サンドウィッチマン」の伊達みきお（51）が脳梗塞のため入院、治療していると28日、公式サイトで発表された。発表では「弊社所属のサンドウィッチマン伊達みきおが、先日、体調不良を訴え病院で検査を受けたところ、脳梗塞と診断されました」と報告。「医療関係者の皆様に迅速にご対応いただいたこともあり、幸い大事には至らず、現在は入院治療を受けております」と説明した。",
                "en": "It was announced on the official website on the 28th that Date Mikio (51) of the comedy duo \"Sandwich Man\" is hospitalized and undergoing treatment for a cerebral infarction. The announcement reported, \"Our affiliated Sandwich Man member Date Mikio recently complained of feeling unwell, and when he was examined at the hospital, he was diagnosed with a cerebral infarction.\" It explained, \"Thanks to the prompt response of the medical staff, fortunately it did not become serious, and he is currently receiving treatment in the hospital.\"",
                "literal": "搞笑组合「三明治人」的伊达干生（51）因脑梗塞入院、正在治疗，28日通过官网发布。发布中报告称「本公司所属的三明治人成员伊达干生，前几天主诉身体不适，在医院接受检查后，被诊断为脑梗塞」。并说明「承蒙医疗相关人士迅速应对，所幸未发展到严重地步，现在正接受住院治疗」。",
                "grammar": "「〜ため」— 因为…。例：脳梗塞のため入院（因脑梗塞而住院）。\n「〜たところ」— 结果发现…。例：検査を受けたところ診断されました（接受检查后发现被诊断为…）。\n「〜にもかかわらず／〜こともあり」— 也因为…。例：迅速にご対応いただいたこともあり（也因为承蒙迅速应对）。",
                "vocab": [["脳梗塞", "のうこうそく", "脑梗塞"], ["活動休止", "かつどうきゅうし", "暂停活动"], ["体調不良", "たいちょうふりょう", "身体不适"], ["診断", "しんだん", "诊断"], ["迅速", "じんそく", "迅速"], ["大事に至らない", "だいじにいたらない", "不至于严重"]]
            },
            {
                "ja": "伊達の脳梗塞を受け、相方の富澤たけし（52）が自身のブログを更新。「病名を聞くとショックを受ける方もいらっしゃると思いますが、早期発見だった為に頭も体も元気なので院内を歩いたり、食事が足りないと増量を要求したり、よくメールのやり取りもしています」と伊達の近況を報告した。",
                "en": "In response to Date's cerebral infarction, his partner Tomizawa Takeshi (52) updated his own blog. He reported on Date's recent condition, saying, \"Some people may be shocked to hear the name of the illness, but because it was discovered early, his head and body are fine, so he walks around the hospital, asks for more food when it's not enough, and we frequently exchange emails.\"",
                "literal": "得知伊达的脑梗塞后，搭档富泽武志（52）更新了自己的博客。「听到病名时，有些人可能会受到打击，但因为早期发现，头脑和身体都很健康，所以在医院内走动，食物不够了就要求加量，也常进行邮件往来」，他报告了伊达的近况。",
                "grammar": "「〜を受け」— 鉴于…、因…而。例：伊達の脳梗塞を受け（因伊达的脑梗塞）。\n「〜為に」— 因为…（因为是早期发现）。例：早期発見だった為に（因为是早期发现）。\n「〜たり〜たり」— 又…又…。例：歩いたり、増量を要求したり（又走动又要求加量）。",
                "vocab": [["相方", "あいかた", "搭档、伙伴"], ["更新", "こうしん", "更新"], ["早期発見", "そうきはっけん", "早期发现"], ["増量", "ぞうりょう", "增加分量"], ["やり取り", "やりとり", "往来、交流"], ["近況", "きんきょう", "近况"]]
            },
            {
                "ja": "さらに富澤は「暇だろうと思って病院の怖い話の動画を送ったら『ふざけんなマジで！霊安室近いんだぞ！』と、病人とは思えないツッコミメールもいただきました」とつづった。また、予定されていたライブツアーは中止となった。富澤は「相方が帰ってくる場所が無いと困るので、しばらく1人で活動する姿を温かく見守ってもらえたら幸いです」と呼びかけた。",
                "en": "Furthermore, Tomizawa wrote, \"Thinking he'd be bored, I sent him a video of scary hospital stories, and I got a comeback email that doesn't sound like it's from a sick person: 'Don't mess with me! I'm near the morgue!'\" Also, the scheduled live tour was cancelled. Tomizawa appealed, \"I'd be in trouble if there were no place for my partner to come back to, so I'd be glad if you could warmly watch over me working alone for a while.\"",
                "literal": "此外富泽写道「想着他会无聊，送了他医院恐怖故事的视频，结果收到了『别开玩笑了，真的！离太平间很近啊！』这样不像病人会说出的吐槽邮件」。另外，预定的巡演演唱会也中止了。富泽呼吁道「如果搭档没有回来的地方会很困扰，所以若能温暖地守护我暂时一个人活动的样子就太好了」。",
                "grammar": "「〜たら〜た」— 一…就…。例：送ったら…メールもいただきました（一送去就收到了…邮件）。\n「〜と思えない」— 不像…、难以认为…。例：病人とは思えない（不像病人）。\n「〜てもらえたら幸い」— 若能…就太好了。例：見守ってもらえたら幸いです（若能守护就太好了）。",
                "vocab": [["怖い話", "こわいはなし", "可怕的故事、恐怖故事"], ["ツッコミ", "つっこみ", "吐槽、插科打诨"], ["霊安室", "れいあんしつ", "太平间、停尸房"], ["ライブツアー", "らいぶつあー", "演唱会巡演"], ["中止", "ちゅうし", "中止、取消"], ["見守る", "みまもる", "守护、守望"]]
            },
        ]
    },
    {
        "slug": "nipponham-reyes-zanryuu",
        "title": "日本ハム・レイエス 異例の残留訴え 「ここは僕の居場所」「一緒に優勝を」",
        "subtitle": "from デイリースポーツ",
        "paras": [
            {
                "ja": "「日本ハム６－４ロッテ」日本ハムが逆転勝ちで２連勝。貯金１２とした。２打席連発５打点の活躍をみせたレイエスは試合後、お立ち台で来季以降の残留を力強くファンに訴えた。レイエスは「（三回の本塁打は）小島投手のカットがすごくよかったが、いいスイングができた。いいホームランになったと思います」と笑顔で振り返った。",
                "en": "In the game Nippon-Ham 6-4 Lotte, Nippon-Ham won a come-from-behind victory for their second straight win, improving their balance to +12. Reyes, who starred with home runs in two straight at-bats and five RBIs, strongly appealed to fans after the game on the victory stage to stay with the team beyond next season. Reyes recalled with a smile, \"(My home run in the third inning) Kozushima's cutter was really good, but I managed a good swing. I think it became a good home run.\"",
                "literal": "「日本火腿6-4罗德」。日本火腿逆转获胜取得二连胜。储蓄（胜数减败数）达到12。展现连续两个打席开轰、5分打点的活跃表现的雷耶斯，赛后在上台受访的台上，向粉丝强力呼吁下赛季以后的留队。雷耶斯笑着回顾说「（三局的本垒打）小岛投手的外角切球非常好，但我做出了好的挥棒。我觉得打出了一个漂亮的本垒打」。",
                "grammar": "「〜で２連勝」— 以…取得二连胜。例：逆転勝ちで２連勝（以逆转获胜取得二连胜）。\n「〜をみせた」— 展现了…。例：活躍をみせた（展现了活跃表现）。\n「〜と思います」— 我认为…。例：いいホームランになったと思います（我认为成为了漂亮的本垒打）。",
                "vocab": [["逆転勝ち", "ぎゃくてんがち", "逆转获胜"], ["貯金", "ちょきん", "（棒球）胜差、储蓄"], ["打席連発", "だせきれんぱつ", "连续打席开轰"], ["打点", "だてん", "打点、得分"], ["お立ち台", "おたちだい", "（棒球）采访台、领奖台"], ["残留", "ざんりゅう", "留队、留下"]]
            },
            {
                "ja": "その後、レイエスは座りこんで「心から皆さんは、僕と僕の家族にすごく特別な場所を作ってくれたと思っています。北海道の皆さん、ファイターズの皆さんは全員家族だと思っています。ここは僕たちの家、ここは僕の居場所です。僕はここにずっといたいと思っています」と、「フォーエバー」を繰り返しながら力強く来季以降の残留を訴えた。",
                "en": "Afterward, Reyes sat down and strongly appealed to stay with the team beyond next season, repeating \"forever\": \"From the bottom of my heart, I feel you have created a really special place for me and my family. All of you in Hokkaido, all of the Fighters, are family. This is our home, this is where I belong. I want to stay here forever.\"",
                "literal": "之后，雷耶斯坐下来，一边反复说「永远」，一边强力呼吁下赛季以后的留队：「我由衷地觉得，大家为我、为我的家人创造了一个非常特别的地方。北海道的各位、日本火腿的各位，我认为全员都是家人。这里是我们家，这里是我的归属地。我想永远留在这里」。",
                "grammar": "「〜てくれた」— （为我）做了…。例：場所を作ってくれた（为我创造了地方）。\n「〜と思っています」— 我一直认为…。例：全員家族だと思っています（我认为全员都是家人）。\n" 
                "「〜に訴えた」— 向…呼吁。例：残留を訴えた（呼吁留队）。",
                "vocab": [["心から", "こころから", "由衷地"], ["特別", "とくべつ", "特别"], ["居場所", "いばしょ", "归属地、容身之处"], ["繰り返す", "くりかえす", "反复"], ["力強く", "ちからづよく", "有力地"], ["訴える", "うったえる", "呼吁、诉求"]]
            },
            {
                "ja": "そして、立ち上がると「素晴らしい監督、素晴らしいコーチ、素晴らしい選手の皆さん、素晴らしいファンの皆さんと素晴らしいことを成し遂げることができる。最後の１日まで諦めません。これからも戦い続けて一緒に優勝を掴みとりましょう」と、約２分３０秒にわたって訴えた。その後の取材でレイエスは「ファイターズが好きでファイターズに居たいっていうのはみなさんご存知だと思うんですけど、やっぱりそこは自分のコントロールできる範囲ではないので」と、発言の真意を明かした。",
                "en": "Then, standing up, he appealed for about two minutes and 30 seconds: \"We can achieve something great with our wonderful manager, wonderful coaches, wonderful players, and wonderful fans. We won't give up until the very last day. Let's keep fighting and grab the championship together.\" In a later interview, Reyes revealed his true intention: \"Everyone knows I love the Fighters and want to stay with the Fighters, but after all, that's not something within my control.\"",
                "literal": "然后，一站起来就说「能与出色的教练、出色的教练组（复数）、出色的各位选手、出色的各位粉丝成就出色的事情。直到最后一天也不放弃。今后也将继续战斗，一起夺得优胜吧」，持续呼吁了约2分30秒。在之后的采访中，雷耶斯透露发言的真意说「大家应该都知道我喜欢日本火腿、想留在日本火腿，但那毕竟不在自己能控制的范围内」。",
                "grammar": "「〜と立ち上がると」— 一站起来就…。例：立ち上がると…と訴えた（一站起来就…呼吁）。\n「〜ましょう」— 一起…吧（劝诱）。例：一緒に優勝を掴みとりましょう（一起夺得优胜吧）。\n「〜んですが、〜ので」— 虽然…但是因为…。例：ご存知だと思うんですけど、範囲ではないので（虽然我想大家都知道，但因为不在范围内）。",
                "vocab": [["成し遂げる", "なしとげる", "实现、完成"], ["諦める", "あきらめる", "放弃"], ["優勝", "ゆうしょう", "夺冠、冠军"], ["掴み取る", "つかみとる", "夺得、抓到"], ["真意", "しんい", "真意、真实意图"], ["コントロール", "こんとろーる", "控制"]]
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
