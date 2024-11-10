from flask import render_template, request

icon = None
meta = None
title_header = None

def initialize_app_data(return_favicon_func, return_meta_func, return_title_func):
    global icon, meta, title_header
    icon = return_favicon_func()
    meta = return_meta_func()
    title_header = return_title_func()

def compiler(element):
    data = element.render()
    tag = data["tagName"]
    children = data["children"]
    content = children[0] if len(children) > 0 else ""
    props = children[1] if len(children) > 1 else {}

    html_str = f"<{tag}"
    if props:
        for key, value in props.items():
            html_str += f' {key}="{value}"'
    html_str += f">{content}</{tag}>"

    return html_str

def render(content, Layout, title=None):
    converted = None
    try:
        converted = Layout(compiler(content)).render()
    except TypeError:
        converted = Layout(content.render()).render()

    if title:
        return render_template("main.html", content=converted, icon=icon, title=title, meta=meta)
    else:
        return render_template("main.html", content=converted, icon=icon, title=title_header, meta=meta)

def compare_dy_url(url):
    if url != "home":
        return request.path.startswith(url)
    else:
        return request.path == "/"
