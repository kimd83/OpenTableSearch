from sqlalchemy.engine.url import URL

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'david',
    'password': '',
    'database': 'findtable'
}

SQLALCHEMY_DATABASE_URI = URL(**DATABASE)

# PIPELINES = ['app.pipelines.FindTablePipeline']
# ITEMS_PIPELINES = ['scraper_app.pipelines.FindTablePipeline']