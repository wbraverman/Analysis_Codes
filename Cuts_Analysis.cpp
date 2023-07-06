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


int Cuts_Analysis(int RunID1, int RunID2){

int GoodEvents;

char run1[80]; 
char run2[80]; 
char run3[80];
char CombinedRun[80];

char ring[80];
char ring_plot[80];

char ring_tac[80];
char ring_tac_plot[80];

char ring_fvb[80];
char ring_fvb_plot[80];

char ring_both[80];
char ring_both_plot[80];

char wedge_both[100];
char wedge_both_plot[100];

char ring_grouped_cut[100];
char ring_grouped_plot[100];

char wedge_num[80];
char wedge[80];

char str5[150];
char str6[150];
char str7[150];
char str8[150];
char str9[150];
char str10[150];
char plot_name[100];

char wedge_cut[100];

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



TCanvas *c9 = new TCanvas("c9", "Ring Number vs. Energy (Cuts)", 0, 0, 1000, 500);
c9->Divide(4,1);

c9->cd(1);

TH2F *h4 = new TH2F("h4", "Ring Number vs. Energy (no cut)", 1000, 0, 70, 16, 0, 16);
gPad->SetLogz();
ch.Draw("r_num:Si_r>>h4", "", "colz");

c9->cd(2);

TH2F *h5 = new TH2F("h5", "Ring Number vs Energy (tac cut)", 1000, 0, 70, 16, 0, 16);
gPad->SetLogz();
ch.Draw("r_num:Si_r>>h5", "tac_cut", "colz");

c9->cd(3);

TH2F *h6 = new TH2F("h6", "Ring Number vs Energy (FvB cut)", 1000, 0, 70, 16, 0, 16);
gPad->SetLogz();
ch.Draw("r_num:Si_r>>h6", "FvB", "colz");


c9->cd(4);

TH2F *h7 = new TH2F("h7", "Ring Number vs. Energy (both cuts)", 1000, 0, 70, 16, 0, 16);
gPad->SetLogz();
ch.Draw("r_num:Si_r>>h7", "FvB && tac_cut", "colz");

sprintf(str5,"/mnt/c/Users/wbrav/OneDrive/Desktop/20Ne_root_files/ANL/data/Analysis/new_sort/141MeV/PAlpha/pics/run%d-to-run%da_2D_ring_spectra.png",RunID1,RunID2);
c9->SaveAs(str5);

TCanvas *c18 = new TCanvas("c18", "Ring Spectra (tac cut only)", 500, 500);
c18->Divide(4,4);


for (int i=0; i<16; i++){
    c18->cd(i+1);
    sprintf(ring_both, "r_num==%d && tac_cut", i);
    sprintf(ring_both_plot, "Si_r>>hrb%d(1000,0,70)", i);
    ch.Draw(ring_both_plot, ring_both, "colz");
}

sprintf(str6,"/mnt/c/Users/wbrav/OneDrive/Desktop/20Ne_root_files/ANL/data/Analysis/new_sort/141MeV/PAlpha/pics/run%d-to-run%da_1D_ring_spectra.png",RunID1,RunID2);
c18->SaveAs(str6);


TH1F * pMult[16];
TH1F * pMult_add[8];
TH1F * pMult_final[4];


for(int i=0; i<16; i++){
    sprintf(plot_name, "hrb%d", i);
    pMult[i] = (TH1F*)(gDirectory->Get(plot_name));
}





TCanvas *c14 = new TCanvas("c14", "grouped rings", 500, 500);
c14->Divide(2,2);

char add_title[100];
char add_name[100];
char final_title[100];
char final_name[100];

int k=0;
for(int i=0; i<8; i++){
    sprintf(add_title, "pMult_%d and pMult_%d", 2*i, 2*i + 1 );
    sprintf(add_name, "ring %d and ring %d", 2*i, 2*i+1);
    TH1F * dummy1 = new TH1F("dummy1 title", "dummy1 name", 1000, 0, 70);
    dummy1->Add(pMult[2*i], pMult[2*i + 1]);
    pMult_add[i] = new TH1F(add_title, add_name, 1000, 0, 70);
    pMult_add[i]->Add(dummy1);
    delete dummy1;
    if(i%2!=0){
        sprintf(final_title, "rings %d - %d", 4*k + 1, 4*k + 4);
        sprintf(final_name, "ring %d to ring %d", 4*k + 1, 4*k + 4);
        TH1F * dummy2 = new TH1F("dummy2 title", "dummy2 name", 1000, 0, 70);
        dummy2->Add(pMult_add[i-1], pMult_add[i]);
        pMult_final[k] = new TH1F(final_title, final_name, 1000, 0, 70);
        pMult_final[k]->Add(dummy2);
        delete dummy2;
        k=k+1;
    }
}

for(int i=0; i<4; i++){
    c14->cd(i+1);
    pMult_final[i]->Draw();
}

sprintf(str7, "/mnt/c/Users/wbrav/OneDrive/Desktop/20Ne_root_files/ANL/data/Analysis/new_sort/141MeV/PAlpha/pics/Added_rings_run%d_to_run%d.png", RunID1, RunID2);
c14->SaveAs(str7);



TCanvas *c17 = new TCanvas("c17", "Wedge Number vs. Energy (Cuts)", 0, 0, 1000, 500);
c17->Divide(4,1);

c17->cd(1);

TH2F *h8 = new TH2F("h8", "Wedge Number vs. Energy (no cut)", 1000, 0, 70, 16, 0, 16);
gPad->SetLogz();
ch.Draw("w_num:Si_w>>h8", "", "colz");

c17->cd(2);

TH2F *h9 = new TH2F("h9", "Wedge Number vs Energy (tac cut)", 1000, 0, 70, 16, 0, 16);
gPad->SetLogz();
ch.Draw("w_num:Si_w>>h9", "tac_cut", "colz");

c17->cd(3);

TH2F *h10 = new TH2F("h10", "Wedge Number vs Energy (FvB cut)", 1000, 0, 70, 16, 0, 16);
gPad->SetLogz();
ch.Draw("w_num:Si_w>>h10", "FvB", "colz");


c17->cd(4);

TH2F *h11 = new TH2F("h11", "Wedge Number vs. Energy (both cuts)", 1000, 0, 70, 16, 0, 16);
gPad->SetLogz();
ch.Draw("w_num:Si_w>>h11", "FvB && tac_cut", "colz");

sprintf(str8, "/mnt/c/Users/wbrav/OneDrive/Desktop/20Ne_root_files/ANL/data/Analysis/new_sort/141MeV/PAlpha/pics/2D_wedge_spectra_run%d_to_run%d.png", RunID1, RunID2);
c17->SaveAs(str8);


TCanvas *c15 = new TCanvas("c15", "Wedge Spectra (tac cut only)", 500, 500);
c15->Divide(4,4);


for (int i=0; i<16; i++){
    c15->cd(i+1);
    sprintf(wedge_both, "w_num==%d && tac_cut", i);
    sprintf(wedge_both_plot, "Si_w>>hwb%d(1000,0,70)", i);
    gPad->SetLogy();
    ch.Draw(wedge_both_plot, wedge_both, "colz");
}

sprintf(str9, "/mnt/c/Users/wbrav/OneDrive/Desktop/20Ne_root_files/ANL/data/Analysis/new_sort/141MeV/PAlpha/pics/1D_wedge_spectra_run%d_to_run%d.png", RunID1, RunID2);
c15->SaveAs(str9);



TCanvas *c12 = new TCanvas("c12", "Ring Spectra (both cuts)", 500, 500);
c12->Divide(4,4);


ch.Draw("Si_r>>rne0(1000,0,70)", "r_num==0 && tac_cut && FvB && Si_r > 37 && Si_r < 39", "goff" );
ch.Draw("Si_r>>rng0(1000,0,70)", "r_num==0 && tac_cut && FvB && Si_r > 39 && Si_r < 41", "goff" );
ch.Draw("Si_r>>rn0(1000,0,70)", "r_num==0 && tac_cut && FvB", "goff");

TH1F *rne0 = (TH1F*)(gDirectory->Get("rne0"));
TH1F *rng0 = (TH1F*)(gDirectory->Get("rng0"));
TH1F *rn0 = (TH1F*)(gDirectory->Get("rn0"));

rne0 -> SetLineColor(4);
rng0 -> SetLineColor(2);
rn0 -> SetLineColor(1);

c12->cd(1);
rn0->Draw();
rng0->Draw("same");
rne0->Draw("same");

auto legend0 = new TLegend(0.1,0.7,0.48,0.9);
legend0->AddEntry(rn0,"All Counts","l");
legend0->AddEntry(rng0,"Ground State","l");
legend0->AddEntry(rne0,"Excited State","l");
legend0->Draw();

ch.Draw("Si_r>>rne1(1000,0,70)", "r_num==1 && tac_cut && FvB && Si_r > 37.5 && Si_r < 39.5", "goff" );
ch.Draw("Si_r>>rng1(1000,0,70)", "r_num==1 && tac_cut && FvB && Si_r > 39.5 && Si_r < 41.5", "goff" );
ch.Draw("Si_r>>rn1(1000,0,70)", "r_num==1 && tac_cut && FvB", "goff");

TH1F *rne1 = (TH1F*)(gDirectory->Get("rne1"));
TH1F *rng1 = (TH1F*)(gDirectory->Get("rng1"));
TH1F *rn1 = (TH1F*)(gDirectory->Get("rn1"));

rne1 -> SetLineColor(4);
rng1 -> SetLineColor(2);
rn1 -> SetLineColor(1);

c12->cd(2);
rn1->Draw();
rng1->Draw("same");
rne1->Draw("same");

auto legend1 = new TLegend(0.1,0.7,0.48,0.9);
legend1->AddEntry(rn1,"All Counts","l");
legend1->AddEntry(rng1,"Ground State","l");
legend1->AddEntry(rne1,"Excited State","l");
legend1->Draw();

ch.Draw("Si_r>>rne2(1000,0,70)", "r_num==2 && tac_cut && FvB && Si_r > 37.5 && Si_r < 39.5", "goff" );
ch.Draw("Si_r>>rng2(1000,0,70)", "r_num==2 && tac_cut && FvB && Si_r > 39.5 && Si_r < 41.5", "goff" );
ch.Draw("Si_r>>rn2(1000,0,70)", "r_num==2 && tac_cut && FvB", "goff");

TH1F *rne2 = (TH1F*)(gDirectory->Get("rne2"));
TH1F *rng2 = (TH1F*)(gDirectory->Get("rng2"));
TH1F *rn2 = (TH1F*)(gDirectory->Get("rn2"));

rne2 -> SetLineColor(4);
rng2 -> SetLineColor(2);
rn2 -> SetLineColor(1);

c12->cd(3);
rn2->Draw();
rng2->Draw("same");
rne2->Draw("same");

auto legend2 = new TLegend(0.1,0.7,0.48,0.9);
legend2->AddEntry(rn2,"All Counts","l");
legend2->AddEntry(rng2,"Ground State","l");
legend2->AddEntry(rne2,"Excited State","l");
legend2->Draw();

ch.Draw("Si_r>>rne3(1000,0,70)", "r_num==3 && tac_cut && FvB && Si_r > 37.5 && Si_r < 39.5", "goff" );
ch.Draw("Si_r>>rng3(1000,0,70)", "r_num==3 && tac_cut && FvB && Si_r > 39.5 && Si_r < 41.5", "goff" );
ch.Draw("Si_r>>rn3(1000,0,70)", "r_num==3 && tac_cut && FvB", "goff");

TH1F *rne3 = (TH1F*)(gDirectory->Get("rne3"));
TH1F *rng3 = (TH1F*)(gDirectory->Get("rng3"));
TH1F *rn3 = (TH1F*)(gDirectory->Get("rn3"));

rne3 -> SetLineColor(4);
rng3 -> SetLineColor(2);
rn3 -> SetLineColor(1);

c12->cd(4);
rn3->Draw();
rng3->Draw("same");
rne3->Draw("same");

auto legend3 = new TLegend(0.1,0.7,0.48,0.9);
legend3->AddEntry(rn3,"All Counts","l");
legend3->AddEntry(rng3,"Ground State","l");
legend3->AddEntry(rne3,"Excited State","l");
legend3->Draw();

ch.Draw("Si_r>>rne4(1000,0,70)", "r_num==4 && tac_cut && FvB && Si_r > 36.5 && Si_r < 38.5", "goff" );
ch.Draw("Si_r>>rng4(1000,0,70)", "r_num==4 && tac_cut && FvB && Si_r > 38.5 && Si_r < 40.5", "goff" );
ch.Draw("Si_r>>rn4(1000,0,70)", "r_num==4 && tac_cut && FvB", "goff");

TH1F *rne4 = (TH1F*)(gDirectory->Get("rne4"));
TH1F *rng4 = (TH1F*)(gDirectory->Get("rng4"));
TH1F *rn4 = (TH1F*)(gDirectory->Get("rn4"));

rne4 -> SetLineColor(4);
rng4 -> SetLineColor(2);
rn4 -> SetLineColor(1);

c12->cd(5);
rn4->Draw();
rng4->Draw("same");
rne4->Draw("same");

auto legend4 = new TLegend(0.1,0.7,0.48,0.9);
legend4->AddEntry(rn4,"All Counts","l");
legend4->AddEntry(rng4,"Ground State","l");
legend4->AddEntry(rne4,"Excited State","l");
legend4->Draw();

ch.Draw("Si_r>>rne5(1000,0,70)", "r_num==5 && tac_cut && FvB && Si_r > 37.25 && Si_r < 39.25", "goff" );
ch.Draw("Si_r>>rng5(1000,0,70)", "r_num==5 && tac_cut && FvB && Si_r > 39.25 && Si_r < 41.25", "goff" );
ch.Draw("Si_r>>rn5(1000,0,70)", "r_num==5 && tac_cut && FvB", "goff");

TH1F *rne5 = (TH1F*)(gDirectory->Get("rne5"));
TH1F *rng5 = (TH1F*)(gDirectory->Get("rng5"));
TH1F *rn5 = (TH1F*)(gDirectory->Get("rn5"));

rne5 -> SetLineColor(4);
rng5 -> SetLineColor(2);
rn5 -> SetLineColor(1);

c12->cd(6);
rn5->Draw();
rng5->Draw("same");
rne5->Draw("same");

auto legend5 = new TLegend(0.1,0.7,0.48,0.9);
legend5->AddEntry(rn5,"All Counts","l");
legend5->AddEntry(rng5,"Ground State","l");
legend5->AddEntry(rne5,"Excited State","l");
legend5->Draw();

ch.Draw("Si_r>>rne6(1000,0,70)", "r_num==6 && tac_cut && FvB && Si_r > 35.75 && Si_r < 37.75", "goff" );
ch.Draw("Si_r>>rng6(1000,0,70)", "r_num==6 && tac_cut && FvB && Si_r > 37.75 && Si_r < 39.75", "goff" );
ch.Draw("Si_r>>rn6(1000,0,70)", "r_num==6 && tac_cut && FvB", "goff");

TH1F *rne6 = (TH1F*)(gDirectory->Get("rne6"));
TH1F *rng6 = (TH1F*)(gDirectory->Get("rng6"));
TH1F *rn6 = (TH1F*)(gDirectory->Get("rn6"));

rne6 -> SetLineColor(4);
rng6 -> SetLineColor(2);
rn6 -> SetLineColor(1);

c12->cd(7);
rn6->Draw();
rng6->Draw("same");
rne6->Draw("same");

auto legend6 = new TLegend(0.1,0.7,0.48,0.9);
legend6->AddEntry(rn6,"All Counts","l");
legend6->AddEntry(rng6,"Ground State","l");
legend6->AddEntry(rne6,"Excited State","l");
legend6->Draw();

ch.Draw("Si_r>>rne7(1000,0,70)", "r_num==7 && tac_cut && FvB && Si_r > 36 && Si_r < 38", "goff" );
ch.Draw("Si_r>>rng7(1000,0,70)", "r_num==7 && tac_cut && FvB && Si_r > 38 && Si_r < 40", "goff" );
ch.Draw("Si_r>>rn7(1000,0,70)", "r_num==7 && tac_cut && FvB", "goff");

TH1F *rne7 = (TH1F*)(gDirectory->Get("rne7"));
TH1F *rng7 = (TH1F*)(gDirectory->Get("rng7"));
TH1F *rn7 = (TH1F*)(gDirectory->Get("rn7"));

rne7 -> SetLineColor(4);
rng7 -> SetLineColor(2);
rn7 -> SetLineColor(1);

c12->cd(8);
rn7->Draw();
rng7->Draw("same");
rne7->Draw("same");

auto legend7 = new TLegend(0.1,0.7,0.48,0.9);
legend7->AddEntry(rn7,"All Counts","l");
legend7->AddEntry(rng7,"Ground State","l");
legend7->AddEntry(rne7,"Excited State","l");
legend7->Draw();

ch.Draw("Si_r>>rne8(1000,0,70)", "r_num==8 && tac_cut && FvB && Si_r > 35.25 && Si_r < 37.25", "goff" );
ch.Draw("Si_r>>rng8(1000,0,70)", "r_num==8 && tac_cut && FvB && Si_r > 37.25 && Si_r < 39.25", "goff" );
ch.Draw("Si_r>>rn8(1000,0,70)", "r_num==8 && tac_cut && FvB", "goff");

TH1F *rne8 = (TH1F*)(gDirectory->Get("rne8"));
TH1F *rng8 = (TH1F*)(gDirectory->Get("rng8"));
TH1F *rn8 = (TH1F*)(gDirectory->Get("rn8"));

rne8 -> SetLineColor(4);
rng8 -> SetLineColor(2);
rn8 -> SetLineColor(1);

c12->cd(9);
rn8->Draw();
rng8->Draw("same");
rne8->Draw("same");

auto legend8 = new TLegend(0.1,0.7,0.48,0.9);
legend8->AddEntry(rn8,"All Counts","l");
legend8->AddEntry(rng8,"Ground State","l");
legend8->AddEntry(rne8,"Excited State","l");
legend8->Draw();

ch.Draw("Si_r>>rne9(1000,0,70)", "r_num==9 && tac_cut && FvB && Si_r > 35.2 && Si_r < 37.2", "goff" );
ch.Draw("Si_r>>rng9(1000,0,70)", "r_num==9 && tac_cut && FvB && Si_r > 37.4 && Si_r < 39.4", "goff" );
ch.Draw("Si_r>>rn9(1000,0,70)", "r_num==9 && tac_cut && FvB", "goff");

TH1F *rne9 = (TH1F*)(gDirectory->Get("rne9"));
TH1F *rng9 = (TH1F*)(gDirectory->Get("rng9"));
TH1F *rn9 = (TH1F*)(gDirectory->Get("rn9"));

rne9 -> SetLineColor(4);
rng9 -> SetLineColor(2);
rn9 -> SetLineColor(1);

c12->cd(10);
rn9->Draw();
rng9->Draw("same");
rne9->Draw("same");

auto legend9 = new TLegend(0.1,0.7,0.48,0.9);
legend9->AddEntry(rn9,"All Counts","l");
legend9->AddEntry(rng9,"Ground State","l");
legend9->AddEntry(rne9,"Excited State","l");
legend9->Draw();


ch.Draw("Si_r>>rne10(1000,0,70)", "r_num==10 && tac_cut && FvB && Si_r > 31 && Si_r < 33", "goff" );
ch.Draw("Si_r>>rng10(1000,0,70)", "r_num==10 && tac_cut && FvB && Si_r > 33 && Si_r < 35", "goff" );
ch.Draw("Si_r>>rn10(1000,0,70)", "r_num==10 && tac_cut && FvB", "goff");

TH1F *rne10 = (TH1F*)(gDirectory->Get("rne10"));
TH1F *rng10 = (TH1F*)(gDirectory->Get("rng10"));
TH1F *rn10 = (TH1F*)(gDirectory->Get("rn10"));

rne10 -> SetLineColor(4);
rng10 -> SetLineColor(2);
rn10 -> SetLineColor(1);

c12->cd(11);
rn10->Draw();
rng10->Draw("same");
rne10->Draw("same");

auto legend10 = new TLegend(0.1,0.7,0.48,0.9);
legend10->AddEntry(rn10,"All Counts","l");
legend10->AddEntry(rng10,"Ground State","l");
legend10->AddEntry(rne10,"Excited State","l");
legend10->Draw();

c12->cd(12);
ch.Draw("Si_r>>rn11(1000,0,70)", "r_num==11 && tac_cut && FvB", "");


ch.Draw("Si_r>>rne12(1000,0,70)", "r_num==12 && tac_cut && FvB && Si_r > 32 && Si_r < 34", "goff" );
ch.Draw("Si_r>>rng12(1000,0,70)", "r_num==12 && tac_cut && FvB && Si_r > 34 && Si_r < 36", "goff" );
ch.Draw("Si_r>>rn12(1000,0,70)", "r_num==12 && tac_cut && FvB", "goff");

TH1F *rne12 = (TH1F*)(gDirectory->Get("rne12"));
TH1F *rng12 = (TH1F*)(gDirectory->Get("rng12"));
TH1F *rn12 = (TH1F*)(gDirectory->Get("rn12"));

rne12 -> SetLineColor(4);
rng12 -> SetLineColor(2);
rn12 -> SetLineColor(1);

c12->cd(13);
rn12->Draw();
rng12->Draw("same");
rne12->Draw("same");

auto legend12 = new TLegend(0.1,0.7,0.48,0.9);
legend12->AddEntry(rn12,"All Counts","l");
legend12->AddEntry(rng12,"Ground State","l");
legend12->AddEntry(rne12,"Excited State","l");
legend12->Draw();


//ch.Draw("Si_r>>rne13(1000,0,70)", "r_num==13 && tac_cut && FvB && Si_r > 32 && Si_r < 34", "goff" );
//ch.Draw("Si_r>>rng13(1000,0,70)", "r_num==13 && tac_cut && FvB && Si_r > 34 && Si_r < 36", "goff" );
ch.Draw("Si_r>>rn13(1000,0,70)", "r_num==13 && tac_cut && FvB", "goff");

//TH1F *rne13 = (TH1F*)(gDirectory->Get("rne13"));
//TH1F *rng13 = (TH1F*)(gDirectory->Get("rng13"));
TH1F *rn13 = (TH1F*)(gDirectory->Get("rn13"));

//rne13 -> SetLineColor(4);
//rng13 -> SetLineColor(2);
rn13 -> SetLineColor(1);

c12->cd(14);
rn13->Draw();
//rng13->Draw("same");
//rne13->Draw("same");

auto legend13 = new TLegend(0.1,0.7,0.48,0.9);
legend13->AddEntry(rn13,"All Counts","l");
//legend13->AddEntry(rng13,"Ground State","l");
//legend13->AddEntry(rne13,"Excited State","l");
legend13->Draw();

//ch.Draw("Si_r>>rne14(1000,0,70)", "r_num==14 && tac_cut && FvB && Si_r > 32 && Si_r < 34", "goff" );
//ch.Draw("Si_r>>rng14(1000,0,70)", "r_num==14 && tac_cut && FvB && Si_r > 34 && Si_r < 36", "goff" );
ch.Draw("Si_r>>rn14(1000,0,70)", "r_num==14 && tac_cut && FvB", "goff");

//TH1F *rne14 = (TH1F*)(gDirectory->Get("rne14"));
//TH1F *rng14 = (TH1F*)(gDirectory->Get("rng14"));
TH1F *rn14 = (TH1F*)(gDirectory->Get("rn14"));

//rne14 -> SetLineColor(4);
//rng14 -> SetLineColor(2);
rn14 -> SetLineColor(1);

c12->cd(15);
rn14->Draw();
//rng14->Draw("same");
//rne14->Draw("same");

auto legend14 = new TLegend(0.1,0.7,0.48,0.9);
legend14->AddEntry(rn14,"All Counts","l");
//legend14->AddEntry(rng14,"Ground State","l");
//legend14->AddEntry(rne14,"Excited State","l");
legend14->Draw();


//ch.Draw("Si_r>>rne15(1000,0,70)", "r_num==15 && tac_cut && FvB && Si_r > 32 && Si_r < 34", "goff" );
//ch.Draw("Si_r>>rng15(1000,0,70)", "r_num==15 && tac_cut && FvB && Si_r > 34 && Si_r < 36", "goff" );
ch.Draw("Si_r>>rn15(1000,0,70)", "r_num==15 && tac_cut && FvB", "goff");

//TH1F *rne15 = (TH1F*)(gDirectory->Get("rne15"));
//TH1F *rng15 = (TH1F*)(gDirectory->Get("rng15"));
TH1F *rn15 = (TH1F*)(gDirectory->Get("rn15"));

//rne15 -> SetLineColor(4);
//rng15 -> SetLineColor(2);
rn15 -> SetLineColor(1);

c12->cd(16);
rn15->Draw();
//rng15->Draw("same");
//rne15->Draw("same");

auto legend15 = new TLegend(0.1,0.7,0.48,0.9);
legend15->AddEntry(rn15,"All Counts","l");
//legend15->AddEntry(rng15,"Ground State","l");
//legend15->AddEntry(rne15,"Excited State","l");
legend15->Draw();


sprintf(str10,"/mnt/c/Users/wbrav/OneDrive/Desktop/20Ne_root_files/ANL/data/Analysis/new_sort/141MeV/PAlpha/pics/ground_vs_excited_run%d-to-run%da.png",RunID1,RunID2);
c12->SaveAs(str10);

ofstream myfile;
myfile.open("counts.txt");

myfile << "Ring 1 Ground State Counts:   " << rng0->GetEntries();
myfile << "\nRing 1 Excited State Counts:  "<< rne0->GetEntries() ;
myfile << "\nRing 1 All counts:            "<<rn0->GetEntries();

myfile << "\n\n";
myfile << "Ring 2 Ground State Counts:   " << rng1->GetEntries();
myfile << "\nRing 2 Excited State Counts:  " << rne1->GetEntries();
myfile << "\nRing 2 All counts:            "<<rn1->GetEntries();

myfile << "\n\n";
myfile << "Ring 3 Ground State Counts:   " << rng2->GetEntries();
myfile << "\nRing 3 Excited State Counts:  " << rne2->GetEntries();
myfile << "\nRing 3 All counts:            "<<rn2->GetEntries();

myfile << "\n\n";
myfile << "Ring 4 Ground State Counts:   " << rng3->GetEntries();
myfile << "\nRing 4 Excited State Counts:  " << rne3->GetEntries();
myfile << "\nRing 4 All counts:            "<<rn3->GetEntries();

myfile << "\n\n";
myfile << "Ring 5 Ground State Counts:   " << rng4->GetEntries();
myfile << "\nRing 5 Excited State Counts:  " << rne4->GetEntries();
myfile << "\nRing 5 All counts:            "<<rn4->GetEntries();

myfile << "\n\n";
myfile << "Ring 6 Ground State Counts:   " << rng5->GetEntries();
myfile << "\nRing 6 Excited State Counts:  " << rne5->GetEntries();
myfile << "\nRing 6 All counts:            "<<rn5->GetEntries();

myfile << "\n\n";
myfile << "Ring 7 Ground State Counts:   " << rng6->GetEntries();
myfile << "\nRing 7 Excited State Counts:  " << rne6->GetEntries();
myfile << "\nRing 7 All counts:            "<<rn6->GetEntries();

myfile << "\n\n";
myfile << "Ring 8 Ground State Counts:   " << rng7->GetEntries();
myfile << "\nRing 8 Excited State Counts:  " << rne7->GetEntries();
myfile << "\nRing 8 All counts:            "<<rn7->GetEntries();

myfile << "\n\n";
myfile << "Ring 9 Ground State Counts:   " << rng8->GetEntries();
myfile << "\nRing 9 Excited State Counts:  " << rne8->GetEntries();
myfile << "\nRing 9 All counts:            "<<rn8->GetEntries();

myfile << "\n\n";
myfile << "Ring 10 Ground State Counts:  " << rng9->GetEntries();
myfile << "\nRing 10 Excited State Counts: " << rne9->GetEntries();
myfile << "\nRing 10 All counts:           "<<rn9->GetEntries();

myfile << "\n\n";
myfile << "Ring 11 Ground State Counts:  " << rng10->GetEntries();
myfile << "\nRing 11 Excited State Counts: " << rne10->GetEntries();
myfile << "\nRing 11 All counts:           "<<rn10->GetEntries();

myfile << "\n\n";
myfile << "Ring 13 Ground State Counts:  " << rng12->GetEntries();
myfile << "\nRing 13 Excited State Counts: " << rne12->GetEntries();
myfile << "\nRing 13 All counts:           "<<rn2->GetEntries();

myfile << "\n\n";
//myfile << "Ring 14 Ground State Counts:  " << rng13->GetEntries();
//myfile << "\nRing 14 Excited State Counts: " << rne13->GetEntries();
myfile << "\nRing 14 All counts:           "<<rn13->GetEntries();

myfile << "\n\n";
//myfile << "Ring 15 Ground State Counts:  " << rng14->GetEntries();
//myfile << "\nRing 15 Excited State Counts: " << rne14->GetEntries();
myfile << "\nRing 15 All counts:           "<<rn14->GetEntries();

myfile << "\n\n";
//myfile << "Ring 16 Ground State Counts:  " << rng15->GetEntries();
//myfile << "\nRing 16 Excited State Counts: " << rne15->GetEntries();
myfile << "\nRing 16 All counts:           "<<rn15->GetEntries();



myfile.close();



return 0;
}


int main1(int argc, char** argv){

  int num1, num2; 
  sscanf (argv[1],"%d",&num1);
  sscanf (argv[2],"%d",&num2);
  
  Cuts_Analysis(num1, num2);
  return 0;
}
