// HOW TO
// 1. Set your custom function
// 2. change the parameter numbers so they're sequential
// 3. update the 'total' function to be whatever components you've chosen
// 4. Set your fitting range
// 5. make sure the histogram name matches to what you've drawn
// 6. Make sure the number of parameters in your CustomFunction is right
// 7. Set initial parameters, which are your guesses. Important ones here are the centroids of the gaussians.
// 8. Set the limits. Again, set the limit of the centroid to be sensible, most other ones can be broad.
// 9. For drawing, uncomment the components you used, changing the parameter numbers if necessary.
// 10. Change the parameter numbers as necessary for the integral output.



   void write_csv(std::string filename, std::vector<std::pair<std::string, std::vector<double>>> dataset){
    // Make a CSV file with one or more columns of integer values
    // Each column of data is represented by the pair <column name, column data>
    //   as std::pair<std::string, std::vector<int>>
    // The dataset is represented as a vector of these columns
    // Note that all columns should be the same size
    
    // Create an output filestream object
    std::ofstream myFile(filename);
    
    // Send column names to the stream
    for(int j = 0; j < dataset.size(); ++j)
    {
        myFile << dataset.at(j).first;
        if(j != dataset.size() - 1) myFile << ","; // No comma at end of line
    }
    myFile << "\n";
    
    // Send data to the stream
    for(int i = 0; i < dataset.at(0).second.size(); ++i)
    {
        for(int j = 0; j < dataset.size(); ++j)
        {
            myFile << dataset.at(j).second.at(i);
            if(j != dataset.size() - 1) myFile << ","; // No comma at end of line
        }
        myFile << "\n";
    }
    
    // Close the file
    myFile.close();
}



   Double_t CustomFunction(Double_t *x, Double_t *par)
   {
      Double_t xx = x[0];
       
      // gaus1
      Double_t arg1;
      arg1 = 0.5*(TMath::Power((xx-par[1]),2)/(TMath::Power(par[2],2)));
      Double_t gaus1 = ((par[0]/TMath::Sqrt(2*3.1415926)/par[2])*exp(-arg1));

      // gaus2
         Double_t arg2;
         arg2 = 0.5*(TMath::Power((xx-par[4]),2)/(TMath::Power(par[5],2)));
         Double_t gaus2 = ((par[3]/TMath::Sqrt(2*3.1415926)/par[5])*exp(-arg2));
      


      
        Double_t quadratic = par[6]+par[7]*xx+par[8]*TMath::Power(xx,2);
       // Double_t linear = par[7]*xx+par[6];
      
       // Double_t total = gaus1+linear;
       // Double_t total = gaus1+quadratic;
        Double_t total = gaus1+gaus2+quadratic;
       // Double_t total = gaus1+gaus2+linear;
       // Double_t total = gaus1 + gaus2;
   
       return total;
     
   }
   

   
   void DataFit()
   {
      
     TFile *f = new TFile("RingHistos.root", "READ");

     TH1F * raw_spec[16];
     TH1F * cut_spec[16];

     char raw_spec_plot[50];
     char rawPlotName[50];
     char function_name[50];
     
     char cutPlotName[50];
     char cut_spec_plot[50];
     char cut_function_name[50];

     TCanvas *rbc = new TCanvas("rbc", "Ring Spectra (raw)", 2000, 2000);
     rbc->Divide(4,4);
     /*
     TCanvas *rtac = new TCanvas("rtac", "Ring Spectra (tac_cut)", 2000, 2000);
     rtac->Divide(4,4);
     */
     for(int i=0; i<16; i++){
    	rbc->cd(i+1);
    	sprintf(rawPlotName, "rnc%d", i);
    	raw_spec[i] = (TH1F*)(gDirectory->Get(rawPlotName));
    	raw_spec[i]->Draw();
    	/*
    	rtac->cd(i+1);
    	sprintf(cutPlotName, "rtc%d", i);
    	cut_spec[i] = (TH1F*)(gDirectory->Get(cutPlotName));
    	cut_spec[i]->Draw();
    	*/
     }


std::vector<Double_t> ring_num, gs_particles, ex_particles, error1, error2;

	TF1 * function_array[16];
	
	Double_t xmax;
	Double_t xmin;
	
	for(int i=0; i<16;i++){
	sprintf(function_name, "f%d", i);
	switch(i){
		case 0:
		     xmin = 3.2;
     		     xmax = 8.0;
     		     break;
		case 1:
		     xmin = 3.4;
     		     xmax = 8.0;
     		     break;
		case 2:
		     xmin = 3.0;
     		     xmax = 8.0;
     		     break;
		case 3:
		     xmin = 3.0;
     		     xmax = 8.0;
     		     break;
		case 4:
		     xmin = 2.6;
     		     xmax = 8.0;
     		     break;
		case 5:
		     xmin = 2.8;
     		     xmax = 8.0;
     		     break;
		case 6:
		     xmin = 3.0;
     		     xmax = 8.0;
     		     break;
		case 7:
		     xmin = 3.0;
     		     xmax = 8.0;
     		     break;
		case 8:
		     xmin = 3.5;
     		     xmax = 8.0;
     		     break;
		case 9:
		     xmin = 3.4;
     		     xmax = 8.0;
     		     break;
		case 10:
		     xmin = 3.7;
     		     xmax = 8.0;
     		     break;
		case 11:
     		     break;
		case 12:
		     xmin = 4.2;
     		     xmax = 8.0;
     		     break;
		case 13:
		     xmin = 4.0;
     		     xmax = 8.0;
     		     break;
		case 14:
		     xmin = 3.9;
     		     xmax = 8.0;
     		     break;
		case 15:
		     xmin = 4.4;
     		     xmax = 8.0;
     		     break;
     	}
	
	function_array[i] = new TF1(function_name,CustomFunction,xmin,xmax,9);
	
	     /*Set initial parameters (a starting point for the minimisation function class)
 You must do this (Parameters 0-2 are the Area, Centroid and Sigma of the Gaussian
 and parameters 3-5 are the coefficients in   par[3]+par[4]*x+par[5]*x^2 */
 
       function_array[i]->SetParameter(0,1000); // gaus1
       function_array[i]->SetParameter(1,4.7);
       function_array[i]->SetParameter(2,0.15);
       function_array[i]->SetParameter(3,1000);    // gaus2
       function_array[i]->SetParameter(4,5.3);
       function_array[i]->SetParameter(5,0.15);
       function_array[i]->SetParameter(6,10); // quadratic
       function_array[i]->SetParameter(7,1);
       function_array[i]->SetParameter(8,0.5);
	
	
        /* Limit the range of values that can be used in fit (i.e. you know the area cannot
 be < 0 so don't let it. Otherwise ROOT will allow all sorts of crazy fits).
 BE AWARE: If the root fit starts complaining that you are *at limit* then you will
 need to start expanding the limits.*/
      
       function_array[i]->SetParLimits(0,0,50000);
       function_array[i]->SetParLimits(1,4.3,5.0);
       function_array[i]->SetParLimits(2,0,0.3);
       function_array[i]->SetParLimits(3,0,50000);
       function_array[i]->SetParLimits(4,5.0,6.0);
       function_array[i]->SetParLimits(5,0,0.3);
       function_array[i]->SetParLimits(6,0,3000);
       function_array[i]->SetParLimits(7,-1000,100);
       function_array[i]->SetParLimits(8,-100,100);
}
	

for(int i=0; i<16; i++){ 
	if (i!=11 /*&& i!=14*/){
		raw_spec[i]->Fit(function_array[i],"R,E,I");
		//cut_spec[i]->Fit(function_array[i],"R,E,I");
		
		

      	//uncomment for raw spectra
      	
      	Double_t area1 = (function_array[i]->GetParameter(0))/(raw_spec[i]->GetBinWidth(1));
      	Double_t area2 = (function_array[i]->GetParameter(3))/(raw_spec[i]->GetBinWidth(1));
      	Double_t errarea1 = (function_array[i]->GetParError(0))/(raw_spec[i]->GetBinWidth(1));
      	Double_t errarea2 = (function_array[i]->GetParError(3))/(raw_spec[i]->GetBinWidth(1));
      	
      	
      	// uncomment for cut spectra
      	/*
      	Double_t area1 = (function_array[i]->GetParameter(0))/(cut_spec[i]->GetBinWidth(1));
      	Double_t area2 = (function_array[i]->GetParameter(3))/(cut_spec[i]->GetBinWidth(1));
      	Double_t errarea1 = (function_array[i]->GetParError(0))/(cut_spec[i]->GetBinWidth(1));
      	Double_t errarea2 = (function_array[i]->GetParError(3))/(cut_spec[i]->GetBinWidth(1));
      	*/
    
      	cout << "Centroid1: " << function_array[i]->GetParameter(1) << " Error: " << function_array[i]->GetParError(1) << endl;
      	cout << "Area: " << area1 << " Error: " << errarea1 << endl << endl;
      	cout << "Centroid2: " << function_array[i]->GetParameter(4) << " Error: " << function_array[i]->GetParError(4) << endl;
      	cout << "Area: " << area2 << " Error: " << errarea2 << endl << endl; 
      	
      	ring_num.push_back(i*1.0);
      	gs_particles.push_back(area1);
      	ex_particles.push_back(area2);
      	error1.push_back(errarea1);
      	error2.push_back(errarea2);
      	  
      	}
   }
   
   std::vector<std::pair<std::string, std::vector<double>>> vals = {{"Ring Number", ring_num}, {"Ground State counts", gs_particles}, {"Error", error1}, {"Excited State counts", ex_particles}, {"Error", error2}};

   write_csv("Beam_Elastic_Counts_raw.csv", vals);
   //write_csv("Beam_Elastic_Counts_cut.csv", vals);

       
   }
