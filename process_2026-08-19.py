#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-19 (Wed) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-19'
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
        "slug": "zankusho-moushobi-kyuusyuu",
        "title": "今日19日は大阪や名古屋で35℃以上の猛暑日か 九州では38℃を超える所も",
        "subtitle": "from tenki.jp",
        "paras": [
            {
                "ja": "今日19日(水)は全国的に残暑が厳しいでしょう。特に九州から東海で35℃以上の猛暑日となる所がありそうです。広島市や大阪市、名古屋市では久しぶりに猛暑日となる可能性があります。九州では38℃を超える所も出てきそうです。屋外での活動は時間を決めて涼しい場所で休憩をとり、こまめに水分を補給してください。",
                "en": "Wednesday the 19th will have severe lingering summer heat nationwide. Especially from Kyushu to Tokai, some places are likely to see \"mōshobi\" days of 35°C or higher. Hiroshima City, Osaka City, and Nagoya City may see their first mōshobi days in a while. Some places in Kyushu are also likely to exceed 38°C. For outdoor activities, set a time limit, take breaks in cool places, and hydrate frequently.",
                "literal": "今天19日（周三）全国残暑将会很严峻。特别是从九州到东海，有些地方似乎会出现35度以上的猛暑日。广岛市、大阪市、名古屋市有可能时隔许久迎来猛暑日。九州也有出现超过38度的地方。户外活动请限定时间、在凉爽处休息，并勤补水。",
                "grammar": "「〜でしょう」— 大概会…吧（推测）。例：残暑が厳しいでしょう（残暑大概会很严峻）。\n「〜がありそうです」— 好像会有…。例：猛暑日となる所がありそうです（好像会有成为猛暑日的地方）。\n「〜てください」— 请…（请求）。例：水分を補給してください（请补充水分）。",
                "vocab": [["残暑", "ざんしょ", "残暑、初秋的炎热"], ["猛暑日", "もうしょび", "猛暑日（最高气温35度以上）"], ["東海", "とうかい", "东海（地区）"], ["屋外", "おくがい", "室外、户外"], ["休憩", "きゅうけい", "休息"], ["水分", "すいぶん", "水分"]]
            },
            {
                "ja": "特に暑くなりそうなのが、九州から東海です。最高気温は昨日と同じくらいか、高くなる所が多く、35℃以上の猛暑日の所が続出するでしょう。広島市は8日ぶりに、大阪市や名古屋市は9日ぶりに猛暑日となる可能性があります。大分県日田市や福岡県久留米市など九州では38℃を超える所も出てきそうです。",
                "en": "The areas likely to get especially hot are Kyushu to Tokai. In many places the highest temperature will be about the same as yesterday or higher, and mōshobi days of 35°C or more are expected to appear one after another. Hiroshima City may see a mōshobi day for the first time in 8 days, and Osaka and Nagoya for the first time in 9 days. In Kyushu, including Hita City in Oita Prefecture and Kurume City in Fukuoka Prefecture, some places are likely to exceed 38°C.",
                "literal": "特别是容易变热的，是从九州到东海。最高气温与昨天差不多或更高的地方很多，35度以上的猛暑日将会接连出现。广岛市时隔8天、大阪市和名古屋市时隔9天有可能出现猛暑日。大分县日田市、福冈县久留米市等九州地区，似乎也会出现超过38度的地方。",
                "grammar": "「〜そうなのが〜です」— 看起来会是…的是…。例：暑くなりそうなのが、九州から東海です（看起来会变热的是九州到东海）。\n「〜続出するでしょう」— 大概会接连出现。例：猛暑日の所が続出するでしょう（猛暑日的地方大概会接连出现）。\n「〜ぶりに」— 时隔…。例：8日ぶりに猛暑日（时隔8天的猛暑日）。",
                "vocab": [["最高気温", "さいこうきおん", "最高气温"], ["続出", "ぞくしゅつ", "接连出现"], ["可能性", "かのうせい", "可能性"], ["超える", "こえる", "超过"], ["日田市", "ひたし", "日田市"], ["久留米市", "くるめし", "久留米市"]]
            },
            {
                "ja": "関東甲信や北陸も33℃前後まで上がる所が多く、内陸部では35℃に迫る所もありそうです。東北は昨日より2℃前後高くなり、30℃を超える所が多いでしょう。北海道は30℃前後の予想で、真夏並みの暑さでしょう。熊本市は37℃の予想で、体にこたえる暑さが続きます。",
                "en": "In Kanto-Koshin and Hokuriku, many places will rise to around 33°C, and some inland areas are likely to approach 35°C. Tohoku will be about 2°C higher than yesterday, with many places exceeding 30°C. Hokkaido is forecast around 30°C, with midsummer-like heat. Kumamoto City is forecast at 37°C, and the punishing heat will continue.",
                "literal": "关东甲信和北陆也有很多地方上升到33度左右，内陆地区似乎也有逼近35度的地方。东北比昨天高出2度左右，超过30度的地方会很多。北海道预计30度左右，会是盛夏般的炎热。熊本市预计37度，折磨身体的炎热将持续。",
                "grammar": "「〜まで上がる」— 上升到…。例：33℃前後まで上がる（上升到33度左右）。\n「〜に迫る」— 逼近…。例：35℃に迫る所もありそうです（似乎也有逼近35度的地方）。",
                "vocab": [["関東甲信", "かんとうこうしん", "关东甲信（地区）"], ["北陸", "ほくりく", "北陆（地区）"], ["内陸部", "ないりくぶ", "内陆地区"], ["東北", "とうほく", "东北（地区）"], ["北海道", "ほっかいどう", "北海道"], ["真夏並み", "まなつなみ", "盛夏程度"]]
            },
            {
                "ja": "お盆休み明けは熱中症の搬送者数が増える時期です。お休み中に涼しい場所で過ごすことが多かった方は、体が暑さに慣れていない可能性があり、無理は禁物です。熱中症警戒アラートが発表された所では、外出をできるだけ控え、のどが渇く前にこまめに水分を補給しましょう。暑さ指数(WBGT)を確認して、行動の目安にしてください。",
                "en": "The period after the Obon holidays is when the number of people transported for heatstroke increases. People who spent much of their time off in cool places may not be acclimated to the heat, so overexertion is a must-avoid. In areas where heatstroke alerts have been issued, refrain from going out as much as possible and hydrate frequently before you feel thirsty. Check the heat index (WBGT) and use it as a guide for your activities.",
                "literal": "盂兰盆节假期结束后是热射病送医人数增加的时期。假期中多在凉爽处度过的人，身体可能还没有适应暑热，勉强硬撑是禁忌。在发布热射病警戒警报的地方，请尽量控制外出，在口渴之前勤补水。请确认暑热指数（WBGT），作为行动的参考。",
                "grammar": "「〜明け」— 结束后。例：お盆休み明け（盂兰盆假结束后）。\n「〜ていません」— 还没有…。例：暑さに慣れていません（还没有适应暑热）。\n「〜ましょう」— 让我们…吧（劝诱）。例：水分を補給しましょう（让我们补充水分吧）。",
                "vocab": [["お盆", "おぼん", "盂兰盆节"], ["熱中症", "ねっちゅうしょう", "中暑、热射病"], ["搬送", "はんそう", "运送、送医"], ["禁物", "きんもつ", "禁忌、切忌"], ["警戒", "けいかい", "警戒"], ["暑さ指数", "あつさしすう", "暑热指数"]]
            },
        ]
    },
    {
        "slug": "chiba-gouu-syaryou-tekkyo",
        "title": "豪雨で路上に残る車両まだ600台 国や千葉県など官民、撤去で連携",
        "subtitle": "from 朝日新聞",
        "paras": [
            {
                "ja": "13日夕から千葉県内を襲った豪雨で水没などした自動車が路上に残っている問題について、県は18日、国や千葉市などとともにプロジェクトチーム(PT)を立ち上げ、連携して車の移動に取り組む方針を明らかにした。",
                "en": "Regarding the problem of cars that were submerged or otherwise damaged in the heavy rain that hit Chiba Prefecture from the evening of the 13th and remain on the roads, the prefecture on the 18th announced a policy of launching a project team (PT) together with the national government and Chiba City to work together on moving the vehicles.",
                "literal": "关于13日傍晚袭击千叶县内的暴雨中遭水淹等而在路上遗留的汽车问题，县政府于18日与国家、千叶市等共同成立项目组（PT），明确了联手推进车辆移动的方针。",
                "grammar": "「〜を襲った」— 袭击了…。例：千葉県内を襲った豪雨（袭击千叶县内的暴雨）。\n「〜とともに」— 与…一起。例：国や千葉市などとともに（与国家、千叶市等一起）。\n「〜方針を明らかにした」— 明确了…的方针。例：取り組む方針を明らかにした（明确了推进的方针）。",
                "vocab": [["豪雨", "ごうう", "暴雨、豪雨"], ["水没", "すいぼつ", "被水淹没"], ["プロジェクトチーム", "ぷろじぇくとちーむ", "项目组"], ["立ち上げる", "たちあげる", "成立、启动"], ["連携", "れんけい", "合作、联动"], ["方針", "ほうしん", "方针"]]
            },
            {
                "ja": "路上に残っている車両は一時、千葉市を中心に少なくとも約2700台に上った。18日午前9時時点で、県内の幹線道路などに残っているのは千葉市内の約200台を含む約600台で、渋滞などの原因にもなっている。",
                "en": "The number of vehicles remaining on the roads temporarily reached at least about 2,700, centered on Chiba City. As of 9 a.m. on the 18th, about 600 vehicles remain on major roads in the prefecture, including about 200 in Chiba City, and they are causing traffic congestion and other problems.",
                "literal": "留在路上的车辆一度以千叶市为中心达到至少约2700辆。截至18日上午9点，留在县内干线道路等上的车辆包括千叶市内约200辆在内共约600辆，也成为交通拥堵等原因。",
                "grammar": "「〜に上った」— 达到…（之多）。例：約2700台に上った（达到约2700辆之多）。\n「〜時点で」— 在…时点。例：18日午前9時時点で（截至18日上午9点）。\n「〜を含む」— 包括…。例：千葉市内の約200台を含む（包括千叶市内约200辆）。",
                "vocab": [["車両", "しゃりょう", "车辆"], ["一時", "いちじ", "一度、暂时"], ["少なくとも", "すくなくとも", "至少"], ["幹線道路", "かんせんどうろ", "干线道路"], ["渋滞", "じゅうたい", "拥堵"], ["原因", "げんいん", "原因"]]
            },
            {
                "ja": "県道路環境課によると、出席者からは車の持ち主への連絡がとりづらい点や、移動後の保管場所の確保などが課題にあげられた。また、路上の車を撤去する際の費用については、持ち主に負担を求める意見もあった。作業完了のめどや今後の会議日程は未定という。",
                "en": "According to the prefecture's Road Environment Division, participants raised issues such as the difficulty of contacting vehicle owners and securing storage locations after moving the cars. There was also an opinion that owners should bear the costs of removing vehicles from the roads. It was said that the timeline for completing the work and the schedule for future meetings are undecided.",
                "literal": "据县道路环境课称，出席者提出了难以联系车主、确保移动后保管场所等问题。另外，关于撤除路上车辆的费用，也有意见要求车主承担。据说作业完成的预期时间和今后的会议日程尚未确定。",
                "grammar": "「〜によると」— 根据…。例：県道路環境課によると（据县道路环境课称）。\n「〜が課題にあげられた」— …被列为课题。例：保管場所の確保などが課題にあげられた（确保保管场所等被列为课题）。\n「〜という」— 据说…。例：未定という（据说尚未确定）。",
                "vocab": [["出席者", "しゅっせきしゃ", "出席者"], ["持ち主", "もちぬし", "所有者"], ["保管場所", "ほかんばしょ", "保管场所"], ["撤去", "てっきょ", "撤除、拆除"], ["費用", "ひよう", "费用"], ["めど", "めど", "预期、眉目"]]
            },
            {
                "ja": "住宅の浸水被害が確認された千葉県大網白里市を視察した熊谷俊人知事は18日午後、報道陣から被災車両への対応について問われ、「できる限り早くめどは示したい。事故や渋滞が起きないような環境を一日も早く実現する。オール行政で取り組んでいきたい」と話した。",
                "en": "Governor Kumagai Toshihito, who inspected Ōamishirasato City, where flood damage to homes has been confirmed, was asked by reporters on the afternoon of the 18th about the response to the affected vehicles. He said, \"We want to show a timeline as soon as possible. We will realize an environment where accidents and congestion do not occur as quickly as possible. We want to work on this with the entire administration.\"",
                "literal": "视察了确认有住宅浸水灾害的千叶县大网白里市的熊谷俊人知事于18日下午被记者问及对受灾车辆的对策，他说：“希望尽早给出眉目。希望尽早实现不发生事故和拥堵的环境。希望全行政合力推进。”",
                "grammar": "「〜を視察した」— 视察了…。例：大網白里市を視察した知事（视察了大网白里市的知事）。\n「〜から問われ」— 被…询问。例：報道陣から問われ（被记者团询问）。\n「〜ていきたい」— 想要继续…。例：取り組んでいきたい（想要继续推进）。",
                "vocab": [["浸水", "しんすい", "浸水、进水"], ["視察", "しさつ", "视察"], ["報道陣", "ほうどうじん", "记者团"], ["被災車両", "ひさいしゃりょう", "受灾车辆"], ["対応", "たいおう", "应对"], ["行政", "ぎょうせい", "行政"]]
            },
        ]
    },
    {
        "slug": "kusakari-netchushou-shibou",
        "title": "【速報】草刈り作業中の男性が死亡 体温は搬送時約40度 熱中症の可能性も 兵庫・小野市",
        "subtitle": "from テレビ朝日系（ABCニュース）",
        "paras": [
            {
                "ja": "18日午後、兵庫県小野市の市道で、草刈り作業をしていた男性が倒れているのが見つかり、その後死亡が確認されました。男性は搬送時、体温が約40度だったといい、警察は熱中症の可能性もあるとみて捜査を進めています。",
                "en": "On the afternoon of the 18th, a man who had been doing grass-cutting work was found collapsed on a city road in Ono City, Hyogo Prefecture, and his death was confirmed afterwards. The man's body temperature was about 40 degrees Celsius when transported, and police are investigating, believing heatstroke was a possibility.",
                "literal": "18日下午，在兵库县小野市的市道上，发现一名正在割草作业的男性倒在地上，之后确认其死亡。据称该男性送医时体温约40度，警方认为有可能是中暑并正在展开调查。",
                "grammar": "「〜ているのが見つかり」— 被发现正在…。例：倒れているのが見つかり（被发现倒在地上）。\n「〜たといい」— 据说…。例：体温が約40度だったといい（据说体温约40度）。\n「〜とみて」— 认为是…。例：熱中症の可能性もあるとみて（认为也可能是中暑）。",
                "vocab": [["草刈り", "くさかり", "割草、除草"], ["倒れる", "たおれる", "倒下"], ["死亡", "しぼう", "死亡"], ["搬送時", "はんそうじ", "送医时"], ["体温", "たいおん", "体温"], ["捜査", "そうさ", "搜查、侦办"]]
            },
            {
                "ja": "18日午後4時40分すぎ、兵庫県小野市菅田町の市道108号線付近で、草刈り作業をしていた男性(77)から、「熱中症の疑いがある男性が倒れている。意識がない」と119番通報がありました。",
                "en": "Just after 4:40 p.m. on the 18th, a man (77) who had been doing grass-cutting work near City Road No. 108 in Sugata-cho, Ono City, Hyogo Prefecture, called 119 reporting, \"A man who appears to have heatstroke has collapsed. He is unconscious.\"",
                "literal": "18日下午4点40分过后，在兵库县小野市菅田町的市道108号线附近，一名正在割草作业的男性（77岁）拨打119报警称“有一名疑似中暑的男性倒在地上。没有意识”。",
                "grammar": "「〜すぎ」— 刚过…。例：午後4時40分すぎ（下午4点40分刚过）。\n「〜から〜通報がありました」— 有来自…的报警。例：男性から通報がありました（有来自男性的报警）。\n「〜の疑いがある」— 有…的嫌疑/可能。例：熱中症の疑いがある（疑似中暑）。",
                "vocab": [["付近", "ふきん", "附近"], ["意識", "いしき", "意识"], ["119番", "ひゃくじゅうきゅうばん", "119（日本急救/火警电话）"], ["通報", "つうほう", "报警、通报"], ["疑い", "うたがい", "嫌疑、疑似"], ["市道", "しどう", "市道"]]
            },
            {
                "ja": "警察によりますと、倒れていたのは、神戸市中央区に住むアルバイトの男性(58)で、病院に搬送されましたが、その後死亡が確認されました。通報した男性(77)は死亡した男性の上司で、2人は午前9時から午後4時にかけて、付近の草刈り作業にあたっていたということです。",
                "en": "According to police, the man who had collapsed was a part-time worker (58) living in Chuo Ward, Kobe City. He was transported to a hospital, but his death was confirmed afterwards. The man (77) who made the call was the deceased man's supervisor, and the two had been engaged in grass-cutting work in the area from 9 a.m. to 4 p.m.",
                "literal": "据警方称，倒地的是住在神户市中央区的一名打工男性（58岁），被送往医院后确认死亡。报警的男性（77岁）是死者上司，据说两人从上午9点到下午4点一直在附近进行割草作业。",
                "grammar": "「〜によりますと」— 根据…。例：警察によりますと（据警方称）。\n「〜にかけて」— 从…到…（时间段）。例：午前9時から午後4時にかけて（从上午9点到下午4点）。\n「〜にあたっていた」— 正在从事…。例：草刈り作業にあたっていた（正在从事割草作业）。",
                "vocab": [["アルバイト", "あるばいと", "打工、兼职"], ["搬送", "はんそう", "送医、运送"], ["上司", "じょうし", "上司"], ["作業", "さぎょう", "作业"], ["午前", "ごぜん", "上午"], ["死亡", "しぼう", "死亡"]]
            },
            {
                "ja": "それぞれ離れた場所で2人は作業にあたっていましたが、午後4時になっても、男性と連絡が取れなかったため、上司が様子を見に行くと、男性が路上で倒れていたということです。搬送時、男性には目立った外傷はなく、体温が約40度だったことなどから、警察は男性が熱中症になっていた可能性もあるとみて、当時の状況を詳しく調べています。",
                "en": "The two had been working in separate locations, but when the man could not be reached even by 4 p.m., the supervisor went to check on him and found him collapsed on the road. At the time of transport, the man had no notable external injuries and his body temperature was about 40 degrees, so police believe he may have suffered heatstroke and are investigating the situation in detail.",
                "literal": "两人分别在相隔的地方作业，但到下午4点仍联系不上男性，上司前去查看情况时，发现男性倒在路上。送医时男性没有明显外伤，因体温约40度等，警方认为男性有可能中暑，正在详细调查当时的情况。",
                "grammar": "「〜ため」— 因为…。例：連絡が取れなかったため（因为联系不上）。\n「〜と、〜た」— 一…就…。例：様子を見に行くと、倒れていた（前去看情况，发现倒着）。\n「〜ことなどから」— 由于…等。例：体温が約40度だったことなどから（由于体温约40度等）。",
                "vocab": [["それぞれ", "それぞれ", "各自、分别"], ["連絡", "れんらく", "联系"], ["様子", "ようす", "情况、样子"], ["外傷", "がいしょう", "外伤"], ["状況", "じょうきょう", "状况"], ["詳しく", "くわしく", "详细地"]]
            },
        ]
    },
    {
        "slug": "jyuugo-sai-houka-ryoushin",
        "title": "15歳中学生“放火”と“殺人未遂”で逮捕 自宅にガソリンか…「お父さんが暴力を振ってくるのが嫌いで」 福岡・大牟田市",
        "subtitle": "from KBC九州朝日放送",
        "paras": [
            {
                "ja": "18日未明、福岡県大牟田市で木造住宅が全焼する火事がありました。この火事で、警察は自宅にガソリンのようなものを撒いて火をつけ、就寝中の両親を殺害しようとしたとして、同居する息子(中学3年・15歳)を現住建造物放火と殺人未遂の疑いで逮捕しました。",
                "en": "In the early hours of the 18th, a fire that completely burned a wooden house broke out in Ōmuta City, Fukuoka Prefecture. In connection with this fire, police arrested the son living in the house (a 15-year-old third-year junior high school student) on suspicion of arson of an occupied building and attempted murder, saying he had poured something like gasoline in the house, set it on fire, and tried to kill his parents while they slept.",
                "literal": "18日凌晨，福冈县大牟田市发生木造住宅全烧的火灾。警方以向家中泼洒类似汽油的液体并点火、企图杀害正在睡觉的父母为由，逮捕了同住的儿子（初中三年级、15岁），涉嫌对现住建筑物放火和杀人未遂。",
                "grammar": "「〜未明」— …凌晨。例：18日未明（18日凌晨）。\n「〜として」— 以…为由。例：殺害しようとしたとして（以企图杀害为由）。\n「〜の疑いで逮捕しました」— 以…的嫌疑逮捕。例：殺人未遂の疑いで逮捕しました（以杀人未遂的嫌疑逮捕）。",
                "vocab": [["未明", "みめい", "凌晨、拂晓"], ["木造住宅", "もくぞうじゅうたく", "木造住宅"], ["全焼", "ぜんしょう", "全部烧毁"], ["撒く", "まく", "泼洒、撒"], ["就寝中", "しゅうしんちゅう", "就寝中、睡觉时"], ["殺人未遂", "さつじんみすい", "杀人未遂"]]
            },
            {
                "ja": "警察と消防によりますと、火事が起きたのは18日午前1時すぎで、火は約2時間後に消し止められましたが、父親(51)が背中や腕に火傷を負いました。意識はあり、命に別状はありません。この家には51歳の夫婦と15歳の息子の3人が暮らしていました。",
                "en": "According to police and fire authorities, the fire broke out just after 1 a.m. on the 18th and was extinguished about two hours later, but the father (51) suffered burns on his back and arms. He is conscious and his life is not in danger. Three people lived in the house: a couple in their 50s (both 51) and their 15-year-old son.",
                "literal": "据警方和消防称，火灾发生在18日凌晨1点多，约2小时后被扑灭，但父亲（51岁）背部、手臂被烧伤。有意识，生命无大碍。这家里住着51岁的夫妇和15岁的儿子共3人。",
                "grammar": "「〜によりますと」— 根据…。例：警察と消防によりますと（据警方和消防称）。\n「〜が、〜」— …但是…。例：消し止められましたが、火傷を負いました（被扑灭了，但受了烧伤）。\n「〜を負いました」— 受了…（伤）。例：火傷を負いました（受了烧伤）。",
                "vocab": [["消防", "しょうぼう", "消防"], ["消し止める", "けしとめる", "扑灭"], ["火傷", "やけど", "烧伤"], ["負う", "おう", "承受（伤）"], ["意識", "いしき", "意识"], ["別状", "べつじょう", "异常、大碍"]]
            },
            {
                "ja": "火災発生から間もない午前2時すぎ、息子が自ら交番を訪れ、名前を明かしたうえで「僕が火をつけました」と話しました。警察が任意同行して事情を聴いたところ、「両親を殺そうと思い、寝ているのを分かっていて自宅に火をつけた」と容疑を認めたため、逮捕に至りました。",
                "en": "Just after 2 a.m., shortly after the fire broke out, the son visited a police box on his own and, after revealing his name, said, \"I set the fire.\" When police brought him in voluntarily and heard his account, he admitted the suspicion, saying, \"I thought of killing my parents and set fire to the house knowing they were sleeping,\" which led to his arrest.",
                "literal": "火灾发生后不久的凌晨2点多，儿子自行来到派出所，报上姓名后说“是我放的火”。警察在任意同行听取情况后，他承认嫌疑称“想杀死父母，明知他们在睡觉仍给家里放了火”，因此被逮捕。",
                "grammar": "「〜間もない」— 不久、没过多久。例：火災発生から間もない（火灾发生后不久）。\n「〜たうえで」— 在…之后。例：名前を明かしたうえで（报上姓名之后）。\n「〜たところ、〜ため」— …之后，因为…。例：聴いたところ、認めたため、逮捕に至りました（听取后因其承认而逮捕）。",
                "vocab": [["交番", "こうばん", "派出所、岗亭"], ["自ら", "みずから", "亲自、自己"], ["明かす", "あかす", "说出、表明"], ["任意同行", "にんいどうこう", "任意同行（警方带问）"], ["事情", "じじょう", "情况、缘由"], ["容疑", "ようぎ", "嫌疑"]]
            },
            {
                "ja": "警察の調べに対して、息子は「日頃からお父さんが暴力を振ってくるのが嫌いで、ストレスがたまって自宅にガソリンをまいて火をつけました」と供述しているということです。警察は、少年の家庭内の状況などについても詳しく調べる方針です。",
                "en": "In response to police questioning, the son is said to have testified, \"I have long hated that my father uses violence against me, and the stress built up, so I poured gasoline in the house and set it on fire.\" Police plan to investigate in detail the situation in the boy's home as well.",
                "literal": "面对警方的调查，儿子供述称：“平时就讨厌父亲对我施暴，压力累积起来，于是往家里泼汽油放火。”警方也计划详细调查少年家庭内的情况等。",
                "grammar": "「〜に対して」— 对于…。例：警察の調べに対して（面对警方的调查）。\n「〜のが嫌いで」— 讨厌…。例：暴力を振ってくるのが嫌いで（讨厌施暴）。\n「〜ということです」— 据说…。例：供述しているということです（据说供述称）。",
                "vocab": [["調べ", "しらべ", "调查"], ["日頃", "ひごろ", "平时、平常"], ["暴力", "ぼうりょく", "暴力"], ["ストレス", "すとれす", "压力"], ["供述", "きょうじゅつ", "供述"], ["家庭内", "かていない", "家庭内部"]]
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