---
layout: page
title: It Will Never Work in Theory
tagline: Empirical Research Results in Software Engineering
---
{% include JB/setup %}

<table class="table table-striped">
  {% for post in site.posts %}
    <tr><td>{{ post.date | date_to_string | replace: ' ', '&nbsp;'}}</td><td><a href="{{ BASE_PATH }}{{ post.url }}">{{ post.title }}</a></td></tr>
  {% endfor %}
</table>
