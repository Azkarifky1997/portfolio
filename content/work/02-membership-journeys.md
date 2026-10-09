---
title: Membership journeys for a UK professional body
slug: membership-journeys
summary: Redesigning how students and members join, qualify, upgrade and renew, so the website does the routine work and staff handle the exceptions.
card_role: Service and UX design
card_result: In build, with my functional specifications handed to the development team
thumbnail: membership-pathways.png
hero_image:
hero_alt:
hero_caption:
snapshot:
  Client: A UK professional body (anonymised)
  My role: Service and UX design: research, process mapping, wireframes and functional specifications
  Scope: Membership pathways (student, affiliate, associate, fellow), exam enrolment and exemptions, CRM data flows, notifications, renewals
  Methods: Workshops, interviews, shared working documents, reviews with CRM operators and developers, wireframes, functional specifications
  Status: In build, with my functional specifications handed to the development team
---

## The challenge

The organisation had four types of membership, and moving between them relied on manual work by staff and guesswork by members.

- **Pathways.** Students join by enrolling for an exam. Others join as affiliates and can upgrade to associate and then fellow, depending on experience and other criteria.
- **Exemptions were chosen by hand.** When enrolling for an exam, students picked their own exemptions while also choosing topics. Nothing linked their existing qualifications to the exemptions they were entitled to, even though much of that information was already on the CRM. Staff checked it all manually.
- **Members were confused.** Many did not understand which pathway they were on, why they were joining as one type of member rather than another, or what it meant for them.
- **Keeping members mattered.** The organisation wanted renewals to run smoothly, and to reach members before their membership lapsed.

The company I worked at was brought in to understand users better, streamline these digital journeys and design a new website.

![Membership pathway map: four membership levels, two ways in. On the exam route, people join at level 1, learner member, by enrolling for an exam. On the professional route, people join at level 2, entry-level member, then upgrade to level 3, experienced member, when experience criteria are met, and to level 4, senior member, when further experience and criteria are met.](membership-pathways.png "Four membership types, two ways in. Recreated and anonymised.")

## Approach

The answers sat across several teams and systems, so I worked in the open with all of them.

1. **Workshops and interviews** with the education and membership teams to understand each process, step by step.
2. **Shared working documents** that the teams reviewed and corrected, so the mapped processes reflected how work was really done.
3. **Reviews with CRM operators and developers** to find out what the systems could and could not do, such as where member data was stored, how it was uploaded and what could trigger an automatic notification.
4. **End-to-end flows** for each pathway, covering what the member sees, what happens in the CRM, how data moves between teams and how members are notified.
5. **Wireframes and functional specifications** detailing every flow, so developers could build from them directly.

## Key design decisions

### 1. Let the system work out exemptions

I designed an exemptions flow that uses qualifications already held on the CRM to identify which exemptions a student is entitled to, instead of asking them to choose from scratch. This removes a manual check for staff and a confusing decision for students.

**Trade-off:** the designs and flows were completed and delivered, but automated exemptions were taken out of the first build for scope reasons. The work is ready for a later phase.

![Before and after comparison of choosing exam exemptions. Before, manual selection and manual checks: the learner picks exemptions by hand while choosing topics, then staff check every request against qualifications, so every request reaches staff. After, suggested from existing records: the system suggests exemptions from CRM records, the learner confirms them, and staff review exceptions only, so only exceptions reach staff.](membership-before-after.png "Before and after: choosing exam exemptions. Recreated and anonymised.")

![Low-fidelity wireframe of a web form step titled Your exemptions. It says the exemptions were suggested from qualifications on the learner's record. Three exemptions are listed with tick boxes, each with a reason line such as Because you hold Qualification X. Below are a Request a different exemption link, noted as sent to the team for review, and a Continue button.](membership-wireframe.png "Low-fidelity wireframe of the exemptions step. Recreated and anonymised.")

### 2. Automate the routine, keep people for the exceptions

Not every case fits a rule. I designed the flows so straightforward cases are handled automatically, while unusual cases still go to a staff member to check. This kept the service safe without forcing staff to review everything.

![Service blueprint for exam enrolment with exemptions, with lanes for learner, website, CRM, education team and membership team. The learner starts enrolment, the website looks up qualifications held on the CRM and suggests eligible exemptions, and the learner confirms exemptions and chooses topics. If it is a standard case, it is approved automatically. If it is unusual, the education team does a staff check. The CRM record is then updated, the learner is notified, and the membership team sees the updated record.](membership-blueprint.png "Service blueprint: exam enrolment with exemptions. Recreated and anonymised.")

### 3. Reach members before they lapse

I designed renewal and lapse reminders, so members are prompted before their membership ends and the organisation has a better chance of keeping them.

![Timeline from membership active to renewal due to membership lapses, not to scale. Reminder 1 and reminder 2 are sent before renewal is due. A final reminder is sent after renewal is due and before the membership lapses.](membership-reminders.png "When members hear from us: renewal and lapse reminders. Recreated and anonymised.")

### 4. Specify the back stage as carefully as the front

For each journey, my functional specifications set out what happens behind the screen: where data goes in the CRM, how it is uploaded, which team acts on it and when the member is notified. This gave developers and the client a shared, buildable picture of the whole service.

## Where it stands

The new website is in build. My wireframes and functional specifications have been handed to the development team, who are building from them. As the project is ongoing, I have not shared screens or results here.

## Reflection

**Design the full version, then phase it.** Automated exemptions did not make the first build, but because the flows and logic are fully designed, the organisation can add them later without starting again. I now plan design work so the most valuable ideas survive a cut in scope.

**Explain the pathway, not just the form.** Members were confused about which membership was right for them and why. That was outside what I designed, but it is the next opportunity I would push for: helping people understand where they stand and what they need to progress, before they reach a form.

**Bring the people who build it in early.** Reviewing designs with CRM operators and developers as we went meant fewer surprises at handover. I would do this from day one on any project with complex systems behind it.
