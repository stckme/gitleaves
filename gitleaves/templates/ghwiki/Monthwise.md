{% for month, people in people_by_month.items() %}

## {{ month }}  

{% for name, days in people.items() %}  
**{{ name }} :**  

{%- for day in days %}  
{{ day.strftime('%Y-%m-%d') }}  
{%- endfor %}  

{% endfor %}

{% endfor %}
