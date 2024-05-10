from airflow import DAG
from tasks.scrape import scrape
from scraper.scrape import web_scrape
from scraper.scrape_details import process_details
from scraper.mongo import start_mongo
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 5, 5),
    'retries': 0,
}

dag = DAG(
    'SCRAPER',
    default_args=default_args,
    description='Scrape Daily Data',
    schedule='@daily',
    catchup=False
)

scrape_task = PythonOperator(
    task_id='Scrape_Category',
    python_callable=scrape,
    dag=dag,
)

details_task = PythonOperator(
    task_id='Get_Category',
    python_callable=process_details,
    dag=dag,
)

db_task = details_task = PythonOperator(
    task_id='DB_Category',
    python_callable=start_mongo,
    dag=dag,
)

scrape_task >> details_task >> db_task