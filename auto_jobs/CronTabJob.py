from data_core.auto_jobs import job
from data_core.auto_jobs.database import Database
##TEST_JOB_TEXT


def runjob():
    Db = Database.conn()
    cursor = Db.cursor()
    node = "3"
    sql = "SELECT count(*) AS count_job FROM ( SELECT b.job_status AS b_bigfarm_job_status,b.job_vm_node AS b_node FROM scheduled_auto_bigfarm_job AS b UNION ALL SELECT c.job_status AS c_bigfarm_job_status,c.job_vm_node AS c_node FROM scheduled_auto_cost_job AS c UNION ALL SELECT p.job_status AS p_bigfarm_job_status,p.job_vm_node AS b_node FROM scheduled_auto_price_job AS p) AS a WHERE a.b_node = %s AND a.b_bigfarm_job_status = 3" % node
    print(sql)
    cursor.execute(sql)
    for data in cursor:
        if data[0] <= 1:
                job.runjob(node)
if __name__ == '__main__':
    runjob()
