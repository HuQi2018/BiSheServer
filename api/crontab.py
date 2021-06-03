import datetime
import time

import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from django_apscheduler.models import DjangoJob, DjangoJobExecution
# from django_pandas.io import read_frame
from BiSheServer.settings import BASE_LOG_DIR, LOG_SUFFIX
from api import upload_log


# 开启定时工作，每日任务，定时执行
scheduler_plan = BackgroundScheduler()  # 实例化调度器
try:
    # 清除原有任务
    dje = DjangoJobExecution.objects.all()
    dj = DjangoJob.objects.all()
    # 判断是否存在该任务
    dj_rs = dj.filter(id="task_time")
    if dj_rs.exists():
        dj_rs = dj_rs.first()
        # 如果启动时已过任务的下一次执行时间，则立即启动上传
        if int(time.mktime(dj_rs.next_run_time.timetuple())) < int(time.time()):
            upload_log.upload_hadoop_log_thread(suffix=(dj_rs.next_run_time + datetime.timedelta(days=-1))
                                                .strftime(LOG_SUFFIX))
    djePd = pd.DataFrame(list(dje.values()))
    djPd = pd.DataFrame(list(dj.values()))
    if not djePd.empty:
        # 如果有执行记录，则将执行记录进行记录到文件后再清空表
        crontab_log_path = BASE_LOG_DIR + "/crontab.log"
        djPd.to_csv(crontab_log_path, mode='a', index=True, sep='\t', encoding='utf_8_sig')
        with open(crontab_log_path, "a") as f:
            f.write("\n")  # 自带文件关闭功能，不需要再写f.close()
        djePd.to_csv(crontab_log_path, mode='a', index=True, sep='\t', encoding='utf_8_sig')
        with open(crontab_log_path, "a") as f:
            f.write("\n\n")  # 自带文件关闭功能，不需要再写f.close()
        dje.delete()
    dj.delete()
    # 任务表清空完毕后，重新设置任务
    # 调度器使用DjangoJobStore()
    scheduler_plan.add_jobstore(DjangoJobStore(), "default")
    # 设置定时任务，选择方式为interval，时间间隔为15 minutes
    # 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记
    # 另一种方式为周一到周五固定时间执行任务，对应代码为：
    # @register_job(scheduler_plan, "interval", minutes=15)
    # @register_job(scheduler_plan, 'cron', day_of_week='mon-sun', hour='20', minute='3', second='1', id='task_time')
    # @register_job(scheduler_plan, "interval", minutes=1, replace_existing=True)
    @register_job(scheduler_plan, 'cron', day_of_week='mon-sun', hour='0', minute='1', second='1', id='task_time',
                  replace_existing=True)
    def my_job():
        # 这里写你要执行的任务
        upload_log.upload_hadoop_log_thread(suffix="")
        # pass
    register_events(scheduler_plan)
    scheduler_plan.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler_plan.shutdown()
