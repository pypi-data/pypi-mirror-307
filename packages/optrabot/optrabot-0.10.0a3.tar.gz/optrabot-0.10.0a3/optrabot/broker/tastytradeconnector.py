import asyncio
from typing import List
from optrabot.broker.brokerconnector import BrokerConnector
from loguru import logger
from tastytrade import Account, DXLinkStreamer, Session
from optrabot.models import Account as ModelAccount
from tastytrade.utils import TastytradeError
from tastytrade.dxfeed import Greeks, Quote
import optrabot.config as optrabotcfg
from optrabot.broker.order import Order as BrokerOrder
from optrabot.tradetemplate.templatefactory import Template

class TastytradeConnector(BrokerConnector):
	def __init__(self) -> None:
		super().__init__()
		self._username = ''
		self._password = ''
		self._sandbox = False
		self._initialize()
		self.id = 'TASTY'
		self.broker = 'TASTY'
		self._session = None
		self._streamer: DXLinkStreamer

	def _initialize(self):
		"""
		Initialize the Tastytrade connector from the configuration
		"""
		config :optrabotcfg.Config = optrabotcfg.appConfig
		try:
			config.get('tastytrade')
		except KeyError as keyErr:
			logger.debug('No Tastytrade connection configured')
			return
		
		try:
			self._username = config.get('tastytrade.username')
		except KeyError as keyErr:
			logger.error('Tastytrade username not configured')
			return
		try:
			self._password = config.get('tastytrade.password')
		except KeyError as keyErr:
			logger.error('Tastytrade password not configured')
			return
		
		try:
			self._sandbox = config.get('tastytrade.sandbox')
		except KeyError as keyErr:
			pass
		self._initialized = True

	async def connect(self):
		await super().connect()
		try:
			self._session = Session(self._username, self._password, is_test=self._sandbox)
			self._emitConnectedEvent()
		except TastytradeError as tastyErr:
			logger.error('Failed to connect to Tastytrade: {}', tastyErr)
			self._emitConnectFailedEvent()

	def disconnect(self):
		super().disconnect()
		if self._session != None:
			self._session.destroy()
			self._session = None
			self._emitDisconnectedEvent()

	def getAccounts(self) -> List[ModelAccount]:
		"""
		Returns the Tastytrade accounts
		"""
		accounts: List[ModelAccount] = []
		if self.isConnected():
			for tastyAccount in Account.get_accounts(self._session):
				account = ModelAccount(id=tastyAccount.account_number, name=tastyAccount.nickname, broker = self.broker, pdt = not tastyAccount.day_trader_status)
				accounts.append(account)
		return accounts
	
	def isConnected(self) -> bool:
		if self._session != None:
			return True
		
	async def prepareOrder(self, order: BrokerOrder) -> bool:
		"""
		Prepares the given order for execution.
		- Retrieve current market data for order legs

		It returns True, if the order could be prepared successfully
		"""
		raise NotImplementedError()

	async def placeOrder(self, order: BrokerOrder, template: Template) -> bool:
		""" 
		Places the given order
		"""
		raise NotImplementedError()

	async def adjustOrder(self, order: BrokerOrder, price: float) -> bool:
		""" 
		Adjusts the given order with the given new price
		"""
		raise NotImplementedError()
		
	async def requestTickerData(self, symbols: List[str]):
		"""
		Request ticker data for the given symbols and their options
		"""
		self._streamer = await DXLinkStreamer.create(self._session)
		await self._streamer.subscribe(Quote, symbols)
		listen_quotes_task = asyncio.create_task(self._update_quotes())
		await asyncio.gather(listen_quotes_task)

	def getFillPrice(self, order: BrokerOrder) -> float:
		""" 
		Returns the fill price of the given order if it is filled
		"""
		raise NotImplementedError

	async def _update_quotes(self):
		logger.debug('Received Quote')
		async for e in self._streamer.listen(Quote):
			logger.trace('Received Quote for {} with data {}', e.eventSymbol, e)
			#self.quotes[e.eventSymbol] = e