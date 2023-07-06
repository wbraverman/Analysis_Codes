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
#include <TTreeReaderArray.h>

#include <TFile.h>
#include <TTree.h>
#include <TChain.h>
#include <TCutG.h>
#include <TCanvas.h>
#include <TH2.h>
#include <TROOT.h>
#include <TString.h>

#include <TGraphPolar.h>

#include <chrono>
using namespace std::chrono;

// function to check if file exists
inline bool exists_test3(const std::string& name) {   
    if (FILE *file = fopen(name.c_str(), "r")) {
        fclose(file);
        return true;
    } else {
        return false;
    }   
}

void write_csv(std::string filename, std::vector<std::pair<std::string, std::vector<int>>> dataset){
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


int SiliconCSV(int RunID1, int RunID2){

auto start = high_resolution_clock::now();

char run1[80]; 
char run2[80]; 
char run3[80];
char CombinedRun[80];


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
  if (exists_test3(run3) ==true){
     ch.Add(run3);
     std::cout << i << "\n";
     i++;
  }
  else{
    std::cout << "File does not exist" << "\n";
    i++;
  }
}

std::vector<Int_t> ring_num, wedge_num, num_counts;

TH1F * RWplot[256];
char wedge_plot_name[150];
char wedge_cut_plot[150];
char wedge_cut[150];



for(int i=0; i<16; i++){
    cout<<Form("i = %d", i)<<endl;
    for(int j=0; j<16; j++){
        cout<<Form("j = %d",j)<<endl;
        sprintf(wedge_cut, "r_num==%d && tac_cut && w_num==%d", i, j); //FvB cut taken out for now.
        sprintf(wedge_cut_plot, "Si_r>>r%dw%d(1000,0,70)",i,j);
        sprintf(wedge_plot_name, "r%dw%d", i, j);
        ch.Draw(wedge_cut_plot, wedge_cut, "goff");
        RWplot[j + 16*i] = (TH1F*)(gDirectory->Get(wedge_plot_name));
        ring_num.push_back(i);
        wedge_num.push_back(j);
        num_counts.push_back(RWplot[j + 16*i] -> GetEntries());   
    }
}

TFile *pf = new TFile("RingWedgePixel.root", "RECREATE");

for(int i = 0; i<16; i++){
	RWplot[i]->Write();
}

pf->Close();

auto stop = high_resolution_clock::now();
auto duration = duration_cast<microseconds>(stop - start);
cout << duration.count() << endl;    

std::vector<std::pair<std::string, std::vector<int>>> vals = {{"Rings", ring_num}, {"Wedges", wedge_num}, {"Counts", num_counts}};

write_csv("rings_wedges.csv", vals);




return 0;
}

int main(int argc, char** argv){

  int num1, num2; 
  sscanf (argv[1],"%d",&num1);
  sscanf (argv[2],"%d",&num2);
  
  SiliconCSV(num1, num2);
  return 0;
}
