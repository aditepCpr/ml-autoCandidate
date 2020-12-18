from data_core.auto_jobs.database import Database


# query path จาก database
def queryModel(select_tables,job_id):
    Db = Database.conn()
    cursor = Db.cursor()
    cursor.execute(
        "SELECT result_model_path,result_sta_path,result_pca_path,result_lda_path,result_model_name FROM %s where job_id = %s" % (
        select_tables, int(job_id)))
    modelDict : dict = {'model':None,'sta':None,'pca':None,'lda':None,'modelname':None}
    for data in cursor:
        modelDict["model"] = data[0]
        modelDict["sta"] = data[1]
        modelDict["pca"] = data[2]
        modelDict["lda"] = data[3]
        modelDict["modelname"] = data[4]
    return modelDict