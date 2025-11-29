-- testing
INSERT INTO Paths(path_type, error_path, normal_path)
VALUES
('testing', '/path/to/test/error/', 'path/to/test/normal/');

-- training
INSERT INTO Paths(path_type, error_path, normal_path)
VALUES
('training', 'path/to/train/error/', 'path/to/train/normal/');

-- insert training error
INSERT INTO Image_Data(file_type, file_name, file_width, file_height, path_id)
VALUES
('training_error', 'name_train_error.png', 720, 480, 2);

-- insert training normal
INSERT INTO Image_Data(file_type, file_name, file_width, file_height, path_id)
VALUES
('training_normal', 'name_train_normal.png', 720, 480, 2);

-- insert testing error
INSERT INTO Image_Data(file_type, file_name, file_width, file_height, path_id)
VALUES
('testing_error', 'name_test_error.png', 720, 480, 1);

-- insert testing normal
INSERT INTO Image_Data(file_type, file_name, file_width, file_height, path_id)
VALUES
('testing_normal', 'name_test_normal.png', 480, 720, 1);