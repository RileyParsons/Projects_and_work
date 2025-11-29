-- get all from paths
SELECT * FROM Paths;

-- get all from image data 
SELECT * FROM image_data;

-- get error training data
SELECT 
    Paths.path_id,
    Paths.path_type,
    Paths.error_path,
    image_data.file_id,
    image_data.file_type,
    image_data.file_name,
    image_data.file_width,
    image_data.file_height
FROM 
    Paths
INNER JOIN 
    image_data ON Paths.path_id = image_data.path_id
WHERE 
    Paths.path_type = 'training' 
    AND image_data.file_type IN ('training_error');

-- get normal training data    
SELECT 
    Paths.path_id,
    Paths.path_type,
    Paths.normal_path,
    image_data.file_id,
    image_data.file_type,
    image_data.file_name,
    image_data.file_width,
    image_data.file_height
FROM 
    Paths
INNER JOIN 
    image_data ON Paths.path_id = image_data.path_id
WHERE 
    Paths.path_type = 'training' 
    AND image_data.file_type IN ('training_normal');

-- get error testing data
SELECT 
    Paths.path_id,
    Paths.path_type,
    Paths.error_path,
    image_data.file_id,
    image_data.file_type,
    image_data.file_name,
    image_data.file_width,
    image_data.file_height
FROM 
    Paths
INNER JOIN 
    image_data ON Paths.path_id = image_data.path_id
WHERE 
    Paths.path_type = 'testing' 
    AND image_data.file_type IN ('testing_error');

-- get normal testing data
SELECT 
    Paths.path_id,
    Paths.path_type,
    Paths.normal_path,
    image_data.file_id,
    image_data.file_type,
    image_data.file_name,
    image_data.file_width,
    image_data.file_height
FROM 
    Paths
INNER JOIN 
    image_data ON Paths.path_id = image_data.path_id
WHERE 
    Paths.path_type = 'testing' 
    AND image_data.file_type IN ('testing_normal');
