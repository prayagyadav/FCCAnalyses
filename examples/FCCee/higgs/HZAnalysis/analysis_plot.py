import ROOT
# Run with: fccanalysis plots --legend-text-size 0.025 --legend-y-min 0.65
# global parameters
intLumi        = 10.80e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} #rightarrow ZH #rightarrow 4#mu+ X'
delphesVersion = '3.4.2'
energy         = 240.0
collider       = 'FCC-ee'
inputDir       = '/eos/user/p/pryadav/ZH_HZZ/4mu/outputs/final/test/sel_p_0/'
formats        = ['jpg']
yaxis          = ['log','lin']
stacksig       = ['nostack']
outdir         = 'cuts_outputs/'
splitLeg       = False
legend_text_size=4656
plotStatUnc    = False
doScale = True
scaleSig =1
variables = ["fourmuons_mass","fourmuons_pmin","Z_res_mass","Z_non_res_mass","vis_e_woMuons","iso_least_isolated_muon","missing_p", "cos_theta_miss"]



#plotStatUnc = True
selections = {}
selections['ZH']   = ["sel0","sel1","sel2","sel3","sel4","sel5",
]


extralabel = {}
extralabel['sel0'] = "No Selection"
extralabel['sel1'] = "4#mu,p_{min}>5 "
extralabel['sel2'] = "4#mu,p_{min}>5,p_{miss}<40"
extralabel['sel3'] = "4#mu,p_{min}>5,p_{miss}<40,E_{vis}>30"
extralabel['sel4'] = "4#mu,p_{min}>5,p_{miss}<40,E_{vis}>30,M_{Z*}<65"
extralabel['sel5'] = "4#mu,p_{min}>5,p_{miss}<40,E_{vis}>30,M_{Z*}<65,120<M_{4#mu}<126"




plots = {}
plots['ZH'] = {
'signal':{
    ##'qqH_HZZ':['wzp6_ee_qqH_HZZ_llll_ecm240'],
    ##'nunuH_HZZ':['wzp6_ee_nunuH_HZZ_ecm240'],
},

'backgrounds':{

'ZZ':['p8_ee_ZZ_ecm240'],
##'Zqq':['p8_ee_Zqq_ecm240'],
##'mumuH_Hjj':['wzp6_ee_mumuH_Hbb_ecm240','wzp6_ee_mumuH_Hcc_ecm240','wzp6_ee_mumuH_Hgg_ecm240',],
#'mumuH_Hbb':['wzp6_ee_mumuH_Hbb_ecm240'],
##'WW':['p8_ee_WW_ecm240'],
##'HWW':['wzp6_ee_mumuH_HWW_ecm240','wzp6_ee_bbH_HWW_ecm240','wzp6_ee_tautauH_HWW_ecm240','wzp6_ee_ccH_HWW_ecm240'],
#'mumuH_HWW':['wzp6_ee_mumuH_HWW_ecm240'],
#'mumuH_Htautau':['wzp6_ee_mumuH_Htautau_ecm240'],
#'bbH_HWW':['wzp6_ee_bbH_HWW_ecm240'],
#'mumuH_Hmumu':['wzp6_ee_mumuH_Hmumu_ecm240'],
#'mumuH_Hcc':['wzp6_ee_mumuH_Hcc_ecm240'],
#'tautauH_HWW':['wzp6_ee_tautauH_HWW_ecm240'],
##'mumuH_HZa':['wzp6_ee_mumuH_HZa_ecm240'],
#'mumuH_Hgg':['wzp6_ee_mumuH_Hgg_ecm240'],
#'ccH_HWW':['wzp6_ee_ccH_HWW_ecm240'],
#'mumuH_Hss':['wzp6_ee_mumuH_Hss_ecm240'],
#'ssH_Hmumu':['wzp6_ee_ssH_Hmumu_ecm240'],
#'qqH_Hmumu':['wzp6_ee_qqH_Hmumu_ecm240'],
#'bbH_Hmumu':['wzp6_ee_bbH_Hmumu_ecm240'],
#'tautauH_Hmumu':['wzp6_ee_tautauH_Hmumu_ecm240'],
#'ccH_Hmumu':['wzp6_ee_ccH_Hmumu_ecm240'],
#'bbH_HZa':['wzp6_ee_bbH_HZa_ecm240'],
#'tautauH_HZa':['wzp6_ee_tautauH_HZa_ecm240'],

},

}

legend = {}
##legend['nunuH_HZZ']='Z(#nu#nu)H(ZZ)'
##legend['qqH_HZZ']='Z(jj)H(4#mu)'
legend['ZZ'] = 'ZZ'
##legend['mumuH_HZa'] = 'Z(#mu#mu)H(Za)'
#legend['mumuH_Hbb'] = 'Z(#mu#mu)H(bb)'
#legend['mumuH_Hmumu'] = 'Z(#mu#mu)H(#mu#mu)'

#legend['mumuH_Htautau'] = 'Z(#mu#mu)H(#tau#tau)'
#legend['mumuH_HWW'] = 'Z(#mu#mu)H(WW)'
##legend['WW'] = 'WW'
#legend['mumuH_Hcc'] = 'Z(#mu#mu)H(cc)'
#legend['bbH_HWW'] = 'Z(bb)H(WW)'
#legend['mumuH_Hgg'] = 'Z(#mu#mu)H(gg)'
#legend['tautauH_HWW'] = 'Z(#tau#tau)H(WW)'
#legend['ccH_HWW'] = 'Z(cc)H(WW)'
##legend['HWW']= 'HWW'
##legend['mumuH_Hjj'] = 'Z(#mu#mu)H(jj)'
#legend['mumuH_Hss'] = 'Z(#mu#mu)H(ss)'
#legend['ssH_Hmumu'] = 'Z(ss)H(#mu#mu)'
#legend['qqH_Hmumu'] = 'Z(qq)H(#mu#mu)'
#legend['bbH_Hmumu'] = 'Z(bb)H(#mu#mu)'
#legend['tautauH_Hmumu'] = 'Z(#tau#tau) H(#mu#mu)'
#legend['bbH_HZa'] = 'Z(bb)H(Za)'
##legend['Zqq'] = 'Zqq'
#legend['ccH_Hmumu'] = 'Z(cc)H(#mu#mu)'
#legend['tautauH_HZa'] = 'Z(#tau#tau) H(Za)'









colors={}
##colors['nunuH_HZZ']=ROOT.kOrange
##colors['qqH_HZZ']= ROOT.kRed
colors['ZZ'] = ROOT.kBlue
##colors['mumuH_HZa']=ROOT.kGreen
#colors['mumuH_Hbb'] = ROOT.kYellow
#colors['mumuH_Hmumu'] = ROOT.kViolet

#colors['mumuH_Htautau'] = ROOT.kMagenta
#colors['mumuH_HWW'] = ROOT.kCyan+5
##colors['WW'] = ROOT.kGray
#colors['mumuH_Hcc'] = ROOT.kYellow+1
#colors['bbH_HWW'] = ROOT.kCyan
#colors['mumuH_Hgg'] = ROOT.kYellow+3
#colors['tautauH_HWW'] = ROOT.kCyan+4
#colors['ccH_HWW'] = ROOT.kCyan+1
##colors['HWW'] = ROOT.kTeal
##colors['mumuH_Hjj'] = ROOT.kCyan
#colors['mumuH_Hss'] = ROOT.kYellow+2
#colors['ssH_Hmumu'] = ROOT.kTeal+2
#colors['qqH_Hmumu'] = ROOT.kTeal+3
#colors['bbH_Hmumu'] = ROOT.kTeal
#colors['tautauH_Hmumu'] = ROOT.kTeal+4
#colors['bbH_HZa'] = ROOT.kViolet
##colors['Zqq'] = ROOT.kYellow
#colors['ccH_Hmumu'] = ROOT.kTeal+1
#colors['tautauH_HZa'] = ROOT.kViolet+5




