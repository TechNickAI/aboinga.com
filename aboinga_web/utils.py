def get_real_ip(request):
    """ Get the IP from the proxy (varnish, cdn) if one is used"""
    if "HTTP_X_FORWARDED_FOR" in request.META:
        # multiple proxies, take the first one
        if ',' in request.META["HTTP_X_FORWARDED_FOR"]:
            parts = request.META["HTTP_X_FORWARDED_FOR"].split(',')
            return parts[0].strip()
        else:
            return request.META["HTTP_X_FORWARDED_FOR"]
    else:
        return request.META["REMOTE_ADDR"]
