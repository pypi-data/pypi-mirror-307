import asyncio
import datetime as dt
from typing import Dict, List
from optrabot.optionhelper import OptionHelper
from optrabot.broker.brokerconnector import BrokerConnector
from loguru import logger
from ib_insync import *
import optrabot.config as optrabotcfg
from optrabot.models import Account
from optrabot.broker.order import Leg, OptionRight, Order as BrokerOrder, OrderAction, OrderType, OrderStatus as BrokerOrderStatus
from optrabot.tradetemplate.templatefactory import Template

class OptionPriceData:
	def __init__(self) -> None:
		self.callBid: float = None
		self.callAsk: float = None
		self.callDelta: float = None
		self.putBid: float = None
		self.putAsk: float = None
		self.putDelta: float = None

class OptionStrikeData:
	def __init__(self) -> None:
		pass
		self.strikeData: Dict[float, OptionPriceData] = {}

class IBSymbolData:
	def __init__(self) -> None:
		self.symbol: str = None
		self.contract: Contract = None
		self.ticker = None
		self.noPriceDataCount = 0
		self.optionPriceData: Dict[dt.date, OptionStrikeData] = {}

class IBTWSTConnector(BrokerConnector):
	def __init__(self) -> None:
		super().__init__()
		self._host = ''
		self._port = None
		self._clientid = None
		self._initialize()
		self.id = 'IBTWS'
		self.broker = 'IBKR'
		self._ib = None
		self._symbolData: Dict[str, IBSymbolData] = {}
		self._orders: List[BrokerOrder] = []

	def _initialize(self):
		"""
		Initialize the TWS connector from the configuration
		"""
		config :optrabotcfg.Config = optrabotcfg.appConfig
		if not config.get('tws'):
			logger.debug('No TWS connection configured')
			return
		
		self._host = config.get('tws.host')
		if self._host == '':
			self._host = 'localhost'
		
		try:
			self._port = int(config.get('tws.port'))
		except KeyError as keyErr:
			self._port = 7496
		try:
			self._clientid = int(config.get('tws.clientid'))
		except KeyError as keyErr:
			self._clientid = 21
		self._initialized = True

	async def connect(self):
		await super().connect()
		self._ib = IB()
		asyncio.create_task(self._connect_tws_task())

	def disconnect(self):
		super().disconnect()
		try:
			self._ib.disconnectedEvent -= self.onDisconnected
			self._ib.errorEvent -= self.onErrorEvent
			self._ib.execDetailsEvent -= self.onExecDetailsEvent
			self._ib.orderStatusEvent -= self.onOrderStatusEvent
			self._ib.commissionReportEvent -= self.onCommissionReportEvent
			self._ib.pendingTickersEvent -= self.onPendingTickers
			self._ib.disconnect()
		except Exception as excp:
			pass

	def getAccounts(self) -> List[Account]:
		"""
		Returns the accounts managed by the TWS connection
		"""
		accounts: List[Account] = []
		for managedAccount in self._ib.managedAccounts():
			account = Account(id = managedAccount, name = managedAccount, broker = self.broker, pdt = False)
			accounts.append(account)
		return accounts

	def isConnected(self) -> bool:
		return self._ib.isConnected()
	
	async def prepareOrder(self, order: BrokerOrder) -> bool:
		"""
		Prepares the given order for execution.
		- Retrieve current market data for order legs

		It returns True, if the order could be prepared successfully
		"""
		logger.debug("Prepare Order")
		symbolData = self._symbolData[order.symbol]
		current_date = dt.date.today()
		expiration = current_date.strftime('%Y%m%d')
		comboLegs: list[ComboLeg] = []
		comboContracts: list[Contract] = []
		for leg in order.legs:
			legContract = Option(symbolData.contract.symbol, expiration, leg.strike, self._mappedRight(leg.right), 'SMART', tradingClass = self._determineTradingClass(symbolData.contract.symbol))
			await self._ib.qualifyContractsAsync(legContract)
			if not OptionHelper.checkContractIsQualified(legContract):
				logger.error("Contract {} is not qualified!", legContract)
				return False
			comboContracts.append(legContract)
			leg.brokerSpecific['contract'] = legContract
			comboLeg = ComboLeg(conId=legContract.conId, ratio=1, action=self._mappedOrderAction(leg.action), exchange='SMART')
			comboLegs.append(comboLeg)

		order.brokerSpecific['comboLegs'] = comboLegs

		# Request Market Data
		validPriceData = True
		for i in range(5):
			tickers: List[Ticker] = await self._ib.reqTickersAsync(*comboContracts)
			logger.debug("Tickers {}", tickers)
			
			for leg in order.legs:
				for ticker in tickers:
					if ticker.contract.strike == leg.strike and ticker.contract.right == self._mappedRight(leg.right):
						if (util.isNan(ticker.ask) or util.isNan(ticker.bid) or (ticker.ask == -1.00 and ticker.bid == -1.00)) and leg.action == OrderAction.SELL:
							# No ask/bid price for sell leg. This is not valid
							validPriceData = False
						else:
							if util.isNan(ticker.ask) or ticker.ask == -1.00:
								leg.askPrice = 0
							else:
								leg.askPrice = ticker.ask
							if util.isNan(ticker.bid) or ticker.bid == -1.00:
								leg.bidPrice = 0
							else:
								leg.bidPrice = ticker.bid
						break
			if validPriceData:
				break
			await asyncio.sleep(1)
		if validPriceData == False:
			logger.error("No valid price data could be retrieved for order legs!")
			return False
		
		return True

	async def placeOrder(self, order: BrokerOrder, template: Template) -> bool:
		""" 
		Places the given order. It returns True if the entry order has been placed.
		"""
		logger.debug('Place order')
		symbolData = self._symbolData[order.symbol]

		logger.debug('Checking for open Trades if Combo Legs are colliding')
		contractsWithOpenOrders = await self._getAllOpenOrderContracts(template.account, symbolData.contract.symbol)

		comboLegs = order.brokerSpecific['comboLegs']
		if not comboLegs:
			logger.error("Internal Error: Broker specific attribute comboContracts not filled!")
			return
		
		comboContract = Contract(symbol=symbolData.contract.symbol, secType='BAG', exchange='SMART', currency=symbolData.contract.currency, comboLegs=comboLegs)
		if order.type == OrderType.LIMIT:
			#order.price -= 0.50
			ibOrder = LimitOrder(self._mappedOrderAction(order.action), order.quantity, order.price)
			ibOrder.account = template.account
			ibOrder.outsideRth = True
		elif order.type == OrderType.STOP:
			ibOrder = StopOrder(self._mappedOrderAction(order.action), order.quantity, order.price)
			ibOrder.account = template.account
			ibOrder.outsideRth = True
		else:
			logger.error(f'Order type {order.type} currently not supported by IBKR Connector!')

		ibOrder.orderRef = order.orderReference
		if order.ocaGroup:
			ibOrder.ocaGroup = order.ocaGroup
		trade = self._ib.placeOrder(comboContract, ibOrder)
		order.brokerSpecific['comboContract'] = comboContract
		order.brokerSpecific['order'] = ibOrder
		order.brokerSpecific['trade'] = trade
		self._orders.append(order)
		logger.debug("Account: {} Trade placed: {} Number of contracts: {}", template.account, trade, order.quantity)

		return True
	
	async def adjustOrder(self, order: BrokerOrder, price: float) -> bool:
		""" 
		Adjusts the given order with the given new price
		"""
		if order.status == BrokerOrderStatus.FILLED:
			logger.info('Order {} is already filled. Adjustment not required.', order)
			return True
		
		trade: Trade = order.brokerSpecific['trade']
		try:
			comboContract = order.brokerSpecific['comboContract']
			ibOrder: Order = order.brokerSpecific['order']
			ibOrder.lmtPrice = price
			self._ib.placeOrder(comboContract, ibOrder)
			return True
		except Exception as excp:
			logger('Exception beim Anpassen der Order')
		return False



	async def requestTickerData(self, symbols: List[str]):
		"""
		Request ticker data for the given symbols and their options
		"""
		self._ib.pendingTickersEvent += self.onPendingTickers
		for symbol in symbols:
			requestOptionsData = False
			optiontradingclass = ''
			match symbol:
				case 'SPX':
					symbolData = IBSymbolData()
					symbolData.symbol = symbol
					symbolData.contract = Index('SPX', 'CBOE')
					self._symbolData[symbol] = symbolData
					requestOptionsData = True
					optiontradingclass = 'SPXW'
				case 'VIX':
					symbolData = IBSymbolData()
					symbolData.symbol = symbol
					symbolData.contract = Index('VIX', 'CBOE')
					self._symbolData[symbol] = symbolData
				case _:
					logger.error(f'Symbol {symbol} currently not supported by IBKR Connector!')
					continue

			await self._ib.qualifyContractsAsync(symbolData.contract)
			self._ib.reqMktData(symbolData.contract, '', False, False)

			# if requestOptionsData:
			# 	chains = await self._ib.reqSecDefOptParamsAsync(symbolData.contract.symbol, '', symbolData.contract.secType, symbolData.contract.conId)
			# 	chain = next(c for c in chains if c.tradingClass == optiontradingclass and c.exchange == 'SMART')
			# 	if chain == None:
			# 		logger.error(f'No Option Chain for trading class {optiontradingclass} found. Unable to request option data')
			# 		return
				
			# 	current_date = dt.date.today()
			# 	expiration = current_date.strftime('%Y%m%d')

			# 	if int(chain.expirations[0]) > int(expiration):
			# 		logger.warning('There are no SPX options expiring today!')
			# 		return

	async def _connect_tws_task(self):
		try:
			self._ib.errorEvent += self.onErrorEvent
			await self._ib.connectAsync(self._host, self._port, clientId=self._clientid)
			self._emitConnectedEvent()
			self._ib.disconnectedEvent += self.onDisconnected
			self._ib.execDetailsEvent += self.onExecDetailsEvent
			self._ib.orderStatusEvent += self.onOrderStatusEvent
			self._ib.commissionReportEvent += self.onCommissionReportEvent
			
		except Exception as excp:
			self._emitConnectFailedEvent()
			#logger.error("Error connecting TWS: {}", excp)
			#attempt += 1
			#logger.error('Connect failed. Retrying {}. attempt in {} seconds', attempt, delaySecs)
			#await asyncio.sleep(delaySecs)
			#asyncio.create_task(self._connect_ib_task(attempt, delaySecs))

	async def onDisconnected(self):
		#logger.warning('Disconnected from TWS, attempting to reconnect in 30 seconds ...')
		self._tradingEnabled = False
		#asyncio.create_task(self._reconnect_ib_task())
		self._emitDisconnectedEvent()

	async def onErrorEvent(self, reqId: int, errorCode: int, errorString: str, contract: Contract):
		if errorCode in { 201, 202, 399, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2157, 2158}:
			# 201: Order rejected - reason:Stop price revision is disallowed after order has triggered
			# 202: Order wurde storniert z.B. TP order bei OCO, wenn SL Order ausgeführt wurde
			# 399: Warnung das die Order nur während der regulären Handelszeiten ausgeführt wird
			# 2103, 2104, 2105, 2106, 2108, 2158: Marktdatenverbindung ignorieren
			# 2107: Die Verbindung zum HMDS-Datenzentrum is inaktv, sollte jedoch auf Anfrage verfügbar seind
			# 2109: Warnhinweis zu einem Orderereignis außerhalb der regulären Handelszeiten
			# 2157: Verbindung zum Sec-def-Datenzentrum unterbrochen
			return
		elif errorCode == 1100:
			# Connection between TWS and IB lost.
			logger.warning('Connection between TWS and Interactive Brokers lost -> Trading disabled!')
			self._tradingEnabled = False
			return
		elif errorCode == 1102:
			# Connection between TWS and IB restored
			logger.success('Connection between TWS and Interactive Brokers has been reestablished! -> Trading enabled!')
			self._tradingEnabled = True
			return

		errorData = {'action': 'errorEvent','reqId':reqId, 'errorCode':errorCode, 'errorString':errorString, 'contract': contract}
		logger.error('IB raised following error: {}', errorData)
	
	async def onExecDetailsEvent(self, trade: Trade, fill: Fill):
		""" This eventhandler is called on trade execution
		"""
		logger.warning("TWS Connector Handler: onExecDetailsEvent not implemented")

	async def onCommissionReportEvent(self, trade: Trade, fill: Fill, report: CommissionReport):
		"""
		Handles the Commission Report Event
		"""
		logger.warning("TWS Connector Handler: onCommissionReportEvent not implemented")

	async def onOrderStatusEvent(self, trade: Trade):
		"""
		Handles the Order Status Event
		"""
		logger.debug(f'onOrderStatusEvent() Status: {trade.orderStatus.status}')
		relevantOrder: BrokerOrder = None
		for order in self._orders:
			brokerSpecificTrade: Trade = order.brokerSpecific['trade']
			if brokerSpecificTrade.order.orderId == trade.order.orderId:
				relevantOrder = order
				break
		if relevantOrder == None:
			logger.debug(f'No managed order matched the status event')
			return
		
		if trade.orderStatus.status == OrderStatus.Cancelled:
			logEntry: TradeLogEntry = None
			for logEntry in trade.log:
				if logEntry.status != 'Cancelled':
					continue
				logger.debug(f'Order Log: {logEntry}')
			if logEntry == None:
				logger.error(f'No log entry found for cancelled order!')
			elif logEntry.errorCode == 103:
				# Error 103, reqId 10292: Doppelt vorhandene Order-ID
				logger.info('Adjustment of entry order has been rejected, because Duplicate Order-ID. Entry Order still active.')
				# Das Ereignis nicht weiter verarbeiten
				return
		
		filledAmount = 0
		if trade.orderStatus.status == OrderStatus.Filled:
			filledAmount = relevantOrder.quantity - trade.remaining()
			relevantOrder.averageFillPrice = trade.orderStatus.avgFillPrice

		self._emitOrderStatusEvent(relevantOrder, self._genericOrderStatus(trade.orderStatus.status), filledAmount)
		
	def getFillPrice(self, order: BrokerOrder) -> float:
		""" 
		Returns the fill price of the given order if it is filled
		"""
		trade: Trade = order.brokerSpecific['trade']
		return trade.orderStatus.avgFillPrice

	async def onPendingTickers(self, tickers: List[Ticker]):
		"""
		Handles the pending tickers event
		"""
		for ticker in tickers:
			if ticker.contract.symbol in self._symbolData.keys():
				logger.trace(f'Ticker for symbol {ticker.contract.symbol} received.')
				self._tradingEnabled = True
				ticker.lastExchange
				logger.trace(f'Ticker Last {ticker.last}: {ticker}')

				symbolData = self._symbolData[ticker.contract.symbol]
				symbolData.ticker = ticker

				# Prüfen ob Preisdaten vorhanden sind
				lastPrice = symbolData.ticker.last
				if util.isNan(lastPrice):
					lastPrice = symbolData.ticker.close
				if util.isNan(lastPrice):
					# Wenn mehrmals keine gültigen Preisdaten empfangen wurden, dann wird der Handel deaktiviert
					symbolData.noPriceDataCount += 1
					if symbolData.noPriceDataCount > 5:
						logger.error(f'Receiving no valid price data for symbol {symbolData.symbol}. Trading disabled!')
						self._tradingEnabled = False
						break
				else:
					symbolData.noPriceDataCount = 0
					self._tradingEnabled = True

				# Für VIX werden keine weiteren Daten gelesen
				if ticker.contract.symbol == 'VIX':
					break

				# Options Stikes ermitteln und deren Preisdaten abfrangen, wenn notwendig
				# 20 Strikes um den ATM Strike herum
				atmStrike = OptionHelper.roundToStrikePrice(lastPrice)
				#logger.debug(f'ATM Strike: {atmStrike}')
				# TODO: Ticker Daten für Optionen abfragen
				break

	def _genericOrderStatus(self, status: OrderStatus) -> BrokerOrderStatus:
		"""
		Maps the IBKR specific order status to the general order status
		"""
		match status:
			case OrderStatus.PendingSubmit:
				return BrokerOrderStatus.OPEN
			case OrderStatus.PreSubmitted:
				return BrokerOrderStatus.OPEN
			case OrderStatus.Submitted:
				return BrokerOrderStatus.OPEN
			case OrderStatus.ApiCancelled:
				return BrokerOrderStatus.CANCELLED
			case OrderStatus.Cancelled:
				return BrokerOrderStatus.CANCELLED
			case OrderStatus.Filled:
				return BrokerOrderStatus.FILLED
			case OrderStatus.Inactive:
				return BrokerOrderStatus.CANCELLED
			case OrderStatus.PendingCancel:
				return BrokerOrderStatus.OPEN
			case OrderStatus.Cancelled:
				return BrokerOrderStatus.CANCELLED

	def _mappedOrderAction(self, action: OrderAction) -> str:
		"""
		Maps the general order action to the IBKR specific order action
		"""
		match action:
			case OrderAction.BUY:
				return 'BUY'
			case OrderAction.BUY_TO_OPEN:
				return 'BUY'
			case OrderAction.SELL:
				return 'SELL'
			case OrderAction.SELL_TO_CLOSE:
				return 'SELL'
			case _:
				logger.error(f'Order action {action} not supported by IBKR Connector!')
				return None
	
	def _mappedRight(self, right: OptionRight) -> str:
		"""
		Maps the general option right to the IBKR specific option right
		"""
		match right:
			case OptionRight.CALL:
				return 'C'
			case OptionRight.PUT:
				return 'P'
			case _:
				raise ValueError(f'Option right {right} not supported by IBKR Connector!')
				return None
			
	async def _getAllOpenOrderContracts(self, account, symbol) -> List:
		"""
		Determine the ContractIds of all open Orders for the given account and symbol
		"""
		openTrades: List[Trade] = await self._ib.reqAllOpenOrdersAsync()
		openOrderContracts = list()
		for openTrade in openTrades:
			if openTrade.contract.symbol != symbol or openTrade.order.account != account:
				continue
			if openTrade.contract.secType == 'BAG':
				for leg in openTrade.contract.comboLegs:
					openOrderContracts.append(leg.conId)
			else:
				openOrderContracts.append(openTrade.contract.conId)
		return openOrderContracts
	
	def _determineTradingClass(self, symbol: str) -> str:
		"""
		Determine the trading class for the given symbol
		"""
		match symbol:
			case 'SPX':
				return 'SPXW'
			case _:
				return ''
	
	def _calculateMidPrice(self, legs: List[Leg], tickers: List[Ticker], contracts: List[Contract]) -> float:
		"""
		Calculates the mid price for the given tickers
		"""
		midPrice = None
		for leg in legs:
			for ticker in tickers:
				if ticker.contract.strike == leg.strike and ticker.contract.right == self._mappedRight(leg.right):
					leg
					legMidPrice = (ticker.ask + ticker.bid) / 2
					if util.isNan(legMidPrice) or (ticker.ask == -1.00 and ticker.bid == -1.00):
						if leg.action == OrderAction.BUY:
							legMidPrice = 0.05
						else:
							return None
					if leg.action == OrderAction.SELL:
						midPrice = -legMidPrice
					else:
						midPrice += legMidPrice
					break

		return OptionHelper.roundToTickSize(midPrice)