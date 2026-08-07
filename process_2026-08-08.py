#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-08 (Sat) Edition"""
import json, os, subprocess, re, time
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-08'
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
# TODAY'S ARTICLES — 2026-08-08
# ==================================================================
articles = []
articles += [
    {
        "slug": "taifuu15-obon-koutsuu",
        "title": "来週は台風15号が東日本・北日本を直撃か お盆期間中の交通に影響のおそれ",
        "subtitle": "from tenki.jp",
        "paras": [
            {
                "ja": "来週は台風15号が東日本や北日本に接近し、お盆期間中の帰省や旅行の交通に影響がでるおそれがあります。進路予想にはまだ幅がありますが、動向に注意し、最新の気象情報を確認するようにしてください。",
                "en": "Next week, Typhoon No. 15 is expected to approach eastern and northern Japan, and there is a risk that it will affect transportation for people returning home or traveling during the Obon holiday period. There is still uncertainty in the forecast track, but please pay attention to the typhoon's movement and check the latest weather information.",
                "literal": "下周，台风15号将接近东日本和北日本，有可能会对盂兰盆节期间的返乡和旅行交通产生影响。路径预测还有不确定性，但请注意动向，并确认最新的气象信息吧。",
                "grammar": "「〜おそれがあります」— 有…的危险/可能性。例：交通に影響がでるおそれがあります（有可能对交通产生影响）。\n「〜ようにしてください」— 请务必…（请求）。例：最新の気象情報を確認するようにしてください（请务必确认最新的气象信息）。\n「〜に注意し、〜」— 注意…，然后…（连用形并列）。例：動向に注意し、最新の気象情報を確認する（注意动向，确认最新气象信息）。",
                "vocab": [["接近", "せっきん", "接近、靠近"], ["お盆", "おぼん", "盂兰盆节"], ["帰省", "きせい", "回乡探亲"], ["進路", "しんろ", "路线、路径（台风路径）"], ["動向", "どうこう", "动向"], ["気象情報", "きしょうじょうほう", "气象信息"]]
            },
            {
                "ja": "大型で強い台風13号は、今日7日午後1時現在、沖縄・奄美に最も接近していて、雨や風が強まっています。台風13号は、明後日9日(日)にかけて東シナ海を西よりに進む見通しです。この先、台風の移動速度が遅くなるため、影響が長引き、降水量が多くなるでしょう。また、沖縄や奄美では線状降水帯が発生する可能性があり、降水量がさらに多くなるおそれがあります。土砂災害や低い土地の浸水、川の増水・氾濫、暴風やうねりを伴った高波、高潮に厳重に警戒してください。",
                "en": "As of 1:00 p.m. today, the 7th, the large and powerful Typhoon No. 13 is at its closest to Okinawa and Amami, and wind and rain are intensifying. Typhoon No. 13 is expected to move westward across the East China Sea through the day after tomorrow, the 9th (Sunday). Because the typhoon's forward speed will slow from here, the effects will last longer and rainfall will increase. In Okinawa and Amami, there is also a possibility of linear rainbands forming, and there is a risk that rainfall will increase even further. Please be on strict alert for landslides, flooding of low-lying land, rising and overflowing rivers, violent winds, high waves with swell, and storm surges.",
                "literal": "大型且强劲的台风13号，截至今天7日下午1点，正最接近冲绳和奄美，雨和风正在增强。台风13号预计到后天9日（周日）为止将向偏西方向穿过东海。今后，由于台风的移动速度会变慢，影响将持续，降水量将增多吧。另外，冲绳和奄美有可能发生线状降水带，降水量有可能会进一步增多。请严加警戒泥石流灾害、低洼地区浸水、河水上涨泛滥、伴随涌浪的暴风大浪以及风暴潮。",
                "grammar": "「〜現在」— 截至…（时间点）。例：今日7日午後1時現在（截至今天7日下午1点）。\n「〜にかけて」— 直到…为止（时间/空间范围）。例：明後日9日にかけて進む見通しです（预计将行进至后天9日）。\n「〜ため、〜でしょう」— 因为…，将…吧。例：移動速度が遅くなるため、影響が長引くでしょう（因为移动速度变慢，影响将持续吧）。",
                "vocab": [["見通し", "みとおし", "预计、展望"], ["線状降水帯", "せんじょうこうすいたい", "线状降水带"], ["土砂災害", "どしゃさいがい", "泥石流灾害"], ["浸水", "しんすい", "浸水、内涝"], ["氾濫", "はんらん", "泛滥"], ["高潮", "たかしお", "风暴潮"]]
            },
            {
                "ja": "最新の進路予想によると、大型の台風15号は日本のはるか東から関東や東北の太平洋側に近づく予想になっています。関東や東北、北海道の太平洋側を中心に、雨の量が多くなり、風が強まって荒れた天気となる可能性があります。お盆期間中の帰省や旅行の交通に影響がでるおそれがあります。進路予想にはまだ幅があり、進路次第では雨や風の強まる地域が大きく変わることがあります。今後の台風の動向に注意が必要です。",
                "en": "According to the latest forecast track, the large Typhoon No. 15 is expected to approach the Pacific side of the Kanto and Tohoku regions from far east of Japan. Centering on the Pacific side of Kanto, Tohoku, and Hokkaido, rainfall amounts are likely to increase, and winds will strengthen, possibly bringing stormy weather. There is a risk of impact on transportation during the Obon holiday period. The forecast track still has uncertainty, and depending on the track, the areas with strong wind and rain may change significantly. It is necessary to keep an eye on the typhoon's future movement.",
                "literal": "根据最新的路径预测，大型台风15号预计将从日本以东的远处接近关东和东北的太平洋沿岸。以关东、东北、北海道的太平洋沿岸为中心，雨量将增多，风力增强，有可能出现恶劣天气。有可能对盂兰盆节期间的返乡和旅行交通产生影响。路径预测仍有不确定性，根据路径的不同，风雨增强的地区有时会发生很大变化。今后需要留意台风的动向。",
                "grammar": "「〜によると」— 根据…。例：最新の進路予想によると（根据最新的路径预测）。\n「〜を中心に」— 以…为中心。例：関東や東北の太平洋側を中心に（以关东、东北太平洋沿岸为中心）。\n「〜次第では」— 根据…情况。例：進路次第では雨や風の強まる地域が大きく変わることがあります（根据路径不同，风雨增强的地区有时会大幅变化）。",
                "vocab": [["太平洋側", "たいへいようがわ", "太平洋一侧"], ["荒れる", "あれる", "（天气）恶劣"], ["可能性", "かのうせい", "可能性"], ["今後の", "こんごの", "今后的"], ["注意", "ちゅうい", "注意"], ["地域", "ちいき", "地区"]]
            },
            {
                "ja": "東日本や北日本の太平洋側の地域では、台風15号が接近する前から、高波に注意が必要です。波浪注意報や波浪警報が発表されたら、海には入らないようにしてください。海水浴場では指示に従ってください。また、サーフィンや釣りも、波が高いときは危険ですので控えるようにしてください。",
                "en": "In the Pacific-side regions of eastern and northern Japan, caution is needed for high waves even before Typhoon No. 15 approaches. If a high-wave advisory or warning is issued, please do not go into the sea. At beach resorts, follow the instructions. Also, surfing and fishing are dangerous when waves are high, so please refrain from them.",
                "literal": "在东日本和北日本的太平洋一侧地区，在台风15号接近之前就需要警惕大浪。如果发布了海浪注意报或海浪警报，请不要下海。在海水浴场请听从指示。另外，冲浪和钓鱼在浪高的时候很危险，请克制一下。",
                "grammar": "「〜前から」— 从…之前起。例：接近する前から、高波に注意が必要です（在接近之前就需要警惕大浪）。\n「〜たら」— 如果…的话。例：波浪警報が発表されたら（如果发布了海浪警报）。\n「〜ないようにしてください」— 请不要…。例：海には入らないようにしてください（请不要下海）。",
                "vocab": [["高波", "たかなみ", "大浪、巨浪"], ["波浪注意報", "はろうちゅういほう", "海浪注意报"], ["指示", "しじ", "指示"], ["危険", "きけん", "危险"], ["控える", "ひかえる", "克制、避免"], ["海水浴場", "かいすいよくじょう", "海水浴场"]]
            },
        ]
    },
    {
        "slug": "kokuzai-hisyouji",
        "title": "国税不祥事、「前例ない事態次々」に危機感 「パパ活」、情報漏えいも",
        "subtitle": "from 時事通信",
        "paras": [
            {
                "ja": "龍ケ崎税務署の男性事務官（25）が調査対象の資産家から受領した多額の現金を元手にギャンブルに興じ、脱税までしていた疑いが明るみに出た。今年に入り、デートなどの見返りに金品を受け取る「パパ活」や納税者情報の漏えいなど不祥事続きの国税当局。ある幹部は「前例のない悪質な不祥事が次々と起きている。税務行政への信頼を揺るがす事態だ」と危機感をあらわにした。",
                "en": "It has come to light that a male clerk (25) at the Ryugasaki Tax Office used a large amount of cash received from a wealthy person under investigation as capital to gamble and even evade taxes. The National Tax Agency has been hit by a string of scandals this year, including \"papa-katsu\" (receiving money in return for dates) and leaks of taxpayer information. One executive voiced a sense of crisis, saying, \"Unprecedented malicious scandals are occurring one after another. This is a situation that shakes trust in tax administration.\"",
                "literal": "龙崎税务署的男性事务官（25岁）以从调查对象富豪处收取的大额现金为本钱沉迷赌博，甚至涉嫌逃税一事被曝光。进入今年以来，收取约会等回报的金钱的\"爸爸活\"、纳税人信息泄露等丑闻不断的国税当局。某干部坦言危机感：\"史无前例的恶性丑闻接连发生。这是动摇税务行政信任的事态。\"",
                "grammar": "「〜を元手に」— 以…为本钱/资本。例：多額の現金を元手にギャンブルに興じた（以巨额现金为本钱沉迷赌博）。\n「〜までしていた」— 甚至做到了…。例：脱税までしていた疑い（甚至涉嫌逃税）。\n「〜続きの」— 连续…的。例：不祥事続きの国税当局（丑闻不断的国税当局）。",
                "vocab": [["事務官", "じむかん", "事务官（公务员职位）"], ["資産家", "しさんか", "富豪、资产家"], ["元手", "もとで", "本金、本钱"], ["脱税", "だつぜい", "逃税"], ["漏えい", "ろうえい", "泄露"], ["危機感", "ききかん", "危机感"]]
            },
            {
                "ja": "人事院の資料によると、昨年1年間で懲戒処分を受けた国税職員は37人。今年は3月時点で20人に上る異常事態だが、以降も不祥事はやまない。5月には、埼玉県内の税務署に勤務していた20代女性がデリバリーヘルスで働き、SNSで知り合った約30人にパパ活をして計約230万円の報酬を得たとして減給処分を受けた。「地下アイドルの推し活資金を捻出したかった」と話し、職を辞した。",
                "en": "According to materials from the National Personnel Authority, 37 tax agency employees received disciplinary punishment last year. This year, the number had already reached 20 as of March — an abnormal situation — and the scandals have not stopped since. In May, a woman in her 20s who worked at a tax office in Saitama Prefecture received a pay-cut punishment for working in delivery health services and doing \"papa-katsu\" with about 30 people she met on social media, earning about 2.3 million yen in total. She said she \"wanted to raise funds for her favorite underground idol,\" and resigned from her job.",
                "literal": "根据人事院的资料，去年一年受到惩戒处分的国税职员有37人。今年截至3月已达到20人的异常事态，但此后丑闻也未停止。5月，在埼玉县内税务署工作的20多岁女性因在派遣型色情服务工作、向在社交网络上认识的约30人提供\"爸爸活\"获得共计约230万日元报酬而受到减薪处分。她说\"想筹措地下偶像的应援资金\"，并辞去了职务。",
                "grammar": "「〜によると」— 根据…。例：人事院の資料によると（根据人事院的资料）。\n「〜に上る」— 达到…（数量）。例：20人に上る異常事態（达到20人的异常事态）。\n「〜たとして」— 因…而（受到处分）。例：報酬を得たとして減給処分を受けた（因获得报酬而受到减薪处分）。",
                "vocab": [["懲戒処分", "ちょうかいしょぶん", "惩戒处分"], ["勤務", "きんむ", "工作、任职"], ["報酬", "ほうしゅう", "报酬"], ["減給", "げんきゅう", "减薪"], ["捻出", "ねんしゅつ", "筹措、挤出（资金）"], ["職を辞する", "しょくをじする", "辞职"]]
            },
            {
                "ja": "大阪国税局でも4月、課税1部の実査官だった30代男性が千葉県警をかたる男から「捜査で嫌疑がかかっている」と電話で告げられ、言われるがまま法人・個人の名前や申告額など259件をLINEで送っていたことが発覚。情報を漏えいされた納税者にはその後、詐欺とみられる電話がかかってきたという。男性は停職処分を受け辞職した。",
                "en": "In April, at the Osaka Regional Taxation Bureau, it was revealed that a man in his 30s who had been an audit officer in the First Tax Division was told by phone by a man impersonating the Chiba Prefectural Police that \"you are under suspicion in an investigation,\" and sent 259 items of information — names of corporations and individuals and declared amounts — via LINE as he was told. Taxpayers whose information was leaked reportedly later received phone calls believed to be fraud. The man received a suspension punishment and resigned.",
                "literal": "大阪国税局也在4月，曾任课税第一部实查官的30多岁男性被冒充千叶县警的男子电话告知\"调查中你受到怀疑\"，他按照对方所说通过LINE发送了法人、个人的姓名和申报金额等259件信息一事被曝光。信息被泄露的纳税人之后接到了疑似诈骗的电话。该男性受到停职处分后辞职。",
                "grammar": "「〜をかたる」— 冒充…。例：千葉県警をかたる男（冒充千叶县警的男子）。\n「〜がまま」— 任凭…、按照…。例：言われるがまま送っていた（任凭对方吩咐发送）。\n「〜とみられる」— 被认为是…。例：詐欺とみられる電話（被认为是诈骗的电话）。",
                "vocab": [["発覚", "はっかく", "败露、暴露"], ["かたる", "かたる（騙る）", "冒充、假冒"], ["嫌疑", "けんぎ", "嫌疑"], ["申告", "しんこく", "申报"], ["詐欺", "さぎ", "诈骗"], ["停職", "ていしょく", "停职"]]
            },
        ]
    },
    {
        "slug": "kioxia-toshiba-junrieki",
        "title": "キオクシアHD株、前身の東芝にも巨額の恩恵 1Q純利益30倍の約4.5兆円",
        "subtitle": "from Bloomberg",
        "paras": [
            {
                "ja": "東芝が7日に発表した4－6月期（第1四半期）の純利益は、前年同期比約30倍の4兆4673億円だった。第1四半期としては過去最高だった。保有するキオクシアホールディングス株の評価益などの計上が寄与した。キオクシアHD関連益は6兆3294億円と、同1000倍超になった。",
                "en": "Toshiba announced on the 7th that its net profit for the April–June quarter (first quarter) was 4.4673 trillion yen, about 30 times higher than the same period last year. It was the highest ever for a first quarter. The booking of valuation gains on its holdings of Kioxia Holdings shares contributed to the result. Profits related to Kioxia HD amounted to 6.3294 trillion yen, more than 1,000 times the previous level.",
                "literal": "东芝于7日公布的4-6月期（第一季度）净利润为4兆4673亿日元，约为去年同期的30倍。作为第一季度为历史最高。所持有的铠侠控股股票的估值收益等计入作出了贡献。铠侠HD相关收益达到6兆3294亿日元，同比超过1000倍。",
                "grammar": "「〜倍だった」— 是…倍。例：前年同期比約30倍（约为上年同期的30倍）。\n「〜としては」— 作为…。例：第1四半期としては過去最高（作为第一季度是历史最高）。\n「〜に寄与した」— 对…作出了贡献。例：評価益などの計上が寄与した（估值收益等的计入作出了贡献）。",
                "vocab": [["純利益", "じゅんりえき", "净利润"], ["前年同期", "ぜねんどうき", "上年同期"], ["評価益", "ひょうかえき", "估值收益"], ["計上", "けいじょう", "计入（账目）"], ["寄与", "きよ", "贡献"], ["保有", "ほゆう", "持有"]]
            },
            {
                "ja": "東芝は5月11日時点でキオクシアHD株の16.1%を保有していたが、6月から7月にかけて市場内で344万7200株（約2616億円に相当）の売却を進め、7月15日時点では15.5％まで低下していた。AIデータセンター投資拡大を背景に4－6月にかけてキオクシア株は急騰。6月下旬には上場来高値を付けていた。",
                "en": "As of May 11, Toshiba held 16.1% of Kioxia HD shares, but it proceeded to sell 3,447,200 shares (equivalent to about 261.6 billion yen) on the market from June through July, reducing its stake to 15.5% as of July 15. Against the backdrop of expanding AI data center investment, Kioxia shares surged from April through June, hitting an all-time high in late June.",
                "literal": "东芝截至5月11日持有铠侠HD股票的16.1%，但从6月到7月在市场上推进出售344万7200股（相当于约2616亿日元），截至7月15日已降至15.5%。以AI数据中心投资扩大为背景，4月至6月铠侠股票暴涨。6月下旬创下上市以来最高价。",
                "grammar": "「〜時点で」— 截至…时点。例：5月11日時点で保有していた（截至5月11日持有）。\n「〜から〜にかけて」— 从…到…（期间）。例：6月から7月にかけて売却を進め（从6月到7月推进出售）。\n「〜を背景に」— 以…为背景。例：投資拡大を背景に急騰（以投资扩大为背景暴涨）。",
                "vocab": [["売却", "ばいきゃく", "出售"], ["相当", "そうとう", "相当于"], ["急騰", "きゅうとう", "暴涨"], ["上場来高値", "じょうじょうらいたかね", "上市以来最高价"], ["拡大", "かくだい", "扩大"], ["低下", "ていか", "下降"]]
            },
            {
                "ja": "第1四半期の営業利益は、約2.8倍の1119億円だった。生成AIの普及に伴う旺盛なデータセンター需要を背景に、ハードディスクドライブ（HDD）や、送変電配電・サーマル関連事業が堅調に推移した。固定費の削減なども進めた。東芝は2023年12月に上場廃止となり、日本産業パートナーズ（JIP）傘下で業績の立て直しや再上場に向けた体制作りを進めている。",
                "en": "Operating profit for the first quarter was 111.9 billion yen, about 2.8 times higher. Against the backdrop of strong data center demand accompanying the spread of generative AI, hard disk drive (HDD) and power transmission/distribution and thermal-related businesses performed solidly. The company also advanced fixed-cost reductions. Toshiba was delisted in December 2023 and is working under Japan Industrial Partners (JIP) to rebuild performance and build a framework toward relisting.",
                "literal": "第一季度的营业利润约为2.8倍，达1119亿日元。以伴随生成式AI普及而旺盛的数据中心需求为背景，硬盘驱动器（HDD）以及输变电配电、热相关业务稳步发展。还推进了固定费用的削减。东芝于2023年12月退市，在日本产业合作伙伴（JIP）旗下推进业绩重建和面向重新上市的制度建设。",
                "grammar": "「〜に伴う」— 伴随…的。例：生成AIの普及に伴う旺盛な需要（伴随生成式AI普及的旺盛需求）。\n「〜を背景に」— 以…为背景。例：旺盛な需要を背景に堅調に推移（以旺盛需求为背景稳步发展）。\n「〜に向けた」— 面向…的。例：再上場に向けた体制作り（面向重新上市的体制建设）。",
                "vocab": [["営業利益", "えいぎょうりえき", "营业利润"], ["普及", "ふきゅう", "普及"], ["旺盛", "おうせい", "旺盛"], ["堅調", "けんちょう", "坚挺、稳健"], ["固定費", "こていひ", "固定费用"], ["上場廃止", "じょうじょうはいし", "退市、摘牌"]]
            },
        ]
    },
    {
        "slug": "usagi-shima-isei",
        "title": "「ウサギの島」生態系に異変、観光客の過剰な餌やりで増えたイノシシがウサギを襲う",
        "subtitle": "from 読売新聞オンライン",
        "paras": [
            {
                "ja": "「ウサギの島」として知られる広島県竹原市の大久野島で、観光客によるウサギへの過剰な餌やりが島の生態系に異変をもたらしている。ウサギが残した餌を島内の野生イノシシが食べて数を増やしているとみられ、ウサギを襲っているケースを福島大などのチームが確認した。国などは、適切な餌やりルールの徹底を呼びかけている。",
                "en": "On Okunoshima in Takehara City, Hiroshima Prefecture, known as \"Rabbit Island,\" excessive feeding of rabbits by tourists is causing changes to the island's ecosystem. Wild boars on the island are believed to be eating leftover rabbit food and increasing in number, and a team including Fukushima University has confirmed cases of them attacking rabbits. National authorities are calling for thorough enforcement of appropriate feeding rules.",
                "literal": "在被称作\"兔子岛\"的广岛县竹原市大久野岛，游客给兔子过度喂食正在给岛的生态系统带来异变。岛内的野生野猪被认为吃掉兔子留下的食物而数量增加，福岛大学等团队确认了野猪袭击兔子的案例。国家等呼吁彻底贯彻适当的喂食规则。",
                "grammar": "「〜として知られる」— 作为…而闻名。例：「ウサギの島」として知られる（作为\"兔子岛\"而闻名）。\n「〜による」— 由…造成的。例：観光客による過剰な餌やり（游客造成的过度喂食）。\n「〜とみられ」— 被认为…。例：数を増やしているとみられ（被认为数量在增加）。",
                "vocab": [["過剰", "かじょう", "过剩、过度"], ["餌やり", "えやり", "喂食"], ["生態系", "せいたいけい", "生态系统"], ["異変", "いへん", "异变、异常变化"], ["野生", "やせい", "野生"], ["徹底", "てってい", "彻底"]]
            },
            {
                "ja": "大久野島は、瀬戸内海国立公園内にある周囲約4キロの無人島。1970年代に島外から持ち込まれた外来種のアナウサギが野生化したとされ、500匹以上が生息する。人気観光スポットとして、国内外から年間約20万人が訪れている。環境省によると、島内にイノシシは元々いなかったが、約15年前に姿を現し、島での繁殖も確認。海を泳いで島に渡り、観光客がウサギの餌用に持ち込んだ野菜などの食べ残しを得て増加したとみられる。",
                "en": "Okunoshima is an uninhabited island with a circumference of about 4 kilometers inside the Seto Inland Sea National Park. European rabbits, an invasive species brought from outside the island in the 1970s, are said to have gone wild, and more than 500 now live there. As a popular tourist spot, about 200,000 people visit from Japan and abroad each year. According to the Ministry of the Environment, there were originally no boars on the island, but they appeared about 15 years ago, and breeding has been confirmed. They are believed to have swum across the sea to the island and increased by eating leftovers of vegetables tourists brought for feeding rabbits.",
                "literal": "大久野岛是濑户内海国立公园内周长约4公里的无人岛。据称1970年代从岛外带来的外来物种穴兔已野生化，栖息着500只以上。作为热门观光景点，国内外每年约有20万人到访。据环境省称，岛内原本没有野猪，但约15年前出现，也确认了在岛上繁殖。被认为游过海来到岛上，获得游客为喂兔子带来的蔬菜等剩食而增加。",
                "grammar": "「〜とされ」— 据称…、被认为…。例：野生化したとされ（被认为已野生化）。\n「〜によると」— 根据…。例：環境省によると（根据环境省）。\n「〜とみられる」— 被认为…。例：食べ残しを得て増加したとみられる（被认为因获得剩食而增加）。",
                "vocab": [["国立公園", "こくりつこうえん", "国立公园"], ["無人島", "むじんとう", "无人岛"], ["外来種", "がいらいしゅ", "外来物种"], ["生息", "せいそく", "栖息"], ["繁殖", "はんしょく", "繁殖"], ["食べ残し", "たべのこし", "剩饭、吃剩的食物"]]
            },
            {
                "ja": "そんな中、イノシシがウサギを襲う様子を福島大や呉高専などの調査チームが確認した。調査の結果、イノシシに捕食されたとみられるウサギの死体も見つかった。自然死したウサギの死体をイノシシが食べることは知られているが、海外での事例も含め、生きたウサギを襲って捕食するケースはこれまで報告がないという。",
                "en": "Amid this situation, a research team including Fukushima University and the National Institute of Technology, Kure College confirmed scenes of boars attacking rabbits. As a result of the investigation, rabbit carcasses believed to have been preyed upon by boars were also found. It has been known that boars eat rabbits that died naturally, but there have been no previous reports — including overseas cases — of boars attacking and preying on live rabbits.",
                "literal": "在这样的情况下，福岛大学和吴工业高等专门学校等调查团队确认了野猪袭击兔子的情形。调查结果还发现了被认为被野猪捕食的兔子尸体。野猪吃自然死亡的兔子尸体是已知的，但包括海外事例在内，袭击并捕食活兔子的案例至今没有报告。",
                "grammar": "「〜を襲う」— 袭击…。例：イノシシがウサギを襲う様子（野猪袭击兔子的情形）。\n「〜とみられる」— 被认为…。例：捕食されたとみられるウサギの死体（被认为被捕食的兔子尸体）。\n「〜という」— 据说…（传闻）。例：報告がないという（据说没有报告）。",
                "vocab": [["捕食", "ほしょく", "捕食"], ["死体", "したい", "尸体"], ["自然死", "しぜんし", "自然死亡"], ["事例", "じれい", "事例"], ["生きた", "いきた", "活着的"], ["報告", "ほうこく", "报告"]]
            },
            {
                "ja": "兼子教授は「餌やりが結果的にイノシシの定着を促し、今まで観察されていない行動につながったのだろう。生態系に思わぬ影響を与えている可能性を考慮すべきだ」と指摘する。環境省や観光協会などでつくる「大久野島未来づくり実行委員会」はすでに、観光客向けの餌やりルールを作成。ウサギが餌を食べ終わるまで見守り、残った餌は持ち帰るよう求めている。",
                "en": "Professor Kaneko points out, \"The feeding has, as a result, encouraged the establishment of boars and likely led to behavior never observed before. We should consider the possibility that it is having unexpected effects on the ecosystem.\" The \"Okunoshima Future Creation Executive Committee,\" made up of the Ministry of the Environment, the tourism association, and others, has already created feeding rules for tourists. They ask visitors to watch over the rabbits until they finish eating and take leftover food home.",
                "literal": "兼子教授指出：\"喂食结果上促进了野猪的定居，大概导致了至今未被观察到的行为吧。应该考虑可能正在对生态系统产生意想不到的影响。\"由环境省和观光协会等组成的\"大久野岛未来创建执行委员会\"已经制定了面向游客的喂食规则。要求守着兔子吃完食物，把剩下的食物带回去。",
                "grammar": "「〜のだろう」— 大概…吧（推测）。例：つながったのだろう（大概导致了…吧）。\n「〜可能性を考慮すべきだ」— 应该考虑…的可能性。例：影響を与えている可能性を考慮すべきだ（应该考虑正在产生影响的可能性）。\n「〜よう求めている」— 要求…。例：持ち帰るよう求めている（要求带回去）。",
                "vocab": [["定着", "ていちゃく", "定居、扎根"], ["促す", "うながす", "促进、促使"], ["観察", "かんさつ", "观察"], ["指摘", "してき", "指出"], ["実行委員会", "じっこういいんかい", "执行委员会"], ["見守る", "みまもる", "守护、照看"]]
            },
        ]
    },
    {
        "slug": "penguin-torimaria",
        "title": "八木山動物公園のフンボルトペンギン4羽、死因は「鳥マラリア」",
        "subtitle": "from ORICON NEWS",
        "paras": [
            {
                "ja": "仙台市の八木山動物公園は7日、公式サイトを更新。7月に相次いで4羽が死亡したフンボルトペンギンの死因について「『鳥マラリア』によるものと考えられます」と発表した。同園では、7月9日に「あらまさ（オス）」、10日に「ひめ（メス）」、18日に「いずみ（オス）」、19日に「かすみ（メス）」が死亡した。同園は「あらまさ」が死んだ段階で展示を休止し、バックヤードでの飼育に切り替え、原因を調べていた。",
                "en": "Sendai City's Yagiyama Zoological Park updated its official website on the 7th, announcing that the cause of death of four Humboldt penguins that died one after another in July \"is considered to be avian malaria.\" At the park, \"Aramasa\" (male) died on July 9, \"Hime\" (female) on the 10th, \"Izumi\" (male) on the 18th, and \"Kasumi\" (female) on the 19th. The park suspended the exhibit when Aramasa died, switched to keeping them in the back area, and investigated the cause.",
                "literal": "仙台市的八木山动物园于7日更新了官网。关于7月接连死亡的4只洪堡企鹅的死因，公布\"被认为是由'禽疟疾'造成的\"。该园于7月9日\"阿正（雄性）\"、10日\"姬（雌性）\"、18日\"泉（雄性）\"、19日\"霞（雌性）\"死亡。该园在\"阿正\"死亡的阶段停止了展示，转为在后台饲养，并调查原因。",
                "grammar": "「〜について」— 关于…。例：死因について発表した（就死因进行了公布）。\n「〜によるものと考えられます」— 被认为是由…造成的。例：鳥マラリアによるものと考えられます（被认为是由禽疟疾造成的）。\n「〜段階で」— 在…的阶段。例：死んだ段階で展示を休止した（在死亡的阶段停止了展示）。",
                "vocab": [["死因", "しいん", "死因"], ["相次いで", "あいついで", "接连不断"], ["発表", "はっぴょう", "公布、发表"], ["展示", "てんじ", "展示"], ["飼育", "しいく", "饲养"], ["休止", "きゅうし", "暂停"]]
            },
            {
                "ja": "同園によると、4羽とも死亡前日まで体調不良や食欲低下などの異常は認められず、通常どおりの様子で過ごしていたという。「あらまさ」と「ひめ」は短期間に連続して急死。他園での類似例より「鳥マラリア」が疑われたため、「いずみ」と「かすみ」には抗マラリア薬を投与したが、死亡した。同園は研究機関で血液および臓器の検査を実施。複数羽から鳥マラリア原虫の遺伝子が確認された。",
                "en": "According to the park, none of the four showed abnormalities such as poor health or loss of appetite until the day before death, and they spent their time as usual. Aramasa and Hime died suddenly in quick succession within a short period. Because avian malaria was suspected based on similar cases at other zoos, anti-malarial drugs were administered to Izumi and Kasumi, but they died. The park conducted blood and organ tests at research institutions, and the genes of the avian malaria parasite were confirmed in multiple birds.",
                "literal": "据该园称，4只企鹅在死亡前一天之前都没有出现身体不适、食欲下降等异常，像平常一样度过。\"阿正\"和\"姬\"在短期内连续急死。由于根据其他园的类似案例怀疑是\"禽疟疾\"，对\"泉\"和\"霞\"投用了抗疟疾药，但还是死亡了。该园在研究机构实施了血液及脏器检查。从多只企鹅身上确认了禽疟疾原虫的基因。",
                "grammar": "「〜によると」— 根据…。例：同園によると（据该园称）。\n「〜ため」— 因为…。例：疑われたため、投与した（因为被怀疑，所以投药）。\n「〜たが、〜」— 虽然…但是…。例：投与したが、死亡した（虽然投药了，但还是死亡了）。",
                "vocab": [["体調不良", "たいちょうふよう", "身体不适"], ["食欲低下", "しょくよくていか", "食欲下降"], ["急死", "きゅうし", "猝死"], ["投与", "とうよ", "投药、给药"], ["臓器", "ぞうき", "脏器"], ["遺伝子", "いでんし", "基因"]]
            },
            {
                "ja": "鳥マラリアとは、鳥類に広く見られるマラリア原虫の感染によって起こる病気であり、蚊が媒介する。人に感染することはない。同園は、展示場内に水たまりができないように地面の凹凸を改善するとともに、除草によって風通しを良くし、蚊が発生しにくい環境を整え、定期的に抗マラリア薬を投与し、鳥マラリアの発症リスクを低減させる。このほか、暑熱による体力低下を防ぐため、既設の日よけやミスト設備に加え、新たに送風機を設置する再発防止策を講じて、展示再開を目指すとしている。",
                "en": "Avian malaria is a disease caused by infection with malaria parasites widely found in birds, transmitted by mosquitoes. It does not infect humans. The park will improve uneven ground so that puddles do not form in the exhibit area, improve airflow through weeding, create an environment where mosquitoes are less likely to breed, and regularly administer anti-malarial drugs to reduce the risk of avian malaria. In addition, to prevent physical decline due to heat, the park will install new fans in addition to existing shade and mist equipment as part of measures to prevent recurrence, aiming to resume the exhibit.",
                "literal": "禽疟疾是由广泛见于鸟类的疟疾原虫感染引起的疾病，由蚊子传播。不会感染人类。该园将改善展示场内地面凹凸以防止积水，同时通过除草改善通风，营造蚊子不易滋生的环境，定期投用抗疟疾药，降低禽疟疾的发病风险。此外，为防止暑热导致的体力下降，在既有遮阳棚和喷雾设备的基础上，新安装送风机，采取防止再发的措施，力争重新开放展示。",
                "grammar": "「〜とは」— 所谓…是（定义）。例：鳥マラリアとは…病気であり（禽疟疾是…的疾病）。\n「〜とともに」— 同时、随着。例：改善するとともに、風通しを良くし（在改善的同时，改善通风）。\n「〜にくい」— 难以…。例：蚊が発生しにくい環境（蚊子难以滋生的环境）。",
                "vocab": [["媒介", "ばいかい", "传播媒介"], ["感染", "かんせん", "感染"], ["水たまり", "みずたまり", "水洼"], ["除草", "じょそう", "除草"], ["再発防止", "さいはつぼうし", "防止复发"], ["送風機", "そうふうき", "送风机"]]
            },
        ]
    },
    {
        "slug": "spacex-tsuki-shoutotsu",
        "title": "スペースXのロケット残骸が月面に衝突 衝突地点の画像を公開",
        "subtitle": "from 共同通信",
        "paras": [
            {
                "ja": "韓国航空宇宙庁は6日、米宇宙企業スペースXが1年半前に打ち上げたロケットの残骸が月面に衝突した地点の画像を公開した。月周回探査機で撮影した。意図しない形でロケット残骸が月面に衝突するのは、中国のロケットが衝突した2022年以来2回目。衝突後に撮影された複数の画像からは、衝突前にはなかった放射状の形状や黒い影が確認できた。",
                "en": "On the 6th, the Korea AeroSpace Administration released images of the site where debris from a rocket launched by U.S. space company SpaceX a year and a half ago crashed into the lunar surface. The images were taken by a lunar orbiter. This is the second time rocket debris has unintentionally crashed into the Moon, following a Chinese rocket in 2022. From multiple images taken after the impact, radial shapes and black shadows that did not exist before the impact were confirmed.",
                "literal": "韩国航空宇宙厅于6日公开了美国航天企业SpaceX一年半前发射的火箭残骸撞击月球表面的地点图像。由月球轨道探测器拍摄。火箭残骸以非预期方式撞击月面，是继中国火箭撞击的2022年以来第二次。从撞击后拍摄的多张图像中，确认了撞击前不存在的放射状形状和黑色阴影。",
                "grammar": "「〜に衝突した」— 撞击了…。例：月面に衝突した地点（撞击月面的地点）。\n「〜以来」— 自…以来。例：2022年以来2回目（自2022年以来第二次）。\n「〜からは」— 从…（能看出）。例：複数の画像からは確認できた（从多张图像中能够确认）。",
                "vocab": [["残骸", "ざんがい", "残骸"], ["打ち上げる", "うちあげる", "发射"], ["月周回探査機", "つきしゅうかいたんさき", "月球轨道探测器"], ["衝突", "しょうとつ", "撞击、碰撞"], ["放射状", "ほうしゃじょう", "放射状"], ["確認", "かくにん", "确认"]]
            },
            {
                "ja": "事前にロケットや人工衛星などの衝突を把握して追跡できた事例は珍しく、米航空宇宙局（NASA）は画像を詳細に解析するなどして今後の月面探査に生かす。衝突地点は、地球から見える側と見えない側の境界近くにあるアインシュタイン・クレーター付近。NASAは衝撃により直径約18メートル、深さ約3.7メートルのクレーターができると分析していた。",
                "en": "It is rare to be able to grasp and track a collision of a rocket or satellite in advance, and NASA will analyze the images in detail and use them for future lunar exploration. The impact site is near the Einstein crater, close to the boundary between the side visible from Earth and the far side. NASA had analyzed that the impact would create a crater about 18 meters in diameter and about 3.7 meters deep.",
                "literal": "事先掌握并追踪火箭或人造卫星撞击的事例很罕见，美国宇航局（NASA）将通过详细解析图像等方式用于今后的月面探测。撞击地点位于地球可见面与不可见面的边界附近的爱因斯坦环形山附近。NASA此前分析认为撞击将形成直径约18米、深约3.7米的环形山。",
                "grammar": "「〜は珍しく」— …很罕见。例：追跡できた事例は珍しく（能追踪的事例很罕见）。\n「〜に生かす」— 活用于…。例：今後の月面探査に生かす（用于今后的月面探测）。\n「〜により」— 由于…。例：衝撃によりクレーターができる（因撞击形成环形山）。",
                "vocab": [["把握", "はあく", "掌握"], ["追跡", "ついせき", "追踪"], ["解析", "かいせき", "解析"], ["月面探査", "げつめんたんさ", "月面探测"], ["境界", "きょうかい", "边界"], ["直径", "ちょっけい", "直径"]]
            },
            {
                "ja": "ロケットは25年1月、日本の宇宙企業ispace（アイスペース）の月着陸船などを載せ、フロリダ州のケネディ宇宙センターから打ち上げられた。ロケット上段がその後、太陽活動や重力の影響により月面に向かう軌道に入り、今月5日、月面に衝突した。",
                "en": "The rocket was launched from Kennedy Space Center in Florida in January 2025, carrying a lunar lander from Japanese space company ispace and other payloads. The rocket's upper stage subsequently entered an orbit toward the Moon due to the influence of solar activity and gravity, and crashed into the lunar surface on the 5th of this month.",
                "literal": "该火箭于25年1月搭载日本航天企业ispace的月球着陆器等，从佛罗里达州肯尼迪航天中心发射。火箭末级之后受太阳活动和重力影响进入朝向月面的轨道，于本月5日撞击月面。",
                "grammar": "「〜を載せ」— 搭载着…。例：月着陸船などを載せ、打ち上げられた（搭载着月球着陆器等被发射）。\n「〜により」— 因…。例：太陽活動や重力の影響により（受太阳活动和重力的影响）。\n「〜に入り、〜」— 进入…，然后…。例：軌道に入り、衝突した（进入轨道，然后撞击）。",
                "vocab": [["月着陸船", "つきちゃくりくせん", "月球着陆器"], ["打ち上げ", "うちあげ", "发射"], ["上段", "じょうだん", "（火箭）末级"], ["重力", "じゅうりょく", "重力"], ["軌道", "きどう", "轨道"], ["太陽活動", "たいようかつどう", "太阳活动"]]
            },
        ]
    },
    {
        "slug": "josei-kenkyuusya-sien",
        "title": "若手女性研究者を支援する新制度、大学に年間最大5000万円の補助金",
        "subtitle": "from 読売新聞オンライン",
        "paras": [
            {
                "ja": "文部科学省は来年度、若手女性研究者を支援する新制度を設ける方針を固めた。事務作業や実験など膨大な業務の一部を組織全体で支える仕組みを導入した大学に、年間最大5000万円程度の補助金を交付する。出産や子育てなどと研究を両立できる環境を整えることで、諸外国よりも少ない女性研究者を育成し、研究力の底上げにつなげる。",
                "en": "The Ministry of Education, Culture, Sports, Science and Technology has decided to establish a new system next fiscal year to support young female researchers. It will provide subsidies of up to about 50 million yen per year to universities that introduce a framework in which the entire organization supports part of the enormous workload, such as clerical work and experiments. By creating an environment where research can be balanced with childbirth and child-rearing, the ministry aims to nurture female researchers — who are fewer than in other countries — and raise overall research capacity.",
                "literal": "文部科学省确定了下年度设立支援年轻女性研究员新制度的方针。将向引进了由整个组织支撑事务工作、实验等庞大部分业务的机制的大学，每年发放最高约5000万日元的补助金。通过整备能够兼顾生育、育儿与研究的环境，培养比外国更少的女性研究员，并带动研究实力的提升。",
                "grammar": "「〜方針を固めた」— 确定了…的方针。例：新制度を設ける方針を固めた（确定了设立新制度的方针）。\n「〜を導入した大学に」— 向引进了…的大学。例：仕組みを導入した大学に交付する（向引进了机制的大学发放）。\n「〜ことで、〜」— 通过…，从而…。例：環境を整えることで、育成し（通过整备环境，培养…）。",
                "vocab": [["若手", "わかて", "年轻、晚辈"], ["膨大", "ぼうだい", "庞大"], ["補助金", "ほじょきん", "补助金"], ["交付", "こうふ", "发放、交付"], ["両立", "りょうりつ", "兼顾、两立"], ["底上げ", "そこあげ", "整体提升"]]
            },
            {
                "ja": "総務省の調査では、企業も含む研究者の女性割合は米仏が30%超（2023年時点）で、日本は19%（25年時点）だった。背景には研究者の多忙さがある。特に大学教員は、研究以外に学生指導や事務作業、実験機器の管理なども仕事に抱える。女性の場合、出産や子育て、介護などのライフイベントと両立できず、休職や離職する例も多い。",
                "en": "According to a survey by the Ministry of Internal Affairs and Communications, the proportion of female researchers including those at companies exceeds 30% in the U.S. and France (as of 2023), while Japan was at 19% (as of 2025). Behind this is the busyness of researchers. University faculty in particular also carry student guidance, clerical work, and management of experimental equipment as part of their jobs besides research. In the case of women, many cannot balance research with life events such as childbirth, child-rearing, and caregiving, and take leave or leave their jobs.",
                "literal": "据总务省调查，包括企业在内的研究员中女性占比，美法超过30%（2023年时点），日本为19%（25年时点）。背景是研究员的繁忙。尤其是大学教员，除研究外还要承担学生指导、事务工作、实验设备管理等。女性由于无法兼顾生育、育儿、护理等人生大事，休职或离职的例子很多。",
                "grammar": "「〜では」— 在…方面。例：総務省の調査では（根据总务省的调查）。\n「〜に抱える」— 承担着…。例：仕事に抱える（把…揽入工作中）。\n「〜できず、〜」— 无法…，因而…。例：両立できず、離職する（无法兼顾，因而离职）。",
                "vocab": [["割合", "わりあい", "比例"], ["多忙", "たぼう", "繁忙"], ["学生指導", "がくせいしどう", "学生指导"], ["介護", "かいご", "护理、看护"], ["休職", "きゅうしょく", "停职休假"], ["離職", "りしょく", "离职"]]
            },
            {
                "ja": "そこで新制度は、若手女性研究者への組織ぐるみの支援体制の導入を大学に促す。文科省は具体例として、実験補助員の雇用、事務作業の外部発注、研究を効率化する機器の購入などを通じた負担軽減策を想定する。業務時間が限られても、独自性の高い自身の研究に注力してもらう。",
                "en": "The new system thus encourages universities to introduce an organization-wide support framework for young female researchers. As specific examples, the ministry envisions burden-reduction measures such as hiring experiment assistants, outsourcing clerical work, and purchasing equipment that makes research more efficient. The aim is to let researchers focus on their own highly original research even if their working hours are limited.",
                "literal": "因此，新制度促使大学引进对年轻女性研究员的组织整体支援体制。文科省设想的减轻负担措施的具体例子包括：雇用实验辅助员、外包事务工作、购买使研究高效化的设备等。即使业务时间有限，也希望她们专注于独创性高的自身研究。",
                "grammar": "「〜ぐるみ」— 整个…、全员…。例：組織ぐるみの支援体制（组织整体的支援体制）。\n「〜を通じた」— 通过…的。例：負担軽減策を通じた（通过减轻负担措施）。\n「〜ても」— 即使…也。例：業務時間が限られても（即使业务时间有限）。",
                "vocab": [["促す", "うながす", "促使"], ["雇用", "こよう", "雇用"], ["外部発注", "がいぶちゅうもん", "外部委托"], ["効率化", "こうりつか", "高效化"], ["負担", "ふたん", "负担"], ["注力", "ちゅうりょく", "着力、专注"]]
            },
            {
                "ja": "文科省によると、日本の大学教員は特に理工系の女性が少なく、女性割合は22年度、理学系11%、工学系8%だった。政府はこれまで、上位職の女性登用を推進する大学を支援してきたが、そもそもキャリアを継続できない人が多く、十分な成果が出ていない。文科省幹部は「新制度で若手も実績を積める環境を整え、将来のリーダーとして活躍する人材を輩出したい」と話す。",
                "en": "According to the ministry, female university faculty are especially few in science and engineering fields, with the female ratio in FY2022 at 11% in science and 8% in engineering. The government has so far supported universities that promote women into senior positions, but many people cannot continue their careers in the first place, so sufficient results have not been achieved. A ministry executive says, \"Through the new system, we want to create an environment where young researchers can build achievements and produce people who will play active roles as future leaders.\"",
                "literal": "据文科省称，日本大学教员中尤其是理工科的女性很少，22年度女性占比理学系为11%、工学系为8%。政府至今一直在支援推进高层职位起用女性的大学，但本来就无法持续职业生涯的人很多，尚未取得充分成果。文科省干部表示：\"希望通过新制度整备年轻人也能积累实绩的环境，培养出作为未来领导者活跃的人才。\"",
                "grammar": "「〜によると」— 根据…。例：文科省によると（据文科省称）。\n「〜てきたが、」— 一直…，但是…。例：支援してきたが、成果が出ていない（一直在支援，但没有成果）。\n「〜として活躍する」— 作为…活跃。例：将来のリーダーとして活躍する（作为未来领导者活跃）。",
                "vocab": [["理工系", "りこうけい", "理工科"], ["登用", "とうよう", "起用"], ["そもそも", "そもそも", "本来、首先"], ["実績", "じっせき", "实绩"], ["人材", "じんざい", "人才"], ["輩出", "はいしゅつ", "培养出、涌现出"]]
            },
        ]
    },
    {
        "slug": "wow-shingou",
        "title": "「Wow！信号」受信から50年、正体不明の電波を世界合同観測へ",
        "subtitle": "from 読売新聞オンライン",
        "paras": [
            {
                "ja": "宇宙のどこかに「宇宙人」がいる――。それを確かめようとする研究が国内外で長く続く。謎めいた電波信号が米国で受信されてから50年となる来年8月に合わせ、日本の研究者らが世界合同観測をしようと呼びかけている。",
                "en": "Are there \"aliens\" somewhere in the universe? Research to confirm this has continued for a long time both in Japan and abroad. To coincide with next August, when 50 years will have passed since a mysterious radio signal was received in the United States, Japanese researchers are calling for a joint global observation.",
                "literal": "宇宙的某处有\"外星人\"吗——。为证实这一点的研究在国内外长期持续。配合谜一般的电波信号在美国被接收到50周年的明年8月，日本的研究者们呼吁进行世界联合观测。",
                "grammar": "「〜ようとする」— 想要…。例：確かめようとする研究（想要证实的研究）。\n「〜に合わせ」— 配合…。例：50年となる来年8月に合わせ（配合迎来50周年的明年8月）。\n「〜と呼びかけている」— 呼吁…。例：観測をしようと呼びかけている（呼吁进行观测）。",
                "vocab": [["宇宙人", "うちゅうじん", "外星人"], ["謎めいた", "なぞめいた", "神秘的、谜一般的"], ["電波", "でんぱ", "电波"], ["受信", "じゅしん", "接收"], ["合同観測", "ごうどうかんそく", "联合观测"], ["呼びかける", "よびかける", "呼吁"]]
            },
            {
                "ja": "研究はSETI（セチ）と呼ばれる。「Search for ExtraTerrestrial Intelligence」の略で、地球外知的生命探査と訳される。つまり「宇宙人探し」だ。宇宙人探しの鍵とされるのが77年8月15日（日本時間16日）に米オハイオ州立大の「ビッグイヤー電波望遠鏡」で観測された電波だ。いて座の方角から受けた強い電波を短くとも72秒間、捉えた。",
                "en": "The research is called SETI. It is an abbreviation of \"Search for ExtraTerrestrial Intelligence,\" translated as the search for extraterrestrial intelligent life. In other words, it's \"alien hunting.\" The key to alien hunting is a radio wave observed on August 15, 1977 (the 16th in Japan time) by the \"Big Ear\" radio telescope at Ohio State University in the U.S. It captured a strong radio signal from the direction of the constellation Sagittarius for at least 72 seconds.",
                "literal": "该研究被称为SETI。是\"Search for ExtraTerrestrial Intelligence\"的缩写，被译为地球外知性生命探索。也就是\"寻找外星人\"。被视为寻找外星人关键的是77年8月15日（日本时间16日）由美国俄亥俄州立大学的\"大耳朵电波望远镜\"观测到的电波。从人马座方向接收到的强电波，至少捕捉了72秒。",
                "grammar": "「〜と呼ばれる」— 被称为…。例：研究はSETIと呼ばれる（研究被称为SETI）。\n「〜と訳される」— 被译为…。例：地球外知的生命探査と訳される（被译为地球外智慧生命探索）。\n「〜とされる」— 被视为…。例：鍵とされるのが…電波だ（被视为关键的是…电波）。",
                "vocab": [["略", "りゃく", "缩写、略称"], ["地球外", "ちきゅうがい", "地球外"], ["知的生命", "ちてきせいめい", "智慧生命"], ["探査", "たんさ", "探测"], ["望遠鏡", "ぼうえんきょう", "望远镜"], ["観測", "かんそく", "观测"]]
            },
            {
                "ja": "当時、データはタイプライターで記録用紙に打ち出されていた。自宅の台所で、記録用紙を広げた天文学者ジェリー・イーマン博士は該当の箇所を赤ペンで囲み、余白に「Wow（ワオ）！」と走り書きした。このため、Wow！信号と呼ばれるようになった。",
                "en": "At that time, data was printed out on recording paper by a typewriter. At the kitchen of his home, astronomer Dr. Jerry Ehman spread out the recording paper, circled the relevant section with a red pen, and scribbled \"Wow!\" in the margin. For this reason, it came to be called the \"Wow! Signal.\"",
                "literal": "当时，数据由打字机打印在记录纸上。在自己家的厨房里摊开记录纸的天文学家杰里·埃曼博士用红笔圈出相应位置，并在空白处潦草地写下\"Wow！（哇！）\"。因此，它开始被称为\"Wow！信号\"。",
                "grammar": "「〜で打ち出されていた」— 由…打印出来（被动态）。例：タイプライターで打ち出されていた（由打字机打印出来）。\n「〜ため」— 因此。例：このため、呼ばれるようになった（因此开始被称为）。\n「〜ようになった」— 变得…了。例：呼ばれるようになった（变得被这样称呼了）。",
                "vocab": [["タイプライター", "タイプライター", "打字机"], ["記録用紙", "きろくようし", "记录纸"], ["該当", "がいとう", "符合、相应"], ["余白", "よはく", "空白处"], ["走り書き", "はしりがき", "潦草地写"], ["天文学者", "てんもんがくしゃ", "天文学家"]]
            },
            {
                "ja": "この信号が注目される理由は電波の波長にある。天文学者の間で「宇宙人が交信に使うのではないか」と予想されていた「21センチ」。さらに電波の強さも通常、自然界に存在するものの約30倍で、星の爆発などの自然現象で起こったものとは考えにくかった。日本のSETI研究の第一人者の鳴沢真也・兵庫県立大専任講師は「合理的に考えると、宇宙人からの信号の可能性がある」と話す。",
                "en": "The reason this signal attracts attention lies in its wavelength. It was the \"21 centimeters\" that astronomers had predicted aliens might use for communication. Furthermore, the signal's strength was about 30 times that of things normally existing in nature, making it hard to consider it a natural phenomenon such as a stellar explosion. Narusawa Shinya, a leading figure in Japanese SETI research and a lecturer at the University of Hyogo, says, \"Thinking rationally, there is a possibility it is a signal from aliens.\"",
                "literal": "这个信号受到关注的理由在于电波的波长。是天文学家们之间被预测\"外星人会不会用于通信\"的\"21厘米\"。而且电波的强度也是自然界通常存在之物的约30倍，很难认为是由恒星爆炸等自然现象引起的。日本SETI研究的第一人、兵库县立大学专任讲师鸣泽真也表示：\"合理思考的话，存在来自外星人信号的可能性。\"",
                "grammar": "「〜にある」— 在于…。例：理由は波長にある（理由在于波长）。\n「〜のではないか」— 会不会是…呢。例：交信に使うのではないかと予想されていた（被预测会不会用于通信）。\n「〜にくい」— 难以…。例：考えにくかった（难以认为）。",
                "vocab": [["注目", "ちゅうもく", "注目"], ["波長", "はちょう", "波长"], ["交信", "こうしん", "通信联络"], ["自然界", "しぜんかい", "自然界"], ["自然現象", "しぜんげんしょう", "自然现象"], ["第一人者", "だいいちにんしゃ", "第一人、权威"]]
            },
        ]
    },
    {
        "slug": "seishoku-iryou-gairai",
        "title": "都立病院で初の「生殖医療外来」開設 最新の不妊治療が受けられるように",
        "subtitle": "from TBS NEWS DIG",
        "paras": [
            {
                "ja": "2割を超える夫婦が不妊の検査や治療を受ける中、最新の不妊治療が受けられる「生殖医療外来」が東京都立の病院で初めて開設されました。東京・豊島区の都立大塚病院。「人工授精」などの一般的な不妊治療に加え、最新の機器を使った「体外受精」や精子を針で卵子に直接注入する「顕微授精」といった\"高度な不妊治療\"を受けることができます。こうした治療を受けられるのは、都立の病院では初めてです。",
                "en": "As more than 20% of couples undergo infertility testing and treatment, a \"reproductive medicine outpatient clinic\" where the latest infertility treatments are available has opened for the first time at a Tokyo metropolitan hospital. It is at the Tokyo Metropolitan Otsuka Hospital in Toshima Ward, Tokyo. In addition to general infertility treatments such as artificial insemination, patients can receive \"advanced infertility treatments\" such as in vitro fertilization using the latest equipment and intracytoplasmic sperm injection, in which sperm is directly injected into the egg with a needle. It is the first time such treatments are available at a metropolitan hospital.",
                "literal": "在超过2成夫妇接受不孕检查和治疗的情况下，能够接受最新不孕治疗的\"生殖医疗门诊\"在东京都立医院首次开设。位于东京丰岛区的都立大冢医院。除\"人工授精\"等一般不孕治疗外，还可以接受使用最新设备的\"体外受精\"、用针将精子直接注入卵子的\"显微授精\"等\"高级不孕治疗\"。能够接受这些治疗，在都立医院中尚属首次。",
                "grammar": "「〜に加え」— 除…之外。例：一般的な不妊治療に加え（除一般不孕治疗之外）。\n「〜といった」— 诸如…之类的。例：「顕微授精」といった高度な治療（\"显微授精\"之类的高级治疗）。\n「〜ことができます」— 能够…。例：受けることができます（能够接受）。",
                "vocab": [["不妊", "ふにん", "不孕"], ["開設", "かいせつ", "开设"], ["人工授精", "じんこうじゅせい", "人工授精"], ["体外受精", "たいがいじゅせい", "体外受精"], ["精子", "せいし", "精子"], ["卵子", "らんし", "卵子"]]
            },
            {
                "ja": "国の機関の調査によりますと、国内で不妊の検査や治療の経験がある夫婦は22.7%。また、別の調査では、赤ちゃんのおよそ9人に1人が体外受精などで生まれていることが分かっています。こうしたことから、東京都は今年度、不妊治療の補助に56億円を投入しました。",
                "en": "According to a survey by a national institution, 22.7% of couples in Japan have experience with infertility testing or treatment. Another survey has found that about 1 in 9 babies are born through in vitro fertilization and other methods. For these reasons, the Tokyo Metropolitan Government has invested 5.6 billion yen in infertility treatment subsidies this fiscal year.",
                "literal": "根据国家机构的调查，国内有过不孕检查和治疗经验的夫妇占22.7%。另外，另一项调查表明，大约每9个婴儿中就有1个是通过体外受精等出生的。鉴于这些情况，东京都本年度在不孕治疗补助上投入了56亿日元。",
                "grammar": "「〜によりますと」— 根据…（郑重说法）。例：調査によりますと（根据调查）。\n「〜ことが分かっています」— 已知…。例：生まれていることが分かっています（已知是…出生的）。\n「〜ことから」— 鉴于…、由于…。例：こうしたことから、投入しました（鉴于这些情况，投入了…）。",
                "vocab": [["経験", "けいけん", "经验"], ["補助", "ほじょ", "补助"], ["投入", "とうにゅう", "投入"], ["今年度", "こんねんど", "本年度"], ["調査", "ちょうさ", "调查"], ["夫婦", "ふうふ", "夫妇"]]
            },
            {
                "ja": "東京都の去年の出生数は8万5064人で、10年ぶりに増加。一方、1人の女性が生涯で出産する子どもの数を示す合計特殊出生率は0.96で、全国で最も低くなっています。",
                "en": "The number of births in Tokyo last year was 85,064, increasing for the first time in 10 years. On the other hand, the total fertility rate — which shows the number of children a woman gives birth to over her lifetime — was 0.96, the lowest in the nation.",
                "literal": "东京都去年的出生数为8万5064人，时隔10年增加。另一方面，表示1名女性一生生育孩子数量的合计特殊出生率为0.96，为全国最低。",
                "grammar": "「〜ぶりに」— 时隔…。例：10年ぶりに増加（时隔10年增加）。\n「〜を示す」— 表示…。例：子どもの数を示す合計特殊出生率（表示孩子数量的合计特殊出生率）。\n「〜で最も〜」— 在…中最为…。例：全国で最も低い（全国最低）。",
                "vocab": [["出生数", "しゅっしょうすう", "出生数"], ["増加", "ぞうか", "增加"], ["生涯", "しょうがい", "一生"], ["出産", "しゅっさん", "分娩、生育"], ["合計特殊出生率", "ごうけいとくしゅしゅっしょうりつ", "合计特殊出生率"], ["全国", "ぜんこく", "全国"]]
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
