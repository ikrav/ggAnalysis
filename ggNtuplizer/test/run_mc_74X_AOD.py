import FWCore.ParameterSet.Config as cms

process = cms.Process('ggNtuplizer')

#process.load("Configuration.Geometry.GeometryIdeal_cff")

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')
process.load("Configuration.StandardSequences.MagneticField_cff")


from PhysicsTools.PatAlgos.patTemplate_cfg import *

process.load("PhysicsTools.PatAlgos.patSequences_cff")
process.load( "PhysicsTools.PatAlgos.producersLayer1.patCandidates_cff" )
process.load( "PhysicsTools.PatAlgos.selectionLayer1.selectedPatCandidates_cff" )
#from PhysicsTools.PatAlgos.tools.coreTools import *
#runOnData( process, outputModules = [] )


process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('outTuple.root'),
)

process.ca8PFJetsCHSPrunedLinks = cms.EDProducer("RecoJetDeltaRValueMapProducer",
                                         src = cms.InputTag("ca8PFJetsCHS"),
                                         matched = cms.InputTag("ca8PFJetsCHSPruned"),
                                         distMax = cms.double(0.8),
                                         value = cms.string('mass')
                        )



process.patJets.discriminatorSources = cms.VInputTag(cms.InputTag("jetBProbabilityBJetTags")) 







process.NjettinessCA8 = cms.EDProducer("NjettinessAdder",
                              src=cms.InputTag("ca8PFJetsCHS"),
                              cone=cms.double(0.8),
                              Njets=cms.vuint32(1,2,3)
                              )

#process.out.outputCommands += ['keep *_NjettinessCA8_*_*'] #// FIXME: uncomment?


process.load("ggAnalysis.ggNtuplizer.ggNtuplizer_cfi")

##Taus
#from PhysicsTools.PatAlgos.tools.tauTools import *
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
#process.cleanPatTaus.preselection = cms.string(' tauID("decayModeFinding") > 0.5 ')
#process.cleanPatTaus.finalCut = cms.string(' pt > 15.0 & abs(eta) < 2.5 ')
process.load("ggAnalysis.ggNtuplizer.ggTau_cff")
##Jets

process.ggNtuplizer.dumpSubJets=cms.bool(False)
process.ggNtuplizer.dumpJets=cms.bool(False)
process.ggNtuplizer.dumpTaus=cms.bool(False)

process.TFileService = cms.Service("TFileService", fileName = cms.string('ggtree_mc.root'))

process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
        #'file:/tmp/cmkuo/GJet_Pt40_doubleEMEnriched_TuneZ2star_13TeV-pythia6_Phys14.root'
        'file:/data4/cmkuo/testfiles/GJet_Pt40_doubleEMEnriched_TuneZ2star_13TeV-pythia6_Phys14.root'
        #'root://cmsxrootd.fnal.gov///store/mc/Phys14DR/DYJetsToLL_M-50_13TeV-madgraph-pythia8/AODSIM/PU20bx25_PHYS14_25_V1-v1/00000/00CC714A-F86B-E411-B99A-0025904B5FB8.root'
        )
                            )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )
#process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

###9th April, 2015 SHILPI JAIN
###ADDING ELECTRON ID MVA IN THE PATH: https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentificationRun2

#process.load("EgammaAnalysis.ElectronTools.electronIdMVAProducer_CSA14_cfi")

#setattr(process.patElectrons.electronIDSources, "trigMVAid",cms.InputTag("mvaTrigV050nsCSA14"))


useAOD = True
#####VID framework####################
from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
# turn on VID producer, indicate data format  to be
# DataFormat.AOD or DataFormat.MiniAOD, as appropriate 
if useAOD == True :
    dataFormat = DataFormat.AOD
else :
    dataFormat = DataFormat.MiniAOD

process.ggNtuplizer.isAOD=cms.bool(useAOD)

switchOnVIDElectronIdProducer(process, dataFormat)
switchOnVIDPhotonIdProducer(process, dataFormat)

# define which IDs we want to produce
my_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_PHYS14_PU20bx25_V2_cff',
                 'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV51_cff']

#add them to the VID producer
for idmod in my_id_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
    
my_phoid_modules = ['RecoEgamma.PhotonIdentification.Identification.cutBasedPhotonID_PHYS14_PU20bx25_V2_cff']

#add them to the VID producer
for idmod in my_phoid_modules:
    setupAllVIDIdsInModule(process,idmod,setupVIDPhotonSelection)



process.p = cms.Path(
#process.egmGsfElectronIDSequence
 #process.mvaTrigV050nsCSA14
 #+ process.mvaTrigV025nsCSA14
 #+ process.mvaNonTrigV050nsCSA14
 #+ process.mvaNonTrigV025nsCSA14
 #+ process.mvaNonTrigV025nsPHYS14
 #* process.NjettinessCA8
     process.egmGsfElectronIDSequence 
     * process.egmPhotonIDSequence 
     * process.patDefaultSequence
    * process.ggNtuplizer
)

#process.p = cms.Path(
#process.patDefaultSequence
# *    process.NjettinessCA8
# *  process.ggNtuplizer
#)

process.outpath = cms.EndPath(process.out)
process.outpath.remove(process.out)

#print process.dumpPython()
