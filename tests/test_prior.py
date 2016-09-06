import sys

sys.path.append('../')

import LMR_config as cfg
import LMR_prior
import numpy as np
import pytest


def test_prior_seed():
    cfg_obj = cfg.Config()
    prior_cfg = cfg_obj.prior
    prior_cfg.seed = 2
    prior_source = '20cr'
    datadir_prior = 'data'
    datafile_prior = '[vardef_template]_gridded_dat.nc'
    state_variables = ['air']
    state_kind = 'anom'

    X = LMR_prior.prior_assignment(prior_source)

    X.prior_datadir = datadir_prior
    X.prior_datafile = datafile_prior
    X.statevars = state_variables
    X.Nens = 1
    X.detrend = False
    X.kind = state_kind

    X.populate_ensemble(prior_source, prior_cfg)

    X2 = LMR_prior.prior_assignment(prior_source)

    X2.prior_datadir = datadir_prior
    X2.prior_datafile = datafile_prior
    X2.statevars = state_variables
    X2.Nens = 1
    X2.detrend = False
    X2.kind = state_kind

    X2.populate_ensemble(prior_source, prior_cfg)

    np.testing.assert_equal(X2.ens, X.ens)


def test_prior_use_full_prior():
    cfg_obj = cfg.Config()
    prior_cfg = cfg_obj.prior
    prior_cfg.seed = None
    prior_source = '20cr'
    datadir_prior = 'data'
    datafile_prior = '[vardef_template]_gridded_dat.nc'
    state_variables = ['air']
    state_kind = 'anom'

    X = LMR_prior.prior_assignment(prior_source)

    X.prior_datadir = datadir_prior
    X.prior_datafile = datafile_prior
    X.statevars = state_variables
    X.Nens = None
    X.detrend = False
    X.kind = state_kind

    X.populate_ensemble(prior_source, prior_cfg)

    X2 = LMR_prior.prior_assignment(prior_source)
    X2.prior_datadir = datadir_prior
    X2.prior_datafile = datafile_prior
    X2.statevars = state_variables
    X2.Nens = None
    X2.detrend = False
    X2.kind = state_kind

    X2.read_prior()

    # Transform full prior into ensemble-like shape
    prior_vals = X2.prior_dict['air']['value']
    prior_vals = prior_vals.reshape(prior_vals.shape[0], -1)
    prior_vals = prior_vals.T

    np.testing.assert_equal(X.ens, prior_vals)



