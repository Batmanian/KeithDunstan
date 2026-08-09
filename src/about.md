---
layout: layouts/default.njk
title: About this site
summary: How this archive works, how to follow updates via RSS, how to reach Keith Dunstan's literary estate, and the numbers behind the collection.
---

<p class="lead">This site is a growing digital archive of the writing of Keith Dunstan (1925&ndash;2013), Australian journalist and author. It's maintained by his literary estate and volunteers, and new chapters and articles are added regularly.</p>

<hr>

<h2>A note on historical language</h2>
<p>This archive spans journalism and books written from the 1950s to the 1990s. Some of it reflects the attitudes, assumptions and language of the era in which it was written, including references to race, gender, sexuality, disability and other cultural groups that would not be considered acceptable in an inclusive society today.</p>
<p>Material is presented here unedited and in its original form, as a historical record of Keith Dunstan's work and of Australian society and journalism at the time. Its inclusion is not an endorsement of the views or language it contains.</p>

<hr>

<h2>Getting updates (RSS)</h2>
<p>The fastest way to know when something new is published, whether that's a newly transcribed Bulletin column or another chapter of a memoir, is to subscribe to the site's RSS feed rather than checking back manually.</p>
<p>The feed lives at <a href="{{ '/feed.xml' | url }}">{{ metadata.url }}/feed.xml</a>. To use it:</p>
<ol>
  <li>Pick a feed reader if you don't already have one &mdash; free options include <a href="https://feedly.com/news-reader">Feedly</a>, <a href="https://netnewswire.com">NetNewsWire</a> (Mac/iOS) and <a href="https://www.inoreader.com">Inoreader</a>.</li>
  <li>Paste <code>{{ metadata.url }}/feed.xml</code> into the reader's "add feed" or "subscribe" box.</li>
  <li>New book chapters and articles will then appear in your reader as they're published here, newest first.</li>
</ol>
<p><small><a href="{{ '/feed.xml' | url }}"><i class="fa fa-rss" aria-hidden="true"></i> Subscribe via RSS</a></small></p>

<hr>

<h2>Contact Keith's literary estate</h2>
<p>Copyright in Keith Dunstan's writing is held by his literary estate. If you have a permissions request, a correction, a suggestion, or material you think belongs in this archive, <a href="mailto:jack@dunsta.net?cc=daviddunstan@batmania.net&subject=Query%20regarding%20Keith%20Dunstan" title="jack@dunsta.net">please get in touch</a>.</p>
<p>See the <a href="{{ '/licence/' | url }}">licence and reuse</a> page for what you're free to do with this material without asking first.</p>
<p>Contributors to this site:</p>
<ul>
  <li><a href="https://batmania.net">David Dunstan</a></li>
  <li><a href="https://www.linkedin.com/in/jackdunstan/">Jack Dunstan</a></li>
</ul>

<hr>

<h2>This site, in numbers</h2>
<div class="row text-center g-4 my-2">
  <div class="col-12 col-md-4">
    <div class="border rounded p-4 h-100">
      <div class="h3 fw-bold text-nowrap">{{ siteStats.totalWordsFormatted }}</div>
      <div class="text-muted">words published</div>
    </div>
  </div>
  <div class="col-12 col-md-4">
    <div class="border rounded p-4 h-100">
      <div class="h3 fw-bold text-nowrap">{{ siteStats.totalReadTime }}</div>
      <div class="text-muted">to read the whole archive</div>
    </div>
  </div>
  <div class="col-12 col-md-4">
    <div class="border rounded p-4 h-100">
      <div class="h3 fw-bold text-nowrap">{{ siteStats.totalTopics }}</div>
      <div class="text-muted">topics indexed</div>
    </div>
  </div>
</div>
<p><small>Word count and reading time (at 200 words a minute) are drawn from every published book chapter and article; the topic count reflects the people, places and organisations catalogued on the <a href="{{ '/search/' | url }}">search and topics</a> page. All three update automatically as more of Keith's work is added.</small></p>
