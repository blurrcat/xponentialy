BEGIN;
# add house id on challengeparticipant

ALTER TABLE `challengeparticipant`
  ADD COLUMN `house_id` INTEGER NOT NULL;

CREATE INDEX `challengeparticipant_house_id_index`
  ON `challengeparticipant` (`house_id`);

# remove not null on challengeparticipant.end_time
ALTER TABLE `challengeparticipant`
  MODIFY COLUMN `end_time` DATETIME;

# add unique constraint on challengeparticipant(user_id, challenge_id)
ALTER TABLE `challengeparticipant`
  ADD CONSTRAINT `challengeparticipant_user_id_challenge_id`
    UNIQUE (`user_id`, `challenge_id`);

COMMIT;