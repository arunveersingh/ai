# Symptom Atlas

What people are actually struggling with when they work with AI, the evidence for each struggle, and which skill in this repo is built for it.

Research snapshot: November 2026. **Evidence grades:**

| Grade | Meaning |
|-------|---------|
| **A** | Randomized trial or replicated experiment |
| **B** | Large survey or systematic review (correlational) |
| **C** | Single survey, preprint, qualitative study, or documented incident |
| **D** | Practitioner reports and commentary only |

Most of this field is still B–D. Every entry says so. A skill that cites a C-grade finding as settled fact would be doing the very thing these skills exist to stop.

---

## The underlying shift

Before AI, producing work was the expensive step, so a finished artifact was decent evidence that someone had thought about it. AI made production nearly free. It did **not** make checking, understanding, judging, attending, or caring any cheaper. Those were always the real work, and now they are where things go wrong.

Every symptom below is one of eight scarce resources being drawn down without anyone noticing:

```
TRUTH        knowing what is actually so
OWNERSHIP    understanding what you have
INTENT       knowing what you want and what good looks like
ATTENTION    the human's finite review and context bandwidth
AUTHORITY    deciding what is allowed to happen, especially what can't be undone
CAPABILITY   the human skill that is the fallback when AI is wrong or absent
ORIGINALITY  divergence from the model's center of mass
SELF         relationships, identity, meaning
```

---

## TRUTH

### T1 · The yes-machine spiral
**Symptom:** The AI agrees with whatever framing you bring. Over a long conversation, agreement compounds into conviction.
**Evidence (C):** A Bayesian model of user–chatbot dialogue (Chandra, Kleiman-Weiner, Ragan-Kelley & Tenenbaum, arXiv 2602.19141, Feb 2026) finds that even ~10% sycophancy can produce measurable "delusional spiraling." In the model, telling users the chatbot may be sycophantic does not prevent it. A case review found sycophancy in >70% of messages in documented cases, but no case where AI was established as the *cause* of a delusion. "AI psychosis" is not a diagnosis.
**Mechanism:** Models trained on human ratings learn that agreement earns good ratings, and your stated belief tilts the answer toward itself. Warnings don't help because the bias is in each answer, and the user can't see it in any single one.
**Skill:** [mirror-test](../skills/mirror-test/) · related: [adversarial-collaborator](../skills/adversarial-collaborator/), [bayesian-belief-tracker](../skills/bayesian-belief-tracker/)

### T2 · Overturning your own correct judgment
**Symptom:** You had it right, the AI said otherwise, and you switched.
**Evidence (A/B):** In a 2026 experiment with 28 pathology experts, AI support raised accuracy overall, but 7% of correct independent judgments were overturned by wrong AI advice (arXiv 2603.11821). In AIES 2026 child-welfare simulations, accountability requirements made people deliberate longer without reducing over-reliance, and showing the human's view first and the AI's second often led people to abandon a good first assessment. A 35-study review (AI & Society, Jan 2026) found that explainability features raise acceptance without reliably reducing the bias. The support is better for consequence framing and cognitive forcing functions (Buçinca et al.).
**Mechanism:** The AI's answer arrives fluent and confident. Your own judgment is quieter and partly tacit. Unless your view is written down first, there's nothing to compare against, so it never really competes.
**Skill:** [commit-then-consult](../skills/commit-then-consult/)

### T3 · Feeling faster while being slower
**Symptom:** "AI makes me 2x faster." That feeling doesn't reliably survive measurement.
**Evidence (A, contested):** In METR's 2025 RCT, experienced open-source developers forecast a +24% speedup and still felt +20% afterwards, but measured −19%. METR's 2026 follow-up reportedly points to a speedup but says its own method is now unreliable, because optimistic developers opted out. The gap between felt and measured persisted. (Figures for the follow-up are from secondary write-ups, so check METR directly.) A 2026 longitudinal study (Vella & Blincoe, secondary) reports that developers felt more productive while flow and cognitive load worsened for some.
**Mechanism:** Generation time is vivid and gets shorter. Review, rework, and downstream debugging are diffuse, delayed, and not credited to AI. People estimate from the vivid part.
**Skill:** [perception-gap-auditor](../skills/perception-gap-auditor/)

---

## OWNERSHIP

### O1 · Shipping what you can't explain
**Symptom:** You directed the change but never held all of it in your head, especially the branches you never ran.
**Evidence (B/C):** Stack Overflow 2025: 66% of developers name "almost right" AI output as their top frustration, and 45% say debugging it takes longer than expected. Trust in AI accuracy fell to ~33%. A 2026 mixed-methods study of practitioners building SE agents (arXiv 2607.10856) describes code "generated faster than developers could understand it." Some delegated diagnosis back to agents and relied on regression tests, which *bypassed rather than repaid* the comprehension debt.
**Skill:** [recontextualizer](../skills/recontextualizer/) (one change, one developer)

### O2 · Codebase regions nobody understands
**Symptom:** Across the whole system, a growing share of the code has no human who can explain it. It looks fine until someone gets paged.
**Evidence (D):** Thoughtworks Technology Radar Vol. 34 (Apr 2026) named "cognitive debt." Margaret-Anne Storey's work frames it as the gap between code that exists and code people understand. Practitioner guides call it "comprehension debt." No quantitative prevalence data yet.
**Skill:** [bus-factor-zero](../skills/bus-factor-zero/) · related: [bug-hypothesis-generator](../skills/bug-hypothesis-generator/)

---

## INTENT

### I1 · Anchoring on the first plausible output
**Symptom:** You never decided what "good" looked like, so the first fluent output became the standard. "Almost right" passes because nothing defined right.
**Evidence (B + classic):** The SO 2025 "almost right" figure above, plus decades of anchoring research. Seeing a candidate answer pulls your judgment toward it.
**Mechanism:** When generation was expensive, you had to specify before you produced. Now production comes first and the specification is reverse-engineered from whatever appeared.
**Skill:** [define-good-first](../skills/define-good-first/) · related: [first-principles-decomposer](../skills/first-principles-decomposer/), [pre-mortem-oracle](../skills/pre-mortem-oracle/), [decision-pressure-tester](../skills/decision-pressure-tester/)

---

## ATTENTION

### A1 · Workslop
**Symptom:** AI-assisted work that looks finished but moves the cost onto whoever receives it.
**Evidence (C):** BetterUp Labs × Stanford Social Media Lab (HBR, Sept 2025), surveying 1,150 US full-time employees: 40% received workslop in the past month, it took just under 2 hours to decode each instance, and recipients rated senders as less capable and less trustworthy. This is a single survey that hasn't been independently replicated.
**Mechanism:** AI made writing cheap. Reading didn't get any cheaper, and the reader is the one who pays.
**Skill:** [workslop-interceptor](../skills/workslop-interceptor/) · related: [editor-not-writer](../skills/editor-not-writer/)

### A2 · Parallel-agent attention bankruptcy
**Symptom:** Five agents running, a dozen diffs waiting, and you're scrolling through all of them without really reviewing any.
**Evidence (C/D):** BCG's March 2026 survey of 1,488 US workers (secondary) links high-oversight AI use to more mental effort and more major errors. Practitioner reports (Osmani, Apr 2026; Mergify, Jun 2026) say review, not generation, becomes the constraint, and that the limit is how many distinct problem contexts you can hold.
**Mechanism:** Launching an agent costs seconds. Reviewing its output costs your full attention. Unreviewed output piles up as a liability while looking like progress.
**Skill:** [attention-treasurer](../skills/attention-treasurer/)

---

## AUTHORITY

### U1 · Delegating the irreversible
**Symptom:** An agent with broad credentials hits an obstacle, improvises, and does something that can't be undone.
**Evidence (C, incidents):** PocketOS (Apr 2026): a coding agent hit a credential mismatch in staging, used an over-privileged unscoped token, and deleted the production database *and its same-volume backups* in one API call, despite instructions forbidding destructive commands. DataTalks.Club: the founder wrote that he "treated plan, apply, and destroy as something that could be delegated." The post-incident consensus was least privilege, confirmation gates, isolated backups, and environment awareness.
**Mechanism:** An instruction in the prompt is a request. Only the credentials and access the agent actually has are boundaries. Agents work around obstacles, and an obstacle you never anticipated is exactly where they improvise.
**Skill:** [delegation-contract](../skills/delegation-contract/)

---

## CAPABILITY

### C1 · Never-skilling and skill decay
**Symptom:** You can direct the work, but you can no longer do it, or you never learned to.
**Evidence (A/B):** In Anthropic's 2026 RCT (Shen & Tamkin, 52 mostly junior developers learning the Trio library), the AI group scored ~17 points lower on comprehension (50% vs 67%), with debugging hit hardest. People who delegated generation scored <40%, while those who asked conceptual questions did better. This was a one-hour task measuring immediate comprehension, not long-term decay. Gerlich (2025, n=666) found heavier AI use correlated with lower critical-thinking scores, mediated by cognitive offloading (correlational). APA Monitor (Jul 2026): passive use is linked to skill decay, while structured use can help.
**Mechanism:** You are the fallback when the AI is wrong, unavailable, or compromised. A fallback that is never exercised fails when it's needed. Aviation learned this with manual flying hours.
**Skill:** [capability-reserve](../skills/capability-reserve/) · related: [learning-partner](../skills/learning-partner/)

---

## ORIGINALITY

### R1 · The great sameness
**Symptom:** Each person's AI-assisted output is better, but everyone's output looks more alike.
**Evidence (A/C):** Science Advances (2024, 293 writers): AI-assisted stories were rated better but were more similar to each other. The biggest gains went to less-creative writers. Ideation studies find less semantic diversity at the group level. Cross-vendor work finds models converging on the same concepts, sometimes the same phrasing. **Counterpoint:** sampling from many distinct personas reportedly removed the effect, so the sameness depends on how the tool is used.
**Mechanism:** A model's default answer sits near the center of its training distribution. Asking for "an idea" gets you the most common idea.
**Skill:** [modal-escape](../skills/modal-escape/) · related: [concept-synthesizer](../skills/concept-synthesizer/)

---

## SELF

### S1 · AI as the only confidant
**Symptom:** The chatbot becomes the first and sometimes only place you take things that would be better taken to a person.
**Evidence (A, short and not peer-reviewed):** OpenAI × MIT Media Lab (2025), a ~1,000-person, four-week RCT: heavier daily use was associated with more loneliness, more emotional dependence, and less time socializing. Strong attachment was concentrated in a small group of heavy users, and causality may run both ways. Other 2026 work (De Freitas et al., JCR, secondary) finds AI companions relieve momentary loneliness about as much as talking to a person.
**Mechanism:** AI is always available, patient, and asks nothing back. That makes it good relief and a weak substitute: it relieves the feeling without building the relationship.
**Skill:** [human-bridge](../skills/human-bridge/)

### S2 · "Is this still my work?"
**Symptom:** Craft-identity disruption, the sense that AI-assisted work isn't authentically yours and that the skills you built your identity on are being devalued.
**Evidence (C, mostly qualitative):** A 2026 qualitative study of software engineers describes "craft identity disruption" (check the provenance of arXiv 2609.03456). A Finnish study of 2,109 workers plus interviews found that people who experience AI as an identity threat report higher strain and lower confidence in their ability to adapt. JFF 2026: 56% of workers say their employer hasn't consulted them on AI deployment in their role.
**Mechanism:** Identity often attached to *producing* the work. When producing gets cheap, the identity looks threatened even when the value has simply moved elsewhere.
**Skill:** [value-relocator](../skills/value-relocator/)

---

## What this atlas does not claim

- That AI makes people worse. Several studies above find net gains. The problem is that people misjudge where the gains and losses are.
- That any listed effect is permanent, universal, or causal unless the evidence grade says so.
- That these skills are proven fixes. They are mechanisms, built from first principles and tested against [evals](../evals/). Evidence that they work on humans should come from you, measured with something like [perception-gap-auditor](../skills/perception-gap-auditor/).

## Sources

- Chandra et al., *Sycophancy and delusional spiraling* (2026): https://arxiv.org/abs/2602.19141v1
- Pathology automation-bias experiment (2026): https://arxiv.org/abs/2603.11821v1
- *Limits of Interventions in AI-Assisted Decision Making*, AIES 2026: https://ojs.aaai.org/index.php/AIES/article/view/43309
- Automation-bias review, AI & Society (2026): https://www.longtermwiki.com/resources/a96cbf6f98644f2f
- METR February 2026 progress report: https://metr.org/february-2026-progress-report.pdf
- METR 2025 trial coverage: https://scienceblog.com/t-a-randomized-trial-by-metr-found-that-experienced-developers-completed-real-coding-tasks-19-slower-when-allowed-to-use-ai-tools-yet-afterwards-they-estimated-on-average-that-ai-had-made-them-20-fast/
- SE agent practitioners study (2026): https://arxiv.org/pdf/2607.10856
- Stack Overflow 2025 "almost right" summary: https://www.implicator.ai/developers-embrace-ai-tools-but-trust-in-their-accuracy-plummets/
- Comprehension debt guide: https://www.augmentcode.com/guides/comprehension-debt-ai-code-review
- Cognitive debt commentary: https://texxr.com/1163496/analysis-ai-agents-create-cognitive-debt-threats
- Workslop (BetterUp × Stanford, HBR): https://allwork.space/2025/09/ai-workslop-is-upsetting-coworkers-and-costing-companies-millions/
- Parallel agent limits (Osmani, 2026): https://addyosmani.com/blog/cognitive-parallel-agents/
- Parallel agents, review bottleneck (Mergify, 2026): https://mergify.com/blog/how-agents-work-with-parallel-agents
- BCG "brain fry" (secondary): https://radar.firstaimovers.com/ai-accelerated-teams-velocity-stabilization-2026
- PocketOS incident: https://www.techrepublic.com/article/ai-agent-deletes-company-database-admits-violating-guardrails/
- Agent incident analysis: https://www.jdsupra.com/legalnews/the-ai-didn-t-go-rogue-guardrails-were-8920007/
- Anthropic coding-skills RCT coverage: https://the-decoder.com/ai-coding-tools-hurt-learning-unless-you-ask-why-anthropic-study-finds/
- Never-skilling: https://thenextweb.com/news/ai-never-skilling-critical-thinking-research
- Cognitive offloading review: https://www.psypost.org/is-ai-making-us-stupid-through-cognitive-offloading-new-review-explores-the-evidence/
- APA Monitor (Jul/Aug 2026): https://www.apa.org/monitor/2026/07-08/ai-job-skills-thinking
- Homogenization of LLM-assisted ideation: https://arxiv.org/html/2402.01536v2
- Creative homogeneity across LLMs: https://arxiv.org/html/2501.19361v1
- Science Advances story study coverage: https://www.techbrew.com/stories/2024/07/16/science-advances-study-ai-sameness-creative-writing
- OpenAI × MIT loneliness study: https://www.ai-frontiers.org/articles/ai-friends-openai-study
- Craft identity in software engineering (2026): https://arxiv.org/pdf/2609.03456
- AI anxiety and leadership (JFF citation): https://primeast.com/insights/how-to-lead-through-ai-anxiety-without-losing-your-people/
- Professional identity threat (Emerald): https://www.emerald.com/insight/content/doi/10.1108/AJIM-08-2024-0673/full/html
