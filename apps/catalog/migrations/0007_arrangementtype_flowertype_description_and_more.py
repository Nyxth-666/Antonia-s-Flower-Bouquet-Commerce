import django.db.models.deletion
from django.db import migrations, models


def migrate_arrangement_types(apps, schema_editor):
    Bouquet = apps.get_model("catalog", "Bouquet")
    ArrangementType = apps.get_model("catalog", "ArrangementType")

    db_alias = schema_editor.connection.alias

    # Seed the predefined arrangement types.
    arrangement_data = [
        ("Inaugural Flowers", "Flowers for inaugurations and special ceremonies."),
        ("Flower Bouquets", "Beautiful flower bouquets for every occasion."),
        ("Chocolate Bouquets", "Creative bouquets made with flowers and chocolates."),
        ("Flower in a Card", "A lovely flower presented with a greeting card."),
        ("Flowers in a Box", "Flowers arranged beautifully inside a box."),
        ("Flower in a Vase", "Flowers arranged in an elegant vase."),
        ("Petite Bouquets", "Small and lovely bouquets for simple gifts."),
    ]

    for name, description in arrangement_data:
        ArrangementType.objects.using(db_alias).get_or_create(
            name=name,
            defaults={"description": description},
        )

    # Transfer existing bouquet arrangement names to their new ForeignKey.
    for bouquet in Bouquet.objects.using(db_alias).all().iterator():
        arrangement_name = (bouquet.arrangement_type or "").strip()

        if not arrangement_name:
            continue

        arrangement, _ = ArrangementType.objects.using(db_alias).get_or_create(
            name=arrangement_name,
        )

        Bouquet.objects.using(db_alias).filter(pk=bouquet.pk).update(
            arrangement_type_new_id=arrangement.pk
        )


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0006_flowertype_remove_bouquet_flower_type_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArrangementType",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="arrangement_types/",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name_plural": "Arrangement Types",
                "ordering": ["name"],
            },
        ),

        migrations.AddField(
            model_name="flowertype",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="flowertype",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="flower_types/",
            ),
        ),
        migrations.AddField(
            model_name="flowertype",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="occasion",
            name="description",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="occasion",
            name="icon",
            field=models.CharField(
                blank=True,
                help_text="Enter an emoji, e.g. 🎂 or 💐",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="occasion",
            name="is_active",
            field=models.BooleanField(default=True),
        ),

        # Temporary nullable ForeignKey.
        migrations.AddField(
            model_name="bouquet",
            name="arrangement_type_new",
            field=models.ForeignKey(
                to="catalog.arrangementtype",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                null=True,
                blank=True,
            ),
        ),

        # Copy the old text values into the new ForeignKey.
        migrations.RunPython(
            migrate_arrangement_types,
            migrations.RunPython.noop,
        ),

        # Remove the old text field.
        migrations.RemoveField(
            model_name="bouquet",
            name="arrangement_type",
        ),

        # Give the new ForeignKey its original field name.
        migrations.RenameField(
            model_name="bouquet",
            old_name="arrangement_type_new",
            new_name="arrangement_type",
        ),

        # Make the relationship required.
        migrations.AlterField(
            model_name="bouquet",
            name="arrangement_type",
            field=models.ForeignKey(
                to="catalog.arrangementtype",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="bouquets",
            ),
        ),
    ]