from jinja2 import Template

OUTPUT_FILE = 'out.sol'

CONTRACT_TEMPLATE = Template('''
    pragma ton-solidity >= 0.39.0;
    contract {{ contract_name }} {
        {% for variable in variables -%}
            {{ variable }}
        {% endfor %}
    {%- for function in functions -%}
        {{ function }}
    {% endfor %}
    }
''')

VARIABLE_TEMPLATE = Template('''{{ type }} {{ name }}{% if default_value %} = {{default_value}}{% endif %};''')

FUNCTION_TEMPLATE = Template('''
    function {{ function_name }}(
    {%- for arg_name, arg_type in function_args -%}
        {{ arg_type }} {{ arg_name }}{% if not loop.last %}, {% endif %}
    {% endfor %}
    ) {{ access }} returns ( {% for return_type in return_types %} {{ return_type }} {% endfor %}){
        {%- for code_line in code -%}
            {{ code_line }}
        {% endfor %}
    }
''')
