{% extends "maintemplate.html" %}

{% block main_container %}

<form action="">
  <div class="row justify-content-between">
    <div class="col-1 fw-bold fs-2 text-start">QnA</div>
    <div class="col-3">
      <select class="form-control" name="key_name">
        <option value="ques_title" {{ 'selected' if request._query_params.key_name=='ques_title' else '' }}>제목
        </option>
      </select>
    </div>
    <div class="col-6">
      <input class="form-control" placeholder="Enter Search!" name="search_word" value="{{request._query_params.word}}">
    </div>
    <div class="col-2">
      <button type="submit" class="btn btn-primary" formaction="/other/other_QnA" formmethod="get">검색</button>
    </div>
  </div>
  </div>
  <hr>
  <div style="text-align: end;">
    <a class="btn btn-success" href="/other/other_QnA_write">글쓰기</a>
  </div>
  <table class="table table-hover">
    <thead>
      <tr>
        <th>번호</th>
        <th>질문</th>
        <th>작성자</th>
        <th>작성일</th>
        <th>답변</th>
      </tr>
    </thead>
    <tbody>
      {% for QnA in QnAs %}
      <tr onclick="location.href='/other/other_QnA_read/{{QnA.id}}'" style="cursor: pointer;">
        <td>{{pagination.total_records - (pagination.start_record_number + loop.index0) + 1}}</td>
        <td id="readpage">{{QnA.ques_title}}</td>
        <td>{{QnA.ques_writer}}</td>
        <td>{{QnA.ques_time.date()}}</td>
        <td>{%if QnA.ques_answer %}
          답변완료
          {% else %}
          <div class="text-primary">답변대기</div>
          {% endif%}
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  <nav aria-label="Page navigation">
    <ul class="pagination justify-content-center">
      <li class="page-item {{ '' if pagination.has_previous_block else 'disabled' }}">
        <button type="submit" class="page-link"
          formaction="/other/other_QnA_main/{{pagination.first_page}}?{% if request._query_params.key_name %}key_name={{ request._query_params.key_name|urlencode }}{% endif %}{% if request._query_params.search_word %}&search_word={{ request._query_params.search_word|urlencode }}{% endif %}" formmethod="get">
          맨 처음
        </button>

      </li>
      <li class="page-item {{ '' if pagination.has_previous_page else 'disabled' }}">
        <button type="submit" class="page-link"
          formaction="/other/other_QnA_main/{{pagination.previous_page}}?{% if request._query_params.key_name %}key_name={{ request._query_params.key_name|urlencode }}{% endif %}{% if request._query_params.search_word %}&search_word={{ request._query_params.search_word|urlencode }}{% endif %}" formmethod="get">이전</button>
      </li>
      {% for page_num in pagination.current_page_range %}
      <li class="page-item {{ 'active' if page_num == pagination.current_page else '' }}">
        <button type="submit" class="page-link"
          formaction="/other/other_QnA_main/{{ page_num }}?{% if request._query_params.key_name %}key_name={{ request._query_params.key_name|urlencode }}{% endif %}{% if request._query_params.search_word %}&search_word={{ request._query_params.search_word|urlencode }}{% endif %}" formmethod="get">
          {{page_num}}
        </button>
      </li>
      {% endfor %}
      <li class="page-item {{ '' if pagination.has_next_page else 'disabled' }}">
        <button type="submit" class="page-link"
          formaction="/other/other_QnA_main/{{ pagination.next_page }}?{% if request._query_params.key_name %}key_name={{ request._query_params.key_name|urlencode }}{% endif %}{% if request._query_params.search_word %}&search_word={{ request._query_params.search_word|urlencode }}{% endif %}" formmethod="get">다음</button>
      </li>
      <li class="page-item {{ '' if pagination.has_next_block else 'disabled' }}">
        <button type="submit" class="page-link"
          formaction="/other/other_QnA_main/{{ pagination.last_page }}?{% if request._query_params.key_name %}key_name={{ request._query_params.key_name|urlencode }}{% endif %}{% if request._query_params.search_word %}&search_word={{ request._query_params.search_word|urlencode }}{% endif %}" formmethod="get">
          맨 끝
        </button>
      </li>
    </ul>
  </nav>
</form>
{% endblock %}