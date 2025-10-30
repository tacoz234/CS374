import models
from app import appbuilder
from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

class Topic(ModelView):
    datamodel = SQLAInterface(models.Topic)
    route_base = '/topic'
    list_title = 'Topics'
    list_columns = ['topic_id', 'topic_name']

class History(ModelView):
    datamodel = SQLAInterface(models.History)
    route_base = '/history'
    list_title = 'History'
    list_columns = ['paper_id', 'timestamp', 'paper_status', 'notes']

class Paper(ModelView):
    datamodel = SQLAInterface(models.Paper)
    route_base = '/paper'
    list_title = 'Papers'
    list_columns = ['paper_id', 'title', 'abstract', 'filename', 'contact_email', 'year']
    add_exclude_columns = edit_exclude_columns = show_exclude_columns = ["topics", "history"]
    related_views = [Topic, History]

class Conference(ModelView):
    datamodel = SQLAInterface(models.Conference)
    route_base = '/conference'
    list_title = 'Conferences'
    list_columns = ['year', 'location']
    add_exclude_columns = edit_exclude_columns = show_exclude_columns = ["papers"]
    related_views = [Paper]

appbuilder.add_view(
    Conference,
    "Conferences",
    icon="fa-database",
    category="Admin",
)

appbuilder.add_view(
    History,
    "History",
    icon="fa-database",
    category="Admin",
)

appbuilder.add_view(
    Paper,
    "Papers",
    icon="fa-database",
    category="Admin",
)

appbuilder.add_view(
    Topic,
    "Topics",
    icon="fa-database",
    category="Admin",
)

