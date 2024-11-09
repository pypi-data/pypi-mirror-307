import os
import time
import logging
import subprocess
import platform, socket, sys
import pickle
from enum import Enum

from datetime import datetime
from uuid import uuid4
from abc import ABC, abstractmethod

import redis

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from docketpy.db.engine import DATABASE_URL
from docketpy.db.models import Workspace, Workflow, WorkflowRun, WorkflowRunLog

from docketpy.gcs import save_logs_to_bucket_from_redis
from docketpy.config import LOGS_BUCKET, REDIS_HOST, REDIS_PORT

# Initialize Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
try:
    redis_client.rpush('docket-log', f"{datetime.now()}: Connected to Redis at {REDIS_HOST}:{REDIS_PORT} from {socket.gethostname()}!") 
    redis_client.rpush('docket-log', f"{datetime.now()}: Docketpy Initializing from {socket.gethostname()}!")
except Exception as e:
    print(f"Failed to initialize Redis client: {e}")
    sys.exit(1)


# Initialize Redis logger
class RedisHandler(logging.Handler):
    def __init__(self, host='localhost', port=6379, key='app-logs'):
        logging.Handler.__init__(self)
        self.client = redis.Redis(host=host, port=port)
        self.key = key

    def emit(self, record):
        try:
            log_entry = self.format(record)
            self.client.rpush(self.key, log_entry)
            # print(f"RedisHandler: {self.key} {log_entry}")
        except Exception as e:
            print(f"An exception in RedisHandler: {str(e)}")


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """
    def __init__(self, logger, level):
       self.logger = logger
       self.level = level
       self.linebuf = ''
       self._in_write = False
    
    def write(self, message):
        # Avoid empty messages and recursion
        if not self._in_write and message.strip():  
            self._in_write = True
            try:
                self.logger.log(self.level, message.strip())
            finally:
                self._in_write = False

    def flush(self):
        pass


# Function to configure the Redis logger
def configure_redis_logger(name='redis_logger', host='localhost', port=6379, key='app-logs'):
    logger = logging.getLogger(name)
    redis_handler = RedisHandler(host=host, port=port, key=key)
    redis_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(redis_handler)
    logger.setLevel(logging.DEBUG)
    return logger


def close_logger(logger):
    """Close all handlers of the logger."""
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)

class WorkflowState(Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"
    

class TaskStatus(Enum):
    ERRORED = "ERRORED"
    KILLED = "KILLED"
    INITIATED = "INITIATED"
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    COMPLETED = "COMPLETED"

class WorkflowRunStatus(Enum):
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    ERRORED = "ERRORED"
    KILLED = "KILLED"
    

class BaseTask(ABC):
    def __init__(self):
        self.task_id = str(uuid4()).split('-')[-1]
        self.redis_logger_key = f"app-logs-{self.task_id}"
        self.task_status = TaskStatus.INITIATED
        self.redis_logger = configure_redis_logger(
            name=f"redis_logger-{self.task_id}", 
            host=REDIS_HOST, 
            port=REDIS_PORT, 
            key=self.redis_logger_key
            )

    def get_task_id(self):
        return self.task_id

    def set_status(self, status):
        self.task_status = status
    
    def log_platform_info(self):
        self.redis_logger.info(f"Running {self.__class__.__name__}")
        self.redis_logger.info(f"Platform: {platform.platform()}")
        self.redis_logger.info(f"Hostname: {socket.gethostname()}")
        self.redis_logger.info(f"IP: {socket.gethostbyname(socket.gethostname())}")
        self.redis_logger.info(f"Python: {platform.python_version()}")
        
    def close_and_save_logs(self):
        close_logger(self.redis_logger)
        save_logs_to_bucket_from_redis(REDIS_HOST, REDIS_PORT, self.redis_logger_key, LOGS_BUCKET, self.redis_logger_key)

    @abstractmethod
    def run(self):
        pass


class PgDbManager:
    session = None
    def __init__(self):
        PgDbManager.session = self.create_pg_session()
    
    def create_pg_session(self):
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        return Session()
    
    @staticmethod
    def get_session():
        if PgDbManager.session is None:
            PgDbManager().__init__()
            return PgDbManager.session
        else:
            return PgDbManager.session
        

class DocketWorkspace:
    def __init__(self, name, location, logs_bucket, url):
        self.name = name
        self.location = location
        self.logs_bucket = logs_bucket
        self.url = url
        # self.initialize_workspace()
        
    def initialize_workspace(self) -> Workspace:
        session = PgDbManager.get_session()
        if DocketWorkspace.get(name=self.name) is None: 
            new_ws = Workspace(name=self.name, location=self.location, logs_bucket=self.logs_bucket, url=self.url)
            session.add(new_ws)
            session.commit()
        return DocketWorkspace.get(name=self.name)

    @staticmethod
    def get(name) -> Workspace:
        session = PgDbManager.get_session()
        return session.query(Workspace).filter_by(name=name).first()
    
    @staticmethod
    def create(name, location, logs_bucket, url) -> Workspace:
        return DocketWorkspace(name, location, logs_bucket, url).initialize_workspace()


class DocketWorkflow:
    def __init__(self, 
                 name:str, 
                 description, 
                 state:WorkflowState, 
                 version, 
                 git_repo_url, 
                 git_branch, 
                 git_commit_id, 
                 workspace):
        self.name = name
        self.description = description
        self.state = state
        self.version = version
        self.git_repo_url = git_repo_url
        self.git_branch = git_branch
        self.git_commit_id = git_commit_id  
        self.workspace = workspace
        # self.initialize_workflow()
        
    def initialize_workflow(self) -> Workflow:
        session = PgDbManager.get_session()
        if DocketWorkflow.get(name=self.name, version=self.version, workspace=self.workspace) is None: 
            new_wf = Workflow(name=self.name, 
                              description = self.description, 
                              state=self.state.value, 
                              workspace=self.workspace, 
                              version=self.version,
                              git_repo_url=self.git_repo_url,
                            #   "https://github.com/wayfair/docket-py-package.git"
                              git_branch=self.git_branch, 
                            #   "main", 
                              git_commit_id=self.git_commit_id)
                            #   "0000000000000000000000000000000000000000"
            print(f"new_ws: {new_wf}")
            session.add(new_wf)
            session.commit()
        return DocketWorkflow.get(name=self.name, version=self.version, workspace=self.workspace)
    
    @staticmethod
    def get(name, version, workspace:Workspace) -> Workflow:
        session = PgDbManager.get_session()
        return session.query(Workflow).filter(and_(Workflow.name==name, Workflow.version == version, Workflow.workspace_id == workspace.id)).first()
        # return session.query(Workflow).filter_by(name=name).first()

    @staticmethod
    def create(name:str, 
               description, 
               state:WorkflowState, 
               version, 
               git_repo_url, 
               git_branch, 
               git_commit_id, 
               workspace:Workspace) -> Workflow:
        return DocketWorkflow(
            name, description, 
            version=version, 
            state=state, 
            git_repo_url=git_repo_url, 
            git_branch=git_branch, 
            git_commit_id=git_commit_id, 
            workspace=workspace).initialize_workflow()
        
    @staticmethod
    def update(name:str, status:WorkflowState) -> Workflow:
        session = PgDbManager.get_session()
        workflow_to_update = session.query(Workflow).filter(and_(Workflow.name == name, 1 == 1)).first()
        workflow_to_update.status = status.value
        if status == WorkflowState.DRAFT:
            pass
        if status == WorkflowState.PUBLISHED:
            workflow_to_update.published_dt = datetime.now()
        if status == WorkflowState.ARCHIVED:
            workflow_to_update.archived_dt = datetime.now()
        session.commit()
        return workflow_to_update
    

class DocketWorkflowRun:
    def __init__(self, submitted_by, workflow:Workflow):
        self.run_id = None
        self.submitted_by = submitted_by
        self.workflow = workflow
        
    @staticmethod
    def generate_run_id(type='auto'):
        return "{}-{}-{}".format(type, datetime.now().strftime("%Y-%m-%d-%H-%M"), str(uuid4()).split('-')[-1])
        
    def initialize_workflow_run(self) -> WorkflowRun:
        session = PgDbManager.get_session()
        if DocketWorkflowRun.get(run_id=self.run_id, workflow=self.workflow) is None: 
            self.run_id = DocketWorkflowRun.generate_run_id()
            new_wf_run = WorkflowRun(run_id=self.run_id, 
                              start_dt = datetime.now(), 
                              status=WorkflowRunStatus.STARTED.value, 
                              submitted_by=self.submitted_by,
                              workflow=self.workflow)
            print(f"adding new_wf_run: {new_wf_run}")
            session.add(new_wf_run)
            session.commit()
        return DocketWorkflowRun.get(run_id=self.run_id, workflow=self.workflow)
    
    @staticmethod
    def get(run_id, workflow:Workflow) -> WorkflowRun:
        session = PgDbManager.get_session()
        return session.query(WorkflowRun).filter(and_(WorkflowRun.run_id == run_id, WorkflowRun.workflow_id == workflow.id)).first()
    
    @staticmethod
    def get_workflow_run(run_id) -> WorkflowRun:
        session = PgDbManager.get_session()
        return session.query(WorkflowRun).filter(and_(WorkflowRun.run_id == run_id, 1 == 1)).first()
    
    @staticmethod
    def create(submitted_by, workflow:Workflow) -> WorkflowRun:
        return DocketWorkflowRun(submitted_by, workflow).initialize_workflow_run()
    
    @staticmethod
    def get_status(run_id) -> str:
        session = PgDbManager.get_session()
        wfr = session.query(WorkflowRun).filter_by(run_id=run_id).first()
        return wfr.status
    
    @staticmethod
    def update(run_id, status:WorkflowRunStatus) -> WorkflowRun:
        session = PgDbManager.get_session()
        workflow_run_to_update = session.query(WorkflowRun).filter(and_(WorkflowRun.run_id == run_id, 1 == 1)).first()
        workflow_run_to_update.status = status.value
        if status == WorkflowRunStatus.COMPLETED:
            workflow_run_to_update.end_dt = datetime.now()
        if status == WorkflowRunStatus.ERRORED:
            pass
        if status == WorkflowRunStatus.KILLED:
            workflow_run_to_update.killed_dt = datetime.now()
        session.commit()
        return workflow_run_to_update
    

class DocketWorkflowRunLog:
    def __init__(self, workflow_run:WorkflowRun, task_name, task_id, task_type, status:TaskStatus):
        self.workflow_run = workflow_run
        self.task_name = task_name
        self.task_id = task_id
        self.task_type = task_type
        self.status = status

    def initialize_workflow_run_log(self)->WorkflowRunLog:
        print("adding new_wf_run_log")
        session = PgDbManager.get_session()
        new_wf_run_log = WorkflowRunLog(task_name=self.task_name, 
                            task_id = self.task_id, 
                            task_type=self.task_type, 
                            status=self.status.value,
                            workflow_run_id=self.workflow_run.id)
        print(f"adding new_wf_run_log: {new_wf_run_log}")
        session.add(new_wf_run_log)
        session.commit()
        return new_wf_run_log
    
    @staticmethod
    def add(workflow_run:WorkflowRun, task_name, task_id, task_type, status:TaskStatus) -> WorkflowRunLog:
        return DocketWorkflowRunLog(workflow_run, task_name, task_id, task_type, status).initialize_workflow_run_log()


# create some helper methods 
def add_or_get_workspace(name, location, logs_bucket, url):
    pass

def add_workspace():
    pass

def create_workflow():
    pass

def create_workflow_run():
    pass

def add_workflow_run_log():
    pass

if __name__ == "__main__":
    def create_workspace(name, location, logs_bucket, url):
        return DocketWorkspace.create(name, location, logs_bucket, url)
    
    def create_workflow(workflow_name, description, state, version, git_repo_url, git_branch, git_commit_id, workspace_name):
        ws = DocketWorkspace.get(workspace_name)
        print(ws.id)
        wf = DocketWorkflow.create(
            name=workflow_name, 
            description=description, 
            state=state, 
            version=version, 
            git_repo_url=git_repo_url, 
            git_branch=git_branch, 
            git_commit_id=git_commit_id, 
            workspace=ws)
        print(wf.name)
        return wf
    
    def update_workflow(name, status):
        wf = DocketWorkflow.update(name, status)
        print(wf.name)
        return wf
    

    def create_workflow_run(submitted_by, workflow_name, version, workspace_name):
        wf = DocketWorkflow.get(workflow_name, version, DocketWorkspace.get(workspace_name))
        wf_run = DocketWorkflowRun.create(submitted_by, wf)
        print(wf_run.run_id)
        return wf_run

    def update_workflow_run(run_id, status):
        wf_run = DocketWorkflowRun.update(run_id, status)
        print(wf_run.run_id)
        return wf_run


    def add_workflow_run_log(run_id, task_name, task_id, task_type, status):
        wf_run = DocketWorkflowRun.get_workflow_run(run_id)
        wf_run_log = DocketWorkflowRunLog.add(wf_run, task_name, task_id, task_type, status)
        return wf_run_log


    create_workspace('rsi', 'Providence, RI', 'rsi-logs-bucket', 'www.rsi.com')
    create_workspace('wayfair', 'Boston, MA', 'ma-logs-bucket', 'www.ma.com')
    create_workspace('docket', 'Los Angeles, CA', 'docket-logs-bucket', 'www.docket.com')

    create_workflow(workflow_name='create_budget_ma', 
                    description='Create State Budget for MA', 
                    state='draft', 
                    version=2, 
                    git_repo_url='https://github.com/wayfair/docket-py-package.git', 
                    git_branch='main', 
                    git_commit_id='abcdef', 
                    workspace_name='rsi')
    
    wf_run = create_workflow_run(submitted_by='sthota', 
                        workflow_name='create_budget_ma', 
                        version=2, 
                        workspace_name='rsi')
    
    # DocketWorkflowRunLog.add(wf_run, 'get_budget_data', 'task_id', 'PythonTask', 'started')
    # DocketWorkflowRunLog.add(wf_run, 'get_budget_data', 'task_id', 'PythonTask', 'running')
    # DocketWorkflowRunLog.add(wf_run, 'get_budget_data', 'task_id', 'PythonTask', 'completed')
    
    add_workflow_run_log(wf_run.run_id, 'get_budget_data', 'task_id', 'PythonTask', TaskStatus.STARTED)
    add_workflow_run_log(wf_run.run_id, 'get_budget_data', 'task_id', 'PythonTask', TaskStatus.RUNNING)
    add_workflow_run_log(wf_run.run_id, 'get_budget_data', 'task_id', 'PythonTask', TaskStatus.COMPLETED)
    
    update_workflow_run(run_id=wf_run.run_id, status=WorkflowRunStatus.COMPLETED)
    # update_workflow_run(run_id="auto-2024-11-08-14-19-f4598d791080", status="KILLED")
    # update_workflow_run(run_id="auto-2024-11-08-14-21-9c6e35ad0bf7", status="COMPLETED")
    # update_workflow_run(run_id="auto-2024-11-08-14-22-95aa73952fcc", status="KILLED")
    # update_workflow_run(run_id="auto-2024-11-08-14-23-146aeef89356", status="COMPLETED")
    # update_workflow_run(run_id="auto-2024-11-08-14-27-2b9df04bbfec", status="KILLED")
    
    print(DocketWorkflowRun.get_status(wf_run.run_id))
    # update_workflow(name='create_budget_ma', status=WorkflowState.PUBLISHED)
    

    
