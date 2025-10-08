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
  /**
   * In v4.5.1 ldmx-sw and earlier, forgetting `getHistoDirectory()`
   * led to silently not creating any histograms.
   * In v4.5.2 ldmx-sw and newer, it can be left out but it does
   * no harm if left in.
   */
  getHistoDirectory();
  histograms_.create(
      "total_ecal_rec_energy",
      "Total ECal Rec Energy [GeV]", 160, 0.0, 16.0
  );
}

void MyAnalyzer::analyze(const framework::Event& event) {
  const auto& ecal_rec_hits{event.getCollection<ldmx::EcalHit>("EcalRecHits","")};
  double total = 0.0;
  for (const auto& hit : ecal_rec_hits) {
    total += hit.getEnergy();
  }
  histograms_.fill("total_ecal_rec_energy", total/1000.);
}

DECLARE_ANALYZER(MyAnalyzer);
