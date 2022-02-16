from iapws.humidAir import *
from iapws import *
from math import *

'''
mfr = mass flow rate
HR = humidity ratio
RH = relative humidity
MR = mass flow rate ratio = m_sw/m_a
h = specific enthalpy
H = enthalpy per second [kJ/s]
wb = wet bulb temperture

'''

class desalintaion():
    def __init__(self,parameter):
        T_A1 = parameter['Ta1'] # in [K]
        T_A2 = parameter['Ta2'] # in [K]
        
        T_SW1=parameter['Tsw1'] # in [K]
        T_SW2=parameter['Tsw2'] # in [K]

        P = parameter['P'] # in [MPa]

        HR_ideal = parameter['hr_ideal'] # humidity ratio for ideal situation, in float
        HR_h = parameter['hr_h'] 
        HR_dh=parameter['hr_dh']

        S = parameter['S'] # salinity of water, in [kg/kg]

        MFR_RATIO = parameter['MR']
        MFR_SW= parameter['mfr_sw']
        MFR_A = MFR_SW/MFR_RATIO

        EFF_h=parameter['eff_h'] # effectiveness of humidifier
        EFF_dh=parameter['eff_dh'] # effectiveness of dehumidfier

        T_A1_ideal = T_SW1 # In ideal, temp of air equal to seawater
        T_A2_ideal = T_SW2
        h_a1 = self.ha_enthalpy(T = T_A1, P =P, HR = HR_dh)
        h_a2 = self.ha_enthalpy(T = T_A2, P =P, HR = HR_h)
        wb1 = self.wetbulb_temp(T = T_A1, P =P, HR = HR_dh)
        wb2 = self.wetbulb_temp(T = T_A2, P =P, HR = HR_h)
        h_a1_ideal = self.ha_enthalpy(T = T_A1_ideal, P =P, HR = HR_ideal)
        h_a2_ideal = self.ha_enthalpy(T = T_A2_ideal, P =P, HR = HR_ideal)

        hsw1 = self.sw_enthalpy(T = T_SW1, P = P, S = S)
        hsw2 = self.sw_enthalpy(T = T_SW2, P = P, S = S)
        hsw1_ideal = self.sw_enthalpy(T = wb1, P = P, S = S)
        hsw2_ideal = self.sw_enthalpy(T = wb2, P = P, S = S)

        MFR_FW = MFR_A * (HR_h-HR_dh) # Based on equation (3)
        MFR_BRINE = MFR_SW - MFR_FW # Based on equation (2) or (6)

        T_FW = (T_A1+T_A2)/2 # The temperture of frewater equal to the average value of air's temperture
        hfw = self.sw_enthalpy(T = T_FW, P = P, S = 0.000000001) # For freshwater, take thesalinity as 0.000 000 001 kg/kg, so that the difference between real frewater can be negligible
        
        max_Hsw_dh = MFR_SW*(hsw2_ideal - hsw1)
        max_Ha_dh = MFR_A*(h_a2 - h_a1_ideal)

        if max_Ha_dh > max_Hsw_dh: # compare the maximum enthalpy to get the minimum heat cap 
            hsw3 = (EFF_dh*max_Hsw_dh) + hsw1 # Definition of effectiveness E = max_Hsw_dh*(hsw3-hsw1)
            # energy balance between air and water: mfr_a * (ha2 - ha1) = mfr_sw * (hsw3 - hsw1) -mfr_fw * hfw
            ha1 = h_a2 - ((MFR_SW*(hsw3 - hsw1) + MFR_FW*hfw )/ MFR_A)




    def ha_enthalpy(self, T, P, HR):
        A = 1/(1+HR) # Mass fraction of water in humid air, m of water / (m of water + m of air)
        moist = HumidAir(T = T, P = P, A = A)
        h = moist.h
        return h

    def sw_enthalpy(self, T, P, S):
        seawater = SeaWater(T = T, P = P, S = S)
        h = seawater.h
        return h

    def wetbulb_temp(self, T, P, HR):
        A = 1/(1+HR)# Mass fraction of water in humid air
        moist = HumidAir(T = T, P = P, A = A)
        rh = moist.RH * 100
        wbt = T *  atan(0.151977*((rh+8.313659)**(1/2))) + atan(T + rh) - atan(rh - 1.676331) + 0.00391838*((rh)**(3/2)) * atan(0.0231013*rh) - 4.686035 # Wet-bulb temp of humid air ; Based on the Stull formula ; in radians
        # Wet-Bulb Temperature from Relative Humidity and Air Temperature
        return wbt

Ta1 = 300
Ta2 = 275
Tsw1 = 300
Tsw2 = 300
P = 0.101325
hr_ideal = 1
hr_dh = 0.5
hr_h = 0.5 
MR = 0.5
mfr_sw = 0.05 # kg/s; Based on the work of pump 
S = 0.035 # kg/kg
eff_h = 0.8
eff_dh = 0.8
param = {   
            'Ta1':Ta1,
            'Ta2':Ta2,
            'Tsw1':Tsw1,
            'Tsw2':Tsw2,
            'P':P,
            'S':S,
            'hr_ideal':hr_ideal,
            'hr_dh':hr_dh,
            'hr_h':hr_h,
            'MR':MR,
            'mfr_sw':mfr_sw,
            'eff_h':eff_h,
            'eff_dh':eff_dh
        }
desalination_param = desalintaion(parameter = param)
    hi
