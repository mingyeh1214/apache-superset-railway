import os

FEATURE_FLAGS = {
    "ENABLE_TEMPLATE_PROCESSING": True,
}

ENABLE_PROXY_FIX = True

SECRET_KEY = os.environ.get("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE")
# i18n: 預設繁體中文。LANGUAGES whitelist 控制 user Settings → Info 下拉選單,
# 只留中英文避免 30 種語系雜訊;flag = ISO-3166 alpha-2 國家代碼,Superset
# UI 拿來算 emoji 國旗。
BABEL_DEFAULT_LOCALE = "zh_TW"
LANGUAGES = {
    "zh_TW": {"flag": "tw", "name": "繁體中文"},
    "zh": {"flag": "cn", "name": "简体中文"},
    "en": {"flag": "us", "name": "English"},
}
