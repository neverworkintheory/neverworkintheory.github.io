---
layout: page
title: Contributing
permalink: /contributing/
---
<div align="center">
  <img src="https://imgs.xkcd.com/comics/clinical_trials.png" alt="XKCD cartoon on clinical trials" />
</div>

<ul>
  <li><a href="#guidelines">Guidelines</a></li>
  <li><a href="#academic">For Faculty and Students</a></li>
  <li><a href="#mechanics">How to Contribute</a></li>
  <li><a href="#methods">But Wait, There's More</a></li>
  <li><a href="#acknowledgments">Acknowledgments</a></li>
  <li><a href="#colophon">Colophon</a></li>
  <li><a href="#footnote">A Footnote on Comments</a></li>
</ul>

Contributions to this site are very welcome.
Our aim is to strengthen ties between research and practice,
so please write in the style of a popular science article
rather than in dry academic prose.
([This article](https://www.americanscientist.org/article/empirical-software-engineering)
from <em>American Scientist</em> is a good example.)
Our focus is software engineering,
with some ventures into software architecture and computing education.
We prefer that people do not review their own work (though we welcome reviews of adjacent work),
and the final decision on contributions will be made by [the current editor](mailto:{{site.author.url}});
we would be happy to talk with you about specifics and give feedback on drafts.

All contributors must abide by our [Code of Conduct]({{'/conduct/' | relative_url}}).
By submitting material to this site, you agree that we may publish it under the terms of
the [Creative Commons - Attribution License</a> (CC-BY)]({{'/license/' | relative_url}}).

<h2 id="guidelines">Guidelines</h2>

1. *Would you express your opinion so strongly if the paper had come to the opposite conclusion?
   For example, if it had found that doing X actually did improve code quality, or that Y *wasn't* better than Z, would you write the same way?
1. *Are you criticizing the paper's actual claims?*
   If it says that P holds for novices who are learning how to program, there is no point saying, "But no experienced programmer would do that!"
1. *Are your criticisms of the paper's statistics valid?*
   It's meaningless to say, "The paper's sample size is too small," without some quantification.
1. *Are you employing proof by rhetoric?*
   The statement, "It's obvious that J," is verbal bullying, not proof. And many "obvious" things aren't actually true: that's why we do studies.

<h2 id="academic">For Faculty and Students</h2>

We encourage faculty to have students write popular summaries of papers as graded work in courses and to submit them to this site.
To avoid ethical concerns, we recommend that:

1. Students be told that their work *can* be submitted,
   but that this is not a course requirement
   and that whether or not they do this will not affect their grade.
1. Students do not indicate whether or not they're going to submit their work to this site until *after* it has been graded.

If your institution or your legal jurisdiction requires submissions to be handled in some other way,
please [get in touch](mailto:{{site.author.email}});
we'd be happy to try to accommodate you.

<h2 id="mechanics">How to Contribute</h2>

1. Fork [this repository]({{site.repositoryurl}}) on GitHub.
1. Create a branch with a name like <code><em>author-year-short-title</em></code>, e.g., `wilson-2021-example-subject`.
   Please use the surname of the paper's first author as the <code><em>author</em></code> field and a four-digit year.
1. If your paper is already in `tex/todo.bib`, move the entry to `tex/nwit.bib`.
   If you have chosen another paper, please enter its DOI into <https://doi2bib.org/>
   and copy that BibTeX into `tex/nwit.bib`.
   Please remember to copy the paper's abstract into the `abstract` field.
1. Copy `./_template.html` to create <code>_posts/<em>YYYY</em>/<em>YYYY-MM-DD-short-title.html</em></code>,
   where <code><em>YYYY-MM-DD</em></code> is the date of your post (*not* the publication date of the paper)
   and <code><em>short-title</em></code> matches the short title of your branch (e.g., `example-subject`).
1. Fill in the HTML file (see below).
1. When you are done, create a pull request from your repository to [this one]({{site.repositoryurl}})
   and [email us]((mailto:{{site.author.email}}) to let us know your post is ready for review.
   Please also let us know what URL to use for you in the [acknowledgments](#acknowledgments).

When filling in the HTML template:

1. Replace *Your Name* with the name you would like to appear in the review.
   Please note that we do will only accept anonymous or pseudonymous reviews by prior agreement:
   [get in touch](mailto:{{site.author.email}}) if you want to do this.
1. Replace *Paper Title* with the paper's title (in double quotes).
1. Replace *YYYY-MM-DD* with the post's publication date (which should match the first part of your file's name).
1. Replace the list of categories with ones appropriate to your paper.
   Please use [existing categories]({{ '/category/' | relative_url }}) if you can rather than adding new ones.
1. Replace all occurrences of `BibliographyKey` with the BibTeX key of the paper you are reviewing
   and fill in the bibliographic details inside the paragraph block.
   We will reformat this for you if necessary when we merge your pull request.
1. Copy the full abstract of the paper into the `blockquote` below the citation.
   If the abstract is written as several paragraphs in the paper,
   please preserve that formatting.
1. Finally, write your review in the `div` below the abstract.

<h2 id="methods">But Wait, There's More</h2>

You (or your students) can also submit short explanations of the methods most commonly used in software engineering research,
with examples that use software engineering data—something like
[Statology's explanation of the Mann-Whitney test](https://statology.org/mann-whitney-u-test/) but with SE data,
or an explanation of similar length and depth of something like the card sorting used in many qualitative studies
(again, using data from software engineering or computing education studies).
Note that while we think the tidyverse is more approachable than Pandas for people new to programming,
computer scientists and software engineers are more likely to already know Python,
so we prefer it for code examples.
We can translate for you if necessary.

<h2 id="acknowledgments">Acknowledgments</h2>

Our entries have been written by:

- [Jorge Aranda](https://cuevano.ca/)
- [Neil Ernst](https://www.neilernst.net/)
- [Sakib Hasan](https://www.linkedin.com/in/sakib-hasan-071a05152/)
- [Felienne Hermans](https://www.felienne.com/)
- [Lorin Hochstein](http://lorinhochstein.org/)
- [Alexandru Ianta](https://github.com/aianta/)
- [Fayola Peters](https://lero.ie/lero-15/fayola-peters)
- [Eddie Antonio Santos](https://eddieantonio.ca/)
- [Leif Singer](https://leif.me/)
- [Andreas Stefik](http://web.cs.unlv.edu/stefika/)
- [Christoph Treude](https://ctreude.ca/)
- [Greg Wilson](https://third-bit.com/)
- [Donny Winston](https://donnywinston.com/)

We are also grateful to [Shashi Kumar](https://www.linkedin.com/in/shashi-kumar-371b2649/)
and [Bailey Harrington](https://github.com/baileythegreen)
for help with LaTeX.

<h2 id="colophon">Colophon</h2>

Our Jekyll theme is based on Dominic Elayda's [Celeste](https://github.com/nicoelayda/celeste).
We rely heavily on David Graf's [doi2bib.org](https://doi2bib.org),
the [Semantic Scholar API](https://www.semanticscholar.org/product/api),
and the work of [Alexandra Elbakyan](https://sci-hub.se/alexandra)
to find papers and obtain bibliography entries for them.
We use [Plausible Analytics](https://plausible.io/) to collect traffic statistics
without using cookies or any gathering personal identifying information:
please see [their website](https://plausible.io/privacy-focused-web-analytics) for details.

<h2 id="footnote">A Footnote on Comments</h2>

In the wake of Greg Wilson's posts on his personal blog about
[Shopify's support for white nationalists](https://third-bit.com/2018/05/06/cigarettes-and-shopify/)
and
[DataCamp's attempts to cover up sexual harassment](https://third-bit.com/2019/04/15/an-exchange-with-datacamp/)
we had to disable open comments on sites he contributes to.
Please [email us](mailto:{{site.author.email}}) if you'd like to add a comment on any of the posts on this site.
