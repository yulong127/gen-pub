from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'hello_world_kubernetes',
    default_args=default_args,
    description='A simple hello world DAG using KubernetesPodOperator',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=['example'],
)

# Define the task using KubernetesPodOperator
hello_world_task = KubernetesPodOperator(
    image="python:3.8-slim",
    cmds=["python", "-c"],
    arguments=["print('Hello, World!')"],
    labels={"foo": "bar"},
    name="hello-world-task",
    task_id="hello_world_task",
    get_logs=True,
    is_delete_operator_pod=True,  # Ensure the pod gets cleaned up after execution
    in_cluster=True,
    dag=dag,
)

hello_world_task
