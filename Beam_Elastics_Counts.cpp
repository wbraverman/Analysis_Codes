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


int Beam_Elastics_Counts(int RunID1, int RunID2){

int GoodEvents;

char run1[80]; 
char run2[80]; 
char run3[80];
char CombinedRun[80];

char ring_both[80];
char ring_both_plot[80];
char plot_name[80];

char ring_both_cut[80];
char ring_both_plot_cut[80];
char plot_name_cut[80];

char sat_plot_name[80];
char ring_both_sat[80];
char ring_both_sat_plot[80];


//Search for runs with the name you want in your current directory (assuming you launch root in said directory)

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


TCanvas *c19 = new TCanvas("c19", "Ring Spectra (raw)", 500, 500);
c19->Divide(4,4);

TCanvas *c20 = new TCanvas("c20", "Ring Spectra (tac cut)", 500, 500);
c20->Divide(4,4);

TCanvas *c21 = new TCanvas("c21", "Ring Spectra Saturation Peak", 500, 500);
c21->Divide(4,4);

TH1F * raw_spec[16];
TH1F * cut_spec[16];
TH1F * sat_spec[16];

for (int i=0; i<16; i++){
    c19->cd(i+1);
    sprintf(ring_both, "r_num==%d", i);
    sprintf(ring_both_plot, "Si_r>>rnc%d(1000,0,70)", i);
    sprintf(plot_name, "rnc%d", i);
    ch.Draw(ring_both_plot, ring_both, "colz");
    raw_spec[i] = (TH1F*)(gDirectory->Get(plot_name));
    
    c20->cd(i+1);
    sprintf(ring_both_cut, "r_num==%d && tac_cut", i);
    sprintf(ring_both_plot_cut, "Si_r>>rtc%d(1000, 0, 70)", i);
    sprintf(plot_name_cut, "rtc%d",i);
    ch.Draw(ring_both_plot_cut, ring_both_cut, "colz");
    cut_spec[i] = (TH1F*)(gDirectory->Get(plot_name_cut));  
    
    c21->cd(i+1);
    sprintf(ring_both_sat, "r_num==%d", i);
    sprintf(ring_both_sat_plot, "Si_r>>rsp%d(150,50,60)", i);
    sprintf(sat_plot_name, "rsp%d", i);
    ch.Draw(ring_both_sat_plot, ring_both, "colz");
    sat_spec[i] = (TH1F*)(gDirectory->Get(sat_plot_name));
    
}

TFile *pf = new TFile("RingHistos.root", "RECREATE");

for(int i = 0; i<16; i++){
	raw_spec[i]->Write();
	cut_spec[i]->Write();
	sat_spec[i]->Write();
}

pf->Close();



return 0;
}
