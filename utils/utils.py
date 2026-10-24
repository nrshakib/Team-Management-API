from rest_framework.response import Response


def api_response(
        message, data = None, status_text = 'Success', http_status = 200
):
    return Response({
        "message": message,
        "status_text": status_text,
        "data": data,
    }, status = http_status)