# Multi-Agent Assistant

Multi-Agent Research & Decision Assistant — это multi-agent система на базе LangGraph, предназначенная для обработки сложных пользовательских запросов через управляемый workflow.

Проект создавался как система, в которой разделение ролей действительно оправдано:

- один агент определяет тип задачи,
- другой собирает рабочий материал,
- третий пишет финальный ответ,
- четвёртый проверяет качество и при необходимости отправляет ответ на доработку.

---

## 1. Цель проекта

Цель проекта — построить **управляемый multi-agent workflow**, когда один LLM-call уже недостаточно хорошо контролирует задачу.

В отличие от single-shot генерации, здесь запрос проходит несколько стадий:
- routing,
- research,
- drafting,
- review,
- optional revision.

---

## 2. Почему не один LLM-call

Если задача сводится к ответу на вопрос, одного хорошего LLM-вызова часто достаточно.

Однако этот проект решает другой класс задач:  
**подготовка структурированного, проверенного ответа по сложному запросу**.

Примеры таких запросов:
- сравнить два подхода,
- подготовить decision memo,
- сделать аналитический разбор,
- построить практический план действий.

Для таких задач важно:
- разделить этапы reasoning,
- сделать routing,
- подготовить рабочие notes,
- отдельно сформировать финальный ответ,
- отдельно проверить его качество.

Именно поэтому здесь используется **multi-agent workflow**, а не один универсальный prompt.

---

## 3. Основные возможности

### Workflow layer
- graph-based orchestration через **LangGraph**
- typed shared state
- routing по типу задачи
- reviewer loop с возможностью revision

### Agents
- `router`
- `researcher`
- `writer`
- `reviewer`

### Tools
- local knowledge lookup
- structured note scaffold
- task-specific decision / comparison / plan / analysis framing

### API
- FastAPI endpoint для запуска workflow
- structured response
- logging graph transitions

---

## 4. Архитектура

### High-level flow

```text
user request
-> router
-> researcher
-> writer
-> reviewer
   -> approve -> final answer
   -> revise -> writer again
```

## 5. Роли агентов

Одна из важных целей проекта — избежать ситуации, когда несколько агентов делают почти одно и то же.

Для этого роли были специально разведены:

### Router
Определяет тип задачи.
Поддерживаемые task types:
- comparison
- decision
- plan
- analysis

### Researcher
Собирает internal research notes, а не пишет финальный ответ.

Задача researcher:
- извлечь факты,
- собрать options,
- выделить pros / cons / risks,
- подготовить материал для writer.

### Writer
Преобразует internal notes в user-facing structured answer.

Writer является task-aware:
- для comparison пишет один формат,
- для decision — другой,
- для analysis — третий,
- для plan — четвёртый.

### Reviewer
Проверяет ответ:
- по общим критериям качества,
- по критериям конкретного task type.

Если ответ недостаточно хорош, reviewer отправляет его на revise.

## 5. Структура проекта
```
app/
  agents/
    router.py
    researcher.py
    writer.py
    reviewer.py
  api/
    routes/
      run_workflow.py
    schemes/
      workflow.py
  core/
    config.py
    logging.py
  graph/
    nodes.py
    state.py
    workflow.py
  llm/
    client.py
  tools/
    local_knowledge.py
    structured_note_tool.py
    decision_frame_tool.py
data/
  knowledge/
    knowledge.json
```

---
## 6. Состояния графа

В графе используется общее состояние, которое живёт на протяжении всего workflow.

Основные поля:
- user_query
- task_type
- research_notes
- draft_answer
- review_feedback
- final_answer
- revision_count
- max_revisions
- next_step

---
## 7. Вспомогательные инструменты
Проект использует не один, а несколько вспомогательных инструментов.

### local_knowledge_tool

Используется для получения базового контекста из локального knowledge store.

### structured_note_tool

Помогает researcher не стартовать с пустого листа, а работать с более удобным scaffold для заметок.

### decision_frame_tool

Даёт task-specific framing:
- decision frame
- comparison frame
- planning frame
- analysis frame

---

## 8. Task-aware генерация

Одна из ключевых идей проекта — один и тот же запросный pipeline не должен писать одинаковые ответы для разных типов задач.

### comparison

Фокус:
- side-by-side comparison
- balanced trade-offs
- where each option fits better
- balanced conclusion

### decision

Фокус:
- decision context
- options
- recommendation
- rationale
- risks
- next step

### analysis

Фокус:
- situation summary
- observations
- interpretation
- implications
- practical takeaway

### plan

Фокус:
- objective
- steps
- dependencies
- risks
- execution order

---

## 9. Демо сценарии
### 1 — Comparison

**Input**:
Compare monolith and microservices for a small AI startup.

**Detected task type**:
comparison

**Что демонстрирует**:
Система не выдаёт recommendation memo, а строит сравнительный ответ с trade-offs и best-fit scenarios для каждого варианта.

---

### 2 — Decision

**Input**:
Prepare a decision memo on whether a small AI startup should start with a monolith or microservices.

**Detected task type**:
decision

**Что демонстрирует**:

Workflow формирует recommendation-oriented output с явной рекомендацией, rationale, risks и next step.

---

### 3 — Analysis
**Input**:
Analyze the risks and long-term implications of adopting microservices too early in a small AI product.

**Detected task type**:
analysis

**Что демонстрирует**:

Система пишет интерпретационный аналитический ответ, а не decision memo. Формат отличается по структуре и акценту.

---

### 4 — Plan

**Input**:
Create a practical plan for moving a small AI backend from monolith to microservices, including prerequisites, rollout risks, and fallback steps if the migration goes badly.

**Detected task type**:
plan

**Revision count**:
1

**Что демонстрирует**:

Пример того, что reviewer loop действительно работает.
Ответ был отправлен на revision и затем доработан до более полного execution-oriented плана.
---

## 10. API

**POST /workflow/run**

Пример request:
```json
{
  "query": "Prepare a decision memo on whether a small AI startup should start with a monolith or microservices."
}
```
Пример response:
```json
{
  "task_type": "decision",
  "research_notes": "...",
  "final_answer": "...",
  "revision_count": 0
}
```
---
## 11. Как запустить проект
Установить зависимости
```
pip install -r requirements.txt
```
Создать .env
```
LLM_API_KEY=
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL_NAME=openai/gpt-4o-mini
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1200
MAX_REVISIONS=2
```
Запустить API
```
uvicorn app.main:app --reload
```

## 12. Стек технологий
- Python
- FastAPI
- LangGraph
- LangChain OpenAI client
- OpenRouter