import requests

import logging
from .config import RpaHubConfig

logger = logging.getLogger(__name__)


class XXL_BIZ:
    def __init__(self, config: RpaHubConfig):
        self.base_url = config.xxl_admin_baseurl
        self.client_secret = config.client_secret
        self.app_name = config.executor_app_name

        self.headers = {
            "XXL-JOB-CLIENT_SECRET": config.client_secret,
        }

    def job_registry(self, job_id: str) -> bool:
        payload = dict(
            appname=self.app_name,
            jobName=job_id,
            author="rpa hub",
            scheduleType="NONE",
            scheduleConf="",
            misfireStrategy="DO_NOTHING",
            executorRouteStrategy="FIRST",
            executorHandler=job_id,
            executorParam="",
            executorBlockStrategy="SERIAL_EXECUTION",
            executorTimeout=0,
            executorFailRetryCount=0,
            glueType="BEAN",
        )
        try:
            response = requests.post(
                self.base_url + "jobRegistry", headers=self.headers, json=payload
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error("Job registry executor failed. %s", e.message)
        return False

    def all_jobs_registry(self, job_ids: list[str]) -> bool:
        payload = []

        for job_id in job_ids:
            payload.append(
                dict(
                    appname=self.app_name,
                    jobName=job_id,
                    author="rpa hub",
                    scheduleType="NONE",
                    scheduleConf="",
                    misfireStrategy="DO_NOTHING",
                    executorRouteStrategy="FIRST",
                    executorHandler=job_id,
                    executorParam="",
                    executorBlockStrategy="SERIAL_EXECUTION",
                    executorTimeout=0,
                    executorFailRetryCount=0,
                    glueType="BEAN",
                )
            )
        try:
            response = requests.post(
                self.base_url + "allJobsRegistry", headers=self.headers, json=payload
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            logger.error("Job registry executor failed. %s", e.message)
        return False
