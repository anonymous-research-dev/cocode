# 프로젝트 채점 코드 매뉴얼: 파이썬

이 문서는 Cocode 파이썬 프로젝트를 위한 *채점 코드*를 작성하는 방법에 대한 설명서입니다.

## 채점 코드의 종류

Cocode 파이썬 프로젝트에서는 아래와 같이 세 가지 타입의 채점 코드를 지원합니다. 
- 표준 입출력: 표준 입력으로 특정 데이터를 제공해서 사용자의 코드를 실행시킨 뒤 표준 출력이 적절히 나왔는지 확인해서 채점합니다.
- 결과 검증: 표준 입력으로 특정 데이터를 제공해서 사용자의 코드를 실행시킨 뒤 assertion을 통해 채점합니다.
- 코드: 사용자 코드를 문자열 데이터로 제공받아 채점 결과를 구하는 파이썬 코드를 직접 작성해 채점합니다.

## 종류별 채점 코드 포맷

### 표준 입출력

```json
{
    "grader_type": "stdio",
    "tests": [
        {
            "in": [
                "this is a test program",
                "hello there"
            ],
            "out": "hello world",
            "score": 30
        },
        {
            "in": "this is a test program\nthere there",
            "out": "no hello world",
            "score": 30
        },
        {
            "in": "hello everyone",
            "out": "hello world",
            "score": 40
        }
    ]
}
```

### 결과 검증

```json
{
    "grader_type": "assert",
    "tests": [
        {
            "in": [
                "this is a test program",
                "hello there"
            ],
            "asserts": [
                "input_data",
                "'hello' in input_data"
            ],
            "score": 50
        },
        {
            "in": [
                "this is a test program",
                "there there"
            ],
            "asserts": [
                "input_data",
                "'hello' not in input_data"
            ],
            "score": 50
        }
    ]
}
```

### 코드

여기서는 직접 채점용 코드를 작성해서 넣어주시면 되는데, 이 때 코드 내에서
`__code__` 변수 안에 사용자 코드가 들어있으니 이걸 직접 채점해주시면 되고,
`__set_score__(score)` 를 사용해서 점수를 입력하실 수 있으며,
`__set_message__(message_string)` 을 사용해서 출력할 메시지를
입력하실 수 있습니다.

아래와 같이 채점 코드를 JSON string으로 직접 포함해 주시면 되고:

```json
{
    "grader_type": "code",
    "code": "grade_code = '''\nif not 'bot' in globals:\n    __set_message__('로봇을 안 만드신것 같아요. 아니면 만들긴 했는데 bot 말고 다른 이름을 붙여주신게 아닌가요? bot 변수가 없습니다.')\n    __set_score__(0)\nelif bot.position.to_list() != [9, 9]:\n    __set_message__('로봇을 맨 오른쪽 맨 위에 있는 칸으로 안 보내신것 같아요. 아니면 갔다가 다른데로 다시 움직였을지도요. 프로그램이 끝날 때 로봇이 맨 오른쪽 맨 윗칸에 있도록 해주세요.')\n    __set_score__(10)\nelif __code__.count('bot.move()') > 3:\n    __set_message__('작성하신 코드에 \"bot.move()\"가 세 번 넘게 등장하는것 같아요. For 문을 사용해서 세 번 이하로 줄여보세요.')\n    __set_score__(40)\nelse:\n    __set_score__(100)\n'''\n\nexec(__code__ + grade_code, {\n    '__name__': '__main__', \n    '__code__': __code__,\n    '__set_score__': __set_score__,\n    '__set_message__': __set_message__,\n    '__store__': __store__,\n})"
}
```

이 채점 코드는 실제로 보면 이런 모양입니다:

```python
grade_code = '''
if not 'bot' in globals:
    __set_message__('로봇을 안 만드신것 같아요. 아니면 만들긴 했는데 bot 말고 다른 이름을 붙여주신게 아닌가요? bot 변수가 없습니다.')
    __set_score__(0)
elif bot.position.to_list() != [9, 9]:
    __set_message__('로봇을 맨 오른쪽 맨 위에 있는 칸으로 안 보내신것 같아요. 아니면 갔다가 다른데로 다시 움직였을지도요. 프로그램이 끝날 때 로봇이 맨 오른쪽 맨 윗칸에 있도록 해주세요.')
    __set_score__(10)
elif __code__.count('bot.move()') > 3:
    __set_message__('작성하신 코드에 "bot.move()"가 세 번 넘게 등장하는것 같아요. For 문을 사용해서 세 번 이하로 줄여보세요.')
    __set_score__(40)
else:
    __set_score__(100)
'''

exec(__code__ + grade_code, {
    '__name__': '__main__', 
    '__code__': __code__,
    '__set_score__': __set_score__,
    '__set_message__': __set_message__,
    '__store__': __store__,
})
```