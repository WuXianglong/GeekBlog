PROJECT_NAME = 'geek-blog'

VERSION_CONTROL = "serverdeploy.git"

ROLE_ALIAS = {
    'blog': 'Blog',
    'blog-webfront': 'Blog-Webfront',
}

ROLE_APPS_TABLE = {
    'Blog': ['core', 'blog'],
    'Blog-Webfront': ['blog-webfront'],
}

BUILD_HANDLER_CONFIG = (
    'serverdeploy.handlers.ConfigurationFileHandler',
)
