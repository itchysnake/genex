import psycopg2
from config import Config

def main():
    
    try:
        conn = psycopg2.connect(Config.SQLALCHEMY_DATABASE_URI, sslmode='require')
    
        cur = conn.cursor()
        
        # drops entire schema
        sql = """
        DROP SCHEMA public CASCADE
        """
        cur.execute(sql)
        conn.commit()
        
        # recreates schema
        sql = """
        CREATE SCHEMA public
        """
        cur.execute(sql)
        conn.commit()
        
        cur.close()
        conn.close()
        
    except (Exception, psycopg2.Error) as e:
        print("Error fetching data: ",e)
        
if __name__=="__main__":
    main()