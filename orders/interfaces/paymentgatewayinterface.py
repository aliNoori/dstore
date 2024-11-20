from abc import ABC, abstractmethod

class PaymentGatewayInterface(ABC):
    
    @abstractmethod
    def process_payment(self, amount, order_id, callback_url):
        pass

    @abstractmethod
    def refund(self, transaction_id):
        pass

    @abstractmethod
    def get_status(self, transaction_id):
        pass
