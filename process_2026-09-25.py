import os,re,json,subprocess,requests
from bs4 import BeautifulSoup
from sudachipy import tokenizer,dictionary
B='/home/horse/.openclaw/workspace/asanews'; D='2026-09-25'
T=dictionary.Dictionary().create(); M=tokenizer.Tokenizer.SplitMode.C
PM={'名詞':'noun','動詞':'verb','助詞':'particle','形容詞':'adj','連体詞':'adj','副詞':'adverb','接続詞':'connector','接頭辞':'connector','接尾辞':'connector','助動詞':'grammar','感動詞':'connector'}
def hira(s): return ''.join(chr(ord(c)-96) if 'カ'<=c<='ン' else ('ゔ' if c=='ヴ' else c) for c in s)
def words(s):
 o=[]
 for x in T.tokenize(s,M):
  r=hira(x.reading_form() or ''); d=x.dictionary_form()
  o.append({'s':d if d!='*' else x.surface(),'r':r if r and r!=x.surface() else '','p':PM.get(x.part_of_speech()[0],'')})
 return o
def get(u):
 s=BeautifulSoup(requests.get(u,headers={'User-Agent':'Mozilla/5.0'},timeout=30).text,'html.parser'); b=s.select_one('div.article_body')
 return [p.get_text(' ',strip=True) for p in b.find_all('p') if p.get_text(strip=True) and not p.get_text(strip=True).startswith(('写真','【'))][:3]
A=[
('fukushima-shikei-hyougen','福島党首、ラサール氏の「4人殺している」発言を容認　「表現の仕方の範囲内」','社民党の福島瑞穂党首が、死刑執行をめぐるラサール石井氏の発言について、政治家としての表現の範囲内だと述べた。','eb1bd96f6aef6ac487c12982c2083b96f2ac32cd',
['Social Democratic Party leader Mizuho Fukushima said that a statement about Justice Minister Yamashita was within the speaker’s range of expression. She said executions are killings carried out by the state under the law, while distinguishing them from an individual killing someone.','The remark referred to four executions carried out while Yamashita was justice minister. He served from October 2018 to September 2019, and two executions involving four people took place during his term.','Fukushima also said that calling executions “murder” was within the range of political expression. She noted that some former justice ministers had refused to sign execution orders.'],
['社民党福岛瑞穗党首表示，关于法务大臣山下的发言属于说话者表达方式的范围。她说死刑是依据法律由国家执行的杀人，但不同于个人杀人。','这番话指的是山下担任法务大臣期间执行的4人死刑。他从2018年10月至2019年9月任职，任内执行了两次、共4人的死刑。','福岛还表示，把死刑说成“杀人”属于政治家的表达范围。她指出有些前法务大臣曾拒绝签署执行命令。'],
'「〜を巡り」— 围绕、关于。例：発言を巡り会見した。\n「〜にのっとった」— 依据、按照。例：法律にのっとった手続きだ。\n「〜わけだ」— 也就是说。例：人を殺しているわけだ。',[['党首','とうしゅ','党首'],['幹事長','かんじちょう','干事长'],['法相','ほうしょう','法务大臣'],['死刑','しけい','死刑'],['処刑','しょけい','处刑'],['容認する','ようにんする','认可']]),
('junglia-akaiji-2026','ジャングリア親会社、開業後初決算で173億円の最終赤字　来場者は想定を下回る','沖縄のテーマパーク運営会社の親会社が開業後初の決算で大幅な最終赤字となり、来場者数も想定を下回った。','32356213539e5b3557aea783e84806d6032a8f30',
['The parent company of Okinawa’s Junglia theme park operator posted a final loss of about 17.3 billion yen in its first results after opening. It was expected to explain its finances at a shareholders’ meeting.','The main cause was an impairment loss on shares of the subsidiary operating Junglia. The subsidiary’s final loss reached about 8.9 billion yen.','Junglia opened last July. Although 1.5 million visitors had been projected for the year, the actual total was one million, far below expectations. Some days reportedly had only about 1,000 visitors.'],
['冲绳主题公园Junglia运营公司的母公司在开业后的首次决算中出现约173亿日元最终亏损，并计划说明财务状况。','主要原因是运营Junglia的子公司股票评估损失。该子公司的最终亏损达到约89亿日元。','Junglia去年7月开业，原预计一年有150万人到访，实际累计为100万人，大幅低于预期。有些日子据称仅约1000人。'],
'「〜後初の」— …之后首次。例：開業後初の決算だ。\n「〜を下回る」— 低于。例：想定を大きく下回った。\n「〜に上る」— 达到。例：赤字は173億円に上った。',[['親会社','おやがいしゃ','母公司'],['決算','けっさん','决算'],['最終赤字','さいしゅうあかじ','最终亏损'],['来場者','らいじょうしゃ','到场者'],['想定','そうてい','预想'],['評価損','ひょうかぞん','评估损失']]),
('kitakyushu-sakana-shi','川を埋め尽くす大量の魚が死ぬ　専門家は2つの可能性を指摘　北九州市','北九州市の川で魚の大量死が見つかり、専門家は浅瀬での酸欠や海から流れ込んだ可能性を指摘した。','ff928a305ea1d4305cdc70496cc80dc62cc30fbc',
['A large number of dead fish were found in a Kitakyushu river. A specialist familiar with fish ecology pointed to two possible explanations, and contractors began collecting the fish.','The fish appeared to be members of the sardine family. One possibility is that larger fish or dolphins chased them into shallow water, where they ran out of oxygen and died.','The other possibility is that a school of fish died at sea and flowed into the river. The city is removing them quickly because odors could affect residents’ daily lives.'],
['北九州市一条河流中发现大量死鱼。熟悉鱼类生态的专家指出两种可能，业者开始回收鱼。','鱼看起来属于沙丁鱼一类。一种可能是被大型鱼类或海豚追到浅滩，因缺氧而死亡。','另一种可能是鱼群在海中死亡后流入河中。市政府因恶臭可能影响市民生活而加紧回收。'],
'「〜を埋め尽くす」— 铺满。例：川を魚が埋め尽くす。\n「〜からすると」— 从…来看。例：映像からすると魚の仲間だ。\n「〜かもしれない」— 也许。例：川に流れ込んだかもしれない。',[['大量死','たいりょうし','大量死亡'],['生態','せいたい','生态'],['浅瀬','あさせ','浅滩'],['酸欠','さんけつ','缺氧'],['満潮','まんちょう','满潮'],['悪臭','あくしゅう','恶臭']]),
('kakyo-japan-kanko','中国系の超富裕層が大家族で日本旅行　訪日で求めるものを分析','海外に住む華僑・華人の超富裕層が、両家の両親を含む大家族で日本を訪れる背景を紹介する。','9424ade4fde11c9056173f3493fe60914c8cb849',
['Although visitors from China are declining, some people of Chinese origin continue to visit Japan. They collect travel information on Chinese social media and arrange guides or private cars through Chinese booking sites.','A very wealthy Chinese-descent couple living in Chicago traveled to Japan with their newborn and both sets of parents instead of returning to China. The article analyzes what they seek in Japan.','The couple met at a prestigious American university. The wife built a career at a major company, while the husband achieved financial independence and early retirement. The family plans to move to Seattle for its educational environment.'],
['虽然来自中国的游客减少，但仍有中国系人士来日。他们通过中国社交媒体收集信息，并用预约网站安排向导或专车。','一对居住在芝加哥的中国系超富裕夫妇带着新生儿和双方父母来日本，而不是回中国。文章分析他们在日本寻求的东西。','夫妇在美国名牌大学相识。妻子在大企业发展事业，丈夫实现经济独立和提前退休。全家计划为教育环境搬到西雅图。'],
'「〜一方で」— 一方面…另一方面。例：人数が減る一方で訪日客もいる。\n「〜うえで」— 在…基础上。例：事例を紹介したうえで分析する。\n「〜ことができた」— 能够。例：キャリアを積むことができた。',[['華僑','かきょう','华侨'],['華人','かじん','华人'],['超富裕層','ちょうふゆうそう','超富裕阶层'],['手配する','てはいする','安排'],['資産運用','しさんうんよう','资产运用'],['名門大学','めいもんだいがく','名牌大学']])
]
new=[]
for slug,title,sub,h,en,lit,gram,voc in A:
 ps=get('https://news.yahoo.co.jp/articles/'+h); paras=[]
 for i,ja in enumerate(ps):
  ap=f'assets/audio/{slug}/p{i+1}.mp3'; os.makedirs(os.path.dirname(B+'/'+ap),exist_ok=True)
  subprocess.run(['/home/horse/.local/bin/edge-tts','--voice','ja-JP-NanamiNeural','--text',ja,'--write-media',B+'/'+ap],capture_output=True,timeout=180)
  paras.append({'id':f'p{i+1}','ja':ja,'en':en[i],'literal':lit[i],'grammar':gram,'vocab':voc,'words':words(ja),'audio':ap})
 with open(f'{B}/assets/readings/{slug}.json','w',encoding='utf8') as f: json.dump([{'id':slug,'title':title,'subtitle':sub,'level':'中級','length':len(paras),'date':D,'paragraphs':paras}],f,ensure_ascii=False,indent=2)
 with open(f'{B}/_posts/{D}-{slug}.md','w',encoding='utf8') as f: f.write(f'---\ntitle: {title}\ndate: {D} 07:00:00 +0900\ncategories: [ニュース]\ntags: [ニュース]\n---\n\n'+'\n\n'.join(p['ja'] for p in paras)+f'\n\n<div style="text-align:center"><a href="/asanews/reading-room/?read={slug}">📖 読解ルームで詳しく読む</a></div>\n')
 new.append({'id':slug,'title':title,'level':'中級','length':len(paras),'date':D,'file':f'assets/readings/{slug}.json'})
ip=f'{B}/assets/readings/index.json'; old=json.load(open(ip,encoding='utf8')); ids={x['id'] for x in new}
json.dump(new+[x for x in old if x['id'] not in ids],open(ip,'w',encoding='utf8'),ensure_ascii=False,indent=2)
jp=f'{B}/assets/js/reading-room.js'; js=open(jp,encoding='utf8').read(); allx=new+[x for x in old if x['id'] not in ids]
lines=',\n'.join("    { id: '%s', title: '%s', kicker: '中級', desc: '', badge: '%s段落', file: '/asanews/%s' }"%(x['id'],x['title'].replace("'","\\'"),x['length'],x['file']) for x in allx)
js=re.sub(r'const READING_LIST = \[.*?\];','const READING_LIST = [\n'+lines+'\n    ];',js,flags=re.S)
open(jp,'w',encoding='utf8').write(js)
print('processed',','.join(x['id'] for x in new))
