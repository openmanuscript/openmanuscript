READER = {
    "oms" : "none"
}

def set_database( db ):
    global READER

    READER["db"] = db

def read( omsdb ):
    global READER

    set_database(omsdb)
    print(omsdb)
