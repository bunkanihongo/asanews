#!/usr/bin/env python3
"""Bunkanihongo Daily News — 2026-08-30 (Sun) Edition"""
import json, os, subprocess, re
from sudachipy import tokenizer, dictionary

# === Setup ===
BASE = '/home/horse/.openclaw/workspace/asanews'
TODAY = '2026-08-30'
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
        "slug": "chiba-touhouoki-jishin-m48",
        "title": "千葉県東方沖で地震 M4.8 関東・東北で最大震度4",
        "subtitle": "from 千葉日報オンライン",
        "paras": [
            {
                "ja": "30日午前0時17分ごろ、千葉県東方沖を震源とする地震があった。最大震度4、地震の規模を示すマグニチュード（M）は4.8と推定される。震源の深さは約30キロ。銚子市、旭市、香取市で震度3を観測した。この地震による津波の心配はない。",
                "en": "Around 0:17 a.m. on the 30th, an earthquake occurred with its epicenter off the eastern coast of Chiba Prefecture. The maximum seismic intensity was 4, and the magnitude (M) indicating the scale of the earthquake is estimated at 4.8. The depth of the epicenter is about 30 kilometers. Seismic intensity 3 was observed in Choshi, Asahi, and Katori cities. There is no concern of a tsunami from this earthquake.",
                "literal": "30日凌晨0时17分左右，发生了以千叶县东方海域为震源的地震。最大震度4，表示地震规模的震级(M)推测为4.8。震源深度约30公里。在铫子市、旭市、香取市观测到震度3。此次地震没有海啸的担忧。",
                "grammar": "「〜ごろ」— 大约…时候。例：午前0時17分ごろ（凌晨0点17分左右）。\n「〜を震源とする」— 以…为震源。例：千葉県東方沖を震源とする地震（以千叶县东方海域为震源的地震）。\n「〜と推定される」— 被推测为…。例：Mは4.8と推定される（震级被推测为4.8）。",
                "vocab": [["震源", "しんげん", "震源"], ["最大震度", "さいだいしんど", "最大震度"], ["マグニチュード", "まぐにちゅーど", "震级"], ["震源の深さ", "しんげんのふかさ", "震源深度"], ["津波", "つなみ", "海啸"], ["観測", "かんそく", "观测"]]
            },
            {
                "ja": "地震が及んだ地域（震度1以上）の総人口は約1611.2万人。うち、地震による被害リスクが高いとされる65歳以上人口は25.8％の約415.7万人。千葉県内では震度3を観測したのは銚子市、旭市、香取市の3市で、震度2は東金市や山武市、成田市、佐倉市など広い範囲に及んだ。",
                "en": "The total population of the areas affected by the earthquake (with seismic intensity 1 or higher) is approximately 16.112 million. Of these, the population aged 65 and over, considered to be at high risk of earthquake damage, is about 4.157 million, or 25.8%. Within Chiba Prefecture, seismic intensity 3 was observed in the three cities of Choshi, Asahi, and Katori, while intensity 2 extended over a wide area including Togane, Sanmu, Narita, and Sakura cities.",
                "literal": "地震波及的地区（震度1以上）总人口约1611.2万人。其中，被认为地震受害风险高的65岁以上人口占25.8%，约415.7万人。千叶县内观测到震度3的是铫子市、旭市、香取市这3个市，震度2则波及东金市、山武市、成田市、佐仓市等广大范围。",
                "grammar": "「〜とされる」— 被认为…。例：被害リスクが高いとされる（被认为受害风险高的）。\n「〜うち」— 其中。例：うち、65歳以上人口は（其中，65岁以上人口）。\n「〜に及んだ」— 波及到…。例：広い範囲に及んだ（波及到广大范围）。",
                "vocab": [["及ぶ", "およぶ", "波及、涉及"], ["総人口", "そうじんこう", "总人口"], ["被害リスク", "ひがいリスク", "受害风险"], ["高齢者", "こうれいしゃ", "高龄者"], ["広い範囲", "ひろいはんい", "广大范围"], ["防災意識", "ぼうさいいしき", "防灾意识"]]
            }
        ]
    },
    {
        "slug": "hakajimai-kyuuzou-80sai",
        "title": "墓じまい急増 「娘に負担かけたくない」80歳女性の決断",
        "subtitle": "from HBC北海道放送",
        "paras": [
            {
                "ja": "北海道美唄市にある市営墓地。雨の中行われていたのは…お墓の撤去作業=「墓じまい」です。墓じまいをした加藤美代子さん（80）は「涙が出ます。やっぱり母の思い、夫の思いを考えると、ちょっと申し訳ない気持ちもあります」と語った。多死社会を迎える一方、墓を守る世代は減るばかり。新たに墓を建てるよりも、撤去のほうが多くなっているといいます。",
                "en": "At a municipal cemetery in Bibai City, Hokkaido. What was being carried out in the rain was the removal of a grave—what is called 'hakajimai' (closing a family grave). Miyoko Kato (80), who had her grave removed, said, 'I feel like crying. After all, thinking about my mother's feelings and my husband's feelings, I also feel a bit apologetic.' While society races toward a high-death era, the generation that maintains graves is only decreasing. It is said that removals now outnumber newly built graves.",
                "literal": "在北海道美唄市的市营墓地。在雨中进行的是…墓碑的撤除作业＝「墓じまい（关闭家族墓）」。进行了墓じまい的加藤美代子（80岁）说「要流泪了。毕竟想到母亲的心意、丈夫的心意，也有点抱歉的心情」。在迎来多死社会的同时，守护墓地的世代只增不减地减少。据说新建坟墓的反倒不如撤除的多。",
                "grammar": "「〜じまい」— …结束、…完（复合词）。例：墓じまい（关闭家族墓/处理坟墓）。\n「〜て（い）ます」的敬体用法。例：なっているといいます（听说正变得…）。\n「〜一方」— 一方面…另一方面…。例：多死社会を迎える一方（在迎来多死社会的同时）。",
                "vocab": [["墓じまい", "はかじまい", "关闭家族坟墓"], ["撤去", "てっきょ", "撤除、拆除"], ["申し訳ない", "もうしわけない", "非常抱歉"], ["多死社会", "たししゃかい", "多死社会"], ["世代", "せだい", "世代"], ["霊園", "れいえん", "陵园、墓园"]]
            },
            {
                "ja": "岩見沢に住む加藤さん（80）はおととい、美唄の墓地で墓じまいをしました。「本当にこういう風に自分でできたのは、何か凄く涙がでるほど嬉しいですね」と語ります。墓を建てたのは17年ほど前。夫が生前大切にしていた場所だけに、墓じまいには葛藤があったと言います。「お墓を建てた時に、夫は毎日のように来て、自分の亡くなった時にそこに入る墓を自分で見に来て、すごく思いがあったんです」。",
                "en": "Kato (80), who lives in Iwamizawa, closed her family grave at the cemetery in Bibai the day before yesterday. She says, 'Being able to do it myself in this way makes me incredibly happy, to the point of tears.' The grave was built about 17 years ago. Precisely because it was a place her husband treasured while alive, she says there was conflict in closing it. 'When the tombstone was built, my husband came almost every day, visiting to see for himself the grave he would enter when he died—it held so much meaning.'",
                "literal": "住在岩见泽的加藤（80岁）前天在美唄的墓地做了墓じまい。「真的能这样自己做到，是某种让人几欲落泪的高兴呢」她说道。坟墓建于是约17年前。正因为是丈夫生前非常珍惜的地方，据说墓じまい时曾有过纠结。「建这个墓时，丈夫几乎每天都来，自己死了以后要进去的墓亲自来看，有着非常深的心意」。",
                "grammar": "「〜ほど」— 到…的程度。例：涙がでるほど嬉しい（高兴到落泪的程度）。\n「〜だけに」— 正因为…（所以格外）。例：大切にしていた場所だけに（正因为是珍惜的地方）。\n「〜んです（んですね）」— 强调说明理由。例：すごく思いがあったんです（有着很深的心意）。",
                "vocab": [["おととい", "おととい", "前天"], ["生前", "せいぜん", "生前"], ["葛藤", "かっとう", "纠结、矛盾"], ["解体", "かいたい", "解体、拆除"], ["決断", "けつだん", "决断、决心"], ["負担", "ふたん", "负担"]]
            },
            {
                "ja": "加藤さんは3姉妹の長女な上、子どもも娘たちだけ。これまで、亡くなった夫の墓と、自分の両親から継いだお墓を守ってきましたが、そうした苦労や負担を娘や孫の世代にかけたくないと、墓じまいを決断しました。「ここにお参りに来るとほかに墓を解体している人が結構いまして、やっぱり子どもにもう墓を見てもらうのが大変な世の中になってきてるんじゃないかと思います」。石材店の社長によると、8割がた墓じまいのほうがメインになっているといいます。",
                "en": "Kato is the eldest of three sisters, and her children are only daughters. She had been maintaining her late husband's grave and the grave she inherited from her parents, but she decided on hakajimai in order not to pass such hardship and burden to her daughters and grandchildren. 'When I come here to visit, there are quite a few other people dismantling graves too—I think the world is becoming one where it's hard to ask children to keep looking after graves.' According to a stone shop president, hakajimai has become the main business, at about 80%.",
                "literal": "加藤是三姐妹的长女，而且孩子也只有女儿们。至今为止，她一直守护着亡夫的墓和从自己父母那里继承的墓，但为了不想把这样的辛苦和负担传给女儿和孙辈的世代，她决断了墓じまい。「来这儿参拜时，别处也有不少人正在拆墓，我觉得社会是不是正变成很难再让孩子看墓的时代」。据石材店社长称，大约8成已是墓じまい占主流。",
                "grammar": "「〜な上に」— 不仅…而且…。例：長女な上、子どもも娘たちだけ（不但是长女，孩子也只有女儿）。\n「〜てきました」— 一直…过来（持续到现在）。例：守ってきました（一直守护至今）。\n「〜かけたくない」— 不想让其承担…。例：負担をかけたくない（不想让其承担负担）。",
                "vocab": [["長女", "ちょうじょ", "长女"], ["継ぐ", "つぐ", "继承"], ["参拝/お参り", "おまいり", "参拜、扫墓"], ["石材店", "せきざいてん", "石材店"], ["8割がた", "はちわりがた", "大约八成"], ["メイン", "めいん", "主要、主流"]]
            }
        ]
    },
    {
        "slug": "koukyo-run-kinji-ron",
        "title": "「皇居ラン、そろそろ禁止?」 SNSで賛否 千代田区が現状を説明",
        "subtitle": "from 集英社オンライン",
        "paras": [
            {
                "ja": "SNSで東京・千代田区の皇居周辺を走る、いわゆる「皇居ラン」をめぐって議論が起きている。きっかけのひとつとなったのは、「皇居ラン、そろそろ禁止でいいのでは」というXの投稿だった。観光客や高齢者、子ども連れなど多くの歩行者が行き交うなか、ランナーとの接触を懸念する声が上がる一方、皇居ランに肯定的な意見も寄せられ、SNS上では賛否が分かれている。",
                "en": "A debate is erupting on social media over the so-called 'Imperial Palace run'—running around the Imperial Palace in Chiyoda Ward, Tokyo. One of the triggers was an X post saying, 'Isn't it about time we banned the Imperial Palace run?' Amid the many pedestrians coming and going, such as tourists, the elderly, and families with children, voices of concern about contact with runners have arisen on one hand, while positive opinions about the Imperial Palace run have also been submitted, and opinions on social media are divided.",
                "literal": "在SNS上，围绕在东京・千代田区皇居周边跑步的所谓「皇居跑」，正在引发讨论。契机之一是「皇居跑，差不多该禁止了吧」这样的X帖子。在游客、高龄者、带孩子的家庭等众多行人穿梭往来的情况下，一方面出现对与跑者接触的担忧之声，另一方面也收到了对皇居跑肯定的意见，SNS上赞成与反对呈对立。",
                "grammar": "「〜をめぐって」— 围绕…。例：皇居ランをめぐって議論（围绕皇居跑的讨论）。\n「〜一方」— 一方面…另一方面…。例：声が上がる一方、（一方面是担忧之声，另一方面…）。\n「〜ではないか」— 是不是…（提议/反问）。例：禁止でいいのでは（是不是禁止为好）。",
                "vocab": [["皇居", "こうきょ", "皇居"], ["賛否", "さんぴ", "赞成与反对"], ["行き交う", "いきかう", "往来穿梭"], ["懸念", "けねん", "担忧、疑虑"], ["肯定的", "こうていてき", "肯定的"], ["規制", "きせい", "管制、限制"]]
            },
            {
                "ja": "皇居ランに否定的な意見としては「皇居の歩道は、まず歩く人のためにあってほしい」「すれ違いざまに小声で『どけよ』『邪魔だよ』と言うランナーもおり、危ない以外にも理由はある」といった声が上がる一方、肯定的な意見もみられる。「『誰かが不快になるからとりあえず禁止する』を繰り返した結果、日本はとても生きづらい国になってしまった」という意見も寄せられている。皇居周辺は、観光地であると同時に、都内有数のランニングスポットとして長く親しまれてきた。",
                "en": "Among negative opinions about the Imperial Palace run, there are voices such as 'The Imperial Palace sidewalk should exist first and foremost for walkers' and 'There are also runners who, as they pass by, mutter 'Move it' or 'You're in the way' under their breath, so there are reasons other than danger.' On the other hand, positive opinions are also seen, such as 'As a result of repeating 'let's just ban it because someone finds it unpleasant,' Japan has become a very hard country to live in.' The area around the Imperial Palace, while being a tourist spot, has long been loved as one of the city's foremost running venues.",
                "literal": "关于对皇居跑否定的意见，有「皇居的人行道首先应该是为了让走路的人而存在的」「也有错身时小声说『让开』『碍事』的跑者，除了危险以外还有其他理由」这样的声音；另一方面，也能看到肯定的意见，也有「重复『因为有人不快就先禁止』的结果，日本变成了很难生活的国家」这样的意见被提交。皇居周边既是观光地，同时也是都内屈指可数的跑步地点，长久以来受到喜爱。",
                "grammar": "「〜ざまに」— 在…的一瞬间。例：すれ違いざまに（在擦身而过的时候）。\n「〜てほしい」— 希望（某人）…。例：歩く人のためにあってほしい（希望为步行者而存在）。\n「〜と同時に」— 与…同时。例：観光地であると同時に（既是观光地，同时…）。",
                "vocab": [["歩道", "ほどう", "人行道"], ["すれ違いざま", "すれちがいざま", "擦身而过的瞬间"], ["不快", "ふかい", "不快、不悦"], ["生きづらい", "いきづらい", "难以生活"], ["都内有数", "とないゆうすう", "都内屈指可数"], ["親しむ", "したしむ", "喜爱、亲近"]]
            },
            {
                "ja": "千代田区の担当者は「ランナーが周回している皇居周辺の道路は国道、都道、区道がありますが、こと千代田区にて管理している区道について、区民から危険な走行によって歩行者との接触があったなど歩行環境の改善を望む声をいただいており、安全性の確保は極めて重要であると認識しています」と述べた。一方、ランニングそのものを禁止する考えがあるかについては、平成25年6月に皇居周辺地域委員会で安全で快適な環境づくりに取り組むべく基本方針を策定したと説明した。",
                "en": "A Chiyoda Ward official stated, 'The roads around the Imperial Palace where runners circle include national highways, metropolitan roads, and ward roads, but regarding the ward roads managed by Chiyoda Ward, we have received voices from residents seeking improvement of the walking environment, such as reports of contact with pedestrians due to dangerous running, and we recognize that ensuring safety is extremely important.' Meanwhile, regarding whether there is any intention to ban running itself, he explained that in June 2013, the Imperial Palace surrounding area regional committee formulated a basic policy to work toward creating a safe and comfortable environment.",
                "literal": "千代田区的负责人说「跑者在环绕的皇居周边道路有国道、都道、区道，但就千代田区管理的区道而言，我们收到了区民希望改善步行环境的声音，例如有因危险行驶而与行人发生接触等情况，我们认识到确保安全性极其重要」。另一方面，关于是否有禁止跑步本身的想法，他说明称平成25年6月在皇居周边地域委员会为致力于打造安全舒适的环境策定了基本方针。",
                "grammar": "「〜こと（～について）」— 就…而言（限定话题）。例：こと千代田区にて管理している区道について（就千代田区管理的区道而言）。\n" 
                "「〜であり、認識しています」— 是…并认识到。例：極めて重要であると認識しています（认识到极其重要）。\n「〜べく」— 为（了）…。例：環境づくりに取り組むべく（为致力于环境建设）。",
                "vocab": [["周回", "しゅうかい", "环绕、绕圈"], ["国道/都道/区道", "こくどう/とどう/くどう", "国道/都道/区道"], ["歩行環境", "ほこうかんきょう", "步行环境"], ["安全性", "あんぜんせい", "安全性"], ["基本方針", "きほんほうしん", "基本方针"], ["策定", "さくてい", "制定"]]
            }
        ]
    },
    {
        "slug": "france-mousho-nihon-natsu-item",
        "title": "猛暑のフランスで日本の夏アイテムが大活躍 現地でも絶賛",
        "subtitle": "from Hint-Pot",
        "paras": [
            {
                "ja": "記録的な猛暑に見舞われているフランス。家庭用エアコンの普及率が低い現地では、暑さをしのぐ手段が限られているようです。南フランス・ピレネー山脈の麓で、フランス人の夫と愛娘と暮らす日本人YouTuberのMamiさん。自身のYouTubeチャンネルで、日本から持ち帰った夏アイテムが家族の暮らしを支える様子を公開しました。",
                "en": "France is being hit by record-breaking heat waves. In the country, where the penetration rate of home air conditioners is low, the means to escape the heat appear to be limited. Mami, a Japanese YouTuber living in the foothills of the Pyrenees in southern France with her French husband and beloved daughter, has published on her own YouTube channel how the summer items she brought back from Japan support their family's daily life.",
                "literal": "受到创纪录猛暑袭击的法国。在家庭用空调普及率低的当地，躲避炎热的手段似乎有限。与法国人丈夫和爱女一起生活在南法国・比利牛斯山麓的日本人YouTuber Mami小姐，在自己的YouTube频道上公开了从日本带回的夏季用品支撑一家生活的样子。",
                "grammar": "「〜に見舞われる」— 遭受…、遭遇…。例：猛暑に見舞われている（遭遇到猛暑）。\n「〜をしのぐ」— 忍受、躲避…。例：暑さをしのぐ（忍受酷暑）。\n「〜ようです」— 似乎…、好像…。例：限られているようです（似乎很有限）。",
                "vocab": [["猛暑", "もうしょ", "酷暑、猛暑"], ["普及率", "ふきゅうりつ", "普及率"], ["しのぐ", "しのぐ", "忍受、躲避"], ["山脈の麓", "さんみゃくのふもと", "山脉山麓"], ["持ち帰る", "もちかえる", "带回"], ["公開", "こうかい", "公开"]]
            },
            {
                "ja": "日本で買った冷感シートの快適さを気に入ったお父ちゃん。その良さを周囲にも広めています。気温39度を記録するほどの熱波が襲った日、仕事で南西部のトゥールーズを訪れたお父ちゃんは、日本で購入した冷感タイプの汗拭きシートを仕事の関係者にお裾分けしました。初めて目にする日本の便利グッズに、現地の人々は興味津々。実際に体を拭いてみると、さわやかな香りと冷たさに、次々と感激の声が上がったといいます。",
                "en": "Papa (the husband), who fell in love with the comfort of the cooling sheets bought in Japan, is spreading the word about their goodness to those around him. On a day when a heat wave hit with temperatures reaching 39 degrees, Papa, who was in Toulouse in the southwest for work, shared the cooling-type sweat-wiping sheets he had purchased in Japan with his colleagues. The locals, seeing Japanese convenience goods for the first time, were full of curiosity. When they actually wiped their bodies, voices of delight rose one after another at the refreshing fragrance and coolness, it is said.",
                "literal": "喜欢上在日本买的冷感贴片舒适度的「爸爸」（丈夫）。他也在向周围推广其好处。在气温高达39度的热浪来袭之日，因工作造访西南部图卢兹的爸爸，把在日本购买的冷感型擦汗巾分给了同事。对第一次见到的日本便利产品，当地人兴趣盎然。据说实际擦拭身体时，清爽的香气和凉爽让感激之声接连响起。",
                "grammar": "「〜を気に入った」— 喜欢上…。例：冷感シートの快適さを気に入った（喜欢上冷感贴片的舒适）。\n「〜ほど」— 达到…的程度。例：39度を記録するほど（达到记录39度的程度）。\n「〜てみると」— 实际做…一看。例：体を拭いてみると（实际擦拭身体一看）。",
                "vocab": [["冷感シート", "れいかんシート", "冷感贴片"], ["熱波", "ねっぱ", "热浪"], ["汗拭きシート", "あせふきシート", "擦汗巾"], ["お裾分け", "おすそわけ", "分送、分享"], ["興味津々", "きょうみしんしん", "兴趣盎然"], ["感激", "かんげき", "感动、感激"]]
            },
            {
                "ja": "Mamiさんが暮らす地域では、気温が45度を超える日もあるそう。エアコンがなく、扇風機に頼るしかない状況のなか、一家では日本で買った冷却ジェルシートが活躍しています。額に貼った娘のマカロンちゃんは、実に気持ち良さそうな表情。動画のコメント欄には「もちろんフランスにはこれは存在せず」「これが私たちの命綱」「このヨーロッパ猛暑を機に大量輸出すべき!」と、日本の技術力を称賛する声が寄せられています。",
                "en": "In the region where Mami lives, there are days when the temperature exceeds 45 degrees. In a situation where there is no air conditioner and they can only rely on a fan, the cooling gel sheets bought in Japan are proving useful for the family. Their daughter Macaron, with a sheet on her forehead, wears a truly comfortable-looking expression. In the video's comment section, voices praising Japanese technology have been submitted, such as 'Of course, this doesn't exist in France,' 'This is our lifeline,' and 'You should mass-export these amid this European heat wave!'",
                "literal": "在Mami生活的地区，据说也有气温超过45度的日子。在没有空调、只能依赖电风扇的状况下，一家中在日本买的冷却凝胶贴片正大显身手。额头上贴着贴片的女儿小马卡龙，露出着实看起来很舒服的表情。视频评论区里收到了「法国当然没有这东西」「这是我们的救命稻草」「趁这次欧洲酷暑应该大量出口!」等称赞日本技术力的声音。",
                "grammar": "「〜に頼るしかない」— 只能依靠…。例：扇風機に頼るしかない（只能依靠电扇）。\n「〜そう」— 看起来…（样态）。例：気持ち良さそうな表情（看起来很舒服的表情）。\n「〜を機に」— 以…为契机。例：この猛暑を機に（以这次酷暑为契机）。",
                "vocab": [["扇風機", "せんぷうき", "电扇"], ["冷却ジェル", "れいきゃくジェル", "冷却凝胶"], ["額", "ひたい", "额头"], ["命綱", "いのちづな", "救命稻草、生命线"], ["大量輸出すべき", "たいりょうゆしゅつすべき", "应该大量出口"], ["称賛", "しょうさん", "称赞"]]
            }
        ]
    }
]


processed = []
for art in articles:
    slug = art['slug']
    title = art['title']
    print(f"\n{'='*60}\n📰 {title}")

    paragraphs_out = []
    for i, p in enumerate(art['paras']):
        paragraphs_out.append({
            "id": f"p{i+1}",
            "ja": p['ja'],
            "en": p['en'],
            "literal": p['literal'],
            "grammar": p['grammar'],
            "vocab": p['vocab'],
            "words": tokenize_text(p['ja']),
            "audio": f"assets/audio/{slug}/p{i+1}.mp3"
        })

    reading = [{
        "id": slug,
        "title": title,
        "subtitle": art['subtitle'],
        "level": "中級",
        "length": len(art['paras']),
        "date": TODAY,
        "paragraphs": paragraphs_out
    }]

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
        # verify format types
        p0 = d[0]['paragraphs'][0]
        gt = type(p0['grammar']).__name__
        vt = type(p0['vocab']).__name__
        v0t = type(p0['vocab'][0]).__name__
        pc = len(d[0]['paragraphs'])
        audio_ok = True
        for i in range(pc):
            ap = f'{BASE}/assets/audio/{slug}/p{i+1}.mp3'
            if not os.path.exists(ap):
                audio_ok = False
        if audio_ok and gt == 'str' and vt == 'list' and v0t == 'list':
            ok += 1
            print(f"   ✅ {slug}: {pc} paragraphs, grammar={gt}, vocab={vt}/{v0t}, audio OK")
        else:
            print(f"   ⚠️ {slug}: type={gt}/{vt}/{v0t} audio_ok={audio_ok}")
print(f"\n{ok}/{len(processed)} articles verified")
