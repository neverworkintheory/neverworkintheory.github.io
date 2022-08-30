---
layout: post
author: Greg Wilson
title: "Software Engineering Research Questions"
date: 2022-08-30
categories: ["Research Topics"]
---

*Cross-posted from [The Third Bit](https://third-bit.com/2022/08/30/research-topics/):*

I have been collecting random software engineering research ideas from friends and colleagues
for more than a decade.
These are the questions I've been asked since I started taking notes ten years ago.
I apologize for not keeping track of who wanted to know,
but if you're working on any of these,
please get in touch and I'll try to track them down.

1.  Does putting documentation in code (e.g., Python's docstrings) actually work better
    than keeping the documentation in separate files,
    and if so,
    by what measure(s)?

1.  Do [doctest](https://docs.python.org/3/library/doctest.html)-style tests
    (i.e., tests embedded directly in the code being tested)
    have any impact long-term usability or maintainability
    compared to putting tests in separate files?

1.  Which tasks do developers collaborate on most often
    and which do they do solo most often?
    (If I'm reading my handwriting correctly,
    the questioner hypothesized that programmers routinely do bug triage in groups,
    but usually write new code alone,
    with other tasks falling in between.)

1.  Are slideshows written using HTML- or Markdown-based tools more text-intensive
    than those written in PowerPoint?
    In particular,
    are slides written in formats that version control understands (text)
    less likely to use diagrams
    than slides written with GUI tools?

1.  A lot of [code metrics](https://neverworkintheory.org/category/#metrics)
    have been developed over the years;
    are there any for measuring/ranking the difficulty of getting software installed and configured?

1.  How does the percentage of effort devoted to tooling and deployment change
    as a project grows and/or ages?
    And how has it changed as we've moved from desktop applications to cloud-based applications?
    (Note: coming back to full-time coding after a decade away,
    my impression is that we've gone from packaging or building an installer taking 10% of effort
    to cloud deployment infrastructure being 25-30% of effort,
    but that's just one data point.)

1.  Has anyone developed a graphical notation for software development processes
    like [this one for game play](https://lostgarden.home.blog/2006/01/16/creating-a-system-of-game-play-notation/)?

1.  How do open source projects actually track and manage requirements or user needs?
    Do they use issues,
    is it done through discussion threads on email or chat,
    do people write wiki pages or [PEPs](https://peps.python.org/),
    etc.?

1.  Has anyone ever done a quantitative survey of programming books aimed at professionals
    (i.e., not textbooks)
    to find out what people in industry care enough to write about
    or think others care about?

1.  Has anyone ever done a quantitative survey of the data structures used in undergraduate textbooks
    for courses that *aren't* about data structures?
    I.e.,
    do we know what data structures students are shown
    in their "other" courses?

1.  Has anyone ever compared a list of things empirical software engineering research has "proven"
    (ranked by confidence)
    versus a list of things programmers believe (similarly ranked)?

1.  Has anyone ever done a quantitative survey of
    how many claims in the top 100 software development books are backed by citations,
    and of those,
    how many are still considered valid?

1.  Are there any metrics for code fitness that take process and team into account?
    (I actually have [the source](https://twitter.com/sarahmei/status/819256231869214721) for this one.)

1.  Which of the techniques catalogued in
    [*The Discussion Book*](https://www.wiley.com/en-us/The+Discussion+Book%3A+50+Great+Ways+to+Get+People+Talking-p-9781119049715)
    are programmers familiar with?
    Which ones do they use informally (i.e., without explicit tool support),
    and how do they operationalize them?

1.  Is there a graphical notation like UML to show the problems you're designing around
    or the special cases you've had to take into account
    rather than the finished solution to the problem
    (other than complete UML diagrams of the solutions you didn't implement)?

1.  Ditto for architectural evolution over time:
    is there an explicit notation for "here's how the system has changed",
    and if so,
    can it show multiple changes in a single diagram
    or is it just stepwise?

1.  The Turing Test classifies a machine as "intelligent"
    if an independent observer can't distinguish between it and a human being in conversation.
    Has anyone ever implemented a similar test for malicious software
    (which we should call the [Hoye Test](https://exple.tive.org/blarg/) in honor of the person who proposed it,
    or the [Moses Test](https://twitter.com/gvwilson/status/1159605481196937216) in "honor" of the person who inspired it):
    1.	Pick an application (e.g., Twitter).
    1.	Build a work-alike that is deliberately malicious in some way
    	(e.g., designed to radicalize its users).
    1.	Have people selected at random use both and then guess which is which.

1.  Has anyone ever summarized the topics covered
    by [ACM Doctoral Dissertation Award](https://awards.acm.org/doctoral-dissertation) winners
    to see what computer science is *actually* about?
    (A subject is defined by what it gives awards for…)

1.  Has anyone ever surveyed developers to find out what the most boring part of their job is?

1.  Is there data anywhere on speakers' fees at tech conferences
    broken down by by age, subject, gender, and geography?

1.  Are programmers with greenery or mini-gardens in the office happier and/or more productive
    than programmers with foosball tables?
    What about programmers working from home:
    does the presence of greenery and/or pets make a difference?

1.  How much do software engineering managers know about organizational behavior and/or social psychology?
    What mistruths and urban myths do they believe?

1.  Has anyone ever compared how long it takes to reach a workable level of understanding of a software system
    with and without UML diagrams or other graphical notations?
    More generally,
    is there any correlation between the amount or quality of different kinds of developer-oriented documentation
    and time-to-understanding,
    and if so,
    which kinds of documentation fare best?

1.  Is it possible to trace the genealogy of the slide decks used in undergrad software engineering classes
    (i.e., figure out who is adapting lessons originally written by whom)?
    If so,
    how does the material change over time?

1.  How do people physically organize coding lessons when using static site generators?
    For example,
    do they keep example programs in the same directory or subdirectory as the slides,
    or keep the slides in one place and the examples in another?
    And how do they handle incremental evolution of examples,
    where the first lesson builds a simple version of X,
    the next lesson changes some parts but leaves others alone,
    etc.?

1.  Has anyone ever applied security analysis techniques to emerging models of peer review
    to (for example) anticipate ways in which different kinds of open review might be gamed?

1.  Has anyone ever written a compare-and-contrast feature analysis
    of tools for building documentation and tutorials?
    For example,
    how do [Sphinx](https://www.sphinx-doc.org/),
    [Jekyll](https://jekyllrb.com/),
    and [roxygen](https://roxygen2.r-lib.org/) stack up?

1.  [Käfer et al's paper](https://programming-journal.org/2017/1/17/)
    comparing text and video tutorials for learning new software tools
    was interesting:
    has anyone done a follow-up?

1.  [Bjarnason et al's paper](https://ieeexplore.ieee.org/document/6619486) on retrospectives
    was interesting:
    has anyone looked in more detail at what developers discuss in retrospectives
    and (crucially) what impact that has?

1.  Has anyone studied adoption over time of changes (read: fixes) to Git's interface?
    For example, how widely is `git switch` actually now being used?
    And how do adopters find out about it?

1.  Same questions for adoption of new CSS features.

1.  Is ther any correlation between the length of a project's `README` file
    and how widely that software is used?
    If so, which drives which:
    does a more detailed `README` drive adoption
    or does adoption spur development of a more detailed `README`?

1.  Do any programming languages use one syntax for assigning an initial value to a variable
    and another syntax for updating that value,
    and if so,
    does distinguishing the two cases help?
    (Note: I think the person asking this question initially assumed that
    Python's new `:=` operator could only be used to assign an initial value.)

1.  How, when, and why do people move from one open source project to another?
    For example,
    do they tend to move from a project to one of its dependencies
    or one of the projects that depends on it?
    And do they tend to keep the same role in the new project
    or use the switch as an opportunity to change roles?

1.  How often do developers do performance profiling,
    what do they measure,
    and how do they measure it?

1.  Has anyone ever created some like [Sajaniemi's roles of variables](https://www.ppig.org/files/2005-PPIG-17th-sajaniemi.pdf)
    for refactoring steps or test cases?
    (Note: the person asking the question is a self-taught programmer
    who found [Gamma et al's book](https://www.pearson.com/en-us/subject-catalog/p/design-patterns-elements-of-reusable-object-oriented-software/P200000009480)
    a bit intimidating,
    and is looking for beginner-level patterns.)

1.  Has anyone defined a set of design patterns for the roles that columns play in dataframes
    during a data analysis?

1.  (How) does team size affect the proportion of time spent on planning and the accuracy of plans?

1.  Is there any way to detect altruism in software teams
    (i.e., how much time developer A spends helping developer B
    even though B's problem isn't officially A's concern)?
    If so,
    is there any correlation between altruism and
    (for example)
    staff turnover or the long-term maintainability of the code base?

1.  Is there any correlation between the quality of the error messages in a software system
    and the quality of the community?
    (Note: by "quality of the community",
    I believe the questioner meant things like "welcoming to newcomers"
    and "actually enforces its code of conduct".)

1.  If you collect data from a dozen projects
    and guess which ones think they're doing agile and which aren't,
    is there anything more than a weak correlation to
    what process team members tell you they think they're following?
    I.e.,
    are different development methodologies distinct rhetorically but not practically?

1.  What are students taught about debugging after their introductory courses?
    How much of what they're explicitly taught is domain-specific
    (e.g., "how to debug a graphics pipeline")?

1.  Can we assess students' proficiency with tools by watching screencasts of their work?
    And can we do it efficiently enough to make it a feasible way to grade how they code
    (as well as the code they write)?

1.  A lot of people have built computational notebooks based on text formats (like Markdown)
    or that run in the browser.
    Has anyone built a computational notebook starting with Microsoft Word or OpenOffice,
    i.e.,
    embedded runnable code chunks and their output in a rich document?

1.  When people write essay-length explanations about [error handling](https://beepb00p.xyz/mypy-error-handling.html)
    or [database internals](https://fly.io/blog/sqlite-internals-wal/),
    how do they decide what's worth explaining?
    Is it "I struggled to figure this out and want to save you the pain"
    or "I'm trying to build my reputation as an expert in this field"
    or something else?

1.  Has anyone done a study that plots when people get funded on a loose timeline of "building a startup"
    broken out by founders' characteristics?
    I.e.,
    if 0 is "I have an idea"
    and 100 is fully functioning company,
    where do most black/brown founders get funded vs. other poc founders vs. white founders?

1.  Has anyone analyzed videos of coding clubs for children or teens
    to see if girls are treated differently than boys by instructors
    and by their peers?

1.  How does the distribution of language constructs actually used in large programs vary by language?
    For example,
    if we plot percentage of programs that use feature X in a language,
    ordered by decreasing frequency,
    how do the curves for different languages compare?

1.  Is it possible to calculate something like a Gini coefficient to see how effectively scientists use computing?
    If so,
    is inequality static, decreasing, or increasing?
    (Note: the questioner felt strongly that
    the most proficient scientists are getting better at programming
    but the vast majority haven't budged in the last three decades,
    so the gap between "median" and "best" is actually widening.)

1.  If you train a Markov text generator on your software's documentation,
    generate some fake man pages,
    and give users a mix of real and fake pages,
    can they tell which are which?

1.  How does the number of (active) Slack channels in an organization grow as a function of time
    or of the number of employees?

1.  How well are software engineering researchers able to summarize each other's work
    based solely on the abstracts of their research papers,
    and how does that compare to researchers in other domains?

1.  Second-line tech support staff often spend a lot of time explaining how things work in general
    so that they can solve a specific problem.
    How do they tell how much detail they need to go into?

1.  Is there a notation like CSS selectors for selecting parts of a program to display in tutorials?
    (Note: I've used several systems that relied on specially-formatted comments
    to slice sections out of programs for display;
    the questioner was using one of these for the first time
    and wondering if there was something simpler, more robust, or more general.)

1.  How does the order in which people write code
    differ from the order in which they explain code in a tutorial and why?

1.  Has anyone built a computational notebook that presents a two-column display
    with the code on the left and commentary on the right?
    If so, how does that change what people do or how they do it?

1.  Is it possible to extract entity-relationship diagrams
    from programs that use Pandas or the tidyverse
    to show how dataframes are being combined
    (e.g., to infer foreign key relationships)?

1.  What percentage of time to developers spend debugging
    and how does that vary by the kind of code they're working on?

1.  At what point is it more economical to throw away a module and write a replacement
    instead of refactoring or extending the module to meet new needs?

1.  Are SQL statements written in execution order easier for novices to understand
    or less likely to be buggy
    than ones written in standard order?
    (Note: the questioner was learning SQL after learning to manipulate dataframes with the tidyverse,
    and found the out-of-order execution of SQL confusing
    after the in-order execution of tidyverse pipelines.)

1.  What error recovery techniques are used in what languages and applications how often?

1.  What labels do people define for GitHub issues and pull requests,
    and do they take those labels with them to new projects
    or re-think each project?

1.  Has anyone ever taught software engineering ethics by:
    1.	Creating a set of scenarios, each with multiple-choice options.
    1.	Having an ethics expert determine the best answer for each.
    1.	Then have students and professionals answer the same questions.
    1.	Analyzed the results to see how well each group matches the experts' opinions
    	and whether practitioners are any better than students.

1.  Has anyone ever studied students from the first year to the final year of their program
    to see what tools they actually start using when.
    In particular,
    when (if ever) do they start to use more advanced features of their IDE
    (e.g., "rename variable in scope")?

1.  Underrepresented groups often develop "whisper networks" to share essential knowledge
    (e.g., a young woman joining a company might be taken aside for an off-the-record chat
    by an older colleague and cautioned about the behavior of certain senior male colleagues).
    How have these networks changed during the COVID-19 lockdown?
