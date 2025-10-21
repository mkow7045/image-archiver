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

    def __del__(self):
        self.conn.close()
