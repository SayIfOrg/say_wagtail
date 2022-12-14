# Generated by Django 4.1.1 on 2022-09-08 05:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("super_page", "0004_delete_telegramactionorderable_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="TelegramInstance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Group"), (2, "Channel")]
                    ),
                ),
                ("chat_id", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="TelegramPublishMode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="The title for you to recognize this action",
                        max_length=63,
                    ),
                ),
                (
                    "publish_message",
                    models.BooleanField(
                        help_text="Incase of first publish(create) the content: Send new message?"
                    ),
                ),
                (
                    "republish_message",
                    models.BooleanField(
                        help_text="Incase of republish(edit) the content: Send new message?"
                    ),
                ),
                (
                    "edit_past_messages",
                    models.BooleanField(
                        help_text="Incase of republish(edit) the content: Edit previously sent messages?"
                    ),
                ),
                (
                    "as_reference_to_original_message",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "No reference"), (1, "Link"), (2, "Reply")],
                        default=0,
                        help_text="Incase of republish(edit) the content: How to mention original sent message?",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TelegramAction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="page_telegramactions",
                        to="super_page.simplepage",
                    ),
                ),
                (
                    "telegram_instance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="linked_account.telegraminstance",
                    ),
                ),
                (
                    "telegram_publish_mode",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="linked_account.telegrampublishmode",
                    ),
                ),
            ],
        ),
    ]
