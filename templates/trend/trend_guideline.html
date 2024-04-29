{% extends "maintemplate.html"%}
{% block css %}
<style>
    * {
        border-style: dotted 1px black;
        font-family: "Noto Sans KR", sans-serif;
        font-optical-sizing: auto;
        list-style-type: none;
        text-decoration: none;
        color: black;
        text-decoration-line: none;


    }

    #field {
        font-size: larger;
        font-weight: bold;
    }

    a,
    li * {
        text-decoration: none;
        color: black;
        text-decoration-line: none;


        ;
    }
</style>
{% endblock css %}

{% block main_container %}
<h4 class="text-center m-3 fw-bold" width="100%" height="100px"> <a href="/trend/trend_guideline">고시·지침</a> </h4>

<div class="justify-content-center row">
    <div class="row col-7 justify-content-center" style="align-items: center;">
        <div class="col-3">
            <select class="form-control" style="border-radius: 25px;" name="key_name">
                <option value="dise_name_kr"> 제목</option>
            </select>
        </div>
        <div class="col-6">
            <input class="form-control" style="border-radius: 0px;" placeholder="Enter Search!" name="search_word"
                value="{{request._query_params.word}}">
        </div>
        <div class="col-2">
            <button type="submit" style="border:none; background: none;" formaction="/manag/manag_QnA_main"
                formmethod="get"><svg width="32" height="32" viewBox="0 0 80 80" fill="none"
                    xmlns="http://www.w3.org/2000/svg">
                    <g filter="url(#filter0_d_7_45)">
                        <path
                            d="M5 40C5 20.67 20.67 5 40 5C59.33 5 75 20.67 75 40C75 59.33 59.33 75 40 75C20.67 75 5 59.33 5 40Z"
                            fill="#04CBFC" fill-opacity="0.47" shape-rendering="crispEdges" />
                    </g>
                    <path d="M35 50L45 40L35 30" stroke="white" stroke-width="5" stroke-linecap="round" />
                    <defs>
                        <filter id="filter0_d_7_45" x="0" y="0" width="80" height="80" filterUnits="userSpaceOnUse"
                            color-interpolation-filters="sRGB">
                            <feFlood flood-opacity="0" result="BackgroundImageFix" />
                            <feColorMatrix in="SourceAlpha" type="matrix"
                                values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 127 0" result="hardAlpha" />
                            <feOffset />
                            <feGaussianBlur stdDeviation="2.5" />
                            <feComposite in2="hardAlpha" operator="out" />
                            <feColorMatrix type="matrix" values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.25 0" />
                            <feBlend mode="normal" in2="BackgroundImageFix" result="effect1_dropShadow_7_45" />
                            <feBlend mode="normal" in="SourceGraphic" in2="effect1_dropShadow_7_45" result="shape" />
                        </filter>
                    </defs>
                </svg>
            </button>
        </div>
    </div>
</div>


<div class="container" style="width: 80%">
    <hr>
    {% for guideline in guidelines %}
    <div class="container" style="width: 80%;" onclick="location.href='/trend/trend_guideline_read/{{guideline.id}}'">
        <h7 class="category">
            {% if guideline.post_cate==None %}
            <p></p>
            {% else %}
            <a href="/trend/trend_guideline_read/{{guideline.id}}" style="color: #4b4b4b;" class="">
                분류 : {{guideline.post_cate}}
                {% endif %}</a>
        </h7>
        <div class="tit">
            <h5 class="">
                {% if guideline.post_title==None %}
                <p></p>
                {% else %}
                <a href="/trend/trend_guideline_read/{{guideline.id}}" class="">
                    {{guideline.post_title}}
                    {% endif %}
                </a>
            </h5>
        </div>
        <div class="sub row justify-content-between">
            <h7 class="name col-3">
                {% if guideline.order_number==None %}

                {% else %}
                <a href="/trend/trend_guideline_read/{{guideline.id}}" class="">
                    발령번호 : {{guideline.order_number}}
                    {% endif %}</a>
            </h7>
            <h7 class="name col-3">
                {% if guideline.date_legislation==None %}
                {% else %}
                <a href="/trend/trend_guideline_read/{{guideline.id}}" class="">
                    제·개정일 : {{guideline.date_legislation}}
                    {% endif %}
                </a>
            </h7>
            <h7 class="name col-3"> <a href="/trend/trend_guideline_read/{{guideline.id}}" class="">
                    {% if guideline.date_start==None %}
                    {% else %}
                    시행일 : {{guideline.date_start}}
                    {% endif %}</a></p>
            </h7>

        </div>
    </div>
    <hr>
    {% endfor %}
</div>

<nav aria-label="Page navigation">
    <ul class="pagination justify-content-center">
        <li class="page-item {{ '' if pagination.has_previous_block else 'disabled' }}">
            <button style="border: none; background: none;" type="submit" class="page-link"
                formaction="/trend/trend_news/{{pagination.first_page}}">
                <svg width="21" height="18" viewBox="0 0 21 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M18 3L12 9L18 15" stroke="#696969" stroke-width="5" stroke-linecap="round" />
                    <path d="M10 3L4 9L10 15" stroke="#696969" stroke-width="5" stroke-linecap="round" />
                </svg>
            </button>
        </li>
        <li class="page-item {{ '' if pagination.has_previous_page else 'disabled' }}">
            <button style="border: none; background: none;" type="submit" class="page-link"
                formaction="/trend/trend_news/{{pagination.previous_page}}"><svg width="13" height="18"
                    viewBox="0 0 13 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10 3L4 9L10 15" stroke="#696969" stroke-width="5" stroke-linecap="round" />
                </svg></button>
        </li>
        {% for page_num in pagination.current_page_range %}
        <li class=" page-item {{ 'active' if page_num == pagination.current_page else '' }}">
            <button style="border: none; background: none; color: black;" type=" submit" class="page-link"
                formaction="/trend/trend_news/{{ page_num }}">
                {{page_num}}
            </button>
        </li>
        {% endfor %}
        <li class=" page-item {{ '' if pagination.has_next_page else 'disabled' }}">
            <button style="border: none; background: none;" type=" submit" class="page-link"
                formaction="/trend/trend_news/{{ pagination.next_page }}"><svg width="13" height="18"
                    viewBox="0 0 13 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 15L9 9L3 3" stroke="#696969" stroke-width="5" stroke-linecap="round" />
                </svg>
                <path d="M4 0V22" stroke="#EDEDED" stroke-width="7" />
                </svg>
            </button>
        </li>
        <li class=" page-item {{ '' if pagination.has_next_block else ' disabled' }}">
            <button style="border: none; background: none;" type=" submit" class="page-link"
                formaction="/trend/trend_news/{{ pagination.last_page }}">
                <svg width="21" height="18" viewBox="0 0 21 18" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 15L9 9L3 3" stroke="#696969" stroke-width="5" stroke-linecap="round" />
                    <path d="M11 15L17 9L11 3" stroke="#696969" stroke-width="5" stroke-linecap="round" />
                </svg>
            </button>
        </li>
    </ul>
</nav>
{% endblock main_container %}