# I am getting tired of the mess in these alpha calculation files. Time to do something about it.

import numpy as np
import csv as csv
import matplotlib.pyplot as plt

class BeamCurrentCalc:


	
	
	def __init__(self): 
	
		#self.NeMass = 20.    
		#self.HMass = 1.
		
		# When we get more precise about beam energy uncertainties and such I will start using ion masses. For now passing through with amu = 20 & 1 should be fine
		self.NeMass = 19.992 # 9+
		self.HMass = 1.00728 
		
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
		else:
			print('No data for this energy.')
			return 0
		
		return target_thickness
			
	
	def GetFernandezData(self, BeamEnergyInput, Diagnostic=False):
    		
		FernandezCS = []
		FernandezEnergy = []
    	
		Fernandez_data = r"/home/wbrave1/Desktop/20Ne_data/ANL/new_sort/Fernandez_fig2.csv"

		with open(Fernandez_data) as csvfile:
			lines = csvfile.readlines()[1:];
			FernandezFig2Energy = [round((float(i.split(',', 1)[0]))/self.HMass, 3) for i in lines[:]];
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
			GScounts = [round(float(i.split(',', 2)[1]), 0) for i in lines[self.Fernandez165RingStart: self.Fernandez165RingStop + 1]];
			GSerror = [round(float(i.split(',', 3)[2]), 0) for i in lines[self.Fernandez165RingStart: self.Fernandez165RingStop + 1]];
			EXcounts = [round(float(i.split(',', 4)[3]), 0) for i in lines[self.Fernandez165RingStart: self.Fernandez165RingStop + 1]];
			EXerror = [round(float(i.split(',', 5)[4]), 0) for i in lines[self.Fernandez165RingStart: self.Fernandez165RingStop + 1]];
			
			
		runtime = self.GetRuntime(BeamEnergyInput)
		
		target_thickness = self.GetTargetThickness(BeamEnergyInput)
			
		EnergyLoss = self.GetEnergyLoss(BeamEnergyInput)
    			
		MaxEnergy = round(BeamEnergyInput/self.NeMass, 3)
		MinEnergy = round((BeamEnergyInput - EnergyLoss) / self.NeMass, 3)
    		
		for i in range(len(FernandezFig2Energy)):
			if FernandezFig2Energy[i] <= MaxEnergy and FernandezFig2Energy[i] >= MinEnergy:
				FernandezEnergy.append(FernandezFig2Energy[i])
				FernandezCS.append(FernandezFig2CrossSection[i])
    	
		
		CManglesElastic = [169.936, 168.678, 167.42, 166.162, 164.904, 163.646, 162.388, 161.131, 159.873, 158.616, 157.358, 156.101, 154.843, 153.586, 152.329, 151.072, 149.815]
		# For simplicity sake I am just assuming CoM angles stay constant across all energies. It's not a bad assumption, at the worst they should only be a couple tenths of a degree off.
		
		CManglesElastic = np.array(CManglesElastic)
		CManglesElastic = CManglesElastic*(np.pi/180)
		
		Domega = round(2*np.pi*(np.cos(CManglesElastic[self.Fernandez165RingStop + 1]) - np.cos(CManglesElastic[self.Fernandez165RingStart])), 3)
		
		CurrentTargetTime = [sum(GScounts) / (FernandezCS[i] * Domega) for i in range(len(FernandezCS))]
		CurrentTargetTime = np.array(CurrentTargetTime)
		
		AverageCurrentTargetTime = sum(CurrentTargetTime) / len(CurrentTargetTime)
						
		CurrentTargetTimeError = [sum(GSerror) / (FernandezCS[i] * Domega) for i in range(len(FernandezCS))]
		CurrentTargetTimeError = np.array(CurrentTargetTimeError)
		
		
		AverageCurrentTargetTimeError = sum(CurrentTargetTimeError) / len(CurrentTargetTimeError)
		
		HydrogenAtoms = round((target_thickness/self.MethyleneMolarMass)*self.Mol*2, 3)
				
		AverageBeamCurrent = round((AverageCurrentTargetTime / (runtime*HydrogenAtoms*(10**(-27))))*(self.NeChargeState*self.ElectronCharge*10**12), 2)
		AverageBeamCurrentError = round((AverageCurrentTargetTimeError / (runtime*HydrogenAtoms*(10**(-27))))*(self.NeChargeState*self.ElectronCharge*10**12), 2)
		
		if Diagnostic:
		
			print('Beam Energy: ', BeamEnergyInput, ' MeV')
			print('Max Energy: ', MaxEnergy, ' MeV/u')
			print('Min Energy: ', MinEnergy, ' MeV/u')
			print('Runtime: ', runtime, ' seconds')
			print('Hydrogen Atoms: ', HydrogenAtoms)
			print('Solid Angle: ', Domega, ' str')
			print('Neon Charge State: ', self.NeChargeState)
			print('Neon Mass: ', self.NeMass, ' Daltons')
			print('Hydrogen Mass: ', self.HMass, ' Daltons')
			print('Average Beam Current: ', AverageBeamCurrent, ' epA')
			print('Avegage Beam Current Error: ', AverageBeamCurrentError, ' epa')
			print('Fernandez Energies (MeV/u): ')
			
			for i in range(len(FernandezEnergy)):
				print(FernandezEnergy[i])
			
			print('Fernandez Cross Section (mB/str): ')	
			
			for i in range(len(FernandezCS)):
				print(FernandezCS[i])
			
			
		
		  		
		return AverageCurrentTargetTime, AverageCurrentTargetTimeError
		
	
	
	
	
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
		elif BeamEnergy == 152.5:
			CMAngles = [158.292, 155.512, 152.706, 149.871, 147.002, 144.094, 141.142, 138.137, 135.073, 131.94, 128.726, 125.417, 121.994, 118.432, 114.7, 110.75, 106.512]
			CMAngles = np.array(CMAngles)
			CMAngles = CMAngles*(np.pi/180)
		else:
			print('No data for this energy')
			return 0
			
		
		MidpointAngles = [(CMAngles[i] + CMAngles[i+1])/2 for i in range(len(CMAngles)-1)]
		MidpointAngles = np.array(MidpointAngles)
		
		return CMAngles, MidpointAngles
	
	
	
	
	def SolidAngleCalc(self, BeamEnergy, StartRing, StopRing, RingByRing = False):
	
	
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
		elif BeamEnergy == 152.5:
			CMAngles = [158.292, 155.512, 152.706, 149.871, 147.002, 144.094, 141.142, 138.137, 135.073, 131.94, 128.726, 125.417, 121.994, 118.432, 114.7, 110.75, 106.512]
			CMAngles = np.array(CMAngles)
			CMAngles = CMAngles*(np.pi/180)
		else:
			print('No data for this energy')
			return 0
		
		
		
		if RingByRing:
		
			CMAnglesTheta = CMAngles*(180/np.pi)
			
			SolidAngleList = [round(2*np.pi*(np.cos(CMAngles[i+1]) - np.cos(CMAngles[i])), 3) for i in range(StartRing, StopRing + 1)]
			
			MidAngle = [round((CMAnglesTheta[i+1] + CMAnglesTheta[i])/2, 2) for i in range(StartRing, StopRing + 1)]
			
			return SolidAngleList, MidAngle
		else:
		
			SolidAngle = round(2*np.pi*(np.cos(CMAngles[StopRing+1]) - np.cos(CMAngles[StartRing])), 3)
			
			MidAngle = [round((CMAngles[i+1] + CMAngles[i])/2, 2) for i in range(StartRing, StopRing + 1)]
		
			return SolidAngle
		
	
	
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
	
	
	
	
	def ExSolidAngleCalc(self, BeamEnergy, StartRing, StopRing):
	
		
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
		else:
			print('No data for this energy.')
			return 0
			
		
		SolidAngle = round(2*np.pi*(np.cos(CMAngles[StopRing+1]) - np.cos(CMAngles[StartRing])), 3)
		
		return SolidAngle
		
		
		
		
		
		
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
			SatPeakCounts = [round(float(i.split(',', 2)[1]), 0) for i in lines[self.SatPeakRingStart:self.SatPeakRingStop+1]]
			SatPeakCountsError = [round(float(i.split(',', 3)[2]), 0) for i in lines[self.SatPeakRingStart:self.SatPeakRingStop+1]];
		
		
		
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
				SatPeakCountsScaleTo = [round(float(i.split(',', 2)[1]), 0) for i in lines[self.SatPeakRingStart:self.SatPeakRingStop+1]];
				SatPeakCountsErrorScaleTo = [round(float(i.split(',', 3)[2]), 0) for i in lines[self.SatPeakRingStart:self.SatPeakRingStop+1]];
				
				
				
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
			
			HydrogenAtoms = round((target_thickness/self.MethyleneMolarMass)*self.Mol*2, 3) 
			
			AvgBeamCurrent = round((AvgSatPeakCurrentTargetTime / (runtime*HydrogenAtoms*(10**(-27))))*(self.NeChargeState*self.ElectronCharge*10**12), 2)
				
			AvgBeamCurrentError = round((AvgSatPeakError / (runtime*HydrogenAtoms*(10**(-27))))*(self.NeChargeState*self.ElectronCharge*10**12), 2)
				
			print('Beam current from saturation peaks: ', AvgBeamCurrent, ' epa')
				
			print('Beam current error: ', AvgBeamCurrentError, ' epa')
				
				
			
		
		return AvgSatPeakCurrentTargetTime, AvgSatPeakError
		
		
class CSCalc:



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
			
		#print('Total number of alphas: ', sum(alpha_counts))
			
		return alpha_counts, error
		
		
		
		
		
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
		
		
		
	def GetTotalCS(self, BeamEnergy, StartRing, StopRing):
	
		if BeamEnergy == 137 or BeamEnergy == 141 or BeamEnergy == 143 or BeamEnergy == 152.4:
			
			DiffCS = self.GetDiffCS(BeamEnergy, StartRing, StopRing, CMFrame = True, SatPeakNorm=True)
			
		else:
			
			DiffCS = self.GetDiffCS(BeamEnergy, StartRing, StopRing, CMFrame = True, SatPeakNorm=False)
	

		Angles, MidPoints = BeamCurrentCalc().GetCMAngles(BeamEnergy)
		
		TotalCSList = [DiffCS[i] * np.sin(MidPoints[i]) * abs((Angles[i+1] - Angles[i])) for i in range(len(DiffCS))]
		
		TotalCS = 2*np.pi*sum(TotalCSList)
		
		return TotalCS
		
		
		
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
		
	
	
	def GetRingTotalCSError(self, BeamEnergy, StartRing, StopRing):
	
		
		if BeamEnergy == 137 or BeamEnergy == 141 or BeamEnergy == 143 or BeamEnergy == 152.4:
			
			DiffCSErrors = self.GetRingDiffCSError(BeamEnergy, StartRing, StopRing, SatPeakNorm = True)
			
		else:
			
			DiffCSErrors = self.GetRingDiffCSError(BeamEnergy, StartRing, StopRing, SatPeakNorm = False)
			
		
		SquaredDiffCSErrors = [DiffCSErrors[i]**2 for i in range(len(DiffCSErrors))]
		
		TotalCSError = np.sqrt(sum(SquaredDiffCSErrors))
		
		return TotalCSError
		
		
	# Well it seems we are again at the point we are saying fuck all to this beam current shit. It is what it is. I guess now its time to split the difference between the logbook and what I calculate. That's awesome becuase now I have to rely on the runtimes recorded in the ELOG to make cross section calculations. That's extra awesome because I still have no path for getting exact times. Not only was I not able to get the scalars file to print it before, but now I can't even SSH with my own login info. So fuck me I guess. It is what it is I guess. Just another stupid time waste of an excercise for the sake of it. Maybe one day this will all come to an end.

	
	def GetDiffCSFromBC(self, BeamEnergy, StartRing, StopRing):
	

		if BeamEnergy == 132:
			current = 14 # epa
			current_error = 3.5
		else:
			print('No data for this energy.')
			return 0
			
		
		target_thickness = BeamCurrentCalc().GetTargetThickness(BeamEnergy)
		
		runtime = BeamCurrentCalc().GetRuntime(BeamEnergy)	
			
		Alphas, AlphaError = self.GetAlphaCounts(BeamEnergy, StartRing, StopRing)
		
		RingEff = BeamCurrentCalc().SingleRingEff(BeamEnergy, StartRing, StopRing, ExcitedState = False, PrintEff = False, RingByRing = True)
		
		HydrogenAtoms = round((target_thickness/BeamCurrentCalc().MethyleneMolarMass)*BeamCurrentCalc().Mol*2, 3)
		
		BeamParticles = (current / (BeamCurrentCalc().NeChargeState*BeamCurrentCalc().ElectronCharge*10**12)) * runtime
		
		BeamParticlesError = (current_error / (BeamCurrentCalc().NeChargeState*BeamCurrentCalc().ElectronCharge*10**12)) * runtime
			
		###################################################################################
		
		# Calculate alpha cross section	
				
		DiffCS = [Alphas[i] / (BeamParticles * HydrogenAtoms*(10**(-27)) * 4*np.pi)/ RingEff[i]  for i in range(len(Alphas))] 
		
		###################################################################################
		
		# Calculate alpha error
		
		SquaredErrorFromAlphas = [(AlphaError[i] / (BeamParticles * HydrogenAtoms*(10**(-27)) * 4*np.pi)/ RingEff[i])**2 for i in range(len(Alphas))]
		
		SquaredCurrentError = [((Alphas[i] / ( (BeamParticles**2) * HydrogenAtoms * (10**(-27)) * 4 * np.pi) / RingEff[i])**2) * (BeamParticlesError**2) for i in range(len(Alphas))]
		
		ErrorDiffCS = [np.sqrt(SquaredErrorFromAlphas[i] + SquaredCurrentError[i]) for i in range(len(SquaredCurrentError))]
		
		###################################################################################
		
		

		
		return DiffCS, ErrorDiffCS
		

	def GetLabDiffCS(self, BeamEnergy, StartRing, StopRing):
	
		if BeamEnergy == 132:
			
			MidPointLabAngle = [149.15, 145.47, 141.79, 138.06, 134.31, 130.52, 126.68, 122.77, 118.78, 114.71]
			
			Jacobian = [1.4265, 1.4067, 1.3852, 1.3620, 1.3375, 1.3116, 1.2845, 1.2561, 1.2268, 1.1964]
			
		else:
		
			print('No data for this energy.')
			
			return 0
			
			
		CoMDiffCS, CoMErrorDiffCS = self.GetDiffCSFromBC(BeamEnergy, StartRing, StopRing)
		
		LabDiffCS = [round(CoMDiffCS[i]*Jacobian[i], 3) for i in range(len(CoMDiffCS))]
		
		LabDiffErrorCS = [round(CoMErrorDiffCS[i]*Jacobian[i], 3) for i in range(len(CoMErrorDiffCS))]
		
		return np.array(LabDiffCS), np.array(LabDiffErrorCS), MidPointLabAngle

		
class CSPlot:
		
		
	def GSDiffCSPlot(self, BeamEnergy, StartRing, StopRing, SatPeakNorm = False):
	
		SolidAngles, MidpointAngles = BeamCurrentCalc().SolidAngleCalc(BeamEnergy, StartRing, StopRing, RingByRing = True)
		
		AlphaDiffCS = CSCalc().GetDiffCS(BeamEnergy, StartRing, StopRing, CMFrame=True, SatPeakNorm = SatPeakNorm)
		
		DiffCSError = CSCalc().GetRingDiffCSError(BeamEnergy, StartRing, StopRing, SatPeakNorm = SatPeakNorm)
		
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

	
	def write_arrays_to_csv(self, filename, *arrays, headers=None):

		with open(filename, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile)

			if headers:
				writer.writerow(headers)

			for row in zip(*arrays):
				writer.writerow(row)

	
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

	
	def InputFile(self, BeamEnergy, StartRing, StopRing):
	
		
		LabDiffCS, LabErrorDiffCS, LabMidAngle = CSCalc().GetLabDiffCS(BeamEnergy, StartRing, StopRing)
		
		LabDiffCSBarn = LabDiffCS/1000
		
		LabErrorDiffCSBarn = LabErrorDiffCS/1000
		
		AZUREEnergy = round(((BeamEnergy - (BeamCurrentCalc().GetEnergyLoss(BeamEnergy)/2)) / BeamCurrentCalc().NeMass) * BeamCurrentCalc().HMass , 3)
			
		EnergyIndex = [AZUREEnergy for i in range(len(LabDiffCS))]
		
		CSFormatted = ['{:.3e}'.format(LabDiffCSBarn[x]) for x in range(len(LabDiffCSBarn))]
			
		CSErrorFormatted = ['{:.3e}'.format(LabErrorDiffCSBarn[x]) for x in range(len(LabErrorDiffCSBarn))]
			
		FilenameCSV = 'AZUREInputANL' + str(BeamEnergy) + 'MeV.csv'
		
		FilenameDat = 'AZUREInputANL' + str(BeamEnergy) + 'MeV.dat'
		
		CSVwriter().write_arrays_to_csv(FilenameCSV, EnergyIndex, LabMidAngle, CSFormatted, LabErrorDiffCSBarn)
		
		
			
		with open(FilenameDat, 'w') as wf:
			with open(FilenameCSV, 'r') as rf:
				[ wf.write('    '.join(row)+'\n') for row in csv.reader(rf)]
			wf.close()
			
		return 0 
			
