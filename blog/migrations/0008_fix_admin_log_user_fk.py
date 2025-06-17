from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0007_update_react_types'),
    ]

    operations = [
        migrations.RunSQL(
            # Forward SQL - Update the foreign key to point to blog_user
            """
            -- Drop existing indexes for django_admin_log
            DROP INDEX IF EXISTS django_admin_log_user_id_c564eba6;
            DROP INDEX IF EXISTS django_admin_log_content_type_id_c4bce8eb;
            
            -- Create a temporary table with the correct structure
            CREATE TABLE django_admin_log_new (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                action_time DATETIME NOT NULL,
                object_id TEXT NULL,
                object_repr VARCHAR(200) NOT NULL,
                action_flag SMALLINT UNSIGNED NOT NULL,
                change_message TEXT NOT NULL,
                content_type_id INTEGER NULL REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED,
                user_id INTEGER NOT NULL REFERENCES blog_user(id) DEFERRABLE INITIALLY DEFERRED
            );
            
            -- Copy data from the old table to the new one (if any exists)
            INSERT INTO django_admin_log_new (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id)
            SELECT id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id 
            FROM django_admin_log WHERE user_id IN (SELECT id FROM blog_user);
            
            -- Drop the old table
            DROP TABLE django_admin_log;
            
            -- Rename the new table to the original name
            ALTER TABLE django_admin_log_new RENAME TO django_admin_log;
            
            -- Recreate the indexes
            CREATE INDEX django_admin_log_user_id_c564eba6 ON django_admin_log (user_id);
            CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON django_admin_log (content_type_id);
            """,
            
            # Reverse SQL - Revert the foreign key back to auth_user
            """
            -- Drop existing indexes
            DROP INDEX IF EXISTS django_admin_log_user_id_c564eba6;
            DROP INDEX IF EXISTS django_admin_log_content_type_id_c4bce8eb;
            
            -- Create a temporary table with the original structure
            CREATE TABLE django_admin_log_new (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                action_time DATETIME NOT NULL,
                object_id TEXT NULL,
                object_repr VARCHAR(200) NOT NULL,
                action_flag SMALLINT UNSIGNED NOT NULL,
                change_message TEXT NOT NULL,
                content_type_id INTEGER NULL REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED,
                user_id INTEGER NOT NULL REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED
            );
            
            -- Copy data from the current table to the new one
            INSERT INTO django_admin_log_new (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id)
            SELECT id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id FROM django_admin_log;
            
            -- Drop the current table
            DROP TABLE django_admin_log;
            
            -- Rename the new table to the original name
            ALTER TABLE django_admin_log_new RENAME TO django_admin_log;
            
            -- Recreate the indexes
            CREATE INDEX django_admin_log_user_id_c564eba6 ON django_admin_log (user_id);
            CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON django_admin_log (content_type_id);
            """
        ),
    ] 