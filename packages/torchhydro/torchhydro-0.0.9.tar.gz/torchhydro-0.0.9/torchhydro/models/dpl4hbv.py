from typing import Union

import torch
import numpy as np
from torch import nn

from torchhydro.models.ann import SimpleAnn
from torchhydro.models.dpl4xaj import ann_pbm, lstm_pbm, SimpleLSTM
from torchhydro.models.kernel_conv import uh_conv, uh_gamma

class Hbv4Dpl(torch.nn.Module):
    """HBV Model Pytorch version"""

    def __init__(self, warmup_length, kernel_size=15):
        """Initiate a HBV instance

        Parameters
        ----------
        warmup_length : _type_
            _description_
        kernel_size : int, optional
            conv kernel for unit hydrograph, by default 15
        """
        super(Hbv4Dpl, self).__init__()
        self.name = "HBV"
        self.params_names = [
            "BETA",
            "FC",
            "K0",
            "K1",
            "K2",
            "LP",
            "PERC",
            "UZL",
            "TT",
            "CFMAX",
            "CFR",
            "CWH",
            "A",
            "THETA",
        ]
        self.warmup_length = warmup_length
        self.kernel_size = kernel_size
        # there are 3 input vars in HBV: P, PET and TEMPERATURE
        self.feature_size = 3

    def forward(
        self, x, parameters, out_state=False, rout_opt=True
    ) -> Union[tuple, torch.Tensor]:
        """
        Runs the HBV-light hydrological model (Seibert, 2005).

        The code comes from mhpi/hydro-dev.
        NaN values have to be removed from the inputs.

        Parameters
        ----------
        x
            p_all = array with daily values of precipitation (mm/d)
            pet_all = array with daily values of potential evapotranspiration (mm/d)
            t_all = array with daily values of air temperature (deg C)
        parameters
            array with parameter values having the following structure and scales
            BETA[1,6]: parameter in soil routine
            FC[50,1000]: maximum soil moisture content
            K0[0.05,0.9]: recession coefficient
            K1[0.01,0.5]: recession coefficient
            K2[0.001,0.2]: recession coefficient
            LP[0.2,1]: limit for potential evapotranspiration
            PERC[0,10]: percolation from upper to lower response box
            UZL[0,100]
            TT[-2.5,2.5]: temperature limit for snow/rain; distinguish rainfall from snowfall
            CFMAX[0.5,10]: degree day factor; used for melting calculation
            CFR[0,0.1]: refreezing factor
            CWH[0,0.2]:
        out_state
            if True, the state variables' value will be output
        rout_opt
            if True, route module will be performed

        Returns
        -------
        Union[tuple, torch.Tensor]
            q_sim = daily values of simulated streamflow (mm)
            sm = soil storage (mm)
            suz = upper zone storage (mm)
            slz = lower zone storage (mm)
            snowpack = snow depth (mm)
            et_act = actual evaporation (mm)
        """
        hbv_device = x.device
        precision = 1e-5
        buffer_time = self.warmup_length
        # Initialization
        if buffer_time > 0:
            with torch.no_grad():
                x_init = x[0:buffer_time, :, :]
                warmup_length = 0
                init_model = Hbv4Dpl(warmup_length)
                if init_model.warmup_length > 0:
                    raise RuntimeError(
                        "Please set warmup_length as 0 when initializing HBV model"
                    )
                _, snowpack, meltwater, sm, suz, slz = init_model(
                    x_init, parameters, out_state=True, rout_opt=False
                )
        else:

            # Without buff time, initialize state variables with zeros
            n_grid = x.shape[1]
            snowpack = (torch.zeros(n_grid, dtype=torch.float32) + 0.001).to(hbv_device)
            meltwater = (torch.zeros(n_grid, dtype=torch.float32) + 0.001).to(
                hbv_device
            )
            sm = (torch.zeros(n_grid, dtype=torch.float32) + 0.001).to(hbv_device)
            suz = (torch.zeros(n_grid, dtype=torch.float32) + 0.001).to(hbv_device)
            slz = (torch.zeros(n_grid, dtype=torch.float32) + 0.001).to(hbv_device)

        # the sequence must be p, pet and t
        p_all = x[buffer_time:, :, 0]
        pet_all = x[buffer_time:, :, 1]
        t_all = x[buffer_time:, :, 2]

        # scale the parameters
        parasca_lst = [
            [1, 6],
            [50, 1000],
            [0.05, 0.9],
            [0.01, 0.5],
            [0.001, 0.2],
            [0.2, 1],
            [0, 10],
            [0, 100],
            [-2.5, 2.5],
            [0.5, 10],
            [0, 0.1],
            [0, 0.2],
            [0, 2.9],
            [0, 6.5],
        ]

        par_beta = parasca_lst[0][0] + parameters[:, 0] * (
            parasca_lst[0][1] - parasca_lst[0][0]
        )
        # parCET = parameters[:,1]
        par_fc = parasca_lst[1][0] + parameters[:, 1] * (
            parasca_lst[1][1] - parasca_lst[1][0]
        )
        par_k0 = parasca_lst[2][0] + parameters[:, 2] * (
            parasca_lst[2][1] - parasca_lst[2][0]
        )
        par_k1 = parasca_lst[3][0] + parameters[:, 3] * (
            parasca_lst[3][1] - parasca_lst[3][0]
        )
        par_k2 = parasca_lst[4][0] + parameters[:, 4] * (
            parasca_lst[4][1] - parasca_lst[4][0]
        )
        par_lp = parasca_lst[5][0] + parameters[:, 5] * (
            parasca_lst[5][1] - parasca_lst[5][0]
        )
        # parMAXBAS = parameters[:,7]
        par_perc = parasca_lst[6][0] + parameters[:, 6] * (
            parasca_lst[6][1] - parasca_lst[6][0]
        )
        par_uzl = parasca_lst[7][0] + parameters[:, 7] * (
            parasca_lst[7][1] - parasca_lst[7][0]
        )
        # parPCORR = parameters[:,10]
        par_tt = parasca_lst[8][0] + parameters[:, 8] * (
            parasca_lst[8][1] - parasca_lst[8][0]
        )
        par_cfmax = parasca_lst[9][0] + parameters[:, 9] * (
            parasca_lst[9][1] - parasca_lst[9][0]
        )
        # parSFCF = parameters[:,13]
        par_cfr = parasca_lst[10][0] + parameters[:, 10] * (
            parasca_lst[10][1] - parasca_lst[10][0]
        )
        par_cwh = parasca_lst[11][0] + parameters[:, 11] * (
            parasca_lst[11][1] - parasca_lst[11][0]
        )

        n_step, n_grid = p_all.size()
        # Apply correction factor to precipitation
        # p_all = parPCORR.repeat(n_step, 1) * p_all

        # Initialize time series of model variables
        q_sim = (torch.zeros(p_all.size(), dtype=torch.float32) + 0.001).to(hbv_device)
        # # Debug for the state variables
        # SMlog = np.zeros(p_all.size())
        log_sm = np.zeros(p_all.size())
        log_ps = np.zeros(p_all.size())
        log_swet = np.zeros(p_all.size())
        log_re = np.zeros(p_all.size())

        for i in range(n_step):
            # Separate precipitation into liquid and solid components
            precip = p_all[i, :]
            tempre = t_all[i, :]
            potent = pet_all[i, :]
            rain = torch.mul(precip, (tempre >= par_tt).type(torch.float32))
            snow = torch.mul(precip, (tempre < par_tt).type(torch.float32))
            # snow = snow * parSFCF

            # Snow
            snowpack = snowpack + snow
            melt = par_cfmax * (tempre - par_tt)
            # melt[melt < 0.0] = 0.0
            melt = torch.clamp(melt, min=0.0)
            # melt[melt > snowpack] = snowpack[melt > snowpack]
            melt = torch.min(melt, snowpack)
            meltwater = meltwater + melt
            snowpack = snowpack - melt
            refreezing = par_cfr * par_cfmax * (par_tt - tempre)
            # refreezing[refreezing < 0.0] = 0.0
            # refreezing[refreezing > meltwater] = meltwater[refreezing > meltwater]
            refreezing = torch.clamp(refreezing, min=0.0)
            refreezing = torch.min(refreezing, meltwater)
            snowpack = snowpack + refreezing
            meltwater = meltwater - refreezing
            to_soil = meltwater - (par_cwh * snowpack)
            # to_soil[to_soil < 0.0] = 0.0
            to_soil = torch.clamp(to_soil, min=0.0)
            meltwater = meltwater - to_soil

            # Soil and evaporation
            soil_wetness = (sm / par_fc) ** par_beta
            # soil_wetness[soil_wetness < 0.0] = 0.0
            # soil_wetness[soil_wetness > 1.0] = 1.0
            soil_wetness = torch.clamp(soil_wetness, min=0.0, max=1.0)
            recharge = (rain + to_soil) * soil_wetness

            # log for displaying
            log_sm[i, :] = sm.detach().cpu().numpy()
            log_ps[i, :] = (rain + to_soil).detach().cpu().numpy()
            log_swet[i, :] = (sm / par_fc).detach().cpu().numpy()
            log_re[i, :] = recharge.detach().cpu().numpy()

            sm = sm + rain + to_soil - recharge
            excess = sm - par_fc
            # excess[excess < 0.0] = 0.0
            excess = torch.clamp(excess, min=0.0)
            sm = sm - excess
            evap_factor = sm / (par_lp * par_fc)
            # evap_factor[evap_factor < 0.0] = 0.0
            # evap_factor[evap_factor > 1.0] = 1.0
            evap_factor = torch.clamp(evap_factor, min=0.0, max=1.0)
            et_act = potent * evap_factor
            et_act = torch.min(sm, et_act)
            sm = torch.clamp(
                sm - et_act, min=precision
            )  # sm can not be zero for gradient tracking

            # Groundwater boxes
            suz = suz + recharge + excess
            perc = torch.min(suz, par_perc)
            suz = suz - perc
            q0 = par_k0 * torch.clamp(suz - par_uzl, min=0.0)
            suz = suz - q0
            q1 = par_k1 * suz
            suz = suz - q1
            slz = slz + perc
            q2 = par_k2 * slz
            slz = slz - q2
            q_sim[i, :] = q0 + q1 + q2

            # # for debug state variables
            # SMlog[t,:] = sm.detach().cpu().numpy()

        if rout_opt is True:  # routing
            temp_a = parasca_lst[-2][0] + parameters[:, -2] * (
                parasca_lst[-2][1] - parasca_lst[-2][0]
            )
            temp_b = parasca_lst[-1][0] + parameters[:, -1] * (
                parasca_lst[-1][1] - parasca_lst[-1][0]
            )
            rout_a = temp_a.repeat(n_step, 1).unsqueeze(-1)
            rout_b = temp_b.repeat(n_step, 1).unsqueeze(-1)
            uh_from_gamma = uh_gamma(rout_a, rout_b, len_uh=self.kernel_size)
            rf = torch.unsqueeze(q_sim, -1)
            qs = uh_conv(rf, uh_from_gamma)

        else:
            qs = torch.unsqueeze(q_sim, -1)  # add a dimension
        return (qs, snowpack, meltwater, sm, suz, slz) if out_state is True else qs


class DplLstmHbv(nn.Module):
    def __init__(
        self,
        n_input_features,
        n_output_features,
        n_hidden_states,
        warmup_length,
        param_limit_func="sigmoid",
        param_test_way="final",
    ):
        """
        Differential Parameter learning model: LSTM -> Param -> XAJ

        The principle can be seen here: https://doi.org/10.1038/s41467-021-26107-z

        Parameters
        ----------
        n_input_features
            the number of input features of LSTM
        n_output_features
            the number of output features of LSTM, and it should be equal to the number of learning parameters in XAJ
        n_hidden_states
            the number of hidden features of LSTM
        warmup_length
            the time length of warmup period
        param_limit_func
            function used to limit the range of params; now it is sigmoid or clamp function
        param_test_way
            how we use parameters from dl model when testing;
            now we have three ways:
            1. "final" -- use the final period's parameter for each period
            2. "mean_time" -- Mean values of all periods' parameters is used
            3. "mean_basin" -- Mean values of all basins' final periods' parameters is used
        """
        super(DplLstmHbv, self).__init__()
        self.dl_model = SimpleLSTM(
            n_input_features, n_output_features, n_hidden_states
        )
        self.pb_model = Hbv4Dpl(warmup_length)
        self.param_func = param_limit_func
        self.param_test_way = param_test_way

    def forward(self, x, z):
        """
        Differential parameter learning

        z (normalized input) -> lstm -> param -> + x (not normalized) -> xaj -> q
        Parameters will be denormalized in xaj model

        Parameters
        ----------
        x
            not normalized data used for physical model; a sequence-first 3-dim tensor. [sequence, batch, feature]
        z
            normalized data used for DL model; a sequence-first 3-dim tensor. [sequence, batch, feature]

        Returns
        -------
        torch.Tensor
            one time forward result
        """
        return lstm_pbm(self.dl_model, self.pb_model, self.param_func, x, z)


class DplAnnHbv(nn.Module):
    def __init__(
        self,
        n_input_features: int,
        n_output_features: int,
        n_hidden_states: Union[int, tuple, list],
        warmup_length: int,
        param_limit_func="sigmoid",
        param_test_way="final",
    ):
        """
        Differential Parameter learning model only with attributes as DL model's input: ANN -> Param -> Gr4j

        The principle can be seen here: https://doi.org/10.1038/s41467-021-26107-z

        Parameters
        ----------
        n_input_features
            the number of input features of ANN
        n_output_features
            the number of output features of ANN, and it should be equal to the number of learning parameters in XAJ
        n_hidden_states
            the number of hidden features of ANN; it could be Union[int, tuple, list]
        warmup_length
            the length of warmup periods;
            hydrologic models need a warmup period to generate reasonable initial state values
        param_limit_func
            function used to limit the range of params; now it is sigmoid or clamp function
        param_test_way
            how we use parameters from dl model when testing;
            now we have three ways:
            1. "final" -- use the final period's parameter for each period
            2. "mean_time" -- Mean values of all periods' parameters is used
            3. "mean_basin" -- Mean values of all basins' final periods' parameters is used
        """
        super(DplAnnHbv, self).__init__()
        self.dl_model = SimpleAnn(n_input_features, n_output_features, n_hidden_states)
        self.pb_model = Hbv4Dpl(warmup_length)
        self.param_func = param_limit_func
        self.param_test_way = param_test_way

    def forward(self, x, z):
        """
        Differential parameter learning

        z (normalized input) -> ANN -> param -> + x (not normalized) -> gr4j -> q
        Parameters will be denormalized in gr4j model

        Parameters
        ----------
        x
            not normalized data used for physical model; a sequence-first 3-dim tensor. [sequence, batch, feature]
        z
            normalized data used for DL model; a 2-dim tensor. [batch, feature]

        Returns
        -------
        torch.Tensor
            one time forward result
        """
        return ann_pbm(self.dl_model, self.pb_model, self.param_func, x, z)
