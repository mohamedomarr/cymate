from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0003_merge_20250515_2143'),
        ('authtoken', '0003_tokenproxy'),
    ]

    operations = [
        migrations.RunSQL(
            # Forward SQL - Update the foreign key to point to blog_user
            """
            -- Drop existing indexes
            DROP INDEX IF EXISTS authtoken_token_user_id_key;
            DROP INDEX IF EXISTS authtoken_token_key_10f0b77e_uniq;
            
            -- Create a temporary table with the correct structure
            CREATE TABLE authtoken_token_new (
                key varchar(40) NOT NULL PRIMARY KEY,
                created timestamp with time zone NOT NULL,
                user_id integer NOT NULL REFERENCES blog_user(id) UNIQUE DEFERRABLE INITIALLY DEFERRED
            );
            
            -- Copy data from the old table to the new one
            INSERT INTO authtoken_token_new (key, created, user_id)
            SELECT key, created, user_id FROM authtoken_token;
            
            -- Drop the old table
            DROP TABLE authtoken_token;
            
            -- Rename the new table to the original name
            ALTER TABLE authtoken_token_new RENAME TO authtoken_token;
            
            -- Recreate the indexes
            CREATE UNIQUE INDEX authtoken_token_user_id_key ON authtoken_token (user_id);
            CREATE UNIQUE INDEX authtoken_token_key_10f0b77e_uniq ON authtoken_token (key);
            """,
            
            # Reverse SQL - Revert the foreign key back to auth_user
            """
            -- Drop existing indexes
            DROP INDEX IF EXISTS authtoken_token_user_id_key;
            DROP INDEX IF EXISTS authtoken_token_key_10f0b77e_uniq;
            
            -- Create a temporary table with the original structure
            CREATE TABLE authtoken_token_new (
                key varchar(40) NOT NULL PRIMARY KEY,
                created timestamp with time zone NOT NULL,
                user_id integer NOT NULL REFERENCES auth_user(id) UNIQUE DEFERRABLE INITIALLY DEFERRED
            );
            
            -- Copy data from the current table to the new one
            INSERT INTO authtoken_token_new (key, created, user_id)
            SELECT key, created, user_id FROM authtoken_token;
            
            -- Drop the current table
            DROP TABLE authtoken_token;
            
            -- Rename the new table to the original name
            ALTER TABLE authtoken_token_new RENAME TO authtoken_token;
            
            -- Recreate the indexes
            CREATE UNIQUE INDEX authtoken_token_user_id_key ON authtoken_token (user_id);
            CREATE UNIQUE INDEX authtoken_token_key_10f0b77e_uniq ON authtoken_token (key);
            """
        ),
        
        # Also fix the SocialAccount table
        migrations.RunSQL(
            # Forward SQL
            """
            -- Drop existing indexes
            DROP INDEX IF EXISTS socialaccount_socialaccount_user_id_fc810c6e;
            DROP INDEX IF EXISTS socialaccount_socialaccount_provider_uid_fc810c6e_uniq;
            
            -- Create a temporary table with the correct structure
            CREATE TABLE socialaccount_socialaccount_new (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                provider varchar(30) NOT NULL,
                uid varchar(191) NOT NULL,
                last_login datetime NOT NULL,
                date_joined datetime NOT NULL,
                extra_data text NOT NULL,
                user_id integer NOT NULL REFERENCES blog_user(id) DEFERRABLE INITIALLY DEFERRED
            );
            
            -- Copy data from the old table to the new one
            INSERT INTO socialaccount_socialaccount_new (id, provider, uid, last_login, date_joined, extra_data, user_id)
            SELECT id, provider, uid, last_login, date_joined, extra_data, user_id FROM socialaccount_socialaccount;
            
            -- Drop the old table
            DROP TABLE socialaccount_socialaccount;
            
            -- Rename the new table to the original name
            ALTER TABLE socialaccount_socialaccount_new RENAME TO socialaccount_socialaccount;
            
            -- Recreate the indexes
            CREATE INDEX socialaccount_socialaccount_user_id_fc810c6e ON socialaccount_socialaccount (user_id);
            CREATE UNIQUE INDEX socialaccount_socialaccount_provider_uid_fc810c6e_uniq ON socialaccount_socialaccount (provider, uid);
            """,
            
            # Reverse SQL
            """
            -- No need to change the social account table structure when reverting
            """
        )
    ]
