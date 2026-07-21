#!/usr/bin/env python3
"""Bunkanihongo Daily News Processing — July 22, 2026"""

import json, os, sys, re, subprocess, time
from sudachipy import tokenizer, dictionary

# === Setup Sudachi ===
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

def map_pos(pos_parts):
    if not pos_parts: return ''
    return {'名詞':'noun','動詞':'verb','助詞':'particle','形容詞':'adj','連体詞':'adj','副詞':'adverb','接続詞':'connector','接頭辞':'connector','接尾辞':'connector','助動詞':'grammar'}.get(pos_parts[0], '')

def tokenize_text(text):
    words = []
    for t in tok.tokenize(text, mode):
        p = t.part_of_speech()
        r = t.reading_form() or ''
        if r: r = kata_to_hira(r)
        words.append({
            's': t.dictionary_form() if t.dictionary_form() != '*' else t.surface(),
            'r': r if r and r != t.surface() else '',
            'p': map_pos(p)
        })
    return words

def gen_mp3(text, outpath):
    if os.path.exists(outpath) and os.path.getsize(outpath) > 1000:
        return True
    try:
        r = subprocess.run(['edge-tts', '--voice', 'ja-JP-NanamiNeural',
                            '--text', text, '--write-media', outpath],
                           capture_output=True, timeout=120)
        return os.path.exists(outpath) and os.path.getsize(outpath) > 1000
    except:
        return False

base_dir = '/home/horse/.openclaw/workspace/asanews'

# ============================================================
# ARTICLE DATA — July 22, 2026
# ============================================================
articles_data = [
    {
        "slug": "trump-wcup-zensetsu",
        "title": "W杯表彰式 トランプ氏の執着に批判殺到 FIFA会長が慌てて案内",
        "subtitle": "米国開催のW杯決勝でトランプ大統領が表彰台に居座り。FIFA会長が退去を促す一幕。",
        "paras": [
            {
                "ja": "アメリカ・ニュージャージー州で19日に行われたサッカーW杯決勝で、トランプ米大統領が表彰式に参加し、優勝したスペイン代表にトロフィーを授与した。しかし、トランプ氏が壇上に居続けたため、FIFAのインファンティーノ会長が退去を促す場面が見られた。",
                "en": "At the FIFA World Cup final held on the 19th in New Jersey, USA, US President Trump attended the awards ceremony and presented the trophy to the winning Spanish national team. However, because Trump remained on stage, FIFA President Infantino was seen urging him to leave.",
                "literal": "在美国新泽西州19日举行的足球世界杯决赛中，美国总统特朗普参加了表彰仪式，向获胜的西班牙代表队颁发了奖杯。但是，由于特朗普先生持续停留在台上，出现了FIFA的因凡蒂诺会长催促他离开的场面。",
                "grammar": "「〜で行われる」— 在…举行。例：州で行われた（在州举行）。\n「〜に参加し」— 参加…。例：表彰式に参加し（参加表彰仪式）。\n「〜ため」— 因为…。例：居続けたため（因为持续停留）。",
                "vocab": [
                    ["決勝", "けっしょう", "决赛"],
                    ["表彰式", "ひょうしょうしき", "颁奖仪式"],
                    ["大統領", "だいとうりょう", "总统"],
                    ["授与する", "じゅよする", "授予、颁发"],
                    ["壇上", "だんじょう", "讲台、台上"],
                    ["退去", "たいきょ", "离开、退场"]
                ]
            },
            {
                "ja": "会場からはトランプ氏に対して激しいブーイングが起こった。トランプ氏はトロフィーを渡した後も壇上の端にとどまり、選手たちとトロフィーセレモニーの写真に収まろうとした。SNSでは「空気が読めない」「降りろ」といった批判が殺到した。",
                "en": "Fierce booing erupted from the venue directed at Trump. Even after handing over the trophy, Trump remained at the edge of the stage, trying to get into the trophy ceremony photos with the players. On social media, criticism poured in with comments like 'can't read the room' and 'get off the stage.'",
                "literal": "会场上对特朗普先生发出了激烈的嘘声。特朗普先生交出奖杯后也停留在舞台边缘，试图与选手们一起出现在奖杯仪式的照片中。SNS上「不会察言观色」「下来吧」等批评蜂拥而至。",
                "grammar": "「〜に対して」— 对…。例：トランプ氏に対して（对特朗普）。\n「〜ようとした」— 试图做…。例：収まろうとした（试图进入画面）。\n「〜といった」— …之类的。例：批判が殺到した（批评蜂拥而至）。",
                "vocab": [
                    ["会場", "かいじょう", "会场"],
                    ["ブーイング", "ぶーいんぐ", "嘘声"],
                    ["セレモニー", "せれもにー", "仪式"],
                    ["空気を読む", "くうきをよむ", "察言观色"],
                    ["批判", "ひはん", "批评"],
                    ["殺到する", "さっとうする", "蜂拥而至"]
                ]
            },
            {
                "ja": "英紙ガーディアンは「トランプ氏に優勝チームの一員ではないことを丁寧に説明するインファンティーノ会長」とキャプションをつけた写真を掲載。ホワイトハウスは抗議するようにトランプ氏が写った写真を公開した。FIFAは公式SNSの写真からトランプ氏をカットして掲載し、物議を醸している。",
                "en": "The British newspaper The Guardian published a photo captioned 'Infantino politely explaining to Trump that he is not a member of the winning team.' The White House, as if in protest, released photos showing Trump. FIFA cut Trump from its official SNS photos, sparking controversy.",
                "literal": "英国《卫报》刊登了附有说明文字「向特朗普先生礼貌说明他不是获胜队伍一员的因凡蒂诺会长」的照片。白宫像是抗议般地公开了有特朗普先生的照片。FIFA从官方SNS的照片中去掉了特朗普先生，引发了争议。",
                "grammar": "「〜を掲載する」— 刊登…。例：写真を掲載した（刊登了照片）。\n「〜ように」— 像是…一样。例：抗議するように（像抗议一样）。\n「〜を醸す」— 引起、酝酿。例：物議を醸している（引起争议）。",
                "vocab": [
                    ["英紙", "えいし", "英国报纸"],
                    ["キャプション", "きゃぷしょん", "说明文字、字幕"],
                    ["掲載する", "けいさいする", "刊登"],
                    ["ホワイトハウス", "ほわいとはうす", "白宫"],
                    ["物議", "ぶつぎ", "争议"],
                    ["醸す", "かもす", "引起、酝酿"]
                ]
            }
        ]
    },
    {
        "slug": "chugoku-reearth-kenkin",
        "title": "中国で邦人2名拘束 レアアース巡る「人質外交」に懸念拡大",
        "subtitle": "富士電機社員が中国で逮捕。レアアース磁石の持ち出しが問題に。専門家は警告を発していた。",
        "paras": [
            {
                "ja": "中国当局が6月、東京に本社を置く富士電機グループの社員2名を逮捕したことが明らかになった。2名は規制対象となるレアアース磁石を日本へ持ち出そうとした容疑で拘束された。木原官房長官が定例会見で事実を認めている。",
                "en": "It has been revealed that Chinese authorities arrested two employees of the Fuji Electric Group, headquartered in Tokyo, in June. The two were detained on suspicion of attempting to take regulated rare earth magnets to Japan. Chief Cabinet Secretary Kihara confirmed the fact at a regular press conference.",
                "literal": "中国当局于6月逮捕了总部位于东京的富士电机集团的2名员工一事被曝光。2人因涉嫌试图将受管制的稀土磁石带出至日本而被拘留。木原官房长官在定期记者会上承认了事实。",
                "grammar": "「〜ことが明らかになった」— …已明确、被曝光。例：逮捕したことが明らかに（逮捕一事被曝光）。\n「〜ようとした」— 试图做…。例：持ち出そうとした（试图带出）。\n「〜容疑で」— 以…嫌疑。例：容疑で拘束された（以嫌疑被拘留）。",
                "vocab": [
                    ["当局", "とうきょく", "当局"],
                    ["逮捕する", "たいほする", "逮捕"],
                    ["社員", "しゃいん", "员工"],
                    ["レアアース", "れああーす", "稀土"],
                    ["磁石", "じしゃく", "磁铁"],
                    ["拘束する", "こうそくする", "拘留、拘束"]
                ]
            },
            {
                "ja": "今回の容疑で有罪となれば、5年以下の懲役が言い渡される可能性がある。特に軍民両用品に該当する場合はさらに重い刑罰となる。中国は米中関係の悪化を受けてレアアースの輸出規制を強化しており、日本の経済安全保障に深刻な影響を与える可能性が指摘されている。",
                "en": "If found guilty of this charge, there is a possibility of being sentenced to up to five years in prison. Especially if the items are deemed dual-use goods, the penalties could be even heavier. China has strengthened its export controls on rare earths amid worsening US-China relations, and experts point out this could have a serious impact on Japan's economic security.",
                "literal": "如果此次嫌疑被判有罪，可能被判处5年以下有期徒刑。特别是如果属于军民两用品，刑罚会更重。中国受美中关系恶化影响，加强了稀土出口管制，专家指出可能对日本的经济安全保障产生严重影响。",
                "grammar": "「〜となれば」— 如果变成…。例：有罪となれば（如果被判有罪）。\n「〜可能性がある」— 有可能…。例：可能性がある（有可能）。\n「〜を受けて」— 因为…、受…影响。例：悪化を受けて（受恶化影响）。",
                "vocab": [
                    ["有罪", "ゆうざい", "有罪"],
                    ["懲役", "ちょうえき", "徒刑"],
                    ["軍民両用品", "ぐんみんりょうようひん", "军民两用物品"],
                    ["輸出規制", "ゆしゅつきせい", "出口管制"],
                    ["強化する", "きょうかする", "强化"],
                    ["経済安全保障", "けいざいあんぜんほしょう", "经济安全保障"]
                ]
            },
            {
                "ja": "専門家は高市首相率いる官邸に対し、今年に入ってから繰り返し警告を発していた。中国は高性能磁石の材料である重希土の対日輸出を全面停止しており、日本の産業界への影響が懸念されている。政府は対応に乗り出していないと批判もある。",
                "en": "Experts had repeatedly issued warnings to the Prime Minister Takaichi's office since the beginning of this year. China has completely halted exports to Japan of heavy rare earths, which are materials for high-performance magnets, and there are concerns about the impact on Japanese industry. There is also criticism that the government has not yet taken action.",
                "literal": "专家对高市首相领导的官邸从今年开始反复发出了警告。中国全面停止了作为高性能磁铁材料的重稀土对日出口，对日本产业界的影响令人担忧。也存在批评称政府尚未着手应对。",
                "grammar": "「〜率いる」— 率领…。例：首相率いる官邸（首相率领的官邸）。\n「〜を発していた」— 发出了…。例：警告を発していた（发出了警告）。\n「〜への影響」— 对…的影响。例：産業界への影響（对产业界的影响）。",
                "vocab": [
                    ["専門家", "せんもんか", "专家"],
                    ["警告する", "けいこくする", "警告"],
                    ["重希土", "じゅうきど", "重稀土"],
                    ["全面停止", "ぜんめんていし", "全面停止"],
                    ["産業界", "さんぎょうかい", "产业界"],
                    ["懸念する", "けねんする", "担忧"]
                ]
            }
        ]
    },
    {
        "slug": "suisu-nihonjin-suibotsu",
        "title": "スイス・ベルンの川でSUP中 日本人男性が溺れて死亡",
        "subtitle": "観光で訪れていた日本人男性がSUP中に川に転落し死亡。スイス警察が捜査中。",
        "paras": [
            {
                "ja": "スイスの首都ベルンを流れるアーレ川で21日、スタンドアップパドルボード（SUP）をしていた日本人男性が溺れて死亡した。川の流れに飲み込まれた可能性があるとみられ、スイス警察が当時の詳しい状況を調べている。",
                "en": "On the 21st, a Japanese man who was stand-up paddleboarding (SUP) drowned in the Aare River flowing through Bern, the capital of Switzerland. He is believed to have been swallowed by the river current, and Swiss police are investigating the detailed circumstances.",
                "literal": "在流经瑞士首都伯尔尼的阿勒河上，21日一名正在玩站立式桨板（SUP）的日本男性溺亡。被认为可能被河水卷入，瑞士警方正在调查当时的具体情况。",
                "grammar": "「〜を流れる」— 流过…。例：川を流れる（流经的河流）。\n「〜とみられる」— 被认为是…。例：飲み込まれたとみられる（被认为被卷入）。\n「〜ている」— 正在…。例：調べている（正在调查）。",
                "vocab": [
                    ["首都", "しゅと", "首都"],
                    ["溺れる", "おぼれる", "溺水"],
                    ["死亡する", "しぼうする", "死亡"],
                    ["流れ", "ながれ", "水流"],
                    ["飲み込む", "のみこむ", "吞入、卷入"],
                    ["捜査する", "そうさする", "搜查、调查"]
                ]
            },
            {
                "ja": "SUPは近年、世界的に人気が高まっているウォータースポーツだ。しかし、川や海では予期せぬ流れや風でバランスを崩し、転落する事故が相次いでいる。現地のガイドブックには川の危険性についての注意喚起が掲載されているものの、観光客が十分に認識しないケースも多い。",
                "en": "SUP is a water sport that has been growing in popularity worldwide in recent years. However, accidents where people lose their balance due to unexpected currents or wind and fall off are occurring one after another in rivers and seas. Although local guidebooks include warnings about the dangers of the river, there are many cases where tourists do not fully recognize them.",
                "literal": "SUP是近年来全球人气增长的水上运动。但是，在河川和海上，因无法预料的流水和风而失去平衡、跌落的事故接连发生。当地的旅游指南上虽然刊登了关于河流危险性的提醒，但观光客没有充分认识的情况也很多。",
                "grammar": "「〜が高まる」— 高涨、提升。例：人気が高まっている（人气高涨）。\n「〜で」— 因…。例：流れで（因水流）。\n「〜ものの」— 虽然…但是。例：掲載されているものの（虽然刊登了）。",
                "vocab": [
                    ["ウォータースポーツ", "うぉーたーすぽーつ", "水上运动"],
                    ["予期せぬ", "よきせぬ", "无法预料的"],
                    ["バランス", "ばらんす", "平衡"],
                    ["転落する", "てんらくする", "跌落、坠落"],
                    ["ガイドブック", "がいどぶっく", "旅游指南"],
                    ["観光客", "かんこうきゃく", "观光客"]
                ]
            },
            {
                "ja": "外務省は海外でマリンスポーツを楽しむ際には、現地の天候や水流の情報を十分に確認し、安全装備を着用するよう呼びかけている。日本人観光客の事故は世界各地で報告されており、注意が必要だ。",
                "en": "The Ministry of Foreign Affairs is calling on people to thoroughly check local weather and water current information and wear safety equipment when enjoying marine sports overseas. Accidents involving Japanese tourists have been reported around the world, and caution is necessary.",
                "literal": "外务省呼吁在海外享受海上运动时，要充分确认当地的天气和水流信息，并穿戴安全装备。日本游客的事故在世界各地都有报告，需要引起注意。",
                "grammar": "「〜際」— 在…的时候。例：楽しむ際（在享受的时候）。\n「〜よう呼びかける」— 呼吁…。例：確認するよう呼びかけている（呼吁确认）。\n「〜ており」— 正在…。例：報告されており（正在被报告）。",
                "vocab": [
                    ["外務省", "がいむしょう", "外务省"],
                    ["マリンスポーツ", "まりんすぽーつ", "海上运动"],
                    ["天候", "てんこう", "天气、气候"],
                    ["安全装備", "あんぜんそうび", "安全装备"],
                    ["着用する", "ちゃくようする", "穿戴"],
                    ["呼びかける", "よびかける", "呼吁"]
                ]
            }
        ]
    },
    {
        "slug": "myze-hasan-model",
        "title": "ミュゼプラチナム破産 前受金依存の「自転車操業」が招いた末路",
        "subtitle": "会員430万人を抱えた脱毛サロン最大手が破産。前受金を先食いするビジネスモデルの崩壊。",
        "paras": [
            {
                "ja": "美容脱毛サロン最大手だったミュゼプラチナムが破産した。最盛期の会員数は430万人を超え、業界を席巻したが、その急成長の裏では前受金に依存した自転車操業が進んでいた。経営権は次々と売買され、「ミュゼ転がし」と呼ばれる異常事態に陥った。",
                "en": "Muse Platinum, once the largest beauty hair removal salon, has gone bankrupt. At its peak, membership exceeded 4.3 million people and it dominated the industry, but behind its rapid growth was a bootstrap operation dependent on advance payments. Management rights were bought and sold one after another, falling into an abnormal situation called 'Muse flipping.'",
                "literal": "曾是美容脱毛沙龙最大公司的Muse Platinum破产了。鼎盛时期会员数超过430万人，席卷了整个行业，但在其快速增长的背后，是依赖预收款的自转车经营。经营权被相继买卖，陷入了被称为「Muse转手」的异常事态。",
                "grammar": "「〜だった」— 曾是…。例：最大手だった（曾是最大企业）。\n「〜を超え」— 超过…。例：430万人を超え（超过430万人）。\n「〜裏では」— 在…背后。例：急成長の裏では（在快速增长的背后）。",
                "vocab": [
                    ["美容脱毛", "びようだつもう", "美容脱毛"],
                    ["最大手", "さいおおで", "最大企业"],
                    ["破産する", "はさんする", "破产"],
                    ["前受金", "まえうけきん", "预收款"],
                    ["自転車操業", "じてんしゃそうぎょう", "自转车经营"],
                    ["経営権", "けいえいけん", "经营权"]
                ]
            },
            {
                "ja": "ミュゼは複数回の施術を受けられる権利を30万円程度で一括販売する手法をとっていた。顧客から支払われた前受金を本来の会計処理とは別に、新規出店や広告費に流用。さらに解約金の支払いにも充てるなど、新規顧客から集めた金を次々と別の用途に回す悪循環に陥った。",
                "en": "Muse used a method of selling the right to receive multiple treatments in a lump sum for around 300,000 yen. The advance payments received from customers were diverted to new store openings and advertising costs, separate from proper accounting treatment. Furthermore, they used it to pay cancellation fees, falling into a vicious cycle of diverting money collected from new customers to other uses one after another.",
                "literal": "Muse采用了一种将可接受多次治疗的权利以30万日元左右一次性销售的手法。从顾客处收到的预收款被挪用于新开店和广告费，与正常的会计处理不同。此外，还用于支付解约金，陷入了将从新顾客处收集的资金接连转用于其他用途的恶性循环。",
                "grammar": "「〜程度で」— 以…左右的价格。例：30万円程度で（以30万日元左右）。\n「〜とは別に」— 与…不同。例：会計処理とは別に（与会计处理不同）。\n「〜に陥る」— 陷入…。例：悪循環に陥った（陷入恶性循环）。",
                "vocab": [
                    ["施術", "しじゅつ", "治疗、施术"],
                    ["一括販売", "いっかつはんばい", "一次性销售"],
                    ["流用する", "りゅうようする", "挪用"],
                    ["解約金", "かいやくきん", "解约金"],
                    ["悪循環", "あくじゅんかん", "恶性循环"],
                    ["充てる", "あてる", "充作、使用"]
                ]
            },
            {
                "ja": "前受金の適切な管理ができず、解約が急増したことで経営は急速に悪化。2015年8月期には約52億円の最終赤字に転落した。専門家は「売上高は大きいが、実態は借金を繰り返す自転車操業だった」と指摘する。消費者保護の観点から、前受金型ビジネスの規制見直しが求められている。",
                "en": "Unable to properly manage advance payments and with cancellations rapidly increasing, management deteriorated quickly. In the fiscal year ending August 2015, it fell into a final deficit of approximately 5.2 billion yen. Experts point out that 'although revenue was large, the reality was a bootstrap operation repeating debt.' From a consumer protection perspective, a review of regulations for advance payment-type businesses is being called for.",
                "literal": "未能适当管理预收款，解约骤增导致经营急速恶化。2015年8月期陷入了约52亿日元的最终赤字。专家指出「销售额虽然很大，但实态是重复借款的自转车经营」。从消费者保护的角度来看，要求重新审视预收款型业务的监管。",
                "grammar": "「〜できず」— 不能…。例：管理できず（不能管理）。\n「〜ことで」— 因为…。例：急増したことで（因为骤增）。\n「〜観点から」— 从…观点来看。例：消費者保護の観点から（从消费者保护的观点）。",
                "vocab": [
                    ["急速に", "きゅうそくに", "急速地"],
                    ["最終赤字", "さいしゅうあかじ", "最终赤字"],
                    ["転落する", "てんらくする", "跌落、陷入"],
                    ["実態", "じったい", "实态、实际情况"],
                    ["借金", "しゃっきん", "借款、债务"],
                    ["規制見直し", "きせいみなおし", "重新审视监管"]
                ]
            }
        ]
    },
    {
        "slug": "zara-shi-no-pantsu",
        "title": "ZARA「死のパンツ」に注意 ワイドパンツで転倒・骨折が相次ぐ",
        "subtitle": "海外SNSでZARAのワイドパンツによる転倒事故が続出。大手メディアも警鐘。",
        "paras": [
            {
                "ja": "ファストファッションブランド「ZARA」のあるワイドパンツを着用したところ、転倒して怪我をしたとの報告が海外のSNSで相次いでいる。中には骨折などの大怪我につながった人もおり、「ZARAの死のパンツ」と呼ばれ、注意を呼びかける動きが広がっている。",
                "en": "Reports of people falling and getting injured after wearing a certain pair of wide-leg pants from the fast fashion brand 'ZARA' are emerging one after another on overseas social media. Some have suffered major injuries including fractures, and the pants are being called 'ZARA's death pants,' with calls for caution spreading.",
                "literal": "穿着快时尚品牌「ZARA」的某款阔腿裤后摔倒受伤的报告在海外SNS上接连出现。其中也有人导致骨折等重伤，被称为「ZARA的死亡裤」，呼吁注意的动向正在扩大。",
                "grammar": "「〜ところ」— 刚…的时候。例：着用したところ（穿着后）。\n「〜との報告」— …的报告。例：怪我をしたとの報告（受伤的报告）。\n「〜ており」— 正在…。例：相次いでおり（接连出现）。",
                "vocab": [
                    ["ファストファッション", "ふぁすとふぁっしょん", "快时尚"],
                    ["着用する", "ちゃくようする", "穿着"],
                    ["転倒する", "てんとうする", "摔倒"],
                    ["怪我", "けが", "受伤"],
                    ["骨折", "こっせつ", "骨折"],
                    ["呼びかける", "よびかける", "呼吁"]
                ]
            },
            {
                "ja": "問題の商品は「FLOWY WIDE LEG PANTS」と呼ばれ、地面まで届くロング丈と裾が大きく広がったデザインが特徴だ。インフルエンサーが転倒する様子をTikTokに投稿したことをきっかけに問題が表面化した。アメリカのCNNやイギリスのガーディアンなど大手メディアも報じている。",
                "en": "The product in question is called 'FLOWY WIDE LEG PANTS,' characterized by its floor-length cut and wide-flared hem. The problem came to light when an influencer posted a video on TikTok of herself falling down. Major media outlets including CNN in the US and The Guardian in the UK have also reported on it.",
                "literal": "问题商品被称为「FLOWY WIDE LEG PANTS」，特点是触及地面的长版和大幅展开的裤脚。以一名网红将在TikTok上投稿摔倒的样子的契机，问题表面化了。美国的CNN和英国的《卫报》等主要媒体也进行了报道。",
                "grammar": "「〜と呼ばれる」— 被称为…。例：問題の商品と呼ばれる（被称为问题商品）。\n「〜が特徴だ」— 以…为特征。例：デザインが特徴だ（设计为特征）。\n「〜をきっかけに」— 以…为契机。例：投稿したことをきっかけに（以投稿为契机）。",
                "vocab": [
                    ["商品", "しょうひん", "商品"],
                    ["ロング丈", "ろんぐたけ", "长款"],
                    ["裾", "すそ", "下摆、裤脚"],
                    ["デザイン", "でざいん", "设计"],
                    ["インフルエンサー", "いんふるえんさー", "网红、影响者"],
                    ["表面化する", "ひょうめんかする", "表面化"]
                ]
            },
            {
                "ja": "ファッション関係者は、素材や丈の長さ、裾の広さによっては、自転車のチェーンやエスカレーターに引っかかる危険性があると指摘する。夏に人気のワイドパンツだが、歩行時には足元に注意が必要だ。ZARAは現時点でコメントを出していない。",
                "en": "Fashion experts point out that depending on the material, length, and width of the hem, there is a risk of getting caught in bicycle chains or escalators. Although wide-leg pants are popular in summer, caution is needed when walking. ZARA has not issued a comment at this point.",
                "literal": "时尚相关人士指出，根据材质、长度和裤脚宽度，存在被自行车链条或自动扶梯挂住的风险。虽然是夏季流行的阔腿裤，但步行时需要注意脚下。ZARA目前尚未发表评论。",
                "grammar": "「〜によっては」— 根据…不同、有的…。例：裾の広さによっては（根据裤脚宽度）。\n「〜危険性がある」— 有…的危险。例：引っかかる危険性（被挂住的危险）。\n「〜が」— 虽然…但是。例：ワイドパンツだが（虽然是阔腿裤）。",
                "vocab": [
                    ["素材", "そざい", "材质"],
                    ["チェーン", "ちぇーん", "链条"],
                    ["エスカレーター", "えすかれーたー", "自动扶梯"],
                    ["引っかかる", "ひっかかる", "挂住、卡住"],
                    ["足元", "あしもと", "脚下"],
                    ["コメント", "こめんと", "评论"]
                ]
            }
        ]
    }
]

# ============================================================
# PROCESS ALL ARTICLES
# ============================================================

def process_article(art):
    slug = art['slug']
    print(f"\n{'='*60}")
    print(f"Processing: {art['title']}")
    print(f"Slug: {slug}")

    # 1. Build JSON
    reading_data = [{
        "id": slug,
        "title": art['title'],
        "subtitle": art.get('subtitle', ''),
        "level": "中級",
        "length": len(art['paras']),
        "date": "2026-07-22",
        "paragraphs": []
    }]

    for i, p in enumerate(art['paras']):
        print(f"  Tokenizing P{i+1}...")
        words = tokenize_text(p['ja'])
        reading_data[0]['paragraphs'].append({
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
    os.makedirs(f'{base_dir}/assets/readings', exist_ok=True)
    with open(f'{base_dir}/assets/readings/{slug}.json', 'w', encoding='utf-8') as f:
        json.dump(reading_data, f, ensure_ascii=False, indent=2)
    print(f"  ✅ JSON saved")

    # 3. Generate MP3s
    os.makedirs(f'{base_dir}/assets/audio/{slug}', exist_ok=True)
    for i, p in enumerate(art['paras']):
        outpath = f'{base_dir}/assets/audio/{slug}/p{i+1}.mp3'
        if gen_mp3(p['ja'], outpath):
            size = os.path.getsize(outpath)
            print(f"  ✅ MP3 P{i+1} ({size//1024}KB)")
        else:
            print(f"  ❌ MP3 P{i+1} FAILED")

    # 4. Create blog post
    paras_ja = '\n\n'.join([p['ja'] for p in art['paras']])
    post = f"""---
title: {art['title']}
date: 2026-07-22 11:30:00 +0900
categories: [ニュース]
tags: [ニュース]
---

{paras_ja}

<div class="mt-4 p-3" style="background:#f0f4f8;border-radius:8px;text-align:center;">
  <a href="/asanews/reading-room/?read={slug}" class="btn btn-danger" style="color:#fff;padding:10px 24px;border-radius:6px;font-weight:bold;">
    📖 読解ルームで詳しく読む
  </a>
</div>
"""
    os.makedirs(f'{base_dir}/_posts', exist_ok=True)
    with open(f'{base_dir}/_posts/2026-07-22-{slug}.md', 'w', encoding='utf-8') as f:
        f.write(post)
    print(f"  ✅ Blog post created")

    return slug

# Process all articles
processed = []
for art in articles_data:
    slug = process_article(art)
    processed.append(slug)

# ============================================================
# 5. Update index.json
# ============================================================
# Read existing index
index_path = f'{base_dir}/assets/readings/index.json'
existing_index = []
if os.path.exists(index_path):
    try:
        with open(index_path, 'r') as f:
            existing_index = json.load(f)
    except:
        pass

# Get existing IDs to avoid duplicates
existing_ids = {item['id'] for item in existing_index}

# Add new articles at the beginning
new_items = []
for art in articles_data:
    if art['slug'] not in existing_ids:
        new_items.append({
            "id": art['slug'],
            "title": art['title'],
            "level": "中級",
            "length": len(art['paras']),
            "date": "2026-07-22",
            "file": f"assets/readings/{art['slug']}.json"
        })

# Merge: new first, then existing (keeping kiken-unten-kijun at its position)
index = new_items + existing_index

with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)
print(f"\n✅ index.json updated with {len(index)} articles (added {len(new_items)} new)")

# ============================================================
# 6. Update READING_LIST in reading-room.js
# ============================================================
js_path = f'{base_dir}/assets/js/reading-room.js'
with open(js_path, 'r') as f:
    js = f.read()

js_list = []
for item in index:
    js_list.append(f"    {{\n      id: '{item['id']}',\n      title: '{item['title']}',\n      kicker: '{item['level']}',\n      desc: '',\n      badge: '{item['length']}段落',\n      file: '/asanews/assets/readings/{item['id']}.json'\n    }}")

js_replace = "  const READING_LIST = [\n" + ",\n".join(js_list) + "\n  ];"

js_new = re.sub(
    r'const READING_LIST = \[.*?\];',
    js_replace,
    js,
    flags=re.DOTALL
)

with open(js_path, 'w') as f:
    f.write(js_new)

print(f"✅ reading-room.js READING_LIST updated ({len(index)} articles)")

# ============================================================
# 7. Verify
# ============================================================
print(f"\n{'='*60}")
print("Verification:")
for slug in processed:
    j = f'{base_dir}/assets/readings/{slug}.json'
    if os.path.exists(j):
        with open(j) as f:
            d = json.load(f)
        pc = len(d[0]['paragraphs'])
        print(f"  📄 {slug:30s} | {pc} paragraphs")
        # Check audio files
        for pi in range(pc):
            ap = f'{base_dir}/assets/audio/{slug}/p{pi+1}.mp3'
            if os.path.exists(ap):
                print(f"     🎵 p{pi+1}.mp3 ({os.path.getsize(ap)//1024}KB)")
            else:
                print(f"     ❌ p{pi+1}.mp3 MISSING!")
    else:
        print(f"  ❌ {slug} MISSING!")

print(f"\n{'='*60}")
print(f"🎉 ALL DONE! Processed {len(processed)} articles")
print(f"{'='*60}")
