import mariadb as md
import sys

try:
    conn = md.connect(
        user ="root",
        password = "Buffroo",
        host="127.0.0.1",
        port= 3306,
        database="sys"
    )
except md.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()

cur.execute("""
        SELECT Paths.path_id, Paths.path_type, Paths.error_path, 
               image_data.file_id, image_data.file_type, image_data.file_name, 
               image_data.file_width, image_data.file_height 
        FROM Paths 
        INNER JOIN image_data ON Paths.path_id = image_data.path_id 
        WHERE Paths.path_type = 'training' AND image_data.file_type = 'training_normal'
    """)

for (path_id, path_type, error_path, file_id, file_type, file_name, file_width, file_height) in cur:
    print(f"Path ID: {path_id}\nPath Type: {path_type}\nPath: {error_path}\nFile ID: {file_id}\nFile Type: {file_type}\nFile Name: {file_name}\nFile Width: {file_width}\nFile Height: {file_height}\n")