from dotenv import load_dotenv;load_dotenv();import anthropic, os;import pandas as pd

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=os.getenv("claude"))
message = client.messages.create(model="claude-3-7-sonnet-20250219",messages=[
        {"role": "user", "content": """
- 너는 사용자의 질문과 연관된 문서인지 검증하는 전문가야.
- 너에게는 json 형식의 문서가 주어질꺼야.
- 너가 봐야할 칼럼은 standalone_query(str형식), topk(list형식), references(list형식) 세가지 뿐이야.
- answer 칼럼은 무시해
- 특히 references 리스트에서는 scores보다는 content만 중요해. 

1. "standalone_query"는 사용자의 질문이다
2. "references"는 사용자의 질문과 관련된 문서의 내용이야.
3. "topk"는 사용자의 질문과 관련된 문서의 id이다.

- topk 순서는 references 순서와 같다

- standalone_query와 references를 읽고, 사용자의 질문과 관련된 문서인지 판단해야 해.
- 만약 사용자의 질문과 관련이 없는 references가 있다면, 그 항목을 references와 topks list에서 제거해야 해. 다음 [예시]를 참고해

답변은 json 형식으로 항목은 eval_id, standalone_query, topk, references로 구성되어 있다.

[예시]

1. 변경전

{"eval_id": 81, "standalone_query": "통학 버스가 환경과 사회에 미치는 영향 및 그 가치, 학생 안전과 접근성 개선에 대한 역할", "topk": ["54a3c876-121f-48a6-8c49-c52e53990786", "bd91bda8-351e-4683-bb1a-8254f93e2376", "4dd38664-fc38-4c4d-9969-1d99474a427b"], "answer": "통학 버스의 가치는 학생들의 안전한 등하교를 보장하고, 교통 체증 완화에 기여하며, 환경 보호에 도움이 됩니다. 또한, 통학 버스는 학생들의 사회성 발달과 공동체 의식을 함양하는 데에도 기여합니다.", "references": [{"score": 23.044512, "content": "현재로서 2019년 기준으로, 전 세계 인구 중에서는 30%의 인구가 안전하게 마실 물을 이용할 수 없습니다. 이는 매우 심각한 문제로, 많은 사람들이 깨끗하고 안전한 물에 접근할 수 없는 상황에 처해있습니다. 이러한 문제는 주로 개발도상국이나 빈곤 지역에서 더욱 심각하게 나타나며, 인간의 기본적인 생존에 필요한 물을 얻기 어려운 상황에 놓여있는 수많은 사람들이 있습니다. 이러한 문제를 해결하기 위해서는 국제사회와 각국 정부들이 협력하여 물 접근성을 개선하고, 물 관리에 대한 투자와 인프라 구축을 강화해야 합니다. 또한, 물 접근성을 개선하기 위한 교육과 정보 제공, 환경 보호 등의 다양한 노력이 필요합니다. 이러한 노력들을 통해 모든 사람들이 안전하고 깨끗한 물을 마실 수 있는 세상을 만들어야 합니다."}, {"score": 22.728752, "content": "학교 버스는 동일한 거리에 놓여 있을 때, 가장 큰 인력을 가질 것이다. 이는 학교 버스 간에 존재할 것이다. 학교 버스는 많은 학생들을 운송하고, 학교로 가는 길에 많은 사람들을 만난다. 따라서, 학교 버스는 많은 사람들의 관심과 주목을 받을 것이다. 또한, 학교 버스는 학교의 상징이기도 하며, 학생들에게 안전하고 편리한 이동 수단을 제공한다. 따라서, 학교 버스는 동일한 거리에 놓여 있을 때, 가장 큰 인력을 가지고 있을 것이다."}, {"score": 21.617325, "content": "라틴계 미국인들 사이에서의 HIV 유병률은 아프리카계 미국인을 제외한 모든 다른 민족 집단보다 높습니다. 이는 연구와 조사에 의해 확인된 사실입니다. 라틴계 미국인들은 HIV에 노출되는 위험이 더 높은 환경에서 살고 있으며, 예방 및 치료에 대한 접근성이 제한되는 경우가 많습니다. 이러한 상황은 라틴계 미국인들의 건강과 복지에 부정적인 영향을 미치고 있습니다. 따라서, 라틴계 미국인들을 대상으로 한 예방 및 교육 프로그램의 중요성이 강조되고 있으며, 이를 통해 HIV 유병률을 낮추는 노력이 진행되고 있습니다. 그러나 여전히 많은 과제와 도전이 남아있으며, 사회적, 경제적, 문화적인 요인들을 고려한 종합적인 대책이 필요합니다. 라틴계 미국인들의 건강과 복지를 보호하고 개선하기 위해 지속적인 노력이 필요합니다."}]}

2. 변경후 

{"eval_id": 81, "standalone_query": "통학 버스가 환경과 사회에 미치는 영향 및 그 가치, 학생 안전과 접근성 개선에 대한 역할", "topk": ["bd91bda8-351e-4683-bb1a-8254f93e2376"], "answer": "통학 버스의 가치는 학생들의 안전한 등하교를 보장하고, 교통 체증 완화에 기여하며, 환경 보호에 도움이 됩니다. 또한, 통학 버스는 학생들의 사회성 발달과 공동체 의식을 함양하는 데에도 기여합니다.", "references": [{"score": 22.728752, "content": "학교 버스는 동일한 거리에 놓여 있을 때, 가장 큰 인력을 가질 것이다. 이는 학교 버스 간에 존재할 것이다. 학교 버스는 많은 학생들을 운송하고, 학교로 가는 길에 많은 사람들을 만난다. 따라서, 학교 버스는 많은 사람들의 관심과 주목을 받을 것이다. 또한, 학교 버스는 학교의 상징이기도 하며, 학생들에게 안전하고 편리한 이동 수단을 제공한다. 따라서, 학교 버스는 동일한 거리에 놓여 있을 때, 가장 큰 인력을 가지고 있을 것이다."}]}
         
         """}])
print(message.content[0].text)

# JSONL 파일 불러오기
file_path='/data/ephemeral/home/upstageailab-ir-competition-ir_s3/person/DU/output/02-2-5_solar_o1.csv' 
df=pd.read_csv(file_path)
# JSON 파일로 저장 (JSON Lines 형식)
json_file_path = '/data/ephemeral/home/upstageailab-ir-competition-ir_s3/person/DU/output/02-2-5_solar_o1.jsonl'
df.to_json(json_file_path, orient='records', lines=True, force_ascii=False)
df['query']=[get_key(msg) for msg in df['msg']]

print(df.head(30)) # 데이터프레임 확인

df.to_csv('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added_query.csv', index=False, encoding='utf-8-sig')
df.to_json('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added_query.jsonl',orient='records', lines=True, force_ascii=False)

if line['topk']:
    
def get_key(msg):
    completion=openai.chat.completions.create(model="o1-preview",messages=[{"role":"user","content":f"""
- 너는 채팅 사용자의 의도를 분류해서 응대하는 안내원이야.
- 너는 [사용자와의 기존 대화]를 마지막까지 읽고 사용자를 분류해.
- 사용자가 "안녕, 잘 있었어", "나 오늘 너무 슬퍼", "너 누구야?" 등 정서적인 공감이나 일상적인 대화를 원하는지 아니면 어떤 객관적인 사실에 대한 '지식'을 알고 싶어 하는지 분류해야 해.
- 사용자가 일상적인 대화를 원하면 '0', 과학적인 지식을 궁금해하면 '1'을 반환해
- 답변은 오직 한개의 숫자로 출력해야 해.

[사용자와의 기존 대화]
{msg}
"""}])    
    ans=completion.choices[0].message.content
    print(ans)
    return ans

# JSONL 파일 불러오기
file_path='/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval.jsonl' 
df=pd.read_json(file_path, lines=True)
df['intent']=[get_key(msg) for msg in df['msg']]