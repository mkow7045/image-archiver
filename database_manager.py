import sqlite3

class DatabaseManager:
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect("archive.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS images(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            model_name TEXT,
            class_name TEXT,
            conf REAL,
            x1 INTEGER,
            y1 INTEGER,
            x2 INTEGER,
            y2 INTEGER
            )
            """)
        
        self.conn.commit()

    def add_image_to_table(self,name,model_name,class_name,conf,x1,y1,x2,y2):
        self.cursor.execute("""
        INSERT INTO images(name, model_name, class_name, conf, x1, y1, x2, y2)
        VALUES(?,?,?,?,?,?,?,?)
        """,(name,model_name,class_name,conf,x1,y1,x2,y2))
        self.conn.commit()

    def choose_from_db(self,filter_yes,filter_no):
        query = "SELECT name FROM images GROUP BY name HAVING"
        if filter_yes:
            for cls in filter_yes:
                query += " SUM("
                query += f" class_name = '{cls}'"
                query += ") >= 1"
                query += " AND "
            
        

        if filter_no:
            for cls in filter_no:
                query += " SUM("
                query += f" class_name = '{cls}'"
                query += ") = 0"
                query += " AND "
            

        query = query[:-4]

        print(query)

        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def __del__(self):
        self.conn.close()
