from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ptuevents', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='PTUsers',
            old_name='ad_guid',
            new_name='ad_sid',
        ),

        migrations.RenameField(
            model_name='PTWorkstations',
            old_name='ad_guid',
            new_name='ad_sid',
        ),

        migrations.AlterField(
            model_name='PTUsers',
            name='name',
            field=models.CharField(max_length=250),
        ),

        migrations.AddField(
            model_name='PTWorkstations',
            name='location',
            field=models.CharField(max_length=100, blank=True),
        ),

        migrations.RemoveField(
            model_name='PTUsers',
            name='comments',
        ),
    ]
