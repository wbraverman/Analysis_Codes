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

using namespace std;


// function to check if file exists
inline bool exists_test1(const std::string& name) {   
    if (FILE *file = fopen(name.c_str(), "r")) {
        fclose(file);
        return true;
    } else {
        return false;
    }   
}


int Make_Cuts(int RunID1, int RunID2){

int GoodEvents;

char run1[80]; 
char run2[80]; 
char run3[80];
char CombinedRun[80];

char ring_cut[100];
char list_num[100];

char str1[150];
char str2[150];
char str3[150];
char str4[150];
char str5[150];
char str6[150];
char plot_name[100];

//Search for runs with the name you want in your current directory (assuming you launch root in said directory)
sprintf(run1, "run%d.root", RunID1);
sprintf(run2, "run%d.root", RunID2);

sprintf(CombinedRun, "run%dtorun%d.root", RunID1, RunID2);

TFile *f = new TFile(CombinedRun, "RECREATE");

TChain ch("tree");


//Chain runs together
int i = RunID1;
while(i <= RunID2){
	sprintf(run3, "run%d.root", i);
  if (exists_test1(run3) ==true){
	 ch.Add(run3);
     std::cout << i << "\n";
     i++;
  }
  else{
    std::cout << "File does not exist" << "\n";
    i++;
  }
}


TCanvas *c1 = new TCanvas("c1", "A4 vs. TAC", 0,0,500,500);
//TH2F *h = new TH2F("h", "",1000,50,4000,1000,0,5000);

//Plot A4 measurements vs. tac measurements (good plot for cutting data)
ch.Draw("A4:tac>>h(1000,50,4000,1000,0,5000)","","colz");




TCanvas *c13 = new TCanvas("c13", "A23 vs. A67", 0, 0, 500, 500);
gPad->SetLogy();
ch.Draw("(A3-A2)*1000/(A3+A2)>>pos(800,-1000,1000)","A3>200 && A2>200","");
TH1F *A23_pos = (TH1F*)(gDirectory->Get("pos"));
A23_pos -> SetLineColor(2);



TCanvas *c16 = new TCanvas("c16", "A4", 500, 500);
gPad->SetLogy();
ch.Draw("A4*100>>mon(125,500,15000)", "","colz");



if (exists_test1("cuts.root")){
    TFile *cf = new TFile("cuts.root");
    TCutG *tac_cut = (TCutG*)gROOT->FindObject("tac_cut");
    TCutG *FvB = (TCutG*)gROOT->FindObject("FvB");
    TCutG *blob = (TCutG*)gROOT->FindObject("blob");

    //double integral = FvB->IntegralHist(h3);
    
    c1->cd();
    tac_cut->SetLineColor(2);
    tac_cut->Draw("same");
    c1->Modified();
    c1->Update();
    sprintf(str1,"/mnt/c/Users/wbrav/OneDrive/Desktop/20Ne_root_files/ANL/data/Analysis/new_sort/141MeV/PAlpha/pics/run%d-to-run%da_tac_cut.png",RunID1,RunID2);
    c1->SaveAs(str1);
    
    TCanvas *c6 = new TCanvas("Ring signal vs. Wedge signal", "Ring Energy vs. Wedge Energy",500,500);
    gPad->SetLogz();
    ch.Draw("Si_r:Si_w>>h3(1000, 0, 70, 1000, 0, 70)", "tac_cut", "colz");

    c13->cd();
    ch.Draw("(A3-A2)*1000/(A3+A2)>>pos_coinc(800,-1000,1000)","A3>200 && A2>200 && tac_cut","");
    A23_pos->Draw("same");
    gPad->SetLogy();
    c13->Modified();
    c13->Update();

    sprintf(str2,"/mnt/c/Users/wbrav/OneDrive/Desktop/20Ne_root_files/ANL/data/Analysis/new_sort/141MeV/PAlpha/pics/run%d_to_run%d_position.png",RunID1,RunID2);
    c13->SaveAs(str2);

    if (FvB != nullptr){

        
        c6->cd();
        FvB->Draw("same");
        c6->Modified();
        c6->Update();
        sprintf(str3,"/mnt/c/Users/wbrav/OneDrive/Desktop/20Ne_root_files/ANL/data/Analysis/new_sort/141MeV/PAlpha/pics/run%d-to-run%da_FvB.png",RunID1,RunID2);
        c6->SaveAs(str3);
    }
}

TCanvas *c19 = new TCanvas("c19", "ring num vs. wedge num", 500, 500);
gPad->SetLogz();
ch.Draw("r_num:w_num>>loc(16, 0, 16, 16, 0, 16)", "tac_cut && FvB", "colz");
sprintf(str4, "/mnt/c/Users/wbrav/OneDrive/Desktop/20Ne_root_files/ANL/data/Analysis/new_sort/141MeV/PAlpha/pics/mapping_run%d_to_run%d.png", RunID1, RunID2);
c19->SaveAs(str4);


return 0;
}


/*int main(int argc, char** argv){

  int num1, num2; 
  sscanf (argv[1],"%d",&num1);
  sscanf (argv[2],"%d",&num2);
  
  Make_Cuts(num1, num2);
  return 0;
}*/