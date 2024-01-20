-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
        DECLARE Average FLOAT;
        DECLARE user_id INT;
        DECLARE done BOOLEAN DEFAULT FALSE;
        DECLARE cur CURSOR FOR SELECT id FROM users;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
        OPEN cur;

        insert_loop: LOOP
                FETCH cur INTO user_id;
                IF done THEN
                        LEAVE insert_loop;
                END IF;
                SELECT SUM(corrects.score * projs.weight) / SUM(projs.weight) INTO Average
                FROM projects projs
                INNER JOIN corrections corrects ON projs.id = corrects.project_id AND corrects.user_id = user_id;
                UPDATE users SET average_score = Average WHERE id = user_id;
        END LOOP;
        CLOSE cur;
END $$
DELIMITER ;
