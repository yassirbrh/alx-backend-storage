-- SQL script that creates a stored procedure AddBonus that adds a new correction for a student.
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
        DECLARE check_project INT;
        SELECT id INTO check_project
        FROM projects
        WHERE name = project_name;
        IF check_project IS NULL THEN
                INSERT INTO projects(name) VALUES(project_name);
                SET check_project = LAST_INSERT_ID();
        END IF;
        INSERT INTO corrections(user_id, project_id, score) VALUES(user_id, check_project, score);
END $$
DELIMITER ;
