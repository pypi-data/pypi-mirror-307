from flask import url_for


def use_title(init):
  title = {"title": init}

  def setTitle(new):
    title["title"] = new

  def getTitle():
    return title["title"]

  return getTitle, setTitle


def use_favicon(path):
  icon = {
      "icon":
      f'''\n <link rel="icon" type="image/x-icon" href="../assets/{path}" /> \n'''
  }

  def setFavicon(new):
    icon[
        "icon"] = f'''\n <link rel="icon" type="image/x-icon" href="../assets/{new}" /> \n'''

  def getFavicon():
    return icon["icon"]

  return getFavicon, setFavicon


def use_css(file_path):
  return f"""\n <link href="../assets/{file_path}.css" rel="stylesheet" /> \n"""


def use_img(file_path, type):
  return f"""\n <img src="../assets/{file_path}.{type}" /> \n"""


def use_js(file_path):
  return f"""\n <script src="../assets/{file_path}.js"></script> \n"""


def use_fonts(path):
  return f"""\n <link href="../assets/{path}" rel="stylesheet" /> \n"""


def use_google_fonts(url):
  return f"""\n <link href="https://fonts.googleapis.com/css?family={url}" rel="stylesheet" /> \n"""


def use_icons(path):
  return f"""\n <link href="../assets/{path}" rel="icon" /> \n"""


def use_bootstrap_icons():
  return """\n <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css"> \n"""


def use_external_script(url):
  return f"""\n <script src="{url}"></script> \n"""


def use_link(url):
  return url_for(url) or f"/{url}"


def use_link_with_params(url, **kwargs):
  return url_for(url, **kwargs) or f"/{url}"

def use_asset(file):
  return f"../assets/{file}"

def use_tailwind():
  return "\n <script src=\"https://cdn.tailwindcss.com\"></script> \n"

def use_tailwind_config(file):
  return f"\n <script src=\"../assets/{file}\"></script> \n"

def use_meta(meta_info):
  tags = []
  for name, content in meta_info.items():
      tags.append(f'<meta name="{name}" content="{content}"> \n')
  return '\n'.join(tags)

def use_bootstrap_components():
  return "\n https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css \n"
  from flask import url_for


def use_title(init):
  title = {"title": init}

  def setTitle(new):
    title["title"] = new

  def getTitle():
    return title["title"]

  return getTitle, setTitle


def use_favicon(path):
  icon = {
      "icon":
      f'''\n <link rel="icon" type="image/x-icon" href="../assets/{path}" /> \n'''
  }

  def setFavicon(new):
    icon[
        "icon"] = f'''\n <link rel="icon" type="image/x-icon" href="../assets/{new}" /> \n'''

  def getFavicon():
    return icon["icon"]

  return getFavicon, setFavicon


def use_css(file_path):
  return f"""\n <link href="../assets/{file_path}.css" rel="stylesheet" /> \n"""


def use_img(file_path, type):
  return f"""\n <img src="../assets/{file_path}.{type}" /> \n"""


def use_js(file_path):
  return f"""\n <script src="../assets/{file_path}.js"></script> \n"""


def use_fonts(path):
  return f"""\n <link href="../assets/{path}" rel="stylesheet" /> \n"""


def use_google_fonts(url):
  return f"""\n <link href="https://fonts.googleapis.com/css?family={url}" rel="stylesheet" /> \n"""


def use_icons(path):
  return f"""\n <link href="../assets/{path}" rel="icon" /> \n"""


def use_bootstrap_icons():
  return """\n <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.3.0/font/bootstrap-icons.css"> \n"""


def use_external_script(url):
  return f"""\n <script src="{url}"></script> \n"""


def use_link(url):
  return url_for(url) or f"/{url}"


def use_link_with_params(url, **kwargs):
  return url_for(url, **kwargs) or f"/{url}"

def use_asset(file):
  return f"../assets/{file}"

def use_tailwind():
  return "\n <script src=\"https://cdn.tailwindcss.com\"></script> \n"

def use_tailwind_config(file):
  return f"\n <script src=\"../assets/{file}\"></script> \n"

def use_meta(meta_info):
  tags = []
  for name, content in meta_info.items():
      tags.append(f'<meta name="{name}" content="{content}"> \n')
  return '\n'.join(tags)

def use_bootstrap_components():
  return "\n https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css \n"
  