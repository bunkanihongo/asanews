/* ==========================================================================
   takanote 読解ルーム — v3（改良版）
   Interactive Japanese reading room with audio, translation, and grammar
   ========================================================================== */
(function () {
  'use strict';

  // ---- 状態 ----
  let currentData = null;
  let currentAudio = null;
  let currentParaIdx = -1;
  let isPlaying = false;
  let audioQueue = [];
  let isAutoMode = false;

  // ---- DOM 参照 ----
  let container, progressBar;

  // ======================================================================
  //  初期化
  // ======================================================================
  document.addEventListener('DOMContentLoaded', () => {
    container = document.getElementById('reading-room-container');
    if (!container) return;

    // CSS
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = '/asanews/assets/css/reading-room.css?v4';
    document.head.appendChild(link);

    // プログレスバー
    progressBar = document.createElement('div');
    progressBar.className = 'rr-progress-bar';
    document.body.appendChild(progressBar);

    // スクロール進捗
    window.addEventListener('scroll', updateProgress, { passive: true });

    // ルート（?read=slug パラメータ）
    const params = new URLSearchParams(window.location.search);
    const readingId = params.get('read');
    if (readingId) {
      loadReading(readingId);
    } else {
      renderList();
    }

    window.addEventListener('popstate', () => {
      const p = new URLSearchParams(window.location.search);
      const id = p.get('read');
      if (id) {
        loadReading(id);
      } else {
        renderList();
      }
    });
  });

  // ======================================================================
  //  プログレスバー
  // ======================================================================
  function updateProgress() {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? Math.min(scrollTop / docHeight * 100, 100) : 0;
    if (progressBar) progressBar.style.width = pct + '%';
  }

  // ======================================================================
  //  読解リスト
  // ======================================================================
                                                                                                                                                                                          const READING_LIST = [
    {
      id: 'taifuu15-obon-koutsuu',
      title: '来週は台風15号が東日本・北日本を直撃か お盆期間中の交通に影響のおそれ',
      kicker: '中級',
      desc: '',
      badge: '4段落',
      file: '/asanews/assets/readings/taifuu15-obon-koutsuu.json'
    },
    {
      id: 'kokuzai-hisyouji',
      title: '国税不祥事、「前例ない事態次々」に危機感 「パパ活」、情報漏えいも',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/kokuzai-hisyouji.json'
    },
    {
      id: 'kioxia-toshiba-junrieki',
      title: 'キオクシアHD株、前身の東芝にも巨額の恩恵 1Q純利益30倍の約4.5兆円',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/kioxia-toshiba-junrieki.json'
    },
    {
      id: 'usagi-shima-isei',
      title: '「ウサギの島」生態系に異変、観光客の過剰な餌やりで増えたイノシシがウサギを襲う',
      kicker: '中級',
      desc: '',
      badge: '4段落',
      file: '/asanews/assets/readings/usagi-shima-isei.json'
    },
    {
      id: 'penguin-torimaria',
      title: '八木山動物公園のフンボルトペンギン4羽、死因は「鳥マラリア」',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/penguin-torimaria.json'
    },
    {
      id: 'spacex-tsuki-shoutotsu',
      title: 'スペースXのロケット残骸が月面に衝突 衝突地点の画像を公開',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/spacex-tsuki-shoutotsu.json'
    },
    {
      id: 'josei-kenkyuusya-sien',
      title: '若手女性研究者を支援する新制度、大学に年間最大5000万円の補助金',
      kicker: '中級',
      desc: '',
      badge: '4段落',
      file: '/asanews/assets/readings/josei-kenkyuusya-sien.json'
    },
    {
      id: 'wow-shingou',
      title: '「Wow！信号」受信から50年、正体不明の電波を世界合同観測へ',
      kicker: '中級',
      desc: '',
      badge: '4段落',
      file: '/asanews/assets/readings/wow-shingou.json'
    },
    {
      id: 'seishoku-iryou-gairai',
      title: '都立病院で初の「生殖医療外来」開設 最新の不妊治療が受けられるように',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/seishoku-iryou-gairai.json'
    },
    {
      id: 'taifuu13-okinawa-amami-sekken',
      title: '台風13号、沖縄・奄美に最接近 線状降水帯発生のおそれ 長時間の暴風・高波に警戒',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/taifuu13-okinawa-amami-sekken.json'
    },
    {
      id: 'hinanjo-kakusa-kumamoto-jishin',
      title: '避難所めぐる“格差” 男女同室で「着替えられない」 雑魚寝続く被災地 専門家「標準化されていない」',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/hinanjo-kakusa-kumamoto-jishin.json'
    },
    {
      id: 'aeon-kumamoto-bakuhatsu-lpg',
      title: 'イオンモール熊本の爆発事故 LPガス供給会社「調査に全面的に協力」 経産省「LPガス爆発の可能性高い」',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/aeon-kumamoto-bakuhatsu-lpg.json'
    },
    {
      id: 'zaimushou-jinji-iten-haran',
      title: 'エース級の財務官僚が異例転出へ 官邸幹部「協力的でなかったから」 消費減税巡り対立か',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/zaimushou-jinji-iten-haran.json'
    },
    {
      id: 'taiyou-hyoumen-saikou-kaizoudo',
      title: '太陽表面を過去最高の解像度で観測、磁気にまつわる謎が明らかに 米研究チーム',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/taiyou-hyoumen-saikou-kaizoudo.json'
    },
    {
      id: 'sanseitou-kamiya-gusaku',
      title: '参政党の神谷代表、食料品の消費減税「天下の愚策」と批判 「一律減税でないと後押しにならない」',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/sanseitou-kamiya-gusaku.json'
    },
    {
      id: 'reiwa-inochi-no-tou-meishou',
      title: 'れいわ新選組が「いのちの党」に党名変更 “脱・山本太郎”へ 山本譲司新代表のもと臨時総会',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/reiwa-inochi-no-tou-meishou.json'
    },
    {
      id: 'mukikei-karikiyaku-4nin',
      title: '無期刑の仮釈放、2025年は「わずか4人」 2024年は32人が獄中死 「終身刑化」の傾向続く',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/mukikei-karikiyaku-4nin.json'
    },
    {
      id: 'shakaihosho-zaigen-5chouen',
      title: '日本の社会保障、岐路に 消費減税で財源5兆円の穴 手当てする具体策見えず',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/shakaihosho-zaigen-5chouen.json'
    },
    {
      id: 'shiroi-zarigani-tenji',
      title: '白いザリガニ発見 遺伝的変異の可能性 親子が捕まえ岡山の科学館に寄贈 「赤青白」3色そろう',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/shiroi-zarigani-tenji.json'
    },
    {
      id: 'taifuu13-okinawa-sekken',
      title: '台風13号、7日昼過ぎに沖縄本島へ最接近 暴風や高波に厳重警戒',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/taifuu13-okinawa-sekken.json'
    },
    {
      id: 'shokuhin-zei-1-paasento',
      title: '飲食料品消費税1％へ、外食に「割高感」も 農家にも打撃の恐れ 政府、対策を検討',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/shokuhin-zei-1-paasento.json'
    },
    {
      id: 'genbaku-touka-81-nen',
      title: '原爆投下81年、高まる核リスク 被爆者減る中、広島から平和訴え',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/genbaku-touka-81-nen.json'
    },
    {
      id: 'spacex-rocket-tsuki-shoutotsu',
      title: 'スペースXのロケット残骸、月面に衝突か ファルコン9の上段',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/spacex-rocket-tsuki-shoutotsu.json'
    },
    {
      id: 'shime-ramen-yokkyuu-no-genin',
      title: '飲酒後の「締めのラーメン欲」の原因は？ 脳の錯覚と真実【医師解説】',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/shime-ramen-yokkyuu-no-genin.json'
    },
    {
      id: 'higashihiroshima-zenkai-kaji',
      title: '「家の中から叫び声」焼け跡から4人の遺体 家族4人全員死亡か 東広島市の住宅火災',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/higashihiroshima-zenkai-kaji.json'
    },
    {
      id: 'nippon-seishi-hachioji-koujou',
      title: '9人が犠牲の日本製紙八代工場、社長ら初会見 工場長「正直何もできなかった」',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/nippon-seishi-hachioji-koujou.json'
    },
    {
      id: 'mercari-nashi-tenbai-giwaku',
      title: 'メルカリ、梨の転売疑惑を否定「誹謗中傷はやめて」 生産者を現地確認',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/mercari-nashi-tenbai-giwaku.json'
    },
    {
      id: 'neko-ga-pan-wo-koneru',
      title: 'なぜ猫は「パンをこねる」のか？ 前足で飼い主をもむ習性を生物学者が解説',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/neko-ga-pan-wo-koneru.json'
    },
    {
      id: 'tai-de-shinshu-kyouryuu',
      title: '体長27m・体重27tの新種恐竜をタイで発見 東南アジア最大か、なぜ巨大に進化できた？',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/tai-de-shinshu-kyouryuu.json'
    },
    {
      id: 'takeda-shinichi-tenkin',
      title: '武田真一アナ、NHK時代の5度の転勤を回想 「会社が一方的に働く場所を決める時代」に転機',
      kicker: '中級',
      desc: '',
      badge: '4段落',
      file: '/asanews/assets/readings/takeda-shinichi-tenkin.json'
    },
    {
      id: 'aeon-kumamoto-sainyuukan',
      title: 'イオンモール熊本、避難後になぜ再入館？ 生存した従業員らの証言が浮かび上がらせる実態',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/aeon-kumamoto-sainyuukan.json'
    },
    {
      id: 'keikan-happa-kawachinagano',
      title: '警察官が刃物持った男に発砲、男は搬送先で死亡 大阪・河内長野市',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/keikan-happa-kawachinagano.json'
    },
    {
      id: 'ichou-54pon-kareru',
      title: '名物イチョウ54本が一斉に枯れる 原因は伐採時の除草剤、根がつながっていた 東京・町田',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/ichou-54pon-kareru.json'
    },
    {
      id: 'kome-nouka-akaji',
      title: '「とんでもない赤字」コメ作りやめる農家も JA福井県が概算金示せない中、ハナエチゼンの収穫始まる',
      kicker: '中級',
      desc: '',
      badge: '4段落',
      file: '/asanews/assets/readings/kome-nouka-akaji.json'
    },
    {
      id: 'joshi-kousei-kyouhaku',
      title: '「会わんかったら親や学校に言うぞ」女子高校生を脅迫しホテルへ…44歳男を逮捕 大阪府警',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/joshi-kousei-kyouhaku.json'
    },
    {
      id: 'ny-dow-54000-dai',
      title: 'NYダウ900ドル超高、連日の最高値 中東情勢の緊張緩和に期待',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/ny-dow-54000-dai.json'
    },
    {
      id: 'kumamoto-jishin-isshuukan',
      title: '熊本地震1週間、避難所に7538人・断水4万4380戸 連日の猛暑で被災者の心身の不調懸念',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/kumamoto-jishin-isshuukan.json'
    },
    {
      id: 'ion-bakuhatsu-wedding-dress',
      title: 'イオンモール爆発で犠牲となった妻、告別式にウェディングドレス飾った夫「生前に着させてあげたかった」',
      kicker: '中級',
      desc: '',
      badge: '4段落',
      file: '/asanews/assets/readings/ion-bakuhatsu-wedding-dress.json'
    },
    {
      id: 'fukuoka-kengikai-daisansha',
      title: '福岡県議会が第三者委設置へ 正副議長ポスト巡る金銭授受疑惑、批判高まり方針転換',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/fukuoka-kengikai-daisansha.json'
    },
    {
      id: 'higashino-keigo-eien-no-kioku',
      title: '東野圭吾さん最新作「永遠の記憶」発売 涙を流しながら本を受け取るファンの姿も',
      kicker: '中級',
      desc: '',
      badge: '4段落',
      file: '/asanews/assets/readings/higashino-keigo-eien-no-kioku.json'
    },
    {
      id: 'habita-kanai-modosu-siji',
      title: 'イオン熊本爆発 死亡の従業員2人「館内へ戻るよう指示」と運営会社が認める',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/habita-kanai-modosu-siji.json'
    },
    {
      id: 'jishingumo-gosoku-chuui',
      title: '地震と雲を関係付ける誤情報に注意 命を守るための「正しい防災」とは',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/jishingumo-gosoku-chuui.json'
    },
    {
      id: 'kihara-nijuu-saigai-mousho',
      title: '木原官房長官「今年の猛暑、まさに二重の災害」 災害関連死の抑制へ対策',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/kihara-nijuu-saigai-mousho.json'
    },
    {
      id: 'takaichi-shijiritsu-teika',
      title: '高市内閣の支持率59.2% 先月調査から6.7ポイント下落 JNN世論調査',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/takaichi-shijiritsu-teika.json'
    },
    {
      id: 'kuwaki-shiho-zen-ei-v',
      title: '桑木志帆が涙の日本勢7人目メジャーV 渋野日向子に続く全英制覇',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/kuwaki-shiho-zen-ei-v.json'
    },
    {
      id: 'docomo-no-ginkou-sidou',
      title: '「ドコモの銀行」きょう始動 「d NEOBANK」消滅、最大4.5%還元',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/docomo-no-ginkou-sidou.json'
    },
    {
      id: 'iphone-shin-seihin-hinusu',
      title: '今年のiPhone新製品、発売直後から品薄になる可能性 クックCEOが警告',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/iphone-shin-seihin-hinusu.json'
    },
    {
      id: 'perseus-ryuuseigun-mikoro',
      title: '1時間に最大100個の流星 2026年最大の天体ショー「ペルセウス座流星群」',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/perseus-ryuuseigun-mikoro.json'
    },
    {
      id: 'windows-hotel-wifi-keikoku',
      title: 'Windowsユーザーは「ホテルのWi-Fiは使うな」 マイクロソフトが緊急警告',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/windows-hotel-wifi-keikoku.json'
    },
    {
      id: 'windows11-8gb-memory',
      title: 'Windows 11は8GBメモリでも快適に使えるようになる？ 品質向上への中間報告',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/windows11-8gb-memory.json'
    },
    {
      id: 'moushobi-kumamoto-40do',
      title: '2日は300超の地点で猛暑日か 週明けは熊本で統計史上初の40℃',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/moushobi-kumamoto-40do.json'
    },
    {
      id: 'risai-shoumeisho-satsuei',
      title: '熊本地震5日目 「片付ける前に撮影を」罹災証明書申請の注意点',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/risai-shoumeisho-satsuei.json'
    },
    {
      id: 'en-kyuushin-nichibei-kainyuu',
      title: '円急伸、日米で協調介入か 円安是正へ週明け方針表明',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/en-kyuushin-nichibei-kainyuu.json'
    },
    {
      id: 'nisai-danji-yukuefumei',
      title: '祖母の自宅に帰省中 京都府宇治市の2歳の男の子が行方不明 岡山・矢掛町',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/nisai-danji-yukuefumei.json'
    },
    {
      id: 'puruja-san-setsunai-shibou',
      title: '著名登山家ニルマル・プルジャさん死亡確認 ブロードピークで雪崩遭遇',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/puruja-san-setsunai-shibou.json'
    },
    {
      id: 'dena-maki-baachan-homerun',
      title: 'DeNA・牧「ばあちゃんに打たせてもらった」 慶弔休暇明けに祖母へ捧げる本塁打',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/dena-maki-baachan-homerun.json'
    },
    {
      id: 'bare-danshi-america-sekihai',
      title: 'バレー男子 決勝ならず…米にフルセット惜敗 スロベニアとの3位決定戦へ',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/bare-danshi-america-sekihai.json'
    },
    {
      id: 'goto-maki-tif-40sai',
      title: '後藤真希 TIFで自虐あいさつ「40歳おばさん」 LOVEマシーンなど5曲披露',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/goto-maki-tif-40sai.json'
    },
    {
      id: 'roshia-kiu-daikibo-kougeki',
      title: 'ロシアがウクライナ・キーウに大規模攻撃 9人死亡、30人以上けが',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/roshia-kiu-daikibo-kougeki.json'
    },
    {
      id: 'ishiba-syouhizei-hihan',
      title: '石破前首相 高市首相の「消費税率1％」方針を批判 「財源示さなければ無責任」',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/ishiba-syouhizei-hihan.json'
    },
    {
      id: 'kumamoto-yure-saidaichi-2437gal',
      title: '熊本地震の揺れ 10年前の地震を上回る 最大2400ガル超',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kumamoto-yure-saidaichi-2437gal.json'
    },
    {
      id: 'hamas-busou-kaijo-goui',
      title: 'ハマス 武装解除で合意と幹部が明かす ガザ撤退も含む',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/hamas-busou-kaijo-goui.json'
    },
    {
      id: 'aeon-kumamoto-bakuhatsu-haha',
      title: 'イオン爆発で娘失った母親 「金庫にお金を入れないと」と言い残し戻る',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/aeon-kumamoto-bakuhatsu-haha.json'
    },
    {
      id: 'kurashiki-sasareru-sibou',
      title: '倉敷市で男性が刺され死亡 おいの男を殺人容疑で確保',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kurashiki-sasareru-sibou.json'
    },
    {
      id: 'kitami-tamanegi-konbena',
      title: 'たまねぎ処理工場で男性がコンテナに挟まれ死亡 北海道・北見市',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kitami-tamanegi-konbena.json'
    },
    {
      id: 'henoko-kousu-henkou-chusen',
      title: '死亡した高校2年の生徒 辺野古コースの変更希望も抽選で外れる',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/henoko-kousu-henkou-chusen.json'
    },
    {
      id: 'bado-shida-igarashi-kaisyou',
      title: 'バドミントン 志田千陽・五十嵐有紗ペアが解消 日本代表も辞退',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/bado-shida-igarashi-kaisyou.json'
    },
    {
      id: 'wagaya-sugiyama-nyuuin',
      title: 'お笑いトリオ「我が家」杉山裕之 ギラン・バレー症候群の疑いで入院',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/wagaya-sugiyama-nyuuin.json'
    },
    {
      id: 'syouhizei-1p-hyoumei',
      title: '高市首相 食料品の消費税率「1％」を正式表明 実質ゼロへ',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/syouhizei-1p-hyoumei.json'
    },
    {
      id: 'taifuu13-dolphin-mouretsu',
      title: '台風13号「ドルフィン」猛烈な勢力で北上 九州・沖縄に接近か',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/taifuu13-dolphin-mouretsu.json'
    },
    {
      id: 'saichou-katsudansou-m8',
      title: '「南海トラフだけではない」1000年以上沈黙する日本最長の活断層',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/saichou-katsudansou-m8.json'
    },
    {
      id: 'kumamoto-jishin-hisaisha-koe',
      title: '「シャワーが泥水」熊本地震 被災者の生の声と求める支援',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kumamoto-jishin-hisaisha-koe.json'
    },
    {
      id: 'matsunoya-mama-ouen-natsu',
      title: '松のや「ママ応援企画」に批判 謝罪し「夏休み企画」に変更',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/matsunoya-mama-ouen-natsu.json'
    },
    {
      id: 'fukuoka-kengikai-kingin',
      title: '福岡県議会「カツアゲ問題」 告発議員を支える重鎮とフジ人気アナ',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/fukuoka-kengikai-kingin.json'
    },
    {
      id: 'juuminzei-hikaze-hikaku',
      title: '住民税非課税の目安は年収110万円に 国の一律給付なし',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/juuminzei-hikaze-hikaku.json'
    },
    {
      id: 'doru157en-kawase-kainyu',
      title: 'ドル円 一時157円台に急騰 政府・日銀が為替介入か',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/doru157en-kawase-kainyu.json'
    },
    {
      id: 'souri-kumamoto-nyuuri',
      title: '首相 8月3日にも熊本入り 被災状況を把握へ',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/souri-kumamoto-nyuuri.json'
    },
    {
      id: 'senbotsusha-izoku-50nen-gosiharu',
      title: '戦没者遺族への特別弔慰金 50年間誤って支給 総額180万円',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/senbotsusha-izoku-50nen-gosiharu.json'
    },
    {
      id: 'onward-aeon-kumamoto-shain',
      title: 'オンワードが従業員の死亡を発表 イオンモール熊本',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/onward-aeon-kumamoto-shain.json'
    },
    {
      id: 'syouhizei-1p-hyoumei',
      title: '高市首相 食料品の消費税率「1％」を正式表明 実質ゼロへ',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/syouhizei-1p-hyoumei.json'
    },
    {
      id: 'taifuu13-dolphin-mouretsu',
      title: '台風13号「ドルフィン」猛烈な勢力で北上 九州・沖縄に接近か',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/taifuu13-dolphin-mouretsu.json'
    },
    {
      id: 'saichou-katsudansou-m8',
      title: '「南海トラフだけではない」1000年以上沈黙する日本最長の活断層',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/saichou-katsudansou-m8.json'
    },
    {
      id: 'kumamoto-jishin-hisaisha-koe',
      title: '「シャワーが泥水」熊本地震 被災者の生の声と求める支援',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kumamoto-jishin-hisaisha-koe.json'
    },
    {
      id: 'matsunoya-mama-ouen-natsu',
      title: '松のや「ママ応援企画」に批判 謝罪し「夏休み企画」に変更',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/matsunoya-mama-ouen-natsu.json'
    },
    {
      id: 'fukuoka-kengikai-kingin',
      title: '福岡県議会「カツアゲ問題」 告発議員を支える重鎮とフジ人気アナ',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/fukuoka-kengikai-kingin.json'
    },
    {
      id: 'juuminzei-hikaze-hikaku',
      title: '住民税非課税の目安は年収110万円に 国の一律給付なし',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/juuminzei-hikaze-hikaku.json'
    },
    {
      id: 'doru157en-kawase-kainyu',
      title: 'ドル円 一時157円台に急騰 政府・日銀が為替介入か',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/doru157en-kawase-kainyu.json'
    },
    {
      id: 'souri-kumamoto-nyuuri',
      title: '首相 8月3日にも熊本入り 被災状況を把握へ',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/souri-kumamoto-nyuuri.json'
    },
    {
      id: 'senbotsusha-izoku-50nen-gosiharu',
      title: '戦没者遺族への特別弔慰金 50年間誤って支給 総額180万円',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/senbotsusha-izoku-50nen-gosiharu.json'
    },
    {
      id: 'onward-aeon-kumamoto-shain',
      title: 'オンワードが従業員の死亡を発表 イオンモール熊本',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/onward-aeon-kumamoto-shain.json'
    },
    {
      id: 'takaichi-shijiritsu-bunseki',
      title: '高市首相の支持率急落 原因は「説明不足」と物価高 各社調査',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/takaichi-shijiritsu-bunseki.json'
    },
    {
      id: 'aeon-kumamoto-tuma-onshin',
      title: 'イオンモールで働く妻から「そっちは大丈夫？」 その後途絶えた音信',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/aeon-kumamoto-tuma-onshin.json'
    },
    {
      id: 'fukuoka-kengikai-kenkin',
      title: '福岡県議会で金銭授受疑惑 自民県議団が大きく揺れる',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/fukuoka-kengikai-kenkin.json'
    },
    {
      id: 'kome-neage-sinn-hannin',
      title: 'コメの価格を吊り上げている「真犯人」 JAや農家ではなかった',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kome-neage-sinn-hannin.json'
    },
    {
      id: 'taifuu13-gou-mouretsu-0730',
      title: '台風13号「ドルフィン」きょう午後にも「猛烈な」勢力 910hPa予想',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/taifuu13-gou-mouretsu-0730.json'
    },
    {
      id: 'taiimee-hoikushi-kyanseru',
      title: 'タイミー保育士が直前キャンセルで賃金ゼロ 労基署が是正指導',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/taiimee-hoikushi-kyanseru.json'
    },
    {
      id: 'volley-danshi-junkesshou',
      title: 'バレー男子日本代表が中国に逆転勝利 準決勝進出13連勝',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/volley-danshi-junkesshou.json'
    },
    {
      id: 'iwaya-takeshi-kugen-renpatsu',
      title: '岩屋毅前外相が高市政権に苦言 国旗損壊罪や副首都法に疑問',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/iwaya-takeshi-kugen-renpatsu.json'
    },
    {
      id: 'seikatsudouro-houriteisoku-30',
      title: '生活道路の法定速度30キロに 9月から60キロで一発免停',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/seikatsudouro-houriteisoku-30.json'
    },
    {
      id: 'aeon-kumamoto-bakuhatsu-kaiken',
      title: 'イオン社長「爆発、想定しきれず」 熊本震度7の事故で謝罪',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/aeon-kumamoto-bakuhatsu-kaiken.json'
    },
    {
      id: 'kumamoto-m71-shindo7',
      title: '熊本県で最大震度7 M7.1の地震 広範囲で被害',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/kumamoto-m71-shindo7.json'
    },
    {
      id: 'kumamoto-seihu-zien',
      title: '高市首相「人命第一で対応」 政府が被災地支援を急ぐ',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kumamoto-seihu-zien.json'
    },
    {
      id: 'kumamoto-kisyatu-rikisya',
      title: '熊本で震度7の地震 熱中症にも警戒を',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kumamoto-kisyatu-rikisya.json'
    },
    {
      id: 'byd-karukei-ev',
      title: '中国BYDが日本で軽EV「ラッコ」 実質100万円台',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/byd-karukei-ev.json'
    },
    {
      id: 'kokuren-futsu-hatugen-taiseki',
      title: '国連安保理で仏発言中に米代表団が退席',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kokuren-futsu-hatugen-taiseki.json'
    },
    {
      id: 'higashino-keigo-daichogan',
      title: '作家・東野圭吾さん 大腸がんのため死去 68歳',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/higashino-keigo-daichogan.json'
    },
    {
      id: 'sekai-ijou-kishou',
      title: '欧州で史上最悪の山火事 世界で異常気象が続出',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/sekai-ijou-kishou.json'
    },
    {
      id: 'natsu-kaisoku-nouhizyou',
      title: '夏の快眠 専門家がすすめ「脳を冷やす」方法',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/natsu-kaisoku-nouhizyou.json'
    },
    {
      id: 'kodomo-sns-nenrei-seigen',
      title: '子どものSNS利用に一律年齢制限 政府が検討へ',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kodomo-sns-nenrei-seigen.json'
    },
    {
      id: 'm-kunren-tairan-kougeki',
      title: '米大統領 イランと友好的協議続けるも決裂なら攻撃も',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/m-kunren-tairan-kougeki.json'
    },
    {
      id: 'apple-shijyou-syuri',
      title: 'Apple時価総額 世界首位に返り咲き 株価過去最高',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/apple-shijyou-syuri.json'
    },
    {
      id: 'shokuhin-syouhizei-1p',
      title: '食料品の消費税1％ 政府・与党が方針固める 首相が30日にも指示へ',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/shokuhin-syouhizei-1p.json'
    },
    {
      id: 'taifuu13-gou-mouretsu',
      title: '台風13号「ドルフィン」最強ランク「猛烈な」勢力へ 中心気圧915hPa',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/taifuu13-gou-mouretsu.json'
    },
    {
      id: 'henoko-doushisha-sousaku',
      title: '辺野古転覆事故 海上保安当局が同志社国際高校を家宅捜索',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/henoko-doushisha-sousaku.json'
    },
    {
      id: 'trump-frb-risage',
      title: 'トランプ氏 FRBに利下げを要求 ウォーシュ議長は「素晴らしい」',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/trump-frb-risage.json'
    },
    {
      id: 'rosia-gun-teiin-zou',
      title: 'ロシア軍の定員242万6000人に引き上げ プーチン大統領が署名',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/rosia-gun-teiin-zou.json'
    },
    {
      id: 'ukuraina-rosia-douin',
      title: 'ウクライナ大統領「ロシアが30万〜50万人の動員を計画」',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/ukuraina-rosia-douin.json'
    },
    {
      id: 'reomichan-itaiken',
      title: '「頑張ったね、おうちに帰ろうね」 行方不明の5歳男児・嶺臣ちゃん 父親が最後の対面語る',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/reomichan-itaiken.json'
    },
    {
      id: 'kiritani-hiroto-gan',
      title: '桐谷広人さん 前立腺と大腸に「2つのがん」 闘病と株主優待の日々',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kiritani-hiroto-gan.json'
    },
    {
      id: 'chugoku-teppomizu',
      title: '中国のキャンプ場で「鉄砲水」 テントが次々濁流に 10人死亡',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/chugoku-teppomizu.json'
    },
    {
      id: 'takaichi-shijiritsu-57',
      title: '高市内閣支持が急落57％ 首相の説明「不十分」62％',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/takaichi-shijiritsu-57.json'
    },
    {
      id: 'josei-tennou-younin-81',
      title: '女性天皇容認に賛成81％ 共同通信世論調査',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/josei-tennou-younin-81.json'
    },
    {
      id: 'iran-houfuku-kyuushi',
      title: 'イランが報復休止 米軍の攻撃停止受け',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/iran-houfuku-kyuushi.json'
    },
    {
      id: 'toyota-6nen-sekaiichi',
      title: '豊田章男の5年前の警告は正しかった トヨタが6年連続世界一',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/toyota-6nen-sekaiichi.json'
    },
    {
      id: 'funai-denki-hasan',
      title: '船井電機が破産 社員が見た「いちばん長い日」',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/funai-denki-hasan.json'
    },
    {
      id: 'squeeze-ryuukou',
      title: '「スクイーズ」なぜ流行？ 専門家が明かす4つの理由',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/squeeze-ryuukou.json'
    },
    {
      id: 'fujisan-taiwan-josei',
      title: '富士登山中の台湾女性 山頂で突然意識失う',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/fujisan-taiwan-josei.json'
    },
    {
      id: 'taifuu-nettaiteikiatsu',
      title: '新たな熱帯低気圧が台風に発達か 今後の進路に注意',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/taifuu-nettaiteikiatsu.json'
    },
    {
      id: 'takaichi-tsuyoki-kokkai',
      title: '高市首相 強気貫く国会運営 自民重鎮「いつかしっぺ返し」',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/takaichi-tsuyoki-kokkai.json'
    },
    {
      id: 'topnews-pickup-0727',
      title: '今日の注目ニュースピックアップ（7月27日）',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/topnews-pickup-0727.json'
    },
    {
      id: 'fukutokyo-kakuchi-meigori',
      title: '副首都に大阪・福岡・愛知が名乗り 北海道・宮城も意欲',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/fukutokyo-kakuchi-meigori.json'
    },
    {
      id: 'shinagawa-mansion-kaji',
      title: '品川区のマンションで火事 ソーラーパネル充電中に出火か',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/shinagawa-mansion-kaji.json'
    },
    {
      id: 'okayadokari-4163-taiho',
      title: '天然記念物オカヤドカリ4163匹を発送 中国籍の男3人逮捕',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/okayadokari-4163-taiho.json'
    },
    {
      id: 'chugokujin-kankoku-hanchuu',
      title: '習近平「日本は危険」で中国人が韓国へ 反中感情が爆発',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/chugokujin-kankoku-hanchuu.json'
    },
    {
      id: 'ukuraina-dorone-taikoku',
      title: 'ウクライナが「ドローン大国」に変貌 生産量は年間300万〜600万機',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/ukuraina-dorone-taikoku.json'
    },
    {
      id: 'ozumo-atsumifuji-360man',
      title: '横綱撃破で360万円 大相撲・熱海富士が懸賞60本を獲得',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/ozumo-atsumifuji-360man.json'
    },
    {
      id: 'maeda-daizen-premier',
      title: '前田大然がプレミアリーグへ イプスウィッチが獲得発表',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/maeda-daizen-premier.json'
    },
    {
      id: 'takaichi-shijiritsu-kokkarinen',
      title: '混迷国会で「高市離れ」の兆候 期待と違う市民の声',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/takaichi-shijiritsu-kokkarinen.json'
    },
    {
      id: 'okamoto-kouzou-soushiki',
      title: 'レバノンで岡本公三元被告の葬儀 英雄視する声も',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/okamoto-kouzou-soushiki.json'
    },
    {
      id: 'fukutokyo-kakuchi-meigori',
      title: '副首都に大阪・福岡・愛知が名乗り 北海道・宮城も意欲',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/fukutokyo-kakuchi-meigori.json'
    },
    {
      id: 'shinagawa-mansion-kaji',
      title: '品川区のマンションで火事 ソーラーパネル充電中に出火か',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/shinagawa-mansion-kaji.json'
    },
    {
      id: 'okayadokari-4163-taiho',
      title: '天然記念物オカヤドカリ4163匹を発送 中国籍の男3人逮捕',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/okayadokari-4163-taiho.json'
    },
    {
      id: 'chugokujin-kankoku-hanchuu',
      title: '習近平「日本は危険」で中国人が韓国へ 反中感情が爆発',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/chugokujin-kankoku-hanchuu.json'
    },
    {
      id: 'ukuraina-dorone-taikoku',
      title: 'ウクライナが「ドローン大国」に変貌 生産量は年間300万〜600万機',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/ukuraina-dorone-taikoku.json'
    },
    {
      id: 'ozumo-atsumifuji-360man',
      title: '横綱撃破で360万円 大相撲・熱海富士が懸賞60本を獲得',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/ozumo-atsumifuji-360man.json'
    },
    {
      id: 'maeda-daizen-premier',
      title: '前田大然がプレミアリーグへ イプスウィッチが獲得発表',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/maeda-daizen-premier.json'
    },
    {
      id: 'takaichi-shijiritsu-kokkarinen',
      title: '混迷国会で「高市離れ」の兆候 期待と違う市民の声',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/takaichi-shijiritsu-kokkarinen.json'
    },
    {
      id: 'okamoto-kouzou-soushiki',
      title: 'レバノンで岡本公三元被告の葬儀 英雄視する声も',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/okamoto-kouzou-soushiki.json'
    },
    {
      id: 'fukushuto-houritsu-seiritsu',
      title: '「副首都構想」具体化に向けた法律が可決・成立',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/fukushuto-houritsu-seiritsu.json'
    },
    {
      id: 'taifuu12-gou-hattatsu',
      title: '台風12号「ノウル」南シナ海で発達 強い勢力で中国華南に上陸へ',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/taifuu12-gou-hattatsu.json'
    },
    {
      id: 'shijiritsu-kyuuraku-takaichi',
      title: '支持率急落を招く高市首相の「人間不信」 その原点となった地元との確執',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/shijiritsu-kyuuraku-takaichi.json'
    },
    {
      id: 'nihonka-suru-chugoku',
      title: '「日本化」する中国 2050年の1人当たりGDPは米国の4分の1に',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/nihonka-suru-chugoku.json'
    },
    {
      id: 'syouhizei-genzei-seiken-owaru',
      title: '消費減税見送りなら「政権終わる」 支持率下落で官邸に危機感',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/syouhizei-genzei-seiken-owaru.json'
    },
    {
      id: 'ukuraina-dorone-kougeki',
      title: 'ウクライナ軍がロシアの通販倉庫にドローン攻撃 物流網への攻撃強める',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/ukuraina-dorone-kougeki.json'
    },
    {
      id: 'ro-gun-kitahouryou-ryoukuu',
      title: '露軍の航空機 北方領土を領空侵犯 日本が厳重抗議',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/ro-gun-kitahouryou-ryoukuu.json'
    },
    {
      id: 'gaikokujin-eijyu-genkaku',
      title: '政府が外国人の永住許可要件を厳格化へ 納税義務違反で取消も',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/gaikokujin-eijyu-genkaku.json'
    },
    {
      id: 'isha-haikibutsu-iho-taiho',
      title: '医師の男を廃棄物処理法違反疑いで逮捕 麻酔薬を自身に注射か',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/isha-haikibutsu-iho-taiho.json'
    },
    {
      id: 'kirishima-nanji-itaibu',
      title: '霧島市の遺体は行方不明の5歳男児と判明 父親が胸中を語る',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kirishima-nanji-itaibu.json'
    },
    {
      id: 'kousho-ondo-40-do-ichigatsu',
      title: '8月初旬 関東甲信など40℃以上「酷暑日」の可能性 1か月予報',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/kousho-ondo-40-do-ichigatsu.json'
    },
    {
      id: 'seven-eleven-tenpai-fusei-tenbai',
      title: 'セブンイレブン 店舗関係者が人気キャラ商品を不正転売 法的には？',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/seven-eleven-tenpai-fusei-tenbai.json'
    },
    {
      id: 'tsubame-suzume-otonari',
      title: 'ツバメとスズメ 隣同士で子育て 長野で珍しい光景',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/tsubame-suzume-otonari.json'
    },
    {
      id: 'disney-owakonka-neage',
      title: '値上げディズニーの「オワコン化」 子ども200万人減の裏で増える大人客',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/disney-owakonka-neage.json'
    },
    {
      id: 'hannmono-otoko-keisatsu-happou',
      title: 'コンビニ駐車場で刃物男に警察官が発砲 住宅街に銃声 熊本',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/hannmono-otoko-keisatsu-happou.json'
    },
    {
      id: 'gundam-shinsaku-2027',
      title: '『ガンダム』新作アニメ発表 2027年展開 神山健治監督が挑む新世界線',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/gundam-shinsaku-2027.json'
    },
    {
      id: 'naikaku-shijiritsu-teika-kikikan',
      title: '内閣支持率減 与党に危機感 皇室典範改正・国会運営が影響',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/naikaku-shijiritsu-teika-kikikan.json'
    },
    {
      id: 'trump-ohtani-sansan-dodgers',
      title: 'トランプ大統領が大谷翔平を絶賛 25分スピーチ ドジャース表敬訪問',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/trump-ohtani-sansan-dodgers.json'
    },
    {
      id: 'yanagita-kyuuen-senshutsu',
      title: '柳田が球宴に 家族旅行キャンセルし9回目の出場へ',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/yanagita-kyuuen-senshutsu.json'
    },
    {
      id: 'hammono-otoko-keisatsu-kan-happou',
      title: 'コンビニに刃物男 警察官の発砲受け21歳男を逮捕 熊本',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/hammono-otoko-keisatsu-kan-happou.json'
    },
    {
      id: 'fujinami-kouta-kouhan',
      title: '降板のDeNA・藤浪晋太郎に甲子園全体から異例の拍手 4年ぶりの聖地登板',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/fujinami-kouta-kouhan.json'
    },
    {
      id: 'yamada-goroo-shi-kyokyo',
      title: '「アド街」が山田五郎さんを追悼 最期の収録は亡くなる6日前',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/yamada-goroo-shi-kyokyo.json'
    },
    {
      id: 'sns-de-chuuko-manshon-kounyu-zou',
      title: '人生最大の買い物なのに…なぜSNSで中古マンションを買う人が増えているのか',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/sns-de-chuuko-manshon-kounyu-zou.json'
    },
    {
      id: '23nichi-mo-saigaikyuu-no-atsusa',
      title: '23日も災害級の暑さ 山梨・東海・近畿で40℃以上酷暑日か',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/23nichi-mo-saigaikyuu-no-atsusa.json'
    },
    {
      id: 'net-chuushou-toukou-syousatsu-1man-ken',
      title: 'ネット中傷、投稿者特定の申し立てが1万件超 22年に導入後初めて',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/net-chuushou-toukou-syousatsu-1man-ken.json'
    },
    {
      id: 'ritou-hikkoshi-nenshou-8oku-en',
      title: '大手が敬遠する離島引っ越しで年商8億円 フリーデザイナーから転身した38歳が開拓したビジネスモデル',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/ritou-hikkoshi-nenshou-8oku-en.json'
    },
    {
      id: 'trump-wcup-zensetsu',
      title: 'W杯表彰式 トランプ氏の執着に批判殺到 FIFA会長が慌てて案内',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/trump-wcup-zensetsu.json'
    },
    {
      id: 'chugoku-reearth-kenkin',
      title: '中国で邦人2名拘束 レアアース巡る「人質外交」に懸念拡大',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/chugoku-reearth-kenkin.json'
    },
    {
      id: 'suisu-nihonjin-suibotsu',
      title: 'スイス・ベルンの川でSUP中 日本人男性が溺れて死亡',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/suisu-nihonjin-suibotsu.json'
    },
    {
      id: 'myze-hasan-model',
      title: 'ミュゼプラチナム破産 前受金依存の「自転車操業」が招いた末路',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/myze-hasan-model.json'
    },
    {
      id: 'zara-shi-no-pantsu',
      title: 'ZARA「死のパンツ」に注意 ワイドパンツで転倒・骨折が相次ぐ',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/zara-shi-no-pantsu.json'
    },
    {
      id: 'ishiba-sho-hizei-minaoshi',
      title: '石破前総理 消費税1％減税見直し「選択肢にあってしかるべき」',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/ishiba-sho-hizei-minaoshi.json'
    },
    {
      id: 'chuugoku-EEZ-syageki-hanron',
      title: '中国外務省が反論 艦艇のEEZ内射撃訓練「懸念は理にかなっていない」',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/chuugoku-EEZ-syageki-hanron.json'
    },
    {
      id: 'takasugi-sumin-0-3jikan',
      title: '「0〜3時間睡眠が常態化」高市首相アピールに波紋 野党から懸念',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/takasugi-sumin-0-3jikan.json'
    },
    {
      id: 'nichirei-hacker-ransom',
      title: 'ニチレイ障害 ハッカー集団「ランサムハウス」が犯行声明',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/nichirei-hacker-ransom.json'
    },
    {
      id: 'nenkyuu-800man-chou',
      title: '年収800万円超は日本に何％？国税庁調査が示す給与の実態',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/nenkyuu-800man-chou.json'
    },
    {
      id: 'kousho-ondo-10nen-ichido',
      title: '気象庁「10年に一度の高温」早期天候情報 今月末にかけ危険な暑さ',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/kousho-ondo-10nen-ichido.json'
    },
    {
      id: 'kiken-unten-kijun',
      title: '「危険運転」に数値基準導入 速度や飲酒の線引きで何が変わる？',
      kicker: '中級',
      desc: '',
      badge: '6段落',
      file: '/asanews/assets/readings/kiken-unten-kijun.json'
    },
    {
      id: 'eu-chuukei-tsuuhan',
      title: 'EU 中国系ネット通販「アリエク」に制裁金 過去最高1022億円',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/eu-chuukei-tsuuhan.json'
    },
    {
      id: 'kogekibi-kousho',
      title: 'どこまで暑くなる 関東・東海で初の「酷暑日」か 危険な暑さ',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/kogekibi-kousho.json'
    },
    {
      id: 'beihei-iran-keikoku',
      title: 'トランプ氏 米兵死亡でイランに「報い」警告 仲介国は停戦模索',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/beihei-iran-keikoku.json'
    },
    {
      id: 'gmo-saitaku-kinmu-shazai',
      title: 'GMO熊谷氏 在宅勤務「完全廃止」投稿を謝罪 真意を説明',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/gmo-saitaku-kinmu-shazai.json'
    },
    {
      id: 'shuugiin-shisan-koukai',
      title: '衆院議員の資産公開 平均3278万円 トップは7億円超',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/shuugiin-shisan-koukai.json'
    },
    {
      id: 'ennchuu-kokkai-fukushuto',
      title: '延長国会 実質審議3日間 「副首都」法案など4法案成立は綱渡り',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/ennchuu-kokkai-fukushuto.json'
    },
    {
      id: 'horumuzu-tanker-bakuhatsu',
      title: 'イラン ホルムズ海峡でタンカー2隻が爆発 航行不能に',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/horumuzu-tanker-bakuhatsu.json'
    },
    {
      id: 'samsung-bei-kyouin-sakugen',
      title: '韓国サムスン 米国本社移転で大規模な人員削減や配置転換',
      kicker: '中級',
      desc: '',
      badge: '3段落',
      file: '/asanews/assets/readings/samsung-bei-kyouin-sakugen.json'
    },
    {
      id: 'kokkai-ennchuu-gaiyuu-chuushi',
      title: '国会延長で自民幹部の外遊中止 要人との会談機会失う',
      kicker: '中級',
      desc: '',
      badge: '2段落',
      file: '/asanews/assets/readings/kokkai-ennchuu-gaiyuu-chuushi.json'
    }
    ];

  function renderList() {
    container.innerHTML = '';
    document.title = '読解ルーム | asanews';

    const wrapper = document.createElement('div');
    wrapper.id = 'page-category';
    wrapper.className = 'reading-room-layout';

    // 見出し
    const h1 = document.createElement('h1');
    h1.className = 'ps-lg-2';
    h1.innerHTML = `
      <i class="far fa-book-open fa-fw text-muted"></i>
      読解ルーム
      <span class="lead text-muted ps-2">${READING_LIST.length} 記事</span>
    `;
    wrapper.appendChild(h1);

    // サブタイトル
    const sub = document.createElement('p');
    sub.className = 'text-muted ps-lg-2';
    sub.textContent = '短い文章で日本語を深く読む。逐語訳・文法解説・音声練習付き。';
    wrapper.appendChild(sub);

    // 記事リスト
    const ul = document.createElement('ul');
    ul.className = 'content ps-0';

    READING_LIST.forEach(r => {
      const li = document.createElement('li');
      li.className = 'd-flex justify-content-between px-md-3';
      li.style.cursor = 'pointer';

      const a = document.createElement('a');
      a.textContent = r.title;
      a.href = `/asanews/reading-room/?read=${r.id}`;

      const dash = document.createElement('span');
      dash.className = 'dash flex-grow-1';

      const level = document.createElement('span');
      level.className = 'text-muted small text-nowrap';
      level.textContent = r.kicker;

      li.appendChild(a);
      li.appendChild(dash);
      li.appendChild(level);

      li.addEventListener('click', (e) => {
        e.preventDefault();
        loadReading(r.id);
        history.pushState({}, '', `/asanews/reading-room/?read=${r.id}`);
      });

      ul.appendChild(li);
    });

    wrapper.appendChild(ul);
    container.appendChild(wrapper);
  }

  // ======================================================================
  //  読解ロード
  // ======================================================================
  function loadReading(id) {
    const reading = READING_LIST.find(r => r.id === id);
    if (!reading) { renderList(); return; }

    container.innerHTML = '<div class="rr-loading">読み込み中…</div>';

    fetch(reading.file)
      .then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then(data => {
        const doc = Array.isArray(data) ? data[0] : data;
        renderReader(doc);
      })
      .catch(err => {
        container.innerHTML = `<div class="rr-error">❌ 読み込みエラー: ${escHtml(err.message)}</div>`;
      });
  }

  // ======================================================================
  //  読解表示
  // ======================================================================
  function renderReader(data) {
    currentData = data;
    currentParaIdx = -1;
    currentAudio = null;
    isPlaying = false;
    audioQueue = [];
    isAutoMode = false;

    container.innerHTML = '';

    // タイトル
    document.title = `${escHtml(data.title)} | 読解ルーム | asanews`;

    const wrapper = document.createElement('div');
    wrapper.className = 'rr-reader';

    // 戻る
    const backWrap = document.createElement('div');
    backWrap.className = 'rr-back-wrap';

    const backBtn = document.createElement('button');
    backBtn.className = 'rr-back-btn';
    backBtn.innerHTML = '← 一覧へ戻る';
    backBtn.addEventListener('click', () => {
      stopAudio();
      renderList();
      history.pushState({}, '', '/asanews/reading-room/');
    });
    backWrap.appendChild(backBtn);

    // 残段落表示
    const paraCount = document.createElement('span');
    paraCount.className = 'rr-para-count';
    paraCount.textContent = `${data.paragraphs.length}段落`;
    backWrap.appendChild(paraCount);

    wrapper.appendChild(backWrap);

    // タイトル
    const hdr = document.createElement('div');
    hdr.className = 'rr-reader-header';
    hdr.innerHTML = `<h1 class="rr-reader-title">${escHtml(data.title)}</h1>`;
    wrapper.appendChild(hdr);

    // ツールバー
    wrapper.appendChild(buildToolbar());

    // 凡例
    wrapper.appendChild(buildLegend());

    // 本文
    const article = document.createElement('div');
    article.className = 'rr-article';
    article.id = 'rr-article';

    data.paragraphs.forEach((para, idx) => {
      article.appendChild(buildParagraph(para, idx));
    });

    wrapper.appendChild(article);



    container.appendChild(wrapper);

    // ツールバー状態復元
    restoreToolbarState();

    // キーボードバインド
    if (!window._rrKeyBound) {
      window._rrKeyBound = true;
      document.addEventListener('keydown', handleKeydown);
    }

    // 最初の段落にスクロール
    setTimeout(() => {
      const firstPara = document.querySelector('.rr-para');
      if (firstPara) firstPara.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }

  // ======================================================================
  //  ツールバー
  // ======================================================================
  const TOOLBAR_TOGGLES = [
    { id: 'ruby',    label: '🔤 ルビ',        cls: 'rr-hide-ruby',  default: false },
    { id: 'gap',     label: '📏 間隔なし',    cls: 'rr-no-gap',     default: false },
    { id: 'color',   label: '🎨 品詞色',      cls: 'rr-no-color',   default: false },
    { id: 'compact', label: '📄 コンパクト',  cls: 'rr-compact',    default: false },
    { id: 'large',   label: '🔍 拡大',        cls: 'rr-large',      default: false },
  ];

  function buildToolbar() {
    const tb = document.createElement('div');
    tb.className = 'rr-toolbar';
    const inner = document.createElement('div');
    inner.className = 'rr-toolbar-inner';

    TOOLBAR_TOGGLES.forEach(t => {
      const btn = document.createElement('button');
      btn.className = 'rr-toolbar-btn' + (t.default ? ' active' : '');
      btn.textContent = t.label;
      btn.dataset.toggleId = t.id;
      btn.addEventListener('click', () => {
        const isActive = document.body.classList.toggle(t.cls);
        btn.classList.toggle('active', isActive);
        saveToolbarState();
      });
      inner.appendChild(btn);
    });

    inner.appendChild(sep());

    // 停止
    const stopBtn = document.createElement('button');
    stopBtn.className = 'rr-toolbar-btn';
    stopBtn.textContent = '⏹ 停止';
    stopBtn.addEventListener('click', stopAudio);
    inner.appendChild(stopBtn);

    // 自動再生
    const autoBtn = document.createElement('button');
    autoBtn.className = 'rr-toolbar-btn';
    autoBtn.textContent = '▶ 全再生';
    autoBtn.addEventListener('click', () => playAll());
    inner.appendChild(autoBtn);

    inner.appendChild(sep());

    // ループ
    const loopLabel = document.createElement('label');
    loopLabel.className = 'rr-loop-toggle';
    loopLabel.innerHTML = `<input type="checkbox" id="rr-loop-cb"> 🔁 ループ`;
    inner.appendChild(loopLabel);

    tb.appendChild(inner);
    return tb;
  }

  function sep() {
    const el = document.createElement('span');
    el.className = 'rr-toolbar-sep';
    return el;
  }

  function buildLegend() {
    const l = document.createElement('div');
    l.className = 'rr-legend';
    [
      ['名詞', 'noun'],
      ['動詞', 'verb'],
      ['助詞', 'particle'],
      ['形容詞', 'adj'],
      ['副詞', 'adverb'],
      ['接続', 'connector'],
      ['文法', 'grammar'],
    ].forEach(([label, cls]) => {
      const span = document.createElement('span');
      span.className = `rr-legend-item`;
      span.style.color = `var(--rr-${cls})`;
      const dot = document.createElement('span');
      dot.className = 'rr-legend-dot';
      dot.style.background = `var(--rr-${cls})`;
      span.appendChild(dot);
      span.appendChild(document.createTextNode(label));
      l.appendChild(span);
    });
    return l;
  }

  // ---- ツールバー状態保存 ----
  function saveToolbarState() {
    const state = {};
    TOOLBAR_TOGGLES.forEach(t => {
      state[t.id] = document.body.classList.contains(t.cls);
    });
    try { localStorage.setItem('rr-toolbar', JSON.stringify(state)); } catch (e) {}
  }

  function restoreToolbarState() {
    try {
      const raw = localStorage.getItem('rr-toolbar');
      if (!raw) return;
      const state = JSON.parse(raw);
      TOOLBAR_TOGGLES.forEach(t => {
        const val = state[t.id];
        if (val === undefined) return;
        document.body.classList.toggle(t.cls, val);
        const btn = document.querySelector(`[data-toggle-id="${t.id}"]`);
        if (btn) btn.classList.toggle('active', val);
      });
    } catch (e) {}
  }

  // ======================================================================
  //  段落構築
  // ======================================================================
  function buildParagraph(para, idx) {
    const sec = document.createElement('section');
    sec.className = 'rr-para';
    sec.id = para.id || ('p' + (idx + 1));
    sec.dataset.idx = idx;

    // 段ヘッダー
    const head = document.createElement('div');
    head.className = 'rr-para-head';

    const no = document.createElement('span');
    no.className = 'rr-para-no';
    no.textContent = `§ ${String(idx + 1).padStart(2, '0')}`;
    head.appendChild(no);

    // 音声ボタン
    const ab = document.createElement('div');
    ab.className = 'rr-audio-btns';

    const text4audio = escAttr(para.ja);

    const normalBtn = document.createElement('button');
    normalBtn.className = 'rr-audio-btn normal';
    normalBtn.innerHTML = '▶ 普通';
    normalBtn.dataset.text = text4audio;
    normalBtn.dataset.speed = '1';
    normalBtn.dataset.audio = para.audio || '';
    normalBtn.dataset.paraIdx = idx;

    const slowBtn = document.createElement('button');
    slowBtn.className = 'rr-audio-btn slow';
    slowBtn.innerHTML = '▶ ゆっくり';
    slowBtn.dataset.text = text4audio;
    slowBtn.dataset.speed = '0.65';
    slowBtn.dataset.audio = para.audio || '';
    slowBtn.dataset.paraIdx = idx;

    ab.appendChild(normalBtn);
    ab.appendChild(slowBtn);
    head.appendChild(ab);
    sec.appendChild(head);

    // ナビボタン（段落間）
    const prevBtn = document.createElement('button');
    prevBtn.className = 'rr-para-nav-btn';
    prevBtn.textContent = '↑ 前';
    prevBtn.addEventListener('click', () => scrollToPara(idx - 1));
    if (idx === 0) prevBtn.style.visibility = 'hidden';

    const nextBtn = document.createElement('button');
    nextBtn.className = 'rr-para-nav-btn';
    nextBtn.textContent = '↓ 次';
    nextBtn.addEventListener('click', () => scrollToPara(idx + 1));
    if (idx === currentData.paragraphs.length - 1) nextBtn.style.visibility = 'hidden';

    const navInline = document.createElement('div');
    navInline.className = 'rr-nav-inline';
    navInline.appendChild(prevBtn);
    navInline.appendChild(nextBtn);
    head.appendChild(navInline);

    // 本文
    const jpDiv = document.createElement('div');
    jpDiv.className = 'rr-jp-text';
    jpDiv.appendChild(buildTokens(para.words));
    sec.appendChild(jpDiv);

    // 詳細パネル
    sec.appendChild(buildDetail(para));

    // 音声バインド
    ab.querySelectorAll('.rr-audio-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const pIdx = parseInt(btn.dataset.paraIdx);
        playPara(pIdx, btn);
      });
    });

    return sec;
  }

  // ---- トークン構築（CSS ツールチップ対応） ----
  function buildTokens(words) {
    const frag = document.createDocumentFragment();
    (words || []).forEach(w => {
      if (!w.s) return;

      // 句読点/空白はそのまま
      if (/^[　 　、。．，！？\n\r]+$/.test(w.s)) {
        frag.appendChild(document.createTextNode(w.s));
        return;
      }

      const span = document.createElement('span');
      span.className = 'rr-tok';
      if (w.p && ['noun','verb','particle','adj','adverb','connector','grammar'].includes(w.p)) {
        span.classList.add(w.p);
      }

      // 注釈 → data-note（CSSツールチップ）
      if (w.n) {
        span.setAttribute('data-note', w.n);
      }

      // Ruby 注音
      if (w.r && /[\u4e00-\u9fff]/.test(w.s)) {
        const ruby = document.createElement('ruby');
        ruby.textContent = w.s;
        const rt = document.createElement('rt');
        rt.textContent = w.r;
        ruby.appendChild(rt);
        span.appendChild(ruby);
      } else {
        span.textContent = w.s;
        if (w.r) {
          const sup = document.createElement('sup');
          sup.textContent = `(${w.r})`;
          sup.style.cssText = 'font-size:0.5em;color:var(--rr-muted);';
          span.appendChild(sup);
        }
      }

      frag.appendChild(span);
    });
    return frag;
  }

  // ---- 詳細パネル ----
  function buildDetail(para) {
    const dt = document.createElement('details');
    dt.className = 'rr-detail';

    const sum = document.createElement('summary');
    sum.className = 'rr-detail-summary';
    sum.textContent = ' 翻訳・文法・語彙';
    dt.appendChild(sum);

    const body = document.createElement('div');
    body.className = 'rr-detail-body';

    // 翻訳
    if (para.en) {
      const block = document.createElement('div');
      block.className = 'rr-trans-block';
      block.innerHTML = `
        <span class="rr-trans-label">Translation</span>
        <div class="rr-trans-text">${escHtml(para.en)}</div>
      `;
      body.appendChild(block);
    }

    // 直訳
    if (para.literal) {
      const lit = document.createElement('div');
      lit.className = 'rr-literal';
      lit.textContent = '直訳: ' + para.literal;
      body.appendChild(lit);
    }

    // 文法
    if (para.grammar) {
      const gs = document.createElement('div');
      gs.className = 'rr-grammar-section';
      gs.innerHTML = `
        <span class="rr-grammar-label">Grammar</span>
        <div>${escHtml(para.grammar)}</div>
      `;
      body.appendChild(gs);
    }

    // 語彙
    if (para.vocab && para.vocab.length) {
      const vl = document.createElement('div');
      vl.className = 'rr-vocab-list';
      para.vocab.forEach(v => {
        const item = document.createElement('div');
        item.className = 'rr-vocab-item';
        const reading = v[1] ? ` <span class="rr-vocab-reading">（${escHtml(v[1])}）</span>` : '';
        item.innerHTML = `<strong>${escHtml(v[0])}</strong>${reading} — ${escHtml(v[2])}`;
        vl.appendChild(item);
      });
      body.appendChild(vl);
    }

    dt.appendChild(body);
    return dt;
  }

  // ======================================================================
  //  音声再生
  // ======================================================================
  function playPara(idx, btn) {
    if (!currentData || !currentData.paragraphs[idx]) return;
    stopAudio();
    currentParaIdx = idx;

    const para = currentData.paragraphs[idx];
    const audioSrc = btn.dataset.audio;
    const text = btn.dataset.text;
    const speed = parseFloat(btn.dataset.speed) || 1;

    // スクロール
    const section = document.getElementById(para.id);
    if (section) section.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // ハイライト
    document.querySelectorAll('.rr-para.playing').forEach(p => p.classList.remove('playing'));
    if (section) section.classList.add('playing');

    btn.classList.add('playing');

    if (audioSrc) {
      const audio = new Audio('/asanews/' + audioSrc);
      audio.playbackRate = speed;
      audio.loop = document.getElementById('rr-loop-cb').checked;

      audio.addEventListener('ended', () => {
        btn.classList.remove('playing');
        if (audio.loop) {
          audio.currentTime = 0;
          audio.play();
          return;
        }
        if (isAutoMode) {
          playNextInQueue();
        }
      });

      audio.addEventListener('error', () => {
        btn.classList.remove('playing');
        fallbackTTS(text, speed, idx);
      });

      currentAudio = audio;
      isPlaying = true;
      audio.play().catch(() => {
        btn.classList.remove('playing');
        fallbackTTS(text, speed, idx);
      });
    } else {
      fallbackTTS(text, speed, idx);
    }
  }

  function fallbackTTS(text, rate, idx) {
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'ja-JP';
    u.rate = rate / 1.2;
    u.onend = () => {
      const loop = document.getElementById('rr-loop-cb');
      if (loop && loop.checked) {
        setTimeout(() => fallbackTTS(text, rate, idx), 400);
        return;
      }
      if (isAutoMode) {
        playNextInQueue();
      }
    };
    u.onerror = () => {
      if (isAutoMode) playNextInQueue();
    };
    window.speechSynthesis.speak(u);
    isPlaying = true;
  }

  function stopAudio() {
    if (currentAudio) {
      currentAudio.pause();
      currentAudio = null;
    }
    window.speechSynthesis.cancel();
    isPlaying = false;
    isAutoMode = false;
    audioQueue = [];
    document.querySelectorAll('.rr-audio-btn.playing').forEach(b => b.classList.remove('playing'));
    document.querySelectorAll('.rr-para.playing').forEach(p => p.classList.remove('playing'));
  }

  // ---- 全段落自動再生 ----
  function playAll() {
    if (!currentData || !currentData.paragraphs.length) return;
    stopAudio();

    isAutoMode = true;
    audioQueue = currentData.paragraphs.map((_, idx) => idx);

    // 最初の段落の「普通」ボタンを探す
    playNextInQueue();
  }

  function playNextInQueue() {
    if (!isAutoMode || audioQueue.length === 0) {
      isAutoMode = false;
      return;
    }

    const nextIdx = audioQueue.shift();
    const section = document.getElementById(currentData.paragraphs[nextIdx].id);
    if (!section) return;

    // この段落の「普通」ボタンを探して再生
    const normalBtn = section.querySelector('.rr-audio-btn.normal');
    if (normalBtn) {
      playPara(nextIdx, normalBtn);
    }
  }

  // ======================================================================
  //  キーボードショートカット
  // ======================================================================
  function handleKeydown(e) {
    // テキスト入力中は無視
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;

    switch (e.key) {
      case 'n':
      case 'N':
        e.preventDefault();
        nextPara();
        break;
      case 'p':
      case 'P':
        e.preventDefault();
        prevPara();
        break;
      case ' ':
        e.preventDefault();
        toggleCurrentParaAudio();
        break;
    }
  }

  function scrollToPara(idx) {
    if (!currentData || idx < 0 || idx >= currentData.paragraphs.length) return;
    const section = document.getElementById(currentData.paragraphs[idx].id);
    if (section) section.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }

  function nextPara() {
    if (currentParaIdx < 0) { scrollToPara(0); currentParaIdx = 0; return; }
    scrollToPara(currentParaIdx + 1);
    if (currentParaIdx + 1 < currentData.paragraphs.length) currentParaIdx++;
  }

  function prevPara() {
    scrollToPara(currentParaIdx - 1);
    if (currentParaIdx > 0) currentParaIdx--;
  }

  function toggleCurrentParaAudio() {
    if (isPlaying) {
      stopAudio();
      return;
    }
    // 現在表示中の最初の段落に「普通」ボタンがあれば再生
    const firstSection = document.querySelector('.rr-para');
    if (!firstSection) return;
    const btn = currentParaIdx >= 0
      ? document.querySelector(`.rr-para[data-idx="${currentParaIdx}"] .rr-audio-btn.normal`)
      : firstSection.querySelector('.rr-audio-btn.normal');
    if (btn) {
      playPara(parseInt(btn.dataset.paraIdx), btn);
    }
  }

  // ======================================================================
  //  ユーティリティ
  // ======================================================================
  function escHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
  }

  function escAttr(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#039;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

})();
