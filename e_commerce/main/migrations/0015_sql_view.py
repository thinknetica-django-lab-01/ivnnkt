from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_auto_20210302_2057'),
    ]

    sql = """
    CREATE OR REPLACE VIEW user_product AS
      SELECT main_product.name AS name, auth_user AS user 
      FROM main_product INNER JOIN auth_user
      ON auth_user.id = main_product.owner;

    """

    operations = [
        migrations.RunSQL('DROP VIEW IF EXISTS user_product;'),
        migrations.RunSQL(sql)
    ]