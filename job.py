from database import Database
from train_model import Trainning
import time
# อัพเดท job_status



def updateCost(job_id, status):
    Db = Database.conn()
    cursor = Db.cursor()
    sql = "UPDATE scheduled_cost_job SET job_status = %s WHERE job_id = %s"
    val = (status, int(job_id))
    cursor.execute(sql, val)
    Db.commit()

def updateProductBigfarm(job_id, status):
    Db = Database.conn()
    cursor = Db.cursor()
    sql = "UPDATE scheduled_bigfarm_job SET job_status = %s WHERE job_id = %s"
    val = (status, int(job_id))
    cursor.execute(sql, val)
    Db.commit()

def updateProductProduction(job_id, status):
    Db = Database.conn()
    cursor = Db.cursor()
    sql = "UPDATE scheduled_production_job SET job_status = %s WHERE job_id = %s"
    val = (status, int(job_id))
    cursor.execute(sql, val)
    Db.commit()

# อัพเดท job_status
def updatePrice(job_id, status):
    Db = Database.conn()
    cursor = Db.cursor()
    sql = "UPDATE scheduled_price_job SET job_status = %s WHERE job_id = %s"
    val = (status, int(job_id))
    cursor.execute(sql, val)
    Db.commit()


# run job เช็ค ถ้า job_status == 2 ให้ทำงาน
def runjobProductBigfarm():
    Db = Database.conn()
    cursor = Db.cursor()
    cursor.execute("SELECT job_id,job_status,suit_check FROM scheduled_bigfarm_job where job_status in (2)  ORDER BY job_status DESC , created_at ASC  LIMIT 1")
    for data in cursor:
        if data[1] == 2:
            try:
                print("runjobProductBigfarm running.....!!")
                updateProductBigfarm(data[0], 3)
                Trainning.training(data[0], 'bigfarm',data[2])
                print('job_ID ',data[0], '   OK')
            except IndexError:
                print('IndexError : ProductBigfarm ข้อมูล job_id =',data[0],'ไม่พร้อมใช้งาน')
                updateProductBigfarm(data[0],404)
            except ValueError:
                print('ValueError :ProductBigfarm ข้อมูล job_id =', data[0], 'ไม่พร้อมใช้งาน')
                updateProductBigfarm(data[0], 404)

# run job เช็ค ถ้า job_status == 2 ให้ทำงาน
def runjobProductProduction():
    Db = Database.conn()
    cursor = Db.cursor()
    cursor.execute("SELECT job_id,job_status,suit_check FROM scheduled_production_job where job_status in (2)  ORDER BY job_status DESC , created_at ASC  LIMIT 1")
    for data in cursor:
        if data[1] == 2:
            try:
                print("runjobProductProduction running.....!!")
                updateProductProduction(data[0], 3)
                Trainning.training(data[0], 'production',data[2])
                print('job_ID ',data[0], '   OK')
            except IndexError:
                print('IndexError : ProductProduction ข้อมูล job_id =',data[0],'ไม่พร้อมใช้งาน')
                updateProductProduction(data[0],404)
            except ValueError:
                print('ValueError :ProductProduction ข้อมูล job_id =', data[0], 'ไม่พร้อมใช้งาน')
                updateProductProduction(data[0], 404)
def runjobPrice():
    Db = Database.conn()
    cursor = Db.cursor()
    cursor.execute("SELECT job_id,job_status,export_check FROM scheduled_price_job where job_status in (2)  ORDER BY job_status DESC , created_at ASC  LIMIT 1")
    for data in cursor:
        if data[1] == 2:
            try:
                print("runjobPrice running.....!!")
                updatePrice(data[0], 3)
                Trainning.training(data[0], 'price',data[2])
                print('job_ID ',data[0], '   OK')
            except IndexError:
                print('IndexError :Price ข้อมูล job_id =',data[0],'ไม่พร้อมใช้งาน')
                updatePrice(data[0],404)
            except ValueError:
                print('ValueError :Price ข้อมูล job_id =', data[0], 'ไม่พร้อมใช้งาน')
                updatePrice(data[0], 404)

# run job เช็ค ถ้า job_status == 2 ให้ทำงาน
def runjobCost():
    Db = Database.conn()
    cursor = Db.cursor()
    cursor.execute("SELECT job_id,job_status,suit_check FROM scheduled_cost_job where job_status in (2)  ORDER BY job_status DESC , created_at ASC  LIMIT 1")
    for data in cursor:
        if data[1] == 2:
            try:
                print("runjobCost running.....!!")
                updateCost(data[0], 3)
                Trainning.training(data[0], 'cost',data[2])
                print('job_ID ',data[0], '   OK')
            except IndexError:
                print('IndexError :Cost ข้อมูล job_id =',data[0],'ไม่พร้อมใช้งาน')
                updateCost(data[0],404)
            except ValueError:
                print('ValueError :Cost ข้อมูล job_id =',data[0],'ไม่พร้อมใช้งาน')
                updateCost(data[0],404)
if __name__ == '__main__':
    runjobProductBigfarm()
    runjobProductProduction()
    runjobPrice()
    runjobCost()



