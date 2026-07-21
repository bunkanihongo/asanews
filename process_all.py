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
    with open('/tmp/tts_input.txt', 'w') as f:
        f.write(text)
    r = subprocess.run(['edge-tts', '--voice', 'ja-JP-NanamiNeural', 
                        '--text', text, '--write-media', outpath],
                       capture_output=True, timeout=120)
    return os.path.exists(outpath) and os.path.getsize(outpath) > 1000

##########################
# ARTICLE DATA
##########################

articles_data = [
    {
        "slug": "eu-chuukei-tsuuhan",
        "title": "EU 中国系ネット通販「アリエク」に制裁金 過去最高1022億円",
        "subtitle": "EUが中国系通販サイトに巨額制裁金。デジタルサービス法違反では過去最大。",
        "paras": [
            {
                "ja": "欧州連合（EU）の行政を担う欧州委員会は20日、中国のアリババ集団が運営する海外向けネット通販「アリエクスプレス」に対し、デジタルサービス法（DSA）違反では過去最高の5億5千万ユーロ（約1022億円）の制裁金を科したと発表した。",
                "en": "The European Commission, which handles the administration of the European Union (EU), announced on the 20th that it has imposed a fine of 550 million euros (approximately 102.2 billion yen) on AliExpress, the overseas e-commerce platform operated by China's Alibaba Group — the highest penalty ever for violating the Digital Services Act (DSA).",
                "literal": "承担EU行政的欧洲委员会20日宣布，对中国的阿里巴巴集团运营的海外网络购物平台「AliExpress」，处以了数字服务法（DSA）违反史上最高的5亿5千万欧元（约1022亿日元）的制裁金。",
                "grammar": "「〜を担う」— 负责…、承担…。例：行政を担う（承担行政事务）。\n「〜に対し」— 对…。例：企業に対し制裁金（对企业处以制裁金）。\n「〜では過去最高」— 在…方面为历史最高。",
                "vocab": [["欧州連合", "おうしゅうれんごう", "欧盟"], ["制裁金", "さいばいさん", "罚款、制裁金"], ["デジタルサービス法", "でじたるさーびすほう", "数字服务法"], ["運営する", "うんえいする", "运营"], ["科す", "かす", "处以、施加"]]
            },
            {
                "ja": "欧州委員会は10月20日までに改善計画を出すように求めた。EUは違法な商品の流通を防ぐ対策が不十分だと判断した。アリエクスプレスは中国系ネット通販として欧州市場で広く利用されている。",
                "en": "The European Commission has requested that an improvement plan be submitted by October 20th. The EU determined that measures to prevent the distribution of illegal products were insufficient. AliExpress is widely used in the European market as a Chinese e-commerce platform.",
                "literal": "欧洲委员会要求10月20日之前提交改善计划。EU判断防止违法商品流通的对策不充分。AliExpress作为中国系网络购物在欧美市场被广泛使用。",
                "grammar": "「〜までに」— 在…之前。例：10月までに（在10月之前）。\n「〜と判断した」— 判断为…。例：不十分だと判断した（判断为不充分）。\n「〜として」— 作为…。例：通販として（作为网购平台）。",
                "vocab": [["改善計画", "かいぜんけいかく", "改善计划"], ["違法", "いほう", "违法"], ["流通", "りゅうつう", "流通"], ["不十分", "ふじゅうぶん", "不充分"], ["判断する", "はんだんする", "判断"]]
            },
            {
                "ja": "EUのデジタルサービス法は、大規模なプラットフォームに対して違法コンテンツや商品の拡散防止を義務付ける規制法だ。欧州委はこれまでもX（旧ツイッター）やTikTokなどに対する調査を進めている。",
                "en": "The EU's Digital Services Act is a regulatory law that obligates large platforms to prevent the spread of illegal content and products. The European Commission has also been conducting investigations into X (formerly Twitter), TikTok, and others.",
                "literal": "EU的数字服务法是对大规模平台义务防止违法内容和商品扩散的规制法。欧洲委员会至今也在推进对X（原Twitter）和TikTok等的调查。",
                "grammar": "「〜に対して」— 对…。例：プラットフォームに対して（对平台）。\n「〜を義務付ける」— 义务化、有义务…。例：防止を義務付ける（有义务防止）。\n「〜ても」— 即使…也…。例：これまでも（至今也…）。",
                "vocab": [["大規模", "だいきぼ", "大规模"], ["プラットフォーム", "ぷらっとふぉーむ", "平台"], ["違法コンテンツ", "いほうこんてんつ", "违法内容"], ["拡散防止", "かくさんぼうし", "防止扩散"], ["義務付ける", "ぎむづける", "有义务、强制"]]
            }
        ]
    },
    {
        "slug": "kogekibi-kousho",
        "title": "どこまで暑くなる 関東・東海で初の「酷暑日」か 危険な暑さ",
        "subtitle": "今年初めて40℃超えの「酷暑日」が関東・東海で予想。熱中症に厳重警戒。",
        "paras": [
            {
                "ja": "全国的に午前中から気温が高くなっていますが、午後は東日本の内陸を中心に一段と暑さが際立ってきそうです。体温超えの高温範囲が広がるため、きょうは予定を変更してでも危険な暑さを避ける行動が必要です。",
                "en": "Temperatures have been high nationwide since the morning, and in the afternoon the heat is expected to become even more pronounced, especially in inland areas of eastern Japan. Since the area of above-body-temperature heat is expanding, today it's necessary to take action to avoid dangerous heat, even if it means changing your plans.",
                "literal": "全国从上午开始气温就在升高，下午以东日本内陆为中心暑气将进一步突出。超过体温的高温范围扩大，今天即使改变计划也需要采取避免危险高温的行动。",
                "grammar": "「〜を中心に」— 以…为中心。例：東日本を中心に（以东日本为中心）。\n「〜てきそうです」— 看起来要…。例：際立ってきそうです（看起来会更加突出）。\n「〜でも」— 即使…也。例：予定を変更してでも（即使改变计划也）。",
                "vocab": [["気温", "きおん", "气温"], ["東日本", "ひがしにほん", "东日本"], ["内陸", "ないりく", "内陆"], ["際立つ", "きわだつ", "突出、显著"], ["高温", "こうおん", "高温"], ["危険な暑さ", "きけんなあつさ", "危险高温"]]
            },
            {
                "ja": "とくに高温となる地域は、今夜遅くにかけて雷雨の可能性が高くなるため、暑さとあわせて天気の急変にも注意してください。気象庁は日最高気温が40度以上の日を「酷暑日」と命名しています。",
                "en": "In areas expected to reach especially high temperatures, there is a high possibility of thunderstorms toward late tonight, so please also be cautious of sudden weather changes in addition to the heat. The Japan Meteorological Agency has named days with a maximum temperature of 40°C or higher 'Extreme Heat Days.'",
                "literal": "特别是高温地区，到今天深夜为止雷雨可能性变高，请注意暑热的同时也注意天气骤变。气象厅将日最高气温40度以上的日子命名为「酷暑日」。",
                "grammar": "「〜にかけて」— 到…为止（时间范围）。例：今夜遅くにかけて（到今天深夜）。\n「〜とあわせて」— 与…一起。例：暑さとあわせて（与暑热一起）。\n「〜と命名する」— 命名为…。",
                "vocab": [["雷雨", "らいう", "雷雨"], ["天気の急変", "てんきのきゅうへん", "天气骤变"], ["気象庁", "きしょうちょう", "气象厅"], ["最高気温", "さいこうきおん", "最高气温"], ["酷暑日", "こくしょび", "酷暑日、极热天"], ["命名する", "めいめいする", "命名"]]
            },
            {
                "ja": "この危険な暑さは、東海など地域によっては週末にかけても続く予想です。こまめな水分補給や涼しい場所での休憩など、熱中症対策を徹底してください。",
                "en": "This dangerous heat is expected to continue through the weekend in some regions such as Tokai. Please thoroughly implement heatstroke prevention measures such as frequent hydration and resting in cool places.",
                "literal": "这个危险高温，在东海等地区预计将持续到周末。请彻底实施补充水分和凉快地方休息等中暑对策。",
                "grammar": "「〜によっては」— 根据情况、有的…。例：地域によっては（根据地区不同）。\n「〜にかけても」— 到…为止。例：週末にかけても（到周末为止）。\n「〜を徹底する」— 彻底实施。",
                "vocab": [["東海", "とうかい", "东海地区"], ["週末", "しゅうまつ", "周末"], ["こまめな", "こまめな", "勤快的、频繁的"], ["水分補給", "すいぶんほきゅう", "补充水分"], ["熱中症", "ねっちゅうしょう", "中暑"], ["徹底する", "てっていする", "彻底实施"]]
            }
        ]
    },
    {
        "slug": "beihei-iran-keikoku",
        "title": "トランプ氏 米兵死亡でイランに「報い」警告 仲介国は停戦模索",
        "subtitle": "米兵3人死亡を受け、米軍がイラン標的を攻撃。仲介国が新たな停戦案を提示。",
        "paras": [
            {
                "ja": "トランプ米大統領は、過去数日で米兵3人が死亡したことを受け、イランは「報いを受けることになる」と警告した。その後、米軍はイランの標的を攻撃した。",
                "en": "U.S. President Trump warned that Iran 'will face consequences' following the deaths of three U.S. soldiers in recent days. Subsequently, the U.S. military attacked targets in Iran.",
                "literal": "美国总统特朗普，对于过去数日3名美军士兵死亡一事，警告伊朗「将受到报应」。之后，美军攻击了伊朗的目标。",
                "grammar": "「〜を受け」— 鉴于…、基于…。例：死亡したことを受け（鉴于死亡一事）。\n「〜ことになる」— 将会…。例：受けることになる（将会受到）。\n「〜を攻撃した」— 攻击了…。",
                "vocab": [["大統領", "だいとうりょう", "总统"], ["米兵", "べいへい", "美军士兵"], ["報い", "むくい", "报应、报复"], ["警告する", "けいこくする", "警告"], ["標的", "ひょうてき", "目标"], ["攻撃する", "こうげきする", "攻击"]]
            },
            {
                "ja": "一方、中東で戦闘がさらに拡大する中、仲介国は新たな停戦案を提示した。トランプ氏はイランに対し「米兵殺害ならイランが代償を払う」と強調している。",
                "en": "Meanwhile, as fighting in the Middle East expands further, mediating countries have presented a new ceasefire proposal. Trump has emphasized to Iran that 'if U.S. soldiers are killed, Iran will pay the price.'",
                "literal": "另一方面，在中东战斗进一步扩大的情况下，仲介国提出了新的停战方案。特朗普对伊朗强调「如果杀害美军士兵，伊朗将付出代价」。",
                "grammar": "「〜中」— 在…之中。例：拡大する中（在扩大之中）。\n「〜に対し」— 对…。例：イランに対し（对伊朗）。\n「〜なら」— 如果…的话。例：殺害なら（如果是杀害）。",
                "vocab": [["中東", "ちゅうとう", "中东"], ["戦闘", "せんとう", "战斗"], ["拡大する", "かくだいする", "扩大"], ["仲介国", "ちゅうかいこく", "仲介国"], ["停戦案", "ていせんあん", "停战方案"], ["代償", "だいしょう", "代价"]]
            },
            {
                "ja": "仲介国は10日間の停戦を提案しているとみられる。米軍はイラン攻撃を続けており、9日連続で攻撃を行っている。地域の緊張はさらに高まっている。",
                "en": "The mediating countries are believed to have proposed a 10-day ceasefire. The U.S. military continues its attacks on Iran, carrying out operations for the 9th consecutive day. Regional tensions are further escalating.",
                "literal": "仲介国被认为提议了10天的停战。美军持续攻击伊朗，已经连续9天进行攻击。地区的紧张进一步升高。",
                "grammar": "「〜とみられる」— 被认为…。例：提案しているとみられる（被认为在提案）。\n「〜ており」— 持续…（连接形式）。例：攻撃を続けており（持续攻击）。\n「〜連続で」— 连续…。例：9日連続（连续9天）。",
                "vocab": [["提案する", "ていあんする", "提案"], ["連続", "れんぞく", "连续"], ["地域", "ちいき", "地区、区域"], ["緊張", "きんちょう", "紧张"], ["高まる", "たかまる", "升高、加剧"]]
            }
        ]
    },
    {
        "slug": "gmo-saitaku-kinmu-shazai",
        "title": "GMO熊谷氏 在宅勤務「完全廃止」投稿を謝罪 真意を説明",
        "subtitle": "GMOインターネットグループ代表が在宅勤務廃止発言を謝罪。「表現の過剰性で誤解を生んだ」。",
        "paras": [
            {
                "ja": "GMOインターネットグループの熊谷正寿代表は7月21日、在宅勤務の「完全廃止」を公表した一連の投稿について、「『表現の過剰性』で誤解を生み、お騒がせした」とXで謝罪した。",
                "en": "Masatoshi Kumagai, representative of the GMO Internet Group, apologized on X (formerly Twitter) on July 21st regarding a series of posts announcing the 'complete abolition' of remote work, stating that 'excessive expression caused misunderstandings and caused a stir.'",
                "literal": "GMO互联网集团的熊谷正寿代表于7月21日，对于公布在家办公「完全废止」的一系列投稿，在X上道歉说「因『表达的过度性』产生了误解，给大家添了麻烦」。",
                "grammar": "「〜について」— 关于…。例：投稿について（关于投稿）。\n「〜を生み」— 产生…。例：誤解を生み（产生误解）。\n「〜する」— 做…。例：謝罪した（道歉了）。",
                "vocab": [["在宅勤務", "ざいたくきんむ", "在家办公"], ["完全廃止", "かんぜんはいし", "完全废止"], ["投稿", "とうこう", "投稿"], ["謝罪する", "しゃざいする", "道歉"], ["過剰性", "かじょうせい", "过度性"], ["誤解", "ごかい", "误解"]]
            },
            {
                "ja": "熊谷氏は在宅勤務という働き方そのものを否定するものではなく、見直したのは「グループとして在宅勤務を推奨する」という基本方針だと説明。真意は「AI時代におけるオフィスの価値再定義」だと述べた。",
                "en": "Kumagai explained that he was not denying remote work itself as a working style, but rather that what was being reviewed was the basic policy of 'recommending remote work as a group.' He stated that his true intention was 'redefining the value of the office in the AI era.'",
                "literal": "熊谷氏说明并非否定在家办公这种工作方式本身，重新审视的是「作为集团推荐在家办公」这一基本方针。真意是「AI时代中办公室价值的重新定义」。",
                "grammar": "「〜ものではなく」— 并非…。例：否定するものではなく（并非否定）。\n「〜として」— 作为…。例：グループとして（作为集团）。\n「〜における」— 在…中的。例：AI時代における（在AI时代中的）。",
                "vocab": [["働き方", "はたらきかた", "工作方式"], ["否定する", "ひていする", "否定"], ["見直す", "みなおす", "重新审视"], ["基本方針", "きほんほうしん", "基本方针"], ["推奨する", "すいしょうする", "推荐"], ["再定義", "さいていぎ", "重新定义"]]
            },
            {
                "ja": "GMOは在宅勤務の「グループとしての推奨」見直しを巡り、従業員同士のコミュニケーション重視へと方針転換している。AI競争が激化する中、オフィスでの対面業務の重要性が再認識されている。",
                "en": "GMO has been shifting its policy regarding the review of 'recommending remote work as a group' toward emphasizing communication among employees. Amid intensifying AI competition, the importance of in-person office work is being re-recognized.",
                "literal": "GMO围绕「作为集团推荐在家办公」的重新审视，正在向重视员工间沟通的方向转变方针。在AI竞争激化之中，办公室面对面业务的重要性被重新认识。",
                "grammar": "「〜を巡り」— 围绕…。例：見直しを巡り（围绕重新审视）。\n「〜へと」— 向着…。例：重視へと（向着重视的方向）。\n「〜中」— 在…之中。例：激化する中（在激化之中）。",
                "vocab": [["従業員", "じゅうぎょういん", "员工"], ["コミュニケーション", "こみゅにけーしょん", "沟通"], ["方針転換", "ほうしんてんかん", "方针转变"], ["激化する", "げきかする", "激化"], ["対面", "たいめん", "面对面"], ["再認識する", "さいにんしきする", "重新认识"]]
            }
        ]
    },
    {
        "slug": "shuugiin-shisan-koukai",
        "title": "衆院議員の資産公開 平均3278万円 トップは7億円超",
        "subtitle": "今年2月の衆院選で当選した議員の資産が公開。平均は3278万円で前回より600万円増。",
        "paras": [
            {
                "ja": "今年2月の衆議院選挙で当選した議員の資産がきょう（21日）公開され、資産総額の平均は3278万円でした。過去最も少なかった前回より600万円あまり増えました。",
                "en": "The assets of lawmakers elected in February's House of Representatives election were released today (the 21st), with the average total assets being 32.78 million yen. This is an increase of over 6 million yen from the previous release, which was the lowest ever.",
                "literal": "今年2月众议院选举当选的议员的资产今天（21日）公开，资产总额平均为3278万日元。比过去最少的上次增加了600多万日元。",
                "grammar": "「〜で当選した」— 通过…当选的。例：選挙で当選した議員（通过选举当选的议员）。\n「〜より」— 比…。例：前回より（比上次）。\n「〜あまり」— 多、有余。例：600万円あまり（600多万日元）。",
                "vocab": [["衆議院", "しゅうぎいん", "众议院"], ["選挙", "せんきょ", "选举"], ["当選する", "とうせんする", "当选"], ["資産", "しさん", "资产"], ["公開する", "こうかいする", "公开"], ["平均", "へいきん", "平均"]]
            },
            {
                "ja": "資産が1億円を超えたのは27人で、前回より5人増えた。上位3人はいずれも自民党の議員で、トップは自民党の逢沢一郎氏で7億9044万円だった。高市総理の資産は1143万円で、全議員の平均を下回った。",
                "en": "There were 27 people with assets exceeding 100 million yen, up 5 from the previous time. The top three were all Liberal Democratic Party lawmakers, with the highest being LDP's Ichiro Aisawa at 790.44 million yen. Prime Minister Takaichi's assets were 11.43 million yen, below the average of all lawmakers.",
                "literal": "资产超过1亿日元的有27人，比上次增加了5人。上位3人全是自民党议员，第一是自民党的逢泽一郎氏7亿9044万日元。高市总理的资产为1143万日元，低于全体议员的平均水平。",
                "grammar": "「〜を超えた」— 超过…。例：1億円を超えた（超过1亿日元）。\n「〜いずれも」— 全都是。例：上位3人はいずれも（前3名全都是）。\n「〜を下回った」— 低于…。例：平均を下回った（低于平均）。",
                "vocab": [["1億円", "いちおくえん", "1亿日元"], ["上位", "じょうい", "上位"], ["自民党", "じみんとう", "自民党"], ["トップ", "とっぷ", "第一、首位"], ["下回る", "したまわる", "低于、未达到"]]
            },
            {
                "ja": "衆院議員の資産公開は年1回行われ、議員の透明性を確保するための重要な制度です。資産額には土地や建物、預貯金などが含まれ、株やゴルフ会員権なども対象となります。",
                "en": "The asset disclosure of House of Representatives members is conducted once a year and is an important system for ensuring transparency among lawmakers. The asset amount includes land, buildings, deposits, and savings, with stocks and golf memberships also subject to disclosure.",
                "literal": "众议院议员的资产公开每年进行一次，是确保议员透明性的重要制度。资产额包括土地、建筑物、存款等，股票和高尔夫会员权等也是对象。",
                "grammar": "「〜年1回」— 每年一次。例：年1回行われる（每年进行一次）。\n「〜ための」— 为了…的。例：確保するための（为了确保…的）。\n「〜が含まれる」— 包含…。例：土地や建物が含まれる（包含土地和建筑物）。",
                "vocab": [["透明性", "とうめいせい", "透明性"], ["確保する", "かくほする", "确保"], ["土地", "とち", "土地"], ["建物", "たてもの", "建筑物"], ["預貯金", "よちょきん", "存款"], ["対象", "たいしょう", "对象"]]
            }
        ]
    },
    {
        "slug": "ennchuu-kokkai-fukushuto",
        "title": "延長国会 実質審議3日間 「副首都」法案など4法案成立は綱渡り",
        "subtitle": "25日まで会期延長の今国会。審議できるのは実質3日間だけ。副首都法案の行方が焦点。",
        "paras": [
            {
                "ja": "政府・与党は25日まで会期を延長した今国会で「副首都構想」関連法案など4法案の成立に全力を挙げる構えだが、綱渡りの展開となる見通しだ。現状で法案審議を見込めるのは実質3日間しかない。",
                "en": "The government and ruling party are poised to go all out to pass four bills including those related to the 'sub-capital concept' in the current Diet session extended until the 25th, but it is expected to be a tightrope walk. Currently, only three days of substantive deliberation can be expected.",
                "literal": "政府·执政党在会期延长至25日的本届国会中，全力争取包括「副首都构想」相关法案在内的4个法案成立，但预计将是一场走钢丝般的展开。目前能期待法案审议的实质上只有3天。",
                "grammar": "「〜に全力を挙げる」— 尽全力…。例：成立に全力を挙げる（尽全力使其成立）。\n「〜構えだ」— 做好…准备、采取…姿态。例：挙げる構えだ（准备尽全力）。\n「〜しかない」— 只有…。例：3日間しかない（只有3天）。",
                "vocab": [["政府", "せいふ", "政府"], ["与党", "よとう", "执政党"], ["会期", "かいき", "会期"], ["延長する", "えんちょうする", "延长"], ["法案", "ほうあん", "法案"], ["綱渡り", "つなわたし", "走钢丝"]]
            },
            {
                "ja": "4法案は最後の平日となる24日の参院本会議での採決を想定する。副首都法案は少数与党の参院で可決できるかどうか予断を許さない状況で、成否が焦点となる。",
                "en": "The four bills are expected to be voted on in the House of Councillors plenary session on the 24th, the last weekday. Whether the sub-capital bill can be passed in the House of Councillors, where the ruling party is in the minority, remains uncertain, making its fate the focal point.",
                "literal": "4个法案预计在作为最后工作日的24日的参议院全体会议上进行表决。副首都法案能否在少数执政党的参议院通过，形势不容乐观，成败成为焦点。",
                "grammar": "「〜を想定する」— 设想、预计。例：採決を想定する（预计表决）。\n「〜かどうか」— 是否…。例：可決できるかどうか（是否能通过）。\n「〜予断を許さない」— 不容乐观、难以预测。",
                "vocab": [["採決", "さいけつ", "表决"], ["参院", "さんいん", "参议院"], ["本会議", "ほんかいぎ", "全体会议"], ["可決する", "かけつする", "通过（议案）"], ["予断", "よだん", "预断"], ["焦点", "しょうてん", "焦点"]]
            },
            {
                "ja": "野党側は猛抗議しており、与野党の攻防が激化している。会期延長を巡っては自民党幹部の外遊が中止となり、職場放棄だと野党から批判されている。",
                "en": "The opposition parties are fiercely protesting, and the ruling-opposition party battle is intensifying. Regarding the Diet session extension, senior LDP officials' overseas trips have been canceled, drawing criticism from the opposition who called it 'abandonment of their post.'",
                "literal": "在野党方面正在强烈抗议，执政党与在野党的攻防愈演愈烈。围绕会期延长，自民党干部的海外出行被取消，被在野党批评为「放弃职守」。",
                "grammar": "「〜ており」— 正在…。例：抗議しており（正在抗议）。\n「〜を巡って」— 围绕…。例：延長を巡って（围绕延长）。\n「〜と批判する」— 批评为…。例：職場放棄だと批判（批评为放弃职守）。",
                "vocab": [["野党", "やとう", "在野党"], ["猛抗議", "もうこうぎ", "强烈抗议"], ["与野党", "よやとう", "执政党与在野党"], ["攻防", "こうぼう", "攻防"], ["幹部", "かんぶ", "干部"], ["職場放棄", "しょくばほうき", "放弃职守"]]
            }
        ]
    },
    {
        "slug": "horumuzu-tanker-bakuhatsu",
        "title": "イラン ホルムズ海峡でタンカー2隻が爆発 航行不能に",
        "subtitle": "イラン革命防衛隊が石油タンカー2隻が爆発したと発表。米軍が関与と主張。",
        "paras": [
            {
                "ja": "イランのイスラム革命防衛隊は20日、石油タンカー2隻がホルムズ海峡南側の安全でないルートを通航しようとして爆発し、航行不能になったと発表した。",
                "en": "Iran's Islamic Revolutionary Guard Corps announced on the 20th that two oil tankers exploded and became disabled while attempting to navigate an unsafe route south of the Strait of Hormuz.",
                "literal": "伊朗的伊斯兰革命卫队20日宣布，2艘石油油轮在霍尔木兹海峡南侧试图通过不安全的航线时爆炸，无法航行。",
                "grammar": "「〜が…と発表した」— 发表了…。例：爆発したと発表した（发表了爆炸的消息）。\n「〜しようとして」— 试图做…时。例：通航しようとして（试图通过时）。",
                "vocab": [["革命防衛隊", "かくめいぼうえいたい", "革命卫队"], ["石油タンカー", "せきゆたんかー", "石油油轮"], ["ホルムズ海峡", "ほるむずかいきょう", "霍尔木兹海峡"], ["爆発する", "ばくはつする", "爆炸"], ["航行不能", "こうこうふのう", "无法航行"]]
            },
            {
                "ja": "２隻が米軍にこの航路を使うよう促されていたと主張した。ホルムズ海峡は世界の石油輸送の要所であり、この地域の緊張がエネルギー市場に影響を与える可能性がある。",
                "en": "It claimed that the two vessels had been urged by the U.S. military to use this route. The Strait of Hormuz is a chokepoint for global oil transportation, and tensions in this region could affect energy markets.",
                "literal": "主张2艘船被美军促使使用了这条航线。霍尔木兹海峡是世界石油运输的要道，该地区的紧张可能对能源市场产生影响。",
                "grammar": "「〜よう促す」— 促使…。例：使うよう促す（促使使用）。\n「〜と主張した」— 主张…。例：促されていたと主張（主张被促使）。\n「〜可能性がある」— 有可能…。例：影響を与える可能性（可能产生影响）。",
                "vocab": [["主張する", "しゅちょうする", "主张"], ["航路", "こうろ", "航线"], ["要所", "ようしょ", "要地、关键地点"], ["エネルギー市場", "えねるぎーしじょう", "能源市场"], ["影響", "えいきょう", "影响"]]
            },
            {
                "ja": "ホルムズ海峡情勢は日本への影響も懸念されており、日用品など物価の上昇やガソリン代の高騰が心配されている。中東の緊張は依然として続いている。",
                "en": "The situation in the Strait of Hormuz is also a concern regarding its impact on Japan, with worries about rising prices of daily goods and soaring gasoline costs. Tensions in the Middle East continue unabated.",
                "literal": "霍尔木兹海峡的形势对日本的影响也令人担忧，日用品等物价上涨和汽油费的高涨令人担心。中东的紧张仍然持续。",
                "grammar": "「〜が懸念される」— 令人担忧…。例：影響が懸念される（影响令人担忧）。\n「〜ており」— 正在…。例：懸念されており（正在被担忧）。",
                "vocab": [["情勢", "じょうせい", "形势"], ["懸念する", "けねんする", "担忧"], ["日用品", "にちようひん", "日用品"], ["物価", "ぶっか", "物价"], ["高騰", "こうとう", "高涨、飙升"], ["依然として", "いぜんとして", "仍然、依然"]]
            }
        ]
    },
    {
        "slug": "samsung-bei-kyouin-sakugen",
        "title": "韓国サムスン 米国本社移転で大規模な人員削減や配置転換",
        "subtitle": "サムスン電子が米国で大規模な人員削減を実施。ディスプレー・携帯電話部門が対象。",
        "paras": [
            {
                "ja": "韓国サムスン電子は、米国のディスプレー、携帯電話などの民生用電子機器の部門で大規模な人員削減を実施した。東部ニュージャージー州と南部テキサス州の従業員が主な対象となった。",
                "en": "Samsung Electronics of South Korea has implemented large-scale job cuts in its U.S. consumer electronics divisions, including displays and mobile phones. Employees in eastern New Jersey and southern Texas were the main targets.",
                "literal": "韩国三星电子在美国的显示器、手机等民生用电子设备部门实施了大规模人员削减。东部新泽西州和南部德克萨斯州的员工成为主要对象。",
                "grammar": "「〜を実施した」— 实施了…。例：削減を実施した（实施了削减）。\n「〜が対象となった」— 成为对象。例：従業員が対象（员工成为对象）。",
                "vocab": [["韓国", "かんこく", "韩国"], ["人員削減", "じんいんさくげん", "人员削减"], ["民生用", "みんせいよう", "民用"], ["電子機器", "でんしきき", "电子设备"], ["実施する", "じっしする", "实施"], ["対象", "たいしょう", "对象"]]
            },
            {
                "ja": "サムスンは米本社を移転し、組織再編を進めている。AIメモリー事業は好調で、2四半期連続で営業利益が89兆ウォン（約10兆円）を超えた。一方で不採算部門の整理を進めている。",
                "en": "Samsung is relocating its U.S. headquarters and proceeding with organizational restructuring. Its AI memory business is performing well, with operating profit exceeding 89 trillion won (about 10 trillion yen) for two consecutive quarters. Meanwhile, it is restructuring unprofitable divisions.",
                "literal": "三星正在迁移美国总部，推进组织重组。AI内存业务表现良好，连续2个季度营业利润超过89万亿韩元（约10万亿日元）。另一方面，正在推进亏损部门的整理。",
                "grammar": "「〜を移転し」— 迁移…。例：本社を移転し（迁移总部）。\n「〜連続で」— 连续…。例：2四半期連続（连续2个季度）。\n「〜一方で」— 另一方面。例：好調な一方で（一方面表现良好，另一方面）。",
                "vocab": [["本社", "ほんしゃ", "总部"], ["移転する", "いてんする", "迁移"], ["組織再編", "そしきさいへん", "组织重组"], ["好調", "こうちょう", "良好、势头好"], ["営業利益", "えいぎょうりえき", "营业利润"], ["不採算", "ふさいさん", "不盈利"]]
            },
            {
                "ja": "サムスンは最近、バークレイズと提携し米国でクレジットカード事業にも進出している。AI時代に向けた事業ポートフォリオの見直しが加速している。",
                "en": "Samsung recently partnered with Barclays to also enter the credit card business in the U.S. The review of its business portfolio toward the AI era is accelerating.",
                "literal": "三星最近与巴克莱银行合作，在美国也进军信用卡业务。面向AI时代的事业组合的重新审视正在加速。",
                "grammar": "「〜と提携し」— 与…合作。例：バークレイズと提携し（与巴克莱合作）。\n「〜に向けた」— 面向…的。例：AI時代に向けた（面向AI时代的）。",
                "vocab": [["提携する", "ていけいする", "合作"], ["クレジットカード", "くれじっとかーど", "信用卡"], ["進出する", "しんしゅつする", "进军、进入"], ["事業ポートフォリオ", "じぎょうぽーとふぉりお", "业务组合"], ["加速する", "かそくする", "加速"]]
            }
        ]
    },
    {
        "slug": "kokkai-ennchuu-gaiyuu-chuushi",
        "title": "国会延長で自民幹部の外遊中止 要人との会談機会失う",
        "subtitle": "国会会期延長を受け、自民党幹部らの海外渡航が相次いで中止に。野党からは「職場放棄」と批判。",
        "paras": [
            {
                "ja": "国会の会期延長を受け、自民党幹部らの海外渡航が相次いで中止となりました。中でもパプアニューギニアへの訪問については、「重要な外交機会だった」という指摘も出ています。",
                "en": "Following the extension of the Diet session, overseas trips by senior Liberal Democratic Party officials have been canceled one after another. In particular, the visit to Papua New Guinea has been noted as having been 'an important diplomatic opportunity.'",
                "literal": "受国会会期延长影响，自民党干部等的海外出行相继被取消。其中，关于对巴布亚新几内亚的访问，也出现了「是重要的外交机会」的指摘。",
                "grammar": "「〜を受け」— 基于…、因…。例：延長を受け（因延长）。\n「〜が相次ぐ」— 接连发生。例：中止となりました（相继被取消）。\n「〜という指摘」— …的指摘。例：という指摘も出ている（也出现了…的指摘）。",
                "vocab": [["海外渡航", "かいがいとこう", "海外出行"], ["相次ぐ", "あいつぐ", "接连发生"], ["中止", "ちゅうし", "取消、中止"], ["訪問", "ほうもん", "访问"], ["外交機会", "がいこうきかい", "外交机会"], ["指摘", "してき", "指摘、指出"]]
            },
            {
                "ja": "野党側は「職場放棄だ」と反発している。少数与党の国会運営を巡っては、与野党の攻防が激化しており、今後の政治日程に影響を与える可能性がある。",
                "en": "The opposition parties are pushing back, calling it 'abandonment of their post.' Regarding the management of the Diet with a minority ruling party, the battle between the ruling and opposition parties is intensifying, which could affect future political schedules.",
                "literal": "在野党方面反弹称「这是放弃职守」。围绕少数执政党的国会运营，执政党与在野党的攻防激化，有可能对今后的政治日程产生影响。",
                "grammar": "「〜だ」— 是…（断定）。例：職場放棄だ（是放弃职守）。\n「〜を巡って」— 围绕…。例：運営を巡って（围绕运营）。\n「〜可能性がある」— 有可能…。例：影響を与える可能性（可能产生影响）。",
                "vocab": [["反発する", "はんぱつする", "反对、反弹"], ["少数与党", "しょうすうよとう", "少数执政党"], ["国会運営", "こっかいうんえい", "国会运营"], ["政治日程", "せいじにってい", "政治日程"], ["影響を与える", "えいきょうをあたえる", "产生影响"]]
            }
        ]
    }
]

##########################
# PROCESS ALL ARTICLES
##########################

base_dir = '/home/horse/.openclaw/workspace/asanews'

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
        "date": "2026-07-21",
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
    post = f"""---
title: {art['title']}
date: 2026-07-21 11:30:00 +0900
categories: [ニュース]
tags: [ニュース]
---

{chr(10).join([p['ja'] for p in art['paras'][:3]])}

<div class="mt-4 p-3" style="background:#f0f4f8;border-radius:8px;text-align:center;">
  <a href="/asanews/reading-room/?read={slug}" class="btn btn-danger" style="color:#fff;padding:10px 24px;border-radius:6px;font-weight:bold;">
    📖 読解ルームで詳しく読む
  </a>
</div>
"""
    os.makedirs(f'{base_dir}/_posts', exist_ok=True)
    with open(f'{base_dir}/_posts/2026-07-21-{slug}.md', 'w', encoding='utf-8') as f:
        f.write(post)
    print(f"  ✅ Blog post created")
    
    return slug

# Process all articles
processed = []
for art in articles_data:
    slug = process_article(art)
    processed.append(slug)

# 5. Update index.json
index = []
for art in articles_data:
    index.append({
        "id": art['slug'],
        "title": art['title'],
        "level": "中級",
        "length": len(art['paras']),
        "date": "2026-07-21",
        "file": f"assets/readings/{art['slug']}.json"
    })

# Also include the first article (kiken-unten-kijun) if it exists
if os.path.exists(f'{base_dir}/assets/readings/kiken-unten-kijun.json'):
    with open(f'{base_dir}/assets/readings/kiken-unten-kijun.json', 'r') as f:
        kd = json.load(f)
    index.insert(0, {
        "id": "kiken-unten-kijun",
        "title": kd[0]['title'],
        "level": "中級",
        "length": kd[0]['length'],
        "date": "2026-07-21",
        "file": "assets/readings/kiken-unten-kijun.json"
    })

with open(f'{base_dir}/assets/readings/index.json', 'w', encoding='utf-8') as f:
    json.dump(index, f, ensure_ascii=False, indent=2)
print(f"\n✅ index.json updated with {len(index)} articles")

# 6. Update READING_LIST in reading-room.js
# Build the JS array
js_list = []
for item in index:
    js_list.append(f"    {{\n      id: '{item['id']}',\n      title: '{item['title']}',\n      kicker: '{item['level']}',\n      desc: '',\n      badge: '{item['length']}段落',\n      file: '/asanews/assets/readings/{item['id']}.json'\n    }}")

js_replace = "  const READING_LIST = [\n" + ",\n".join(js_list) + "\n  ];"

# Read current reading-room.js and replace READING_LIST
js_path = f'{base_dir}/assets/js/reading-room.js'
with open(js_path, 'r') as f:
    js = f.read()

import re
js_new = re.sub(
    r'const READING_LIST = \[.*?\];',
    js_replace,
    js,
    flags=re.DOTALL
)

with open(js_path, 'w') as f:
    f.write(js_new)

print(f"✅ reading-room.js READING_LIST updated ({len(index)} articles)")

# Verify
import os
for slug in processed + ['kiken-unten-kijun']:
    j = f'{base_dir}/assets/readings/{slug}.json'
    if os.path.exists(j):
        with open(j) as f:
            d = json.load(f)
        pc = len(d[0]['paragraphs'])
        print(f"  📄 {slug:30s} | {pc} paragraphs")
    else:
        print(f"  ❌ {slug} missing!")

print(f"\n{'='*60}")
print(f"🎉 ALL DONE! Processed {len(processed)} articles")
print(f"{'='*60}")
