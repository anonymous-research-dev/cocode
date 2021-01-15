# 과목 내용 작성 매뉴얼

과목 내용은 다음과 같이 YAML 포맷으로 작성해주시면 됩니다.

```yaml
- {자료 경로}   {제목}
- {자료 경로}   {제목}
- {자료 경로}   {제목}
...
```

여기서 **자료 경로**와 **제목** 사이에는 1개 이상의 연속되는
whitespace 문자를 넣어주시면 되고, **제목**에 포함되어 있는 
1개 이상의 연속되는 whitespace 문자는 모두 1개의 space 문자로
치환됨을 유의해주시기 바랍니다.

**자료 경로**는 다음과 같이 작성하시면 됩니다.

```yaml
{자료 타입}/{사용자명}/{자료 ID}
```

여기서 **자료**는 프로젝트, 문서, 비디오 중 한 가지이며, 각각의 자료 타입은
앞에서 언급된 것과 같은 순서로 `projects`, `articles`, `videos`로
적어주시면 됩니다.

예를 들면, 다음과 같이 파이썬 기초 강의 내용을 작성하는 것이 가능합니다.

```yaml
- articles/cocode/python-intro          What is Python?
- videos/cocode/python                  Introduction to Python
- projects/cocode/python-hello-world    Hello world with Python
- articles/cocode/comment-intro         What are comments?
- projects/cocode/python-comment        Add comments on Python code
- projects/cocode/python-variable       Use variables in Python code
```

이렇게 작성된 과목 내용은 정적으로 이 과목에 저장되므로, 
여기 포함된 **자료**의 ID가 변경되거나 **자료** 자체가 삭제될 경우
과목 페이지에서 해당 **자료**를 열어볼 수 없게 되니 
주의해 주시기 바랍니다.