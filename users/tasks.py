# cashdesks/tasks.py
from decimal import Decimal
from datetime import datetime, timedelta
from celery import shared_task
from orders.models.order import Order
from users.models.lottery import Lottery
from users.models.customuser import CustomUser
from users.models.wallet import Wallet
from users.models.score import Score
from users.models.coupon import Coupon
import logging
logger = logging.getLogger(__name__)
#from users.models.notification import Notification


@shared_task(queue='gift_to_user')
def add_gift_to_user(order_id):
    try:
        # پیدا کردن سفارش بر اساس order_id
        order = Order.objects.get(pk=order_id)
        user = order.user
        
        # بررسی اینکه آیا این اولین سفارش کاربر است یا خیر
        is_first_order = not Order.objects.filter(user=user).exclude(pk=order_id).exists()

        if is_first_order:

            reason='is_first_order'            
            # ارسال تسک به صف قرعه‌کشی
            add_user_to_lottery.apply_async(args=[reason, order_id], queue='lottery')
            
            logger.info(f"User {user.username} with order {order_id} has been entered into the lottery queue.")
            # ایجاد تخفیف برای اولین سفارش

            # ثبت لاگ برای نمایش در سیستم
            logger.info(f"First order discount applied to user {user.username} with order {'order_id'}. Discount amount: {'discount_amount'}")
        
        else:
            logger.info(f"Order {'order_id'} is not the first order for user {user.username}. No discount applied.")
    
    except Order.DoesNotExist:
        logger.error(f"Order with ID {'order_id'} does not exist.")
    except Exception as e:
        logger.error(f"Error applying gift to user for order {'order_id'}: {e}")
        raise


@shared_task(queue='lottery')
def add_user_to_lottery(reason, order_id):
    try:
        # Try to retrieve the order by its ID
        order = Order.objects.get(pk=order_id)
        user = order.user
        
        # Create a lottery entry with the provided reason
        lottery = Lottery.objects.create(user=user, order=order, reason=reason)
        lottery.save()
        
        logger.info(f"User {user.username} with order {order_id} has been entered into the lottery for reason: {reason}.")
    
    except Order.DoesNotExist:
        logger.error(f"Order with ID {order_id} does not exist. Cannot add user to lottery.")
    
    except Exception as e:
        logger.error(f"Error adding user to lottery for order {order_id}: {e}")
        raise


@shared_task(queue='high_value_order')
def handle_high_value_order(order_id):

    reason='high_value_order'            
    # ارسال تسک به صف قرعه‌کشی
    add_user_to_lottery.apply_async(args=[reason, order_id], queue='lottery')


@shared_task(queue='apply_coupon')
def apply_coupon(order_id, code):
    order = Order.objects.get(pk=order_id)
    user = order.user
    
    # Calculate expiration date as 10 days from today
    expire_date = datetime.now() + timedelta(days=30)
    
    # Create the coupon with the expiration date
    coupon = Coupon.objects.create(user=user, code=code, expire_date=expire_date)
    coupon.save()


@shared_task(queue='send_notification')
def send_payment_notification(user_id, order_id):
    # منطق ارسال اعلان
    pass


@shared_task(queue='charge_wallet')
def charge_wallet(user_id, amount):
    try:
        logger.info(f"Starting charge_wallet for user {user_id} with amount {amount}")
        user = CustomUser.objects.get(id=user_id)
        
        # بررسی اینکه آیا ولتی برای یوزر وجود دارد یا نه
        wallet, created = Wallet.objects.get_or_create(user=user)

        # Convert amount to Decimal after removing commas
        amount = Decimal(amount.replace(',', ''))

        # Calculate 10% of the amount
        amount = amount * Decimal('0.10')
        #amount = amount * 1.10

        if not created:
            # اگر ولت قبلاً وجود داشته باشد، موجودی آن را افزایش دهید
            wallet.balance += Decimal(amount)
        else:
            wallet.balance = Decimal(amount)  # موجودی اولیه برای ولت جدید
        
        wallet.save()
        logger.info(f"Successfully charged wallet for user {user_id} with amount {amount}")

    except CustomUser.DoesNotExist:
        logger.error(f"User with id {user_id} does not exist.")
    except Exception as e:
        logger.error(f"Error charging wallet for user {user_id}: {e}")
        raise


@shared_task(queue='add_score')
def add_score(user_id,initial_order_score,reason,description):

    user=CustomUser.objects.filter(pk=user_id).first()

    Score.objects.create(user=user, score=initial_order_score, reason=reason, description=description)


