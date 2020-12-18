import pickle

model_files = []
def dump_model_tf(fileName, model,PathFiles):
    try:
        model.save(PathFiles + fileName + ".hdf5")
        print(fileName, 'Dump_file OK...')
    except IOError as e:
        print(e)

def dump_model(fileName, model,PathFiles):
    try:
        f = open(PathFiles + fileName + ".pkl", "wb")
        pickle.dump(model, f)
        f.close()
        print(fileName, 'Dump_file OK...')
    except IOError as e:
        print(e)

def add_model_wait_dump(fileName, model,PathFiles):
    model_files.append([fileName, model,PathFiles])

def dump_model_list():
    for fileName, model,PathFiles in model_files:
        dump_model(fileName, model,PathFiles)
    print('dump_model_list Ok...')