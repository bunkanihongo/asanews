#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-28 (Fri) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-28'
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
        "slug": "nakano-tokei-settou",
        "title": "中野ブロードウェイ時計店“2億円相当”窃盗　チリ国籍の男2人を逮捕",
        "subtitle": "from 日テレNEWS NNN",
        "paras": [
            {
                "ja": "東京・中野区の「中野ブロードウェイ」にある時計販売店から、腕時計4本あわせて約2億円相当が盗まれた事件で、警視庁は24歳と30歳のチリ国籍の男2人を逮捕しました。逮捕されたのは、いずれもチリ国籍のピニャ・グスマン容疑者とマンサーノ・ケサダ容疑者です。警視庁によりますと、2人は今月25日、時計店のショーケースをハンマーで割り、腕時計を盗んだ疑いがもたれています。",
                "en": "In a case in which four wristwatches worth a total of about 200 million yen were stolen from a watch shop in the \"Nakano Broadway\" in Tokyo's Nakano Ward, the Metropolitan Police Department arrested two Chilean men aged 24 and 30. Those arrested were Pina Guzman and Manzano Quesada, both Chilean nationals. According to the Metropolitan Police, the two are suspected of smashing the shop's display case with a hammer and stealing wristwatches on the 25th of this month.",
                "literal": "在从东京・中野区的「中野百老汇」内的手表销售店被盗走4只手表、合计约2亿日元的事件中，警视厅逮捕了24岁和30岁的2名智利国籍男子。被逮捕的是均为智利国籍的皮尼亚・古斯曼嫌疑人和曼萨诺・凯萨达嫌疑人。据警视厅称，2人于本月25日，用锤子砸碎手表店的展示柜，涉嫌盗走手表。",
                "grammar": "「〜あわせて」— 合计、共计…。例：腕時計4本あわせて約2億円相当（4只手表合计约2亿日元）。\n「〜られました」— 被…（被动式）。例：逮捕されました（被逮捕了）。\n「〜によりますと」— 据…、按照…。例：警視庁によりますと（据警视厅称）。",
                "vocab": [["時計販売店", "とけいはんばいてん", "手表销售店"], ["窃盗", "せっとう", "盗窃"], ["逮捕", "たいほ", "逮捕"], ["ショーケース", "しょーけーす", "展示柜、橱窗"], ["ハンマー", "はんまー", "锤子"], ["容疑", "ようぎ", "嫌疑"]]
            },
            {
                "ja": "2人は25日の犯行後、電動キックボードを借りて二手に分かれて逃走していましたが、27日午後、大阪市内の民泊施設にいたところを捜査員に身柄を確保されました。被害品とみられる高級腕時計1本を所持していたということです。また、2人は事件の4日前に来日して都内の民泊施設に滞在し、2日前に現場を下見していたことも分かりました。",
                "en": "After the crime on the 25th, the two separated and fled by renting electric kick scooters, but on the afternoon of the 27th they were detained by investigators at a private lodging facility in Osaka City. They reportedly possessed one luxury wristwatch believed to be part of the stolen goods. It was also learned that the two had arrived in Japan four days before the incident, stayed at a private lodging facility in Tokyo, and had scouted the scene two days earlier.",
                "literal": "2人于25日作案后，租借电动滑板车分头逃走，但27日下午，在大阪市内的民宿设施被搜查人员控制住。据说持有1只被认为是赃物的高级手表。另外，也查明2人在事件4天前来到日本，滞留在东京都内的民宿设施，并在2天前预先查看了现场。",
                "grammar": "「〜二手に分かれて」— 分成两路…。例：二手に分かれて逃走（分成两路逃走）。\n「〜ところを」— 正在…的时候被…。例：民泊施設にいたところを身柄を確保されました（正在民宿时被控制住）。\n「〜ということも分かりました」— 也查明…。例：下見していたことも分かりました（也查明曾预先查看）。",
                "vocab": [["犯行", "はんこう", "作案、犯罪行为"], ["電動キックボード", "でんどうきっくぼーど", "电动滑板车"], ["捜査員", "そうさいん", "搜查人员、调查员"], ["身柄を確保", "みがらをかくほ", "拘留、控制住"], ["所持", "しょじ", "持有"], ["下見", "したみ", "预先查看、踩点"]]
            },
            {
                "ja": "調べに対し、ピニャ・グスマン容疑者は「私が盗んだのは1本で、他の3本は分からない」と容疑を一部否認していますが、マンサーノ・ケサダ容疑者は容疑を認め、「時計を売って金にして母国に持って帰るつもりだった」と供述しているということです。警視庁は2人の余罪や、被害品の売却先などについても詳しく調べています。",
                "en": "In response to questioning, Pina Guzman denies the charges in part, saying \"I only stole one, and I don't know about the other three,\" while Manzano Quesada reportedly admitted to the charges, stating, \"I intended to sell the watches, turn them into money, and take it back to my home country.\" The Metropolitan Police Department is also investigating the two's other possible crimes and the destination where the stolen goods were sold.",
                "literal": "面对调查，皮尼亚・古斯曼嫌疑人称「我偷的只有1只，另外3只我不知道」，部分否认嫌疑，但曼萨诺・凯萨达嫌疑人承认嫌疑，并供述称「打算卖掉手表换成钱带回母国」。警视厅也在详细调查2人的其他罪行以及赃物出售去向等。",
                "grammar": "「〜に対し」— 对于…、面对…。例：調べに対し（面对调查）。\n「〜ところを／〜と供述している」— 据供述…。例：母国に持って帰るつもりだったと供述（供述打算带回母国）。\n「〜についても」— 关于…也…。例：売却先などについても調べています（也调查出售去向等）。",
                "vocab": [["否認", "ひにん", "否认"], ["供述", "きょうじゅつ", "供述"], ["母国", "ぼこく", "母国、祖国"], ["余罪", "よざい", "其余罪行"], ["売却先", "ばいきゃくさき", "出售去向、变卖对象"], ["詳細", "しょうさい", "详细"]]
            },
        ]
    },
    {
        "slug": "jichidai-shugaku-shikin",
        "title": "自治医大・修学資金3766万円“一括返還”巡る訴訟　「約束したんだから返せ」の声に原告医師が反論",
        "subtitle": "from 弁護士JPニュース",
        "paras": [
            {
                "ja": "自治医科大学を2022年に卒業した医師のA氏は、母校と愛知県を相手取り、修学資金3766万円の“一括返還”を求められる制度は違憲・違法だと主張して、東京地裁で争っています。8月26日、第7回口頭弁論の期日後、A氏は都内で会見を開き「約束だけで世の中がうまく回るなら、そもそも法律という仕組みはいらないのではないか」と述べ、報道を見る人にこの一点を考えてほしいと訴えました。",
                "en": "Doctor A, who graduated from Jichi Medical University in 2022, is fighting in the Tokyo District Court against his alma mater and Aichi Prefecture, arguing that the system requiring a \"lump-sum repayment\" of 37.66 million yen in educational funds is unconstitutional and illegal. After the date of the 7th oral argument on August 26, Mr. A held a press conference in Tokyo, stating, \"If the world could work properly on promises alone, then the system of law wouldn't be needed in the first place,\" and appealed to people watching the news to think about that one point.",
                "literal": "2022年毕业于自治医科大学的医生A先生，以母校和爱知县为对方，主张要求“一次性返还”3766万日元修学资金的制度违宪、违法，正在东京地方法院进行诉讼。8月26日，在第7次口头辩论的期日之后，A先生在东京都内召开记者会，表示「如果仅凭约定就能让世界顺利运转，那么从一开始就不需要法律这样的机制吧」并呼吁看报道的人思考这一点。",
                "grammar": "「〜を相手取り」— 以…为对手、状告…。例：母校と愛知県を相手取り（以母校和爱知县为对手）。\n" 
                "「〜ではないか」— 难道不是…吗。例：法律という仕組みはいらないのではないか（难道不需要法律机制吗）。\n「〜と訴えた」— 呼吁…、倾诉…。例：考えてほしいと訴えました（呼吁希望大家思考）。",
                "vocab": [["卒業", "そつぎょう", "毕业"], ["修学資金", "しゅうがくしきん", "修学资金、就学资助"], ["一括返還", "いっかつへんかん", "一次性返还"], ["違憲", "いけん", "违宪"], ["口頭弁論", "こうとうべんろん", "口头辩论"], ["記者会見", "きしゃかいけん", "记者会"]]
            },
            {
                "ja": "A氏は昨年3月の提訴時の会見で、自治医大の修学資金制度を「無知な受験生を囲い込んで、卒業後、退職の自由を奪った上、不当な労働条件で使いたおす、まさに悪魔のような制度」と非難していました。一方で、A氏の訴えに対し、ネット上などでは「そういう大学だと分かって入ったのに、なぜ文句を言うのか」という声が繰り返し向けられてきたといいます。",
                "en": "At a press conference when he filed suit last March, Mr. A criticized Jichi Medical University's educational fund system as \"truly a devil-like system that corners ignorant examinees, takes away their freedom to resign after graduation, and wears them out under unfair working conditions.\" Meanwhile, against Mr. A's claims, voices such as \"You entered knowing what kind of university it was, so why complain?\" have reportedly been repeatedly directed at him online.",
                "literal": "A先生于去年3月提起诉讼时的记者会上，批评自治医大的修学资金制度是「把无知的考生圈住，毕业后剥夺辞职自由，再用不当的劳动条件使人耗尽，简直是恶魔般的制度」。另一方面，针对A先生的诉求，网络等处据称反复传来「既然知道是这样的大学还进去，为什么要抱怨」的声音。",
                "grammar": "「〜を奪った上」— 在剥夺…之后、还…。例：退職の自由を奪った上（剥夺辞职自由之后）。\n" 
                "「〜に対し」— 针对…。例：A氏の訴えに対し（针对A先生的诉求）。\n「〜のに」— 明明…却…。例：分かって入ったのに（明明知道却进去了）。",
                "vocab": [["提訴", "ていそ", "提起诉讼"], ["無知", "むち", "无知"], ["退職", "たいしょく", "辞职、退休"], ["不当", "ふとう", "不当、不合理"], ["非難", "ひなん", "批评、指责"], ["文句", "もんく", "抱怨、牢骚"]]
            },
            {
                "ja": "会見でA氏は「卒業後に地域医療に従事する大学だという点は理解して入学した」と認めたうえで、知らされていなかった点が2つあったと語りました。1つは、条件の苛烈さで、卒業後の約10年間は勤務地も診療科も決められ、制度から離脱すれば元本に利息が加わって一括返還を迫られます。もう1つは、そうした具体的な契約内容が、入学手続きの段階で初めて示されたことだといいます。A氏は「世の中には約束より上位に立つ法律がある」と強調しました。",
                "en": "At the press conference, Mr. A acknowledged, \"I entered the university understanding that it is a school where graduates work in community medicine,\" but said there were two points he had not been informed of. One was the harshness of the conditions: for about 10 years after graduation, both the workplace and the clinical department were decided for him, and if he left the system, interest would be added to the principal and he would be forced to repay in a lump sum. The other, he says, is that such specific contract details were only first shown at the stage of enrollment procedures. Mr. A emphasized, \"In this world, there is law that stands above promises.\"",
                "literal": "在记者会上，A先生承认「毕业后面向地域医疗工作的这一点是理解后入学的」，但说有两个未被告知的地方。一个是条件的严酷。毕业后约10年间工作地点和诊疗科目都被决定，如果脱离制度，本金会加上利息被迫一次性返还。另一个据说是，这样的具体合同内容，在入学手续阶段才第一次被出示。A先生强调「世界上有比约定更上位、站得更高的法律」。",
                "grammar": "「〜に従事する」— 从事…。例：地域医療に従事する大学（从事地域医疗的大学）。\n" 
                "「〜たうえで」— 在…之后、…的基础上。例：認めたうえで（承认之后）。\n「〜ば〜られる」— 如果…就会被…。例：離脱すれば…迫られます（一旦脱离就会被迫…）。",
                "vocab": [["地域医療", "ちいきいりょう", "地域医疗"], ["従事", "じゅうじ", "从事"], ["苛烈", "かれつ", "严酷、苛刻"], ["診療科", "しんりょうか", "诊疗科目"], ["離脱", "りだつ", "脱离、退出"], ["元本", "がんぽん", "本金"], ["強調", "きょうちょう", "强调"]]
            },
        ]
    },
    {
        "slug": "takaichi-chuugoku-dentatsu",
        "title": "「高市首相の答弁変わらぬ限り、政策変えぬ」　中国側が訪中団に伝達",
        "subtitle": "from 毎日新聞",
        "paras": [
            {
                "ja": "中国を訪問中の中道改革連合の伊佐進一広報委員長ら超党派の議員団は27日、中国共産党の対外交流部門である中央対外連絡部の陸慷副部長と会談しました。終了後、伊佐氏は記者団の取材に応じ、台湾有事を巡る高市早苗首相の国会答弁について「この発言あるいは認識が変わらない限りは、中国としては政策を変えるつもりはない」と陸氏から伝えられたと明らかにしました。",
                "en": "A bipartisan delegation led by Isao Isa, public relations chairman of the Reform Coalition, which is currently visiting China, met on the 27th with Lu Kang, deputy head of the International Department of the CPC Central Committee, the external exchange body of the Chinese Communist Party. Afterward, Mr. Isa told reporters that Mr. Lu had conveyed that \"as long as this statement or the understanding does not change, China has no intention of changing its policy,\" referring to Prime Minister Sanae Takaichi's Diet response regarding a Taiwan contingency.",
                "literal": "正在访问中国的中间改革联合公关委员长伊佐进一等超党派议员团，于27日与中国共产党的对外交流部门、中央对外联络部副部长陆慷进行了会谈。结束后，伊佐氏应记者团采访，就围绕台湾有事的高市早苗首相的国会答辩透露「只要这个发言或认识不改变，中国方面就不打算改变政策」，这是陆氏传达给他的。",
                "grammar": "「〜を巡る」— 围绕…。例：台湾有事を巡る国会答弁（围绕台湾有事的国会答辩）。\n「〜限りは」— 只要…就…。例：認識が変わらない限りは（只要认识不改变）。\n「〜と明らかにした」— 明确表示…、透露…。例：伝えられたと明らかにしました（明确表示被告知…）。",
                "vocab": [["超党派", "ちょうとうは", "跨党派、超党派"], ["会談", "かいだん", "会谈"], ["外交部", "がいこうぶ", "外交部"], ["答弁", "とうべん", "答辩、答复"], ["有事", "ゆうじ", "突发事件、紧急事态"], ["伝達", "でんたつ", "传达"]]
            },
            {
                "ja": "会談は当初予定の1時間を超え、2時間にわたったといいます。伊佐氏は文化・青年交流を提案したほか、中国での日本人の拘束事案を巡る懸念や、デュアルユース（軍民両用）品目の輸出規制などが中国経済にも悪影響を与えることを伝達しました。また、東・南シナ海で活発化する中国の軍事活動などについても議論したということです。",
                "en": "The talks reportedly lasted two hours, exceeding the initially scheduled one hour. In addition to proposing cultural and youth exchanges, Mr. Isa conveyed concerns over cases of Japanese nationals detained in China, and that export restrictions on dual-use (civilian and military) items would also have a negative impact on China's economy. He also discussed topics including China's increasingly active military activities in the East and South China Seas.",
                "literal": "会谈据说超过了最初预定的一小时，长达两小时。伊佐氏除了提议文化・青年交流之外，也传达了围绕中国境内日本人被拘案件的不安，以及军民两用品目（军民两用）的出口限制等也会给中国经济带来负面影响。另外，也就东海・南海趋于活跃的中国军事活动等进行了讨论。",
                "grammar": "「〜にわたった」— 持续…、长达…。例：2時間にわたった（长达2小时）。\n「〜ほか」— 除了…之外。例：文化・青年交流を提案したほか（除了提议文化青年交流之外）。\n「〜を巡る」— 围绕…。例：拘束事案を巡る懸念（围绕拘押案件的不安）。",
                "vocab": [["超える", "こえる", "超过"], ["青年交流", "せいねんこうりゅう", "青年交流"], ["拘束", "こうそく", "拘押、限制"], ["懸念", "けねん", "担忧、不安"], ["デュアルユース", "でゅあるゆーす", "军民两用"], ["輸出規制", "ゆしゅつきせい", "出口限制"]]
            },
            {
                "ja": "伊佐氏は「今回の訪中は、正常化に向けた雰囲気作りだという点については、両者ともお互いに認識の一致があった」と語る一方で、「激しいやりとりも多く、中国側の厳しい姿勢が示された」とも振り返りました。11月に中国で開かれるAPEC首脳会議での日中首脳会談などハイレベル交流が進む可能性については「そんな簡単な話ではないと思う」と述べています。",
                "en": "While saying \"regarding the point that this visit to China was about creating an atmosphere toward normalization, both sides shared a mutual understanding,\" Mr. Isa also recalled that \"there was a lot of intense exchange, and China's tough posture was shown.\" Regarding the possibility of high-level exchanges such as a Japan-China summit meeting at the APEC leaders' meeting to be held in China in November, he stated, \"I don't think it's that simple.\"",
                "literal": "伊佐氏一方面说「关于这次的访华是面向正常化营造氛围这一点，双方彼此有认识的一致」，另一方面回顾说「激烈的交锋也很多，显示了中方的严厉姿态」。关于11月在中国举行的APEC首脑会议上日中首脑会谈等高层交流推进的可能性，他表示「我认为并不是那么简单的事」。",
                "grammar": "「〜一方で」— 一方面…另一方面…。例：語る一方で（一方面这样说）。\n「〜に向けた」— 面向…的。例：正常化に向けた雰囲気作り（面向正常化的氛围营造）。\n「〜可能性については」— 关于…的可能性。例：ハイレベル交流が進む可能性については（关于高层交流推进的可能性）。",
                "vocab": [["訪中", "ほうちゅう", "访华"], ["正常化", "せいじょうか", "正常化"], ["雰囲気作り", "ふんいきづくり", "营造氛围"], ["激しい", "はげしい", "激烈的"], ["姿勢", "しせい", "姿态、态度"], ["ハイレベル", "はいれべる", "高层、高水准"]]
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
