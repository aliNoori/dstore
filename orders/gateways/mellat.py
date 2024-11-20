from requests import Session
from zeep import Client, Settings, Transport

from orders.interfaces.paymentgatewayinterface import PaymentGatewayInterface

class MellatGateway(PaymentGatewayInterface):
    def __init__(self):
        self.terminal_id = 'UHdf9J1D4QweieQOqVZT'
        self.wsdl = 'https://sandbox.banktest.ir/parsian/pec.shaparak.ir/NewIPGServices/Sale/SaleService.asmx?wsdl'
        self.wsdl_confirm = 'https://sandbox.banktest.ir/parsian/pec.shaparak.ir/NewIPGServices/Confirm/ConfirmService.asmx?wsdl'
        self.wsdl_reverse = 'https://sandbox.banktest.ir/parsian/pec.shaparak.ir/NewIPGServices/Reverse/ReversalService.asmx?wsdl'
        self.wsdl_multiplexed = 'https://sandbox.banktest.ir/parsian/pec.shaparak.ir/NewIPGServices/MultiplexedSale/OnlineMultiplexedSalePaymentService.asmx?wsdl'
        self.payment_gateway = 'https://sandbox.banktest.ir/parsian/pec.shaparak.ir/NewIPG'

    def process_payment(self, amount, order_id, callback_url):        
        
        # ایجاد یک جلسه درخواست (optional)
        session = Session()
        session.verify = True  # در صورتی که نیاز به بررسی گواهینامه SSL ندارید

        # تنظیمات خاص برای zeep
        settings = Settings(strict=False, xml_huge_tree=True)

        # ایجاد کلاینت با تنظیمات و transport
        client = Client(wsdl=self.wsdl, settings=settings, transport=Transport(session=session))
        service = client.bind('SaleService', 'SaleServiceSoap12')

        # Define your parameters
        params = {
            "LoginAccount": self.terminal_id,  # Replace with your actual account
            "Amount": amount,  # Example amount, replace with your actual amount
            "OrderId": order_id,  # Example Order ID, replace with your actual order ID
            "CallBackUrl": callback_url,  # Replace with your actual callback URL
            "AdditionalData": "Test data",
            "Originator": "",  # Optional, you can leave it as an empty string
        }
        
        try:
            # Make the SOAP request
            result = service.SalePaymentRequest(requestData=params)
            print(result)           
            token = result.Token
            url = f'{self.payment_gateway}/?Token={token}'            
            return url 
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # Optionally handle the exception

    def refund(self, transaction_id):
        # Logic for refunding payment
        print(f"Refunding transaction {transaction_id}")
        return True

    def get_status(self, transaction_id):
        # Logic for getting status of payment
        print(f"Getting status of transaction {transaction_id}")
        return "completed"
