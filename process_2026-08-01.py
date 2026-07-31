#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-01 (Sat) Edition"""
import json, os, subprocess, re, time
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-01'
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
# TODAY'S ARTICLES — 2026-08-01
# ==================================================================
articles = [
    {
        "slug": "kumamoto-yure-saidaichi-2437gal",
        "title": "熊本地震の揺れ 10年前の地震を上回る 最大2400ガル超",
        "subtitle": "今回の熊本地震で観測された揺れの大きさが10年前の熊本地震を上回った。宇城市豊野町では2437ガルを観測し、阪神・淡路大震災を上回るレベルに。",
        "paras": [
            {
                "ja": "今回の地震で観測された揺れの大きさは、10年前の熊本地震を上回ったことが分かりました。物を固定していないと吹き飛ぶレベルとされる1000ガルに対し、宇城市豊野町で観測された揺れは2400ガルを超えました。熊本市が金沢大学などと共同で行った実験では、補強していない石垣は200ガルで崩れましたが、補強した石垣は1000ガルでも崩れませんでした。",
                "en": "It has been found that the shaking observed in this earthquake exceeded that of the Kumamoto earthquake 10 years ago. While 1,000 gal is considered the level at which unsecured objects get blown away, the shaking observed in Toyono-cho, Uki City exceeded 2,400 gal. In an experiment conducted jointly by Kumamoto City and Kanazawa University, an unreinforced stone wall collapsed at 200 gal, but a reinforced wall did not collapse even at 1,000 gal.",
                "literal": "此次地震观测到的摇晃程度，已判明超过了10年前的熊本地震。相对于不固定的物体就会被吹飞的水平1000伽，宇城市丰野町观测到的摇晃超过了2400伽。在熊本市与金泽大学等共同进行的实验中，未加固的石墙在200伽时崩塌，但加固后的石墙即使在1000伽也没有崩塌。",
                "grammar": "「〜ことが分かりました」— 判明…。例：上回ったことが分かりました（判明超过了）。\n「〜とされる」— 被认为是…。例：吹き飛ぶレベルとされています（被认为是吹飞的水平）。\n「〜に対し」— 相对于…。例：1000ガルに対し（相对于1000伽）。",
                "vocab": [
                    ["観測", "かんそく", "观测"],
                    ["上回る", "うわまわる", "超过、超出"],
                    ["固定", "こてい", "固定"],
                    ["石垣", "いしがき", "石墙"],
                    ["補強", "ほきょう", "加固、补强"],
                    ["崩れる", "くずれる", "崩塌、坍塌"]
                ]
            },
            {
                "ja": "気象庁などのまとめによりますと、今回の地震の最大値は宇城市豊野町で観測した2437ガルで、10年前の熊本地震で大津町が観測した1791ガルを大きく上回りました。この2400ガルは阪神・淡路大震災を上回り、最近では能登半島地震に次ぐレベルとなっています。九州大学の松本聡教授は「かなり大きい加速度だと思います。壊れていく方向など、詳しく調査されていくと思います」と話しています。",
                "en": "According to summaries by the Japan Meteorological Agency and others, the maximum value of this earthquake was 2,437 gal observed in Toyono-cho, Uki City, far exceeding the 1,791 gal recorded in Ozu Town during the Kumamoto earthquake 10 years ago. This 2,400 gal level exceeds the Great Hanshin-Awaji Earthquake and is second only to the Noto Peninsula earthquake in recent years. Professor Satoshi Matsumoto of Kyushu University commented, 'This is quite a large acceleration. The direction of fracturing and other details will be investigated in depth.'",
                "literal": "据气象厅等的汇总，此次地震的最大值是宇城市丰野町观测到的2437伽，大幅超过了10年前熊本地震中大津町观测到的1791伽。这2400伽超过了阪神·淡路大地震，是最近仅次于能登半岛地震的水平。九州大学的松本聪教授表示：「我认为这是相当大的加速度。破坏的方向等，预计会被详细调查。」",
                "grammar": "「〜によりますと」— 据…称。例：気象庁などのまとめによりますと（据气象厅等的汇总）。\n「〜に次ぐ」— 仅次于…。例：能登半島地震に次ぐレベル（仅次于能登半岛地震的水平）。\n「〜と話しています」— 表示说…。例：調査されていくと思いますと話しています（表示说预计会被调查）。",
                "vocab": [
                    ["最大値", "さいだいち", "最大值"],
                    ["加速度", "かそくど", "加速度"],
                    ["阪神・淡路大震災", "はんしんあわじだいしんさい", "阪神淡路大地震"],
                    ["能登半島地震", "のとはんとうじしん", "能登半岛地震"],
                    ["教授", "きょうじゅ", "教授"],
                    ["詳しく", "くわしく", "详细地"]
                ]
            }
        ]
    },
    {
        "slug": "hamas-busou-kaijo-goui",
        "title": "ハマス 武装解除で合意と幹部が明かす ガザ撤退も含む",
        "subtitle": "イスラム組織ハマスの幹部が31日、イスラエルとの紛争終結に向けた合意に、武器に関する規定やガザからのイスラエル軍の段階的撤退が含まれると明かした。",
        "paras": [
            {
                "ja": "イスラム組織ハマスの幹部は31日、イスラエルと結ばれた紛争終結に向けた合意には、ハマスの武器に関する規定や、パレスチナ自治区ガザ地区からのイスラエル軍の段階的撤退が含まれていると明かしました。ハマスの武装解除は、昨年10月からガザで続く停戦協定の進展において、大きな障害の一つとなっていました。",
                "en": "A senior Hamas official revealed on the 31st that the agreement toward ending the conflict with Israel includes provisions regarding Hamas's weapons and a phased withdrawal of Israeli forces from the Gaza Strip in the Palestinian territories. Hamas's disarmament had been one of the major obstacles in the progress of the ceasefire agreement that has continued in Gaza since last October.",
                "literal": "伊斯兰组织哈马斯的干部31日透露，与以色列缔结的旨在终结纷争的协议中，包含关于哈马斯武器的规定以及以色列军队从巴勒斯坦自治区加沙地带阶段性撤退的内容。哈马斯的解除武装，在去年10月以来加沙持续的停战协定的进展中，一直是重大障碍之一。",
                "grammar": "「〜に向けた」— 面向…的。例：紛争終結に向けた合意（面向终结纷争的协议）。\n「〜が含まれている」— 包含…。例：規定が含まれている（包含规定）。\n「〜において」— 在…中。例：停戦協定の進展において（在停战协定的进展中）。",
                "vocab": [
                    ["幹部", "かんぶ", "干部、高层"],
                    ["紛争終結", "ふんそうしゅうけつ", "终结纷争"],
                    ["武器", "ぶき", "武器"],
                    ["段階的", "だんかいてき", "阶段性的"],
                    ["撤退", "てったい", "撤退"],
                    ["停戦協定", "ていせんきょうてい", "停战协定"]
                ]
            },
            {
                "ja": "幹部は「武器の問題に関して合意に達した。さらに、イスラエル軍の段階的な撤退についても合意に達した」と述べました。ハマスは今後、仲介者やドナルド・トランプ米大統領の平和評議会が、イスラエルに合意条件の順守を促すことを期待しています。ハマス交渉団の幹部は「ガザの人々のために、殺りくと強制移住から救うべく譲歩を行っている」と説明しています。",
                "en": "The official stated, 'We have reached an agreement on the weapons issue. Furthermore, we have also reached an agreement on the phased withdrawal of Israeli forces.' Hamas now expects mediators and the peace council of U.S. President Donald Trump to urge Israel to comply with the agreement's terms. A senior Hamas negotiating team official explained that they are 'making concessions to save the people of Gaza from slaughter and forced displacement.'",
                "literal": "干部表示：「关于武器问题已达成一致。此外，关于以色列军队的阶段性撤退也已达成一致。」哈马斯今后期待调解者和美国总统特朗普的和平评议会促使以色列遵守协议条件。哈马斯谈判团的干部说明：「为了加沙的人们，正在做出让步以将他们从杀戮和强制迁移中拯救出来。」",
                "grammar": "「〜に達した」— 达成了…。例：合意に達した（达成了协议）。\n「〜と述べました」— 表示说…。例：合意に達したと述べました（表示说达成了协议）。\n「〜べく」— 为了…。例：救うべく譲歩を行っている（为了拯救而做出让步）。",
                "vocab": [
                    ["仲介者", "ちゅうかいしゃ", "调解者、中间人"],
                    ["順守", "じゅんしゅ", "遵守"],
                    ["交渉団", "こうしょうだん", "谈判团"],
                    ["譲歩", "じょうほ", "让步"],
                    ["殺りく", "さつりく", "杀戮"],
                    ["強制移住", "きょうせいいじゅう", "强制迁移"]
                ]
            }
        ]
    },
    {
        "slug": "aeon-kumamoto-bakuhatsu-haha",
        "title": "イオン爆発で娘失った母親 「金庫にお金を入れないと」と言い残し戻る",
        "subtitle": "最大震度7の熊本地震から4日目。爆発事故のあったイオンモール熊本では7人の死亡が確認され、犠牲になった22歳女性の母親が当時の心境を語った。",
        "paras": [
            {
                "ja": "最大震度7を記録した熊本地震から4日目です。地震直後に爆発事故が起きた熊本県嘉島町のイオンモール熊本では、これまでに7人の死亡が確認されています。そのうち3人はアパレル大手「オンワードホールディングス」の従業員だったことが明らかになっています。別の店舗で働いていた22歳の女性の母親が、RKK熊本放送の取材に応じ、苦しい胸の内を語りました。",
                "en": "It is the fourth day since the Kumamoto earthquake that recorded a maximum seismic intensity of 7. At Aeon Mall Kumamoto in Kashima Town, Kumamoto Prefecture, where an explosion occurred right after the earthquake, seven deaths have been confirmed so far. It has been revealed that three of them were employees of the major apparel company Onward Holdings. The mother of a 22-year-old woman who worked at another store spoke to RKK Kumamoto Broadcasting about her painful feelings.",
                "literal": "是记录了最大震度7的熊本地震的第4天。在地震后立刻发生爆炸事故的熊本县嘉岛町AEON MALL熊本，迄今已确认7人死亡。其中3人是服装大企业「Onward Holdings」的员工一事已经明确。在另一家店铺工作的22岁女性的母亲，接受了RKK熊本放送的采访，讲述了痛苦的心情。",
                "grammar": "「〜から4日目」— 距…第4天。例：熊本地震から4日目です（是熊本地震后第4天）。\n「〜が確認されています」— 已确认…。例：死亡が確認されています（已确认死亡）。\n「〜が明らかになっています」— 已明确…。例：従業員だったことが明らかになっています（已明确曾是员工）。",
                "vocab": [
                    ["最大震度", "さいだいしんど", "最大震度"],
                    ["爆発", "ばくはつ", "爆炸"],
                    ["アパレル大手", "あぱれるおおて", "服装业大企业"],
                    ["従業員", "じゅうぎょういん", "员工"],
                    ["取材", "しゅざい", "采访"],
                    ["胸の内", "むねのうち", "内心、心事"]
                ]
            },
            {
                "ja": "母親によりますと、娘は爆発が起きたとみられる場所の近くにある2階の店舗で働いていて、爆発の後から連絡が取れなくなりました。地震の直後に一度、建物の外へ避難しましたが、「金庫にお金を入れないといけないと言われたので戻る」と言って、同僚と2人で建物の中に戻ったといいます。母親は「入金のために、お金のために…。会社には真実をはっきり話してほしい」と訴えています。",
                "en": "According to the mother, her daughter worked at a second-floor store near where the explosion is believed to have occurred, and contact was lost after the explosion. She had once evacuated outside the building immediately after the earthquake, but reportedly said, 'I was told I have to put money in the safe, so I'm going back,' and returned inside the building with a colleague. The mother pleads, 'She went back for the deposit, for the money... I want the company to tell us the truth clearly.'",
                "literal": "据母亲称，女儿在疑似爆炸发生地点附近的2楼店铺工作，爆炸后失去了联系。地震后立刻一度避难到建筑物外，但说着「被告知必须把钱放进金库所以要回去」，与同事2人回到了建筑物内。母亲呼吁：「为了入账，为了钱…。希望公司清楚地告诉我们真相。」",
                "grammar": "「〜によりますと」— 据…称。例：母親によりますと（据母亲称）。\n「〜とみられる」— 被认为是…。例：起きたとみられる場所（被认为是发生的地点）。\n「〜と言って戻った」— 说着…回去了。例：「戻る」と言って戻った（说着要回去便回去了）。",
                "vocab": [
                    ["店舗", "てんぽ", "店铺"],
                    ["連絡が取れない", "れんらくがとれない", "联系不上"],
                    ["避難", "ひなん", "避难"],
                    ["金庫", "きんこ", "保险柜、金库"],
                    ["同僚", "どうりょう", "同事"],
                    ["訴える", "うったえる", "呼吁、申诉"]
                ]
            }
        ]
    },
    {
        "slug": "kurashiki-sasareru-sibou",
        "title": "倉敷市で男性が刺され死亡 おいの男を殺人容疑で確保",
        "subtitle": "31日午後、岡山県倉敷市の会社敷地内で62歳の男性が刃物で刺され死亡。県警は被害者のおいで40代の男を確保し、事情を聴いている。",
        "paras": [
            {
                "ja": "31日午後5時20分ごろ、岡山県倉敷市真備町箭田の有限会社古城池開発で「夫が刺された」と110番通報がありました。岡山県警などによりますと、会社員の下田一郎さん（62）が事務所の外で血を流して倒れているのを、悲鳴を聞いて駆けつけた妻（64）が発見しました。下田さんは意識不明の状態で病院に搬送されましたが、その後、死亡が確認されました。",
                "en": "Around 5:20 PM on the 31st, a 110 emergency call was made reporting 'My husband has been stabbed' at the limited company Kojoike Kaihatsu in Mabi-cho Yata, Kurashiki City, Okayama Prefecture. According to Okayama Prefectural Police and others, the wife (64) of company employee Ichiro Shimoda (62), who rushed over upon hearing screams, found him collapsed and bleeding outside the office. Shimoda was taken to the hospital unconscious and his death was later confirmed.",
                "literal": "31日下午5点20分左右，冈山县仓敷市真备町箭田的有限公司古城池开发接到「丈夫被刺了」的110报警。据冈山县警等称，听到惨叫赶来的妻子（64岁）发现了公司职员下田一郎（62岁）在办公室外流血倒地。下田先生以意识不明的状态被送往医院，但之后确认死亡。",
                "grammar": "「〜ごろ」— 大约…时。例：午後5時20分ごろ（下午5点20分左右）。\n「〜によりますと」— 据…称。例：岡山県警などによりますと（据冈山县警等称）。\n「〜を発見しました」— 发现了…。例：倒れているのを発見しました（发现了倒地的他）。",
                "vocab": [
                    ["110番通報", "ひゃくとうばんつうほう", "拨打110报警"],
                    ["会社員", "かいしゃいん", "公司职员"],
                    ["血を流す", "ちをながす", "流血"],
                    ["悲鳴", "ひめい", "惨叫、尖叫声"],
                    ["駆けつける", "かけつける", "赶到、急忙赶到"],
                    ["搬送", "はんそう", "运送（送医）"]
                ]
            },
            {
                "ja": "県警は、下田さんを刺した後、車で逃走したとみられる人物の行方を追い、下田さんのおいで40代の男を同市内で確保しました。男は酒津公園付近の川の中で見つかり、警察の説得に応じたということです。県警は殺人容疑で詳しい事情を聴くとともに、2人の間に何らかのトラブルがあったとみて調べています。",
                "en": "The prefectural police pursued the person believed to have fled by car after stabbing Shimoda, and located the suspect — a man in his 40s who is Shimoda's nephew — within the city. The man was found in a river near Sakazu Park and reportedly responded to police persuasion. The police are questioning him on suspicion of murder while investigating the possibility that some kind of trouble existed between the two men.",
                "literal": "县警追踪了被认为刺伤下田后驾车逃跑的人物的行踪，在市内确保了是下田外甥的40多岁男子。男子在酒津公园附近的河中被发现，据称听从了警察的劝说。县警以杀人嫌疑听取详细情况的同时，认为两人之间可能存在某种纠纷，正在进行调查。",
                "grammar": "「〜とみられる」— 被认为是…。例：逃走したとみられる人物（被认为是逃跑的人物）。\n「〜に応じた」— 听从了…。例：説得に応じた（听从了劝说）。\n「〜とみて調べています」— 认为…并正在调查。例：トラブルがあったとみて調べています（认为有纠纷正在调查）。",
                "vocab": [
                    ["逃走", "とうそう", "逃跑"],
                    ["行方", "ゆくえ", "行踪、下落"],
                    ["確保", "かくほ", "抓获、确保"],
                    ["説得", "せっとく", "劝说、说服"],
                    ["容疑", "ようぎ", "嫌疑"],
                    ["トラブル", "とらぶる", "纠纷、麻烦"]
                ]
            }
        ]
    },
    {
        "slug": "kitami-tamanegi-konbena",
        "title": "たまねぎ処理工場で男性がコンテナに挟まれ死亡 北海道・北見市",
        "subtitle": "7月31日、北海道北見市のたまねぎ処理工場で、機械の点検中だった男性が倒れてきたコンテナに上半身を挟まれ、死亡した。",
        "paras": [
            {
                "ja": "北海道・北見警察署は2026年7月31日、北見市端野町で作業事故が発生し、男性が死亡したと発表しました。作業事故があったのは、北見市端野町にあるたまねぎ処理工場です。31日正午ごろ、消防から警察に「たまねぎ処理工場内での事故」と通報がありました。",
                "en": "Kitami Police Station in Hokkaido announced on July 31, 2026 that a work accident occurred in Tanno-cho, Kitami City and a man died. The accident took place at an onion processing factory in Tanno-cho, Kitami City. Around noon on the 31st, the fire department notified police of 'an accident inside the onion processing factory.'",
                "literal": "北海道·北见警察署于2026年7月31日宣布，北见市端野町发生了作业事故，一名男性死亡。发生作业事故的是位于北见市端野町的洋葱处理工厂。31日正午左右，消防向警察通报了「洋葱处理工厂内的事故」。",
                "grammar": "「〜と発表しました」— 发表了…。例：死亡したと発表しました（发表了死亡的消息）。\n「〜によると」— 据…。例：消防から警察に（此处表示通报内容）。\n「〜ごろ」— 大约…时。例：31日正午ごろ（31日正午左右）。",
                "vocab": [
                    ["作業事故", "さぎょうじこ", "作业事故"],
                    ["処理工場", "しょりこうじょう", "处理工厂"],
                    ["たまねぎ", "たまねぎ", "洋葱"],
                    ["発表", "はっぴょう", "公布、发表"],
                    ["通報", "つうほう", "通报、报警"]
                ]
            },
            {
                "ja": "男性は、たまねぎの茎と葉を取り除く機械の点検中、異音が聞こえたことからのぞき込んだところ、倒れてきたコンテナに上半身を挟まれたということです。男性は病院に搬送されましたが、その後、死亡しました。警察は当時の詳しい状況を調べています。",
                "en": "The man was inspecting a machine that removes onion stems and leaves when, after hearing an unusual noise and leaning in to look, he was reportedly pinned by the upper half of his body under a container that fell over. He was taken to the hospital but later died. The police are investigating the detailed circumstances at the time.",
                "literal": "男性在检查去除洋葱茎和叶的机械时，因听到异常声音而探身查看，结果上半身被倒下的集装箱夹住。男性被送往医院，但之后死亡。警察正在调查当时的详细情况。",
                "grammar": "「〜ことから」— 因为…。例：異音が聞こえたことから（因为听到了异常声音）。\n「〜たところ」— …结果（表示契机）。例：のぞき込んだところ（探身一看结果）。\n「〜ということです」— 据说…。例：挟まれたということです（据说被夹住了）。",
                "vocab": [
                    ["点検", "てんけん", "检查、检修"],
                    ["異音", "いおん", "异常声音"],
                    ["のぞき込む", "のぞきこむ", "探身往里看"],
                    ["上半身", "じょうはんしん", "上半身"],
                    ["挟まれる", "はさまれ", "被夹住"],
                    ["詳しい状況", "くわしいじょうきょう", "详细情况"]
                ]
            }
        ]
    },
    {
        "slug": "henoko-kousu-henkou-chusen",
        "title": "死亡した高校2年の生徒 辺野古コースの変更希望も抽選で外れる",
        "subtitle": "沖縄・辺野古沖の船転覆事故で亡くなった同志社国際高校2年の武石知華さんが、研修旅行前、辺野古で乗船するコースからの変更希望を出していたことが報告書で分かった。",
        "paras": [
            {
                "ja": "辺野古沖の船転覆事故で亡くなった同志社国際高校2年の武石知華さん（17）が、研修旅行の前に辺野古で乗船するコースからの変更希望を提出していたことが31日、第三者委員会の調査報告書で分かりました。辺野古コースは定員を超え、別コースへの変更希望者を担当教諭が募ったところ、複数の生徒が応じましたが、武石さんは抽選に外れて認められませんでした。",
                "en": "It was revealed on the 31st in the investigation report of a third-party committee that Tomoka Takeishi (17), a second-year student at Doshisha International High School who died in the boat capsizing accident off Henoko, had submitted a request to change from the course that boards the boat at Henoko before the school trip. The Henoko course exceeded its capacity, and although the teacher in charge recruited students wishing to switch to another course and several students applied, Takeishi lost the lottery and her request was not accepted.",
                "literal": "在边野古海面船只倾覆事故中身亡的同志社国际高中2年级学生武石知华（17岁），在研修旅行前提交了变更在边野古乘船路线的希望一事，于31日通过第三方委员会的调查报告书得以判明。边野古路线超过了定员，负责教师征集希望变更到其他路线的学生时，多名学生响应，但武石同学抽签落选而未被认可。",
                "grammar": "「〜ことが分かりました」— 判明…。例：提出していたことが分かりました（判明曾提交过）。\n「〜たところ」— …结果。例：募ったところ（征集的结果）。\n「〜に外れて」— 落选…。例：抽選に外れて（抽签落选）。",
                "vocab": [
                    ["転覆", "てんぷく", "倾覆、翻船"],
                    ["研修旅行", "けんしゅうりょこう", "修学旅行"],
                    ["第三者委員会", "だいさんしゃいいんかい", "第三方委员会"],
                    ["定員", "ていいん", "定员、名额"],
                    ["担当教諭", "たんとうきょうゆ", "负责教师"],
                    ["抽選", "ちゅうせん", "抽签"]
                ]
            },
            {
                "ja": "武石さんの両親は31日、「知華が一度、コース変更希望を出していたことや、抽選で外れて辺野古コースに残ることになったことを報告書で初めて知り、心の整理がまだできていません」とコメントしました。報告書によりますと、同校は昨年10月に希望コースの調査を実施。定員超過後、変更の申し出は締め切りまでにありませんでしたが、改めて募ったところ武石さんを含む複数の生徒が希望を提出。抽選で変更を認められたのは14人で、武石さんは外れたということです。",
                "en": "Takeishi's parents commented on the 31st, 'We learned for the first time from the report that Tomoka had once submitted a request to change courses and that she remained in the Henoko course after losing the lottery, and we have not yet been able to sort out our feelings.' According to the report, the school conducted a survey of preferred courses last October. After the capacity was exceeded, no students applied for a change by the deadline, but when the school again recruited volunteers, several students including Takeishi submitted requests. Fourteen students were approved through the lottery, and Takeishi was not selected.",
                "literal": "武石同学的父母31日发表评论：「知华曾提交过变更路线的希望，以及因抽签落选而留在边野古路线一事，我们通过报告书首次得知，心情还无法整理。」据报告书称，该校去年10月实施了希望路线的调查。超过定员后，到截止日期为止没有学生提出变更申请，但再次征集时包括武石同学在内的多名学生提交了希望。通过抽签被认可变更是14人，武石同学落选了。",
                "grammar": "「〜とコメントしました」— 发表评论说…。例：心の整理がまだできていませんとコメントしました（评论说心情还无法整理）。\n「〜によりますと」— 据…称。例：報告書によりますと（据报告书称）。\n「〜たところ」— …结果。例：改めて募ったところ（再次征集的结果）。",
                "vocab": [
                    ["両親", "りょうしん", "父母、双亲"],
                    ["報告書", "ほうこくしょ", "报告书"],
                    ["心の整理", "こころのせいり", "整理心情"],
                    ["申し出", "もうしで", "申请、申报"],
                    ["締め切り", "しめきり", "截止日期"],
                    ["認められる", "みとめられる", "被认可、被批准"]
                ]
            }
        ]
    },
    {
        "slug": "bado-shida-igarashi-kaisyou",
        "title": "バドミントン 志田千陽・五十嵐有紗ペアが解消 日本代表も辞退",
        "subtitle": "バドミントン女子ダブルスの「シダガシ」ペア、志田千陽選手と五十嵐有紗選手が31日、ペア解消を発表。2人は日本代表ナショナルチームも辞退した。",
        "paras": [
            {
                "ja": "バドミントン女子ダブルスの志田千陽選手が31日、自身のインスタグラムを更新し、五十嵐有紗選手と組んでいた「シダガシ」ペアの解消を発表しました。また同日、日本バドミントン協会は、2人の日本代表ナショナルチーム辞退の申し出を受け、これを受理したと発表しました。",
                "en": "Badminton women's doubles player Chiharu Shida updated her Instagram on the 31st and announced the dissolution of the 'Shidagashi' pair she had formed with Arisa Igarashi. On the same day, the Japan Badminton Association also announced that it had received and accepted the two players' requests to resign from the Japan national team.",
                "literal": "羽毛球女子双打的志田千阳选手31日更新了自己的Instagram，宣布了与五十岚有纱选手组队的「シダガシ」组合解散。另外同日，日本羽毛球协会宣布，已受理2人退出日本代表国家队的申请。",
                "grammar": "「〜を発表しました」— 发表了…。例：ペアの解消を発表しました（宣布了组合解散）。\n「〜を通じて」— 通过…。例：日本バドミントン協会を通じて（通过日本羽毛球协会）。\n「〜と発表しました」— 发表说…。例：受理したと発表しました（宣布已受理）。",
                "vocab": [
                    ["女子ダブルス", "じょしだぶるす", "女子双打"],
                    ["ペア解消", "ぺあかいしょう", "组合解散"],
                    ["日本代表", "にほんだいひょう", "日本国家队"],
                    ["辞退", "じたい", "辞退、退出"],
                    ["協会", "きょうかい", "协会"],
                    ["受理", "じゅり", "受理"]
                ]
            },
            {
                "ja": "発表によりますと「ペア結成以来、互いに理想とするプレースタイルを追求しながら、より良い形を模索してまいりました。その中で、競技に対する考え方や今後の方向性を踏まえ、ペアを解消するという決断に至りました」と理由を説明しています。志田選手は「シダマツ」ペアでオリンピック銅メダルを獲得。五十嵐選手は渡辺勇大選手との「ワタガシ」ペアで人気を集めた後、女子ダブルスに転向し、2人は2028年ロサンゼルス五輪を目指していました。",
                "en": "According to the announcement, the reason was explained as: 'Since the pair was formed, we have pursued our ideal playing styles and searched for a better form. In the process, based on our views on competition and future direction, we have reached the decision to dissolve the pair.' Shida won an Olympic bronze medal with the 'Shidamatsu' pair. Igarashi, after gaining popularity with the 'Watagashi' pair alongside Yuta Watanabe, switched to women's doubles, and the two had been aiming for the 2028 Los Angeles Olympics.",
                "literal": "据公布称，理由说明为：「自组合结成以来，在追求彼此理想的比赛风格的同时，摸索了更好的形式。在此过程中，基于对竞技的看法和今后的方向性，做出了解散组合的决定。」志田选手以「シダマツ」组合获得了奥运会铜牌。五十岚选手在与渡边勇大选手的「ワタガシ」组合中聚集人气后转向女子双打，2人曾以2028年洛杉矶奥运会为目标。",
                "grammar": "「〜によりますと」— 据…称。例：発表によりますと（据公布称）。\n「〜を踏まえ」— 基于…。例：方向性を踏まえ（基于方向性）。\n「〜に至りました」— 最终做出了…。例：決断に至りました（最终做出了决断）。",
                "vocab": [
                    ["結成", "けっせい", "结成、组建"],
                    ["追求", "ついきゅう", "追求"],
                    ["模索", "もさく", "摸索、探索"],
                    ["決断", "けつだん", "决断、决定"],
                    ["銅メダル", "どうめだる", "铜牌"],
                    ["転向", "てんこう", "转向、改行"]
                ]
            }
        ]
    },
    {
        "slug": "wagaya-sugiyama-nyuuin",
        "title": "お笑いトリオ「我が家」杉山裕之 ギラン・バレー症候群の疑いで入院",
        "subtitle": "お笑いトリオ「我が家」の杉山裕之さんが、免疫系の難病ギラン・バレー症候群の疑いで入院し、現在は一人での歩行が困難な状態。",
        "paras": [
            {
                "ja": "お笑いトリオ「我が家」の杉山裕之さんが、免疫系の難病として知られる「ギラン・バレー症候群」の疑いで入院していることが31日、分かりました。メンバーの坪倉由幸さんが自身のXで「数日前、手足が痺れると病院へ行き、診断していただいたところ、ギラン・バレー症候群の疑いがあるとして現在、入院し治療中です」と報告しました。",
                "en": "It was learned on the 31st that Hiroyuki Sugiyama of the comedy trio 'Wagaya' is hospitalized with suspected Guillain-Barré syndrome, a disease known as a rare immune system disorder. Fellow member Yoshiyuki Tsubokura reported on his X account, 'A few days ago, he went to the hospital because his hands and feet were numb. After examination, he is currently hospitalized and undergoing treatment for suspected Guillain-Barré syndrome.'",
                "literal": "搞笑三人组「我が家」的杉山裕之先生，因疑似被称为免疫系统疑难病症的「吉兰-巴雷综合征」而住院一事，于31日获悉。成员坪仓由幸先生在自己的X上报告：「数天前因手脚麻木去了医院，经诊断疑似吉兰-巴雷综合征，目前正在住院治疗。」",
                "grammar": "「〜として知られる」— 作为…为人所知。例：難病として知られる（作为疑难病症为人所知）。\n「〜ことが分かりました」— 判明…。例：入院していることが分かりました（判明正在住院）。\n「〜たところ」— …结果。例：診断していただいたところ（经诊断的结果）。",
                "vocab": [
                    ["お笑いトリオ", "おわらいとりお", "搞笑三人组"],
                    ["難病", "なんびょう", "疑难病症"],
                    ["疑い", "うたがい", "疑似、嫌疑"],
                    ["手足", "てあし", "手脚"],
                    ["痺れる", "しびれる", "麻木"],
                    ["診断", "しんだん", "诊断"]
                ]
            },
            {
                "ja": "坪倉さんは「現状、一人での歩行が困難な状況にあり、回復に向けてリハビリを行っています」と説明し、「憶測でヘンなこと言わないでくださいね」と呼びかけました。また、8月1日に出演予定だったフジテレビ系「爆笑レッドカーペット」について、杉山さんの体調不良により出演を見合わせると発表しました。ギラン・バレー症候群は、免疫のシステムが自身の末梢神経を攻撃することで起きる病気で、全身の力が入りづらくなります。",
                "en": "Tsubokura explained, 'Currently, he is in a condition where walking alone is difficult, and he is undergoing rehabilitation toward recovery,' and appealed, 'Please don't say strange things based on speculation.' He also announced that the trio would skip their scheduled appearance on Fuji TV's 'Bakusho Red Carpet' on August 1st due to Sugiyama's poor health. Guillain-Barré syndrome is a disease caused by the immune system attacking one's own peripheral nerves, making it difficult to put strength into the whole body.",
                "literal": "坪仓先生说明：「目前处于一个人步行困难的状态，正在为恢复进行康复训练」，并呼吁：「请不要基于臆测说奇怪的话。」另外，关于原定8月1日出演的富士电视台系「爆笑红毯」，因杉山先生身体状况不佳宣布暂缓出演。吉兰-巴雷综合征是因免疫系统攻击自身末梢神经而发生的疾病，全身会变得难以用力。",
                "grammar": "「〜状況にあり」— 处于…状态。例：困難な状況にあり（处于困难的状态）。\n「〜を見合わせる」— 暂缓…。例：出演を見合わせる（暂缓出演）。\n「〜ことで起きる」— 因…而发生。例：攻撃することで起きる（因攻击而发生）。",
                "vocab": [
                    ["歩行", "ほこう", "步行"],
                    ["リハビリ", "りはびり", "康复训练"],
                    ["憶測", "おくそく", "臆测"],
                    ["体調不良", "たいちょうふりょう", "身体状况不佳"],
                    ["末梢神経", "まっしょうしんけい", "末梢神经"],
                    ["攻撃", "こうげき", "攻击"]
                ]
            }
        ]
    }
]

# ==================================================================
# PROCESSING
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
