#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-17 (Mon) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-17'
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
        "slug": "sakasama-taifuu-chiba-gouu",
        "title": "いつもと違う今年の夏 異例の逆走台風と千葉豪雨はなぜ起きた？カギは“夏の太平洋高気圧”",
        "subtitle": "from TBS NEWS DIG",
        "paras": [
            {
                "ja": "2026年の夏はいつもの夏と違う状況です。その一つが、8月13日の千葉豪雨です。千葉県では大雨特別警報が発表され、24時間の雨量は千葉市で8月の観測史上1位となる367ミリ、平年の8月1か月分の3倍を超える雨の量となりました。500ミリを超えたところもあります。記録的な大雨となったポイントが「大量の湿った空気」と「風向き」です。",
                "en": "The summer of 2026 is different from usual. One example is the heavy rain in Chiba on August 13th. A heavy rain emergency warning was issued in Chiba Prefecture, and the 24-hour rainfall in Chiba City reached 367 mm, the highest ever recorded for August, more than three times the normal amount for an entire August. Some areas exceeded 500 mm. The keys to the record rain were \"a large amount of moist air\" and \"wind direction.\"",
                "literal": "2026年的夏天与往常不同。其中一个就是8月13日的千叶暴雨。千叶县发布了暴雨特别警报，千叶市24小时降雨量达到8月观测史上第1位的367毫米，超过往年8月整个月降雨量的3倍。也有超过500毫米的地方。创纪录暴雨的关键点是“大量潮湿空气”和“风向”。",
                "grammar": "「〜とは違う」— 与…不同。例：いつもの夏と違う状況（与平常夏天不同的状况）。\n「〜としても」— 作为…也…。例：観測史上1位となる（成为观测史上第1位）。\n「〜を超える」— 超过…。例：3倍を超える（超过3倍）。",
                "vocab": [["豪雨", "ごうう", "暴雨、豪雨"], ["特別警報", "とくべつけいほう", "特别警报"], ["観測史上", "かんそくしじょう", "观测史上"], ["平年", "へいねん", "常年、平年"], ["湿った", "しめった", "潮湿的"], ["風向き", "かざむき", "风向"]]
            },
            {
                "ja": "この湿った空気を運んできたのが、逆走した台風15号です。夏の太平洋高気圧が北に張り出していたため、台風15号はその縁に沿うように東から西へと進む異例の進路となって、茨城県に初めて上陸しました。この台風が大量の湿った空気を吹き込んできたのです。",
                "en": "The tropical depression that carried this moist air was Typhoon No. 15, which reversed its path. Because the summer Pacific high-pressure system had extended northward, Typhoon No. 15 took the unusual route of traveling from east to west along its edge, making landfall in Ibaraki Prefecture for the first time. This typhoon blew in a vast amount of moist air.",
                "literal": "带来这些潮湿空气的，是逆向移动的台风15号。由于夏季太平洋高气压向北延伸，台风15号沿着其边缘从东向西推进，形成罕见的路径，首次登陆茨城县。这个台风吹来了大量潮湿空气。",
                "grammar": "「〜のが、〜です」— 是…的（提示主语）。例：運んできたのが、台風15号です（运来湿气的是台风15号）。\n「〜ため」— 因为…。例：高気圧が張り出していたため（因为高气压向北延伸）。\n「〜に沿うように」— 沿着…那样。例：縁に沿うように進む（沿着边缘推进）。",
                "vocab": [["逆走", "ぎゃくそう", "逆行、反向行进"], ["張り出す", "はりだす", "向外延伸"], ["縁", "ふち", "边缘"], ["異例", "いれい", "例外、破例"], ["進路", "しんろ", "路径、行进路线"], ["上陸", "じょうりく", "登陆"]]
            },
            {
                "ja": "そもそもなぜ台風が逆走したり、立て続けに発生したりしているのかというと、夏の太平洋高気圧が北に偏っていて、この縁で吹く東風と南西の季節風という2つの風によって「大きな反時計回りの循環」ができていたからです。いつもは台風をブロックする高気圧があるはずの場所で、台風が発生しやすい状況だったのです。",
                "en": "As for why typhoons have been reversing direction or forming one after another in the first place, it is because the summer Pacific high-pressure system was shifted northward, and the two winds blowing along its edge — the easterly wind and the southwest seasonal wind — created a \"large counterclockwise circulation.\" In the place where the high-pressure system that usually blocks typhoons should be, conditions were favorable for typhoons to form.",
                "literal": "要说为什么台风逆向行进或接连不断发生，是因为夏季太平洋高气压偏北，在其边缘吹的东风和西南季风这两种风形成了“大的逆时针循环”。在平时本应有阻挡台风的太平洋高气压的地方，反而成了台风容易发生的状况。",
                "grammar": "「〜といいますと、〜からです」— 要说…，（是因为）…。例：なぜ逆走しているのかというと…からです（要说为何逆行，是因为…）。\n「〜たり〜たり」— 又…又…。例：逆走したり、発生したり（逆向移动、接连发生）。\n「〜はずの場所」— 本应…的地方。例：高気圧があるはずの場所（本应有高气压的地方）。",
                "vocab": [["そもそも", "そもそも", "说到底、本来"], ["立て続け", "たてつづけ", "接连不断"], ["偏る", "かたよる", "偏向、偏斜"], ["季節風", "きせつふう", "季节风"], ["反時計回り", "はんとけいまわり", "逆时针"], ["循環", "じゅんかん", "循环"]]
            },
            {
                "ja": "ただ、このあと次第に高気圧はいつもの場所に戻ってきそうです。日差しが戻って、厳しい残暑になりそうです。大雨の被害を受けた地域では、土砂災害や川の増水などに引き続き注意が必要です。",
                "en": "However, the high-pressure system looks set to gradually return to its usual position after this. Sunshine should return, and it looks set to become a severe late-summer heat. In areas that suffered heavy rain damage, continued caution is needed against landslides and rising rivers.",
                "literal": "只是，此后太平洋高气压似乎会逐渐回到平常的位置。阳光回归，似乎会变成严酷的残暑。在遭受暴雨灾害的地区，仍需持续注意泥石流灾害和河水上涨等。",
                "grammar": "「〜そうです」— 看起来…。例：戻ってきそうです（似乎会回来）。\n「〜になりそうです」— 似乎将变成…。例：残暑になりそうです（似乎将变成残暑）。\n「〜が必要です」— 有必要…。例：引き続き注意が必要です（有必要持续注意）。",
                "vocab": [["次第に", "しだいに", "逐渐地"], ["日差し", "ひざし", "阳光"], ["残暑", "ざんしょ", "残暑、初秋的炎热"], ["土砂災害", "どしゃさいがい", "泥石流灾害"], ["増水", "ぞうすい", "涨水"], ["注意", "ちゅうい", "注意"]]
            },
        ]
    },
    {
        "slug": "openai-keiei-kanbu-taisya",
        "title": "オープンAIで経営幹部が相次ぎ退社 半年前加入の「中心人物」も…新規株式公開前に「危険信号」",
        "subtitle": "from 読売新聞オンライン",
        "paras": [
            {
                "ja": "対話型AIサービス「チャットGPT」を手がける米オープンAIで、経営幹部の退社が相次いでいます。米国や中国の同業との競争が激化しており、背景には収益向上への対応がありそうです。年内にも新規株式公開（IPO）に踏み切る可能性がある中、経営体制の不安定さが懸念材料となっています。",
                "en": "At OpenAI, the U.S. company behind the conversational AI service \"ChatGPT,\" a series of executives are leaving. Competition with rivals in the U.S. and China is intensifying, and there appears to be a response to improving revenue behind the departures. With the possibility of an initial public offering (IPO) as early as within the year, the instability of the management structure has become a concern.",
                "literal": "在推出对话式AI服务“ChatGPT”的美国OpenAI中，经营高管接连离职。与美国和中国的同行竞争正在激化，背景似乎是对提升收益的应对。在年内可能就要进行首次公开募股（IPO）的情况下，经营体制的不稳定成为令人担忧的因素。",
                "grammar": "「〜を手がける」— 从事…、经营…。例：チャットGPTを手がける（经营ChatGPT）。\n「〜が相次いでいます」— 接连不断地…。例：経営幹部の退社が相次いでいます（经营高管接连离职）。\n「〜ている」— （状态）正在…。例：競争が激化しています（竞争正在激化）。",
                "vocab": [["対話型", "たいわがた", "对话型、交互式"], ["経営幹部", "けいえいかんぶ", "经营高管"], ["相次ぐ", "あいつぐ", "相继、接连发生"], ["激化", "げきか", "激化"], ["収益", "しゅうえき", "收益"], ["懸念材料", "けねんざいりょう", "令人担忧的因素"]]
            },
            {
                "ja": "法人向け事業を担当する最高収益責任者の女性が13日、従業員に宛てたメッセージで退社を告げ、突然の発表に驚きが広がりました。この女性は2025年12月に別のIT企業のCEOから転じたばかりで、収益拡大を担う中心人物とみなされていたからです。その2日前には元最高執行責任者の男性も「新しいことを始める」と退社を表明しました。",
                "en": "On the 13th, the chief revenue officer in charge of the enterprise business announced her departure in a message to employees, and the sudden announcement caused surprise. She had just moved from being CEO of another IT company in December 2025 and was regarded as a central figure responsible for expanding revenue. Two days earlier, a former chief operating officer also announced his departure, saying he would \"start something new.\"",
                "literal": "负责企业业务的最高收益责任人的女性于13日在发给员工的讯息中宣布离职，这一突然发表令人们感到震惊。因为这名女性2025年12月刚从中途转任，是另一家IT企业的CEO，被认为是负责收益扩大的核心人物。在那之前两天，前最高执行责任人的男性也表示“要开始新的尝试”而宣布离职。",
                "grammar": "「〜に宛てた」— 寄给…的。例：従業員に宛てたメッセージ（寄给员工的讯息）。\n「〜たばかりで」— 刚刚…。例：転じたばかりで（刚刚转任）。\n「〜とみなされていた」— 被认为是…。例：中心人物とみなされていた（被认为是核心人物）。",
                "vocab": [["法人向け", "ほうじんむけ", "面向企业"], ["最高収益責任者", "さいこうしゅうえきせきにんしゃ", "首席营收官(CRO)"], ["従業員", "じゅうぎょういん", "员工"], ["転じる", "てんじる", "转任、转变"], ["中心人物", "ちゅうしんじんぶつ", "核心人物"], ["退社", "たいしゃ", "离职、离开公司"]]
            },
            {
                "ja": "AI業界では人材の引き抜きが激しく、幹部や有力研究者の移籍は珍しくありません。ただ、「Cスイート」と称される最高幹部らの短期間での相次ぐ退社は、業界内でも異例の事態と受け止められています。AI新興企業の創業者で、業界に詳しい人物はX（旧ツイッター）に「IPOを前に大きな危険信号だ」と投稿しました。",
                "en": "In the AI industry, poaching of talent is fierce, and moves of executives and leading researchers are not unusual. However, the successive departures of top executives, the so-called \"C-suite,\" over a short period is being taken as an unusual situation even within the industry. A founder of an AI startup who is familiar with the industry posted on X (formerly Twitter), \"This is a big danger signal ahead of the IPO.\"",
                "literal": "在AI行业，人才挖角激烈，高管和知名研究人员的转职并不罕见。只是，被称为“C套房（最高管理层）”的最高干部们在短期内相继离职，在行业内也被视为异例的事态。熟悉行业的AI初创企业创始人也在X（原推特）上发文称“IPO之前这是巨大的危险信号”。",
                "grammar": "「〜が激しく」— …很激烈。例：引き抜きが激しく（挖角激烈）。\n「〜と受け止められています」— 被视为…。例：異例の事態と受け止められています（被视为异例事态）。\n「〜に詳しい」— 精通…、熟悉…。例：業界に詳しい人物（熟悉行业的人物）。",
                "vocab": [["引き抜き", "ひきぬき", "挖角、挖走"], ["有力研究者", "ゆうりょくけんきゅうしゃ", "知名研究者"], ["移籍", "いせき", "转会、跳槽"], ["異例", "いれい", "异例、破例"], ["受け止める", "うけとめる", "理解、领会"], ["新興企業", "しんこうきぎょう", "新兴企业、初创企业"]]
            },
            {
                "ja": "オープンAIを取り巻く環境は厳しさを増しています。収益拡大の要となる法人向け事業は、米アンソロピックに先行され、低価格モデルでは中国勢の追い上げを受けています。市場では、相次ぐ幹部の退社が、オープンAIに対する投資家の信頼や上場時の企業価値の評価に影響しかねないとの懸念も出ています。",
                "en": "The environment surrounding OpenAI is growing harsher. In the enterprise business, the key to revenue growth, it has been overtaken by U.S. rival Anthropic, and in low-priced models it is being pressured by Chinese players. On the market, there are concerns that the successive departures of executives could affect investors' trust in OpenAI and the valuation of the company at the time of listing.",
                "literal": "围绕OpenAI的环境正变得更加严峻。作为收益扩大的关键的企业业务被美国Anthropic领先，在低价模型上又受到中国势力的追赶。市场上也出现了担忧：相继的高管离职可能影响投资者对OpenAI的信任以及上市时企业价值的评价。",
                "grammar": "「〜を取り巻く」— 围绕…。例：オープンAIを取り巻く環境（围绕OpenAI的环境）。\n「〜に先行され」— 被…领先。例：アンソロピックに先行され（被Anthropic领先）。\n「〜かねない」— 有可能…（负面）。例：影響しかねない（有可能影响）。",
                "vocab": [["取り巻く", "とりまく", "围绕、环绕"], ["厳しさを増す", "きびしさをます", "更加严峻"], ["追い上げ", "おいあげ", "追赶、紧逼"], ["投資家", "とうしか", "投资者"], ["上場", "じょうじょう", "上市"], ["企業価値", "きぎょうかち", "企业价值"]]
            },
        ]
    },
    {
        "slug": "bbq-kawa-nagare-josei-jyushou",
        "title": "友人とのBBQ中に川に流される 20代女性が心肺停止 埼玉・飯能市",
        "subtitle": "from テレビ朝日系（ANN）",
        "paras": [
            {
                "ja": "埼玉県飯能市で、20代の女性が川に流され、心肺停止の重体となっています。16日午後4時45分ごろ、飯能市の高麗川で「20代の女性が川に流された」と、友人の30代の女性から通報がありました。",
                "en": "In Hanno City, Saitama Prefecture, a woman in her twenties was swept away in a river and is in critical condition with cardiac and respiratory arrest. Around 4:45 p.m. on the 16th, there was a report from a friend in her thirties that \"a woman in her twenties was swept away in a river\" on the Koma River in Hanno City.",
                "literal": "在埼玉县饭能市，一名20多岁的女性被河水冲走，处于心肺停止的重症状态。16日下午4点45分左右，在饭能市的高丽川，一名30多岁的女性朋友报警称“20多岁的女性被河水冲走了”。",
                "grammar": "「〜ごろ」— …左右。例：午後4時45分ごろ（下午4点45分左右）。\n「〜と通報がありました」— 接到…的报警。例：川に流されたと通報がありました（接到被河水冲走的报警）。\n「〜ています」— （状态）正在…。例：心肺停止の重体となっています（处于心肺停止的重症状态）。",
                "vocab": [["流される", "ながされる", "被冲走"], ["心肺停止", "しんぱいていし", "心肺停止"], ["重体", "じゅうたい", "重症、危重"], ["通報", "つうほう", "报警、通报"], ["高麗川", "こまがわ", "高丽川（河名）"], ["友人", "ゆうじん", "朋友"]]
            },
            {
                "ja": "警察などによりますと、友人とバーベキューをしていた女性が、川の岩の上で遊んでいたところ、水かさが急に増して流されたということです。女性は、川に落下した場所から下流におよそ500メートル流されたところで友人に救出されましたが、心肺停止の重体です。警察は事故の詳しい原因を調べています。",
                "en": "According to police and others, the woman, who was having a barbecue with friends, was playing on a rock in the river when the water level suddenly rose and she was swept away. She was rescued by her friends about 500 meters downstream from where she fell into the river, but she is in critical condition with cardiac and respiratory arrest. Police are investigating the detailed cause of the accident.",
                "literal": "据警方等称，与朋友一起烧烤的女性在河中的岩石上玩耍时，水位突然上涨而被冲走。女性在落入河中的位置下游约500米处被朋友救出，但处于心肺停止的重症状态。警方正在调查事故的详细原因。",
                "grammar": "「〜ところ」— 正在…的时候。例：遊んでいたところ（正在玩耍时）。\n「〜ということです」— 据说…。例：流されたということです（据说被冲走了）。\n「〜の重体です」— 处于…的重症状态。例：心肺停止の重体です（处于心肺停止的重症状态）。",
                "vocab": [["バーベキュー", "ばーべきゅー", "烧烤、BBQ"], ["水かさ", "みずかさ", "水位、水量"], ["急に", "きゅうに", "突然、急剧"], ["落下", "らっか", "落下、掉落"], ["下流", "かりゅう", "下游"], ["救出", "きゅうしゅつ", "救出"]]
            },
        ]
    },
    {
        "slug": "beiran-iran-husantei-koutyaku",
        "title": "米イラン「不安定な膠着」 覚書期限、海峡開放見えず",
        "subtitle": "from 共同通信",
        "paras": [
            {
                "ja": "米国とイランは、戦闘終結に向けた最終合意の交渉期限とされる16日を迎えました。期限は延長可能ですが、両国が6月17日に結んだ覚書は形骸化し、双方は期限延長にも言及していません。エネルギー輸送の要衝ホルムズ海峡の開放に向けてイランとオマーンが協議を続けますが、正常化は遠く、「不安定な膠着状態」が長期化するとの見方が強まっています。",
                "en": "The U.S. and Iran reached the 16th, which is considered the deadline for final-agreement negotiations aimed at ending hostilities. The deadline can be extended, but the memorandum the two countries signed on June 17 has become hollow, and neither side has even mentioned extending the deadline. Iran and Oman will continue talks toward opening the Strait of Hormuz, a key point for energy transport, but normalization is far off, and the view that the \"unstable deadlock\" will be prolonged is strengthening.",
                "literal": "美国与伊朗迎来了被视作战斗终结最终协议谈判期限的16日。期限可以延长，但两国6月17日缔结的备忘录已形同虚设，双方都未提及延期。为开放能源运输要冲霍尔木兹海峡，伊朗与阿曼将继续协商，但正常化遥遥无期，“不稳定胶着状态”长期化的看法正在加强。",
                "grammar": "「〜に向けた」— 面向…的。例：戦闘終結に向けた合意（面向战争终结的协议）。\n「〜とされる」— 被认为是…。例：交渉期限とされる（被认为是谈判期限）。\n「〜との見方が強まっています」— …的看法正在加强。例：長期化するとの見方が強まっています（长期化的看法在加强）。",
                "vocab": [["戦闘終結", "せんとうしゅうけつ", "战争终结"], ["覚書", "おぼえがき", "备忘录"], ["形骸化", "けいがいか", "形骸化、有名无实"], ["言及", "げんきゅう", "提及、言及"], ["要衝", "ようしょう", "要冲、咽喉要地"], ["膠着状態", "こうちゃくじょうたい", "胶着状态、僵局"]]
            },
            {
                "ja": "トランプ米大統領は事態打開への道筋を描けておらず、原油やガソリン価格は高止まりしています。ホルムズ海峡は世界の原油輸送の約5分の1が通過する重要な場所で、イランが通行を妨げる威嚇を続けてきたことが、国際的な原油価格の上昇を招いてきました。",
                "en": "U.S. President Trump has not laid out a path to resolve the situation, and crude oil and gasoline prices remain high. The Strait of Hormuz is an important location through which about one-fifth of the world's crude oil shipments pass, and Iran's continued threats to hinder passage have contributed to rising international crude oil prices.",
                "literal": "美国特朗普总统未能绘出打开局面的路径，原油和汽油价格持续居高。霍尔木兹海峡是世界原油运输约五分之一通过的的重要地点，伊朗持续威胁阻碍通行，导致了国际原油价格上涨。",
                "grammar": "「〜への道筋を描けていない」— 未能描绘出通往…的路径。例：事態打開への道筋（打开局面的路径）。\n「〜が通過する」— …通过。例：原油輸送の5分の1が通過する（五分之一原油运输通过）。\n「〜を招いてきました」— 一直招致…。例：価格の上昇を招いてきました（一直导致价格上涨）。",
                "vocab": [["事態打開", "じたいだかい", "打开局面"], ["道筋", "みちすじ", "路径、方法"], ["原油", "げんゆ", "原油"], ["高止まり", "たかどまり", "居高不下"], ["通過", "つうか", "通过"], ["威嚇", "いかく", "威吓、恐吓"]]
            },
            {
                "ja": "イランは独自に海峡封鎖に踏み切る動きを抑えていますが、オマーンとの交渉は進展していません。両国の間には長年の不信感が残り、地域全体の緊張が続く中、国際社会は「戦闘でも平和でもない不安定な状態」がいつまで続くのか、注視しています。",
                "en": "Iran is holding back from unilaterally moving to block the strait, but negotiations with Oman are not progressing. Long-standing distrust remains between the two countries, and as tensions across the region continue, the international community is watching closely how long the \"unstable state that is neither war nor peace\" will last.",
                "literal": "伊朗抑制着独自封锁海峡的动向，但与阿曼的谈判没有进展。两国之间残留着多年的不信任感，在地区整体紧张持续的情况下，国际社会正密切关注“既非战争也非和平的不稳定状态”会持续到何时。",
                "grammar": "「〜に踏み切る」— 下定决心做…。例：封鎖に踏み切る動き（决心封锁的动向）。\n「〜が残り」— …残留。例：不信感が残り（不信任感残留）。\n「〜中」— 在…之中。例：緊張が続く中（在紧张持续之中）。",
                "vocab": [["封鎖", "ふうさ", "封锁"], ["進展", "しんてん", "进展"], ["不信感", "ふしんかん", "不信任感"], ["地域全体", "ちいきぜんたい", "整个地区"], ["緊張", "きんちょう", "紧张"], ["注視", "ちゅうし", "注视、密切关注"]]
            },
        ]
    },
    {
        "slug": "dorifuto-soukou-toruko-taiho",
        "title": "ドリフト走行した疑いでトルコ国籍の男を逮捕 愛知県警はアジア大会へ取り締まり強化方針",
        "subtitle": "from メ〜テレ（名古屋テレビ）",
        "paras": [
            {
                "ja": "愛知県弥富市の路上で、禁止されているドリフト走行をしたなどとして、トルコ国籍の男が逮捕されました。道路交通法違反などの疑いで逮捕されたのは、トルコ国籍の会社員の男（29）です。",
                "en": "A Turkish national was arrested for allegedly performing prohibited drifting on a road in Yatomi City, Aichi Prefecture. The man arrested on suspicion of violating the Road Traffic Act and other laws is a Turkish company employee, 29 years old.",
                "literal": "因在爱知县弥富市的路面上进行被禁止的漂移行驶等嫌疑，一名土耳其国籍男子被捕。因违反道路交通法等的嫌疑被捕的是一名土耳其国籍的公司职员男子（29岁）。",
                "grammar": "「〜などとして」— 因…等嫌疑。例：ドリフト走行をしたなどとして（因进行了漂移行驶等）。\n「〜の疑いで逮捕された」— 因…的嫌疑被捕。例：道路交通法違反の疑いで逮捕された（因违反道路交通法嫌疑被捕）。\n「〜は、〜です」— …是…。例：会社員の男（29）です（是公司职员男子29岁）。",
                "vocab": [["ドリフト走行", "どりふとそうこう", "漂移行驶、甩尾驾驶"], ["逮捕", "たいほ", "逮捕"], ["道路交通法", "どうろこうつうほう", "道路交通法"], ["疑い", "うたがい", "嫌疑"], ["会社員", "かいしゃいん", "公司职员"], ["国籍", "こくせき", "国籍"]]
            },
            {
                "ja": "男は今年7月、弥富市の路上で乗用車を運転し、タイヤを横滑りさせて急回転するいわゆる「ドリフト走行」を、他の人物が運転する車とともにしたなどの疑いが持たれています。警察は男の認否を明らかにしていません。男はこれまでも周辺で仲間とともにドリフト走行を繰り返していたとみられ、警察は詳しく調べています。",
                "en": "The man is suspected of driving a passenger car on a road in Yatomi City in July this year and performing so-called \"drifting\" — sliding the tires sideways and spinning sharply — together with a car driven by another person. Police have not disclosed whether the man admits or denies the allegations. The man is believed to have repeatedly drifted with companions in the area, and police are investigating in detail.",
                "literal": "男子今年7月在弥富市的路面上驾驶乘用车，疑与另一人物驾驶的车辆一起进行了让轮胎侧滑并急转的所谓“漂移行驶”。警方未公布男子的认罪态度。男子此前也被认为一直在周边与同伴反复进行漂移行驶，警方正在详细调查。",
                "grammar": "「〜とともに」— 与…一起。例：他の人物が運転する車とともに（与另一人驾驶的车一起）。\n「〜とみられ」— 被认为…。例：繰り返していたとみられ（被认为一直在重复）。\n「〜を明らかにしていません」— 未公布…。例：認否を明らかにしていません（未公布认罪态度）。",
                "vocab": [["乗用車", "じょうようしゃ", "乘用车、轿车"], ["横滑り", "よこすべり", "侧滑"], ["急回転", "きゅうかいてん", "急转"], ["繰り返す", "くりかえす", "反复、重复"], ["認否", "にんぴ", "认罪与否、承认与否"], ["仲間", "なかま", "同伴、同伙"]]
            },
            {
                "ja": "現場を含む名古屋港エリアには、来月以降に開催されるアジア・アジアパラ競技大会で選手が泊まる施設が設営されています。警察は周辺でのドリフト走行など、違法行為の取り締まりを強化する方針です。",
                "en": "In the Nagoya Port area, including the scene, facilities where athletes will stay during the Asia and Asian Para Games, to be held from next month onward, are being set up. Police plan to strengthen crackdowns on illegal acts such as drifting in the surrounding area.",
                "literal": "在包括现场在内的名古屋港地区，将于下月以后举办的亚洲·亚洲残运会上选手们住宿的设施正在搭建。警方计划强化对周边漂移行驶等违法行为的取缔。",
                "grammar": "「〜を含む」— 包括…。例：現場を含むエリア（包括现场在内的地区）。\n「〜に設営されています」— …正在搭建。例：施設が設営されています（设施正在搭建）。\n「〜方針です」— 计划…。例：取り締まりを強化する方針です（计划强化取缔）。",
                "vocab": [["エリア", "えりあ", "地区、区域"], ["アジアパラ競技大会", "あじあぱらきょうぎたいかい", "亚洲残运会"], ["選手", "せんしゅ", "选手"], ["施設", "しせつ", "设施"], ["設営", "せつえい", "搭建、设置"], ["取り締まり", "とりしまり", "取缔、管制"]]
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
        if audio_ok:
            ok += 1
            print(f"   ✅ {slug}: {pc} paragraphs, audio OK")
        else:
            print(f"   ⚠️ {slug}: audio missing")
print(f"\n{ok}/{len(processed)} articles verified")
