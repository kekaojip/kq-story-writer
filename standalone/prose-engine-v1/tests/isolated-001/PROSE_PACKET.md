# ISOLATED TEST 001 — PROSE_PACKET

```yaml
PROSE_PACKET:
  language: zh-CN
  genre: 现代都市
  audience: 中文网文读者
  length_hint: 700-1000 中文字

  prose:
    register: 现代自然中文白话
    pace: 中快
    distance_bias: close

  pov:
    person: third_limited
    character: 陈默

  scene:
    start:
      place: 城中村一间小修理铺
      time: 晚上九点多
      current_action: 陈默正准备关店
      attention_seed: 卷帘门刚拉下一半，有人从外面伸手挡住
    immediate_want: 尽快关店回家
    immediate_pressure: 来人是房东的儿子，平时说话很不客气
    beats:
      - 房东儿子把一部摔坏的手机递给陈默，要他今晚修好
      - 陈默检查后发现主板进水，不可能今晚修好
      - 对方要求他直接换一块拆机主板，并暗示房租下个月可能涨
      - 陈默没有争吵，只把手机放回柜台，告诉他这单自己不接
      - 对方愣了一下，问陈默是不是不想继续租了
      - 陈默把卷帘门继续往下拉，只回一句“明天房租按合同交”
    end_state: 陈默完成拒绝，双方关系出现第一次明显变化
    stop_point: 卷帘门彻底落地，门外的人没有再拍门

  knowledge:
    pov_knows:
      - 自己租这间铺子两年，房租一直按合同准时交
      - 房东儿子平时会拿一些麻烦活强塞给周边商户
      - 这部手机如果强行换拆机主板，后续很容易继续扯皮
    pov_does_not_know:
      - 房东是否真的准备涨租
      - 对方今晚为什么特别着急

  constraints:
    must_keep:
      - 陈默不是热血硬刚型人物
      - 拒绝应该克制、直接，不发表大道理
      - 手机维修细节只写到支撑判断所需，不科普
    must_not_add:
      - 肢体冲突
      - 新角色
      - 隐藏身份
      - 系统、异能、金手指
      - 对方突然认怂道歉
    must_not_reveal:
      - 房东后续是否真的涨租

  characters:
    - name: 陈默
      relation: POV
      current_state: 忙了一天，累，但判断清楚
      speech_note: 话不多，不爱解释，真正决定后很少反复
    - name: 赵鹏
      relation: 房东的儿子
      current_state: 急躁，习惯别人让步
      speech_note: 说话随意带压迫感，不需要刻意脸谱化

  voice:
    profile_id: null
    approved_sample_ids: []
    explicit_preferences:
      - 中文像正常人写的小说
      - 不要古风
      - 不要论文腔
      - 不要策划分析腔
      - 不追求金句

  reader:
    target: 喜欢节奏顺、对白自然、人物克制的中文网文读者
```
