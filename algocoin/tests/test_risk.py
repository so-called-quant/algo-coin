class TestRisk:
    def setup(self):
        from ..lib.config import RiskConfig
        from ..risk import Risk

        rc = RiskConfig()
        rc.max_risk = 100.0
        rc.max_drawdown = 100.0
        rc.total_funds = 100.0

        self.risk = Risk(rc)

        # setup() before each test method

    def teardown(self):
        pass
        # teardown() after each test method

    @classmethod
    def setup_class(cls):
        pass
        # setup_class() before any methods in this class

    @classmethod
    def teardown_class(cls):
        pass
        # teardown_class() after any methods in this class

    def test_construct_reponse(self):
        pass

    def test_request(self):
        from ..lib.structs import TradeRequest, MarketData
        from ..lib.enums import TickType, Side
        from ..lib.utils import parse_date

        data = MarketData(type=TickType.TRADE,
                          time=parse_date('1479272400'),
                          price=float(1),
                          volume=float(100),
                          side=Side.BUY)
        req = TradeRequest(data=data, side=Side.BUY, volume=100.0, price=1.0)
        resp = self.risk.request(req)

        assert resp.risk_check == True
        assert resp.volume == 100.0
        assert self.risk.outstanding == 100.0
        assert self.risk.max_running_outstanding == 100.0
        assert self.risk.max_running_outstanding_incr == [100.0]

        req = TradeRequest(data=data, side=Side.BUY, volume=100.0, price=1.0)
        resp = self.risk.request(req)

        assert resp.risk_check == False

    def test_request2(self):
        from ..lib.structs import TradeRequest, MarketData
        from ..lib.enums import TickType, Side
        from ..lib.utils import parse_date

        data = MarketData(type=TickType.TRADE,
                          time=parse_date('1479272400'),
                          price=float(1),
                          volume=float(100),
                          side=Side.BUY)
        req = TradeRequest(data=data, side=Side.BUY, volume=50.0, price=1.0)
        resp = self.risk.request(req)

        assert resp.risk_check == True
        assert resp.volume == 50.0
        assert self.risk.outstanding == 50.0
        assert self.risk.max_running_outstanding == 50.0
        assert self.risk.max_running_outstanding_incr == [50.0]

        req = TradeRequest(data=data, side=Side.BUY, volume=100.0, price=1.0)
        resp = self.risk.request(req)

        assert resp.risk_check == True
        assert resp.volume == 50.0
        assert self.risk.outstanding == 100.0
        assert self.risk.max_running_outstanding == 100.0
        assert self.risk.max_running_outstanding_incr == [50.0, 100.0]

        req = TradeRequest(data=data, side=Side.BUY, volume=100.0, price=1.0)
        resp = self.risk.request(req)

        assert resp.risk_check == False

    def test_update(self):
        pass
