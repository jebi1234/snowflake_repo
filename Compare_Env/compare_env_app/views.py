from django.shortcuts import render
import snowflake.connector

# Replace with your actual Snowflake credentials
SNOWFLAKE_CONFIG = {
    'dev': {
        'user': 'XXXXXX',
        'password': 'XXXXXX',
        'account': 'XXXXXX',
        'warehouse': 'XXXXXX',
        'database': 'XXXXXX',
        'schema': 'XXXXXX'
    },
    'qa': {
        'user': 'XXXXXX',
        'password': 'XXXXXX',
        'account': 'XXXXXX',
        'warehouse': 'XXXXXX',
        'database': 'XXXXXX',
        'schema': 'XXXXXX'
    }
}

def get_tables_and_views(config):
    ctx = snowflake.connector.connect(**config)
    cs = ctx.cursor()
    try:
        cs.execute("SHOW TABLES")
        tables = {row[1] for row in cs.fetchall()}
        cs.execute("SHOW VIEWS")
        views = {row[1] for row in cs.fetchall()}
        return tables, views
    finally:
        cs.close()
        ctx.close()

def compare_envs(request):
    result = None
    if request.method == 'POST':
        env1 = request.POST['env1']
        env2 = request.POST['env2']

        tables1, views1 = get_tables_and_views(SNOWFLAKE_CONFIG[env1])
        tables2, views2 = get_tables_and_views(SNOWFLAKE_CONFIG[env2])

        table_diff = {
            'only_in_' + env1: tables1 - tables2,
            'only_in_' + env2: tables2 - tables1
        }
        view_diff = {
            'only_in_' + env1: views1 - views2,
            'only_in_' + env2: views2 - views1
        }

        result = f"Table Differences:\n{table_diff}\n\nView Differences:\n{view_diff}"

    return render(request, 'compare.html', {'result': result})
