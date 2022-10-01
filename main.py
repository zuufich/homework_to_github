import json
from flask import Flask

app = Flask(__name__)

data = []


def load_candidates():
    # загрузит данные из файла
    global data
    with open('candidates.json') as f:
        data = json.load(f)


def get_all():
    # покажет всех кандидатов
    if not data:
        load_candidates()
    print(data)


def get_by_pk(pk):
    # вернет кандидата по pk
    for candidate in data:
        if candidate["pk"] == pk:
            return candidate


def get_by_skill(skill_name):
    # вернет кандидатов по навыку
    candidates = []
    for candidate in data:
        if skill_name.lower() in candidate["skills"].lower():
            # Поиск по навыку не зависит от регистра
            candidates.append(candidate)
    return candidates


@app.route('/')
# представление для роута / (главная страница)
def index():
    # список в формате (тег <pre> - преформатирование)
    res = """
            <pre>"""
    load_candidates()
    for candidate in data:
        res += f"""Имя кандидата - {candidate["name"]}
{candidate["position"]}
{candidate["skills"]}

"""
    res += """
            </pre>
            """
    return res


@app.route('/candidates/<int:x>')
# представление для роута candidates/<x>
def single_candidate(x):
    # выводил данные про кандидата
    load_candidates()
    candidate = get_by_pk(x)
    res = f"""
<img src="{candidate["picture"]}">

<pre>
Имя кандидата - {candidate["name"]} 
{candidate["position"]}
{candidate["skills"]}
</pre>

"""
    return res


@app.route('/skills/<x>')
# представление /skills/<x> для поиска по навыкам
def candidate_with_skill(x):
    # Выводит тех кандидатов, в списке навыков у которых содержится skill
    res = """
            <pre>"""
    load_candidates()
    candidates = get_by_skill(x)
    for candidate in candidates:
        res += f"""Имя кандидата - {candidate["name"]}
{candidate["position"]}
{candidate["skills"]}

"""
    res += """
            </pre>
            """
    return res


if __name__ == '__main__':
    # flask
    app.run(port=8080, host='127.0.0.1')

    get_all()
    load_candidates()
    print(get_by_skill("python"))
