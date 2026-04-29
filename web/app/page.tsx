import { Nav } from "@/components/Nav";
import { Hero } from "@/components/Hero";
import { ProblemSection } from "@/components/ProblemSection";
import { HowItWorks } from "@/components/HowItWorks";
import { IntegrationsStrip } from "@/components/IntegrationsStrip";
import { Pricing } from "@/components/Pricing";
import { AudienceSection } from "@/components/AudienceSection";
import { WaitlistFooter } from "@/components/WaitlistFooter";

export default function HomePage() {
  return (
    <main>
      <Nav />
      <Hero />
      <ProblemSection />
      <HowItWorks />
      <IntegrationsStrip />
      <Pricing />
      <AudienceSection />
      <WaitlistFooter />
    </main>
  );
}
