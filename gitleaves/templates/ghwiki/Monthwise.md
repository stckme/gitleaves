{% for month, people in people_by_month.items() %}

## {{ month }}  

{% for name, days in people.items() %}  

### {{ name }}  

{%- for day in days %}  
1. {{ day.strftime('%Y-%m-%d') }}  
{%- endfor %}  
{% endfor %}  
<br>  
{% endfor %}
