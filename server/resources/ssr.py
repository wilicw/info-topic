# -*- encoding: utf8-*-
import os
import model
from flask import Flask, Blueprint, render_template
from entities import config

app = Flask(__name__, static_url_path='', static_folder=config.static_path)
api_bp = Blueprint("ui", __name__, url_prefix="/",
                   template_folder=config.static_path)


class SEO(object):
  description = ""
  key = ""
  tags = ""
  author = ""
  title = ""
  image = ""


@api_bp.route('/js/<path:path>')
def send_js(path):
  return app.send_static_file(os.path.join('js', path))


@api_bp.route('/css/<path:path>')
def send_css(path):
  return app.send_static_file(os.path.join('css', path))


@api_bp.route('/', defaults={'path': ''})
@api_bp.route('/<path:path>')
def ui_render(path):
  path = os.path.split(path)
  page = list(filter(lambda x: len(x) > 0, path))
  if page == None or len(page) == 0:
    page = ['']
  seo = SEO()
  if page[0] == "":
    seo.title = f"首頁 || {config.title}"
    seo.description = f"大安高工資訊科學生專題製作展示與成果發表之平臺。"
  elif page[0] == "year":
    seo.title = f"{path[1]} 年專題 || {config.title}"
    seo.description = f"{path[1]} 年專題列表"
  elif page[0] == "rank":
    seo.title = f"{path[1]} 年度專題排名 || {config.title}"
    seo.description = f"{path[1]} 年專題排行榜"
  elif page[0] == "search":
    seo.title = f"搜尋 || {config.title}"
    seo.description = "輸入關鍵字以搜尋專題"
  elif page[0] == "teachers":
    seo.title = f"指導老師 || {config.title}"
    seo.description = "當年度指導老師列表"
  elif page[0] == "reference":
    seo.title[0] = f"參考資料 || {config.title}"
    seo.description = "專題製作參考資料"
  elif page[0] == "login":
    seo.title = f"登入 || {config.title}"
    seo.description = f"登入{config.title}"
  elif len(page) > 1 and page[0] == "topic":
    uuid = str(page[1])
    result = model.Project.query.filter_by(uuid=uuid).first()
    if result != None:
      __project = result.to_detail()
      seo.title = f"{__project['title']} || {config.title}"
      seo.description = __project['description']
      seo.image = __project['cover']
      seo.keywords = __project['keywords']
      seo.author = ",".join(__project['students'])
  else:
    seo.title = f"{config.title}"

  return render_template('index.html', **seo.__dict__)


app.register_blueprint(api_bp)
