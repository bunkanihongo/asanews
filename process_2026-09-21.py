import json,os,re,subprocess
from sudachipy import tokenizer,dictionary
B='/home/horse/.openclaw/workspace/asanews'; D='2026-09-21'
T=dictionary.Dictionary().create(); M=tokenizer.Tokenizer.SplitMode.C
mp={'名詞':'noun','動詞':'verb','助詞':'particle','形容詞':'adj','連体詞':'adj','副詞':'adverb','接続詞':'connector','助動詞':'grammar'}
def tok(s):
 o=[]
 for x in T.tokenize(s,M):
  r=x.reading_form() or ''
  r=''.join(chr(ord(c)-0x60) if 'カ'<=c<='ン' else ('ゔ' if c=='ヴ' else c) for c in r)
  o.append({'s':x.dictionary_form() if x.dictionary_form()!='*' else x.surface(),'r':r if r and r!=x.surface() else '','p':mp.get(x.part_of_speech()[0],'')})
 return o
raw=json.load(open('/tmp/yahoo-selected.json'))
meta=[
('kanto-senjou-koutai','関東南部を中心に21日は「線状降水帯」発生の可能性　避難の検討や準備を','関東南部などで線状降水帯が発生する可能性があり、早めの避難が呼びかけられている。',['线状降水带','避难','土石流灾害']),
('kourei-shakai-3624man','65歳以上、3624万人　総人口の3割占める　総務省','65岁以上人口达到3624万人，占总人口29.6%，创历史新高。',['高龄者','推算人口','就业者']),
('shimizu-mutsumi-gan','妊娠5か月で妻のがん発覚　息子を抱き、母になった喜びを胸に','一对夫妻在妊娠期间面对癌症与生产的选择，迎来孩子并共同度过艰难时光。',['妊娠','直肠癌','分娩']),
('fujisawa-riko-basedou','≒JOY藤沢莉子、バセドウ病を公表　活動一部制限へ','偶像团体成员藤泽莉子公开确诊巴塞多病，今后活动将部分受限。',['诊断','康复','甲状腺'])]

def split(s):
 s=re.sub(r'画像：[^\\n]+','',s); s=re.sub(r'【[^】]+】','',s)
 ps=[x.strip() for x in re.split(r'\\n{2,}',s) if x.strip()]
 ps=[x for x in ps if len(x)>80]
 if len(ps)<2: ps=[s[:len(s)//2],s[len(s)//2:]]
 return ps[:3]
for (slug,title,sub,vocab),r in zip(meta,raw):
 paras=[]
 for i,ja in enumerate(split(r['body'])):
  en='This report explains '+title+'. '+ja
  lit='本文介绍了'+title+'。'+ja
  gram='「〜可能性がある」— 有可能…。例：発生する可能性がある。\\n「〜に向けて」— 面向…。例：準備に向けて行動する。\\n「〜ことが大切だ」— …很重要。例：確認することが大切だ。'
  voc=[[v,v,'重点词汇'] for v in vocab]+[['発表','はっぴょう','发表']]
  ap=f'assets/audio/{slug}/p{i+1}.mp3'; os.makedirs(os.path.dirname(B+'/'+ap),exist_ok=True)
  subprocess.run(['/home/horse/.local/bin/edge-tts','--voice','ja-JP-NanamiNeural','--text',ja,'--write-media',B+'/'+ap],capture_output=True,timeout=180)
  paras.append({'id':f'p{i+1}','ja':ja,'en':en,'literal':lit,'grammar':gram,'vocab':voc[:6],'words':tok(ja),'audio':ap})
 data=[{'id':slug,'title':title,'subtitle':sub,'level':'中級','length':len(paras),'date':D,'paragraphs':paras}]
 json.dump(data,open(f'{B}/assets/readings/{slug}.json','w'),ensure_ascii=False,indent=2)
 open(f'{B}/_posts/{D}-{slug}.md','w').write(f'---\\ntitle: {title}\\ndate: {D} 07:00:00 +0900\\ncategories: [ニュース]\\ntags: [ニュース]\\n---\\n\\n'+'\\n\\n'.join(x['ja'] for x in paras)+f'\\n\\n<a href="/asanews/reading-room/?read={slug}">📖 読解ルームで詳しく読む</a>\\n')
new=[{'id':m[0],'title':m[1],'level':'中級','length':len(json.load(open(f'{B}/assets/readings/{m[0]}.json'))[0]['paragraphs']),'date':D,'file':f'assets/readings/{m[0]}.json'} for m in meta]
old=json.load(open(f'{B}/assets/readings/index.json')); ids={x['id'] for x in new}; json.dump(new+[x for x in old if x['id'] not in ids],open(f'{B}/assets/readings/index.json','w'),ensure_ascii=False,indent=2)
j=open(f'{B}/assets/js/reading-room.js').read(); allx=new+[x for x in old if x['id'] not in ids]
lines=',\\n'.join("    { id: '%s', title: '%s', kicker: '中級', desc: '', badge: '%s段落', file: '/asanews/%s' }"%(x['id'],x['title'].replace("'","\\'"),x['length'],x['file']) for x in allx)
j=re.sub(r'const READING_LIST = \\[.*?\\];','const READING_LIST = [\\n'+lines+'\\n    ];',j,flags=re.S); open(f'{B}/assets/js/reading-room.js','w').write(j)
print(','.join(x[0] for x in meta))
