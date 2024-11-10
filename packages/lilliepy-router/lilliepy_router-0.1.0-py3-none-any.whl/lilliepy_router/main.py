from flask import request, url_for, redirect


def use_router(url):
  return url == request.path


def use_dynamic_router(base_url):
  path = request.path
  base_url = base_url.rstrip('/')
  path = path.rstrip('/')
  if path.startswith(base_url):
    return True
  return False


def goto(url_name, options=None):
  if (options):
    return redirect(url_for(url_name), options)
  else:
    return redirect(url_for(url_name))


def returnurl(url):
  if url != "current":
    return url_for(url)
  else:
    return request.path
