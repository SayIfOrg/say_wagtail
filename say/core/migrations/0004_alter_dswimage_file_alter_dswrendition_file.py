# Generated by Django 4.2.1 on 2023-05-06 13:40

from django.db import migrations
import say.core.models
import wagtail.images.models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_dswdocument"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dswimage",
            name="file",
            field=say.core.models.DynamicWagtailImageField(
                height_field="height",
                upload_to=wagtail.images.models.get_upload_to,
                verbose_name="file",
                width_field="width",
            ),
        ),
        migrations.AlterField(
            model_name="dswrendition",
            name="file",
            field=say.core.models.DynamicWagtailImageField(
                height_field="height",
                storage=wagtail.images.models.get_rendition_storage,
                upload_to=wagtail.images.models.get_rendition_upload_to,
                width_field="width",
            ),
        ),
    ]
