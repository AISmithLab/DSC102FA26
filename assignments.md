---
layout: assignments
title: Assignments
permalink: /assignments/
ai_resources: true
---

## Instructions and Caveats

{% include assignment_list.html %}

### Team composition

- You can work on the PAs in teams of between 1-3 individuals.
- Submit your team decision via a Google Form that we will provide before PA0’s release. One submission suffices per team.
- Team decisions cannot be changed.
- The TAs will then confirm your team memberships and team IDs.

### Academic integrity

- It is okay to discuss about the assignment with your peers at a conceptual level. It is also okay to post conceptual or high-level questions, logistical questions, and useful references on Slack. But do not share any code across teams and do not post any of your solution code for discussion on the public channels. A team’s code submission must be entirely their own.
- Please post conceptual questions on the public Slack channels for the benefit of all students.
- Do not go searching for any code posted online by other students or prior editions. We will use advanced program analysis tools to compare your code submissions. These go well beyond basic string or syntactic comparisons to catch plagiarism.
- If plagiarism is detected in your code or if any other form of academic integrity violation is identified, you will get zero for that component of your score and get downgraded substantially. I will also notify the University authorities for appropriate disciplinary action to be taken, up to and including expulsion from the University.
- There are no late days for the programming assignments. So, plan your work accordingly!

### AI interaction history

For each programming assignment in which your team uses AI, submit the complete interaction history from the AI tools you used. The history should include your prompts, the AI's responses, and the iterations that influenced your final solution. If your team does not use AI for an assignment, no AI interaction history is required. See the export instructions below.

## Export AI conversation history

[CLIcodeLog](https://github.com/monk1337/clicodelog) is an open-source tool for browsing conversations from Codex, Claude Code, and Gemini CLI in one interface. It organizes your locally saved sessions by project or working directory. Follow these steps to export and submit your session logs:

1. Follow the repository’s installation and setup instructions to install the latest source version.
2. Select your AI tool and search for your assignment’s project.
3. Open the sessions and inspect their logs to identify those relevant to the assignment.
4. Use the <strong style="color: #000;">Raw</strong> button (not Export!) to download each relevant session in JSON or JSONL format.
5. Submit the downloaded file. If there are multiple files, compress all relevant session files from your team into `session_log.zip` for submission.

<a href="{{ '/_images/screenshots/clicodelog-session-raw.jpg' | prepend: site.baseurl }}"><img src="{{ '/_images/screenshots/clicodelog-session-raw.jpg' | prepend: site.baseurl }}" alt="Full CLIcodeLog session view with the Raw download button highlighted in red" style="display: block; width: 100%; height: auto; margin: 1.5rem 0; border: 1px solid #ddd; border-radius: 6px;"></a>
