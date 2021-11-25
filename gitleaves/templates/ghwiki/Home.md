# Leaves Dashboard

## Today

{% for name in today_leaves %}
- {{name}}
{% endfor %}

{% for month, leaves in next_leaves_by_month %}

## {{month}}

| Date | Name |
| -----|------|
{% for date, names in leaves.items() %}
| {{date.strftime('%d')}} | {{names|join(', ')}} |
{% endfor %}
{% endfor %}

