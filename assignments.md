---
layout: assignments
title: Assignments
permalink: /assignments/
ai_resources: true
---

## Instructions and Caveats

All assignment submissions must be made through Canvas.

{% include assignment_list.html %}

### Team composition

- You can work on the PAs in teams of between 1-3 individuals.
- Submit your team decision via a Google Form that we will provide before PA0’s release. One submission suffices per team.
- Team decisions cannot be changed.
- The TAs will then confirm your team memberships and team IDs.

### Academic integrity

- It is okay to discuss about the assignment with your peers at a conceptual level. It is also okay to post conceptual or high-level questions, logistical questions, and useful references on Piazza. But do not share any code across teams and do not post any of your solution code for discussion on the public channels. A team’s code submission must be entirely their own.
- Please post conceptual questions on the public Piazza for the benefit of all students.
- Do not go searching for any code posted online by other students or prior editions. We will use advanced program analysis tools to compare your code submissions. These go well beyond basic string or syntactic comparisons to catch plagiarism.
- If plagiarism is detected in your code or if any other form of academic integrity violation is identified, you will get zero for that component of your score and get downgraded substantially. I will also notify the University authorities for appropriate disciplinary action to be taken, up to and including expulsion from the University.
- There are no late days for the programming assignments. So, plan your work accordingly!

### AI interaction history

For each programming assignment in which your team uses AI, submit the complete interaction history from the AI tools you used. The history should include your prompts, the AI's responses, and the iterations that influenced your final solution. If your team does not use AI for an assignment, no AI interaction history is required. See the export instructions below.

## Export AI conversation history

[CLIcodeLog](https://github.com/AISmithLab/clicodelog) is an open-source tool for browsing conversations from Codex, Claude Code, Gemini CLI, Github Copilot and Cursor in one interface. It organizes your locally saved sessions by project or working directory. Follow these steps to export and submit your session logs:

1. Follow the repository’s installation and setup instructions to install the latest source version.
2. Select your AI tool and search for your assignment’s project.
3. Open the sessions and inspect their logs to identify those relevant to the assignment.
4. Use the <strong style="color: #000;">Raw</strong> button (not Export!) to download each relevant session in JSON or JSONL format.
5. Submit the downloaded file. If there are multiple files, compress all relevant session files from your team into `session_log.zip` for submission.

<a href="{{ '/_images/screenshots/clicodelog-session-raw.jpg' | prepend: site.baseurl }}"><img src="{{ '/_images/screenshots/clicodelog-session-raw.jpg' | prepend: site.baseurl }}" alt="Full CLIcodeLog session view with the Raw download button highlighted in red" style="display: block; width: 100%; height: auto; margin: 1.5rem 0; border: 1px solid #ddd; border-radius: 6px;"></a>

## Student presentations

You may volunteer to present your experience with the AI Coding Gym assignments during discussion and earn extra credit. Participation is completely optional, and extra credit applies only to the presenter(s). You can share what you tried, where the AI helped or struggled, and what you learned through the process.

We tentatively plan to discuss bug fixes (**PA0**) on **October 7 and 14**, using the remaining discussion time after the other PA tutorials. Presentations on the MLE challenges (**PA3/PA4**) are tentatively planned for **November 4 and 18**. If you have an AI workflow or personal experience to share beyond the assignments, you may volunteer to present it as well. Scheduling is flexible and depends on the time available in discussion.

Each presentation should focus on a small, coherent topic. We aim to cover diverse perspectives on how people work with AI and effective strategies for collaboration.

You can sign up to present through the [form](https://forms.gle/YLe6DLxHodm4xbpv9). Please indicate your topic and mark your available and preferred presentation times. Please choose a presentation option based on the scope of your topic and the time you need:

- **Lightning Talk:** 5 minutes.
- **Standard Talk:** 10 minutes.
- **Extended Talk:** 15 minutes or more, approved on a case-by-case basis.

Each presentation will be followed by 1–2 minutes of Q&A with the TA and audience. Slides are strongly encouraged but not required. Longer presentations should have enough substance to justify the time. These are especially encouraged for multiple presenters or an in-depth discussion of complex challenges. However, presentations are judged by quality, not length.

We will regularly review sign-ups, subject to available discussion time, and notify selected presenters **by 4 p.m. Pacific Time the day before the discussion**.

### Preparing your talk

Practice your talk in advance and stay within your time slot. Make your main takeaway clear. One clear lesson is better than five competing points. Consider what your classmates already know and explain any background they need. Start with concrete examples to make your main point easier to understand.

For practical advice on preparing and giving a talk, see Jonathan Shewchuk’s [Giving an Academic Talk (UC Berkeley)](https://people.eecs.berkeley.edu/~jrs/speaking.html) and Geoffrey Gordon’s [Advice for Technical Speaking (Carnegie Mellon)](https://www.cs.cmu.edu/~ggordon/speaking-advice.html).
