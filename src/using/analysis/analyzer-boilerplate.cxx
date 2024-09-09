// filename: MyAnalyzer.cxx
#include "Framework/EventProcessor.h"

#include "Ecal/Event/EcalHit.h"

class MyAnalyzer : public framework::Analyzer {
 public:
  MyAnalyzer(const std::string& name, framework::Process& p)
    : framework::Analyzer(name, p) {}
  ~MyAnalyzer() override = default;
  void onProcessStart() override;
  void analyze(const framework::Event& event) override;
};

void MyAnalyzer::onProcessStart() {
  // this is where we will define the histograms we want to fill
}

void MyAnalyzer::analyze(const framework::Event& event) {
  // this is where we will fill the histograms
}

DECLARE_ANALYZER(MyAnalyzer);
