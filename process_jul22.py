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
    r = subprocess.run(['edge-tts', '--voice', 'ja-JP-NanamiNeural', 
                        '--text', text, '--write-media', outpath],
                       capture_output=True, timeout=120)
    return os.path.exists(outpath) and os.path.getsize(outpath) > 1000

##########################
# ARTICLE DATA - July 22, 2026
##########################

articles_data = [
    {
        "slug": "ishiba-sho-hizei-minaoshi",
        "title": "石破前総理 消費税1％減税見直し「選択肢にあってしかるべき」",
        "subtitle": "石破茂前首相が消費税減税の見直しに言及。皇室典範改正にも疑問呈す。",
        "paras": [
            {
                "ja": "石破茂前総理大臣は21日、政府与党が検討している食料品の消費税率1％への減税について、状況次第では見直しも検討すべきだとの考えを示した。フジテレビの番組で「今の状況に必ずしも適合していないとするならば、それを改めるのも一つの見識だ」と述べた。",
                "en": "Former Prime Minister Shigeru Ishiba indicated on the 21st that the government and ruling party should consider revising the proposed tax reduction on food items to 1%, depending on the situation. On a Fuji TV program, he stated, 'If it does not necessarily fit the current situation, revising it is also a matter of wisdom.'",
                "literal": "前总理大臣石破茂21日表示，对于政府和执政党正在讨论的食品消费税降至1%的减税政策，根据情况也应考虑重新审视。在富士电视台节目中表示「如果未必适合当前状况，修正它也是一个见识」。",
                "grammar": "「〜次第では」— 根据情况…、取决于…。例：状況次第では（根据情况）。\n「〜べきだ」— 应该…。例：検討すべきだ（应该讨论）。\n「〜とするならば」— 如果…的话。例：適合しないとするならば（如果不适合的话）。",
                "vocab": [["前総理大臣", "ぜんそうりだいじん", "前总理大臣"], ["消費税", "しょうひぜい", "消费税"], ["減税", "げんぜい", "减税"], ["見直し", "みなおし", "重新审视"], ["適合する", "てきごうする", "适合、符合"], ["見識", "けんしき", "见识、见解"]]
            },
            {
                "ja": "また、17日に成立した改正皇室典範では、女性皇族が結婚後も皇室に残ることが可能となった一方、その配偶者と子どもは皇族とはならない。石破氏は「一つの家庭で、奥様は皇族で、配偶者と子どもはそうではない。そうすると、その家庭とは何なんだろうとなる」と疑問を呈した。",
                "en": "Furthermore, regarding the revised Imperial Household Law enacted on the 17th, which allows female imperial family members to remain in the imperial family after marriage, while their spouses and children do not become imperial family members, Ishiba questioned, 'In one family, the wife is an imperial member, but the spouse and children are not. Then what kind of family is that?'",
                "literal": "此外，关于17日成立的修改后的皇室典范，女性皇族结婚后可以留在皇室，但其配偶者和孩子不成为皇族。石破氏提出疑问「在一个家庭中，妻子是皇族，而配偶和孩子不是。那这个家庭到底是什么呢」。",
                "grammar": "「〜が可能となった」— 变得可能。例：残ることが可能となった（变得可以留下）。\n「〜一方」— 另一方面。例：可能となった一方（一方面变得可能，另一方面）。\n「〜とはならない」— 不成为…。例：皇族とはならない（不成为皇族）。",
                "vocab": [["皇室典範", "こうしつてんぱん", "皇室典范"], ["女性皇族", "じょせいこうぞく", "女性皇族"], ["配偶者", "はいぐうしゃ", "配偶者"], ["疑問を呈す", "ぎもんをていす", "提出疑问"], ["家庭", "かてい", "家庭"]]
            },
            {
                "ja": "非核三原則について石破氏は、「防衛庁長官の時も防衛大臣の時もこの議論は必要だと言ってきた」と述べ、核共有の議論の重要性を強調した。その上で「議論した結果として説明できるのであれば、やるべきだ」と述べた。",
                "en": "Regarding the Three Non-Nuclear Principles, Ishiba stated, 'I have been saying that this discussion is necessary both when I was Director General of the Defense Agency and when I was Defense Minister,' emphasizing the importance of discussing nuclear sharing. He added, 'If we can explain the results of the discussion, we should do it.'",
                "literal": "关于非核三原则，石破氏说「在担任防卫厅长官时和防卫大臣时都说过这个讨论是必要的」，强调了核共享讨论的重要性。在此基础上表示「如果作为讨论结果能够说明的话，就应该做」。",
                "grammar": "「〜に関して」— 关于…。例：非核三原則に関して（关于非核三原则）。\n「〜てきた」— 一直…（持续到现在）。例：言ってきた（一直说）。\n「〜のであれば」— 如果是…的话。例：説明できるのであれば（如果能说明的话）。",
                "vocab": [["非核三原則", "ひかくさんげんそく", "非核三原则"], ["防衛庁長官", "ぼうえいちょうちょうかん", "防卫厅长官"], ["防衛大臣", "ぼうえいだいじん", "防卫大臣"], ["強調する", "きょうちょうする", "强调"], ["核共有", "かくきょうゆう", "核共享"]]
            }
        ]
    },
    {
        "slug": "chuugoku-EEZ-syageki-hanron",
        "title": "中国外務省が反論 艦艇のEEZ内射撃訓練「懸念は理にかなっていない」",
        "subtitle": "中国艦艇が日本のEEZ内で射撃訓練。中国側は沖ノ鳥島は「岩礁」と主張。",
        "paras": [
            {
                "ja": "ロシアの艦艇と共同で航行していた中国の艦艇が日本のEEZ＝排他的経済水域の内側で射撃訓練を実施したことについて、中国外務省は「日本のいわゆる懸念は理にかなっておらず、中国はこれを断固として退けた」と反論しました。",
                "en": "Regarding the fact that Chinese naval vessels, which were navigating jointly with Russian vessels, conducted firing drills inside Japan's EEZ (Exclusive Economic Zone), China's Foreign Ministry countered, saying 'Japan's so-called concerns are not reasonable, and China has firmly rejected them.'",
                "literal": "关于与俄罗斯舰艇共同航行的中国舰艇在日本EEZ（排他的经济水域）内侧进行了射击训练一事，中国外交部反驳说「日本的所谓担忧不合理，中国坚决拒绝了这一点」。",
                "grammar": "「〜と共同で」— 与…共同。例：ロシアと共同で（与俄罗斯共同）。\n「〜について」— 关于…。例：訓練を実施したことについて（关于实施了训练一事）。\n「〜として退ける」— 作为…拒绝。例：断固として退けた（坚决拒绝）。",
                "vocab": [["艦艇", "かんてい", "舰艇"], ["排他的経済水域", "はいたてきけいざいすいいき", "排他经济水域（EEZ）"], ["射撃訓練", "しゃげきくんれん", "射击训练"], ["懸念", "けねん", "担忧、悬念"], ["理にかなう", "りにかなう", "合理、合乎道理"], ["断固として", "だんことして", "坚决地"]]
            },
            {
                "ja": "射撃訓練は沖ノ鳥島の南西180キロメートルのEEZ内で行われましたが、報道官は沖ノ鳥島について「岩礁であって島ではなく、排他的経済水域を有することはできない」と主張。「日本は他国の正当で合法的な行動を中傷し脅威をあおっている」と述べました。",
                "en": "The firing drills were conducted within the EEZ 180 kilometers southwest of Okinotorishima, but the spokesperson claimed that Okinotorishima 'is a rock, not an island, and cannot have an exclusive economic zone.' He stated, 'Japan is slandering other countries' legitimate and lawful actions and fanning threats.'",
                "literal": "射击训练在冲之鸟岛西南180公里的EEZ内进行，但发言人主张冲之鸟岛「是岩礁而非岛屿，不能拥有排他经济水域」。「日本正在中伤他国的正当合法行为并煽动威胁」。",
                "grammar": "「〜であって〜ではない」— 是…而不是…。例：岩礁であって島ではない（是岩礁而不是岛）。\n「〜を有する」— 拥有…。例：水域を有する（拥有水域）。\n「〜をあおる」— 煽动…。例：脅威をあおる（煽动威胁）。",
                "vocab": [["沖ノ鳥島", "おきのとりしま", "冲之鸟岛"], ["岩礁", "がんしょう", "岩礁"], ["島", "しま", "岛屿"], ["主張する", "しゅちょうする", "主张"], ["中傷する", "ちゅうしょうする", "中伤、诽谤"], ["脅威", "きょうい", "威胁"]]
            },
            {
                "ja": "日本政府は中国側に厳重に抗議し、再発防止を求めています。中国政府はEEZ内での軍事活動について「国際法上認められた正当な権利だ」と従来から主張しており、両国の立場は平行線をたどっています。",
                "en": "The Japanese government has lodged a strong protest with China and demanded prevention of recurrence. The Chinese government has traditionally claimed that military activities within the EEZ are 'a legitimate right recognized under international law,' and the positions of both countries remain at odds.",
                "literal": "日本政府向中方提出严正抗议并要求防止再次发生。中国政府关于EEZ内的军事活动，从以前就一直主张是「国际法上认可的正当权利」，两国的立场处于平行状态。",
                "grammar": "「〜に抗議する」— 向…抗议。例：中国側に抗議した（向中方抗议）。\n「〜について」— 关于…。例：軍事活動について（关于军事活动）。\n「〜と従来から主張する」— 从以往就一直主张…。例：権利だと主張する（主张是权利）。",
                "vocab": [["厳重に抗議", "げんじゅうにこうぎ", "严正抗议"], ["再発防止", "さいはつぼうし", "防止再次发生"], ["国際法", "こくさいほう", "国际法"], ["正当な権利", "せいとうなけんり", "正当权利"], ["平行線", "へいこうせん", "平行线（无交集）"], ["立場", "たちば", "立场"]]
            }
        ]
    },
    {
        "slug": "takasugi-sumin-0-3jikan",
        "title": "「0〜3時間睡眠が常態化」高市首相アピールに波紋 野党から懸念",
        "subtitle": "高市首相の睡眠不足アピールに批判や懸念の声。野党から「判断力低下リスク」と指摘。",
        "paras": [
            {
                "ja": "高市早苗首相が「就任以来、0〜3時間睡眠が常態化」していると自身のXに投稿し、波紋を広げている。多忙な日常を伝える狙いがあったとみられるが、野党から睡眠不足をアピールする姿勢に疑問や懸念の声が相次いでいる。",
                "en": "Prime Minister Sanae Takaichi posted on her X account that 'since taking office, 0-3 hours of sleep has become the norm,' causing a stir. It appeared intended to convey her busy daily life, but opposition parties have raised questions and concerns about her touting sleep deprivation.",
                "literal": "高市早苗首相在自身的X上投稿说「就任以来，0〜3小时睡眠已成为常态」，引起了波澜。被认为有传达忙碌日常的目的，但在野党方面对她宣传睡眠不足的姿态接连发出疑问和担忧。",
                "grammar": "「〜が常態化する」— 成为常态。例：睡眠が常態化している（睡眠不足已成为常态）。\n「〜とみられる」— 被认为…。例：狙いがあったとみられる（被认为是有目的的）。\n「〜声が相次ぐ」— 声音接连不断。例：懸念の声が相次ぐ（担忧的声音接连不断）。",
                "vocab": [["就任", "しゅうにん", "就任"], ["常態化", "じょうたいか", "常态化"], ["波紋", "はもん", "波澜、波纹"], ["多忙", "たぼう", "繁忙"], ["アピール", "あぴーる", "宣传、呼吁"], ["姿勢", "しせい", "姿态、态度"]]
            },
            {
                "ja": "首相の投稿では、週末に「骨太方針」などの分厚い資料を読んだり、国会答弁の準備をしたりしていたと報告。20日の祝日は久々に5時間眠れ、午後は洗濯やアイロンがけなどの家事ができたと明かした。SNSでは「美談でも何でもない」など批判的な反応が大半を占めた。",
                "en": "In her post, the Prime Minister reported reading thick documents such as the 'Basic Policy on Economic and Fiscal Management' on weekends and preparing for Diet interpellations. She revealed that on the national holiday on the 20th, she was able to sleep five hours for the first time in a while and did household chores like laundry and ironing in the afternoon. On social media, critical reactions such as 'it's not a heartwarming story at all' were in the majority.",
                "literal": "首相的投稿报告了周末阅读「骨太方针」等厚厚资料、准备国会答辩等。透露20日节假日久违地睡了5小时，下午做了洗衣和熨烫等家务。在SNS上，「不是什么美谈」等批评性反应占了大多数。",
                "grammar": "「〜たり〜たりする」— 做…做…等等。例：読んだり準備をしたり（阅读和准备等）。\n「〜を占める」— 占据…。例：大半を占めた（占据了大部分）。\n「〜でも何でもない」— 根本不是…。例：美談でも何でもない（根本不是美谈）。",
                "vocab": [["骨太方針", "ほねぼとほうしん", "骨太方针（经济政策基本方针）"], ["分厚い", "ぶあつい", "厚厚的"], ["国会答弁", "こっかいとうべん", "国会答辩"], ["明かす", "あかす", "透露、说明"], ["洗濯", "せんたく", "洗衣"], ["家事", "かじ", "家务"]]
            },
            {
                "ja": "国民民主党の玉木代表は「休むのも仕事だ」と指摘。中道改革連合の国重議員は睡眠不足が続けば「酩酊状態のように判断力が低下し、国家の危機管理上のリスクになり得る」と苦言を呈した。枝野幸男元官房長官もXで「こうした判断力で外交にあたられて大丈夫なのか」と懸念を示した。",
                "en": "DPFP leader Tamaki pointed out that 'resting is also part of the job.' Kuni Shige, a lawmaker from the Chuto Kaikaku Rengo, warned that continued sleep deprivation 'could lead to impaired judgment similar to intoxication, posing a risk to national crisis management.' Former Chief Cabinet Secretary Yukio Edano also expressed concern on X, asking 'Is it okay to have someone with this level of judgment handling diplomacy?'",
                "literal": "国民民主党的玉木代表指出「休息也是工作」。中道改革联合的国重议员提出苦言说如果睡眠不足持续，「判断力会像酩酊状态一样降低，可能成为国家危机管理上的风险」。枝野幸男前官房长官也在X上表示担忧「用这样的判断力来从事外交没问题吗」。",
                "grammar": "「〜のも仕事だ」— …也是工作的一部分。例：休むのも仕事だ（休息也是工作）。\n「〜得る」— 可能。例：リスクになり得る（可能成为风险）。\n「〜にあたる」— 从事…、担任…。例：外交にあたる（从事外交）。",
                "vocab": [["指摘する", "してきする", "指出"], ["睡眠不足", "すいみんぶそく", "睡眠不足"], ["判断力", "はんだんりょく", "判断力"], ["危機管理", "ききかんり", "危机管理"], ["苦言を呈す", "くげんをていす", "提出忠告"], ["懸念を示す", "けねんをしめす", "表示担忧"]]
            }
        ]
    },
    {
        "slug": "nichirei-hacker-ran samu",
        "title": "ニチレイ障害 ハッカー集団「ランサムハウス」が犯行声明",
        "subtitle": "冷凍食品大手ニチレイへのサイバー攻撃、ランサムウェア集団が犯行声明。",
        "paras": [
            {
                "ja": "サイバー攻撃を受けシステム障害を起こしたニチレイに対し、「ランサムハウス」と呼ばれるハッカー集団がインターネットのダークウェブ上に犯行声明を出したことが21日、セキュリティー関係者への取材で分かった。ランサムハウスは身代金要求型コンピューターウイルス「ランサムウェア」を常用することで知られる。",
                "en": "It was learned on the 21st through interviews with security officials that a hacker group called 'RansomHouse' had posted a claim of responsibility on the dark web regarding the system disruption at Nichirei caused by a cyberattack. RansomHouse is known for commonly using ransomware, a type of extortion computer virus.",
                "literal": "21日，通过对安全相关人员的采访得知，对于受到网络攻击发生系统故障的Nichirei，被称为「RansomHouse」的黑客集团在互联网的暗网上发布了犯案声明。RansomHouse以经常使用勒索型电脑病毒「勒索软件」而闻名。",
                "grammar": "「〜に対し」— 对于…。例：ニチレイに対し（对于Nichirei）。\n「〜で分かる」— 通过…了解到。例：取材で分かった（通过采访得知）。\n「〜ことで知られる」— 以…闻名。例：常用することで知られる（以经常使用而闻名）。",
                "vocab": [["サイバー攻撃", "さいばーこうげき", "网络攻击"], ["システム障害", "しすてむしょうがい", "系统故障"], ["ハッカー集団", "はっかーしゅうだん", "黑客集团"], ["ダークウェブ", "だーくうぇぶ", "暗网"], ["犯行声明", "はんこうせいめい", "犯案声明"], ["ランサムウェア", "らんさむうぇあ", "勒索软件"]]
            },
            {
                "ja": "ニチレイは15日、グループのサーバーがサイバー攻撃を受けたと発表。一部システムが使えなくなり、物流や冷凍食品の出荷に影響が出た。企業を狙ったランサムウェア攻撃は国内外で後を絶たず、ニチレイは復旧作業を進めている。",
                "en": "Nichirei announced on the 15th that its group servers had been hit by a cyberattack. Some systems became unusable, affecting logistics and frozen food shipments. Ransomware attacks targeting companies continue unabated both domestically and internationally, and Nichirei is proceeding with recovery efforts.",
                "literal": "Nichirei于15日宣布，集团的服务器受到了网络攻击。部分系统无法使用，影响了物流和冷冻食品的出货。针对企业的勒索软件攻击在国内外不断发生，Nichirei正在进行恢复工作。",
                "grammar": "「〜と発表した」— 发表了…。例：受けたと発表した（发表了受到攻击）。\n「〜影響が出る」— 出现影响。例：出荷に影響が出た（对出货产生影响）。\n「〜後を絶たない」— 不断发生、络绎不绝。例：後を絶たず（不断发生）。",
                "vocab": [["サーバー", "さーばー", "服务器"], ["物流", "ぶつりゅう", "物流"], ["冷凍食品", "れいとうしょくひん", "冷冻食品"], ["出荷", "しゅっか", "出货"], ["後を絶たない", "あとをたたない", "不断发生"], ["復旧作業", "ふっきゅうさぎょう", "恢复工作"]]
            },
            {
                "ja": "専門家は、企業のセキュリティ対策の重要性を強調する。ランサムウェア攻撃は年々巧妙化しており、被害が発覚した場合、復旧に長期間かかるケースも少なくない。定期的なバックアップや従業員のセキュリティ意識向上が求められている。",
                "en": "Experts emphasize the importance of corporate security measures. Ransomware attacks are becoming more sophisticated year by year, and when damage is discovered, it often takes a long time to recover. Regular backups and improving employee security awareness are required.",
                "literal": "专家强调企业安全对策的重要性。勒索软件攻击逐年变得巧妙，受害被发现时，恢复需要很长时间的情况也不少。定期的备份和员工安全意识提高被要求。",
                "grammar": "「〜を強調する」— 强调…。例：重要性を強調する（强调重要性）。\n「〜傾向がある」— 有…倾向。例：巧妙化している（变得巧妙）。\n「〜が求められている」— 被要求…。例：意識向上が求められている（要求提高意识）。",
                "vocab": [["専門家", "せんもんか", "专家"], ["セキュリティ対策", "せきゅりてぃたいさく", "安全对策"], ["巧妙化", "こうみょうか", "变得巧妙"], ["発覚する", "はっかくする", "被发现、暴露"], ["バックアップ", "ばっくあっぷ", "备份"], ["意識向上", "いしきこうじょう", "意识提高"]]
            }
        ]
    },
    {
        "slug": "nenkyuu-800man-chou",
        "title": "年収800万円超は日本に何％？国税庁調査が示す給与の実態",
        "subtitle": "年収800万円超の割合は全体の12％。男女間で大きな格差。",
        "paras": [
            {
                "ja": "国税庁が実施した「令和6年分民間給与実態統計調査」によると、日本の給与所得者の平均給与は477.5万円となっている。性別では男性が586.7万円、女性が333.2万円と、男女間で大きな差があることが改めて浮き彫りになった。",
                "en": "According to the 'Reiwa 6 Private Salary Actual Survey' conducted by the National Tax Agency, the average salary of Japanese wage earners is 4.775 million yen. By gender, men earn 5.867 million yen and women earn 3.332 million yen, once again highlighting the large gap between men and women.",
                "literal": "根据国税厅实施的「令和6年民间工资实际情况统计调查」，日本工资所得者的平均工资为477.5万日元。按性别，男性586.7万日元，女性333.2万日元，再次突显了男女之间的巨大差距。",
                "grammar": "「〜によると」— 根据…。例：調査によると（根据调查）。\n「〜となっている」— 是…（表示状态）。例：477.5万円となっている（是477.5万日元）。\n「〜が浮き彫りになる」— 被突显出来。例：差が浮き彫りになった（差距被凸显）。",
                "vocab": [["国税庁", "こくぜいちょう", "国税厅"], ["給与所得者", "きゅうよしょとくしゃ", "工资收入者"], ["平均給与", "へいきんきゅうよ", "平均工资"], ["男女間", "だんじょかん", "男女之间"], ["浮き彫り", "うきぼり", "凸显、突出"]]
            },
            {
                "ja": "年収800万円超の割合は全体の12.0％で、上位約1割に位置することがわかった。男性は18.3％が年収800万円を超えているのに対し、女性はわずか3.5％にとどまった。年収800万円は女性のキャリア形成において、今もなお突破しがたい高い壁となっている。",
                "en": "The proportion of people earning over 8 million yen was 12.0% of the total, placing them in the top 10%. While 18.3% of men earn over 8 million yen, only 3.5% of women do. The 8 million yen mark remains a high and difficult-to-break barrier for women's career development.",
                "literal": "年收入800万日元以上的比例为全体的12.0%，处于上位约1成。男性18.3%年收入超过800万日元，而女性仅停留在3.5%。年收入800万日元在女性职业形成上，至今仍然是一个难以突破的高墙。",
                "grammar": "「〜に対し」— 而、相对于…。例：男性18.3％に対し女性3.5％（男性18.3%而女性3.5%）。\n「〜にとどまる」— 停留在…。例：3.5％にとどまった（停留在3.5%）。\n「〜なお」— 仍然、依旧。例：今もなお（至今仍然）。",
                "vocab": [["年収", "ねんしゅう", "年收入"], ["割合", "わりあい", "比例、比率"], ["キャリア形成", "きゃりあけいせい", "职业发展、职业形成"], ["突破する", "とっぱする", "突破"], ["障壁", "しょうへき", "障碍、壁垒"]]
            },
            {
                "ja": "業種別の平均給与には大きな格差が存在し、高年収を目指す上では個人の努力だけでなく「どの産業に属するか」という初期選択が重要となる。年齢上昇とともに平均給与は上昇するが、頭打ちになるタイミングは雇用形態によって異なる。",
                "en": "There are large disparities in average salary by industry, and aiming for a high income depends not only on individual effort but also on the initial choice of 'which industry to belong to.' While average salary increases with age, the timing of when it peaks varies depending on employment type.",
                "literal": "行业别的平均工资存在巨大差距，在以高年收入为目标时，不仅是个人的努力，「属于哪个产业」这一初期选择也很重要。随着年龄上升平均工资会上涨，但到达顶峰的时机因雇佣形态而异。",
                "grammar": "「〜上で」— 在…上、在…方面。例：目指す上で（在追求…方面）。\n「〜だけでなく」— 不仅…。例：努力だけでなく（不仅努力）。\n「〜によって異なる」— 因…而异。例：雇用形態によって異なる（因雇佣形态而异）。",
                "vocab": [["業種", "ぎょうしゅ", "行业、业种"], ["格差", "かくさ", "差距、差异"], ["産業", "さんぎょう", "产业"], ["雇用形態", "こようけいたい", "雇佣形态"], ["頭打ち", "あたまうち", "达到顶峰、停滞"]]
            }
        ]
    },
    {
        "slug": "kousho-ondo-10nen-ichido",
        "title": "気象庁「10年に一度の高温」早期天候情報 今月末にかけ危険な暑さ",
        "subtitle": "7月27〜29日頃から「10年に一度の著しい高温」の可能性。熱中症に厳重警戒。",
        "paras": [
            {
                "ja": "気象庁は22日、7月27日から29日頃にかけて「この時期としては10年に一度程度しか起きないような著しい高温」となる可能性があるとして、「高温に関する早期天候情報」を発表した。関東甲信、近畿、東海、北陸、中国、四国、九州、北海道の広い範囲が対象となっている。",
                "en": "The Japan Meteorological Agency announced on the 22nd an 'Early Weather Information on High Temperatures,' warning of the possibility of 'remarkably high temperatures that typically occur only about once every ten years for this season' from around July 27th to 29th. The warning covers a wide area including Kanto-Koshin, Kinki, Tokai, Hokuriku, Chugoku, Shikoku, Kyushu, and Hokkaido.",
                "literal": "气象厅22日，发表了关于7月27日至29日左右可能出现「这个时期大约10年才有一次的显著高温」的「高温相关的早期天气信息」。关东甲信、近畿、东海、北陆、中国、四国、九州、北海道的广大范围为对象。",
                "grammar": "「〜にかけて」— 到…为止（时间/范围）。例：29日頃にかけて（到29日左右）。\n「〜として」— 作为…。例：時期としては（作为这个时期）。\n「〜可能性がある」— 有…可能性。例：高温となる可能性（可能成为高温）。",
                "vocab": [["気象庁", "きしょうちょう", "气象厅"], ["早期天候情報", "そうきてんこうじょうほう", "早期天气信息"], ["著しい", "いちじるしい", "显著的"], ["高温", "こうおん", "高温"], ["対象", "たいしょう", "对象"]]
            },
            {
                "ja": "関東甲信地方では29日頃から「かなりの高温」が見込まれ、5日間平均気温が平年より2.1℃以上高くなる基準に達する見通し。熱中症の危険性が高い状態となるため、屋外活動では飲料水の確保や日陰での休憩など、徹底した対策が必要だとしている。",
                "en": "In the Kanto-Koshin region, 'considerably high temperatures' are expected from around the 29th, with the 5-day average temperature forecast to reach the standard of 2.1°C or more above normal. Since this creates a high risk of heatstroke, thorough measures such as ensuring drinking water and resting in the shade during outdoor activities are deemed necessary.",
                "literal": "关东甲信地方从29日左右开始预计将出现「相当高温」，5天平均气温预计达到比常年高2.1℃以上的基准。由于会形成中暑危险性高的状态，在室外活动中需要彻底的确保饮用水和阴凉处休息等对策。",
                "grammar": "「〜が見込まれる」— 预计…。例：高温が見込まれる（预计高温）。\n「〜に達する」— 达到…。例：基準に達する（达到标准）。\n「〜としている」— 认为…、规定…。例：必要だとしている（认为有必要）。",
                "vocab": [["かなりの高温", "かなりのこうおん", "相当高的温度"], ["平均気温", "へいきんきおん", "平均气温"], ["平年", "へいねん", "常年、平年"], ["熱中症", "ねっちゅうしょう", "中暑"], ["飲料水", "いんりょうすい", "饮用水"], ["対策", "たいさく", "对策"]]
            },
            {
                "ja": "気象庁は、1週間以内に高温が予測される場合は気象解説情報を、翌日または当日に熱中症の危険性が極めて高くなる場合は熱中症警戒アラートを発表するとしている。農作物や家畜の管理にも注意が必要で、健康管理とあわせて警戒が呼びかけられている。",
                "en": "The Japan Meteorological Agency says it will issue weather advisory information when high temperatures are forecast within a week, and a heatstroke alert when the risk of heatstroke becomes extremely high the next day or on the same day. Caution is also needed for crop and livestock management, with warnings being issued along with health management advice.",
                "literal": "气象厅表示，如果预测一周内有高温，将发布气象解说信息；如果次日或当天中暑危险性极高时，将发布中暑警戒警报。农作物和家畜的管理也需要注意，与健康管理一起被呼吁警戒。",
                "grammar": "「〜場合は」— …的情况下。例：予測される場合は（被预测的情况下）。\n「〜としている」— 规定…、表示。例：発表するとしている（规定将发布）。\n「〜とあわせて」— 与…一起。例：健康管理とあわせて（与健康管理一起）。",
                "vocab": [["気象解説情報", "きしょうかいせつじょうほう", "气象解说信息"], ["熱中症警戒アラート", "ねっちゅうしょうけいかいあらーと", "中暑警戒警报"], ["農作物", "のうさくもつ", "农作物"], ["家畜", "かちく", "家畜"], ["警戒する", "けいかいする", "警戒"], ["呼びかける", "よびかける", "呼吁、号召"]]
            }
        ]
    }
]

##########################
# PROCESS ALL ARTICLES
##########################

base_dir = '/home/horse/.openclaw/workspace/asanews'
today = '2026-07-22'

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
        "date": today,
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
    post_lines = [p['ja'] for p in art['paras'][:3]]
    post = f"""---
title: {art['title']}
date: {today} 11:30:00 +0900
categories: [ニュース]
tags: [ニュース]
---

{chr(10).join(post_lines)}

<div class="mt-4 p-3" style="background:#f0f4f8;border-radius:8px;text-align:center;">
  <a href="/asanews/reading-room/?read={slug}" class="btn btn-danger" style="color:#fff;padding:10px 24px;border-radius:6px;font-weight:bold;">
    📖 読解ルームで詳しく読む
  </a>
</div>
"""
    os.makedirs(f'{base_dir}/_posts', exist_ok=True)
    with open(f'{base_dir}/_posts/{today}-{slug}.md', 'w', encoding='utf-8') as f:
        f.write(post)
    print(f"  ✅ Blog post created")
    
    return slug

# Process all articles
processed = []
for art in articles_data:
    slug = process_article(art)
    processed.append(slug)

# 5. Update index.json - READ the existing, prepend new ones
index_path = f'{base_dir}/assets/readings/index.json'
existing_index = []
if os.path.exists(index_path):
    with open(index_path, 'r', encoding='utf-8') as f:
        try:
            existing_index = json.load(f)
        except:
            existing_index = []

new_index = []
for art in articles_data:
    new_index.append({
        "id": art['slug'],
        "title": art['title'],
        "level": "中級",
        "length": len(art['paras']),
        "date": today,
        "file": f"assets/readings/{art['slug']}.json"
    })

# Prepend new articles to existing
combined_index = new_index + existing_index

with open(index_path, 'w', encoding='utf-8') as f:
    json.dump(combined_index, f, ensure_ascii=False, indent=2)
print(f"\n✅ index.json updated with {len(new_index)} new articles (total {len(combined_index)})")

# 6. Update READING_LIST in reading-room.js
js_list = []
for item in combined_index:
    js_list.append(f"    {{\n      id: '{item['id']}',\n      title: '{item['title']}',\n      kicker: '{item['level']}',\n      desc: '',\n      badge: '{item['length']}段落',\n      file: '/asanews/assets/readings/{item['id']}.json'\n    }}")

js_replace = "  const READING_LIST = [\n" + ",\n".join(js_list) + "\n  ];"

js_path = f'{base_dir}/assets/js/reading-room.js'
with open(js_path, 'r') as f:
    js = f.read()

js_new = re.sub(
    r'const READING_LIST = \[.*?\];',
    js_replace,
    js,
    flags=re.DOTALL
)

with open(js_path, 'w') as f:
    f.write(js_new)

print(f"✅ reading-room.js READING_LIST updated ({len(combined_index)} articles)")

# Verify
print(f"\n{'='*60}")
print("📋 Verification:")
for slug in processed:
    j = f'{base_dir}/assets/readings/{slug}.json'
    if os.path.exists(j):
        with open(j) as f:
            d = json.load(f)
        pc = len(d[0]['paragraphs'])
        # Check audio
        audio_ok = True
        for pi in range(pc):
            ap = f'{base_dir}/assets/audio/{slug}/p{pi+1}.mp3'
            if not os.path.exists(ap) or os.path.getsize(ap) < 1000:
                audio_ok = False
        audio_mark = "🔊" if audio_ok else "❌"
        print(f"  {audio_mark} {slug:30s} | {pc} paragraphs | JSON OK")
        print(f"     📝 {d[0]['title']}")
    else:
        print(f"  ❌ {slug} missing!")

print(f"\n{'='*60}")
print(f"🎉 ALL DONE! Processed {len(processed)} articles for {today}")
print(f"{'='*60}")
