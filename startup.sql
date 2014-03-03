/* ID MUST BE 1 for the two items below */

/* INSERT a default customer whose id should be 0 */
insert into chit_main_app_customer(name, mobile, user_id)
values ('Name of the Chits', '1234567890', 1)

/* INSERT a default group whose id should be 0 */
insert into chit_main_app_group(name, start_date, amount,
                      commision, started, total_months)
values ('Personal Credits', '2000-JAN-1', 0, 0, 1, 0)

/* Add all known users into the default group */
INSERT INTO chit_main_app_subscriptions(member_id, group_id, comments)
SELECT id as member_id, 0 as group_id, "Auto Added" as comments 
FROM chit_main_app_customer
