---
title: Rural Loan, Papua New Guinea
title_html: *Rural Loan:* a first loan for farmers with no ID, bank account or credit history
slug: rural-loan
label: Case study · Financial inclusion · 2021
summary: Designing a first loan for farmers who had never had a bank account, ID card or credit history.
intro: How in-language field research shaped a loan, its rules and the tool bank staff used in the village.
chips: Design thinking, In-language field research, Mixed-method interviews, Affinity mapping, Journey mapping, Service blueprint, Wireframes
header_image: rural-loan-kyc.png
header_image_alt: Diagram comparing identity checks: the bank asking for ID, and the exporter confirming farmers from its trading records
snapshot:
  My role: Co-lead, human-centred design partner (Innovation Quotient)
  Team: Me and one colleague, with two local field researchers
  Timeline: Early 2021, research and design
  Partners: GSMA AgriTech (funded by the Australian Government), MiBank, Kamapim, Field Buzz, YUX Design, a credit risk specialist
---

<!--
Case study sections, in order. Each starts with a +++ settings block.
section: about | challenge | process | insights | thinking | solution | impact | reflection | sources
-->

+++
section: about
eyebrow: About the project
+++

## A loan built around *farmers*, not paperwork

GSMA AgriTech brought together a lender (MiBank), a vanilla buyer that already traded with 3,000 farmers (Kamapim) and an agritech company (Field Buzz). Their goal was a minimum viable credit product built around farmers' real needs. Our job was to find out what those needs were and design a service that worked for farmers, the bank and its staff.

+++
section: challenge
eyebrow: The challenge
question: How could we offer a loan that works for vanilla farmers in Papua New Guinea?
+++

## Banks need an *identity* farmers didn't have

Most smallholder farmers had no ID, bank account, financial history or collateral, and some had no birth certificate. Loan sharks were often the only option. The country speaks over 800 languages, and a trip to the bank in Madang City could take hours.

- Field agents, not farmers, will use the app. | Confirmed
- Loans of 2 to 3 months will suit farmers. | Disproved: farmers needed 6 months or more

+++
section: process
eyebrow: Research process
stages: Empathise: Desk research, Stakeholder interviews, App demo, Field interviews, Gamified voting; Define: Affinity mapping, Journey mapping, Key insights; Ideate: Service flows, Partner workshops; Prototype: Service blueprint, Wireframes, Functional specifications; Deliver: MVP agreed by the consortium, Launched by MiBank
+++

## *Design thinking*, run remotely through local researchers

### Interviews in farmers' own languages
We recruited and trained two bilingual field researchers. They spoke with 54 farmers in 8 villages and 6 field agents, in sessions under an hour, with a closed-question section to count patterns.

### Research that works with low literacy
Researchers drew grids, and farmers voted by marking them with fruit peel.

### Mapping a farmer's financial year
image: rural-loan-farmers-year.png | A 12-month band showing the vanilla cycle in three phases: growing and pollinating, harvest and selling, and waiting for the next harvest. Money is needed for tools and labour while growing, income arrives at harvest, and repayment should follow income. | A farmer's year. Recreated from memory.
We synthesised the transcripts on the wall into pain points, needs and themes, then mapped farmers' financial lives across the harvest year.

### The whole service, not just a screen
image: rural-loan-blueprint.png | Service blueprint with four lanes: farmer, field staff using the loan tool, exporter, and back office. In the village and offline: staff visit the farmer and capture the application, the exporter confirms identity from its trading records, and staff check eligibility. At the bank: data syncs and the back office makes the credit decision. Then the farmer is notified and repays. | Service blueprint, from village visit to repayment. Recreated from memory.
A blueprint from the village visit to repayment, and front-end and back-end flows covering eligibility, KYC, borrowing limits, decisioning and notifications, worked out with the credit risk specialist.

+++
section: insights
eyebrow: Key insights
+++

## What we heard from *farmers*

- coins | No one lives on vanilla alone | Every farmer relied on other income, such as cocoa.
- chart | Credit was new | Only **7%** had taken a formal loan. Interest and repayment terms were unfamiliar.
- phone | Few smartphones | **48%** had a mobile phone, and only **2%** a smartphone.
- alert | Carrying cash is dangerous | Farmers risked violent attack carrying vanilla or cash home after harvest.
- calendar | Longer loans needed | Farmers and agents wanted **6 months** or more, not the 2 to 3 we assumed.
- inclusive | Women often had no money of their own | Where they did, they usually hid what they had at home.

![Five insight cards, each with an icon: Carrying cash is dangerous. Women often have no money of their own. Income arrives once a season. Many farmers have no ID. Banking is new to most farmers.](rural-loan-insights.png "What we heard from farmers. Recreated from memory.")

+++
section: thinking
+++

One early question was whether farmers could apply for the loan through an app themselves. Field research answered it quickly: many farmers had low literacy, little experience of formal finance and often no ID, so a self-service app would have shut most of them out. We shifted to an assisted model, with bank staff applying alongside farmers in their villages, and rethought identity checks around the trading records farmers already had.

+++
section: solution
eyebrow: The solution
+++

## From insight to *design decision*

- No ID, but a trusted trading relationship | Identity from the buyer's trading records
- Few smartphones, agents have them | An assisted model: agents apply alongside farmers in the village
- Loans needed to expand | Three loan sizes tied to vine count (300, 500 and 1,000 kina, about £69 to £230)
- Credit is unfamiliar | Mandatory financial literacy training

**Trade-off:** basing identity on trading records limited the loan to farmers already trading with one buyer. In return, it made KYC possible at all, and it built on a relationship farmers already trusted.

![Before and after comparison. Before: the bank asks for an ID or birth certificate, so most farmers cannot apply. After: the exporter confirms the farmer from its trading records, so the farmer can apply, and their trading history starts their credit history.](rural-loan-kyc.png "KYC without ID documents: how a farmer proves who they are. Recreated from memory.")

**Trade-off:** the tool had to work offline in the field. In our designs, that meant applications were captured in the village and the credit decision followed once staff were back at the bank.

![Four phone-screen wireframes in sequence. 1, Log in: phone number and PIN fields. 2, Enter your details: full name, village and phone number. 3, Choose the amount: a loan amount in kina, chosen from three options, with a note to repay after harvest. 4, Check and apply: a summary of name, village, amount and repayment, a tick box to agree to the loan terms, and an Apply button.](rural-loan-wireframes.png "Wireframes of the loan application tool that MiBank field staff used with farmers. Recreated from memory.")

+++
section: impact
numbers: 355 | loans over a 2.5-year pilot; 330 | farmers reached; 35% | of borrowers were women; 99% | first-time access to a loan
note: GSMA's 2023 evaluation. These results belong to the whole partnership, and the pilot ran after my phase of the work.
+++

> "It helped me buy my new tools and expand my vanilla farm from 300 plants to 1,000 plants."
>
> Farmer quoted in GSMA's evaluation

+++
section: reflection
eyebrow: Reflection
+++

## What I'd do *differently*

- **Test the rules, not just the screens.** Farmers still struggled with a fixed due date that didn't match when they were paid. Terms and fees decide whether someone can repay, so I'd test them with farmers before launch.
- **Design for who's missing.** We heard that women often had no money of their own. GSMA found women were 4% of borrowers early in the pilot and 35% by the end. Next time I'd act on what we heard about women from the start.
- **Make insights survive delivery.** I left before the pilot, so I couldn't see which recommendations held. I'd agree up front how the key findings will be checked in the live product.

+++
section: sources
+++

- GSMA Mobile for Development, "Improving farmers' access to credit: A new GSMA partnership in Papua New Guinea", 15 January 2021
- GSMA Mobile for Development, "Smallholder loans pilot in Papua New Guinea: what did farmers have to say about the service and has it enhanced their access to finance?", 3 August 2023
