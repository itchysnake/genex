import db_fill, db_init, db_clear

def main():
    # aren't modules (the files are self-initiating, so just need to call the file)
    db_clear.main()
    db_init.main()
    db_fill.main()
    
if __name__=="__main__":
    main()