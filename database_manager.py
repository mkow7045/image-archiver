import sqlite3
import os

class DatabaseManager:
    def __init__(self,state_manager):
        super().__init__()
        self.state_manager = state_manager
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
        query = f"SELECT name FROM images WHERE conf >={str(self.state_manager.conf_filter)} GROUP BY name HAVING"
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

        if not filter_yes and not filter_no:
            query = f"SELECT name FROM images WHERE conf >={str(self.state_manager.conf_filter)}"


        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows
    
    def get_results_from_db(self,image_path):
        image_path = image_path[7:]
        query = "SELECT * FROM images WHERE name = ?"
        self.cursor.execute(query, (image_path,))
        rows = self.cursor.fetchall()
        results = []

        for row in rows:
            boxes = [(row[5],row[6],row[7],row[8])]
            scores = [row[4]]
            classes = [row[3]]
            result = boxes,scores,classes
            results.append(result)
        
        return results
    
    def delete_from_db(self, delete_all):
        filter_yes = self.state_manager.filter_yes
        filter_no = self.state_manager.filter_no 
    
        query = f"DELETE FROM images WHERE name IN(SELECT name FROM images GROUP BY name HAVING"
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
        query += ')'

        if not filter_yes and not filter_no:
            query = f"DELETE FROM images WHERE conf >={str(self.state_manager.conf_filter)}"

        if delete_all:
            query = "DELETE FROM images"
            filter_yes = []
            filter_no = []
            rows = self.choose_from_db(filter_yes,filter_no)
        else:
            rows = self.choose_from_db(filter_yes,filter_no)


        self.cursor.execute(query)
        self.conn.commit()

        for img in rows:
            filename = img[0]
            path = os.path.join("./images",filename)

            if os.path.exists(path):
                os.remove(path)

    def delete_single(self,image_path):
        name = os.path.basename(image_path)

        self.cursor.execute("DELETE FROM images WHERE name = ?", (name,))
        self.conn.commit()

        if os.path.exists(image_path):
            os.remove(image_path)

    def get_classes_for_single(self,image_path):
        name = os.path.basename(image_path[0])

        self.cursor.execute("SELECT * FROM images WHERE name = ?", (name,))

        rows = self.cursor.fetchall()
        
        classes = []
        for row in rows:
            classes.append(row[3])

        return classes
    
    def get_class_names(self):
        self.cursor.execute("SELECT class_name, COUNT(*) FROM images GROUP BY class_name ORDER BY COUNT(*) DESC")
        results = self.cursor.fetchall()
        return results



    def __del__(self):
        self.conn.close()
