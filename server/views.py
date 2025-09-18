from django.http import JsonResponse


def clickhouse_test(request):
    return JsonResponse({"clickhouse_time": "not use"})
