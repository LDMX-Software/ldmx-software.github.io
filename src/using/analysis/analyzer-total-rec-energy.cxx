// filename: MyAnalyzer.cxx
#include "Framework/EventProcessor.h"

#include "Ecal/Event/EcalHit.h"

class MyAnalyzer : public framework::Analyzer {
 public:
  MyAnalyzer(const std::string& name, framework::Process& p)
    : framework::Analyzer(name, p) {}
  ~MyAnalyzer() = default;
  void onProcessStart() override;
  void analyze(const framework::Event& event) override;
};

void MyAnalyzer::onProcessStart() {
  getHistoDirectory(); // forget this -> silently no output histogram
  histograms_.create(
      "total_ecal_rec_energy",
      "Total ECal Rec Energy [GeV]", 160, 0.0, 16.0
  );
}

void MyAnalyzer::analyze(const framework::Event& event) {
  const auto& ecal_rec_hits{event.getCollection<ldmx::EcalHit>("EcalRecHits")};
  double total = 0.0;
  for (const auto& hit : ecal_rec_hits) {
    total += hit.getEnergy();
  }
  histograms_.fill("total_ecal_rec_energy", total/1000.);
}

DECLARE_ANALYZER(MyAnalyzer);
