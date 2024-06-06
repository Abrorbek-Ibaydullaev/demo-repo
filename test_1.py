class Currency:
    def __init__(self, amount):
        self.set_amount(amount)

    def get_amount(self):
        return self._amount

    def set_amount(self, amount):
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        self._amount = amount

    def convert_to(self, target):
        if isinstance(target, Currency):
            return self._convert_to_currency(target)
        elif isinstance(target, str):
            return self._convert_to_currency_code(target)
        else:
            raise TypeError("Target must be a Currency object or string")

    def _convert_to_currency(self, target_currency):
        raise NotImplementedError("Subclasses should implement this method")

    def _convert_to_currency_code(self, currency_code):
        raise NotImplementedError("Subclasses should implement this method")

    def __str__(self):
        return f"{self._amount:.0f} {self.__class__.__name__}"


class UniversalCurrency(Currency):
    def __init__(self, amount, currency_code, exchange_rates=None):
        super().__init__(amount)
        self.currency_code = currency_code
        if exchange_rates is None:
            self.exchange_rates = {
                "USD": 1.0,
                "EUR": 0.85,
                "JPY": 110.0,
                "GBP": 0.75,
            }
        else:
            self.exchange_rates = exchange_rates

        if currency_code not in self.exchange_rates:
            raise ValueError(f"Unsupported currency code: {currency_code}")

    def add_currency(self, currency_code, exchange_rate):
        if exchange_rate <= 0:
            raise ValueError("Exchange rate must be positive.")
        self.exchange_rates[currency_code] = exchange_rate
        print(
            f"Added currency {currency_code} with exchange rate {exchange_rate}. Current exchange rates: {self.exchange_rates}")

    def update_exchange_rate(self, currency_code, exchange_rate):
        if currency_code not in self.exchange_rates:
            raise ValueError(f"Currency code {currency_code} does not exist.")
        if exchange_rate <= 0:
            raise ValueError("Exchange rate must be positive.")
        self.exchange_rates[currency_code] = exchange_rate
        print(
            f"Updated exchange rate for {currency_code} to {exchange_rate}. Current exchange rates: {self.exchange_rates}")

    def _convert_to_currency(self, target_currency):
        if not isinstance(target_currency, UniversalCurrency):
            raise TypeError(
                "Target currency must be an instance of UniversalCurrency")

        base_amount = self._amount / self.exchange_rates[self.currency_code]
        target_amount = base_amount * \
            self.exchange_rates[target_currency.currency_code]
        return UniversalCurrency(target_amount, target_currency.currency_code, self.exchange_rates)

    def _convert_to_currency_code(self, currency_code):
        if currency_code not in self.exchange_rates:
            raise ValueError(f"Unsupported currency code: {currency_code}")

        base_amount = self._amount / self.exchange_rates[self.currency_code]
        target_amount = base_amount * self.exchange_rates[currency_code]
        return UniversalCurrency(target_amount, currency_code, self.exchange_rates)

    def __str__(self):
        return f"{self._amount:.2f} {self.currency_code}"


class Transaction:
    def __init__(self, amount, currency_code):
        self.amount = amount
        self.currency_code = currency_code

    def send_money(self, recipient, amount):
        if amount > self.amount:
            raise ValueError("Insufficient funds.")
        self.amount -= amount
        recipient.receive_money(amount)
        print(f"Sent {amount} {self.currency_code} to {recipient}")

    def receive_money(self, amount):
        self.amount += amount
        print(f"Received {amount} {self.currency_code}")

    def __str__(self):
        return f"Transaction(amount={self.amount}, currency_code={self.currency_code})"


class InternationalTransaction(Transaction):
    def __init__(self, amount, currency_code, exchange_rates):
        super().__init__(amount, currency_code)
        self.exchange_rates = exchange_rates

    def send_money(self, recipient, amount, recipient_currency_code):
        if amount > self.amount:
            raise ValueError("Insufficient funds.")
        self.amount -= amount
        converted_amount = self.convert_currency(
            amount, self.currency_code, recipient_currency_code)
        recipient.receive_money(converted_amount, recipient_currency_code)
        print(
            f"Sent {amount} {self.currency_code} ({converted_amount:.2f} {recipient_currency_code}) to {recipient}")

    def receive_money(self, amount, currency_code):
        converted_amount = self.convert_currency(
            amount, currency_code, self.currency_code)
        self.amount += converted_amount
        print(
            f"Received {amount} {currency_code} ({converted_amount:.2f} {self.currency_code})")

    def convert_currency(self, amount, from_currency, to_currency):
        if from_currency not in self.exchange_rates or to_currency not in self.exchange_rates:
            raise ValueError("Unsupported currency code.")
        base_amount = amount / self.exchange_rates[from_currency]
        target_amount = base_amount * self.exchange_rates[to_currency]
        return target_amount

    def __str__(self):
        return f"InternationalTransaction(amount={self.amount}, currency_code={self.currency_code}, exchange_rates={self.exchange_rates})"
