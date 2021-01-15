# 과목 테스트 설정 작성 매뉴얼

과목 테스트 설정은 다음과 같이 YAML 포맷으로 작성해주시면 됩니다.

```yaml
interface_types:
    {인터페이스_타입1}:
        share_peek_view: true
        share_code: true
        show_peek_view: false
        show_code: false
        show_chat: false
    {인터페이스_타입2}:
        share_peek_view: true
        share_code: true
        show_peek_view: true
        show_code: true
        show_chat: true
    {인터페이스_타입3}:
        ...
user_types:
    {사용자_타입1}:
        weight: {비중1}
        interface_map:
            {자료_경로1}: {인터페이스_타입1}
            {자료_경로2}: {인터페이스_타입2}
    {사용자_타입2}:
        weight: {비중2}
        interface_map:
            {자료_경로1}: {인터페이스_타입2}
            {자료_경로2}: {인터페이스_타입1}
```

간략하게 이 설정을 해석해보면, 해당 과목에 **수강** 신청하는 사용자들을
**비중1**:**비중2**의 비율로 **사용자_타입1**과 **사용자_타입2** 중 
하나에 속하도록 하고, 
각 **사용자_타입**의 사용자들에게 **자료_경로**에 해당하는 자료를 보여줄 때
정해진 **인터페이스_타입**을 강제로 적용해서 보여주도록 한다는 뜻입니다. 

여기서 **인터페이스_타입**은 **snake_case**로 적절한 이름을 각각 정해주시면 되며, 
원하면 두 가지 이상도 정의할 수 있습니다. **사용자_타입** 역시 **snake_case**로 
적절한 이름을 각각 정해주시면 됩니다. 

**비중**으로는 자연수를 써 주시고, **자료_경로**는 다음과 같이 작성하시면 됩니다.

```yaml
{자료 타입}/{사용자명}/{자료 ID}
```

이 설정에 **자료_경로**로 포함되지 않은 자료들은, 사용자의 개인 설정을 반영한
인터페이스로 표시되게 됩니다. 

아래는 파이썬 기초 강의의 테스트 설정 예시입니다.

```yaml
interface_types:
    classic:
        share_peek_view: true
        share_code: true
        show_peek_view: false
        show_code: false
        show_chat: false
    modern:
        share_peek_view: true
        share_code: true
        show_peek_view: true
        show_code: true
        show_chat: true
user_types:
    classic_to_modern:
        weight: 50
        interface_map:
            projects/cocode/python-comment: classic
            projects/cocode/python-variable: modern
    modern_to_classic:
        weight: 50
        interface_map:
            projects/cocode/python-comment: modern
            projects/cocode/python-variable: classic
```

이렇게 작성된 과목 내용은 정적으로 이 과목에 저장되므로, 
여기 포함된 **자료**의 ID가 변경되거나 할 경우 이 설정 내용도
같이 직접 바꿔주셔야 하는 점 유의해주시기 바랍니다. 