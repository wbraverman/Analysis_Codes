import numpy as np
import csv as csv
import matplotlib.pyplot as plt
import os.path
import math


class Constants:

	# just a class for storing constants

	def __init__(self):
	
		self.NeMass = 19.992 # 9+
		self.HMass = 1.00728 
		self.HeMass = 4.0026
		self.FMass = 17.0021
		
		# According to https://linac96.web.cern.ch/Compendium/COMPENDI.PDF, it seems like the FWHM of the LINAC beam is 0.04%. This would be a sigma of 0.0004/2.355 = 0.00017. Meaning the beam 
		# enegy will most likely be BeamEnergy +- 0.00034*BeamEnergy (most data in a bell curve falls within 2 sigma of the average). Need to verify with Catherine.
		
		#self.BeamEnergySigma = 0.00017
    	
		self.Fernandez165RingStart = 2
		self.Fernandez165RingStop = 5
		
		self.SatPeakRingStart = 0
		self.SatPeakRingStop = 15
		
		self.NeChargeState = 9 
		
		self.ElectronCharge = 1.6*10**(-19)
		
		self.Mol = 6.0221408*10**(23)
		
		self.MethyleneMolarMass = 14.0266; #g/mol
		self.PolypropelenMolarMass = 3*self.MethyleneMolarMass;
		
		self.NeGSspin = 0;
		self.HeGSspin = 0;
		self.FGSspin = 2.5;
		self.Hspin = 0.5;
		
		# Q value for 20Ne(p,a) reaction
		self.QVal = -4.13; # MeV
		
		self.Boltzmann = 8.6173324*10**(-2) # MeV/GK
		
		self.BarnToCmSquared = 10**(-24)
		self.MilliBarnToCmSquared = 10**(-27)
		

class BeamCurrentCalc:

	# retrieve energy loss	
	def GetEnergyLoss(self, BeamEnergyInput):
	
    		
		if BeamEnergyInput == 117:
			EnergyLoss = 1.8982
		elif BeamEnergyInput == 120:
			EnergyLoss = 1.8625
		elif BeamEnergyInput == 128:
			EnergyLoss = 1.7864
		elif BeamEnergyInput == 130:
			EnergyLoss = 1.8639
		elif BeamEnergyInput == 132:
			EnergyLoss = 1.851
		elif BeamEnergyInput == 134:
			EnergyLoss = 1.8314
		elif BeamEnergyInput == 137:
			EnergyLoss = 1.8016
		elif BeamEnergyInput == 141:
			EnergyLoss = 1.5984
		elif BeamEnergyInput == 143:
			EnergyLoss = 1.5844
		elif BeamEnergyInput == 149:
			EnergyLoss = 1.5358
		elif BeamEnergyInput == 152.4:
			EnergyLoss = 1.1088
		else:
			print('No data for this energy.')
			return 0
			
		return EnergyLoss
		
	# retrieve runtimes. Need to get more accuurate runtimes from ANL computers	
	def GetRuntime(self, BeamEnergyInput):
	
		if BeamEnergyInput == 120:
			runtime = 39780;
		elif BeamEnergyInput == 128:
			runtime = 27240
		elif BeamEnergyInput == 130:
			runtime = 22560
		elif BeamEnergyInput == 132:
			runtime = 14400
		elif BeamEnergyInput == 134:
			runtime = (43+64+64+58+30+30+55)*60
		elif BeamEnergyInput == 137:
			runtime = (60+60+11+62+59+58)*60
		elif BeamEnergyInput == 141:
			runtime = (18+67+54+67+61+60+60+67+61)*60
		elif BeamEnergyInput == 143:
			runtime = (60+45)*60
		elif BeamEnergyInput == 149:
			runtime = (14+6+16+75+7+112+67+62+62+51+60+11+4+5+60)*60
		else:
			print('No data for this energy.')
			return 0
		
		return runtime
		
	# retrieve target thickness	
	def GetTargetThickness(self, BeamEnergyInput):
	
		if BeamEnergyInput == 117:
			target_thickness = 270*10**(-6)	
		elif BeamEnergyInput == 120:
			target_thickness = 270*10**(-6)
		elif BeamEnergyInput == 128:
			target_thickness = 270*10**(-6)
		elif BeamEnergyInput == 130:
			target_thickness = 285*10**(-6)
		elif BeamEnergyInput == 132:
			target_thickness = 285*10**(-6)
		elif BeamEnergyInput == 134:
			target_thickness = 285*10**(-6)
		elif BeamEnergyInput == 137:
			target_thickness = 285*10**(-6)
		elif BeamEnergyInput == 141:
			target_thickness = 258*10**(-6)
		elif BeamEnergyInput == 143:
			target_thickness = 258*10**(-6)
		elif BeamEnergyInput == 149:
			target_thickness = 258*10**(-6)
		elif BeamEnergyInput == 152.4:
			target_thickness = 189*10**(-6)
		else:
			print('No data for this energy.')
			return 0
		
		return target_thickness
			
	# normalize beam current from observed proton elastic scatters to Fernandez data
	def GetFernandezData(self, BeamEnergyInput, Diagnostic=False):
    		
		FernandezCS = []
		FernandezEnergy = []
    	
		Fernandez_data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/Fernandez_fig2.csv"

		with open(Fernandez_data) as csvfile:
			lines = csvfile.readlines()[1:];
			FernandezFig2Energy = [round((float(i.split(',', 1)[0]))/Constants().HMass, 3) for i in lines[:]];
			FernandezFig2CrossSection = [round(float(i.split(',', 2)[1]), 3) for i in lines[:]];
    		
    		
		if BeamEnergyInput == 117:
			ProtonElasticsFile = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/117MeV/PAlpha/6.942kG/Beam_Elastic_Counts_raw.csv'
			
		elif BeamEnergyInput == 120:
			ProtonElasticsFile = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/120MeV/PAlpha/7.02kG/Beam_Elastic_Counts_raw.csv'

		elif BeamEnergyInput == 128:
			ProtonElasticsFile = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/128MeV/PAlpha/7.21kG/Beam_Elastic_Counts_raw.csv'
			
		elif BeamEnergyInput == 130:
			ProtonElasticsFile = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/130MeV/PAlpha/7.250kG/Beam_Elastic_Counts_raw.csv'
			
		elif BeamEnergyInput == 132:
			ProtonElasticsFile = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/132MeV/PAlpha/7.298kG/Beam_Elastic_Counts_raw.csv'
			
		elif BeamEnergyInput == 134:
			ProtonElasticsFile = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/134MeV/PAlpha/7.35kG/Beam_Elastic_Counts_raw.csv'
			
		elif BeamEnergyInput == 137:
			ProtonElasticsFile = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/137MeV/PAlpha/7.4kG/Beam_Elastic_Counts_raw.csv'
			
		elif BeamEnergyInput == 141:
			ProtonElasticsFile = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/141MeV/PAlpha/7.51kG/Beam_Elastic_Counts_raw.csv'
			
		elif BeamEnergyInput == 143:
			ProtonElasticsFile = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/143MeV/PAlpha/7.54kG/Beam_Elastic_Counts_raw.csv'
			
		elif BeamEnergyInput == 149:
			ProtonElasticsFile = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/149MeV/PAlpha/7.69kG/Beam_Elastic_Counts_raw.csv'
			
		elif BeamEnergyInput == 152.4:
			ProtonElasticsFile = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/152.4MeV/7.6kG/Beam_Elastic_Counts_raw.csv'
			
		else:
			print('No data for this energy.')
			return 0
			
			
		with open(ProtonElasticsFile) as csvfile:
			lines = csvfile.readlines()[1:];
			GScounts = [round(float(i.split(',', 2)[1]), 0) for i in lines[Constants().Fernandez165RingStart: Constants().Fernandez165RingStop + 1]];
			GSerror = [round(float(i.split(',', 3)[2]), 0) for i in lines[Constants().Fernandez165RingStart: Constants().Fernandez165RingStop + 1]];
			EXcounts = [round(float(i.split(',', 4)[3]), 0) for i in lines[Constants().Fernandez165RingStart: Constants().Fernandez165RingStop + 1]];
			EXerror = [round(float(i.split(',', 5)[4]), 0) for i in lines[Constants().Fernandez165RingStart: Constants().Fernandez165RingStop + 1]];
			
			
		runtime = self.GetRuntime(BeamEnergyInput)
		
		target_thickness = self.GetTargetThickness(BeamEnergyInput)
			
		EnergyLoss = self.GetEnergyLoss(BeamEnergyInput)
    			
		MaxEnergy = round(BeamEnergyInput/Constants().NeMass, 3)
		MinEnergy = round((BeamEnergyInput - EnergyLoss) / Constants().NeMass, 3)
    		
		for i in range(len(FernandezFig2Energy)):
			if FernandezFig2Energy[i] <= MaxEnergy and FernandezFig2Energy[i] >= MinEnergy:
				FernandezEnergy.append(FernandezFig2Energy[i])
				FernandezCS.append(FernandezFig2CrossSection[i])
    	
		
		CManglesElastic = [169.936, 168.678, 167.42, 166.162, 164.904, 163.646, 162.388, 161.131, 159.873, 158.616, 157.358, 156.101, 154.843, 153.586, 152.329, 151.072, 149.815]
		# For simplicity sake I am just assuming CoM angles stay constant across all energies. It's not a bad assumption, at the worst they should only be a couple tenths of a degree off.
		
		CManglesElastic = np.array(CManglesElastic)
		CManglesElastic = CManglesElastic*(np.pi/180)
		
		Domega = round(2*np.pi*(np.cos(CManglesElastic[Constants().Fernandez165RingStop + 1]) - np.cos(CManglesElastic[Constants().Fernandez165RingStart])), 3)
		
		CurrentTargetTime = [sum(GScounts) / (FernandezCS[i] * Domega) for i in range(len(FernandezCS))]
		CurrentTargetTime = np.array(CurrentTargetTime)
		
		AverageCurrentTargetTime = sum(CurrentTargetTime) / len(CurrentTargetTime)
						
		CurrentTargetTimeError = [sum(GSerror) / (FernandezCS[i] * Domega) for i in range(len(FernandezCS))]
		CurrentTargetTimeError = np.array(CurrentTargetTimeError)
		
		
		AverageCurrentTargetTimeError = sum(CurrentTargetTimeError) / len(CurrentTargetTimeError)
		
		HydrogenAtoms = round((target_thickness/Constants().MethyleneMolarMass)*Constants().Mol*2, 3)
				
		AverageBeamCurrent = round((AverageCurrentTargetTime / (runtime*HydrogenAtoms*Constants().MilliBarnToCmSquared))*(Constants().NeChargeState*Constants().ElectronCharge*10**12), 2)
		AverageBeamCurrentError = round((AverageCurrentTargetTimeError /(runtime*HydrogenAtoms*Constants().MilliBarnToCmSquared))*(Constants().NeChargeState*Constants().ElectronCharge*10**12), 2)
		
		if Diagnostic:
		
			print('Beam Energy: ', BeamEnergyInput, ' MeV')
			print('Max Energy: ', MaxEnergy, ' MeV/u')
			print('Min Energy: ', MinEnergy, ' MeV/u')
			print('Runtime: ', runtime, ' seconds')
			print('Hydrogen Atoms: ', HydrogenAtoms)
			print('Solid Angle: ', Domega, ' str')
			print('Neon Charge State: ', Constants().NeChargeState)
			print('Neon Mass: ', Constants().NeMass, ' Daltons')
			print('Hydrogen Mass: ', Constants().HMass, ' Daltons')
			print('Average Beam Current: ', AverageBeamCurrent, ' epA')
			print('Avegage Beam Current Error: ', AverageBeamCurrentError, ' epa')
			print('Fernandez Energies (MeV/u): ')
			
			for i in range(len(FernandezEnergy)):
				print(FernandezEnergy[i])
			
			print('Fernandez Cross Section (mB/str): ')	
			
			for i in range(len(FernandezCS)):
				print(FernandezCS[i])
			
					  		
		return AverageCurrentTargetTime, AverageCurrentTargetTimeError
		
	
	
	
	# calculate efficiency of detection from Monte Carlo results
	def SingleRingEff(self, BeamEnergy, RingStart, RingStop, ExcitedState = False, PrintEff = False, RingByRing = False):
	
		if BeamEnergy == 128:
			FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_128MeV.dat'
		elif BeamEnergy == 130:
			FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_130MeV.dat'
		elif BeamEnergy == 132:
			FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_132MeV.dat'
		elif BeamEnergy == 134:
			FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_134MeV.dat'
		elif BeamEnergy == 137:
			FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_137MeV.dat'
		elif BeamEnergy == 141:
		
			if ExcitedState:
				FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_141MeV_1st.dat'
			else:
				FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_141MeV.dat'
				
		elif BeamEnergy == 143:
		
			if ExcitedState:
				FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_143MeV_1st.dat'
			else:
				FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_143MeV.dat'
				
		elif BeamEnergy == 149:
			
			if ExcitedState:
				FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_149MeV_1st.dat'
			else:
				FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_149MeV.dat'
				
		elif BeamEnergy == 152.4:
		
			if ExcitedState:
				FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_152MeV_1st.dat'
			else:
				FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/efficiencies/20Ne_outputs/20Ne_152MeV.dat'
				
		else:
			print('No data for this energy.')
			return 0
			
		
		DataFile = open(FilePath)

		lines = DataFile.readlines()[0:]

		DataFile.close()	
		
		
		Ring = RingStart + 1 # The MC file labels the rings 1 thru 16 rather than 0 thru 15
		
		RingEfficiencies = []
		RingEventsList = []
		RingHitsList = []
		
		
		while Ring <= RingStop + 1:
	
			RingHits = 0
			RingEvents = 0
			NumReactions= 0
	
			for line in lines:
		
				newline = line.split();
				NumReactions += 1
		
				if newline[3] == str(2) and newline[8] == str(0):
					if newline[9] == str(Ring):
						RingEvents += 1;
	
	
			RingEventsList.append(RingEvents)
			RingEfficiencies.append((float(RingEvents/NumReactions)))
	
			Ring+=1
			
			
		if PrintEff:
			for i in range(len(RingEfficiencies)):
				print('Ring ', i, ' efficiency: ', RingEfficiencies[i])	
				
		if RingByRing:
			
			return RingEfficiencies
		
		else:
				
			SubRingEff = sum(RingEfficiencies)
		
			return SubRingEff
			
	# retreive center of mass angles for each ring
	def GetCMAngles(self, BeamEnergy):
	
	
		if BeamEnergy == 128:
			CMAngles = [155.571, 152.408, 149.202, 145.944, 142.628, 139.241, 135.771, 132.202, 128.515, 124.682, 120.669, 116.426, 111.878, 106.903, 101.279, 94.496, 84.534]
			CMAngles = np.array(CMAngles)
			CMAngles = CMAngles*(np.pi/180)
		elif BeamEnergy == 130:
			CMAngles = [155.884, 152.765, 149.606, 146.399, 143.136, 139.807, 136.4, 132.902, 129.294, 125.552, 121.647, 117.535, 113.152, 108.402, 103.114, 96.934, 88.833]
			CMAngles = np.array(CMAngles)
			CMAngles = CMAngles*(np.pi/180)
		elif BeamEnergy == 132:
			CMAngles = [156.179, 153.102, 149.987, 146.827, 143.614, 140.34, 136.992, 133.559, 130.024, 126.365, 122.557, 118.561, 114.324, 109.766, 104.75, 99.021, 91.945]
			CMAngles = np.array(CMAngles)
			CMAngles = CMAngles*(np.pi/180)
		elif BeamEnergy == 134:
			CMAngles = [156.453, 153.415, 150.341, 147.224, 144.057, 140.832, 137.538, 134.164, 130.695, 127.111, 123.39, 119.496, 115.386, 110.99, 106.198, 100.814, 94.407]
			CMAngles = np.array(CMAngles)
			CMAngles = CMAngles*(np.pi/180)
		elif BeamEnergy == 137:
			CMAngles = [156.828, 153.844, 150.825, 147.767, 144.662, 141.504, 138.282, 134.987, 131.606, 128.121, 124.513, 120.752, 116.803, 112.609, 108.087, 103.098, 97.366]
			CMAngles = np.array(CMAngles)
			CMAngles = CMAngles*(np.pi/180)
		elif BeamEnergy == 141:
			CMAngles = [157.28, 154.359, 151.407, 148.418, 145.388, 142.308, 139.172, 135.97, 132.69, 129.32, 125.84, 122.23, 118.458, 114.483, 110.243, 105.64, 100.506]
			CMAngles = np.array(CMAngles)
			CMAngles = CMAngles*(np.pi/180)
		elif BeamEnergy == 143:
			CMAngles = [157.48, 154.588, 151.665, 148.707, 145.709, 142.664, 139.565, 136.403, 133.167, 129.845, 126.421, 122.874, 119.176, 115.29, 110.301, 106.709, 101.791]
			CMAngles = np.array(CMAngles)
			CMAngles = CMAngles*(np.pi/180)
		elif BeamEnergy == 149:
			CMAngles = [158.013, 155.195, 152.349, 149.472, 146.559, 143.605, 140.603, 137.545, 134.423, 131.227, 127.943, 124.555, 121.042, 117.375, 113.517, 109.41, 104.966]
			CMAngles = np.array(CMAngles)
			CMAngles = CMAngles*(np.pi/180)
		elif BeamEnergy == 152.4:
			CMAngles = [158.292, 155.512, 152.706, 149.871, 147.002, 144.094, 141.142, 138.137, 135.073, 131.94, 128.726, 125.417, 121.994, 118.432, 114.7, 110.75, 106.512]
			CMAngles = np.array(CMAngles)
			CMAngles = CMAngles*(np.pi/180)
		else:
			print('No data for this energy')
			return 0
			
		
		MidpointAngles = [(CMAngles[i] + CMAngles[i+1])/2 for i in range(len(CMAngles)-1)]
		MidpointAngles = np.array(MidpointAngles)
		
		return CMAngles, MidpointAngles
	
	
	
	# calculate solid angle of individual rings or group of them in center of mass frame
	def SolidAngleCalc(self, BeamEnergy, StartRing, StopRing, ExState = False, RingByRing = False):
		
		if ExState:
		
			if BeamEnergy == 141:
				CMAngles = [155.232, 152.02, 148.762, 145.45, 142.075, 138.625, 135.085, 131.438, 127.662, 123.727, 119.593, 115.199, 110.457, 105.211, 99.157, 91.487]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			elif BeamEnergy == 143:
				CMAngles = [155.542, 152.375, 149.164, 145.903, 142.581, 139.189, 135.714, 132.139, 128.445, 124.605, 120.583, 116.328, 111.766, 106.773, 101.121, 94.283, 84.106]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			elif BeamEnergy == 149:
				CMAngles = [156.348, 153.296, 150.207, 147.073, 143.889, 140.645, 137.332, 133.936, 130.442, 126.831, 123.078, 119.147, 114.991, 110.537, 105.667, 100.164, 93.535]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			elif BeamEnergy == 152.4:
				CMAngles = [156.759, 153.765, 150.736, 147.667, 144.551, 141.381, 138.146, 134.838, 131.441, 127.939, 124.311, 120.528, 116.551, 112.324, 107.758, 102.706, 96.872]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			else:
				print('No data for this energy.')
				return 0
		
		else:
			if BeamEnergy == 128:
				CMAngles = [155.571, 152.408, 149.202, 145.944, 142.628, 139.241, 135.771, 132.202, 128.515, 124.682, 120.669, 116.426, 111.878, 106.903, 101.279, 94.496, 84.534]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			elif BeamEnergy == 130:
				CMAngles = [155.884, 152.765, 149.606, 146.399, 143.136, 139.807, 136.4, 132.902, 129.294, 125.552, 121.647, 117.535, 113.152, 108.402, 103.114, 96.934, 88.833]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			elif BeamEnergy == 132:
				CMAngles = [156.179, 153.102, 149.987, 146.827, 143.614, 140.34, 136.992, 133.559, 130.024, 126.365, 122.557, 118.561, 114.324, 109.766, 104.75, 99.021, 91.945]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			elif BeamEnergy == 134:
				CMAngles = [156.453, 153.415, 150.341, 147.224, 144.057, 140.832, 137.538, 134.164, 130.695, 127.111, 123.39, 119.496, 115.386, 110.99, 106.198, 100.814, 94.407]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			elif BeamEnergy == 137:
				CMAngles = [156.828, 153.844, 150.825, 147.767, 144.662, 141.504, 138.282, 134.987, 131.606, 128.121, 124.513, 120.752, 116.803, 112.609, 108.087, 103.098, 97.366]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			elif BeamEnergy == 141:
				CMAngles = [157.28, 154.359, 151.407, 148.418, 145.388, 142.308, 139.172, 135.97, 132.69, 129.32, 125.84, 122.23, 118.458, 114.483, 110.243, 105.64, 100.506]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			elif BeamEnergy == 143:
				CMAngles = [157.48, 154.588, 151.665, 148.707, 145.709, 142.664, 139.565, 136.403, 133.167, 129.845, 126.421, 122.874, 119.176, 115.29, 110.301, 106.709, 101.791]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			elif BeamEnergy == 149:
				CMAngles = [158.013, 155.195, 152.349, 149.472, 146.559, 143.605, 140.603, 137.545, 134.423, 131.227, 127.943, 124.555, 121.042, 117.375, 113.517, 109.41, 104.966]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			elif BeamEnergy == 152.4:
			        #                   0        1        2        3        4        5        6        7        8       9        10       11       12       13     14     15
				CMAngles = [158.292, 155.512, 152.706, 149.871, 147.002, 144.094, 141.142, 138.137, 135.073, 131.94, 128.726, 125.417, 121.994, 118.432, 114.7, 110.75, 106.512]
				CMAngles = np.array(CMAngles)
				CMAngles = CMAngles*(np.pi/180)
			else:
				print('No data for this energy')
				return 0
		
		
		
		if RingByRing:
		
			CMAnglesTheta = CMAngles*(180/np.pi)
			
			# Still doing calculations in radians
			SolidAngleList = [round(2*np.pi*(np.cos(CMAngles[i+1]) - np.cos(CMAngles[i])), 3) for i in range(StartRing, StopRing + 1) if i != 11 ]
			
			# but printing midpoint angles in degrees
			MidAngle = [round((CMAnglesTheta[i+1] + CMAnglesTheta[i])/2, 2) for i in range(StartRing, StopRing + 1) if i != 11 ]
			
			return SolidAngleList, MidAngle
		else:
		
			SolidAngle = round(2*np.pi*(np.cos(CMAngles[StopRing+1]) - np.cos(CMAngles[StartRing])), 3)
			
			if StopRing >= 11:
				
				ring11 = round(2*np.pi*(np.cos(CMAngles[12]) - np.cos(CMAngles[11])), 3)
				
				SolidAngle = SolidAngle - ring11
			
			
			MidAngle = [round((CMAngles[i+1] + CMAngles[i])/2, 2) for i in range(StartRing, StopRing + 1) if i != 11 ]
		
			print(SolidAngle)
		
			return SolidAngle
		
	
	# calculate solid angle in lab frame
	def GetLabSolidAngle(self, StartRing, StopRing, RingByRing = False):
		
		LabAnglesRad = [(5 + 0.625*i) * (np.pi/180) for i in range(0, 17)]
		
		LabAnglesDeg = [(5 + 0.625*i) for i in range(0, 17)]
		
		if RingByRing:
		
			SolidAngleList = [abs(round(2*np.pi*(np.cos(LabAnglesRad[i+1]) - np.cos(LabAnglesRad[i])), 3)) for i in range(StartRing, StopRing + 1)]
			
			MidAngle = [round((LabAnglesDeg[i+1] + LabAnglesDeg[i])/2, 2) for i in range(StartRing, StopRing + 1)]
			
			return SolidAngleList, MidAngle
			
		else:
		
			SolidAngle = abs(round(2*np.pi*(np.cos(LabAnglesRad[StopRing+1]) - np.cos(LabAnglesRad[StartRing])), 3))
			
			MidAngle = round((LabAnglesDeg[StopRing+1] + LabAnglesDeg[StartRing]) / 2, 3)
			
			return SolidAngle, MidAngle

				
		
	# method to get beam current of runs where proton scattering cross section is low. This method will normalize the current from other runs with appreciable proton scattering cross sections
	# where we can calculate a beam current from Fernandez data. Takes an unspecified number of other runs to scale to.	
	def GetSatPeakCounts(self, BeamEnergy, *ScaleTo, Diagnostic=False):
	
		
		if BeamEnergy == 137:
			FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/137MeV/PAlpha/7.4kG/SaturationPeakCounts.csv'
		elif BeamEnergy == 141:
			FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/141MeV/PAlpha/7.51kG/SaturationPeakCounts.csv'
		elif BeamEnergy == 143:
			FilePath = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/143MeV/PAlpha/7.54kG/SaturationPeakCounts.csv'
		else:
			print('No data for this energy.')
			return 0
			
			
		runtime = BeamCurrentCalc().GetRuntime(BeamEnergy)
		
		target_thickness = BeamCurrentCalc().GetTargetThickness(BeamEnergy)
			
		
		with open(FilePath) as csvfile:
			lines = csvfile.readlines()[1:]
			SatPeakCounts = [round(float(i.split(',', 2)[1]), 0) for i in lines[Constants().SatPeakRingStart:Constants().SatPeakRingStop+1]]
			SatPeakCountsError = [round(float(i.split(',', 3)[2]), 0) for i in lines[Constants().SatPeakRingStart:Constants().SatPeakRingStop+1]];
		
		
		
		ScaledCTTList = []
		SquaredErrorList = []
		
		for element in ScaleTo:
		
			if element == 120:
				FilePathScaleTo = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/120MeV/PAlpha/7.02kG/SaturationPeakCounts.csv'
			elif element == 128:
				FilePathScaleTo = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/128MeV/PAlpha/7.21kG/SaturationPeakCounts.csv'	
			elif element == 130:
				FilePathScaleTo = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/130MeV/PAlpha/7.250kG/SaturationPeakCounts.csv'
			elif element == 132:
				FilePathScaleTo =  r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/132MeV/PAlpha/7.298kG/SaturationPeakCounts.csv'	
			elif element == 134:
				FilePathScaleTo = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/134MeV/PAlpha/7.35kG/SaturationPeakCounts.csv'	
			elif element == 149:
				FilePathScaleTo = r'/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/149MeV/PAlpha/7.69kG/SaturationPeakCounts.csv'	
			else:
				break
				
				
			runtimeScaleTo = BeamCurrentCalc().GetRuntime(element)
			
			
			with open(FilePathScaleTo) as csvfile:
				lines = csvfile.readlines()[1:]
				SatPeakCountsScaleTo = [round(float(i.split(',', 2)[1]), 0) for i in lines[Constants().SatPeakRingStart:Constants().SatPeakRingStop+1]];
				SatPeakCountsErrorScaleTo = [round(float(i.split(',', 3)[2]), 0) for i in lines[Constants().SatPeakRingStart:Constants().SatPeakRingStop+1]];
				
				
				
			SatPeakRatio = (sum(SatPeakCounts)/runtime)/(sum(SatPeakCountsScaleTo)/runtimeScaleTo)
			
			CurrentTargetTime, CurrentTargetTimeError = self.GetFernandezData(element, Diagnostic=False)
			
			ScaledCurrentTargetTime = CurrentTargetTime*SatPeakRatio
			
			ScaledCTTList.append(ScaledCurrentTargetTime)
			
			ErrorRatio = ((sum(SatPeakCountsError)/runtime)/(sum(SatPeakCountsScaleTo)/runtimeScaleTo))**2 + ((sum(SatPeakCounts)/runtime)/((sum(SatPeakCountsScaleTo)**2) /runtimeScaleTo))**2 * sum(SatPeakCountsErrorScaleTo)**2
			
			SquareScaleToError = CurrentTargetTimeError**2 * SatPeakRatio**2 + CurrentTargetTime**2 * ErrorRatio**2
			
			SquaredErrorList.append(SquareScaleToError)
			
		AvgSatPeakCurrentTargetTime = sum(ScaledCTTList)/len(ScaledCTTList)
		
		AvgSatPeakError = np.sqrt(sum(SquaredErrorList))
			
			
			
		if Diagnostic:
			
			HydrogenAtoms = round((target_thickness/Constants().MethyleneMolarMass)*Constants().Mol*2, 3) 
			
			AvgBeamCurrent = round((AvgSatPeakCurrentTargetTime / (runtime*HydrogenAtoms*Constants().MilliBarnToCmSquared))*(Constants().NeChargeState*Constants().ElectronCharge*10**12), 2)
				
			AvgBeamCurrentError = round((AvgSatPeakError / (runtime*HydrogenAtoms*(Constants().MilliBarnToCmSquared)))*(Constants().NeChargeState*Constants().ElectronCharge*10**12), 2)
				
			print('Beam current from saturation peaks: ', AvgBeamCurrent, ' epa')
				
			print('Beam current error: ', AvgBeamCurrentError, ' epa')
				
				
			
		
		return AvgSatPeakCurrentTargetTime, AvgSatPeakError
		
		
class CSCalc:


	# method to retrieve alpha counts from any run
	def GetAlphaCounts(self, BeamEnergy, StartRing, StopRing):
		
		
		if BeamEnergy == 128:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/128MeV/PAlpha/7.21kG/PAlpha_Counts.csv"
		elif BeamEnergy == 130:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/130MeV/PAlpha/7.250kG/PAlpha_Counts.csv"
		elif BeamEnergy == 132:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/132MeV/PAlpha/7.298kG/PAlpha_Counts.csv"
		elif BeamEnergy == 134:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/134MeV/PAlpha/7.35kG/PAlpha_Counts.csv"
		elif BeamEnergy == 137:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/137MeV/PAlpha/7.4kG/PAlpha_Counts.csv"
		elif BeamEnergy == 141:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/141MeV/PAlpha/7.51kG/PAlpha_Counts.csv"
		elif BeamEnergy == 143:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/143MeV/PAlpha/7.54kG/PAlpha_Counts.csv"
		elif BeamEnergy == 149:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/149MeV/PAlpha/7.69kG/PAlpha_Counts.csv"
		elif BeamEnergy == 152.4:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/152.4MeV/7.6kG/PAlpha_Counts.csv"
		else:
			print('No data for this energy.')
			return 0
		
		
		with open(FilePath) as csvfile:
			lines = csvfile.readlines()[1:];
			ring_num = [float(i.split(',', 1)[0]) for i in lines[StartRing:StopRing+1]];
			alpha_counts = [round(float(i.split(',', 2)[1]), 0) for i in lines[StartRing:StopRing+1]];
			error = [round(float(i.split(',', 3)[2]), 0) for i in lines[StartRing:StopRing+1]];
		
		
			
		return alpha_counts, error
		
		
		
		
	# method to retrieve excited state alpha counts from different beam energy runs	
	def GetExAlphaCounts(self, BeamEnergy, StartRing, StopRing):
	
	
		if BeamEnergy == 141:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/141MeV/PAlpha/7.51kG/PAlpha_Counts.csv"
		elif BeamEnergy == 143:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/143MeV/PAlpha/7.54kG/PAlpha_Counts.csv"
		elif BeamEnergy == 149:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/149MeV/PAlpha/7.69kG/PAlpha_Counts.csv"
		elif BeamEnergy == 152.4:
			FilePath = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/152.4MeV/7.6kG/PAlpha_Counts.csv"
		else:
			print('No data for this energy.')
			return 0
		
    		
		with open(FilePath) as csvfile:
			lines = csvfile.readlines()[1:];
			ring_num = [float(i.split(',', 1)[0]) for i in lines[StartRing:StopRing+1]];
			ExAlphaCounts = [float(i.split(',', 4)[3]) for i in lines[StartRing:StopRing+1]];
			ExError = [round(float(i.split(',', 5)[4]), 0) for i in lines[StartRing:StopRing+1]];
			
		return ExAlphaCounts, ExError
		
		
		
	# Calculate differential cross section from Fernandez normalization and saturation peak normalization
	def GetDiffCS(self, BeamEnergy, StartRing, StopRing, CMFrame=True, SatPeakNorm=False):
	
	
		Alphas, AlphaError = self.GetAlphaCounts(BeamEnergy, StartRing, StopRing)
		
		RingEff = BeamCurrentCalc().SingleRingEff(BeamEnergy, StartRing, StopRing, ExcitedState = False, PrintEff = False, RingByRing = True)
		
		
		
		if SatPeakNorm:
		
			CurrentTargetTimeAvg, CurrentTargetTimeErrorAvg = BeamCurrentCalc().GetSatPeakCounts(BeamEnergy)
			
		else:
		
			CurrentTargetTimeAvg, CurrentTargetTimeErrorAvg = BeamCurrentCalc().GetFernandezData(BeamEnergy, Diagnostic=False)
			
		
		if CMFrame:
			
			SolidAngles, MidpointAngles = BeamCurrentCalc().SolidAngleCalc(BeamEnergy, StartRing, StopRing, RingByRing = True)
			
			# Calculating the solid area is not applicable in how we are calculating the differential CS. The efficiency that is being calculated is being done, in essence, corrects for 
			# the entire 4 pi unit sphere. So, we shouldn't be considering the solid angle of each ring. When we do, we essentially have some per solid angle^2 dimension. With the 
			# efficiency factor, we just need to divide by 4 pi.		
				
			DiffCS = [Alphas[i] / (CurrentTargetTimeAvg * 4 * np.pi) / RingEff[i] for i in range(len(AlphaError))] 
			
		else:
		
			SolidAngles = BeamCurrentCalc().GetLabSolidAngle(StartRing, StopRing, RingByRing = True) 
			
			DiffCS = [Alphas[i] / (CurrentTargetTimeAvg * 4 * np.pi) / RingEff[i] for i in range(len(AlphaError))] 
		
			
		return DiffCS
		
		
	# rudimentary riemann sum of differential cross sections to get total cross section	
	def GetTotalCS(self, BeamEnergy, StartRing, StopRing):
	
		if BeamEnergy == 137 or BeamEnergy == 141 or BeamEnergy == 143 or BeamEnergy == 152.4:
			
			DiffCS = self.GetDiffCS(BeamEnergy, StartRing, StopRing, CMFrame = True, SatPeakNorm=True)
			
		else:
			
			DiffCS = self.GetDiffCS(BeamEnergy, StartRing, StopRing, CMFrame = True, SatPeakNorm=False)
	

		Angles, MidPoints = BeamCurrentCalc().GetCMAngles(BeamEnergy)
		
		TotalCSList = [DiffCS[i] * np.sin(MidPoints[i]) * abs((Angles[i+1] - Angles[i])) for i in range(len(DiffCS))]
		
		TotalCS = 2*np.pi*sum(TotalCSList)
		
		return TotalCS
		
		
	# Calculate error in differential cross section from both Fernandez normalization and saturation peak normalization	
	def GetRingDiffCSError(self, BeamEnergy, StartRing, StopRing, SatPeakNorm = False):   # Error from beam current calculation and alpha diff cs calculation added in quaderature
	
	
		if SatPeakNorm:
			CurrentTargetTimeAvg, CurrentTargetTimeErrorAvg = BeamCurrentCalc().GetSatPeakCounts(BeamEnergy)
		else:
			CurrentTargetTimeAvg, CurrentTargetTimeErrorAvg = BeamCurrentCalc().GetFernandezData(BeamEnergy, Diagnostic=False)
		
		SolidAngles, MidpointAngles = BeamCurrentCalc().SolidAngleCalc(BeamEnergy, StartRing, StopRing, RingByRing = True)
		
		Alphas, AlphaError = self.GetAlphaCounts(BeamEnergy, StartRing, StopRing)
		
		RingEff = BeamCurrentCalc().SingleRingEff(BeamEnergy, StartRing, StopRing, ExcitedState = False, PrintEff = False, RingByRing = True)
		
		# Calculating the solid area is not applicable in how we are calculating the differential CS. The efficiency that is being calculated is being done, in essence, corrects for 
		# the entire 4 pi unit sphere. So, we shouldn't be considering the solid angle of each ring. When we do, we essentially have some per solid angle^2 dimension. With the 
		# efficiency factor, we just need to divide by 4 pi.
		
		
		SquaredDiffCSError = [(AlphaError[i] / (CurrentTargetTimeAvg * 4 * np.pi) / RingEff[i])**2 for i in range(len(AlphaError))]
		
		SquaredBeamCurrentError = [((Alphas[i] / ((CurrentTargetTimeAvg**2) * 4 * np.pi) / RingEff[i])**2) * CurrentTargetTimeErrorAvg**2 for i in range(len(Alphas))]
		
		TotalRingError = [np.sqrt(SquaredDiffCSError[i] + SquaredBeamCurrentError[i]) for i in range(len(SquaredDiffCSError))]
		
		
		return TotalRingError
		
	
	# Calculate rudimentary error for total cross section from differential cross section error calculations.
	def GetRingTotalCSError(self, BeamEnergy, StartRing, StopRing):
	
		
		if BeamEnergy == 137 or BeamEnergy == 141 or BeamEnergy == 143 or BeamEnergy == 152.4:
			
			DiffCSErrors = self.GetRingDiffCSError(BeamEnergy, StartRing, StopRing, SatPeakNorm = True)
			
		else:
			
			DiffCSErrors = self.GetRingDiffCSError(BeamEnergy, StartRing, StopRing, SatPeakNorm = False)
			
		
		SquaredDiffCSErrors = [DiffCSErrors[i]**2 for i in range(len(DiffCSErrors))]
		
		TotalCSError = np.sqrt(sum(SquaredDiffCSErrors))
		
		return TotalCSError
		
		
	# Method to calculate differntial cross section from predetermined beam current values. We need to approach how we calculate beam currents from Fernandez data with more scutiny, This 
	# method is a stand in until that time. Calculates cross section in mB.
	def GetDiffCSFromBC(self, BeamEnergy, StartRing, StopRing, ExState = False):
	
		if BeamEnergy == 128:
			current = 13
			current_error = 4
		elif BeamEnergy == 130:
			current = 11.5
			current_error = 2.5
		elif BeamEnergy == 132:
			current = 14 # epa
			current_error = 3.5
		elif BeamEnergy == 134:
			current = 11
			current_error = 5
		elif BeamEnergy == 137:
			current = 18.5
			current_error = 5.5
		elif BeamEnergy == 141:
			current = 14
			current_error = 5
		elif BeamEnergy == 143:
			current = 72.5
			current_error = 12.5
		elif BeamEnergy == 149:
			current = 12.5
			current_error = 2.5
		else:
			print('No data for this energy.')
			return 0
			
		
		target_thickness = BeamCurrentCalc().GetTargetThickness(BeamEnergy)
		
		runtime = BeamCurrentCalc().GetRuntime(BeamEnergy)			
		
		HydrogenAtoms = round((target_thickness/Constants().MethyleneMolarMass)*Constants().Mol*2, 3)
		
		BeamParticles = (current / (Constants().NeChargeState*Constants().ElectronCharge*10**12)) * runtime
		
		BeamParticlesError = (current_error / (Constants().NeChargeState*Constants().ElectronCharge*10**12)) * runtime
		
		if ExState:
		
			Alphas, AlphaError = self.GetExAlphaCounts(BeamEnergy, StartRing, StopRing)
			
			RingEff = BeamCurrentCalc().SingleRingEff(BeamEnergy, StartRing, StopRing, ExcitedState = True, PrintEff = True, RingByRing = True)
			
		else:
			
			Alphas, AlphaError = self.GetAlphaCounts(BeamEnergy, StartRing, StopRing)
			
			RingEff = BeamCurrentCalc().SingleRingEff(BeamEnergy, StartRing, StopRing, ExcitedState = False, PrintEff = True, RingByRing = True)
			
			
		###################################################################################
		
		
				
		
		# Calculate alpha cross section	
				
		DiffCS = [Alphas[i] / (BeamParticles * HydrogenAtoms*Constants().MilliBarnToCmSquared * 4*np.pi)/ RingEff[i]  for i in range(len(Alphas))] 
		
		###################################################################################
		
		# Calculate alpha error
		
		SquaredErrorFromAlphas = [(AlphaError[i] / (BeamParticles * HydrogenAtoms*Constants().MilliBarnToCmSquared * 4*np.pi)/ RingEff[i])**2 for i in range(len(Alphas))]
		
		SquaredCurrentError = [((Alphas[i] / ( (BeamParticles**2) * HydrogenAtoms * Constants().MilliBarnToCmSquared * 4 * np.pi) / RingEff[i])**2) * (BeamParticlesError**2) for i in range(len(Alphas))]
		
		ErrorDiffCS = [np.sqrt(SquaredErrorFromAlphas[i] + SquaredCurrentError[i]) for i in range(len(SquaredCurrentError))]
		
		# Different formulation of error to verify, they are equivalent
		#ErrorDiffCS = [DiffCS[i] * np.sqrt((AlphaError[i]/Alphas[i])**2 + (BeamParticlesError/BeamParticles)**2) for i in range(len(DiffCS))]
		
		###################################################################################
		
		return DiffCS, ErrorDiffCS
		
	
	# Calculates 20Ne(p,a) differential cross section in lab frame. Jacobians and lab angles retrieved from RELKIN.
	def GetLabDiffCS(self, BeamEnergy, StartRing, StopRing, ExState = False):
	
		if ExState:
		
			if BeamEnergy == 149:
			
				MidPointLabAngle = [149.42, 145.77, 142.11, 138.42, 134.71, 130.95, 127.14, 123.29]
				
				Jacobian = [1.4238, 1.4045, 1.3835, 1.3609, 1.3370, 1.3117, 1.2851, 1.2575]
				
			elif BeamEnergy == 143:
			
				MidPointLabAngle = [148.11, 144.31, 140.48, 136.63]
				
				Jacobian = [1.4403, 1.4182, 1.3942, 1.3686]
				
			elif BeamEnergy == 141:
			
				MidPointLabAngle = [147.61, 143.74, 139.86, 135.93, 131.98, 127.98, 123.91, 119.76, 115.51, 111.14]
				
				Jacobian = [1.4465, 1.4232, 1.3981, 1.3712, 1.3427, 1.3128, 1.2815, 1.2490, 1.2153, 1.1806]
		
		else:
		
			if BeamEnergy == 128:
		
				MidPointLabAngle = [148.17, 144.37, 140.55, 136.71, 132.82, 128.90, 124.92, 120.86]
			
				Jacobian = [1.4390, 1.4170, 1.3933, 1.3679, 1.3408, 1.3124, 1.2827, 1.2518]
			
			elif BeamEnergy == 130:
		
				MidPointLabAngle = [148.67, 144.95, 141.19, 137.41, 133.59, 129.73, 125.82, 121.85]
			
				Jacobian = [1.4325, 1.4118, 1.3891, 1.3649, 1.3391, 1.3120, 1.2837, 1.2542]					
		
			elif BeamEnergy == 132:
			
				MidPointLabAngle = [149.15, 145.47, 141.79, 138.06, 134.31, 130.52, 126.68, 122.77, 118.78, 114.71]
			
				Jacobian = [1.4265, 1.4067, 1.3852, 1.3620, 1.3375, 1.3116, 1.2845, 1.2561, 1.2268, 1.1964]
			
			elif BeamEnergy == 134:
		
				MidPointLabAngle = [149.59, 145.98, 142.33, 138.67, 134.97, 131.23, 127.46, 123.62, 119.71, 115.72]
			
				Jacobian = [1.4209, 1.4020, 1.3814, 1.3593, 1.3357, 1.3109, 1.2849, 1.2577, 1.2295, 1.2004]
			
			elif BeamEnergy == 137:
		
				MidPointLabAngle = [150.20, 146.64, 143.08, 139.48, 135.87, 132.22, 128.52, 124.79, 120.97, 117.08]
			
				Jacobian = [1.4131, 1.3953, 1.3760, 1.3551, 1.3330, 1.3096, 1.2851, 1.2595, 1.2328, 1.2053]
			
			elif BeamEnergy == 141:
		
				MidPointLabAngle = [150.91, 147.44, 143.97, 140.47, 136.95, 133.39, 129.80, 126.16, 122.46, 118.70, 114.85, 110.87, 106.77, 102.46, 97.90, 92.94]
			
				Jacobian = [1.4036, 1.3872, 1.3693, 1.3500, 1.3295, 1.3077, 1.2849, 1.2610, 1.2361, 1.2104, 1.1838, 1.1562, 1.1277, 1.0982, 1.0674, 1.0348]
			
			elif BeamEnergy == 143:
		
				MidPointLabAngle = [151.22, 147.81, 144.37, 140.91, 137.43, 133.90, 130.36, 126.76, 123.13, 119.41]
			
				Jacobian = [1.3993, 1.3835, 1.3662, 1.3476, 1.3277, 1.3066, 1.2845, 1.2614, 1.2374, 1.2123]
			
			elif BeamEnergy == 149:
		
				MidPointLabAngle = [152.06, 148.74, 145.41, 142.06, 138.67, 135.27, 131.84, 128.37, 124.85, 121.28, 117.64, 113.92, 110.08, 106.11]
			
				Jacobian = [1.3875, 1.3732, 1.3575, 1.3405, 1.3224, 1.3032, 1.2830, 1.2618, 1.2397, 1.2168, 1.1931, 1.1686, 1.1432, 1.1171]
			
			else:
		
				print('No data for this energy.')
			
				return 0
			
			
		CoMDiffCS, CoMErrorDiffCS = self.GetDiffCSFromBC(BeamEnergy, StartRing, StopRing, ExState=ExState)
		
		LabDiffCS = [round(CoMDiffCS[i]/Jacobian[i], 3) for i in range(len(Jacobian))]
		
		LabDiffErrorCS = [round(CoMErrorDiffCS[i]/Jacobian[i], 3) for i in range(len(Jacobian))]
		
		return np.array(LabDiffCS), np.array(LabDiffErrorCS), MidPointLabAngle
		
		
	# Midpoint Riemann sum integration
	def ExtrapIntegration(self, FilePath, BeamEnergy, Yield=False):
	
		Energy, Angle, DiffCS, SFactor = CSPlot().ExtrapReader(FilePath, BeamEnergy, Yield = Yield)
		
		# The ExtrapReader already converts to mB
		DiffCS = np.array(DiffCS)
		
		# convert to radian
		Angle = np.array(Angle)
		Angle = (np.pi/180)*Angle
		
		
		MidPointDiffCS = [(DiffCS[i]+DiffCS[i+1])/2 for i in range(0, len(DiffCS)-1)]
		MidAngle = [(Angle[i]+Angle[i+1])/2 for i in range(0, len(Angle)-1)]
		
		Areas = [MidPointDiffCS[i]*np.sin(MidAngle[i])*(abs(Angle[i]-Angle[i+1])) for i in range(len(MidPointDiffCS))]
		
		RSum = 2*np.pi*sum(Areas)
	
		return round(RSum, 2)
	
		
	# Calculate the ratio of the number of alpha counts in each state and the respective solid angles. As it stands, everything will be tabulated to the reaction with less counts. In practice this
	# means that it will just take the rings where excited state reactions are detected since they are always fewer. This also just makes it simpler for me as I don't need to do do checks for 
	# which lists are longer, shorter, etc.
	def GsExRatio(self, BeamEnergy, StartRing, ExStopRing, GsStopRing, RingByRing = False):
	
		GsAlphas, GsAlphasError = self.GetAlphaCounts(BeamEnergy, StartRing, GsStopRing)
		ExAlphas, ExAlphasError = self.GetExAlphaCounts(BeamEnergy, StartRing, ExStopRing)
		
		if RingByRing:
			
			GsSolidAngles, GsMidAngle = BeamCurrentCalc().SolidAngleCalc(BeamEnergy, StartRing, StopRing, ExState = False, RingByRing = True)
			ExSolidAngles, ExMidAngle = BeamCurrentCalc().SolidAngleCalc(BeamEnergy, StartRing, StopRing, ExState = True, RingByRing = True)
		
			GsRatios = [GsAlphas[i]/GsSolidAngles[i] for i in range(len(GsSolidAngles))]
			ExRatios = [ExAlphas[i]/ExSolidAngles[i] for i in range(len(ExSolidAngles))]
			
			Ratios = [GsRatios[i]/ExRatios[i] for i in range(len(GsRatios))]
		
			return  Ratios
			
		else:
		
			GsSolidAngles = BeamCurrentCalc().SolidAngleCalc(BeamEnergy, StartRing, GsStopRing, ExState = False, RingByRing = False)
			ExSolidAngles = BeamCurrentCalc().SolidAngleCalc(BeamEnergy, StartRing, ExStopRing, ExState = True, RingByRing = False)
			
			print(GsSolidAngles)
			
			GsAlphas = sum(GsAlphas)
			ExAlphas = sum(ExAlphas)
			
			GsCountsError = [GsAlphasError[i]**2 for i in range(len(GsAlphasError))]
			GsCountsError = np.sqrt(sum(GsCountsError))
			
			ExCountsError = [ExAlphasError[i]**2 for i in range(len(ExAlphasError))]
			ExCountsError = np.sqrt(sum(ExCountsError))
			
			GsRatio = GsAlphas/GsSolidAngles
			ExRatio = ExAlphas/ExSolidAngles
			
			GsExRatio = ExRatio/GsRatio
			
			RatioError = GsExRatio * np.sqrt( (GsCountsError / GsAlphas)**2 + (ExCountsError / ExAlphas)**2 )
			
			CoMEnergy = BeamEnergy*(Constants().HMass / (Constants().HMass + Constants().NeMass))
			
			return round(CoMEnergy, 2), GsExRatio, RatioError, GsSolidAngles
		

		
class CSPlot:

	def EnergyCoMConversion(self, BeamParticle, TargetParticle):
	
		if BeamParticle == '20Ne':
			BeamParticleMass = Constants().NeMass
		elif BeamParticle == '1H':
			BeamParticleMass = Constants().HMass
		elif BeamParticle == '17F':
			BeamParticleMass = Constants().FMass
		elif BeamParticle == '4He':
			BeamParticleMass = Constants().HeMass
		else:
			print('No data for this particle.')
			return 0
			
		if TargetParticle == '20Ne':
			TargetParticleMass = Constants().NeMass
		elif TargetParticle == '1H':
			TargetParticleMass = Constants().HMass
		elif TargetParticle == '17F':
			TargetParticleMass = Constants().FMass
		elif TargetParticle == '4He':
			TargetParticleMass = Constants().HeMass
		else:
			print('No data for this particle.')
			return 0
			
		Conversion = TargetParticleMass / (BeamParticleMass + TargetParticleMass)
		
		return Conversion
	
		
	
	# Read AZURE extrapolation file. Outputs to mB
	def ExtrapReader(self, FilePath, BeamEnergy, Yield = False):
	
		ExtrapFile = open(FilePath)
	
		ExtrapLines = ExtrapFile.readlines()[:]
	
		ExtrapFile.close()
	
		ExtrapCS = []
		ExtrapAngle = []
		SFactor = []
		Energy = []
	
		for line in ExtrapLines:
			newline = line.split()
			if newline == []:
				break
			else:
				Energy.append(float(newline[1]))
				ExtrapAngle.append(float(newline[2]))
				if Yield:
					ExtrapCS.append(float(newline[3])/(AZUREWriter().GetTargetAtoms(BeamEnergy))/(Constants().MilliBarnToCmSquared))
					SFactor.append(float(newline[4])/(AZUREWriter().GetTargetAtoms(BeamEnergy))/(Constants().MilliBarnToCmSquared))
				else:	
					ExtrapCS.append(float(newline[3])*1000)
					SFactor.append(float(newline[4])*1000)
				
		return Energy, ExtrapAngle, ExtrapCS, SFactor
		
		
	def FitReader(self, FilePath, BeamEnergy, Yield=False):
	
		FitFile = open(FilePath)
		
		FitLines = FitFile.readlines()[:]
		
		FitFile.close()
		
		DataCS = []
		DataError = []
		FitData = []
		Energy = []
		Angle = []
		
		for line in FitLines:
			newline = line.split()
			if newline == []:
				break
			else:
				Energy.append(float(newline[1]))
				Angle.append(float(newline[2]))
				if Yield:
					FitData.append(float(newline[3])/(AZUREWriter().GetTargetAtoms(BeamEnergy))/(Constants().MilliBarnToCmSquared))
					DataCS.append(float(newline[5])/(AZUREWriter().GetTargetAtoms(BeamEnergy))/(Constants().MilliBarnToCmSquared))
					DataError.append(float(newline[6])/(AZUREWriter().GetTargetAtoms(BeamEnergy))/(Constants().MilliBarnToCmSquared))
				else:
					FitData.append(float(newline[3])*1000)
					DataCS.append(float(newline[5])*1000)
					DataError.append(float(newline[6])*1000)
					
		BeamEnergySorted = []
		PAlphaDataSorted = []
		PAlphaErrorSorted = []
		FitDataSorted = []
		
		i=0
		while True:
	
			if len(Energy) == 0:
				break
			elif Energy[i] == min(Energy):
	
				BeamEnergySorted.append(Energy[i])
				PAlphaDataSorted.append(DataCS[i])
				PAlphaErrorSorted.append(DataError[i])
				FitDataSorted.append(FitData[i])
		
				Energy.pop(i)
				DataCS.pop(i)
				DataError.pop(i)
				FitData.pop(i)
		
				i=0
			else:
				i+=1
				
		return BeamEnergySorted, Angle, FitDataSorted, PAlphaDataSorted, PAlphaErrorSorted
		
		
	def InputFileReader(self, FilePath, BeamEnergy, BeamParticle, TargetParticle, Yield=False):
	
		EnergyConversion = self.EnergyCoMConversion(BeamParticle, TargetParticle)
	
		InputFile = open(FilePath)
		
		FitLines = InputFile.readlines()[:]
		
		InputFile.close()
		
		DataCS = []
		DataError = []
		Energy = []
		Angle = []
		
		for line in FitLines:
			newline = line.split()
			if newline == []:
				break
			else:
				Energy.append(float(newline[0])*EnergyConversion)
				Angle.append(float(newline[1]))
				if Yield:
					DataCS.append(float(newline[2])/(AZUREWriter().GetTargetAtoms(BeamEnergy))/(Constants().MilliBarnToCmSquared))
					DataError.append(float(newline[3])/(AZUREWriter().GetTargetAtoms(BeamEnergy))/(Constants().MilliBarnToCmSquared))
				else:
					DataCS.append(float(newline[2])*1000)
					DataError.append(float(newline[3])*1000)
				
		return Energy, Angle, DataCS, DataError
	
		
	
	# Plots 20Ne(p,a) differential cross section in CoM Frame	
	def GSDiffCSPlot(self, BeamEnergy, StartRing, StopRing, SatPeakNorm = False, ExState = False):
	
		SolidAngles, MidpointAngles = BeamCurrentCalc().SolidAngleCalc(BeamEnergy, StartRing, StopRing, RingByRing = True)
		
		AlphaDiffCS, DiffCSError = CSCalc().GetDiffCSFromBC(BeamEnergy, StartRing, StopRing, ExState = ExState)
		
		plt.errorbar(x=MidpointAngles, y=AlphaDiffCS, yerr=DiffCSError, c='b', marker='o', ls='none')
		
		
		TitleString = 'p($^{}$'.format('2') + '$^{}$'.format('0') + 'Ne,${}$'.format('\\alpha')  + ')$^{}$'.format('1') + '$^{}$'.format('7') + 'F'
		DiffCSString = '$\left(\\frac{d \sigma}{d \Omega}\\right)_{CM}$'
		DiffCSUnit = '$\left(\\frac{mB}{str}\\right)$'
		Angle = '$\\theta_{CM}$'
		
		plt.title(TitleString + ' Differential Cross Section ' + str(BeamEnergy) + ' MeV', fontsize=24)
		plt.ylabel(DiffCSString + DiffCSUnit, fontsize=24)
		plt.xlabel(Angle + '($^{\circ}$)', fontsize=24)
		plt.yticks(fontsize=20);
		plt.xticks(fontsize=20);
		plt.gca().invert_xaxis()
		plt.show()
		
		return 0
	
		
class CSVwriter:

	# Simple method for outputting csv file for an unspecified number of columns
	def write_arrays_to_csv(self, filename, *arrays, headers=None):

		with open(filename, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)

			if headers:
				writer.writerow(headers)

			for row in zip(*arrays):
				writer.writerow(row)

	
	# Write csv file with relevant information for beam current calculations from Fernandez differential cross sections
	def CalculationParameters(self, BeamEnergy, StartRing, StopRing, SatPeakNorm=False):
	
		RingNumber = [i for i in range(StartRing, StopRing+1)]
	
		SolidAngles, MidpointAngles = BeamCurrentCalc().SolidAngleCalc(BeamEnergy, StartRing, StopRing, RingByRing = True)
		
		Alphas, AlphaError = CSCalc().GetAlphaCounts(BeamEnergy, StartRing, StopRing)	
		
		RingEff = BeamCurrentCalc().SingleRingEff(BeamEnergy, StartRing, StopRing, ExcitedState = False, PrintEff = False, RingByRing = True)	
		
		
		if SatPeakNorm:
			CurrentTargetTimeAvg, CurrentTargetTimeAvgError = BeamCurrentCalc().GetSatPeakCounts(BeamEnergy)
		else:
			CurrentTargetTimeAvg, CurrentTargetTimeAvgError = BeamCurrentCalc().GetFernandezData(BeamEnergy, Diagnostic=False)
			
			
		CurrentTargetTimeList = np.ones(len(Alphas))
		
		CurrentTargetTimeList = CurrentTargetTimeList*CurrentTargetTimeAvg
			
		CurrentTargetTimeErrorList = np.ones(len(Alphas))	
			
		CurrentTargetTimeErrorList = CurrentTargetTimeErrorList*CurrentTargetTimeAvgError
		
		Filename = str(BeamEnergy) + 'MeV_Calculation.csv'
		
		HeaderList = ['Ring Number', 'Alpha Counts', 'Alpha Error', 'Current*(Target Density)*Time', 'Current*(Target Density)*Time Error', 'Solid Angle', 'Ring Efficiency']
		
		
		self.write_arrays_to_csv(Filename, RingNumber, Alphas, AlphaError, CurrentTargetTimeList, CurrentTargetTimeErrorList, SolidAngles, RingEff, headers=HeaderList)
		
		return 0
		

class AZUREWriter:

	# Get the number of target atoms for the "pretend" Neon target
	def GetTargetAtoms(self, BeamEnergy):
	
		if BeamEnergy == 128:
			TargetAtoms = 5.10*10**19
		elif BeamEnergy == 130:
			TargetAtoms = 5.39*10**19
		elif BeamEnergy == 132:
			TargetAtoms = 5.41*10**19
		elif BeamEnergy == 134:
			TargetAtoms = 5.42*10**19
		elif BeamEnergy == 137:
			TargetAtoms = 5.42*10**19
		elif BeamEnergy == 141:
			TargetAtoms = 4.92*10**19
		elif BeamEnergy == 143:
			TargetAtoms = 4.93*10**19
		elif BeamEnergy == 149:
			TargetAtoms = 4.9*10**19
		elif BeamEnergy == 'Activation':
			TargetAtoms = 3.03*10**(19)
		elif BeamEnergy == 'Fernandez':
			TargetAtoms = 2.09*10**(19)
		else:
			print('No data for this energy.')
			return 0
			
		return TargetAtoms

	# Writes input file for AZURE, specifically for differential cross section calculations 
	def InputFile(self, BeamEnergy, StartRing, StopRing, ExState = False, Yield=False):
	
		# calculates quantities in mB
		LabDiffCS, LabErrorDiffCS, LabMidAngle = CSCalc().GetLabDiffCS(BeamEnergy, StartRing, StopRing, ExState = ExState)
			
		
		
		# Convert from mB to B
		LabDiffCSBarn = LabDiffCS/1000 
		
		# Convert from mB to B
		LabErrorDiffCSBarn = LabErrorDiffCS/1000 
		
		# Convert to yield for Target Effect Calculations
		LabDiffCSYield = LabDiffCSBarn*self.GetTargetAtoms(BeamEnergy)*Constants().BarnToCmSquared
		
		# Convert to yield for Target Effect Calculations
		LabErrorDiffCSYield = LabErrorDiffCSBarn*self.GetTargetAtoms(BeamEnergy)*Constants().BarnToCmSquared
		
		
		OutputDirectory = '/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/AZUREFits/data/'
		
		
		if ExState:
			FilenameDat = 'AZUREInputANL' + str(BeamEnergy) + 'MeVExState.dat'
		else:
			FilenameDat = 'AZUREInputANL' + str(BeamEnergy) + 'MeV.dat'
		
		
		
		if Yield:
		
			EnergyIndex = [round(BeamEnergy*(Constants().HMass/Constants().NeMass), 3) for i in range(len(LabDiffCSYield))]
			#EnergyIndex = [6.51 for i in range(len(LabDiffCSYield))]
			
			YieldFormatted = ['{:.3e}'.format(LabDiffCSYield[x]) for x in range(len(LabDiffCSYield))]
			YieldErrorFormatted = ['{:.3e}'.format(LabErrorDiffCSYield[x]) for x in range(len(LabErrorDiffCSYield))]
			
			if ExState:
				FilenameDat = 'AZUREInputYieldANL' + str(BeamEnergy) + 'MeVExState.dat'
				FilenameCSV = 'AZUREInputYieldANL' + str(BeamEnergy) + 'MeVExState.csv'
			else:
				FilenameDat = 'AZUREInputYieldANL' + str(BeamEnergy) + 'MeV.dat'
				FilenameCSV = 'AZUREInputYieldANL' + str(BeamEnergy) + 'MeV.csv'
			
			FilenameCSV = 'AZUREInputYieldANL' + str(BeamEnergy) + 'MeV.csv'
			
			CSVwriter().write_arrays_to_csv(FilenameCSV, EnergyIndex, LabMidAngle, YieldFormatted, YieldErrorFormatted)
			
		else:
		
			AZUREEnergy = round(((BeamEnergy - (BeamCurrentCalc().GetEnergyLoss(BeamEnergy)/2)) / Constants().NeMass) * Constants().HMass , 3)
			EnergyIndex = [AZUREEnergy for i in range(len(LabDiffCS))]
			
			CSFormatted = ['{:.3e}'.format(LabDiffCSBarn[x]) for x in range(len(LabDiffCSBarn))]
			CSErrorFormatted = ['{:.3e}'.format(LabErrorDiffCSBarn[x]) for x in range(len(LabErrorDiffCSBarn))]
			
			if ExState:
				FilenameDat = 'AZUREInputANL' + str(BeamEnergy) + 'MeVExState.dat'
				FilenameCSV = 'AZUREInputANL' + str(BeamEnergy) + 'MeVExState.csv'
			else:
				FilenameDat = 'AZUREInputANL' + str(BeamEnergy) + 'MeV.dat'
				FilenameCSV = 'AZUREInputANL' + str(BeamEnergy) + 'MeV.csv'
			
			CSVwriter().write_arrays_to_csv(FilenameCSV, EnergyIndex, LabMidAngle, CSFormatted, LabErrorDiffCSBarn)
			
			
		FilePath = os.path.join(OutputDirectory, FilenameDat)
		
				
		with open(FilePath, 'w') as wf:
			with open(FilenameCSV, 'r') as rf:
				[ wf.write('    '.join(row)+'\n') for row in csv.reader(rf)]
			wf.close()
			
		return 0
		
	
	# takes energy input in MeV
	def FernandezEnergyShift(self, energy):
	
		# I don't buy the energy loss estimation in their paper. LISE calculations seem to claim different losses. I am going with LISE.
		slope = ((32 - 55) * 10**(-3)) / (7.83 - 3.81)
		yint = 0.0768 # max energy loss in MeV from linear fit
		
		# From Fernandez paper
		#slope = ((25 - 40) * 10**(-3)) / (7.83 - 3.81) # MeV lost / MeV beam
		#yint = 0.0542
		
		ReducedSlope = slope/AZUREWriter().GetTargetAtoms('Fernandez')
		ReducedIntercept = yint/AZUREWriter().GetTargetAtoms('Fernandez')
		
		print('AZURE Intercept: ', ReducedIntercept)
		print('AZURE Slope: ', ReducedSlope)
		
		return energy + (slope*energy + yint)/2
		
	
	# Working fast, just need to create new fernandez input file	
	def FernandezYieldInput(self):
	
		InputCSV = r'/home/wbrave1/Desktop/20Ne_data/PAlphaInelasticExpEffects/Data/FernandezInelastics.csv'
		
		OutputDirectory = '/home/wbrave1/Desktop/20Ne_data/PAlphaInelasticExpEffects/Data'
		#OutputFilename = 'FernandezInelastics.dat'
		
		with open(InputCSV) as csvfile:
			
			for lines in csvfile.readlines()[:]:
			
				BeamEnergy = [self.FernandezEnergyShift(float(i.split(',',1)[0])) for i in lines]
				CS = [float(i.split(',', 3)[2])/self.GetTargetAtoms('Fernandez') for i in lines]
				Error = [float(i.split(',', 4)[3])/self.GetTargetAtoms('Fernandez') for i in lines]
		
		CSFormatted = ['{:.3e}'.format(CS[x]) for x in range(len(CS))]
		EnergyFormatted = ['{:.3e}'.format(BeamEnergy[x]) for x in range(len(BeamEnergy))]
		ErrorFormatted = ['{:.3e}'.format(Error[x]) for x in range(len(Error))]
		zeroes = ['0.000' for i in range(len(BeamEnergy))]
		
		with open(os.path.join(OutputDirectory, 'FernandezInelasticsYield.csv'), 'w') as f:
			writer = csv.writer(f, delimiter=',');
			writer.writerows(zip(EnergyFormatted, zeroes, CSFormatted, ErrorFormatted))
   			 
		with open(os.path.join(OutputDirectory, 'FernandezInelasticsYield.dat'), 'w') as wf:
			with open(os.path.join(OutputDirectory, 'FernandezInelastics.csv'), 'r') as rf:
				[wf.write('    '.join(row)+'\n') for row in csv.reader(rf)]
			wf.close()  
		
		return 0
		
# For calculations in this class I am taking the convention that TimeInverted = True is the 20Ne(p,a) reaction and False is 17F(a,p)
class ReactionRate:


	# Uses reciprocity theorem to convert 20Ne(p,a) reaction cross section to 17F(a,p) reaction cross section. Will add customizability if I need more file flexibility.	
	def GetReactionData(self, FilePath, TimeInverted = False):
		
		ExtrapEnergy, ExtrapAngle, ExtrapCS, SFactor = CSPlot().ExtrapReader(FilePath, BeamEnergy='Activation', Yield=False)
		
		# The Extrap reader outputs in mB, we need it in B for the integration
		ExtrapCS = np.array(ExtrapCS)/1000
		
		if TimeInverted:
		
			return ExtrapEnergy, ExtrapCS
			
		else:
		
			ForawardEnergy = [ExtrapEnergy[i] + Constants().QVal for i in range(len(ExtrapEnergy))]
			
			HeFReducedMass = (Constants().FMass*Constants().HeMass)/(Constants().FMass + Constants().HeMass)
			NeHReducedMass = (Constants().NeMass*Constants().HMass)/(Constants().NeMass + Constants().HMass)
			ReducedMassRatio = (NeHReducedMass/HeFReducedMass)
			
			SpinFactor = ((2*Constants().NeGSspin + 1)*(2*Constants().Hspin + 1))/((2*Constants().FGSspin + 1)*(2*Constants().HeGSspin + 1))
			
			ForwardCS = [ SpinFactor * ReducedMassRatio * (ExtrapEnergy[i]/ForawardEnergy[i]) * ExtrapCS[i] for i in range(len(ExtrapCS))]
		
		
			return ForawardEnergy, ForwardCS
		
			
	# Convert 20Ne(p,a) reaction rate to 17F(a,p). Takes temp in GK. Used to convert NACRE 20Ne(p,a) reaction rate.
	def ReactionRateConversion(self, Temp):
		
		SpinFactor = ((2*Constants().NeGSspin + 1)*(2*Constants().Hspin + 1)) / ((2*Constants().HeGSspin + 1)*(2*Constants().FGSspin + 1))
		
		NeHReducedMass = (Constants().NeMass*Constants().HMass)/(Constants().NeMass + Constants().HMass)
		
		HeFReducedMass = (Constants().FMass*Constants().HeMass)/(Constants().FMass + Constants().HeMass)
		
		ReducedMassRatio = NeHReducedMass/HeFReducedMass
		
		# Iliadis Equation 3.31
		ConversionFactor = SpinFactor * (ReducedMassRatio**(3/2)) * math.exp(-Constants().QVal / (Constants().Boltzmann * Temp))
		
		#print(SpinFactor*(ReducedMassRatio**(3/2)))
		#print(-Constants().QVal / (Constants().Boltzmann))
		
		return ConversionFactor
			
			
			
	# Takes Temp in GK, energies in MeV to calculate reaction rate
	def ReactionRateIntegration(self, FilePath, Temp, TimeInverted=False):
		
		EnergyCoM, CrossSection = self.GetReactionData(FilePath, TimeInverted = TimeInverted)
		
		NeHReducedMass = (Constants().NeMass*Constants().HMass)/(Constants().NeMass + Constants().HMass)
		
		HeFReducedMass = (Constants().FMass*Constants().HeMass)/(Constants().FMass + Constants().HeMass)
				
		if TimeInverted:

			# Illiadis equation 3.10, takes temperature in GK
			ConstantFactor = ((3.7318*10**10) / Temp**(3/2)) * (1 / np.sqrt(NeHReducedMass)) 
			
		else: 
					
			# Illiadis equation 3.10, takes temperature in GK
			ConstantFactor = ((3.7318*10**10) / Temp**(3/2)) * (1 / np.sqrt(HeFReducedMass))
		
		RectangularArea = [CrossSection[j] * EnergyCoM[j] * math.exp(-(EnergyCoM[j]/(Constants().Boltzmann * Temp))) * (EnergyCoM[j+1] - EnergyCoM[j]) for j in range(0, len(EnergyCoM)-1)]	
		
		ReactionRate = ConstantFactor * sum(RectangularArea)	
		
		#print(EnergyCoM)
		
		return ReactionRate
		
		
		
	# Takes Temp in GK to calculate reaction rate from ReacLib function, 17F(a,p)
	def ReacLibForwardReac(self, Temp):
	
		a0 = 3.862870*10;
		a1 = 0.000000;
		a2 = -4.318000*10;
		a3 = 4.468270;
		a4 = -1.639150;
		a5 = 1.234830*10**(-1);
		a6 = -6.66667*10**(-1);
	
		RateFunc = math.exp(a0 + a1/Temp + a2/Temp**(1/3) + a3*Temp**(1/3) + a4*Temp + a5*Temp**(5/3) + a6*math.log(Temp))
		
		return RateFunc
		
	# Reaction Rate 20Ne(p,a)
	def ReacLibInverseReac(self, Temp):
	
		a0 = 4.156300 * 10;
		a1 = -4.792660 * 10;
		a2 = -4.318000 * 10;
		a3 = 4.468270;
		a4 = -1.639150;
		a5 = 1.234830 * 10**(-1);
		a6 = -6.66667 * 10**(-1);
		
		RateFunc = math.exp(a0 + a1/Temp + a2/Temp**(1/3) + a3*Temp**(1/3) + a4*Temp + a5*Temp**(5/3) + a6*math.log(Temp))
		
		return RateFunc
		
	# 20Ne(p,a)
	def NacreRate(self, Temp):
	
		# Tabular values from NACRE paper
		'''
		Temp = [0.9, 1, 1.25, 1.5, 1.75, 2, 2.5, 3] 
		AdoptedRate = [1.22, 1.14, 3.22, 1.72, 9.03, 1.08, 1.01, 1.08]
		Exp = [-24, -21, -16, -12, -10, -7, -4, -2]
		
		Rate = [AdoptedRate[i]*10**Exp[i] for i in range(len(AdoptedRate))]
		
		return Temp, Rate
		'''
		
		# Nacre also provides a functional form of reaction rate
		a0 = 3.75*10**(18)
		a1 = -43.18
		a2 = -47.92
		a3 = -1.40*10**(-3)
		a4 = 3.44*10**(-2)
		a5 = -0.278
		a6 = 0.354
		
		Rate = a0*Temp**(-2/3) *  math.exp(a1*Temp**(-1/3) + a2/Temp) * math.exp(a3*Temp**4 + a4*Temp**3 + a5*Temp**2 + a6*Temp)
		
		return Rate
	
	# only applies for T9=0.9 to T9=10, 20Ne(p,a)	
	def ThermalizedNacreRate(self, Temp):
	
		GSrate = self.NacreRate(Temp)
		
		a0 = 5.341
		a1 = -0.549
		a2 = 0.363
		a3 = -0.0603
		a4 = 2.9*10**(-3)
		
		Rate = GSrate * (a0 + a1*Temp + a2*Temp**2 + a3*Temp**3 + a4*Temp**4)
		
		return Rate
		
		
	def FPartitionFunction(self, Temp):
		
		a1 = 4.16*10**(-1)
		a2 = -3.07*10**(-1)
		a3 = -6.03*10**0
		a4 = 6.64*10**(-2)
		a5 = 0
			
		Partition = 1 + a1*Temp**(a2) * math.exp(a3/Temp + a4*Temp + a5*Temp**(2/3))
		
		return Partition
		
	def NePartitionFunction(self, Temp):
	
		a1 = 1.02*10**1
		a2 = -6.02*10**(-1)
		a3 = -1.99*10**1
		a4 = 8.95*10**(-2)
		a5 = 0
		
		Partition = 1 + a1*Temp**(a2) * math.exp(a3/Temp + a4*Temp + a5*Temp**(2/3))
		
		return Partition
		
		
	# conversion factor for thermalized 20Ne(p,a) reaction rate to thermalized 17F(a,p) using NACRE's prescription
	def ThermalizedConversionFactor(self, Temp):
	
		RevRatio = 5.372*10**(-2) * math.exp(47.920/Temp)
		
		NePartition = self.NePartitionFunction(Temp)
		FPartition = self.FPartitionFunction(Temp)
		HPartition = 1
		HePartition = 1
		
		Conversion = RevRatio*((NePartition*HPartition)/(FPartition*HePartition))
		
		return Conversion

		
	# 20Ne(p,a)
	def CF88Rate(self, Temp):
	
		TA = Temp/(1 + 6.12*(10**(-2))*Temp + 1.30*(10**(-2))*(Temp**(5/3))/(1 + 6.12*(10**(-2))*Temp)**(2/3))
	
		a0 = 3.25*10**(19)
		a1 = 5.31
		a2 = 0.544
		a3 = -0.0523
		a4 = -43.176
		a5 = -47.969
		
		Rate = a0 * (a1 + a2*Temp + a3*Temp**2) * ((TA**(5/6))/(Temp**(3/2))) * math.exp(a4/TA**(1/3) + a5/Temp)
		
		return Rate
		
	# 17F(a,p) reaction rate from analytic S-factor in NACRE paper
	def SFactorRate(self, FilePath, Temp):
	
		FZ = 9
		HeZ = 2
		
		EnergyCoM, CrossSection = self.GetReactionData(FilePath, TimeInverted = False)
	
		HeFReducedMass = (Constants().FMass*Constants().HeMass)/(Constants().FMass + Constants().HeMass)
		
		ConstantFactor = (3.7318*10**10) * Temp**(-3/2) * HeFReducedMass**(-1/2)
		
		Sommerfeld = [0.1575*FZ*HeZ*np.sqrt(HeFReducedMass/EnergyCoM[j]) for j in range(len(EnergyCoM))]
		
		Boltzmann = [math.exp(-(EnergyCoM[j]/(Constants().Boltzmann * Temp))) for j in range(len(EnergyCoM))]
		
		SFactor = [(4.83 * 10**8) * math.exp(-1.5693*EnergyCoM[j]) for j in range(len(EnergyCoM))]
		
		RectangularArea = [ Boltzmann[j] * SFactor[j] * math.exp(-2*np.pi*Sommerfeld[j]) * (EnergyCoM[j+1] - EnergyCoM[j]) for j in range(0, len(EnergyCoM)-1)]
		 
		RSum = sum(RectangularArea)*ConstantFactor
		
		return RSum
		
	def ConvertedSFactorRate(self, Temp):
	
		HeFRate = self.SFactorRate(Temp)
		
		HeFToNePConversion = 1/self.ReactionRateConersion(Temp)
		
		NePRate = HeFRate*HeFToNePConversion
		
		return NePRate
		
		
		
	'''	
	# Comparison of our reaction rate and reaclib. It seems like these are the only plots we care about, I don't really see where we go down a path of wanting a lot of customization. So, I will
	# leave the method as is for now, but I can go through and allow it to take an unspecified number of entries and group them if needed.	
	def ReactionRatePlot(self, FilePath, MinTemp, MaxTemp, TimeInverted = False):
	
		plt.rcParams.update({'font.size': 22})
			
	
		Temperature = [MinTemp + 0.01*i for i in range(0, int(((MaxTemp-MinTemp)*100)) + 1)]
		
		ReactionRate = [self.ReactionRateIntegration(FilePath, Temperature[i], TimeInverted = TimeInverted) for i in range(len(Temperature))]
		
		ExReactionRate = [self.ReactionRateIntegration(FilePath, Temperature[i], TimeInverted = TimeInverted) for i in range(len(Temperature))]
		
		NacreRR = [self.NacreRate(Temperature[i]) for i in range(len(Temperature))]
		
		ThermalizedNacreRR = [self.ThermalizedNacreRate(Temperature[i]) for i in range(len(Temperature))]
		
		CF88 = [self.CF88Rate(Temperature[i]) for i in range(len(Temperature))]
		
		# There is something fishy going on with this S-factor calculation. I'll need to look into it more.
		SFactorRR = [self.SFactorRate(FilePath, Temperature[i]) for i in range(len(Temperature))]
		
		plt.plot(Temperature, ReactionRate, color='r', marker='.', markersize=1, label='Activation Measurement')
		
		if TimeInverted:
		
			ReacLibInverse = [self.ReacLibInverseReac(Temperature[i]) for i in range(len(Temperature))]
			
			ConvertedSFactorRate = [SFactorRR[i]/self.ReactionRateConersion(Temperature[i]) for i in range(len(Temperature))]
			
			plt.plot(Temperature, NacreRR, color='b', marker='.', markersize=1, label='NACRE Rate')
			
			plt.plot(Temperature, ThermalizedNacreRR, color='k', marker='.', markersize=1, label='Thermalized NACRE Rate')
			
			#plt.plot(Temperature, ReacLibInverse, color='g', marker='.', markersize=1, label='REACLIB')
			
			#plt.plot(Temperature, CF88, color='m', marker='.', markersize=1, label='CF88')
			
			plt.plot(Temperature, ConvertedSFactorRate, color='orange', marker='.', markersize=1, label='Converted S-Factor NACRE')
			
			plt.title('$^{20}$Ne(p,$\\alpha$)$^{17}F$ Reaction Rate')
			
		else:
		
			ThermalizedRRconversion = [self.ThermalizedConversionFactor(Temperature[i]) for i in range(len(Temperature))]
			
			ThermalizedForwardReaction = [ThermalizedRRconversion[i]*ThermalizedNacreRR[i] for i in range(len(ThermalizedNacreRR))]
			
			ConvertedNacreRR = [NacreRR[i]*self.ReactionRateConersion(Temperature[i]) for i in range(len(Temperature))]
			
			ReacLibRate = [self.ReacLibForwardReac(Temperature[i]) for i in range(len(Temperature))]
		
			plt.plot(Temperature, ConvertedNacreRR, color='g', marker='.', markersize=1, label='NACRE Ground State Rate')
			
			#plt.plot(Temperature, ReacLibRate, color='b', marker='.', markersize=1, label='ReacLib')
			
			plt.plot(Temperature, ThermalizedForwardReaction, color='b', marker='.', markersize=1, label='NACRE Thermalized Rate')
			
			plt.plot(Temperature, SFactorRR, color='orange', marker='.', markersize=1, label='NACRE S-Factor')
		
			plt.title('$^{17}F$($\\alpha$,p)$^{20}$Ne Reaction Rate')
			
			
		plt.yscale('log')
		
		plt.xlabel('Temperature (GK)')
		
		plt.ylabel('Reaction Rate ($cm^3 mol^{-1} sec^{-1}$)')
		
		plt.legend()
		
		plt.show()
		
		return 0	
	'''
	
	# calculate rtt from NACRE
	def ThermalizationFactor(self, Temperature):
		
		NePF = self.NePartitionFunction(Temperature)
		
		SpinNeGS = 0;
		SpinNeEX = 2; 
		
		FirstExcitedState = 1.633674 # MeV
		
		RateGS = self.NacreRate(Temperature)
		RateThermal = self.ThermalizedNacreRate(Temperature)
		
		SpinFactor = ((2*SpinNeEX + 1)/(2*SpinNeGS + 1))
		
		Rtt = (1/NePF)*SpinFactor*math.exp(-(FirstExcitedState * 11.605) / Temperature) 
		
		return Rtt
		
	def ReadTempFile(self, filepath):
	
		TempFile = open(filepath)
		
		TempLines = TempFile.readlines()[1:]
		
		TempFile.close()
		
		Temp = []
		ReacRate = []
		
		for line in TempLines:
			newline = line.split()
			if newline == []:
				break
			else:
				Temp.append(newline[0])
				ReacRate.append(float(newline[1]))
				
		return Temp, ReacRate
		

	
			
		
