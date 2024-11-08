/* For examples of how to fill out the macros please refer to the postgres adapter and docs
postgres adapter macros: https://github.com/dbt-labs/dbt-core/blob/main/plugins/postgres/dbt/include/postgres/macros/adapters.sql
dbt docs: https://docs.getdbt.com/docs/contributing/building-a-new-adapter
*/

{% macro maxcompute__truncate_relation(relation) -%}
    {% if relation.is_table -%}
        {% if relation.schema -%}
            TRUNCATE TABLE {{ relation.database }}.{{ relation.schema }}.{{ relation.identifier }};
        {% else -%}
            TRUNCATE TABLE {{ relation.database }}.{{ relation.identifier }};
        {% endif -%}
    {% endif -%}
{% endmacro %}

{% macro maxcompute__rename_relation(from_relation, to_relation) -%}
    {% if from_relation.schema -%}
        {% if from_relation.is_table -%}
            ALTER TABLE {{ from_relation.database }}.{{ from_relation.schema }}.{{ from_relation.identifier }}
            RENAME TO {{ to_relation.identifier }};
        {% else -%}
            ALTER VIEW {{ from_relation.database }}.{{ from_relation.schema }}.{{ from_relation.identifier }}
            RENAME TO {{ to_relation.identifier }};
        {% endif -%}
    {% else -%}
        {% if from_relation.is_table -%}
            ALTER TABLE {{ from_relation.database }}.{{ from_relation.identifier }}
            RENAME TO {{ to_relation.identifier }};
        {% else -%}
            ALTER VIEW {{ from_relation.database }}.{{ from_relation.identifier }}
            RENAME TO {{ to_relation.identifier }};
        {% endif -%}
    {% endif -%}
{% endmacro %}

{% macro maxcompute__alter_column_type(relation, column_name, new_column_type) -%}
    {% if relation.schema -%}
        ALTER TABLE {{ relation.database }}.{{ relation.schema }}.{{ relation.identifier }}
        CHANGE {{ column_name }} {{ column_name }} {{ new_column_type }};
    {% else -%}
        ALTER TABLE {{ relation.database }}.{{ relation.identifier }}
        CHANGE {{ column_name }} {{ column_name }} {{ new_column_type }};
    {% endif -%}
{% endmacro %}

{% macro maxcompute__copy_grants() -%}
    {{ return(True) }}
{% endmacro %}

/* {# override dbt/include/global_project/macros/relations/table/create.sql #} */
{% macro maxcompute__create_table_as(temporary, relation, sql) -%}
    {% if relation.schema -%}
        CREATE TABLE IF NOT EXISTS {{ relation.database }}.{{ relation.schema }}.{{ relation.identifier }}
        {% if temporary %}
            LIFECYCLE 1
        {% endif %}
        AS (
            {{ sql }}
        )
    {% else -%}
        CREATE TABLE IF NOT EXISTS {{ relation.database }}.default.{{ relation.identifier }}
        {% if temporary %}
            LIFECYCLE 1
        {% endif %}
        AS (
            {{ sql }}
        )
    {% endif -%}
    ;
{% endmacro %}

/* {# override dbt/include/global_project/macros/relations/view/create.sql #} */
{% macro maxcompute__create_view_as(relation, sql) -%}
    {% if relation.schema -%}
        CREATE OR REPLACE VIEW {{ relation.database }}.{{ relation.schema }}.{{ relation.identifier }} AS (
            {{ sql }}
        );
    {% else -%}
        CREATE OR REPLACE VIEW {{ relation.database }}.default.{{ relation.identifier }} AS (
            {{ sql }}
        );
    {% endif -%}
{% endmacro %}


{% macro maxcompute__current_timestamp() -%}
    current_timestamp()
{%- endmacro %}

-- only change varchar to string, dbt-adapters/dbt/include/global_project/macros/materializations/snapshots/strategies.sql
{% macro maxcompute__snapshot_hash_arguments(args) -%}
    md5({%- for arg in args -%}
        coalesce(cast({{ arg }} as string ), '')
        {% if not loop.last %} || '|' || {% endif %}
    {%- endfor -%})
{%- endmacro %}