import requests

from config import settings


class PaymentService:
    """
    Сервис для обработки онлайн-платежей
    """

    @staticmethod
    def process_online_payment(order, payment_data):
        if order.onlineMethod == 'sbp':
            return PaymentService._process_sbp_payment(order)
        elif order.onlineMethod == 'yoomoney':
            return PaymentService._process_yoomoney_payment(order, payment_data)
        elif order.onlineMethod == 'card':
            return PaymentService._process_card_payment(order, payment_data)
        else:
            raise ValueError("Неизвестный метод онлайн оплаты")

    @staticmethod
    def _process_sbp_payment(order):
        """
        Процесс оплаты через СБП
        """
        sbp_url = "https://sbp-api.example.com/create_invoice"
        headers = {
            "Authorization": f"Bearer {settings.SBP_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": int(order.totalPrice * 100),  # Сумма в копейках
            "order_id": str(order.id),
            "return_url": "https://yourstore.com/payment/success"
        }
        response = requests.post(sbp_url, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception("Ошибка при создании счёта в СБП")
        return response.json()

    @staticmethod
    def _process_yoomoney_payment(order, payment_data):
        """
        Процесс оплаты через YooMoney (бывшая Яндекс.Касса)
        """
        yoomoney_url = "https://yoomoney.ru/api/checkout"
        headers = {
            "Authorization": f"Bearer {settings.YOOMONEY_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": int(order.totalPrice * 100),  # Сумма в копейках
            "order_id": str(order.id),
            "payment_data": payment_data,
            "return_url": "https://yourstore.com/payment/success"
        }
        response = requests.post(yoomoney_url, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception("Ошибка при обработке оплаты через YooMoney")
        return response.json()

    @staticmethod
    def _process_card_payment(order, payment_data):
        """
        Процесс оплаты картой через сторонний процессинг
        """
        card_url = "https://card-api.example.com/process"
        headers = {
            "Authorization": f"Bearer {settings.CARD_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "amount": int(order.totalPrice * 100),  # Сумма в копейках
            "order_id": str(order.id),
            "card_number": payment_data.get('card_number'),
            "cvv": payment_data.get('cvv'),
            "expiry_date": payment_data.get('expiry_date'),
            "return_url": "https://yourstore.com/payment/success"
        }
        response = requests.post(card_url, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception("Ошибка при обработке оплаты картой")
        return response.json()
