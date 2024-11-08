import os
import collections
from .yamler import yamler

class FrozenConfig:

    def __init__(self):

        self.proj_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        default_cfg = yamler(f'{self.proj_path}/basis/config/default_config.yaml').get_all_fields()
        user_cfg = yamler(f'{self.proj_path}/basis/config/user_config.yaml').get_all_fields()
        self.all_config = collections.ChainMap(user_cfg, default_cfg)

        # strategy log config
        self.log_path = self.all_config['log_config']['log_path']

        # database config
        self.database = self.all_config['database_config']['database']

        # framework run config
        self.min_shares = self.all_config['run_config']['min_shares']
        self.upper_bound = self.all_config['run_config']['upper_bound']
        self.lower_bound = self.all_config['run_config']['lower_bound']
        self.seed = self.all_config['run_config']['seed']

        # client config
        self.init_capital = self.all_config['client_config']['init_capital']
        self.slippage = self.all_config['client_config']['slippage']
        self.commission = self.all_config['client_config']['commission']
        self.stamp_duty = self.all_config['client_config']['stamp_duty']
        self.min_cost = self.all_config['client_config']['min_cost']

        # strategy config
        self.benchmark = self.all_config['strategy_config']['benchmark']
        self.index_code = self.all_config['strategy_config']['index_code']
        self.start_date = self.all_config['strategy_config']['start_date']
        self.end_date = self.all_config['strategy_config']['end_date']
        self.max_instruments = self.all_config['strategy_config']['max_instruments']
        self.date_rule = self.all_config['strategy_config']['date_rule']

        # portfolio config
        self.optimizer = self.all_config['portfolio_config']['optimizer']
        self.cov_method = self.all_config['portfolio_config']['cov_est']['cov_method']
        self.cov_window = self.all_config['portfolio_config']['cov_est']['cov_window']
        self.opt_func = self.all_config['portfolio_config']['opt_func']
        self.long_short = self.all_config['portfolio_config']['long_short']


frozen_config = FrozenConfig()
