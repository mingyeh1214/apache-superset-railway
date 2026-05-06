import copy
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

# Talisman CSP: 擴充 img-src 白名單,讓 Supabase auth raw_user_meta_data 內
# 的 OAuth avatar(Google/GitHub/Gravatar)能在 Table chart 啟用「Render
# columns in HTML format」後正常載入。
#
# superset.config 在檔案最末端才執行 `from superset_config import *`(主檔
# line 2611),而預設 TALISMAN_CONFIG 在 line 2149 就已定義,因此這裡反向
# import 拿到的是已具名的 dict;deepcopy 後 extend img-src,可保留 mapbox /
# OpenStreetMap / 主題字型 / scarf 遙測等其他預設來源,避免整包覆寫。
from superset.config import TALISMAN_CONFIG as _DEFAULT_TALISMAN  # noqa: E402

TALISMAN_CONFIG = copy.deepcopy(_DEFAULT_TALISMAN)
TALISMAN_CONFIG["content_security_policy"]["img-src"].extend(
    [
        "https://*.googleusercontent.com",       # Google OAuth (lh3-lh6 CDN)
        "https://avatars.githubusercontent.com",  # GitHub OAuth
        "https://*.gravatar.com",                 # Gravatar 備援
    ]
)
