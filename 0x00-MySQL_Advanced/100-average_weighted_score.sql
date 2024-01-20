-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
        DECLARE Average FLOAT;

        SELECT SUM(corrects.score * projs.weight) / SUM(projs.weight) INTO Average
        FROM projects projs
        INNER JOIN corrections corrects ON projs.id = corrects.project_id AND corrects.user_id = user_id;
        UPDATE users SET average_score = Average WHERE id = user_id;
END $$
DELIMITER ;
