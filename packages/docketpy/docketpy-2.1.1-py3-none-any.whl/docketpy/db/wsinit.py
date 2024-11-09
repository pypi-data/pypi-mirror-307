"""
Workspace initialization
"""
from docketpy.db.models import Workspace
from docketpy.db.engine import DATABASE_URL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_pg_session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()


def initialize_workspace(session, workspace, location, logs_bucket, url):
    session = create_pg_session()
    if get_workspace(session=session, workspace=workspace) is None: 
        new_ws = Workspace(name=workspace, location=location, logs_bucket=logs_bucket, url=url)
        session.add(new_ws)
        session.commit()
    return get_workspace(session=session, workspace=workspace)
    

def get_workspace(session, workspace):
    return session.query(Workspace).filter_by(name=workspace).first()


if __name__ == "__main__":
    print("base.py")
    workspace = "test_workspace"
    location = "test_location"
    logs_bucket = "test_logs_bucket"
    url = "test_url"
    s = create_pg_session()
    print(get_workspace(s, workspace))
    wayfair_ws = initialize_workspace(s, 'wayfair', 'Boston, MA', 'st-temp-docket-logs-bucket', 'www.wayfair.com')
    print(wayfair_ws.id)
    print(wayfair_ws.name)
    print(wayfair_ws.location)
    print(wayfair_ws.logs_bucket)
    print(wayfair_ws.url)
    print(wayfair_ws.added_dt)
    wayfair_ws = get_workspace(s, 'wayfair')
    print(wayfair_ws.id)
    print(wayfair_ws.name)
    print(wayfair_ws.location)
    print(wayfair_ws.logs_bucket)
    print(wayfair_ws.url)
    print(wayfair_ws.added_dt)
    print(get_workspace(s, 'wayfair'))
    print(get_workspace(s, 'not_exist'))
    
    