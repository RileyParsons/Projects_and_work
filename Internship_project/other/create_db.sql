-- Paths table to store pathimage_datas for training and testing datasets
CREATE TABLE Paths (
    path_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    path_type ENUM('training', 'testing') NOT NULL,
    error_path VARCHAR(255) NOT NULL,
    normal_path VARCHAR(255) NOT NULL
);

-- Files table to store details of each file
CREATE TABLE Image_Data (
    file_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    file_type ENUM('training_error', 'training_normal', 'testing_error', 'testing_normal') NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_width INT NOT NULL,
    file_height INT NOT NULL,
    path_id INT NOT NULL,
    FOREIGN KEY (path_id) REFERENCES Paths(path_id)
);