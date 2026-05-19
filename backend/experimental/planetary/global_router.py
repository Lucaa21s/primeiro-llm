

def route_request(region, request):

    return {
        "region": region,
        "request": request,
        "status": "routed",
    }
