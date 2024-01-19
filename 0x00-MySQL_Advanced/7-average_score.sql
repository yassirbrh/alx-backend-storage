-- SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
        DECLARE Average FLOAT;
        SELECT SUM(score) / COUNT(user_id) INTO Average
        FROM corrections
        WHERE corrections.user_id = user_id;
        UPDATE users SET average_score = Average WHERE id = user_id;
END $$
DELIMITER ;
