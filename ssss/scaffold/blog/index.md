Title: Blog
Description: Blog posts
changefreq: weekly
priority: 1.0

# Blog

A collection of writings.

## Posts

{% for post in posts("blog") -%}
- [{{ post.title }}]({{ post.url }}){% if post.date %} — {{ post.date }}{% endif %}
{% endfor %}
