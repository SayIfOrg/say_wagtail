# Generated by Django 4.2.1 on 2023-05-07 22:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("wagtailcore", "0084_merge_20230305_1030"),
        ("utils", "0004_alter_dswimage_file_alter_dswrendition_file"),
    ]

    operations = [
        migrations.AddField(
            model_name="dswimage",
            name="site",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="site_%(class)s",
                to="wagtailcore.site",
            ),
            preserve_default=False,
        ),
    ]
