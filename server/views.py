from django.http import JsonResponse
from api_project.clickhouse_client import get_clickhouse_client

def clickhouse_test(request):
    client = get_clickhouse_client()
    result = client.query('SELECT now()')
    return JsonResponse({'clickhouse_time': result.result_rows[0][0]})
