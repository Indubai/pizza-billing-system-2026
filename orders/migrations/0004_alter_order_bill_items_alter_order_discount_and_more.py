import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_user'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(

            database_operations=[
                migrations.AddField(
                    model_name='order',
                    name='bill_items',
                    field=models.JSONField(default=list),
                ),
                migrations.AddField(
                    model_name='order',
                    name='subtotal',
                    field=models.DecimalField(
                        max_digits=10,
                        decimal_places=2,
                        default=0
                    ),
                ),
                migrations.AddField(
                    model_name='order',
                    name='discount',
                    field=models.DecimalField(
                        max_digits=10,
                        decimal_places=2,
                        default=0
                    ),
                ),
                migrations.AddField(
                    model_name='order',
                    name='final_total',
                    field=models.DecimalField(
                        max_digits=10,
                        decimal_places=2,
                        default=0
                    ),
                ),
                migrations.AddField(
                    model_name='order',
                    name='payment_method',
                    field=models.CharField(
                        max_length=30,
                        default='Cash on Delivery',
                        choices=[
                            ('Cash on Delivery', 'Cash on Delivery'),
                            ('UPI', 'UPI'),
                            ('Card Payment', 'Card Payment'),
                        ],
                    ),
                ),
                migrations.AddField(
                    model_name='order',
                    name='created_at',
                    field=models.DateTimeField(
                        auto_now_add=True
                    ),
                ),
            ],

            state_operations=[
                migrations.AlterField(
                    model_name='order',
                    name='bill_items',
                    field=models.JSONField(default=list),
                ),
                migrations.AlterField(
                    model_name='order',
                    name='discount',
                    field=models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10
                    ),
                ),
                migrations.AlterField(
                    model_name='order',
                    name='final_total',
                    field=models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10
                    ),
                ),
                migrations.AlterField(
                    model_name='order',
                    name='subtotal',
                    field=models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=10
                    ),
                ),
            ],
        ),
    ]