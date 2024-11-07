-- need to add constraint to `messages` table
-- sounds like I need the "full 12-step procedure":
--    https://sqlite.org/lang_altertable.html
BEGIN IMMEDIATE TRANSACTION;
CREATE TABLE `v2_messages`
(
 `app_id` VARCHAR,
 `mailbox_id` VARCHAR,
 `side` VARCHAR,
 `phase` VARCHAR, -- numeric or string
 `body` VARCHAR,
 `server_rx` INTEGER,
 `msg_id` VARCHAR,
 PRIMARY KEY (`app_id`, `mailbox_id`, `side`)
);

INSERT INTO `v2_messages` SELECT * FROM `messages`;
DROP TABLE `messages`;
ALTER TABLE `v2_messages` RENAME TO `messages`;

CREATE INDEX `messages_idx` ON `messages` (`app_id`, `mailbox_id`);
-- no "views" to do anything with, I don't believe
END TRANSACTION;

DELETE FROM `version`;
INSERT INTO `version` (`version`) VALUES (2);
