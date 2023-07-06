#include <iostream>
#include <fstream>
#include <math.h>
#include <vector>

#include <string.h>
#include <stdlib.h>
#include <cstdlib>
#include <unistd.h>
#include <ctype.h>
#include <stdio.h>
#include <time.h>
#include <istream>
#include <iomanip>
#include <cmath>
#include <sstream>

#include <TFile.h>
#include <TTree.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TROOT.h>
#include <TNtuple.h>
#include <TCanvas.h>
#include <TRint.h>
#include <TObjArray.h>
#include <TGraph.h>
#include <TH1.h>
#include <TH1D.h>
#include <TH2.h>
#include <TStyle.h>
#include <TMath.h>
#include <TList.h>
#include <TCutG.h>

#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include <TCutG.h>
#include <TCanvas.h>
#include <TH2.h>
#include <TROOT.h>
#include <ROOT/RDataFrame.hxx>
#include <TApplication.h>

using namespace std;
using namespace ROOT;

// function to check if file exists
inline bool exists_test2(const std::string& name) {   
    if (FILE *file = fopen(name.c_str(), "r")) {
        fclose(file);
        return true;
    } else {
        return false;
    }   
}

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


int PAlpha_Counts(int RunID1, int RunID2){

char run1[80]; 
char run2[80]; 
char run3[80];
char CombinedRun[80];

char ring_both[80];
char ring_both_plot[80];
char r_name[50];
char r_cut[100];
char plot_name[100];


TFile *cf = new TFile("cuts.root");
TCutG *tac_cut = (TCutG*)gROOT->FindObject("tac_cut");
TCutG *FvB = (TCutG*)gROOT->FindObject("FvB");
TCutG *blob = (TCutG*)gROOT->FindObject("blob");

sprintf(run1, "run%d.root", RunID1);
sprintf(run2, "run%d.root", RunID2);

sprintf(CombinedRun, "run%dtorun%d.root", RunID1, RunID2);

TFile *f = new TFile(CombinedRun, "RECREATE");

TChain ch("tree");

//Chain runs together
int i = RunID1;
while(i <= RunID2){
    sprintf(run3, "run%d.root", i);
  if (exists_test2(run3) ==true){
     ch.Add(run3);
     std::cout << i << "\n";
     i++;
  }
  else{
    std::cout << "File does not exist" << "\n";
    i++;
  }
}



TCanvas *c18 = new TCanvas("c18", "Ring Spectra (tac cut only)", 500, 500);
c18->Divide(4,4);


for (int i=0; i<16; i++){
    c18->cd(i+1);
    sprintf(ring_both, "r_num==%d && tac_cut", i);
    sprintf(ring_both_plot, "Si_r>>hrb%d(1000,0,70)", i);
    ch.Draw(ring_both_plot, ring_both, "colz");
}

TH1F * r_plots[16];

/*
for(int i=0; i<16; i++){
	sprintf(r_name, "r%d", i);
	r_plots[i] = (TH1F*)(gDirectory->Get(r_name));
}
*/
for(int i=0; i<16; i++){
	sprintf(plot_name, "Si_r>>r%d(1000,0,70)", i);
	if(i<4){
		sprintf(r_cut, "tac_cut && r_num==%d && Si_r>34 && Si_r<38", i);
		ch.Draw(plot_name, r_cut, "goff");
	}
	else if(i<8){
		sprintf(r_cut, "tac_cut && r_num==%d && Si_r>33 && Si_r<38", i);
		ch.Draw(plot_name, r_cut, "goff");
	}
	else{
		sprintf(r_cut, "tac_cut && r_num==%d && Si_r>32 && Si_r<38", i);
		ch.Draw(plot_name, r_cut, "goff");
	}
	sprintf(r_name, "r%d", i);
	r_plots[i] = (TH1F*)(gDirectory->Get(r_name));
}

std::vector<Double_t> ring_num, counts, error;	


for(int i=0; i<16; i++){
	ring_num.push_back(i*1.0);
	counts.push_back(r_plots[i]->GetEntries());
	error.push_back(sqrt(r_plots[i]->GetEntries()));	
}

std::vector<std::pair<std::string, std::vector<double>>> vals = {{"Ring Number", ring_num}, {"Counts", counts}, {"Error", error}};

write_csv("PAlpha_Counts.csv", vals);



return 0;
}
