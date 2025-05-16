from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
        ('account', '0002_email_max_length'),
    ]

    operations = [
        migrations.RunSQL(
            # Forward SQL - Update the foreign key to point to blog_user
            """
            -- Drop existing indexes
            DROP INDEX IF EXISTS account_emailaddress_user_id_email_987c8728_uniq;
            DROP INDEX IF EXISTS unique_verified_email;
            DROP INDEX IF EXISTS account_emailaddress_user_id_2c513194;
            DROP INDEX IF EXISTS account_emailaddress_email_03be32b2;
            DROP INDEX IF EXISTS unique_primary_email;
            
            -- Create a temporary table with the correct structure
            CREATE TABLE account_emailaddress_new (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                verified BOOL NOT NULL,
                "primary" BOOL NOT NULL,
                user_id INTEGER NOT NULL REFERENCES blog_user(id) DEFERRABLE INITIALLY DEFERRED,
                email VARCHAR(254) NOT NULL
            );
            
            -- Copy data from the old table to the new one
            INSERT INTO account_emailaddress_new (id, verified, "primary", user_id, email)
            SELECT id, verified, "primary", user_id, email FROM account_emailaddress;
            
            -- Drop the old table
            DROP TABLE account_emailaddress;
            
            -- Rename the new table to the original name
            ALTER TABLE account_emailaddress_new RENAME TO account_emailaddress;
            
            -- Recreate the indexes
            CREATE UNIQUE INDEX account_emailaddress_user_id_email_987c8728_uniq ON account_emailaddress (user_id, email);
            CREATE UNIQUE INDEX unique_verified_email ON account_emailaddress (email) WHERE verified;
            CREATE INDEX account_emailaddress_user_id_2c513194 ON account_emailaddress (user_id);
            CREATE INDEX account_emailaddress_email_03be32b2 ON account_emailaddress (email);
            CREATE UNIQUE INDEX unique_primary_email ON account_emailaddress (user_id, "primary") WHERE "primary";
            """,
            
            # Reverse SQL - Revert the foreign key back to auth_user
            """
            -- Drop existing indexes
            DROP INDEX IF EXISTS account_emailaddress_user_id_email_987c8728_uniq;
            DROP INDEX IF EXISTS unique_verified_email;
            DROP INDEX IF EXISTS account_emailaddress_user_id_2c513194;
            DROP INDEX IF EXISTS account_emailaddress_email_03be32b2;
            DROP INDEX IF EXISTS unique_primary_email;
            
            -- Create a temporary table with the original structure
            CREATE TABLE account_emailaddress_new (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                verified BOOL NOT NULL,
                "primary" BOOL NOT NULL,
                user_id INTEGER NOT NULL REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED,
                email VARCHAR(254) NOT NULL
            );
            
            -- Copy data from the current table to the new one
            INSERT INTO account_emailaddress_new (id, verified, "primary", user_id, email)
            SELECT id, verified, "primary", user_id, email FROM account_emailaddress;
            
            -- Drop the current table
            DROP TABLE account_emailaddress;
            
            -- Rename the new table to the original name
            ALTER TABLE account_emailaddress_new RENAME TO account_emailaddress;
            
            -- Recreate the indexes
            CREATE UNIQUE INDEX account_emailaddress_user_id_email_987c8728_uniq ON account_emailaddress (user_id, email);
            CREATE UNIQUE INDEX unique_verified_email ON account_emailaddress (email) WHERE verified;
            CREATE INDEX account_emailaddress_user_id_2c513194 ON account_emailaddress (user_id);
            CREATE INDEX account_emailaddress_email_03be32b2 ON account_emailaddress (email);
            CREATE UNIQUE INDEX unique_primary_email ON account_emailaddress (user_id, "primary") WHERE "primary";
            """
        ),
        
        # Also fix the EmailConfirmation table
        migrations.RunSQL(
            # Forward SQL
            """
            -- Drop existing indexes
            DROP INDEX IF EXISTS account_emailconfirmation_email_address_id_5b7f8c58;
            DROP INDEX IF EXISTS account_emailconfirmation_key_f43612bd_uniq;
            
            -- Create a temporary table with the correct structure
            CREATE TABLE account_emailconfirmation_new (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                created DATETIME NOT NULL,
                sent DATETIME NULL,
                key VARCHAR(64) NOT NULL,
                email_address_id INTEGER NOT NULL REFERENCES account_emailaddress(id) DEFERRABLE INITIALLY DEFERRED
            );
            
            -- Copy data from the old table to the new one
            INSERT INTO account_emailconfirmation_new (id, created, sent, key, email_address_id)
            SELECT id, created, sent, key, email_address_id FROM account_emailconfirmation;
            
            -- Drop the old table
            DROP TABLE account_emailconfirmation;
            
            -- Rename the new table to the original name
            ALTER TABLE account_emailconfirmation_new RENAME TO account_emailconfirmation;
            
            -- Recreate the indexes
            CREATE INDEX account_emailconfirmation_email_address_id_5b7f8c58 ON account_emailconfirmation (email_address_id);
            CREATE UNIQUE INDEX account_emailconfirmation_key_f43612bd_uniq ON account_emailconfirmation (key);
            """,
            
            # Reverse SQL
            """
            -- No need to change the email confirmation table structure when reverting
            """
        )
    ]
