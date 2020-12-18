from data_core.auto_jobs.database import Database
from data_core.auto_jobs.train_model import Trainning
from data_core.auto_jobs.train_model_load import Trainning_load

import time
# อัพเดท job_status



def updateCost(job_id, status,vm):
    Db = Database.conn()
    cursor = Db.cursor()
    sql = "UPDATE scheduled_auto_cost_job SET job_status = %s,job_vm_node = %s WHERE job_id = %s"
    val = (status, vm,int(job_id))
    cursor.execute(sql, val)
    Db.commit()

def updateProductBigfarm(job_id, status,vm):
    Db = Database.conn()
    cursor = Db.cursor()
    sql = "UPDATE scheduled_auto_bigfarm_job SET job_status = %s,job_vm_node = %s WHERE job_id = %s"
    val = (status, vm,int(job_id))
    cursor.execute(sql, val)
    Db.commit()

def updateProductProduction(job_id, status,vm):
    Db = Database.conn()
    cursor = Db.cursor()
    sql = "UPDATE scheduled_production_job SET job_status = %s,job_vm_node = %s WHERE job_id = %s"
    val = (status, vm,int(job_id))
    cursor.execute(sql, val)
    Db.commit()

# อัพเดท job_status
def updatePrice(job_id, status,vm):
    Db = Database.conn()
    cursor = Db.cursor()
    sql = "UPDATE scheduled_auto_price_job SET job_status = %s,job_vm_node = %s WHERE job_id = %s"
    val = (status, vm,int(job_id))
    cursor.execute(sql, val)
    Db.commit()


# run job เช็ค ถ้า job_status == 2 ให้ทำงาน
def runjobProductBigfarm(vm):
    Db = Database.conn()
    cursor = Db.cursor()
    cursor.execute("SELECT job_id,job_status,job_round FROM scheduled_auto_bigfarm_job where job_status in (2)  ORDER BY job_status DESC , job_updated ASC  LIMIT 1")
    for data in cursor:
        if data[1] == 2:
            try:
                print("runjobProductBigfarm running.....!!")
                updateProductBigfarm(data[0], 3, vm)
                if data[2] == 0:
                    Trainning.training(data[0], 'bigfarm', 0, data[2])
                else:
                    Trainning.Trainning_load(data[0], 'bigfarm', 0, data[2])

                print('job_ID ', data[0], '   OK')
            except IndexError:
                print('IndexError : ProductBigfarm ข้อมูล job_id =',data[0],'ไม่พร้อมใช้งาน')
                updateProductBigfarm(data[0],404,vm)
            except ValueError:
                print('ValueError :ProductBigfarm ข้อมูล job_id =', data[0], 'ไม่พร้อมใช้งาน')
                updateProductBigfarm(data[0], 404,vm)
            except TypeError:
                print('TypeError :ProductBigfarm ข้อมูล job_id =', data[0], 'ไม่พร้อมใช้งาน')
                updateProductBigfarm(data[0], 404, vm)


# run job เช็ค ถ้า job_status == 2 ให้ทำงาน
def runjobProductProduction(vm):
    Db = Database.conn()
    cursor = Db.cursor()
    cursor.execute("SELECT job_id,job_status FROM scheduled_production_job where job_status in (2)  ORDER BY job_status DESC , job_updated ASC  LIMIT 1")
    for data in cursor:
        if data[1] == 2:
            try:
                print("runjobProductProduction running.....!!")
                updateProductProduction(data[0], 3,vm)
                Trainning.training(data[0], 'production',data[2])
                print('job_ID ',data[0], '   OK')
            except IndexError:
                print('IndexError : ProductProduction ข้อมูล job_id =',data[0],'ไม่พร้อมใช้งาน')
                updateProductProduction(data[0],404)
            except ValueError:
                print('ValueError :ProductProduction ข้อมูล job_id =', data[0], 'ไม่พร้อมใช้งาน')
                updateProductProduction(data[0], 404)
            except TypeError:
                print('TypeError :ProductProduction ข้อมูล job_id =', data[0], 'ไม่พร้อมใช้งาน')
                updateProductProduction(data[0], 404)


def runjobPrice(vm):
    Db = Database.conn()
    cursor = Db.cursor()
    cursor.execute("SELECT job_id,job_status,export_check,job_round FROM scheduled_auto_price_job where job_status in (2)  ORDER BY job_status DESC , job_updated ASC  LIMIT 1")
    for data in cursor:
        if data[1] == 2:
            try:
                print("runjobPrice running.....!!")
                updatePrice(data[0], 3,vm)
                Trainning.training(data[0], 'price',data[2],data[3])
                print('job_ID ',data[0], '   OK')
            except IndexError:
                print('IndexError :Price ข้อมูล job_id =',data[0],'ไม่พร้อมใช้งาน')
                updatePrice(data[0], 404, vm)
            except ValueError:
                print('ValueError :Price ข้อมูล job_id =', data[0], 'ไม่พร้อมใช้งาน')
                updatePrice(data[0], 404, vm)
            except TypeError:
                print('TypeError :Price ข้อมูล job_id =', data[0], 'ไม่พร้อมใช้งาน')
                updatePrice(data[0], 404, vm)

# run job เช็ค ถ้า job_status == 2 ให้ทำงาน
def runjobCost(vm):
    Db = Database.conn()
    cursor = Db.cursor()
    cursor.execute("SELECT job_id,job_status,job_round FROM scheduled_auto_cost_job where job_status in (2)  ORDER BY job_status DESC , job_updated ASC  LIMIT 1")
    for data in cursor:
        if data[1] == 2:
            try:
                print("runjobCost running.....!!")
                updateCost(data[0], 3,vm)
                Trainning.training(data[0], 'cost',1,data[2])
                print('job_ID ',data[0], '   OK')
            except IndexError:
                print('IndexError :Cost ข้อมูล job_id =',data[0],'ไม่พร้อมใช้งาน')
                updateCost(data[0], 404, vm)
            except ValueError:
                print('ValueError :Cost ข้อมูล job_id =',data[0],'ไม่พร้อมใช้งาน')
                updateCost(data[0], 404, vm)
            except TypeError:
                print('TypeError :Price ข้อมูล job_id =', data[0], 'ไม่พร้อมใช้งาน')
                updateCost(data[0], 404, vm)


def runjob(vm):
    runjobProductBigfarm(vm)
   # runjobProductProduction(vm)
   # runjobPrice(vm)
   # runjobCost(vm)


