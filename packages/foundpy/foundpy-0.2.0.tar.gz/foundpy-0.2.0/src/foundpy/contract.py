from .util import *
from .config import *

@check_setup_on_create
class Account:
    def __init__(self, account=None, privkey=None) -> None:
        if privkey:
            self.account = config.w3.eth.account.from_key(privkey)
        else:
            self.account = account
        self.address = self.account.address

    def send(self, to, value):
        tx = {
            "from": self.address,
            "to": to,
            "value": value
        }
        tx_hash = config.w3.eth.send_transaction(tx)
        return tx_hash
    
    def get_balance(self):
        return get_balance(self.address)

@check_setup_on_create
class Contract:
    def __init__(self, addr, file=None, abi=None) -> None:
        self.file = file
        self.address = addr
        self.abi = None
        if abi:
            self.abi = abi
            self.contract = config.w3.eth.contract(addr, abi=abi)
        elif file:
            self.abi = self.get_abi()
            self.contract = config.w3.eth.contract(addr, abi=self.abi)

    def call(self, func_name, *args):
        if self.abi:
            return getattr(self.contract.functions, func_name)(*args).call()
        else:
            function_selector = calculate_function_selector(func_name)
            encoded_args = encode_arguments(func_name, *args)
            data = function_selector + encoded_args
            tx = {
                "from": config.wallet.address,
                "to": self.address,
                "data": data
            }
            return config.w3.eth.call(tx)
    
    def code(self):
        return config.w3.eth.get_code(self.address)
    
    def codesize(self):
        return len(self.code())

    def send(self, func_name, *args, value=0):
        if self.abi:
            return getattr(self.contract.functions, func_name)(*args).transact({"value":value})
        else:
            function_selector = calculate_function_selector(func_name)
            encoded_args = encode_arguments(func_name, *args)
            data = function_selector + encoded_args
            tx = {
                "from": config.wallet.address,
                "to": self.address,
                "data": data,
                "value": value
            }
            tx_hash = config.w3.eth.send_transaction(tx)
            return tx_hash
        
    def storage(self, slot):
        return config.w3.eth.get_storage_at(self.address, slot)

    def get_abi(self):
        return compile_file(self.file)['abi']
    
    def get_balance(self):
        return get_balance(self.address)

@call_check_setup
def deploy_contract(file, *args, value=0):
    compiled_sol = compile_file(file)
    abi = compiled_sol['abi']
    bytecode = compiled_sol['bin']
    contract = config.w3.eth.contract(abi=abi, bytecode=bytecode)
    tx_hash = contract.constructor(*args).transact({"from":config.wallet.address, "value":value})
    tx_receipt = config.w3.eth.wait_for_transaction_receipt(tx_hash)
    contract = Contract(tx_receipt.contractAddress, file, abi)
    return contract