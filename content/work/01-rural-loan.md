---
title: Rural Loan, Papua New Guinea
slug: rural-loan
summary: Designing a first loan for farmers who had never had a bank account, ID card or credit history.
card_role: Co-lead, human-centred design partner
card_result: Launched by MiBank. The pilot gave 355 loans to 330 farmers over 2.5 years, 35% of them women.
thumbnail: rural-loan-kyc.png
snapshot:
  Project: Rural Loan, a credit product for smallholder vanilla farmers in Madang Province, Papua New Guinea
  Year: 2021 (research and design phase)
  My role: Co-lead, human-centred design partner (Innovation Quotient). I co-owned everything with one colleague: research design, briefing field researchers, synthesis, journey mapping, service flows and wireframes.
  Partners: GSMA AgriTech (funded by the Australian Government), MiBank (lender), Kamapim (vanilla buyer), Field Buzz (agritech), YUX Design (UX partner), a credit risk specialist
  Methods: Remote in-language field research, synthesis and affinity mapping, journey mapping, front-end and back-end service flows, wireframes
  Outcome: Launched by MiBank. The pilot gave 355 loans to 330 farmers over 2.5 years, 35% of them women.
---

## The challenge

Most smallholder farmers in Papua New Guinea are shut out of formal credit. Banks need an economic identity, such as ID documents and a financial history, and most farmers have neither. Many farmers we researched had no ID card, and some had no birth certificate.

The country speaks over 800 languages, and rural areas have few bank branches, ATMs or roads. A trip to the bank in Madang City can take hours, and weather often makes it longer.

GSMA AgriTech brought together a lender (MiBank), a vanilla buyer that already traded with 3,000 farmers (Kamapim) and an agritech company (Field Buzz). Their goal was a minimum viable credit product built around farmers' real needs. Our job was to find out what those needs were and design a service that worked for farmers, the bank and its staff.

## Approach

We could not interview farmers ourselves, so we built the research around people who could. With 800+ languages and low familiarity with financial ideas, an outside researcher would have heard very little.

1. **Research design.** We designed the study and discussion guides around farmers' credit needs, how they made financial decisions, and the vanilla harvest cycle.
2. **Local field researchers.** We recruited and briefed two field researchers in Papua New Guinea to run interviews in farmers' own languages, then gathered the transcripts.
3. **Synthesis.** We synthesised the transcripts on the wall with sticky notes, clustering findings into pain points, needs and themes.
4. **Journey mapping.** We mapped farmers' financial lives across the harvest year, and where a loan could help or harm them.
5. **Service flows.** We designed and iterated front-end and back-end flows covering eligibility, KYC, borrowing limits, decisioning and notifications. We worked with a credit risk specialist, who built the risk models, and with UX partner YUX Design.
6. **Wireframes.** We wireframed the loan application tool that MiBank staff would use with farmers in the field.

## What we learned

A loan is not just money. It lands in a life shaped by harvests, safety, gender and trust, and each of these changes what a good loan looks like.

- **Carrying cash is dangerous.** Farmers risked violent attack when carrying vanilla or cash home after harvest. How money moves is a safety question, not just a convenience.
- **Women often had no money of their own.** Where women did hold money, they usually hid it at home, with no safe place to keep it.
- **Income arrives once a season.** Vanilla pays at harvest, so farmers need money before it and can only repay after it. We studied the harvest cycle closely to shape repayment timing.
- **There was no identity to check.** Many farmers had no ID card or birth certificate, so standard KYC could not work.
- **There was no financial infrastructure or financial literacy to build on.** Most farmers had never had a bank account, and ideas like interest and repayment terms were new.

![Five insight cards, each with an icon: Carrying cash is dangerous. Women often have no money of their own. Income arrives once a season. Many farmers have no ID. Banking is new to most farmers.](rural-loan-insights.png "What we heard from farmers: five insights that shaped the loan. Recreated from memory.")

## Key design decisions

### 1. Use a trusted trading relationship as identity

With no ID documents, we looked for something that already proved who a farmer was. Kamapim, the vanilla buyer and exporter, had records of the farmers it bought from, so we designed verification around Kamapim confirming farmers' details. The launched product made this an eligibility rule: a farmer must have sold beans to Kamapim at least once. A farmer's trading history became both their identity and the start of their credit history.

**Trade-off:** this limited the loan to farmers already trading with one buyer. In return, it made KYC possible at all, and it built on a relationship farmers already trusted.

![Before and after comparison. Before: the bank asks for an ID or birth certificate, so most farmers cannot apply. After: the exporter confirms the farmer from its trading records, so the farmer can apply, and their trading history starts their credit history.](rural-loan-kyc.png "KYC without ID documents: how a farmer proves who they are. Recreated from memory.")

### 2. Design a tool for bank staff, not an app for farmers

A self-service app would have failed people with low literacy and no experience of banking. Instead, we designed a loan application tool that MiBank staff used in the field, sitting with farmers in their villages. We designed for both people at once: the staff member operating the tool, and the farmer who needed to understand and trust what was happening.

**Trade-off:** the tool had to work offline in the field. In our designs, that meant applications were captured in the village and the credit decision followed once staff were back at the bank.

![Four phone-screen wireframes in sequence. 1, Log in: phone number and PIN fields. 2, Enter your details: full name, village and phone number. 3, Choose the amount: a loan amount in kina, chosen from three options, with a note to repay after harvest. 4, Check and apply: a summary of name, village, amount and repayment, a tick box to agree to the loan terms, and an Apply button.](rural-loan-wireframes.png "Wireframes of the loan application tool that MiBank field staff used with farmers. Recreated from memory.")

![Service blueprint with four lanes: farmer, financial provider field staff using the loan tool, exporter, and financial provider back office. In the village and offline: staff visit the farmer and capture the application, the exporter confirms the farmer's identity from its trading records, and staff check eligibility. At the bank: the data syncs and the back office makes the credit decision. After the decision: the farmer is notified and repays the loan. Eligibility checks: has sold vanilla to the exporter, has another income, has a mobile phone, has completed loan training.](rural-loan-blueprint.png "Service blueprint: applying for a Rural Loan, from the village visit to repayment. Recreated from memory.")

### 3. Shape repayment around the harvest

Because farmers earn once a season, we studied the vanilla harvest cycle to inform when repayments should fall.

![A 12-month band showing the vanilla cycle in three phases: growing and pollinating, harvest and selling, and waiting for the next harvest. Farmers need money for tools and labour during the growing phase, income arrives at harvest, and a note says repayment should follow income.](rural-loan-farmers-year.png "A farmer's year: the vanilla cycle in three phases. Recreated from memory.")

### 4. Hold the farmer's view in a busy consortium

Five partners had different priorities: commercial, risk, technical and development. In consortium discussions about what should and should not be built, my colleague and I had to keep making the case for farmers, using what the research showed about their lives.

## Outcome

MiBank launched the product as Rural Loan. GSMA's 2023 evaluation reports that the pilot gave 355 loans to 330 farmers over 2.5 years, and 35% of borrowers were women. These results belong to the whole partnership, and the pilot ran after my phase of the work.

- GSMA reports the loan amounts (300, 500 and 1,000 kina, about £69 to £230) were set based on user experience research into farmers' credit needs.
- 99% of farmers interviewed gained access to a loan for the first time. Only two had a bank account before.
- Every farmer interviewed said they would recommend the service. They valued applying in their own village instead of travelling hours to town.
- Farmers used loans for tools, labour for pollinating and harvesting vanilla, small side businesses, school fees and medicine.

> "It helped me buy my new tools and expand my vanilla farm from 300 plants to 1,000 plants."
>
> Farmer quoted in GSMA's evaluation

## Reflection

The pilot evaluation taught me as much as the research did. Three lessons changed how I design credit.

**Repayment policy is a design decision.** We studied repayment against the harvest cycle. Yet the evaluation found farmers still struggled with a fixed due date that did not match when they were paid, and wanted a set repayment period from the day they took the loan. A rule like this decides whether a customer can repay. Today I would push for designers to be in the room when those rules are set, and I would test the terms with farmers before launch, not just the screens.

**Assisted journeys need a path to independence.** Farmers trusted the process because agents "did everything for us". But most did not feel confident applying alone. I would now design the assisted journey to teach as it goes, with simple step-by-step guides so a second loan is easier than the first.

**Insights must survive into delivery.** I left before the pilot, so I could not see which recommendations held. Next time I would agree with the team how we would check that the most important findings made it into the live product.

## Sources

- GSMA Mobile for Development, "Improving farmers' access to credit: A new GSMA partnership in Papua New Guinea", 15 January 2021
- GSMA Mobile for Development, "Smallholder loans pilot in Papua New Guinea: what did farmers have to say about the service and has it enhanced their access to finance?", 3 August 2023
